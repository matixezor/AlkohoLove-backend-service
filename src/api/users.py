from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException

from src.database.database import get_db
from src.domain.user import User, UserCreate
from src.database.models.user import get_user_by_id, get_user_by_email_or_username, create_user


router = APIRouter(prefix='/users', tags=['users'])


@router.get(
    path='/{user_id}',
    summary='Read user information',
    response_model=User,
    status_code=status.HTTP_200_OK
)
def read_user(user_id: int, db: Session = Depends(get_db)) -> User:
    """
    Read user information
    """
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return db_user


@router.post(
    path='/',
    summary='Create user',
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
def add_user(user: UserCreate, db: Session = Depends(get_db)) -> User:
    """
    Create user. Required body fields:
    - **email**: required
    - **name**: required
    - **password**: required
    """
    if get_user_by_email_or_username(db, user.email, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already exists')
    return create_user(db, user)
