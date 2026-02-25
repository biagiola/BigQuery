import logging
from fastapi import FastAPI
from config import settings

import database
import tasks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/update-database")
def update_database():
    # make the request to the external API and update the database
    tasks.request_new_data()
    tasks.insert_new_data()
    logger.info("Database updated successfully")

    return {"status": "success", "message": "Database updated successfully"}

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