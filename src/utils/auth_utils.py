from datetime import timedelta
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status

from src.config import ALGORITHM
from src.database.database_config import get_db
from src.database.models.user import UserDatabaseHandler as DatabaseHandler, User


def generate_tokens(subject: str, authorize: AuthJWT):
    return {
        'access_token': authorize.create_access_token(
            subject=subject,
            expires_time=timedelta(days=1),
            algorithm=ALGORITHM
        ),
        'refresh_token': authorize.create_refresh_token(
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
        authorize: AuthJWT = Depends()
) -> str:
    authorize.jwt_required()
    username = authorize.get_jwt_subject()
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
