from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException

from src.domain.user import User, UserUpdate
from src.database.database_config import get_db
from src.database.models.user import User as UserInDb
from src.database.models.user import UserDatabaseHandler as DatabaseHandler
from src.utils.auth_utils import get_current_user, get_current_user_username


router = APIRouter(prefix='/me', tags=['me'])


@router.get(
    path='',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Read information about your account'
)
async def get_self(current_user: User = Depends(get_current_user)) -> User:
    return current_user


@router.put(
    path='',
    response_model=User,
    status_code=status.HTTP_200_OK,
    summary='Update your account data'
)
async def update_self(
        update_payload: UserUpdate,
        current_user: UserInDb = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)
) -> User:
    if (update_payload.password and not update_payload.new_password) \
            or (not update_payload.password and update_payload.new_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Both password must be provided'
        )
    elif update_payload.password:
        password_verified = DatabaseHandler.verify_password(
            current_user.password_salt + update_payload.password,
            current_user.password
        )
        if not password_verified:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Passwords do not match'
            )
        update_payload.password = DatabaseHandler.get_password_hash(
            password=update_payload.new_password,
            salt=current_user.password_salt
        )
        update_payload.new_password = None
    return await DatabaseHandler.update_user(
        db,
        current_user,
        update_payload
    )


@router.delete(
    path='',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete your account'
)
async def delete_self(
        current_user: str = Depends(get_current_user_username),
        db: AsyncSession = Depends(get_db)
) -> None:
    await DatabaseHandler.delete_user(db, current_user)
