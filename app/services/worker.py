import asyncio
import random
from pymongo import ReturnDocument
from app.db import collection
from app.services.redis_service import r


async def worker():
    while True:
        try:
            print("Trying to fetch queued Jobs")
            # Atomic fetch + update
            doc = await collection.find_one_and_update(
                {"status": "queued"},
                {"$set": {"status": "processing"}},
                return_document=ReturnDocument.AFTER
            )
            print("QUEUED JOBS: ", doc)
            if not doc:
                await asyncio.sleep(2)
                continue

            doc_id = doc["_id"]
            user_id = doc["user_id"]
            content = doc["content"]
            content_hash = doc["content_hash"]

            try:
                # Simulate processing
                await asyncio.sleep(random.randint(10, 30))

                # 10% failure simulation
                if random.random() < 0.1:
                    raise Exception("Simulated failure")

                # Mock summary
                summary = content[:100]

                # Update DB
                await collection.update_one(
                    {"_id": doc_id},
                    {
                        "$set": {
                            "status": "completed",
                            "summary": summary
                        }
                    }
                )

                # Cache result in Redis
                await r.set(
                    f"cache:{user_id}:{content_hash}",
                    summary,
                    ex=3600
                )

            except Exception as process_error:
                print("Processing error:", process_error)

                await collection.update_one(
                    {"_id": doc_id},
                    {"$set": {"status": "failed"}}
                )

            finally:
                # Decrease active job count
                await r.decr(f"active:{user_id}")

        except Exception as e:
            print("Worker error:", e)
            await asyncio.sleep(5)
