
# In-Memory Log Management System

A minimal, efficient, and concurrency-safe **log aggregation service** designed as per assignment constraints:

- In-memory log storage
- Thread-safe concurrent access
- Asynchronous I/O with concurrency
- Automatic TTL expiration (1 hour)
- Logs are always maintained in sorted order (by timestamp)
- Fast log querying over a time range

--- 


## 🚀 Features

### 🔐 Thread-Safe Log Insertion
- Uses `asyncio.Lock` to protect shared log list from race conditions
- Concurrent requests can safely add/query logs

Here’s the section formatted in proper `README.md` style:

---

### 🧮 Logs Sorted by Timestamp — Efficient and Always Ordered

This in-memory logging system **automatically maintains logs sorted by `timestamp`**, using Python’s built-in `bisect` module.

---

#### Why Keep Logs Sorted?

When logs are sorted on insert:
- No sorting required during read operations
- Range queries return logs in correct order
- Improves performance and efficiency

---

#### 🔧 How It Works

We use Python's `bisect` module to insert each log into the list at the correct position:

```python
import bisect

timestamps = [log.timestamp for log in logs]
index = bisect.bisect(timestamps, new_log.timestamp)
logs.insert(index, new_log)
```

- `timestamps`: Extracts all timestamps from the current list
- `bisect.bisect(...)`: Performs a **binary search** to find the correct insertion index
- `logs.insert(index, new_log)`: Inserts the log in place

This ensures the list remains **sorted at all times**.

---

#### Why This Approach Is Efficient

| Operation      | Complexity            | Notes                                             |
|----------------|------------------------|---------------------------------------------------|
| Insert         | `O(log n)` for index + `O(n)` insert | Very efficient for moderate log volume            |
| Query          | `O(k)` for `k` logs in range | No sort needed — already sorted!                |
| Memory         | Low                    | Pure Python list; no extra indexing overhead      |
| Concurrency    | Thread-safe with `asyncio.Lock()` | Prevents race conditions on write                 |

---

#### Benefits of `bisect`-based Ordering

- Maintains **natural chronological order**
- Avoids repeated sorting on each query
- Works well with **timestamp-based filtering**
- Scales well for in-memory use cases

This approach aligns perfectly with the assignment's emphasis on:
- In-memory storage  
- Efficient querying  
- Thread-safe access  
- Proper ordering without relying on databases or external systems



### 🧹 TTL (Time-To-Live) Cleanup
- Background task deletes logs older than **1 hour**
- Keeps memory usage lean

---

## Tech Stack

- Python 3.9+
- FastAPI (async backend)
- Uvicorn (ASGI server)

---

## Installation

```bash
git clone https://github.com/JyothiSwaroopReddy07/Distributed_Logs.git
cd InMemoryAssignment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## ▶Run the Server

```bash
uvicorn app.main:app --reload --port 8083
```

API will be available at:  
🔗 `http://localhost:8083`

---

## 📘 API Endpoints

### ➕ `POST /logs`

Add a new log.

**Payload:**
```json
{
  "timestamp": "2025-04-01T12:00:00Z",
  "level": "INFO",
  "message": "User login successful",
  "source": "api"
}
```

---

### 🔍 `GET /logs?start=...&end=...`

Fetch logs within a time range.

**Example:**
```
GET /logs?start=2025-04-01T10:00:00Z&end=2025-04-01T13:00:00Z
```

---

## 🧪 How It Works

### 1. **Logs are stored in a list** in memory
```python
logs: List[LogEntry] = []
```

### 2. **Logs inserted in sorted order** using:
```python
index = bisect.bisect([log.timestamp for log in logs], new_log.timestamp)
logs.insert(index, new_log)
```

### 3. **Concurrency-safe access** using `asyncio.Lock`:
```python
async with log_lock:
    # insert or read safely
```

### 4. **Cleaner task runs in background**:
```python
async def cleaner():
    while True:
        # remove logs older than 1 hour
        await asyncio.sleep(30)
```

---


## 📂 File Structure

```
app/
  └── main.py          # Core FastAPI app with insert/query/cleanup logic
requirements.txt       # All required Python packages
README.md              # This file
```

---

## 🔧 requirements.txt

```txt
fastapi==0.110.0
uvicorn==0.29.0
```

---

## 💬 Feedback

This project was built to demonstrate **clean code**, **async programming**, and **thread-safe design** under in-memory constraints.

