from fastapi import HTTPException
from sqlalchemy import Column, Integer, String, select, func, delete, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload
from starlette import status

from src.database.database_metadata import Base
from src.domain.reported_error import ReportedErrorCreate


class ReportedError(Base):
    __tablename__ = 'reported_error'

    error_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    description = Column(String, nullable=False)

    user = relationship('User', uselist=False, viewonly=True)


class ReportedErrorDatabaseHandler:
    @staticmethod
    def raise_error_already_exists(reason: str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error with given {reason} already exists'
        )

    @staticmethod
    async def get_reported_error_by_id(db: AsyncSession, error_id: int) -> ReportedError | None:
        query = select(ReportedError).options(selectinload(ReportedError.user))
        result = await db.execute(query)
        return result.scalar_one()

    # @staticmethod
    # async def get_reported_errors_by_user_id(db: AsyncSession, user_id: int) -> ReportedError | None:
    #     query = select(ReportedError).filter(ReportedError.user_id == user_id)
    #     result = await db.execute(query)
    #     return result.scalars().all()

    @staticmethod
    async def get_reported_errors(db: AsyncSession, limit: int, offset: int) -> list[ReportedError]:
        query = select(ReportedError).offset(offset).limit(limit).options(selectinload(ReportedError.user))
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def count_reported_errors(db: AsyncSession) -> int:
        query = select(func.count()).select_from(select(ReportedError).subquery())
        result = await db.execute(query)
        return result.scalar_one()

    @staticmethod
    async def delete_reported_error(db: AsyncSession, error_id: int) -> None:
        query = delete(ReportedError). \
            where(ReportedError.error_id == error_id)
        await db.execute(query)

    @staticmethod
    async def create_reported_error(db: AsyncSession, reported_error_create_payload: ReportedErrorCreate) -> None:
        db_reported_error = ReportedError(
            **reported_error_create_payload.dict(exclude_none=True),
        )
        db.add(db_reported_error)

    # @staticmethod
    # async def update_reported_error_by_id(
    #         db: AsyncSession,
    #         error_id: int,
    #         reported_error_update_payload: ReportedErrorBase
    # ) -> ReportedError:
    #     query = update(ReportedError) \
    #         .where(ReportedError.error_id == error_id) \
    #         .values(reported_error_update_payload.dict(exclude_none=True))
    #     await db.execute(query)
    #     await db.commit()
    #     return await ReportedErrorDatabaseHandler.get_reported_error_by_id(db, error_id=error_id)
