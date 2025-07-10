from pydantic_settings import BaseSettings
from datetime import timezone

class APISettings(BaseSettings):
    TIME_ZONE: timezone = timezone.utc
    APP_VERSION: str ="1.0.0"
    APP_NAME: str ="Job Tracker"

class DatabaseSettings(BaseSettings):
    MONGO_URL: str
    MONGO_INITDB_DATABASE: str

    class Config:
        env_file = ".env"
        extra = "ignore"
        
        
def get_settings():
    return DatabaseSettings()


