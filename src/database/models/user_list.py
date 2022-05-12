from sqlalchemy import select, Column, Integer, ForeignKey, Date, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database_metadata import Base
from src.database.models import Alcohol, User
from src.domain.user import UserAdminInfo


class UserSearchHistory(Base):
    __tablename__ = 'user_search_history'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    date = Column(Date)


class UserWishlist(Base):
    __tablename__ = 'user_wishlist'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)


class UserFavouriteAlcohol(Base):
    __tablename__ = 'user_favourite_alcohol'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)


class UserListHandler:
    @staticmethod
    async def get_user_search_history(
            user: UserAdminInfo,
            db: AsyncSession,
            limit: int,
            offset: int
    ) -> list[Alcohol] | None:
        query = select(Alcohol).join(UserSearchHistory).join(User).filter(User.user_id == user.user_id).offset(
            offset).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_user_search_history_by_id(
            user_id: int,
            db: AsyncSession,
            limit: int,
            offset: int
    ) -> list[Alcohol] | None:
        query = select(Alcohol).join(UserSearchHistory).join(User).filter(User.user_id == user_id).offset(offset).limit(
            limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def delete_from_user_search_history(
            user: UserAdminInfo,
            alcohol_id: int,
            db: AsyncSession,
    ) -> None:
        query = delete(UserSearchHistory). \
            where((UserSearchHistory.alcohol_id == alcohol_id) & (UserSearchHistory.user_id == user.user_id))
        await db.execute(query)

    @staticmethod
    async def get_user_list(
            user: UserAdminInfo,
            db: AsyncSession,
            limit: int,
            offset: int,
            model
    ) -> list[Alcohol] | None:
        query = select(Alcohol).join(model).join(User).filter(User.user_id == user.user_id).offset(offset).limit(
            limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_user_list_by_id(
            user_id: int,
            db: AsyncSession,
            limit: int,
            offset: int,
            model
    ) -> list[Alcohol] | None:
        query = select(Alcohol).join(model).join(User).filter(User.user_id == user_id).offset(offset).limit(
            limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def delete_from_user_list(
            user: UserAdminInfo,
            alcohol_id: int,
            db: AsyncSession,
            model
    ) -> None:
        query = delete(model). \
            where((model.alcohol_id == alcohol_id) & (model.user_id == user.user_id))
        await db.execute(query)