from sqlalchemy import select, Column, Integer, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.database_metadata import Base
from src.database.models import Alcohol, User
from src.domain.user import UserAdminInfo


class UserFavouriteAlcohol(Base):
    __tablename__ = 'user_favourite_alcohol'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)


class UserFavouriteAlcoholDatabaseHandler:
    @staticmethod
    async def get_user_favourite_alcohols(
            user: UserAdminInfo,
            db: AsyncSession,
            limit: int,
            offset: int
    ) -> Alcohol:
        query = select(Alcohol).join(UserFavouriteAlcohol).join(User).filter(User.user_id == user.user_id).offset(offset).limit(
            limit)
        result = await db.execute(query)
        return result.scalars().all()
