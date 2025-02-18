from pydantic import BaseSettings
import os

class Settings(BaseSettings):
    data_dir: str = os.environ.get('DATA_DIR')
    celery_broker_url: str = os.environ.get('BROKER_URL') #'redis://redis:6379/0'

settings = Settings()
