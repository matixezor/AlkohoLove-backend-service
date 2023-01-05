from bcrypt import gensalt
from random import randbytes
from pydantic import EmailStr
from datetime import datetime
from bson import ObjectId, Int64
from passlib.context import CryptContext
from pymongo.collection import Collection, ReturnDocument

from src.domain.user import UserCreate
from src.domain.user.user_email import UserEmail
from src.infrastructure.database.models.user import User
from src.infrastructure.email.email_handler import Email
from src.infrastructure.database.models.user_tag import UserTag
from src.infrastructure.email.email_utils import dehash_token, hash_token
from src.infrastructure.database.models.user_list.wishlist import UserWishlist
from src.infrastructure.database.models.user_list.favourites import Favourites
from src.infrastructure.exceptions.users_exceptions import UserNotFoundException
from src.infrastructure.config.app_config import get_settings, ApplicationSettings
from src.infrastructure.database.models.user_list.search_history import UserSearchHistory
from src.infrastructure.exceptions.auth_exceptions import UserBannedException, InvalidCredentialsException, \
    EmailNotVerifiedException, SendingEmailError, InvalidVerificationCode

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserDatabaseHandler:
    @staticmethod
    def get_password_hash(password: str, salt: str) -> str:
        return pwd_context.hash(salt + password)

    @staticmethod
    def verify_password(password_raw: str, hashed_password: str) -> bool:
        return pwd_context.verify(password_raw, hashed_password)

    @staticmethod
    async def ban_user(collection: Collection[User], user_id: ObjectId) -> None:
        collection.find_one_and_update({'_id': user_id}, {"$set": {'is_banned': True}})

    @staticmethod
    async def unban_user(collection: Collection[User], user_id: ObjectId) -> None:
        collection.find_one_and_update({'_id': user_id}, {"$set": {'is_banned': False}})

    @staticmethod
    async def get_user_by_id(collection: Collection[User], user_id: ObjectId) -> User | None:
        return collection.find_one({'_id': user_id})

    @staticmethod
    async def get_users(collection: Collection[User], limit: int, offset: int, username: str | None) -> list[User]:
        query = {'username': {'$regex': username, '$options': 'i'}} if username else {}
        return list(
            collection.find(query).skip(offset).limit(limit)
        )

    @staticmethod
    async def count_users(collection: Collection[User], username: str) -> int:
        return (
            collection.count_documents(filter={'username': {'$regex': username, '$options': 'i'}})
            if username
            else collection.estimated_document_count()
        )

    @staticmethod
    async def count_users_without_current(
            collection: Collection[User],
            username: str | None,
            current_user: User
    ) -> int:
        query = {'username': {'$ne': current_user['username']}}
        if username:
            query['username'] |= {'$regex': username, '$options': 'i'}
        return (
            collection.count_documents(filter=query)
            if username
            else collection.estimated_document_count()
        )

    @staticmethod
    async def delete_user(collection: Collection[User], user_id: ObjectId) -> None:
        collection.delete_one({'_id': user_id})

    @staticmethod
    async def delete_user_lists(
            favourites: Collection[Favourites],
            wishlist: Collection[UserWishlist],
            search_history: Collection[UserSearchHistory],
            tags: Collection[UserTag],
            user_id: ObjectId
    ) -> None:
        favourites.delete_one({'user_id': user_id})
        wishlist.delete_one({'user_id': user_id})
        search_history.delete_one({'user_id': user_id})
        tags.delete_many({'user_id': user_id})

    @staticmethod
    async def check_if_user_exists(
            collection: Collection[User],
            email: str = None,
            username: str = None,
            user_id: ObjectId = None
    ) -> bool:
        if email and await UserDatabaseHandler.get_user_by_email(collection, email):
            return True
        if username and await UserDatabaseHandler.get_user_by_username(collection, username):
            return True
        if user_id and await UserDatabaseHandler.get_user_by_id(collection, user_id):
            return True
        else:
            return False

    @staticmethod
    async def get_user_by_email(collection: Collection[User], email: str) -> User | None:
        return collection.find_one({'email': email})

    @staticmethod
    async def get_user_by_username(collection: Collection[User], username: str) -> User | None:
        return collection.find_one({'username': username})

    @staticmethod
    async def create_user(collection: Collection[User], payload: UserCreate):
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
            last_login=None,
            avg_rating=float(0),
            rate_count=Int64(0),
            followers_count=0,
            following_count=0,
            favourites_count=0,
            rate_value=Int64(0),
            wishlist_count=0,
            updated_at=datetime.now(),
            is_verified=False,
            verification_code=None)
        user = collection.insert_one(db_user)
        return collection.find_one({'_id': user.inserted_id})

    @staticmethod
    async def send_verification_mail(
            collection: Collection[User],
            user: User,
            settings: ApplicationSettings
    ):
        token = randbytes(10)
        verification_code = hash_token(token)
        new_user = collection.find_one_and_update({'_id': user['_id']}, {
            '$set': {'verification_code': verification_code, 'updated_at': datetime.utcnow()}},
                                                  return_document=ReturnDocument.AFTER)
        url = f'{settings.HOST}:{settings.HOST_PORT}/auth/verify_email/{token.hex()}'
        await Email(new_user, url, [EmailStr(user['email'])]).send_verification_code()

    @staticmethod
    async def verify_email(
            token: str,
            collection: Collection[User]
    ):
        verification_code = dehash_token(token)
        result = collection.find_one_and_update({'verification_code': verification_code}, {
            '$set': {'verification_code': None, 'is_verified': True, 'updated_at': datetime.utcnow()}}, new=True,
                                                return_document=ReturnDocument.AFTER)
        if not result:
            raise InvalidVerificationCode()

    @staticmethod
    async def authenticate_user(
            collection: Collection[User],
            username: str,
            password: str,
            update_last_login: bool = False
    ) -> User:
        user = await UserDatabaseHandler.get_user_by_username(collection, username)
        if not user:
            raise UserNotFoundException()
        if not user['is_verified']:
            raise EmailNotVerifiedException()
        raw_password = user['password_salt'] + password
        if not UserDatabaseHandler.verify_password(raw_password, user['password']):
            raise InvalidCredentialsException()
        if user['is_banned']:
            raise UserBannedException()
        if update_last_login:
            collection.update_one({'_id': user['_id']}, {'$set': {'last_login': datetime.now()}})
        return user

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

    @staticmethod
    async def search_users_by_phrase(
            collection: Collection,
            limit: int, offset: int,
            phrase: str,
            current_user: User
    ) -> list[dict]:
        result = list(collection.find(
            {'username': {'$regex': phrase, '$options': 'i', '$ne': current_user['username']}}).skip(offset).limit(
            limit))
        return result

    @staticmethod
    async def add_to_favourite_counter(
            collection: Collection,
            user_id: ObjectId
    ):
        collection.update_one({'_id': {'$eq': ObjectId(user_id)}}, {'$inc': {'favourites_count': 1}})

    @staticmethod
    async def remove_from_favourite_counter(
            collection: Collection,
            user_id: ObjectId
    ):
        collection.update_one(
            {
                '_id': {'$eq': ObjectId(user_id)},
                'favourites_count': {'$gt': 0}
            },
            {
                '$inc': {'favourites_count': -1}
            }
        )

    @staticmethod
    async def send_password_reset_request(
            payload: UserEmail,
            collection: Collection[User],
            user: User,
            settings: ApplicationSettings
    ):
        try:
            token = randbytes(10)
            reset_password_code = hash_token(token)
            collection.find_one_and_update({'_id': user['_id']}, {
                '$set': {'reset_password_code': reset_password_code, 'updated_at': datetime.utcnow()}},
                                           return_document=ReturnDocument.AFTER)
            url = f'{settings.WEB_HOST}:{settings.WEB_PORT}/reset_password/{token.hex()}'
            await Email(user, url, [EmailStr(payload.email)]).send_reset_password_code()
        except Exception:
            collection.find_one_and_update({'_id': user['_id']},
                                           {'$set': {'reset_password_code': None, 'updated_at': datetime.utcnow()}},
                                           return_document=ReturnDocument.AFTER)
            raise SendingEmailError()

    @staticmethod
    async def check_reset_token(
            token: str,
            collection: Collection[User]
    ):
        reset_password_code = dehash_token(token)
        return collection.find_one({'reset_password_code': reset_password_code})

    @staticmethod
    async def change_password(
            new_password: str,
            token: str,
            collection: Collection[User]
    ):
        reset_password_code = dehash_token(token)
        password_salt = gensalt().decode('utf-8')
        new_password = UserDatabaseHandler.get_password_hash(new_password, password_salt)
        collection.find_one_and_update({'reset_password_code': reset_password_code},
                                       {'$set': {'password': new_password, 'password_salt': password_salt,
                                                 'reset_password_code': None, 'updated_at': datetime.utcnow()}})

    @staticmethod
    async def send_deletion_request(
            current_user: User,
            collection: Collection[User],
            settings: ApplicationSettings
    ):
        try:
            token = randbytes(10)
            delete_account_code = hash_token(token)
            user = collection.find_one_and_update({'_id': current_user['_id']},
                                                  {'$set': {'delete_account_code': delete_account_code}},
                                                  return_document=ReturnDocument.AFTER)
            url = f'{settings.HOST}:{settings.HOST_PORT}/me/delete_account/{token.hex()}'
            await Email(user, url, [EmailStr(current_user['email'])]).send_delete_account_code()
        except Exception:
            collection.find_one_and_update({'_id': current_user['_id']}, {'$set': {'delete_account_code': None}})
            raise SendingEmailError

    @staticmethod
    async def find_user_by_deletion_code(token: str, collection: Collection[User]):
        delete_account_code = dehash_token(token)
        return collection.find_one({'delete_account_code': delete_account_code})

    @staticmethod
    async def delete_user_by_id(user_id: ObjectId, collection: Collection[User]):
        return collection.find_one_and_delete({'_id': user_id})

    @staticmethod
    async def add_to_wishlist_counter(
            collection: Collection,
            user_id: ObjectId
    ):
        collection.update_one({'_id': {'$eq': ObjectId(user_id)}}, {'$inc': {'wishlist_count': 1}})

    @staticmethod
    async def remove_from_wishlist_counter(
            collection: Collection,
            user_id: ObjectId
    ):
        collection.update_one(
            {
                '_id': {'$eq': ObjectId(user_id)},
                'wishlist_count': {'$gt': 0}
            },
            {
                '$inc': {'wishlist_count': -1}
            }
        )
