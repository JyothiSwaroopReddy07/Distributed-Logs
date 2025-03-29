from elasticsearch import Elasticsearch
import os
from datetime import datetime, timedelta

ES_HOST = os.getenv("ES_HOST", "http://localhost:9200")
es = Elasticsearch(ES_HOST)

INDEX_NAME = "logs-index"

def ensure_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body={
            "mappings": {
                "properties": {
                    "service_name": {"type": "keyword"},
                    "timestamp": {"type": "date"},
                    "message": {"type": "text"}
                }
            }
        })

def insert_log(doc):
    es.index(index=INDEX_NAME, document=doc)

def search_logs(service_name, start, end):
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"service_name": service_name}},
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
    res = es.search(index=INDEX_NAME, body=query)
    return [
        {
            "timestamp": hit["_source"]["timestamp"],
            "message": hit["_source"]["message"]
        }
        for hit in res["hits"]["hits"]
    ]

def delete_old_logs(days=60):
    cutoff = datetime.utcnow() - timedelta(days=60)
    query = {
        "query": {
            "range": {
                "timestamp": {
                    "lt": cutoff.isoformat()
                }
            }
        }
    }
    es.delete_by_query(index=INDEX_NAME, body=query)