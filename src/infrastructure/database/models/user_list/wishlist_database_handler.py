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
        wishlist = wishlist_collection.find_one({'user_id': ObjectId(user_id)}, {'alcohols_and_dates': 1})
        wishlist = wishlist['alcohols_and_dates']
        return list(alcohols_collection.find({'_id': {'$in': wishlist}}).skip(offset).limit(limit))

    @staticmethod
    async def delete_alcohol_from_wishlist(collection: Collection[UserWishlist], user_id: str, alcohol_id: str) -> None:
        collection.update_one({'user_id': ObjectId(user_id)}, {'$pull': {'alcohols_and_dates': ObjectId(alcohol_id)}})

    @staticmethod
    async def add_alcohol_to_wishlist(collection: Collection[UserWishlist], user_id: str, alcohol_id: str) -> None:
        collection.update_one({'user_id': ObjectId(user_id)}, {'$push': {'alcohols_and_dates': ObjectId(alcohol_id)}})

    @staticmethod
    async def check_if_alcohol_in_wishlist(collection: Collection[UserWishlist], user_id: str, alcohol_id: str) -> bool:
        if collection.find_one({'user_id': ObjectId(user_id), 'alcohols_and_dates': ObjectId(alcohol_id)}):
            return True
        else:
            return False

    @staticmethod
    async def count_alcohols_in_wishlist(
            wishlist_collection: Collection[UserWishlist],
            alcohols_collection: Collection,
            user_id: str
    ) -> int:
        alcohols = wishlist_collection.find_one({'user_id': ObjectId(user_id)}, {'alcohols_and_dates': 1})
        alcohols = alcohols['alcohols_and_dates']

        return len(list(alcohols_collection.find({'_id': {'$in': alcohols}})))
