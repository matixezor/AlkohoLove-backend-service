from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException

from src.database.database_config import get_db
from src.domain.user import User, UserCreate, UserUpdate
from src.database.models.user import UserDatabaseHandler as DatabaseHandler

router = APIRouter(prefix='/users', tags=['users'])


def raise_user_not_found():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')


@router.get(
    path='/{user_id}',
    summary='Read user information',
    response_model=User,
    status_code=status.HTTP_200_OK
)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)) -> User:
    """
    Read user information
    """
    db_user = await DatabaseHandler.get_user_by_id(db, user_id)
    if not db_user:
        raise_user_not_found()
    return db_user


@router.put(
    path='/{user_id}',
    summary='Update user',
    response_model=User,
    status_code=status.HTTP_200_OK
)
async def update_user(
        user_id: int,
        user_update_payload: UserUpdate,
        db: AsyncSession = Depends(get_db)
) -> User:
    """
    Update user with request Body:
    - **email**: optional
    validated with regex `[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,3}`
    - **name**: optional
    - **password**: optional
     validated with regex `^(?=.*\\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$`
    - **is_banned**: optional
    """
    db_user = DatabaseHandler.get_user_by_id(db, user_id)
    if not db_user:
        raise_user_not_found()
    return await DatabaseHandler.update_user(db, user_id, user_update_payload)


@router.post(
    path='',
    summary='Create user',
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
async def post_user(user_create_payload: UserCreate, db: AsyncSession = Depends(get_db)) -> User:
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
    return await DatabaseHandler.create_user(db, user_create_payload)
