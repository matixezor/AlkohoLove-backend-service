from datetime import datetime
from operator import itemgetter
from async_fastapi_jwt_auth import AuthJWT
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response, Header, HTTPException

from src.domain.token import Token
from src.domain.user import UserCreate
from src.infrastructure.database.models.user import UserDatabaseHandler
from src.infrastructure.auth.auth_utils import generate_tokens, get_valid_token
from src.infrastructure.database.models.token import TokenBlacklistDatabaseHandler
from src.infrastructure.exceptions.auth_exceptions \
    import UserBannedException, TokenRevokedException, CredentialsException


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/token',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary='Login for token'
)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    authorize: AuthJWT = Depends()
):
    user = await UserDatabaseHandler.authenticate_user(form_data.username, form_data.password, True)
    return await generate_tokens(user['username'], authorize)


@router.post(
    '/refresh',
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def refresh(authorize: AuthJWT = Depends()):
    await authorize.jwt_refresh_token_required()

    token_jti, current_user = itemgetter('jti', 'sub')(await authorize.get_raw_jwt())

    if await TokenBlacklistDatabaseHandler.check_if_token_is_blacklisted(token_jti):
        raise TokenRevokedException(token_type='Refresh')

    db_user = await UserDatabaseHandler.get_user_by_username(current_user)
    if not db_user:
        raise CredentialsException()
    if db_user['is_banned']:
        raise UserBannedException()

    return await generate_tokens(current_user, authorize)


@router.post(
    '/register',
    response_class=Response,
    status_code=status.HTTP_201_CREATED
)
async def register(user_create_payload: UserCreate) -> None:
    """
    Create user with request body:
    - **email**: required
    validated with regex `[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,3}`
    - **name**: required
    - **password**: required
    validated with regex `^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$`
    """
    await UserDatabaseHandler.check_if_user_exists(
        user_create_payload.email,
        user_create_payload.username
    )
    await UserDatabaseHandler.create_user(user_create_payload)


@router.post(
    '/logout',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout(
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

    if await TokenBlacklistDatabaseHandler.check_if_token_is_blacklisted(token_jti=refresh_token_jti):
        raise TokenRevokedException(
            token_type='Refresh'
        )

    await TokenBlacklistDatabaseHandler.add_token_to_blacklist(
        token_jti=access_token_jti, expiration_date=datetime.fromtimestamp(access_token_exp)
    )

    await TokenBlacklistDatabaseHandler.add_token_to_blacklist(
       token_jti=refresh_token_jti, expiration_date=datetime.fromtimestamp(refresh_token_exp)
    )
