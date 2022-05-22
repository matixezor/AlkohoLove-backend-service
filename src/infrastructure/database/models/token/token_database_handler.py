from datetime import datetime
from pymongo.collection import Collection

from src.infrastructure.database.database_config import db


tokens_blacklist_collection: Collection = db.tokens_blacklist


class TokenBlacklistDatabaseHandler:
    @staticmethod
    async def add_token_to_blacklist(token_jti: str, expiration_date: datetime) -> None:
        tokens_blacklist_collection.insert_one({'token_jti': token_jti, 'expiration_date': expiration_date})

    @staticmethod
    async def check_if_token_is_blacklisted(token_jti: str) -> bool:
        return True if tokens_blacklist_collection.find_one({'token_jti': token_jti}) else False
