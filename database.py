import os
from config import settings
from google.cloud import bigquery
from google.api_core import retry
from fastapi import HTTPException
from dotenv import load_dotenv

# Configure a custom retry strategy for BigQuery
# This will automatically retry on 500, 503 errors or network timeouts
custom_retry = retry.Retry(
    initial=1.0,  # First retry after 1 second
    maximum=10.0, # Cap retry delay at 10 seconds
    multiplier=2.0,
    deadline=60.0 # Total time to keep trying
)

# client = bigquery.Client()
client = bigquery.Client(project=settings.PROJECT_ID)

def get_accidentes():
    query = f"SELECT sexo FROM `{settings.TABLE_FULL_PATH}`"
    try:
        # Use 'timeout' to prevent the request from hanging forever
        # Use 'retry' to handle transient network blips
        query_job = client.query(query, timeout=30, retry=custom_retry)
        
        # result() is where the permission check actually happens
        rows = query_job.result() 
        return [dict(row) for row in rows]

    except Exception as e:
        logger.error(f"BigQuery Query Failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"BigQuery Error: {str(e)}")

def insert_test_accidentes():
    query = """
        INSERT INTO `{settings.TABLE_FULL_PATH}` 
        (ID, Fecha, Hora, Ubicacion, Edad, Sexo, Fallecido, alcohol_positivo, tipo_vehiculo, departamento, ciudad)
        VALUES
        (1, '2026-01-01', '11:11:00', NULL, 32, 'F', 0, 1, 'Motocicleta', 'Central', 'Asuncion'),
        (2, '2026-01-01', '11:11:00', NULL, 21, 'M', 1, 0, 'Microbus', 'Concepcion', 'Concepcion'),
        (3, '2026-01-01', '11:11:00', NULL, 19, 'F', 0, 0, 'bicicleta', 'Caazapa', 'Fulgencio Yegros');
    """
    try:
        query_job = client.query(query)
        query_job.result()
        return query_job.num_dml_affected_rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BigQuery Error: {str(e)}")