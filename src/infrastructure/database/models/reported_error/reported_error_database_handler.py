from bson import ObjectId
from pymongo.collection import Collection

from src.domain.reported_errors import ReportedErrorCreate
from src.infrastructure.database.database_config import db
from src.infrastructure.database.models.reported_error import ReportedError


reported_errors: Collection[ReportedError] = db.reported_errors


class ReportedErrorDatabaseHandler:
    @staticmethod
    async def get_reported_error_by_id(error_id: str) -> ReportedError | None:
        return reported_errors.find_one({'_id': ObjectId(error_id)})

    @staticmethod
    async def get_reported_errors(limit: int, offset: int, user_id: str = None) -> list[ReportedError]:
        return (
            list(reported_errors.find({}).skip(offset).limit(limit))
            if not user_id
            else list(reported_errors.find({'user_id': ObjectId(user_id)}).skip(offset).limit(limit))
        )

    @staticmethod
    async def count_reported_errors(user_id: str = None) -> int:
        return (
            reported_errors.estimated_document_count()
            if not user_id
            else reported_errors.count_documents(filter={'user_id': {'$eq': ObjectId(user_id)}})
        )

    @staticmethod
    async def delete_reported_error(error_id: str) -> None:
        reported_errors.delete_one({'_id': ObjectId(error_id)})

    @staticmethod
    async def create_reported_error(
            user_id: str,
            payload: ReportedErrorCreate
    ) -> None:
        db_reported_error = ReportedError(
            **payload.dict(),
            user_id=ObjectId(user_id)
        )
        reported_errors.insert_one(db_reported_error)
