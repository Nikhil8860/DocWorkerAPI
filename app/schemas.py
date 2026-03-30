# app/schemas.py
from pydantic import BaseModel

class DocumentCreate(BaseModel):
    user_id: str
    title: str
    content: str

class DocumentResponse(BaseModel):
    id: str
    status: str
    summary: str | None = None