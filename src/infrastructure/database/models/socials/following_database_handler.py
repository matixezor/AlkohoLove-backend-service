from bson import ObjectId
from pymongo.collection import Collection

from src.infrastructure.database.models.user import User
from src.infrastructure.database.models.socials.followers import Followers
from src.infrastructure.database.models.socials.following import Following
from src.infrastructure.database.models.socials.followers_database_handler import FollowersDatabaseHandler


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
                                         following_user_id: ObjectId) -> int:
        update = collection.update_one({'_id': user_id}, {'$pull': {'following': following_user_id}})
        return update.modified_count

    @staticmethod
    async def add_user_to_following(collection: Collection[Following], user_id: ObjectId,
                                    following_user_id: ObjectId) -> None:
        collection.update_one({'_id': user_id}, {'$push': {'following': following_user_id}})

    @staticmethod
    async def increase_following_counter(collection: Collection, current_user_id: ObjectId) -> None:
        collection.update_one(
            {'_id': {'$eq': ObjectId(current_user_id)}},
            {
                '$inc': {'following_count': 1}
            }
        )

    @staticmethod
    async def decrease_following_counter(collection: Collection, current_user_id: ObjectId) -> None:
        collection.update_one(
            {
                '_id': {'$eq': current_user_id},
                'following_count': {'$gt': 0}
            },
            {
                '$inc': {'following_count': -1}
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

    @staticmethod
    async def batch_decrease_following_counter(collection: Collection[User], user_ids: [ObjectId]) -> None:
        collection.update_many(
            {
                '_id': {'$in': user_ids},
                'following_count': {'$gt': 0}
            },
            {
                '$inc': {'following_count': -1}
            }
        )

    @staticmethod
    async def delete_user_following(
            following_collection: Collection[Following],
            followers_collection: Collection[Followers],
            users: Collection[User],
            user_id: ObjectId
    ):
        followed_users = following_collection.find_one({'_id': user_id}, {'following': 1, '_id': 0})
        followed_users = followed_users.get('following')
        following_collection.delete_one({'_id': user_id})
        await FollowersDatabaseHandler.delete_user_from_many_followers_list(followers_collection, followed_users,
                                                                            user_id)
        await FollowersDatabaseHandler.batch_decrease_followers_counter(users, followed_users)

    @staticmethod
    async def delete_user_followers(
            followers_collection: Collection[Followers],
            following_collection: Collection[Following],
            users: Collection[User],
            user_id: ObjectId
    ):
        users_following_me = followers_collection.find_one({'_id': user_id}, {'followers': 1, '_id': 0})
        users_following_me = users_following_me.get('followers')
        followers_collection.delete_one({'_id': user_id})
        if users_following_me:
            await FollowingDatabaseHandler.delete_user_from_multiple_following_lists(following_collection,
                                                                                     users_following_me, user_id)
            await FollowingDatabaseHandler.batch_decrease_following_counter(users, users_following_me)

    @staticmethod
    async def delete_user_from_multiple_following_lists(
            collection: Collection[Following],
            user_ids: list[ObjectId],
            follower_user_id: ObjectId
    ):
        collection.update_many({'_id': {'$in': user_ids}}, {'$pull': {'following': follower_user_id}})
