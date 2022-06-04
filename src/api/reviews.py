from pymongo.database import Database
from fastapi import APIRouter, Depends, status

from src.domain.common import PageInfo
from src.infrastructure.database.database_config import get_db
from src.domain.review.paginated_review import PaginatedReview
from src.infrastructure.database.models.user import UserDatabaseHandler
from src.infrastructure.database.models.review import ReviewDatabaseHandler
from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler
from src.infrastructure.exceptions.users_exceptions import UserNotFoundException
from src.infrastructure.exceptions.alcohol_exceptions import AlcoholNotFoundException

router = APIRouter(prefix='/reviews', tags=['reviews'])


@router.get(
    path='/{alcohol_id}',
    response_model=PaginatedReview,
    status_code=status.HTTP_200_OK,
    summary='Read alcohol reviews',
    response_model_by_alias=False
)
async def get_reviews(
        alcohol_id: str,
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db)
) -> PaginatedReview:

    if not await AlcoholDatabaseHandler.check_if_alcohol_exists(
            db.alcohols,
            alcohol_id):
        raise AlcoholNotFoundException()

    reviews = await ReviewDatabaseHandler.get_alcohol_reviews(
        db.reviews, limit, offset, alcohol_id
    )
    total = await ReviewDatabaseHandler.count_alcohol_reviews(db.reviews, alcohol_id)
    return PaginatedReview(
        reviews=reviews,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/user/{user_id}',
    response_model=PaginatedReview,
    status_code=status.HTTP_200_OK,
    summary='Read user reviews',
    response_model_by_alias=False
)
async def get_user_reviews(
        user_id: str,
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db)
) -> PaginatedReview:
    if not await UserDatabaseHandler.check_if_user_exists(
        db.users,
        user_id=user_id,
    ):
        raise UserNotFoundException()

    reviews = await ReviewDatabaseHandler.get_user_reviews(
        db.reviews, limit, offset, user_id
    )
    total = await ReviewDatabaseHandler.count_user_reviews(db.reviews, user_id)
    return PaginatedReview(
        reviews=reviews,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )
