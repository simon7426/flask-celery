import os
from pathlib import Path

class BaseConfig:
    BASE_DIR = Path(__file__).parent.parent
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL",f"sqlite:///{BASE_DIR}/db.sqlite3")
    
    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0")

    SECRET_KEY = os.environ.get('SECRET_KEY','my_precious')
    
class DevelopmentConfig(BaseConfig):
    DEBUG = True

class ProductionConfig(BaseConfig):
    DEBUG = False

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
