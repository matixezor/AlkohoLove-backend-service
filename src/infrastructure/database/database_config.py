from pymongo import MongoClient
from pymongo.database import Database

from src.infrastructure.config.app_config import DATABASE_URL


client = MongoClient(DATABASE_URL)
db: Database = client.alkoholove


def get_db():
    return db
