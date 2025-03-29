# 🧠 Distributed Logs System with FastAPI + Kafka + Elasticsearch + Kibana

A robust and scalable logging pipeline using **FastAPI**, **Kafka**, **Elasticsearch**, and **Kibana**. This project allows you to:

- Ingest logs via a POST API
- Send logs to Kafka for decoupled processing
- Store logs in Elasticsearch for querying
- Visualize and explore logs in Kibana
- Simulate logs and test APIs using synthetic generators

---

## 📦 Tech Stack

- **FastAPI** – Web framework
- **Kafka** – Scalable log queue and message broker
- **Elasticsearch** – Log storage and search
- **Kibana** – Log dashboard
- **Python scripts** – For generating and fetching logs

---

## 🤖 Why Kafka + ELK?

Kafka acts as a buffer between the **API ingestion layer** and **Elasticsearch**, ensuring:

- **High throughput log ingestion** without overloading Elasticsearch
- **Fault tolerance**: logs won't be lost if Elasticsearch is down temporarily
- **Decoupling** of log ingestion and storage layers
- **Scalability**: multiple consumers can process the logs in parallel

Together, Kafka + ELK ensures your system remains **resilient, performant, and horizontally scalable**.

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/distributed-logs.git
cd distributed-logs
```

---

## ⚙️ Setting Up Kafka, Elasticsearch & Kibana (Docker)

### 📁 `docker-compose.yml`

```yaml
version: '3.8'

services:
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
    ports:
      - "2181:2181"

  kafka:
    image: confluentinc/cp-kafka:latest
    depends_on:
      - zookeeper
    environment:
      KAFKA_BROKER_ID: 1
      KAFKA_ZOOKEEPER_CONNECT: zookeeper:2181
      KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://localhost:9092
      KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR: 1
    ports:
      - "9092:9092"

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

### 🏁 Start All Services

```bash
docker-compose up -d
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

### 4. Start the Kafka consumer (in a new terminal):

```bash
python -m app.kafka_consumer
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
🔽️ main.py            # FastAPI app with routes
🔽️ models.py          # LogEntry schema
🔽️ es_client.py       # Elasticsearch query/insert functions
🔽️ kafka_producer.py  # Kafka producer logic
🔽️ kafka_consumer.py  # Kafka consumer that pushes logs to ES
🔽️ cleaner.py         # Background log cleaner
log_generator.py       # Sends synthetic logs
log_fetcher.py         # Fetches logs with random queries
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

---

## 🧰 Log Fetcher (Query Tester)

### 📄 `log_fetcher.py`

Sends random GET requests to fetch logs from the `/logs` endpoint.

#### Usage:

```bash
python log_fetcher.py
```

---

## 🗜️ Cleaner Task

A background task that deletes logs older than 60 days, automatically launched during FastAPI startup.

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

## 📸 Resultant Screenshots

![alt text](<public/Screenshot 2025-03-28 at 5.43.44 PM.png>) 
![alt text](<public/Screenshot 2025-03-28 at 5.44.24 PM.png>) 
![alt text](<public/Screenshot 2025-03-28 at 5.44.51 PM.png>) 
![alt text](<public/Screenshot 2025-03-28 at 5.45.29 PM.png>) 
![alt text](<public/Screenshot 2025-03-28 at 5.45.53 PM.png>)
![alt text](<public/Screenshot 2025-03-28 at 5.52.43 PM.png>)

### Kafka Producer
![alt text](<public/Screenshot 2025-03-29 at 9.42.11 AM.png>)

### Kafka Consumer
![alt text](<public/Screenshot 2025-03-29 at 9.42.21 AM.png>)