from bcrypt import gensalt
from datetime import datetime
from passlib.context import CryptContext
from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, select, update

from src.database.database_metadata import Base
from src.domain.user import UserCreate, UserUpdate


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_on = Column(TIMESTAMP, nullable=False)
    last_login = Column(TIMESTAMP)
    is_admin = Column(Boolean, default=False)
    is_banned = Column(Boolean, default=False)
    password_salt = Column(String, nullable=False)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserDatabaseHandler:
    @staticmethod
    def raise_user_already_exists(reason: str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User with given {reason} already exists'
        )

    @staticmethod
    def get_password_hash(password: str, salt: str) -> str:
        return pwd_context.hash(salt + password)

    @staticmethod
    def verify_password(password_raw: str, hashed_password: str) -> bool:
        return pwd_context.verify(password_raw, hashed_password)

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
        return await db.get(User, user_id)

    @staticmethod
    async def check_if_user_exists(db: AsyncSession, email: str, username: str) -> None:
        if await UserDatabaseHandler.get_user_by_email(db, email):
            UserDatabaseHandler.raise_user_already_exists('email')

        if await UserDatabaseHandler.get_user_by_username(db, username):
            UserDatabaseHandler.raise_user_already_exists('username')

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
        query = select(User).filter(User.email == email).limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> User | None:
        query = select(User).filter(User.username == username).limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def create_user(db: AsyncSession, user_create_payload: UserCreate) -> None:
        password_salt = gensalt().decode("utf-8")
        user_create_payload.password = UserDatabaseHandler.get_password_hash(
            user_create_payload.password,
            password_salt
        )

        db_user = User(
            **user_create_payload.dict(),
            created_on=datetime.now(),
            password_salt=password_salt
        )

        db.add(db_user)

    @staticmethod
    async def authenticate_user(db: AsyncSession, username: str, password: str) -> User:
        user = await UserDatabaseHandler.get_user_by_username(db, username)
        raw_password = user.password_salt + password
        if not user or not UserDatabaseHandler.verify_password(raw_password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'Invalid username or password'
            )
        return await UserDatabaseHandler\
            .update_user(db, user.user_id, UserUpdate(last_login=datetime.now()))

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_update_payload: UserUpdate) -> User:
        query = update(User)\
            .where(User.user_id == user_id)\
            .values(user_update_payload.dict(exclude_none=True))
        await db.execute(query)
        await db.commit()
        return await UserDatabaseHandler.get_user_by_id(db, user_id=user_id)
