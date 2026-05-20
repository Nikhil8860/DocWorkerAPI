# app/routes/documents.py
from fastapi import APIRouter, HTTPException
from app.schemas import DocumentCreate
from app.services.document_service import create_document, get_document

router = APIRouter()


@router.post("/documents")
async def create(doc: DocumentCreate):
    try:
        return await create_document(doc)
    except Exception as e:
        if str(e) == "RATE_LIMIT":
            raise HTTPException(status_code=429, detail="Rate limit exceeded")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/documents/{doc_id}")
async def get(doc_id: str):
    doc = await get_document(doc_id)
    if not doc:
        raise HTTPException(404)
    return doc
