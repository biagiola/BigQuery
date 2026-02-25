from google.cloud import bigquery
from fastapi import HTTPException

client = bigquery.Client()

def get_accidentes():
    query = "SELECT sexo FROM `project-6c63eb79-eb66-49ad-b4d.example.accidentes`"
    try:
        query_job = client.query(query)
        return [dict(row) for row in query_job.result()]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def insert_test_accidentes():
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
        query_job.result()
        return query_job.num_dml_affected_rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"BigQuery Error: {str(e)}")