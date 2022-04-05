from bcrypt import gensalt
from datetime import datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import status, HTTPException
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP

from src.database.database import Base
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
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def check_if_user_exists(db: Session, email: str, username: str) -> None:
        if UserDatabaseHandler.get_user_by_email(db, email):
            UserDatabaseHandler.raise_user_already_exists('email')

        if UserDatabaseHandler.get_user_by_username(db, username):
            UserDatabaseHandler.raise_user_already_exists('username')

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create_user(db: Session, user_create_payload: UserCreate) -> User:
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
        db.commit()
        db.refresh(db_user)

        return db_user

    @staticmethod
    def update_user(db: Session, user_id: int, user_update_payload: UserUpdate) -> User:
        db.query(User)\
            .filter(User.user_id == user_id)\
            .update(user_update_payload.dict(exclude_none=True), synchronize_session=False)
        db.commit()
        return UserDatabaseHandler.get_user_by_id(db, user_id=user_id)
