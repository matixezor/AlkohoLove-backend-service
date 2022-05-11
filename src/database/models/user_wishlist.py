from sqlalchemy import select, func, Column, Integer, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.database.database_metadata import Base
from src.database.models import Alcohol, User
from src.domain.user import UserAdminInfo
from src.domain.user_wishlist import PaginatedUserWishlist


class UserWishlist(Base):
    __tablename__ = 'user_wishlist'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)


class WishlistDatabaseHandler:  # WISHLIST
    @staticmethod
    async def get_user_wishlist(
            user: UserAdminInfo,
            db: AsyncSession,
            limit: int,
            offset: int
    ) -> Alcohol:
        query = select(Alcohol).join(UserWishlist).join(User).filter(User.user_id == user.user_id).offset(offset).limit(
            limit)
        result = await db.execute(query)
        return result.scalars().all()
