import asyncio
from datetime import datetime, timedelta
from .storage import logs

async def cleaner_task(lock):
    while True:
        await asyncio.sleep(60)
        cutoff = datetime.utcnow() - timedelta(hours=1)
        async with lock:
            while logs and logs[0].timestamp < cutoff:
                logs.pop(0)
