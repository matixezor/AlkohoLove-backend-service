from datetime import timedelta
from async_fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status, Header

from src.config import ALGORITHM
from src.database.database_config import get_db
from src.database.models.token_blacklist import TokenBlacklistDatabaseHandler
from src.database.models.user import UserDatabaseHandler as DatabaseHandler, User


async def get_valid_token(
        authorization: str | None = Header(default=None),
        db: AsyncSession = Depends(get_db),
        authorize: AuthJWT = Depends()
) -> str:
    await authorize.jwt_required()
    jti = (await authorize.get_raw_jwt())['jti']
    if await TokenBlacklistDatabaseHandler.check_if_token_is_blacklisted(db, jti):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token is revoked'
        )
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


def raise_credentials_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )


async def get_current_user_username(
    token: str = Depends(get_valid_token),
    authorize: AuthJWT = Depends()
) -> str:
    username = (await authorize.get_raw_jwt(token))['sub']
    if username is None:
        raise_credentials_exception()
    return username


async def get_current_user(
    username: str = Depends(get_current_user_username),
    db: AsyncSession = Depends(get_db)
) -> User:
    user = await DatabaseHandler.get_user_by_username(db, username)
    if user is None:
        raise_credentials_exception()
    return user


async def is_admin(user: User = Depends(get_current_user)) -> bool:
    if user.is_admin:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient permissions'
        )
