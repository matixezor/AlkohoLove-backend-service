from bson import ObjectId
from pymongo.collection import Collection

from src.infrastructure.database.models.user import User
from src.infrastructure.database.models.socials.following import Following


class FollowingDatabaseHandler:

    @staticmethod
    async def get_following_by_user_id(
            limit: int,
            offset: int,
            following_collection: Collection[Following],
            users_collection: Collection[User],
            user_id: ObjectId = None,
    ) -> list[dict]:
        following = following_collection.find_one({'_id': user_id}, {'following': 1})
        following = following['following']

        return (
            list(users_collection.find({'_id': {'$in': following}}).skip(offset).limit(limit))
        )

    @staticmethod
    async def delete_user_from_following(collection: Collection[Following], user_id: ObjectId,
                                         following_user_id: ObjectId) -> None:
        collection.update_one({'_id': user_id}, {'$pull': {'following': following_user_id}})

    @staticmethod
    async def add_user_to_following(collection: Collection[Following], user_id: ObjectId,
                                    following_user_id: ObjectId) -> None:
        collection.update_one({'_id': user_id}, {'$push': {'following': following_user_id}})

    @staticmethod
    async def increase_following_counter(collection: Collection, current_user_id: ObjectId) -> None:
        user = collection.find_one({'_id': current_user_id})

        following_count = user['following_count'] + 1

        collection.update_one(
            {'_id': {'$eq': ObjectId(current_user_id)}},
            {
                '$set': {'following_count': following_count}
            }
        )

    @staticmethod
    async def decrease_following_counter(collection: Collection, current_user_id: ObjectId) -> None:
        user = collection.find_one({'_id': current_user_id})

        if user['following_count'] > 0:
            following_count = user['following_count'] - 1

            collection.update_one(
                {'_id': {'$eq': ObjectId(current_user_id)}},
                {
                    '$set': {'following_count': following_count}
                }
            )

    @staticmethod
    async def check_if_user_in_following(collection: Collection[Following], user_id: ObjectId,
                                         following_user_id: ObjectId) -> bool:
        if collection.find_one({'_id': user_id, 'following': following_user_id}):
            return True
        else:
            return False

    @staticmethod
    async def count_following(
            following_collection: Collection[Following],
            users_collection: Collection,
            user_id: ObjectId
    ) -> int:
        following = following_collection.find_one({'_id': user_id}, {'following': 1})
        following = following['following']

        return len(list(users_collection.find({'_id': {'$in': following}})))
