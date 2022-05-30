from bson import ObjectId
from pymongo.collection import Collection

from src.infrastructure.database.models.followers.followers import Followers
from src.infrastructure.database.models.followers.following import Following
from src.infrastructure.database.models.user import User, UserDatabaseHandler


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

    @staticmethod
    async def delete_user_from_followers(collection: Collection[Followers], user_id: str,
                                         follower_user_id: str) -> None:
        collection.update_one({'_id': ObjectId(user_id)}, {'$pull': {'followers': ObjectId(follower_user_id)}})

    @staticmethod
    async def add_user_to_followers(collection: Collection[Followers], user_id: str, follower_user_id: str) -> None:
        collection.update_one({'_id': ObjectId(user_id)}, {'$push': {'followers': ObjectId(follower_user_id)}})

    @staticmethod
    async def check_if_user_in_followers(collection: Collection[Followers], user_id: str,
                                         follower_user_id: str) -> bool:
        if collection.find_one({'_id': ObjectId(user_id), 'followers': ObjectId(follower_user_id)}):
            return True
        else:
            return False

    @staticmethod
    async def create_followers_and_following_lists(
            user_collection: Collection[User],
            username: str,
            followers_collection: Collection[Followers],
            following_collection: Collection[Following],
    ) -> None:
        user = await UserDatabaseHandler.get_user_by_username(user_collection, username)
        empty_followers = Followers(_id=user['_id'], followers=[])
        followers_collection.insert_one(empty_followers)
        empty_following = Following(_id=user['_id'], following=[])
        following_collection.insert_one(empty_following)
