from pymongo import MongoClient
from pymongo.database import Database

from src.infrastructure.config.app_config import get_settings

client = MongoClient(get_settings().DATABASE_URL)
db: Database = client.alkoholove


def get_db():
    return db
