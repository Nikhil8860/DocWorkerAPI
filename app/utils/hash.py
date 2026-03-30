# app/utils/hash.py
import hashlib


def generate_hash(content: str) -> str:
    return hashlib.sha256(content.encode()).hexdigest()
