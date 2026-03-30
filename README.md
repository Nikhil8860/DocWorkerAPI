# Document Processing System (FastAPI + MongoDB + Redis)

A backend system that allows users to submit documents for asynchronous processing, with rate limiting, caching, and worker-based execution.

---

## Features

* Submit documents for processing
* Asynchronous background worker
* MongoDB for persistence
* Redis for caching & rate limiting
* Idempotency using content hashing
* Pagination & filtering support
* Fault-tolerant worker (retry-ready)

---

## Tech Stack

* **Backend:** FastAPI
* **Database:** MongoDB
* **Cache & Queue:** Redis
* **Async Driver:** Motor
* **Environment Config:** python-dotenv

---

## Project Structure

```
app/
│── main.py
│── config.py
│── db.py
│
├── routes/
│   └── document.py
|   └── users.py
│
├── services/
│   ├── document_service.py
│   ├── redis_service.py
│   └── worker.py
│
└── utils/
    └── hash.py
```

---

## ⚙️ Setup Instructions

### Clone Repository

```bash
git clone <your-repo-url>
cd <project-folder>
```

---

### Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Setup Environment Variables

Create a `.env` file:

```env
MONGO_URL=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379
MAX_ACTIVE_JOBS=3
CACHE_TTL=300
```

---

## Running Services

### Start MongoDB

```bash
mongod
```

---

### Start Redis (Docker Recommended)

```bash
docker run -d -p 6379:6379 --name redis redis
```

---

### Run FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

### Run Worker (Important)

```bash
python -m app.services.worker
```

---

## API Endpoints

### Create Document

```
POST /documents
```

**Request Body:**

```json
{
  "user_id": "user123",
  "title": "Sample Doc",
  "content": "Some text..."
}
```

---

### ➤ Get Document

```
GET /documents/{id}
```

---

### ➤ List Documents

```
GET /documents?user_id=user123&page=1&page_size=10&status=completed
```

---

## How It Works

1. User submits a document
2. System checks:

   * Cache (Redis)
   * Rate limit (Redis)
3. Document stored in MongoDB with `queued` status
4. Worker picks document and processes it
5. Result stored + cached
6. Status updated to `completed`

---

## Worker Logic

* Polls MongoDB for `queued` jobs
* Updates status → `processing`
* Processes document
* Saves result → MongoDB + Redis cache
* Handles failures gracefully

---

## Key Concepts

### Rate Limiting

* Limits active jobs per user via Redis

### Caching

* Avoids recomputation for same content

---

## Common Issues

### MongoDB not connecting

* Ensure:

  ```
  MONGO_URL=mongodb://localhost:27017
  ```

---

### Redis connection error

* Start Redis:

  ```bash
  docker run -d -p 6379:6379 redis
  ```

---

### Documents stuck in "processing"

* Worker crashed
* Reset manually:

  ```js
  db.documents.updateMany(
    { status: "processing" },
    { $set: { status: "queued" } }
  )
  ```

---

## Testing Flow

1. Start all services
2. POST `/documents`
3. Wait few seconds
4. GET `/documents/{id}`
5. Status should be `completed`


---

## Author

**Nikhil Kumar**

---

## Notes

This project demonstrates:

* Async backend design
* Distributed system basics
* Queue + worker architecture
* Production-ready coding practices

---
