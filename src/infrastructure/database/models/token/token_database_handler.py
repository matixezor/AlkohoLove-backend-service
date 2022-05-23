from datetime import datetime
from pymongo.collection import Collection


class TokenBlacklistDatabaseHandler:
    @staticmethod
    async def add_token_to_blacklist(
        collection: Collection,
        token_jti: str,
        expiration_date: datetime
    ) -> None:
        collection.insert_one({'token_jti': token_jti, 'expiration_date': expiration_date})

    @staticmethod
    async def check_if_token_is_blacklisted(
        collection: Collection,
        token_jti: str
    ) -> bool:
        return True if collection.find_one({'token_jti': token_jti}) else False
