from bson import ObjectId
from bcrypt import gensalt
from datetime import datetime
from passlib.context import CryptContext
from fastapi import status, HTTPException
from pymongo.collection import Collection, ReturnDocument

from src.domain.alcohol import AlcoholBase
from src.domain.user import UserUpdate, UserAdminInfo
from src.domain.user import UserCreate
from src.infrastructure.database.models.user import User
from src.infrastructure.database.models.user_list.favourites import Favourites
from src.infrastructure.database.models.user_list.search_history import UserSearchHistory
from src.infrastructure.database.models.user_list.wishlist import UserWishlist
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
    async def ban_user(collection: Collection[User], user_id: str) -> None:
        collection.find_one_and_update({'_id': ObjectId(user_id)}, {"$set": {'is_banned': True}})

    @staticmethod
    async def unban_user(collection: Collection[User], user_id: str) -> None:
        collection.find_one_and_update({'_id': ObjectId(user_id)}, {"$set": {'is_banned': False}})

    @staticmethod
    async def get_user_by_id(collection: Collection[User], user_id: str) -> User | None:
        return collection.find_one({'_id': ObjectId(user_id)})

    @staticmethod
    async def get_users(collection: Collection[User], limit: int, offset: int, username: str) -> list[User]:
        return list(
            collection.find({'username': {'$regex': username, '$options': 'i'}}).skip(offset).limit(limit)
        )

    @staticmethod
    async def count_users(collection: Collection[User], username: str) -> int:
        return (
            collection.count_documents(filter={'username': {'$regex': username, '$options': 'i'}})
            if username
            else collection.estimated_document_count()
        )

    @staticmethod
    async def delete_user(collection: Collection[User], user_id: ObjectId) -> None:
        collection.delete_one({'_id': user_id})

    @staticmethod
    async def check_if_user_exists(collection: Collection[User], email: str = None, username: str = None) -> None:
        if email and await UserDatabaseHandler.get_user_by_email(collection, email):
            raise UserExistsException()
        if username and await UserDatabaseHandler.get_user_by_username(collection, username):
            raise UserExistsException()

    @staticmethod
    async def get_user_by_email(collection: Collection[User], email: str) -> User | None:
        return collection.find_one({'email': email})

    @staticmethod
    async def get_user_by_username(collection: Collection[User], username: str) -> User | None:
        return collection.find_one({'username': username})

    @staticmethod
    async def create_user(collection: Collection[User], payload: UserCreate) -> None:
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

        collection.insert_one(db_user)

    @staticmethod
    async def authenticate_user(
            collection: Collection[User],
            username: str,
            password: str,
            update_last_login: bool = False
    ) -> User:
        user = await UserDatabaseHandler.get_user_by_username(collection, username)
        if user['is_banned']:
            raise UserBannedException()
        raw_password = user['password_salt'] + password
        if not user or not UserDatabaseHandler.verify_password(raw_password, user['password']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f'Invalid username or password'
            )
        if update_last_login:
            collection.update_one({'_id': user['_id']}, {'$set': {'last_login': datetime.now()}})
        return user

    @staticmethod
    async def update_user(
            collection: Collection[User],
            user_id: ObjectId,
            user_update_payload: UserUpdate
    ) -> User:
        return collection.find_one_and_update(
            {'_id': user_id},
            {'$set': user_update_payload.dict(exclude_none=True)},
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    async def create_user_lists(
            user_collection: Collection[User],
            username: str,
            wishlist_collection: Collection[UserWishlist],
            favourites_collection: Collection[Favourites],
            search_history_collection: Collection[UserSearchHistory],
    ) -> None:
        user = await UserDatabaseHandler.get_user_by_username(user_collection, username)
        empty_wishlist = UserWishlist(user_id=user['_id'], alcohols=[], _id=ObjectId())
        wishlist_collection.insert_one(empty_wishlist)
        empty_favourites = Favourites(user_id=user['_id'], alcohols=[], _id=ObjectId())
        favourites_collection.insert_one(empty_favourites)
        empty_search_history = UserSearchHistory(user_id=user['_id'], alcohols=[], _id=ObjectId())
        search_history_collection.insert_one(empty_search_history)
