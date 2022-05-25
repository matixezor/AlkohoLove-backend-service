from bson import ObjectId
from pymongo.collection import Collection

from src.infrastructure.database.models.user_list.wishlist import UserWishlist


class UserListHandler:
    @staticmethod
    async def get_user_wishlist_by_user_id(
            user_id: str,
            collection: Collection[UserWishlist],
            limit: int,
            offset: int,
    ) -> list[UserWishlist]:
        return (
            list(collection.find({'user_id': ObjectId(user_id)}).skip(offset).limit(limit))
        )
