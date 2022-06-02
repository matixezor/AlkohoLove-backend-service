from bson import ObjectId
from pymongo.collection import Collection

from src.domain.alcohol import AlcoholBase
from src.infrastructure.database.models.user_list.favourites import Favourites


class UserFavouritesHandler:
    @staticmethod
    async def get_user_favourites_by_user_id(
            limit: int,
            offset: int,
            favourites_collection: Collection[Favourites],
            alcohols_collection: Collection[AlcoholBase],
            user_id: ObjectId,
    ) -> list[dict]:
        favourites = favourites_collection.find_one({'user_id': user_id}, {'alcohols': 1})
        favourites = favourites['alcohols']

        return list(alcohols_collection.find({'_id': {'$in': favourites}}).skip(offset).limit(limit))

    @staticmethod
    async def delete_alcohol_from_favourites(collection: Collection[Favourites], user_id: ObjectId,
                                             alcohol_id: str) -> None:
        collection.update_one({'user_id': user_id}, {'$pull': {'alcohols': ObjectId(alcohol_id)}})

    @staticmethod
    async def add_alcohol_to_favourites(collection: Collection[Favourites], user_id: ObjectId, alcohol_id: str) -> None:
        collection.update_one({'user_id': user_id}, {'$push': {'alcohols': ObjectId(alcohol_id)}})

    @staticmethod
    async def check_if_alcohol_in_favourites(collection: Collection[Favourites], user_id: ObjectId,
                                             alcohol_id: str) -> bool:
        if collection.find_one({'user_id': user_id, 'alcohols': ObjectId(alcohol_id)}):
            return True
        else:
            return False

    @staticmethod
    async def count_alcohols_in_favourites(
            favourites_collection: Collection[Favourites],
            alcohols_collection: Collection,
            user_id: ObjectId
    ) -> int:
        alcohols = favourites_collection.find_one({'user_id': user_id}, {'alcohols': 1})
        alcohols = alcohols['alcohols']

        return len(list(alcohols_collection.find({'_id': {'$in': alcohols}})))
