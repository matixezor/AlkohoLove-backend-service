from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Column, Integer, String, delete, select, ForeignKey, func, insert, update

from src.domain.alcohol import AlcoholBase
from src.domain.user_tag import UserTagCreate
from src.database.database_metadata import Base
from src.database.models.alcohol import AlcoholDatabaseHandler, Alcohol


class UserTag(Base):
    __tablename__ = 'user_tag'

    tag_id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    alcohols = relationship('Alcohol', secondary='alcohol_user_tag', back_populates='user_tags')


class AlcoholUserTag(Base):
    __tablename__ = 'alcohol_user_tag'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('user_tag.tag_id'), primary_key=True)


class UserTagDatabaseHandler:

    @staticmethod
    async def create_user_tag(db: AsyncSession, payload: UserTagCreate, user_id: int) -> None:
        fields_to_exclude = {'alcohol_ids'}
        db_user_tag = UserTag(
            **payload.dict(exclude=fields_to_exclude),
        )
        db_user_tag.user_id = user_id
        if payload.alcohol_ids:
            db_alcohols = await AlcoholDatabaseHandler.get_alcohols_without_pagination(db, payload.alcohol_ids)
            db_user_tag.alcohols = db_alcohols

        db.add(db_user_tag)

    @staticmethod
    async def get_user_tag_by_id(db: AsyncSession, tag_id: int) -> UserTag:
        return await db.get(UserTag, tag_id)

    @staticmethod
    async def add_alcohol_to_user_tag(db: AsyncSession, tag_id: int, alcohol_id: int) -> None:
        query = insert(AlcoholUserTag).values(alcohol_id=alcohol_id, tag_id=tag_id)
        await db.execute(query)
        await db.commit()

    @staticmethod
    async def delete_alcohol_from_user_tag(db: AsyncSession, tag_id: int, alcohol_id: int) -> None:
        query = delete(AlcoholUserTag). \
            where((AlcoholUserTag.tag_id == tag_id) & (AlcoholUserTag.alcohol_id == alcohol_id))
        await db.execute(query)

    @staticmethod
    async def check_if_user_tag_exists(db: AsyncSession, tag_name: str, user_id: int) -> bool:
        if await UserTagDatabaseHandler.get_user_tag_by_name_and_user_id(db, tag_name, user_id):
            return True
        else:
            return False

    @staticmethod
    async def check_if_user_tag_exists_by_id(db: AsyncSession, tag_id: int) -> bool:
        if await UserTagDatabaseHandler.get_user_tag_by_id(db, tag_id):
            return True
        else:
            return False

    @staticmethod
    async def check_if_user_tag_belongs_to_user(db, tag_id: int, user_id: int) -> bool:
        if await UserTagDatabaseHandler.get_user_tag_by_tag_id_and_user_id(db, tag_id, user_id):
            return True
        else:
            return False

    @staticmethod
    async def check_if_alcohol_exists_in_user_tag(db: AsyncSession, tag_id: int, alcohol_id) -> bool:
        if await UserTagDatabaseHandler.get_user_tag_alcohol(db, tag_id, alcohol_id):
            return True
        else:
            return False

    @staticmethod
    async def get_user_tag_by_tag_id_and_user_id(db, tag_id: int, user_id: int) -> UserTag | None:
        query = select(UserTag) \
            .filter((UserTag.tag_id == tag_id) & (UserTag.user_id == user_id)) \
            .limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_tag_by_name_and_user_id(db: AsyncSession, tag_name: str, user_id: int) -> UserTag | None:
        query = select(UserTag) \
            .filter((UserTag.tag_name == tag_name) & (UserTag.user_id == user_id)) \
            .limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_tag_alcohol(db: AsyncSession, tag_id: int, alcohol_id: int) -> AlcoholUserTag | None:
        query = select(AlcoholUserTag). \
            filter((AlcoholUserTag.tag_id == tag_id) & (AlcoholUserTag.alcohol_id == alcohol_id)) \
            .limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_tags_by_user_id(
            db: AsyncSession,
            limit: int,
            offset: int,
            user_id: int,
    ) -> list[UserTag]:
        query = select(UserTag).order_by(UserTag.tag_id) \
            .filter(UserTag.user_id == user_id) \
            .offset(offset) \
            .limit(limit)

        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def count_user_tags(db: AsyncSession, user_id: int) -> int:
        query = select(func.count()).select_from(
            select(UserTag).filter(UserTag.user_id == user_id).subquery()
        )
        result = await db.execute(query)
        return result.scalar_one()

    @staticmethod
    async def get_user_tag_alcohols(
            db: AsyncSession,
            limit: int,
            offset: int,
            tag_id: int
    ) -> list[AlcoholBase]:
        query = select(Alcohol).join(AlcoholUserTag). \
            filter(AlcoholUserTag.tag_id == tag_id). \
            offset(offset). \
            limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def count_user_tag_alcohols(db: AsyncSession, tag_id: int) -> int:
        query = select(func.count()).select_from(
            select(AlcoholUserTag).filter(AlcoholUserTag.tag_id == tag_id).subquery()
        )
        result = await db.execute(query)
        return result.scalar_one()

    @staticmethod
    async def delete_user_tag(db: AsyncSession, tag_id: int) -> None:
        query = delete(UserTag). \
            where(UserTag.tag_id == tag_id)
        await db.execute(query)

    @staticmethod
    async def update_user_tag(
            db: AsyncSession,
            tag_id: int,
            tag_name: str
    ) -> UserTag:
        query = update(UserTag).where(UserTag.tag_id == tag_id).values(tag_name=tag_name)
        await db.execute(query)
        await db.commit()
        return await UserTagDatabaseHandler.get_user_tag_by_id(db, tag_id)
