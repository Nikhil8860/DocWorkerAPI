# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
REDIS_URL = os.getenv("REDIS_URL")

print("MONGO URL: ", MONGO_URL)
print("REDIS_URL: ", REDIS_URL)
DB_NAME = "doc_insights"
COLLECTION = "documents"

MAX_ACTIVE_JOBS = 3
CACHE_TTL = 3600
