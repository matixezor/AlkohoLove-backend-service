from bson import ObjectId
from bcrypt import gensalt
from datetime import datetime
from passlib.context import CryptContext
from fastapi import status, HTTPException
from pymongo.collection import Collection, ReturnDocument

from src.domain.user import UserUpdate
from src.domain.user import UserCreate
from src.infrastructure.database.models.user import User
from src.infrastructure.exceptions.auth_exceptions import UserBannedException
from src.infrastructure.exceptions.users_exceptions import UserExistsException


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserDatabaseHandler:
    @staticmethod
    def get_password_hash(password: str, salt: str) -> str:
        return pwd_context.hash(salt + password)

    @staticmethod
    def verify_password(password_raw: str, hashed_password: str) -> bool:
        return pwd_context.verify(password_raw, hashed_password)

    @staticmethod
    async def ban_user(user_id: str, users_collection: Collection[User]) -> None:
        users_collection.find_one_and_update({'_id': ObjectId(user_id)}, {"$set": {'is_banned': True}})

    @staticmethod
    async def unban_user(user_id: str, users_collection: Collection[User]) -> None:
        users_collection.find_one_and_update({'_id': ObjectId(user_id)}, {"$set": {'is_banned': False}})

    @staticmethod
    async def get_user_by_id(user_id: str, users_collection: Collection[User]) -> User | None:
        return users_collection.find_one({'_id': ObjectId(user_id)})

    @staticmethod
    async def get_users(limit: int, offset: int, username: str, users_collection: Collection[User]) -> list[User]:
        return list(
            users_collection
                .find({'username': {'$regex': username, '$options': 'i'}})
                .skip(offset)
                .limit(limit)
        )

    @staticmethod
    async def count_users(username: str, users_collection: Collection[User]) -> int:
        return (
            users_collection.count_documents(filter={'username': {'$regex': username, '$options': 'i'}})
            if username
            else users_collection.estimated_document_count()
        )

    @staticmethod
    async def delete_user(user_id: ObjectId, users_collection: Collection[User]) -> None:
        users_collection.delete_one({'_id': user_id})

    @staticmethod
    async def check_if_user_exists(users_collection: Collection[User], email: str = None, username: str = None) -> None:
        if email and await UserDatabaseHandler.get_user_by_email(email, users_collection):
            raise UserExistsException()
        if username and await UserDatabaseHandler.get_user_by_username(username, users_collection):
            raise UserExistsException()

    @staticmethod
    async def get_user_by_email(email: str, users_collection: Collection[User]) -> User | None:
        return users_collection.find_one({'email': email})

    @staticmethod
    async def get_user_by_username(username: str, users_collection: Collection[User]) -> User | None:
        return users_collection.find_one({'username': username})

    @staticmethod
    async def create_user(payload: UserCreate, users_collection: Collection[User]) -> None:
        password_salt = gensalt().decode('utf-8')
        payload.password = UserDatabaseHandler.get_password_hash(
            payload.password,
            password_salt
        )

        db_user = User(
            **payload.dict(),
            created_on=datetime.now(),
            password_salt=password_salt,
            is_banned=False,
            is_admin=False,
            last_login=None
        )

        users_collection.insert_one(db_user)

    @staticmethod
    async def authenticate_user(
        username: str,
        password: str,
        users_collection: Collection[User],
        update_last_login: bool = False
    ) -> User:
        user = await UserDatabaseHandler.get_user_by_username(username, users_collection)
        if user['is_banned']:
            raise UserBannedException()
        raw_password = user['password_salt'] + password
        if not user or not UserDatabaseHandler.verify_password(raw_password, user['password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'Invalid username or password'
            )
        if update_last_login:
            users_collection.update_one({'_id': user['_id']}, {'$set': {'last_login': datetime.now()}})
        return user

    @staticmethod
    async def update_user(
        user_id: ObjectId,
        user_update_payload: UserUpdate,
        users_collection: Collection[User]
    ) -> User:
        return users_collection.find_one_and_update(
            {'_id': user_id},
            {'$set': user_update_payload.dict(exclude_none=True)},
            return_document=ReturnDocument.AFTER
        )
