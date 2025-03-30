import asyncio
from fastapi import FastAPI
from app.routes import router, get_lock
from app.cleaner import cleaner_task

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup():
    lock = get_lock()
    asyncio.create_task(cleaner_task(lock))
