# app/main.py
from fastapi import FastAPI
import asyncio
from app.routes import documents, users
from app.services.worker import worker

app = FastAPI()

app.include_router(documents.router)
app.include_router(users.router)


@app.on_event("startup")
async def start_worker():
    asyncio.create_task(worker())


@app.get("/health")
async def health():
    return {"status": "ok"}
