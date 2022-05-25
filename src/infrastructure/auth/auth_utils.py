from datetime import timedelta
from pymongo.database import Database
from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, HTTPException, status, Header

from src.infrastructure.config.app_config import ALGORITHM
from src.infrastructure.database.database_config import get_db
from src.infrastructure.database.models.user import UserDatabaseHandler as DatabaseHandler, User
from src.infrastructure.database.models.token.token_database_handler import TokenBlacklistDatabaseHandler
from src.infrastructure.exceptions.auth_exceptions \
    import CredentialsException, UserBannedException, TokenRevokedException


async def get_valid_token(
        authorization: str | None = Header(default=None),
        authorize: AuthJWT = Depends(),
        db: Database = Depends(get_db)
) -> str:
    await authorize.jwt_required()
    jti = (await authorize.get_raw_jwt())['jti']
    if await TokenBlacklistDatabaseHandler.check_if_token_is_blacklisted(db.tokens_blacklist, jti):
        raise TokenRevokedException(token_type='Access')
    return authorization.replace('Bearer ', '')


async def generate_tokens(subject: str, authorize: AuthJWT):
    return {
        'access_token': await authorize.create_access_token(
            subject=subject,
            expires_time=timedelta(days=1),
            algorithm=ALGORITHM
        ),
        'refresh_token': await authorize.create_refresh_token(
            subject=subject,
            expires_time=timedelta(days=31),
            algorithm=ALGORITHM
        )
    }


async def get_valid_user(
        token: str = Depends(get_valid_token),
        authorize: AuthJWT = Depends(),
        db: Database = Depends(get_db)
) -> User:
    username = (await authorize.get_raw_jwt(token))['sub']
    if username is None:
        raise CredentialsException()
    user = await DatabaseHandler.get_user_by_username(db.users, username)
    if not user:
        raise CredentialsException()
    if user['is_banned']:
        raise UserBannedException()
    return user


async def admin_permission(user: User = Depends(get_valid_user)) -> bool:
    if user['is_admin']:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient permissions'
        )
