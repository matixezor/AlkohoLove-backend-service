from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status, HTTPException
from sqlalchemy import Column, Integer, String, delete, select, ForeignKey, func
from sqlalchemy.orm import relationship, selectinload

from src.database.database_metadata import Base
from src.database.models.alcohol import AlcoholDatabaseHandler
from src.domain.user_tag import UserTagCreate, UserTagAlcohols, UserTagUpdateAlcohols


class UserTag(Base):
    __tablename__ = 'user_tag'

    tag_id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    alcohols = relationship('Alcohol', secondary='alcohol_user_tag')


class AlcoholUserTag(Base):
    __tablename__ = 'alcohol_user_tag'

    alcohol_id = Column(Integer, ForeignKey('alcohol.alcohol_id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('user_tag.tag_id'), primary_key=True)


class UserTagDatabaseHandler:
    @staticmethod
    def raise_user_tag_already_exists():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'User tag with given name and user id already exists'
        )

    @staticmethod
    async def create_user_tag(db: AsyncSession, payload: UserTagCreate) -> None:
        fields_to_exclude = {'alcohol_ids'}
        db_user_tag = UserTag(
            **payload.dict(exclude_none=True, exclude=fields_to_exclude),
        )

        if payload.alcohol_ids:
            db_alcohols = await AlcoholDatabaseHandler.get_alcohols_without_pagination(db, payload.alcohol_ids)
            db_user_tag.alcohols = db_alcohols

        db.add(db_user_tag)
        await db.commit()
        await db.refresh(db_user_tag)

    @staticmethod
    async def check_if_user_tag_exists(db: AsyncSession, tag_name, user_id) -> None:
        if await UserTagDatabaseHandler.get_tag_by_name_and_user_id(db, tag_name, user_id):
            UserTagDatabaseHandler.raise_user_tag_already_exists()

    @staticmethod
    async def get_tag_by_name_and_user_id(db: AsyncSession, tag_name, user_id) -> UserTag | None:
        query = select(UserTag)\
            .filter((UserTag.tag_name == tag_name) & (UserTag.user_id == user_id))\
            .limit(1)
        result = await db.execute(query)
        return result.scalars().first()

    @staticmethod
    async def get_user_tags_by_user_id(
            db: AsyncSession,
            limit: int,
            offset: int,
            user_id: int
    ) -> list[UserTag]:
        query = select(UserTag).order_by(UserTag.tag_id)\
            .filter(UserTag.user_id == user_id)\
            .offset(offset)\
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
    async def get_user_tag_by_id(db: AsyncSession, tag_id: int) -> UserTag | None:
        query = select(UserTag).filter(UserTag.tag_id == tag_id).options(selectinload(UserTag.alcohols))
        result = await db.execute(query)
        return result.scalars().first()

    # @staticmethod
    # async def get_user_tag_with_alcohols_paginated(db: AsyncSession, tag_id: int) -> UserTag | None:
    #     db_tag = await db.get(UserTag, tag_id)
    #     db_tag.alcohols = await AlcoholDatabaseHandler.get_alcohols(db, payload.alcohol_ids)
    #     return db_tag

    @staticmethod
    async def delete_user_tag(db: AsyncSession, tag_id: int) -> None:
        query = delete(UserTag).\
            where(UserTag.tag_id == tag_id)
        await db.execute(query)

    # @staticmethod
    # async def update_user_tag_alcohols(db: AsyncSession, tag_id: int, payload: UserTagUpdateAlcohols) -> UserTag:
    #     # fields_to_exclude = {'alcohol_ids'}
    #     db_user_tag = await UserTagDatabaseHandler.get_user_tag_by_id(db, tag_id)
    #
    #     # payload_dict = payload.dict(exclude_none=True, exclude=fields_to_exclude)
    #     db_alcohols = await AlcoholDatabaseHandler.get_alcohols_without_pagination(db, payload.alcohol_ids)
    #     db_user_tag.alcohols = db_alcohols
    #
    #     await db.commit()
    #     await db.refresh(db_user_tag)
    #     return db_user_tag