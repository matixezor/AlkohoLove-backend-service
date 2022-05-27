from bson import ObjectId
from pymongo.collection import Collection

from src.domain.alcohol import AlcoholBase
from src.infrastructure.database.models.user_list.wishlist import UserWishlist


class UserWishlistHandler:
    @staticmethod
    async def get_user_wishlist_by_user_id(
            limit: int,
            offset: int,
            wishlist_collection: Collection[UserWishlist],
            alcohols_collection: Collection[AlcoholBase],
            user_id: str = None,
    ) -> list[dict]:
        wishlist = list(
            wishlist_collection.find({'user_id': ObjectId(user_id)}, {'alcohols': 1}))
        wishlist = wishlist[0]['alcohols']

        return (
            list(alcohols_collection.find({'_id': {'$in': wishlist}}).skip(offset).limit(limit))
        )
    @staticmethod
    async def count_alcohols_in_wishlist(
            collection: Collection[UserWishlist],
            user_id: str = None
    ) -> int:
        return (
            collection.count_documents(filter={'user_id': {'$eq': ObjectId(user_id)}})
        )
