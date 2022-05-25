from bson import ObjectId
from pymongo.collection import Collection

from src.domain.reported_errors import ReportedErrorCreate
from src.infrastructure.database.models.reported_error import ReportedError


class ReportedErrorDatabaseHandler:
    @staticmethod
    async def get_reported_error_by_id(
            collection: Collection[ReportedError],
            error_id: str
    ) -> ReportedError | None:
        return collection.find_one({'_id': ObjectId(error_id)})

    @staticmethod
    async def get_reported_errors(
            collection: Collection[ReportedError],
            limit: int,
            offset: int,
            user_id: str = None
    ) -> list[ReportedError]:
        return (
            list(collection.find({}).skip(offset).limit(limit))
            if not user_id
            else list(collection.find({'user_id': ObjectId(user_id)}).skip(offset).limit(limit))
        )

    @staticmethod
    async def count_reported_errors(
            collection: Collection[ReportedError],
            user_id: str = None
    ) -> int:
        return (
            collection.estimated_document_count()
            if not user_id
            else collection.count_documents(filter={'user_id': {'$eq': ObjectId(user_id)}})
        )

    @staticmethod
    async def delete_reported_error(collection: Collection[ReportedError], error_id: str) -> None:
        collection.delete_one({'_id': ObjectId(error_id)})

    @staticmethod
    async def create_reported_error(
            collection: Collection[ReportedError],
            user_id: str,
            payload: ReportedErrorCreate
    ) -> None:
        db_reported_error = ReportedError(
            **payload.dict(),
            user_id=ObjectId(user_id)
        )
        collection.insert_one(db_reported_error)
