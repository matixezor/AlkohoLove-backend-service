from bson import ObjectId
from pymongo.collection import Collection

from src.infrastructure.database.models.followers.followed import Followed
from src.infrastructure.database.models.user import User


class FollowedDatabaseHandler:

    @staticmethod
    async def get_followers_by_user_id(
            limit: int,
            offset: int,
            followed_collection: Collection[Followed],
            users_collection: Collection[User],
            user_id: str = None,
    ) -> list[dict]:
        followed = list(followed_collection.find({'_id': ObjectId(user_id)}, {'followed': 1}))
        followed = followed[0]['followed']

        return (
            list(users_collection.find({'_id': {'$in': followed}}).skip(offset).limit(limit))
        )
