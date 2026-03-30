# app/services/redis_service.py
import redis.asyncio as redis
from app.config import REDIS_URL

r = redis.from_url(REDIS_URL, decode_responses=True)
