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
            user_id: str = None,
    ) -> list[dict]:
        favourites = list(
            favourites_collection.find({'user_id': ObjectId(user_id)}, {'alcohols': 1}))
        favourites = favourites[0]['alcohols']

        return (
            list(alcohols_collection.find({'_id': {'$in': favourites}}).skip(offset).limit(limit))
        )

    @staticmethod
    async def delete_alcohol_from_favourites(collection: Collection[Favourites], user_id: str, alcohol_id: str) -> None:
        collection.update_one({'user_id': ObjectId(user_id)}, {'$pull': {'alcohols': ObjectId(alcohol_id)}})

    @staticmethod
    async def add_alcohol_to_favourites(collection: Collection[Favourites], user_id: str, alcohol_id: str) -> None:
        collection.update_one({'user_id': ObjectId(user_id)}, {'$push': {'alcohols': ObjectId(alcohol_id)}})