from bson import ObjectId
from pymongo.collection import Collection


class UserWishlistHandler:
    @staticmethod
    async def get_user_wishlist_by_user_id(
            limit: int,
            offset: int,
            wishlist_collection: Collection,
            alcohols_collection: Collection,
            user_id: str = None,
    ) -> list[dict]:
        wishlist = list(
            wishlist_collection.find({'user_id': ObjectId(user_id)}, {'alcohols': 1}))
        wishlist = wishlist[0]['alcohols']

        return (
            list(alcohols_collection.find({'_id': {'$in': wishlist}}).skip(offset).limit(limit))
        )

