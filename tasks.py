import logging

logger = logging.getLogger(__name__)

def request_new_data():
    # Make external API calls to update database
    logger.info("Cronjob executed: Requesting new data...")

async def request_new_data():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.external.com/data", timeout=10.0)
            response.raise_for_status() # Raises exception for 4xx or 5xx
            return response.json()
    
    except httpx.HTTPStatusError as e:
        logger.error(f"External API Error: {e.response.status_code}")
        raise HTTPException(status_code=502, detail="External provider is down.")
    
    except httpx.RequestError:
        logger.error("External API Timeout/Network Error")
        raise HTTPException(status_code=504, detail="External provider timed out.")


async def insert_new_data():
    # Insert new data into the database
    logger.info("Cronjob executed: Inserting new data...")