from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, String, TIMESTAMP

from src.database.database_metadata import Base


class TokenBlacklist(Base):
    __tablename__ = 'token_blacklist'

    token_jti = Column(String, primary_key=True, index=True)
    expiration_date = Column(TIMESTAMP, nullable=False)


class TokenBlacklistDatabaseHandler:
    @staticmethod
    async def add_token_to_blacklist(db: AsyncSession, token_jti: str, expiration_date: datetime) -> None:
        db_token = TokenBlacklist(token_jti=token_jti, expiration_date=expiration_date)
        db.add(db_token)

    @staticmethod
    async def check_if_token_is_blacklisted(db: AsyncSession, token_jti: str) -> bool:
        db_token = await db.get(TokenBlacklist, token_jti)
        return True if db_token else False
