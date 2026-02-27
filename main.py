import logging
from config import settings
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

import database
import tasks

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure FastAPI app
app = FastAPI()

# Configure global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # Log the full traceback to Cloud Logging
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred.", "type": type(exc).__name__}
    )


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
    return {"message": "Server is running!"}