from fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response

from src.domain.token import Token
from src.domain.user import UserCreate
from src.utils.auth_utils import generate_tokens
from src.database.database_config import get_db
from src.database.models.user import UserDatabaseHandler as DatabaseHandler


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/token',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary='Login for token'
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
    authorize: AuthJWT = Depends()
):
    user = await DatabaseHandler.authenticate_user(db, form_data.username, form_data.password, True)
    return generate_tokens(user.username, authorize)


@router.post(
    '/refresh',
    response_model=Token,
    status_code=status.HTTP_200_OK
)
async def refresh(authorize: AuthJWT = Depends()):
    authorize.jwt_refresh_token_required()

    current_user = authorize.get_jwt_subject()
    return generate_tokens(current_user, authorize)


@router.post(
    '/register',
    response_class=Response,
    status_code=status.HTTP_201_CREATED
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
