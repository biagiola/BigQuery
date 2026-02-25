import logging

logger = logging.getLogger(__name__)

def my_cron_logic():
    # Make external API calls to update database
    logger.info("Cronjob executed: Logic from BigQuery...")