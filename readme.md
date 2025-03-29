# 🧠 Distributed Logs System with FastAPI + Elasticsearch + Kibana

A simple yet powerful logging pipeline using **FastAPI**, **Elasticsearch**, and **Kibana**. This project allows you to:

- Ingest logs via a POST API
- Store them in Elasticsearch
- Visualize and explore them in Kibana
- Simulate logs and test APIs using synthetic generators

---

## 📦 Tech Stack

- **FastAPI** – Web framework
- **Elasticsearch** – Log storage and search
- **Kibana** – Log dashboard
- **Python scripts** – For generating and fetching logs

---


## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/distributed-logs.git
cd distributed-logs
```

---

## ⚙️ Setting Up Elasticsearch & Kibana (Docker)

### 📁 Create `docker-compose.yml`

```yaml
version: '3.8'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.17.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - ES_JAVA_OPTS=-Xms512m -Xmx512m
    ports:
      - "9200:9200"

  kibana:
    image: docker.elastic.co/kibana/kibana:7.17.0
    container_name: kibana
    ports:
      - "5601:5601"
    depends_on:
      - elasticsearch
```

### 🏁 Start Elasticsearch & Kibana

```bash
docker-compose up
```

---

## 🌐 Running the FastAPI Server

### 1. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Start the FastAPI server:

```bash
uvicorn app.main:app --reload --port 8001
```

The API will be available at:  
📍 http://localhost:8001

---

## 🔐 Kibana Dashboard Setup

1. Go to: [http://localhost:5601](http://localhost:5601)
2. Navigate to **"Discover"**
3. Click **"Create Index Pattern"**
4. Use `logs*` as index pattern
5. Select `timestamp` as the time filter
6. Create and explore logs!

---

## 💠 Project Structure

```
app/
🔽️ main.py          # FastAPI app with routes
🔽️ models.py        # LogEntry schema
🔽️ es_client.py     # Elasticsearch query/insert functions
🔽️ cleaner.py       # Background task (optional)
log_generator.py     # Sends synthetic logs
log_fetcher.py       # Fetches logs with random queries
requirements.txt
docker-compose.yml
README.md
```

---

## 🧪 Synthetic Log Generator

### 📄 `log_generator.py`

Generates and POSTs logs to the `/logs` endpoint.

#### Usage:

```bash
python log_generator.py
```

- Sends 100 logs by default
- Each log includes random timestamp, level, message, and source

---

## 🧰 Log Fetcher (Query Tester)

### 📄 `log_fetcher.py`

Sends random GET requests to fetch logs from the `/logs` endpoint.

#### Usage:

```bash
python log_fetcher.py
```

- Makes 20 random queries across services and date ranges
- Helps test retrieval and API accuracy

---

## 🗜️ Cleaner Task (Optional)

- You can write a background task (`cleaner.py`) to remove old logs or do rolling archival.
- Hooked into FastAPI `startup()`.

---

## 🧠 Sample Log Format

```json
{
  "timestamp": "2025-03-28T10:00:00",
  "level": "INFO",
  "message": "User logged in",
  "source": "api-gateway"
}
```

---

## ✅ Sample API Endpoints

### ➕ POST `/logs`

Add a log entry.

```json
POST /logs
Content-Type: application/json

{
  "timestamp": "2025-03-28T10:00:00",
  "level": "ERROR",
  "message": "Something failed",
  "source": "auth-service"
}
```

### 🔍 GET `/logs`

Query logs by source and time range:

```http
GET /logs?service=backend&start=2025-03-20T00:00:00&end=2025-03-28T00:00:00
```

---

## Resultant ScreenShots

![alt text](<public/Screenshot 2025-03-28 at 5.43.44 PM.png>) 
![alt text](<public/Screenshot 2025-03-28 at 5.44.24 PM.png>) 
![alt text](<public/Screenshot 2025-03-28 at 5.44.51 PM.png>) 
![alt text](<public/Screenshot 2025-03-28 at 5.45.29 PM.png>) 
![alt text](<public/Screenshot 2025-03-28 at 5.45.53 PM.png>)
![alt text](<public/Screenshot 2025-03-28 at 5.52.43 PM.png>)