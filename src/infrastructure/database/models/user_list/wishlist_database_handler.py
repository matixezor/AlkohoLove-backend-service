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
            user_id: ObjectId = None,
    ) -> list[dict]:
        wishlist = wishlist_collection.find_one({'user_id': user_id}, {'alcohols': 1})
        wishlist = wishlist['alcohols']
        return list(alcohols_collection.find({'_id': {'$in': wishlist}}).skip(offset).limit(limit))

    @staticmethod
    async def delete_alcohol_from_wishlist(collection: Collection[UserWishlist], user_id: ObjectId,
                                           alcohol_id: ObjectId) -> None:
        collection.update_one({'user_id': user_id}, {'$pull': {'alcohols': alcohol_id}})

    @staticmethod
    async def add_alcohol_to_wishlist(collection: Collection[UserWishlist], user_id: ObjectId,
                                      alcohol_id: ObjectId) -> None:
        collection.update_one({'user_id': user_id}, {'$push': {'alcohols': alcohol_id}})

    @staticmethod
    async def check_if_alcohol_in_wishlist(collection: Collection[UserWishlist], user_id: ObjectId,
                                           alcohol_id: ObjectId) -> bool:
        if collection.find_one({'user_id': user_id, 'alcohols': alcohol_id}):
            return True
        else:
            return False

    @staticmethod
    async def count_alcohols_in_wishlist(
            wishlist_collection: Collection[UserWishlist],
            alcohols_collection: Collection,
            user_id: ObjectId
    ) -> int:
        alcohols = wishlist_collection.find_one({'user_id': user_id}, {'alcohols': 1})
        alcohols = alcohols['alcohols']

        return len(list(alcohols_collection.find({'_id': {'$in': alcohols}})))
