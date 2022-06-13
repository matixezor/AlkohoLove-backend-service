from bson import ObjectId, Int64
from datetime import datetime
from pymongo.collection import Collection, ReturnDocument


from src.domain.review import ReviewCreate
from src.domain.review.review_update import ReviewUpdate
from src.infrastructure.database.models.review import Review


class ReviewDatabaseHandler:
    @staticmethod
    async def get_alcohol_reviews(
            collection: Collection[Review],
            limit: int,
            offset: int,
            alcohol_id: str
    ) -> list[Review]:
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
    async def check_if_review_exists(
            collection: Collection[Review],
            alcohol_id: ObjectId,
            user_id: ObjectId,
    ) -> bool:
        if collection.find_one({'user_id': user_id, 'alcohol_id': alcohol_id}):
            return True
        else:
            return False

    @staticmethod
    async def add_rating_to_alcohol(
            collection: Collection,
            alcohol_id: ObjectId,
            rating: int,
    ):
        alcohol = collection.find_one({'_id': alcohol_id})

        rate_count = alcohol['rate_count'] + 1
        rate_value = alcohol['rate_value'] + rating
        avg_rating = rate_value/rate_count

        collection.update_one(
            {'_id': {'$eq': ObjectId(alcohol_id)}},
            {
                '$set': {'rate_count': Int64(rate_count), 'avg_rating': avg_rating, 'rate_value': Int64(rate_value)}
            }
        )

    @staticmethod
    async def remove_rating_from_alcohol(
            collection: Collection,
            alcohol_id: ObjectId,
            rating: int,
    ):
        alcohol = collection.find_one({'_id': alcohol_id})

        rate_count = alcohol['rate_count'] - 1
        rate_value = alcohol['rate_value'] - rating
        if rate_count < 1:
            avg_rating = 0
        else:
            avg_rating = rate_value/rate_count

        collection.update_one(
            {'_id': {'$eq': ObjectId(alcohol_id)}},
            {
                '$set': {'rate_count': Int64(rate_count), 'avg_rating': avg_rating, 'rate_value': Int64(rate_value)}
            }
        )

    @staticmethod
    async def update_alcohol_rating(
            collection: Collection,
            alcohol_id: ObjectId,
            rating_old: int,
            rating_new: int
    ):
        alcohol = collection.find_one({'_id': alcohol_id})
        rate_count = alcohol['rate_count']
        rate_value = alcohol['rate_value'] - rating_old + rating_new
        avg_rating = rate_value / rate_count

        collection.update_one(
            {'_id': {'$eq': alcohol_id}},
            {
                '$set': {'rate_count': Int64(rate_count), 'avg_rating': avg_rating, 'rate_value': Int64(rate_value)}
            }
        )

    @staticmethod
    async def create_review(
            collection: Collection[Review],
            user_id: ObjectId,
            alcohol_id: ObjectId,
            username: str,
            payload: ReviewCreate
    ):
        db_review = Review(
            **payload.dict(),
            user_id=user_id,
            alcohol_id=alcohol_id,
            username=username,
            date=datetime.now(),
            report_count=0,
            reporters=[]
        )
        return collection.insert_one(db_review)

    @staticmethod
    async def check_if_review_belongs_to_user(
            collection: Collection[Review],
            review_id: ObjectId,
            user_id: ObjectId
    ) -> bool:
        if collection.find_one({'user_id': user_id, '_id': review_id}):
            return True
        else:
            return False

    @staticmethod
    async def delete_review(
            collection: Collection[Review],
            review_id: ObjectId
    ):
        return collection.delete_one({'_id': review_id})

    @staticmethod
    async def get_rating(
            collection: Collection[Review],
            review_id: ObjectId,
    ) -> int:
        review = collection.find_one({'_id': review_id})
        return review['rating']

    @staticmethod
    async def check_if_review_exists_by_id(
            collection: Collection[Review],
            review_id: ObjectId,
    ) -> bool:
        if collection.find_one({'_id': review_id}):
            return True
        else:
            return False

    @staticmethod
    async def update_review(
            collection: Collection[Review],
            review_id: ObjectId,
            payload: ReviewUpdate
    ):
        return collection.find_one_and_update(
            {'_id': review_id},
            {'$set': payload.dict(exclude_none=True)},
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    async def delete_review_admin(
            collection: Collection[Review],
            review_id: ObjectId
    ):
        return collection.delete_one({'_id': review_id})

    @staticmethod
    async def get_user_reviews(
            collection: Collection[Review],
            limit: int,
            offset: int,
            user_id: ObjectId
    ) -> list[Review]:
        return (
            list(collection.find({'user_id': user_id}).skip(offset).limit(limit))
        )

    @staticmethod
    async def count_user_reviews(
            collection: Collection[Review],
            user_id: ObjectId
    ) -> int:
        return (
            collection.count_documents(filter={'user_id': {'$eq': user_id}})
        )
