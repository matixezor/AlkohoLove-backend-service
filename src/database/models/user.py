from bcrypt import gensalt
from datetime import datetime
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP

from src.database.database import Base
from src.domain.user import UserCreate


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


def get_password_hash(password: str, salt: str) -> str:
    return pwd_context.hash(salt + password)


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.user_id == user_id).first()


def get_user_by_email_or_username(db: Session, email: str, username: str) -> list[User] | None:
    return db.query(User).filter(User.email == email, User.username == username)


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate) -> User:
    password_salt = gensalt().decode("utf-8")
    user.password = get_password_hash(user.password, password_salt)
    db_user = User(
        **user.dict(),
        created_on=datetime.now(),
        password_salt=password_salt
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
