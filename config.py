import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PROJECT_ID = os.getenv("PROJECT_ID")
    DATASET_ID = os.getenv("DATASET_ID")
    TABLE_NAME = os.getenv("TABLE_NAME")
    
    CRON_INTERVAL_SECONDS = int(os.getenv("CRON_INTERVAL_SECONDS", 2))

    @property
    def TABLE_FULL_PATH(self):
        return f"{self.PROJECT_ID}.{self.DATASET_ID}.{self.TABLE_NAME}"


settings = Config()