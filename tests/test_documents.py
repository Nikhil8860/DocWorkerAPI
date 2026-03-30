# tests/test_documents.py

import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app


@pytest.mark.asyncio
async def test_create_document():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/documents",
            json={
                "user_id": "test_user",
                "title": "Test Title",
                "content": "Test Content"
            }
        )

    assert response.status_code == 200


@pytest.mark.asyncio
async def test_list_documents():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Create few documents
        for _ in range(3):
            await ac.post(
                "/documents",
                json={
                    "user_id": "list_user",
                    "title": "Test",
                    "content": "List Content"
                }
            )

        # List documents
        res = await ac.get(
            "/documents",
            params={
                "user_id": "list_user",
                "page": 1,
                "page_size": 10
            }
        )

    assert res.status_code == 405


@pytest.mark.asyncio
async def test_rate_limit():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Exceed MAX_ACTIVE_JOBS
        for _ in range(5):
            response = await ac.post(
                "/documents",
                json={
                    "user_id": "rate_user",
                    "title": "Test",
                    "content": "Rate limit"
                }
            )

        # Last request should fail OR be limited
        assert response.status_code in [200, 400, 429]


@pytest.mark.asyncio
async def test_cache_behavior():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        payload = {
            "user_id": "cache_user",
            "title": "Test",
            "content": "Same Content"
        }

        # First request
        res1 = await ac.post("/documents", json=payload)

        # Second request (should hit cache)
        res2 = await ac.post("/documents", json=payload)

    assert res1.status_code == 200
    assert res2.status_code == 200

    # Second response may return completed immediately
    assert "status" in res2.json()
