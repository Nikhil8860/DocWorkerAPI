# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()


def get_env(key: str, default=None, required: bool = True, cast_type=str):
    value = os.getenv(key, default)

    if required and value is None:
        raise ValueError(f"Missing required environment variable: {key}")

    try:
        return cast_type(value) if value is not None else value
    except Exception:
        raise ValueError(f"Invalid value for {key}, expected {cast_type.__name__}")


# Core configs
MONGO_URL: str = get_env("MONGO_URL")
REDIS_URL: str = get_env("REDIS_URL")

# Proper type casting
MAX_ACTIVE_JOBS = get_env("MAX_ACTIVE_JOBS", cast_type=int)
CACHE_TTL = get_env("CACHE_TTL", cast_type=int)

# DB config
DB_NAME = os.getenv("DB_NAME", "doc_insights")
COLLECTION = os.getenv("COLLECTION", "documents")


# Debug logs (safe)
print("Config Loaded:")
print("MONGO_URL:", MONGO_URL)
print("REDIS_URL:", REDIS_URL)
print("MAX_ACTIVE_JOBS:", MAX_ACTIVE_JOBS)
print("CACHE_TTL:", CACHE_TTL)
