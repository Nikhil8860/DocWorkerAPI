# app/services/document_service.py
import random
import asyncio
from bson import ObjectId
from app.db import collection
from app.models import Status
from app.services.redis_service import r
from app.config import MAX_ACTIVE_JOBS, CACHE_TTL
from app.utils.hash import generate_hash


# Create Document
async def create_document(data):
    content_hash = generate_hash(data.content)
    # Check cache
    cached = await r.get(f"cache:{data.user_id}:{content_hash}")
    print("Cached values: ", cached)
    if cached:
        return {
            "status": Status.COMPLETED,
            "summary": cached
        }

    # Rate limiting
    active_jobs = await r.get(f"active:{data.user_id}") or 0
    print("Active Jobs: ", active_jobs)
    if int(active_jobs) >= MAX_ACTIVE_JOBS:
        raise Exception("RATE_LIMIT")

    await r.incr(f"active:{data.user_id}")

    doc = {
        "user_id": data.user_id,
        "title": data.title,
        "content": data.content,
        "content_hash": content_hash,
        "status": Status.QUEUED,
        "summary": None
    }

    result = await collection.insert_one(doc)
    return {"id": str(result.inserted_id), "status": Status.QUEUED}


# Get Document
async def get_document(doc_id):
    doc = await collection.find_one({"_id": ObjectId(doc_id)})
    if not doc:
        return None

    return {
        "id": str(doc["_id"]),
        "status": doc["status"],
        "summary": doc.get("summary")
    }


# List Documents
async def list_documents(user_id, page, page_size, status=None):
    query = {"user_id": user_id}
    if status:
        query["status"] = status

    cursor = collection.find(query).skip((page - 1) * page_size).limit(page_size)

    docs = []
    async for d in cursor:
        docs.append({
            "id": str(d["_id"]),
            "status": d["status"]
        })
    return docs
