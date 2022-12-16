from bson import ObjectId
from pymongo.collection import Collection

from src.infrastructure.database.models.socials.followers import Followers
from src.infrastructure.database.models.socials.following import Following
from src.infrastructure.database.models.user import User, UserDatabaseHandler


class FollowersDatabaseHandler:

    @staticmethod
    async def get_followers_by_user_id(
            limit: int,
            offset: int,
            followers_collection: Collection[Followers],
            users_collection: Collection[User],
            user_id: ObjectId,
    ) -> list[dict]:
        followers = followers_collection.find_one({'_id': user_id}, {'followers': 1})
        followers = followers['followers']

        return list(users_collection.find({'_id': {'$in': followers}}).skip(offset).limit(limit))

    @staticmethod
    async def delete_user_from_followers(collection: Collection[Followers], user_id: ObjectId,
                                         follower_user_id: ObjectId) -> int:
        update = collection.update_one({'_id': user_id}, {'$pull': {'followers': follower_user_id}})
        return update.modified_count

    @staticmethod
    async def add_user_to_followers(collection: Collection[Followers], user_id: ObjectId,
                                    follower_user_id: ObjectId) -> None:
        collection.update_one({'_id': user_id}, {'$push': {'followers': follower_user_id}})

    @staticmethod
    async def increase_followers_counter(collection: Collection, other_user_id: ObjectId) -> None:
        collection.update_one(
            {'_id': {'$eq': ObjectId(other_user_id)}},
            {
                '$inc': {'followers_count': 1}
            }
        )

    @staticmethod
    async def decrease_followers_counter(collection: Collection, other_user_id: ObjectId) -> None:
        collection.update_one(
            {
                '_id': {'$eq': ObjectId(other_user_id)},
                'followers_count': {'$gt': 0}
            },
            {
                '$inc': {'followers_count': -1}
            }
        )

    @staticmethod
    async def batch_decrease_followers_counter(collection: Collection[User], user_ids: [ObjectId]) -> None:
        collection.update_many(
            {
                '_id': {'$in': user_ids},
                'followers_count': {'$gt': 0}
            },
            {
                '$inc': {'following_count': -1}
            }
        )

    @staticmethod
    async def check_if_user_in_followers(collection: Collection[Followers], user_id: ObjectId,
                                         follower_user_id: ObjectId) -> bool:
        if collection.find_one({'_id': user_id, 'followers': follower_user_id}):
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

    @staticmethod
    async def count_followers(
            followers_collection: Collection[Followers],
            users_collection: Collection,
            user_id: ObjectId,
            phrase: str | None = None
    ) -> int:
        followers = followers_collection.find_one({'_id': user_id}, {'followers': 1})
        followers = followers['followers']
        query = {'_id': {'$in': followers}}
        if phrase:
            query |= {'username': {'$regex': phrase, '$options': 'i'}}
        return users_collection.count_documents(filter=query)

    @staticmethod
    async def delete_user_from_many_followers_list(
            collection: Collection[Followers],
            user_ids: list[ObjectId],
            follower_user_id: ObjectId
    ):
        collection.update_many({'_id': {'$in': user_ids}}, {'$pull': {'followers': follower_user_id}})

    @staticmethod
    async def search_followers_by_user_id(
            limit: int,
            offset: int,
            followers_collection: Collection[Followers],
            users_collection: Collection[User],
            phrase: str | None,
            user_id: ObjectId,
    ) -> list[dict]:
        followers = followers_collection.find_one({'_id': user_id}, {'followers': 1})
        followers = followers['followers']
        query = {'_id': {'$in': followers}}
        if phrase:
            query |= {'username': {'$regex': phrase, '$options': 'i'}}
        return (
            list(users_collection.find(query).skip(offset).limit(limit))
        )
