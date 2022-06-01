from bson import ObjectId
from pymongo.collection import Collection, ReturnDocument
from datetime import datetime


from src.domain.alcohol import AlcoholBase
from src.domain.review.review_update import ReviewUpdate
from src.domain.user import UserBase
from src.infrastructure.database.models.review import Review
from src.domain.review import ReviewCreate


class ReviewDatabaseHandler:
    @staticmethod
    async def get_alcohol_reviews(
            collection: Collection[Review],
            limit: int,
            offset: int,
            alcohol_id: str
    ) -> list[Review]:
        print(list(collection.find({'alcohol_id': ObjectId(alcohol_id)}).skip(offset).limit(limit)))
        return (
            list(collection.find({'alcohol_id': ObjectId(alcohol_id)}).skip(offset).limit(limit))
        )

    @staticmethod
    async def count_alcohol_reviews(
            collection: Collection[Review],
            alcohol_id: str
    ) -> int:
        return (
            collection.count_documents(filter={'alcohol_id': {'$eq': ObjectId(alcohol_id)}})
        )

    @staticmethod
    async def check_if_alcohol_exists(
            collection: Collection[AlcoholBase],
            alcohol_id: str
    ) -> bool:
        if collection.find_one({'_id': ObjectId(alcohol_id)}):
            return True
        else:
            return False

    @staticmethod
    async def validate_rating(rating: int) -> bool:
        if (rating > 10) or (rating < 1):
            return False
        else:
            return True

    @staticmethod
    async def check_if_review_exists(
            collection: Collection[Review],
            alcohol_id: str,
            user_id: str,
    ) -> bool:
        if collection.find_one({'user_id': ObjectId(user_id), 'alcohol_id': ObjectId(alcohol_id)}):
            return True
        else:
            return False

    @staticmethod
    async def add_rating_to_alcohol(
            collection: Collection[AlcoholBase],
            alcohol_id: str,
            rating: int,
    ):
        alcohol = collection.find_one({'_id': ObjectId(alcohol_id)})
        rate_count = alcohol['rate_count'] + 1
        avg_rating = (alcohol['avg_rating'] * (rate_count - 1) + rating)/rate_count

        print(avg_rating)

        collection.update_many(
            {"_id": {"$eq": ObjectId(alcohol_id)}},
            {
                "$set": {"rate_count": rate_count, "avg_rating": avg_rating}
            }
        )

    @staticmethod
    async def remove_rating_from_alcohol(
            collection: Collection[AlcoholBase],
            alcohol_id: str,
            rating: int,
    ):
        alcohol = collection.find_one({'_id': ObjectId(alcohol_id)})
        rate_count = alcohol['rate_count'] - 1
        if rate_count < 1:
            avg_rating = 0
        else:
            avg_rating = (alcohol['avg_rating'] * (rate_count + 1) - rating)/rate_count

            print(avg_rating)

        collection.update_many(
            {"_id": {"$eq": ObjectId(alcohol_id)}},
            {
                "$set": {"rate_count": rate_count, "avg_rating": avg_rating}
            }
        )

    @staticmethod
    async def create_review(
            collection: Collection[Review],
            user_id: str,
            alcohol_id: str,
            user_name: str,
            payload: ReviewCreate
    ):
        db_review = Review(
            **payload.dict(),
            user_id=ObjectId(user_id),
            alcohol_id=ObjectId(alcohol_id),
            user_name=user_name,
            date=datetime.now(),
            report_count=0,
            reporters=[]
        )
        return collection.insert_one(db_review)

    @staticmethod
    async def check_if_review_belongs_to_user(
            collection: Collection[Review],
            review_id: str,
            user_id: str
    ) -> bool:
        if collection.find_one({'user_id': ObjectId(user_id), '_id': ObjectId(review_id)}):
            return True
        else:
            return False

    @staticmethod
    async def delete_review(
            collection: Collection[Review],
            review_id: str
    ):
        return collection.delete_one({'_id': ObjectId(review_id)})

    @staticmethod
    async def get_alcohol_id(
            collection: Collection[Review],
            review_id: str,
    ) -> str:
        review = collection.find_one({'_id': ObjectId(review_id)})
        return review['alcohol_id']

    @staticmethod
    async def get_rating(
            collection: Collection[Review],
            review_id: str,
    ) -> int:
        review = collection.find_one({'_id': ObjectId(review_id)})
        return review['rating']

    @staticmethod
    async def check_if_review_exists_by_id(
            collection: Collection[Review],
            review_id: str,
    ) -> bool:
        if collection.find_one({'_id': ObjectId(review_id)}):
            return True
        else:
            return False

    @staticmethod
    async def update_review(
            collection: Collection[Review],
            review_id: str,
            payload: ReviewUpdate
    ):
        return collection.find_one_and_update(
            {'_id': ObjectId(review_id)},
            {'$set': payload.dict(exclude_none=True)},
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    async def delete_review_admin(
            collection: Collection[Review],
            review_id: str
    ):
        return collection.delete_one({'_id': ObjectId(review_id)})

    @staticmethod
    async def check_if_user_exists(
            collection: Collection[UserBase],
            user_name: str
    ) -> bool:
        if collection.find_one({'username': user_name}):
            return True
        else:
            return False

    @staticmethod
    async def get_user_reviews(
            collection: Collection[UserBase],
            limit: int,
            offset: int,
            user_name: str
    ) -> list[Review]:
        print(list(collection.find({'user_name': user_name}).skip(offset).limit(limit)))
        return (
            list(collection.find({'user_name': user_name}).skip(offset).limit(limit))
        )

    @staticmethod
    async def count_user_reviews(
            collection: Collection[UserBase],
            user_name: str
    ) -> int:
        return (
            collection.count_documents(filter={'user_name': {'$eq': user_name}})
        )
