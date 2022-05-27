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
    async def count_alcohols_in_favourites(
            collection: Collection[Favourites],
            user_id: str = None
    ) -> int:
        return (
            collection.count_documents(filter={'user_id': {'$eq': ObjectId(user_id)}})
        )
