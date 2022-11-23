from datetime import datetime
from operator import itemgetter
from pymongo.database import Database
from async_fastapi_jwt_auth import AuthJWT
from starlette.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, status, Response, Header, HTTPException, Request

from src.domain.token import Token
from src.domain.user import UserCreate
from src.domain.user.user_email import UserEmail
from src.infrastructure.database.database_config import get_db
from src.domain.user.user_change_password import UserChangePassword
from src.infrastructure.database.models.user import UserDatabaseHandler
from src.infrastructure.auth.auth_utils import generate_tokens, get_valid_token
from src.infrastructure.database.models.token import TokenBlacklistDatabaseHandler
from src.infrastructure.config.app_config import ApplicationSettings, get_settings
from src.infrastructure.exceptions.users_exceptions import UserExistsException, UserNotFoundException
from src.infrastructure.database.models.socials.followers_database_handler import FollowersDatabaseHandler
from src.infrastructure.exceptions.auth_exceptions \
    import UserBannedException, TokenRevokedException, CredentialsException, InsufficientPermissionsException, \
    EmailNotVerifiedException, SendingEmailError, InvalidVerificationCode

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/token',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary='Login for token'
)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        authorize: AuthJWT = Depends(),
        db: Database = Depends(get_db),
        settings: ApplicationSettings = Depends(get_settings)
):
    user = await UserDatabaseHandler.authenticate_user(db.users, form_data.username, form_data.password, True)
    return await generate_tokens(user['username'], authorize, settings)


@router.post(
    '/token/admin',
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary='Login for admin token'
)
async def admin_login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        authorize: AuthJWT = Depends(),
        db: Database = Depends(get_db),
        settings: ApplicationSettings = Depends(get_settings)
):
    user = await UserDatabaseHandler.authenticate_user(db.users, form_data.username, form_data.password, True)
    if user['is_admin']:
        return await generate_tokens(user['username'], authorize, settings)
    else:
        raise InsufficientPermissionsException()


@router.post(
    '/refresh',
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def refresh(
        authorize: AuthJWT = Depends(),
        db: Database = Depends(get_db),
        settings: ApplicationSettings = Depends(get_settings)
):
    await authorize.jwt_refresh_token_required()

    token_jti, current_user = itemgetter('jti', 'sub')(await authorize.get_raw_jwt())

    if await TokenBlacklistDatabaseHandler.check_if_token_is_blacklisted(db.tokens_blacklist, token_jti):
        raise TokenRevokedException(token_type='Refresh')

    db_user = await UserDatabaseHandler.get_user_by_username(db.users, current_user)
    if not db_user:
        raise CredentialsException()
    if db_user['is_banned']:
        raise UserBannedException()

    return await generate_tokens(current_user, authorize, settings)


@router.post(
    '/register',
    response_class=Response,
    status_code=status.HTTP_201_CREATED
)
async def register(
        user_create_payload: UserCreate,
        request: Request,
        db: Database = Depends(get_db)
) -> None:
    """
    Send verification email to given email address.
    Create user with request body:
    - **email**: required
    validated with regex `[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,3}`
    - **name**: required
    - **password**: required
    validated with regex `^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$`
    """
    if await UserDatabaseHandler.check_if_user_exists(
            db.users,
            user_create_payload.email,
            user_create_payload.username
    ):
        raise UserExistsException()

    user = await UserDatabaseHandler.create_user(db.users, user_create_payload)
    try:
        await UserDatabaseHandler.send_verification_mail(db.users, user, request)
    except Exception:
        await UserDatabaseHandler.delete_user_by_id(user['_id'], db.users)
        raise SendingEmailError()
    await UserDatabaseHandler.create_user_lists(db.users, user_create_payload.username, db.user_wishlist,
                                                db.user_favourites, db.user_search_history)
    await FollowersDatabaseHandler.create_followers_and_following_lists(db.users, user_create_payload.username,
                                                                        db.followers, db.following)


@router.post(
    '/logout',
    response_class=Response,
    status_code=status.HTTP_204_NO_CONTENT
)
async def logout(
        access_token: str = Depends(get_valid_token),
        authorization_refresh: str | None = Header(default=None),
        authorize: AuthJWT = Depends(AuthJWT),
        db: Database = Depends(get_db)
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

    token_blacklisted = await TokenBlacklistDatabaseHandler.check_if_token_is_blacklisted(
        db.tokens_blacklist, token_jti=refresh_token_jti
    )
    if token_blacklisted:
        raise TokenRevokedException(
            token_type='Refresh'
        )

    await TokenBlacklistDatabaseHandler.add_token_to_blacklist(
        db.tokens_blacklist, token_jti=access_token_jti, expiration_date=datetime.fromtimestamp(access_token_exp)
    )

    await TokenBlacklistDatabaseHandler.add_token_to_blacklist(
        db.tokens_blacklist, token_jti=refresh_token_jti, expiration_date=datetime.fromtimestamp(refresh_token_exp)
    )


@router.get(
    '/verify_email/{token}',
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT
)
async def verify_email(
        token: str,
        db: Database = Depends(get_db)

):
    settings = get_settings()
    try:
        await UserDatabaseHandler.verify_email(token, db.users)
    except InvalidVerificationCode:
        url = f'http://{settings.WEB_HOST}:{settings.WEB_PORT}/invalid_email_verification'
        return RedirectResponse(url=url)
    url = f'http://{settings.WEB_HOST}:{settings.WEB_PORT}/valid_email_verification '
    return RedirectResponse(url=url)


@router.post(
    path='/request_password_reset',
    response_class=Response,
    status_code=status.HTTP_200_OK,
    summary='Send email to reset password'
)
async def request_password_reset(
        payload: UserEmail,
        db: Database = Depends(get_db)
) -> None:
    """
    Sends email message with link to web page where you can put new password.
    """
    if not await UserDatabaseHandler.check_if_user_exists(db.users, email=payload.email):
        raise UserNotFoundException()

    db_user = await UserDatabaseHandler.get_user_by_email(db.users, payload.email)
    if not db_user['is_verified']:
        raise EmailNotVerifiedException()
    await UserDatabaseHandler.send_password_reset_request(payload, db.users, db_user)


@router.post(
    '/reset_password',
    response_class=RedirectResponse,
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    summary='Reset password'
)
async def reset_password(
        payload: UserChangePassword,
        db: Database = Depends(get_db)
):
    """
    token: token sent to email
    new_password: required validated with regex `^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$`
    """
    settings = get_settings()
    if not await UserDatabaseHandler.check_reset_token(payload.token, db.users):
        url = f'http://{settings.WEB_HOST}:{settings.WEB_PORT}/invalid_password_change'
        return RedirectResponse(url=url)
    await UserDatabaseHandler.change_password(payload.new_password, payload.token, db.users)
    url = f'http://{settings.WEB_HOST}:{settings.WEB_PORT}/valid_password_change'
    return RedirectResponse(url=url)
