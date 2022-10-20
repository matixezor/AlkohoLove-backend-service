from datetime import datetime
from pymongo import DESCENDING
from bson import ObjectId, Int64
from pymongo.collection import Collection, ReturnDocument

from src.domain.review import ReviewCreate
from src.domain.review.review_update import ReviewUpdate
from src.infrastructure.database.models.review import Review
from src.infrastructure.database.models.review.banned_review import BannedReview


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
    async def get_reported_reviews(
            collection: Collection[Review],
            limit: int,
            offset: int,
    ) -> list[Review]:
        return (
            list(collection.find(filter={'report_count': {'$gt': 0}})
                 .skip(offset)
                 .limit(limit)
                 .sort("report_count", DESCENDING))
        )

    @staticmethod
    async def get_reported_reviews_by_phrase(
            collection: Collection[Review],
            phrase: str,
            limit: int,
            offset: int,
    ) -> list[Review]:
        return (
            list(collection.find(
                {'$and': [{'report_count': {'$gt': 0}}, {'username': {'$regex': phrase, '$options': 'i'}}]})
                 .skip(offset)
                 .limit(limit)
                 .sort("report_count", DESCENDING))
        )

    @staticmethod
    async def count_reported_reviews(
            collection: Collection[Review]
    ) -> int:
        return (
            collection.count_documents(filter={'report_count': {'$gt': 0}})
        )

    @staticmethod
    async def count_reported_reviews_by_phrase(
            collection: Collection[Review],
            phrase: str
    ) -> int:
        return (
            collection.count_documents(
                filter={'$and': [{'report_count': {'$gt': 0}}, {'username': {'$regex': phrase, '$options': 'i'}}]})
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
        avg_rating = rate_value / rate_count

        collection.update_one(
            {'_id': {'$eq': ObjectId(alcohol_id)}},
            {
                '$set': {'rate_count': Int64(rate_count), 'avg_rating': avg_rating, 'rate_value': Int64(rate_value)}
            }
        )

    @staticmethod
    async def add_rating_to_user(
            collection: Collection,
            user_id: ObjectId,
            rating: int,
    ):
        user = collection.find_one({'_id': user_id})

        rate_count = user['rate_count'] + 1
        rate_value = user['rate_value'] + rating
        avg_rating = rate_value/rate_count

        collection.update_one(
            {'_id': {'$eq': ObjectId(user_id)}},
            {
                '$set': {
                    'rate_count': Int64(rate_count),
                    'avg_rating': float(avg_rating),
                    'rate_value': Int64(rate_value)
                }
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
            avg_rating = rate_value / rate_count

        collection.update_one(
            {'_id': {'$eq': ObjectId(alcohol_id)}},
            {
                '$set': {
                    'rate_count': Int64(rate_count),
                    'avg_rating': float(avg_rating),
                    'rate_value': Int64(rate_value)
                }
            }
        )

    @staticmethod
    async def remove_rating_from_user(
            collection: Collection,
            user_id: ObjectId,
            rating: int,
    ):
        user = collection.find_one({'_id': user_id})

        rate_count = user['rate_count'] - 1
        rate_value = user['rate_value'] - rating
        if rate_count < 1:
            avg_rating = 0
        else:
            avg_rating = rate_value/rate_count

        collection.update_one(
            {'_id': {'$eq': ObjectId(user_id)}},
            {
                '$set': {
                    'rate_count': Int64(rate_count),
                    'avg_rating': float(avg_rating),
                    'rate_value': Int64(rate_value)
                }
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
                '$set': {
                    'rate_count': Int64(rate_count),
                    'avg_rating': float(avg_rating),
                    'rate_value': Int64(rate_value)
                }
            }
        )

    @staticmethod
    async def update_user_rating(
            collection: Collection,
            user_id: ObjectId,
            rating_old: int,
            rating_new: int
    ):
        user = collection.find_one({'_id': user_id})
        rate_count = user['rate_count']
        rate_value = user['rate_value'] - rating_old + rating_new
        avg_rating = rate_value / rate_count

        collection.update_one(
            {'_id': {'$eq': user_id}},
            {
                '$set': {'rate_count': Int64(rate_count), 'avg_rating': float(avg_rating),
                         'rate_value': Int64(rate_value)}
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
            reporters=[],
            helpful_count=0,
            helpful_reporters=[]
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
            review_id: ObjectId,
            alcohol_id: ObjectId
    ) -> int:
        delete = collection.delete_one({'_id': review_id, 'alcohol_id': alcohol_id})
        return delete.deleted_count

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
    async def add_to_helpful_reporters(
            collection: Collection[Review],
            review_id: ObjectId,
            user_id: ObjectId
    ):
        return collection.find_one_and_update(
            {'_id': review_id},
            {'$inc': {'helpful_count': 1}, '$push': {'helpful_reporters': user_id}},
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    async def remove_from_helpful_reporters(
            collection: Collection[Review],
            review_id: ObjectId,
            user_id: ObjectId
    ):
        return collection.find_one_and_update(
            {'_id': review_id},
            {"$inc": {'helpful_count': -1}, '$pull': {'helpful_reporters': user_id}},
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
            review_collection: Collection[Review],
            alcohol_collection: Collection,
            limit: int,
            offset: int,
            user_id: ObjectId
    ) -> list[Review]:
        reviews = list(review_collection.find({'user_id': user_id}).skip(offset).limit(limit))
        for review in reviews:
            alcohol = alcohol_collection.find_one({'_id': review["alcohol_id"]})
            review['alcohol_name'] = alcohol['name']
            review['kind'] = alcohol['kind']
        return reviews

    @staticmethod
    async def count_user_reviews(
            collection: Collection[Review],
            user_id: ObjectId
    ) -> int:
        return (
            collection.count_documents(filter={'user_id': {'$eq': user_id}})
        )

    @staticmethod
    async def check_if_user_is_in_reporters(
            collection: Collection[Review],
            user_id: ObjectId,
            review_id: ObjectId
    ) -> bool:
        if collection.find_one({'reporters': user_id, '_id': review_id}):
            return True
        else:
            return False

    @staticmethod
    async def add_user_to_reporters(
            collection: Collection[Review],
            user_id: ObjectId,
            review_id: ObjectId
    ) -> None:
        collection.update_one({'_id': review_id}, {'$push': {'reporters': user_id}})

    @staticmethod
    async def increase_review_report_count(
            collection: Collection[Review],
            review_id: ObjectId
    ) -> None:
        collection.update_one({'_id': review_id}, {'$inc': {'report_count': 1}})

    @staticmethod
    async def get_review_by_id(
            collection: Collection[Review],
            review_id: ObjectId,
    ) -> Review:
        return collection.find_one({'_id': review_id})

    @staticmethod
    async def copy_review_to_banned_collection(
            collection: Collection[Review],
            banned_reviews_collection: Collection[BannedReview],
            review_id: ObjectId,
            reason: str
    ) -> BannedReview:
        db_banned_review = collection.find_one({'_id': review_id})
        db_banned_review = BannedReview(
            **dict(db_banned_review),
            ban_date=datetime.now(),
            reason=reason
        )
        banned_reviews_collection.insert_one(dict(db_banned_review))
        return db_banned_review

    @staticmethod
    async def get_user_banned_reviews(
            collection: Collection[BannedReview],
            limit: int,
            offset: int,
            user_id: ObjectId
    ) -> list[BannedReview]:
        return (
            list(collection.find({'user_id': user_id}).skip(offset).limit(limit))
        )

    @staticmethod
    async def count_user_banned_reviews(
            collection: Collection[BannedReview],
            user_id: ObjectId
    ) -> int:
        return (
            collection.count_documents(filter={'user_id': {'$eq': user_id}})
        )
