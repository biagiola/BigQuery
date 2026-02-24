from fastapi import FastAPI, HTTPException
from google.cloud import bigquery
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
import logging
import os

client = bigquery.Client()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def my_cron_logic():
    logger.info("Cronjob executed: Logic from BigQuery or elsewhere running now...")

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()

    scheduler.add_job(my_cron_logic, "interval", seconds=2)
    scheduler.start()
    logger.info("🚀 Scheduler started...")
    
    yield
    
    scheduler.shutdown()
    logger.info("🛑 Scheduler shut down.")

app = FastAPI(lifespan=lifespan)

@app.get("/read-accidentes")
def select_accidentes_query():
    query = f"""
        SELECT sexo
        FROM `project-6c63eb79-eb66-49ad-b4d.example.accidentes`
    """

    try:
        query_job=client.query(query)
        results=query_job.result()

        ventas=[dict(row) for row in results]

        return ventas
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/insert-accidentes")
def insert_accidentes_query():
    # Your query is syntactically correct for BigQuery!
    query = """
        INSERT INTO `project-6c63eb79-eb66-49ad-b4d.example.accidentes` 
            (ID, Fecha, Hora, Ubicacion, Edad, Sexo, Fallecido, alcohol_positivo, tipo_vehiculo, departamento, ciudad)
        VALUES
            (1, '2026-01-01', '11:11:00', NULL, 32, 'F', 0, 1, 'Motocicleta', 'Central', 'Asuncion'),
            (2, '2026-01-01', '11:11:00', NULL, 21, 'M', 1, 0, 'Microbus', 'Concepcion', 'Concepcion'),
            (3, '2026-01-01', '11:11:00', NULL, 19, 'F', 0, 0, 'bicicleta', 'Caazapa', 'Fulgencio Yegros');
    """
    try:
        query_job = client.query(query)
        query_job.result()  # Wait for the insert to finish
        return {"status": "success", "rows_inserted": query_job.num_dml_affected_rows}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BigQuery Error: {str(e)}")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="project-6c63eb79-eb66-49ad-b4d.example.accidentes"
# We don't need to specify paths or keys; the google-cloud-bigquery library is smart enough to find the ADC file you just created.
# > gcloud init
# > gcloud auth application-default login# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="project-6c63eb79-eb66-49ad-b4d.example.accidentes"
# We don't need to specify paths or keys; the google-cloud-bigquery library is smart enough to find the ADC file you just created.
# > gcloud init
# > gcloud auth application-default login
