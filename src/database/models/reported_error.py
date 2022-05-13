from sqlalchemy import Column, Integer, String, select, func, delete, ForeignKey
from sqlalchemy.orm import relationship, selectinload
from sqlalchemy.ext.asyncio import AsyncSession

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
    async def get_reported_error_by_id(db: AsyncSession, error_id: int) -> ReportedError | None:
        query = select(ReportedError).where(ReportedError.error_id == error_id). \
            options(selectinload(ReportedError.user))
        result = await db.execute(query)
        return result.scalar_one()

    @staticmethod
    async def get_reported_errors(db: AsyncSession, limit: int, offset: int) -> list[ReportedError]:
        query = select(ReportedError).offset(offset).limit(limit) \
            .options(selectinload(ReportedError.user))
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
    async def create_reported_error(
            db: AsyncSession,
            reported_error_create_payload: ReportedErrorCreate
    ) -> None:
        db_reported_error = ReportedError(
            **reported_error_create_payload.dict(exclude_none=True),
        )
        db.add(db_reported_error)
