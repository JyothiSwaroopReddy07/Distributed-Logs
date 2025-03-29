from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from datetime import datetime
import asyncio
from elasticsearch import Elasticsearch

from app.models import LogEntry
from app.es_client import insert_log, search_logs, ensure_index
from app.cleaner import cleaner_task

INDEX_NAME = "logs"
es = Elasticsearch("http://localhost:9200")
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
    print(entry)
    doc = entry.dict()
    es.index(index=INDEX_NAME, document=doc)
    return {"status": "log stored"}

@app.get("/logs")
def search_logs(service, start, end):
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
        }
    }

    response = es.search(index="logs", body=query)
    return [hit["_source"] for hit in response["hits"]["hits"]]

