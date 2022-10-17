from bson import ObjectId
from pymongo.collection import Collection

from src.domain.user import User
from src.domain.reported_errors import ReportedErrorCreate
from src.infrastructure.database.models.reported_error import ReportedError


class ReportedErrorDatabaseHandler:
    @staticmethod
    async def get_reported_error_by_id(
            collection: Collection[ReportedError],
            error_id: ObjectId
    ) -> ReportedError | None:
        return collection.find_one({'_id': error_id})

    @staticmethod
    async def get_reported_errors(
            collection: Collection[ReportedError],
            limit: int,
            offset: int,
            user_id: ObjectId = None
    ) -> list[ReportedError]:
        return (
            list(collection.find({}).skip(offset).limit(limit))
            if not user_id
            else list(collection.find({'user_id': user_id}).skip(offset).limit(limit))
        )

    @staticmethod
    async def count_reported_errors(
            collection: Collection[ReportedError],
            user_id: ObjectId = None
    ) -> int:
        return (
            collection.estimated_document_count()
            if not user_id
            else collection.count_documents(filter={'user_id': {'$eq': user_id}})
        )

    @staticmethod
    async def delete_reported_error(collection: Collection[ReportedError], error_id: ObjectId) -> None:
        collection.delete_one({'_id': error_id})

    @staticmethod
    async def create_reported_error(
            error_collection: Collection[ReportedError],
            user_collection: Collection[User],
            user_id: ObjectId,
            payload: ReportedErrorCreate
    ) -> None:
        username = user_collection.find_one({'_id': user_id})
        db_reported_error = ReportedError(
            **payload.dict(),
            user_id=user_id,
            username=username
        )
        error_collection.insert_one(db_reported_error)
