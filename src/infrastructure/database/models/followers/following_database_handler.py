from bson import ObjectId
from pymongo.collection import Collection

from src.infrastructure.database.models.followers.following import Following
from src.infrastructure.database.models.user import User


class FollowingDatabaseHandler:

    @staticmethod
    async def get_following_by_user_id(
            limit: int,
            offset: int,
            following_collection: Collection[Following],
            users_collection: Collection[User],
            user_id: str = None,
    ) -> list[dict]:
        following = list(following_collection.find({'_id': ObjectId(user_id)}, {'following': 1}))
        following = following[0]['following']

        return (
            list(users_collection.find({'_id': {'$in': following}}).skip(offset).limit(limit))
        )

    @staticmethod
    async def delete_user_from_following(collection: Collection[Following], user_id: str, following_user_id: str) -> None:
        collection.update_one({'_id': ObjectId(user_id)}, {'$pull': {'following': ObjectId(following_user_id)}})

    @staticmethod
    async def add_user_to_following(collection: Collection[Following], user_id: str, following_user_id: str) -> None:
        collection.update_one({'_id': ObjectId(user_id)}, {'$push': {'following': ObjectId(following_user_id)}})

    @staticmethod
    async def check_if_user_in_following(collection: Collection[Following], user_id: str, following_user_id: str) -> bool:
        if collection.find_one({'_id': ObjectId(user_id), 'following': ObjectId(following_user_id)}):
            return True
        else:
            return False
