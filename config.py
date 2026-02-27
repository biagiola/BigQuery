import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # These must match your .env keys exactly
    PROJECT_ID: str
    DATASET_ID: str
    TABLE_NAME: str
    
    # Defaults to 2 if not provided in .env
    CRON_INTERVAL_SECONDS: int = 2 

    # Tells Pydantic to read from the .env file
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def TABLE_FULL_PATH(self) -> str:
        return f"{self.PROJECT_ID}.{self.DATASET_ID}.{self.TABLE_NAME}"

# Create the instance once
settings = Settings()