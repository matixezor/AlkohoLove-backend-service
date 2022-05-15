import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, relationship
from sqlalchemy import select, Column, Integer, ForeignKey, delete, TIMESTAMP

from src.domain.user import UserAdminInfo
from src.database.models import Alcohol, User
from src.database.database_metadata import Base


class UserSearchHistory(Base):
    __tablename__ = 'user_search_history'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    date = Column(TIMESTAMP, primary_key=True)

    alcohol = relationship("Alcohol")


class UserWishlist(Base):
    __tablename__ = 'user_wishlist'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

    alcohol = relationship("Alcohol")


class UserFavouriteAlcohol(Base):
    __tablename__ = 'user_favourite_alcohol'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

    alcohol = relationship("Alcohol")


class UserListHandler:
    @staticmethod
    async def get_user_search_history(
            user: UserAdminInfo,
            db: AsyncSession,
            limit: int,
            offset: int
    ) -> list[UserSearchHistory] | None:
        query = select(UserSearchHistory).filter(UserSearchHistory.user_id == user.user_id).offset(offset). \
            limit(limit).options(
            selectinload(UserSearchHistory.alcohol).selectinload(Alcohol.barcodes))
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_user_search_history_by_id(
            user_id: int,
            db: AsyncSession,
            limit: int,
            offset: int
    ) -> list[UserSearchHistory] | None:
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
    async def delete_whole_user_search_history(
            user: UserAdminInfo,
            db: AsyncSession,
    ) -> None:
        query = delete(UserSearchHistory). \
            where((UserSearchHistory.user_id == user.user_id))
        await db.execute(query)

    @staticmethod
    async def get_user_wishlist(
            user: UserAdminInfo,
            db: AsyncSession,
            limit: int,
            offset: int,
    ) -> list[UserWishlist] | None:
        query = select(UserWishlist).filter(UserWishlist.user_id == user.user_id).offset(offset). \
            limit(limit).options(
            selectinload(UserWishlist.alcohol).selectinload(Alcohol.barcodes))
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_user_favourites_list(
            user: UserAdminInfo,
            db: AsyncSession,
            limit: int,
            offset: int,
    ) -> list[UserFavouriteAlcohol] | None:
        query = select(UserFavouriteAlcohol).filter(UserFavouriteAlcohol.user_id == user.user_id).offset(offset). \
            limit(limit).options(
            selectinload(UserFavouriteAlcohol.alcohol).selectinload(Alcohol.barcodes))
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_user_wishlist_by_user_id(
            user_id: int,
            db: AsyncSession,
            limit: int,
            offset: int,
    ) -> list[UserWishlist] | None:
        query = select(UserWishlist).filter(UserWishlist.user_id == user_id).offset(offset). \
            limit(limit).options(
            selectinload(UserWishlist.alcohol).selectinload(Alcohol.barcodes))
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_user_favourites_by_user_id(
            user_id: int,
            db: AsyncSession,
            limit: int,
            offset: int,
    ) -> list[UserFavouriteAlcohol] | None:
        query = select(UserFavouriteAlcohol).filter(UserFavouriteAlcohol.user_id == user_id).offset(offset). \
            limit(limit).options(
            selectinload(UserFavouriteAlcohol.alcohol).selectinload(Alcohol.barcodes))
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

    @staticmethod
    async def get_alcohol_by_id(db: AsyncSession, alcohol_id: int, user_id, model) -> Alcohol | None:
        query = select(model).filter((model.alcohol_id == alcohol_id) & (model.user_id == user_id)).limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def check_if_alcohol_in_list(
            model,
            db: AsyncSession,
            alcohol_id: int,
            user_id: int
    ) -> bool:
        db_alcohol = await UserListHandler.get_alcohol_by_id(db, alcohol_id, user_id, model)
        if db_alcohol:
            return True if db_alcohol.alcohol_id == alcohol_id else False
        else:
            return False

    @staticmethod
    async def create_list_entry(db: AsyncSession, user_id: int, alcohol_id: int, model) -> None:
        db_list = model(user_id=user_id, alcohol_id=alcohol_id)
        db.add(db_list)

    @staticmethod
    async def create_search_history_entry(db: AsyncSession, user_id: int, alcohol_id: int) -> None:
        db_list = UserSearchHistory(user_id=user_id, alcohol_id=alcohol_id, date=datetime.datetime.now())
        db.add(db_list)
