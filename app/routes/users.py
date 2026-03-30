# app/routes/users.py
from fastapi import APIRouter
from app.services.document_service import list_documents

router = APIRouter()


@router.get("/users/{user_id}/documents")
async def list_docs(user_id: str, page: int = 1, page_size: int = 10, status: str = None):
    return await list_documents(user_id, page, page_size, status)
