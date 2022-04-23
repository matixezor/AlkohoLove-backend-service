from jose import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from src.domain.token import Token
from src.domain.user import UserCreate
from src.config import SECRET_KEY, ALGORITHM
from src.database.database_config import get_db
from src.database.models.user import UserDatabaseHandler as DatabaseHandler


router = APIRouter(prefix='/auth', tags=['auth'])


def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode.update({'exp': datetime.utcnow() + timedelta(hours=24)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post(
    '/token',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    tags=['token']
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await DatabaseHandler.authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={'sub': user.username})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.post(
    '/register',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    tags=['register']
)
async def register(user_create_payload: UserCreate, db: AsyncSession = Depends(get_db)) -> None:
    """
    Create user with request body:
    - **email**: required
    validated with regex `[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,3}`
    - **name**: required
    - **password**: required
    validated with regex `^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$`
    """
    await DatabaseHandler.check_if_user_exists(
        db,
        user_create_payload.email,
        user_create_payload.username
    )
    await DatabaseHandler.create_user(db, user_create_payload)
