from bson import ObjectId
from pymongo.database import Database
from fastapi import APIRouter, Depends, status

from src.domain.common import PageInfo
from src.domain.review import Review
from src.infrastructure.database.database_config import get_db
from src.domain.review.paginated_review import PaginatedReview
from src.infrastructure.auth.auth_utils import get_optional_user
from src.infrastructure.common.validate_object_id import validate_object_id
from src.infrastructure.database.models.review import ReviewDatabaseHandler
from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler
from src.infrastructure.database.models.user import UserDatabaseHandler, User
from src.domain.review.paginated_alcohol_review import PaginatedAlcoholReview
from src.infrastructure.exceptions.users_exceptions import UserNotFoundException
from src.infrastructure.exceptions.alcohol_exceptions import AlcoholNotFoundException

router = APIRouter(prefix='/reviews', tags=['reviews'])


def handle_helpful_review(reporters: list[ObjectId], user_id: ObjectId, review_user_id: ObjectId) -> bool | None:
    return None if user_id == review_user_id else user_id in reporters


@router.get(
    path='/{alcohol_id}',
    response_model=PaginatedAlcoholReview,
    status_code=status.HTTP_200_OK,
    summary='Read alcohol reviews',
    response_model_by_alias=False
)
async def get_reviews(
        alcohol_id: str,
        limit: int = 10,
        offset: int = 0,
        current_user: User | None = Depends(get_optional_user),
        db: Database = Depends(get_db)
) -> PaginatedAlcoholReview:
    alcohol_id = validate_object_id(alcohol_id)
    user_id = None if not current_user else current_user.get('_id')
    if not await AlcoholDatabaseHandler.check_if_alcohol_exists(
            db.alcohols,
            alcohol_id):
        raise AlcoholNotFoundException()

    reviews = await ReviewDatabaseHandler.get_alcohol_reviews(
        db.reviews, limit, offset, alcohol_id
    )
    total = await ReviewDatabaseHandler.count_alcohol_reviews(db.reviews, alcohol_id)
    my_review = next((review for review in reviews if review['user_id'] == user_id), None) if user_id else None
    return PaginatedAlcoholReview(
        reviews=[
            Review(
                **review,
                helpful=handle_helpful_review(
                    review['helpful_reporters'],
                    user_id,
                    review['user_id']
                ) if user_id else False
            ) for review in reviews
        ],
        my_review=my_review,
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
        current_user: User | None = Depends(get_optional_user),
        db: Database = Depends(get_db)
) -> PaginatedReview:
    user_id = validate_object_id(user_id)
    current_user_id = None if not current_user else current_user.get('_id')
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
        reviews=[
            Review(
                **review,
                helpful=handle_helpful_review(
                    review['helpful_reporters'],
                    current_user_id,
                    review['user_id']
                ) if current_user_id else False
            ) for review in reviews
        ],
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )
