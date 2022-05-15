from datetime import datetime
from operator import itemgetter
from async_fastapi_jwt_auth import AuthJWT
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response, Header, HTTPException

from src.domain.token import Token
from src.domain.user import UserCreate
from src.database.database_config import get_db
from src.database.models.user import UserDatabaseHandler
from src.utils.auth_utils import generate_tokens, get_valid_token
from src.database.models.token_blacklist import TokenBlacklistDatabaseHandler


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
    user = await UserDatabaseHandler.authenticate_user(db, form_data.username, form_data.password, True)
    return await generate_tokens(user.username, authorize)


@router.post(
    '/refresh',
    response_model=Token,
    status_code=status.HTTP_200_OK
)
async def refresh(authorize: AuthJWT = Depends()):
    await authorize.jwt_refresh_token_required()

    current_user = await authorize.get_jwt_subject()
    return await generate_tokens(current_user, authorize)


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
    await UserDatabaseHandler.check_if_user_exists(
        db,
        user_create_payload.email,
        user_create_payload.username
    )
    await UserDatabaseHandler.create_user(db, user_create_payload)


@router.post(
    '/logout',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout(
        db: AsyncSession = Depends(get_db),
        access_token: str = Depends(get_valid_token),
        authorization_refresh: str | None = Header(default=None),
        authorize: AuthJWT = Depends(AuthJWT)
) -> None:
    """
    Logout endpoint. This endpoint requires two tokens to be sent.
    Access token under the name `Authorization`
    and refresh token under the name `AuthorizationRefresh`
    *Important!*
    AuthorizationRefresh token should not contain the Bearer prefix
    """
    if not authorization_refresh:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Refresh token must be provided'
        )

    refresh_token_jti, refresh_token_exp = itemgetter('jti', 'exp')(await authorize.get_raw_jwt(authorization_refresh))
    access_token_jti, access_token_exp = itemgetter('jti', 'exp')(await authorize.get_raw_jwt(access_token))

    if await TokenBlacklistDatabaseHandler.check_if_token_is_blacklisted(token_jti=refresh_token_jti, db=db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Refresh token is already blacklisted'
        )

    await TokenBlacklistDatabaseHandler.add_token_to_blacklist(
        db=db, token_jti=access_token_jti, expiration_date=datetime.fromtimestamp(access_token_exp)
    )

    await TokenBlacklistDatabaseHandler.add_token_to_blacklist(
        db=db, token_jti=refresh_token_jti, expiration_date=datetime.fromtimestamp(refresh_token_exp)
    )
