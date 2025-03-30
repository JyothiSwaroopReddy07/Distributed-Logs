from fastapi import APIRouter
from datetime import datetime
import asyncio

from .models import LogEntry
from .storage import insert_sorted, filter_logs, logs

router = APIRouter()
lock = asyncio.Lock()

@router.post("/logs")
async def create_log(entry: LogEntry):
    async with lock:
        await asyncio.to_thread(insert_sorted, entry)
    return {"status": "log stored in memory"}

@router.get("/logs")
async def get_logs(service: str, start: datetime, end: datetime):
    async with lock:
        return await asyncio.to_thread(filter_logs, service, start, end)

def get_lock():
    return lock
