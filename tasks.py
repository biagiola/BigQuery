import logging

logger = logging.getLogger(__name__)

def request_new_data():
    # Make external API calls to update database
    logger.info("Cronjob executed: Requesting new data...")

def insert_new_data():
    # Insert new data into the database
    logger.info("Cronjob executed: Inserting new data...")