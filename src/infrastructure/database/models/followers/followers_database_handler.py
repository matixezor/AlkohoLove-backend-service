from bson import ObjectId
from pymongo.collection import Collection

from src.infrastructure.database.models.followers.followers import Followers
from src.infrastructure.database.models.user import User


class FollowersDatabaseHandler:

    @staticmethod
    async def get_followers_by_user_id(
            limit: int,
            offset: int,
            followers_collection: Collection[Followers],
            users_collection: Collection[User],
            user_id: str = None,
    ) -> list[dict]:
        followers = list(followers_collection.find({'_id': ObjectId(user_id)}, {'followers': 1}))
        followers = followers[0]['followers']

        return list(users_collection.find({'_id': {'$in': followers}}).skip(offset).limit(limit))