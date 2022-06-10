from bson import ObjectId
from pymongo.collection import Collection

from src.domain.user_tag.user_tag_create import UserTagCreate
from src.infrastructure.database.models.user_tag import UserTag


class UserTagDatabaseHandler:
    @staticmethod
    async def get_user_tags(
            collection: Collection[UserTag],
            limit: int,
            offset: int,
            user_id: ObjectId
    ) -> list[UserTag]:
        return (
            list(collection.find({'user_id': user_id}).skip(offset).limit(limit))
        )

    @staticmethod
    async def count_user_tags(
            collection: Collection[UserTag],
            user_id: ObjectId
    ) -> int:
        return (
            collection.count_documents(filter={'user_id': {'$eq': user_id}})
        )

    @staticmethod
    async def delete_user_tag(
            collection: Collection[UserTag],
            tag_id: str
    ) -> None:
        collection.delete_one({'_id': ObjectId(tag_id)})

    @staticmethod
    async def check_if_user_tag_belongs_to_user(
            collection: Collection[UserTag],
            tag_id: str,
            user_id: ObjectId
    ) -> bool:
        if collection.find_one({'user_id': user_id, '_id': ObjectId(tag_id)}):
            return True
        else:
            return False

    @staticmethod
    async def check_if_user_tag_exists(
            collection: Collection[UserTag],
            tag_name: str,
            user_id: ObjectId
    ) -> bool:
        if collection.find_one({'user_id': user_id, 'tag_name': tag_name}):
            return True
        else:
            return False

    @staticmethod
    async def create_user_tag(
            collection: Collection[UserTag],
            user_id: ObjectId,
            payload: UserTagCreate
    ) -> None:
        db_user_tag = UserTag(
            **payload.dict(),
            user_id=user_id,
            alcohols=[]
        )
        collection.insert_one(db_user_tag)

    @staticmethod
    async def add_alcohol(
            collection: Collection[UserTag],
            tag_id: str,
            alcohol_id: str,
    ) -> None:
        collection.update_one({'_id': ObjectId(tag_id)}, {'$push': {'alcohols': ObjectId(alcohol_id)}})

    @staticmethod
    async def remove_alcohol(
            collection: Collection[UserTag],
            tag_id: str,
            alcohol_id: str,
    ) -> None:
        collection.update_one({'_id': ObjectId(tag_id)}, {'$pull': {'alcohols': ObjectId(alcohol_id)}})

    @staticmethod
    async def check_if_alcohol_is_in_user_tag(
            collection: Collection[UserTag],
            tag_id: str,
            alcohol_id: str
    ) -> bool:
        if collection.find_one({'alcohols': ObjectId(alcohol_id), '_id': ObjectId(tag_id)}):
            return True
        else:
            return False

    @staticmethod
    async def update_tag(
            collection: Collection[UserTag],
            tag_id: str,
            tag_name: str
    ) -> UserTag:
        collection.update_one({'_id':  ObjectId(tag_id)}, {'$set': {'tag_name': tag_name}})
        return collection.find_one({'_id': ObjectId(tag_id)})

    @staticmethod
    async def get_tag_alcohols(
            tag_id: str,
            limit: int,
            offset: int,
            tag_collection: Collection[UserTag],
            alcohols_collection: Collection,
    ) -> list[dict]:
        tag = tag_collection.find_one({'_id': ObjectId(tag_id)}, {'alcohols': 1})

        return (
            list(alcohols_collection.find({'_id': {'$in': tag['alcohols']}}).skip(offset).limit(limit))
        )

    @staticmethod
    async def count_alcohols(
            tag_id: str,
            tag_collection: Collection[UserTag],
            alcohols_collection: Collection,
    ):
        tag = tag_collection.find_one({'_id': ObjectId(tag_id)}, {'alcohols': 1})

        return (
            len(list(alcohols_collection.find({'_id': {'$in': tag['alcohols']}})))
        )

    @staticmethod
    async def check_if_tag_exists_by_id(
            collection: Collection[UserTag],
            tag_id: str
    ) -> bool:
        if collection.find_one({'_id': ObjectId(tag_id)}):
            return True
        else:
            return False
