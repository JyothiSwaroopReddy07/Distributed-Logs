from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import asyncio
from elasticsearch import Elasticsearch
from concurrent.futures import ThreadPoolExecutor
import redis
import hashlib
import json

from app.models import LogEntry
from app.es_client import insert_log, search_logs, ensure_index
from app.cleaner import cleaner_task
from app.kafka_producer import send_log_to_kafka

import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost") 


INDEX_NAME = "logs-index"
es = Elasticsearch("http://localhost:9200")
executor = ThreadPoolExecutor(max_workers=10)
redis_client = redis.Redis(host=REDIS_HOST, port=6379, db=0, decode_responses=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await asyncio.to_thread(ensure_index)
    asyncio.create_task(cleaner_task())

@app.post("/logs")
def create_log(entry: LogEntry):
    send_log_to_kafka(entry.dict())
    return {"status": "log sent to Kafka"}

@app.get("/logs")
async def search_logs(service: str, start: datetime, end: datetime):
    key_raw = f"{service}:{start.isoformat()}:{end.isoformat()}"
    cache_key = hashlib.sha256(key_raw.encode()).hexdigest()

    def fetch_or_cache():
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)

        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"source": service}}, 
                        {
                            "range": {
                                "timestamp": {
                                    "gte": start,
                                    "lte": end
                                }
                            }
                        }
                    ]
                }
            },
            "sort": [{"timestamp": {"order": "asc"}}]
        }

        response = es.search(index="logs-index", body=query)
        results = [hit["_source"] for hit in response["hits"]["hits"]]
        redis_client.setex(cache_key, 120, json.dumps(results))  # Cache for 2 minutes
        return results

    return await asyncio.get_event_loop().run_in_executor(executor, fetch_or_cache)
