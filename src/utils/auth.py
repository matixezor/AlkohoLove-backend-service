from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

from domain.token import TokenData
from src.config import SECRET_KEY, ALGORITHM
from src.database.database_config import get_db
from src.database.models.user import UserDatabaseHandler as DatabaseHandler, User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/token')


def raise_credentials_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )


async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise_credentials_exception()
        token_data = TokenData(username=username)
        user = await DatabaseHandler.get_user_by_username(db, token_data.username)
        if user is None:
            raise_credentials_exception()
        return user
    except JWTError:
        raise_credentials_exception()


async def is_admin(user: User = Depends(get_current_user)) -> bool:
    if user.is_admin:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Insufficient permissions'
        )
