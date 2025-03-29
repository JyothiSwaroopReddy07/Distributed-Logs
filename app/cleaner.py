import asyncio
from .es_client import delete_old_logs

async def cleaner_task():
    while True:
        await asyncio.sleep(86400)  # every 1 day
        delete_old_logs()
