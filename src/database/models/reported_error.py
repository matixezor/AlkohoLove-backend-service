from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from sqlalchemy import Boolean, Column, Integer, String, TIMESTAMP, select, update, func, delete, ForeignKey
from src.domain.reported_error import ReportedErrorBase

from src.database.database_metadata import Base


class ReportedError(Base):
    __tablename__ = 'reported_error'

    error_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    description = Column(String, unique=True, nullable=False)




class ReportedErrorDatabaseHandler:
    @staticmethod
    def raise_error_already_exists(reason: str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error with given {reason} already exists'
        )

    @staticmethod
    async def get_reported_error_by_id(db: AsyncSession, error_id: int) -> ReportedError | None:
        return await db.get(ReportedError, error_id)

    @staticmethod
    async def get_reported_errors_by_user_id(db: AsyncSession, user_id: int) -> ReportedError | None:
        query = select(ReportedError).filter(ReportedError.user_id == user_id)
        result = await db.execute(query)
        return result.scalars().all()

    @staticmethod
    async def get_reported_errors(db: AsyncSession, limit: int, offset: int) -> list[ReportedError]:
        query = select(ReportedError).offset(offset).limit(limit)
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
    async def create_reported_error(db: AsyncSession, reported_error_create_payload: ReportedError) -> None:
        db_user = ReportedError(
            **reported_error_create_payload.dict(),
        )
        db.add(db_user)


    @staticmethod
    async def update_reported_error_by_id(
            db: AsyncSession,
            error_id: int,
            reported_error_update_payload: ReportedErrorBase
    ) -> ReportedError:
        query = update(ReportedError) \
            .where(ReportedError.error_id == error_id) \
            .values(reported_error_update_payload.dict(exclude_none=True))
        await db.execute(query)
        await db.commit()
        return await ReportedErrorDatabaseHandler.get_reported_error_by_id(db, error_id=error_id)