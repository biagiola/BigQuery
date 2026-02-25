import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import database
import tasks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(tasks.my_cron_logic, "interval", seconds=2)
    scheduler.start()
    logger.info("Scheduler started...")
    yield
    scheduler.shutdown()
    logger.info("Scheduler shut down.")

app = FastAPI(lifespan=lifespan)

@app.get("/read-accidentes")
def read_accidentes():
    return database.get_accidentes()

@app.post("/insert-accidentes")
def insert_accidentes():
    rows = database.insert_test_accidentes()
    return {"status": "success", "rows_inserted": rows}

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}