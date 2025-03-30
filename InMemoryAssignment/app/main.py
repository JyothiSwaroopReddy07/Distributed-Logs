from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from datetime import datetime, timedelta
import asyncio
import bisect

class LogEntry(BaseModel):
    timestamp: datetime
    level: str
    message: str
    source: str

app = FastAPI()

logs: List[LogEntry] = []
lock = asyncio.Lock()

def insert_sorted(entry: LogEntry):
    timestamps = [log.timestamp for log in logs]
    index = bisect.bisect(timestamps, entry.timestamp)
    logs.insert(index, entry)

def filter_logs(service: str, start: datetime, end: datetime) -> List[LogEntry]:
    return [
        log for log in logs
        if log.source == service and start <= log.timestamp <= end
    ]

@app.post("/logs")
async def create_log(entry: LogEntry):
    async with lock:
        await asyncio.to_thread(insert_sorted, entry)
    return {"status": "log stored in memory"}

@app.get("/logs")
async def get_logs(service: str, start: datetime, end: datetime):
    async with lock:
        results = await asyncio.to_thread(filter_logs, service, start, end)
    return results

@app.on_event("startup")
async def start_cleanup_task():
    async def cleaner():
        while True:
            await asyncio.sleep(60)  # Run every minute
            cutoff = datetime.utcnow() - timedelta(hours=1)
            async with lock:
                while logs and logs[0].timestamp < cutoff:
                    logs.pop(0)
    asyncio.create_task(cleaner())
