from bson import ObjectId
from pymongo.collection import Collection

from src.infrastructure.database.models.user_list.wishlist import UserWishlist


class UserWishlistHandler:
    @staticmethod
    async def get_user_wishlist_by_user_id(
            limit: int,
            offset: int,
            wishlist_collection: Collection[UserWishlist],
            alcohols_collection: Collection,
            user_id: str = None,
    ) -> list[dict]:
        wishlist = list(
            wishlist_collection.find({'user_id': ObjectId(user_id)}, {'alcohols': 1}))
        wishlist = wishlist[0]['alcohols']

        return (
            list(alcohols_collection.find({'_id': {'$in': wishlist}}).skip(offset).limit(limit))
        )

    @staticmethod
    async def delete_alcohol_from_wishlist(collection: Collection[UserWishlist], user_id: str, alcohol_id: str) -> None:
        collection.update_one({'user_id': ObjectId(user_id)}, {'$pull': {'alcohols': ObjectId(alcohol_id)}})
