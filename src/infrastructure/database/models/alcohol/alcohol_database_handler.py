from bson import ObjectId
from bson.int64 import Int64
from pymongo.database import Database
from pymongo.errors import WriteError, OperationFailure
from pymongo.collection import Collection, ReturnDocument

from src.domain.alcohol import AlcoholCreate, AlcoholUpdate
from src.infrastructure.exceptions.validation_exceptions import ValidationErrorException
from src.infrastructure.database.models.alcohol_category import AlcoholCategoryDatabaseHandler


class AlcoholDatabaseHandler:
    @staticmethod
    async def get_alcohol_by_barcode(collection: Collection, barcode: list[str]) -> dict | None:
        return collection.find_one({'barcode': {'$in': barcode}})

    @staticmethod
    async def get_alcohol_by_name(collection: Collection, name: str) -> dict | None:
        return collection.find_one({'name': name})

    @staticmethod
    async def add_alcohol(collection: Collection, payload: AlcoholCreate) -> None:
        payload = payload.dict() | {'avg_rating': float(0), 'rate_count': Int64(0), 'rate_value': Int64(0)}
        try:
            collection.insert_one(payload)
        except WriteError as ex:
            raise ValidationErrorException(ex.args[0])

    @staticmethod
    async def search_alcohols(
            collection: Collection,
            limit: int, offset: int,
            phrase: str = None
    ) -> tuple[list[dict], int]:
        if phrase:
            result = list(collection.aggregate([
                {'$match': {'$text': {'$search': phrase}}},
                {'$addFields': {'score': {'$meta': 'textScore'}}},
                {'$match': {'score': {'$gt': 5.5}}},
                {'$facet': {
                    'alcohols': [{'$skip': offset}, {'$limit': limit}],
                    'totalCount': [{'$count': 'total'}]
                }},
                {'$unwind': '$totalCount'}
            ]))
            total = 0
            if result:
                result = result.pop()
                total = result['totalCount']['total']
                result = result['alcohols']

            return result, total
        else:
            cursor = collection.find({}).skip(offset).limit(limit)
            total = await AlcoholDatabaseHandler.count_alcohols(collection)
            return list(cursor), total

    @staticmethod
    async def count_alcohols(collection: Collection) -> int:
        return collection.estimated_document_count()

    @staticmethod
    async def delete_alcohol(collection: Collection, alcohol_id: str) -> None:
        collection.delete_one({'_id': ObjectId(alcohol_id)})

    @staticmethod
    async def update_alcohol(collection: Collection, alcohol_id: str, payload: AlcoholUpdate) -> dict | None:
        try:
            return collection.find_one_and_update(
                {'_id': ObjectId(alcohol_id)},
                {'$set': payload.dict(exclude_none=True)},
                return_document=ReturnDocument.AFTER
            )
        except OperationFailure as ex:
            raise ValidationErrorException(ex.args[0])

    @staticmethod
    async def update_validation(db: Database) -> None:
        core = {}
        db_categories = await AlcoholCategoryDatabaseHandler.get_all_categories(db.alcohol_categories)
        for db_category in db_categories:
            db_category.pop('_id', None)
            if db_category['title'] == 'core':
                core = db_category
        db_categories.remove(core)
        db.command(
            'collMod',
            'alcohols',
            validator={
                '$jsonSchema':
                    {
                        'bsonType': 'object',
                        'required': core['required'],
                        'properties': core['properties'],
                        'oneOf': db_categories
                    }
            }
        )

    @staticmethod
    async def remove_fields_for_kind(collection: Collection, kind: str, fields: list[str]) -> None:
        fields = {field: '' for field in fields}
        collection.update_many({'kind': kind}, {'$unset': fields})

    @staticmethod
    async def check_if_alcohol_exists(
            collection: Collection,
            alcohol_id: str
    ) -> bool:
        if collection.find_one({'_id': ObjectId(alcohol_id)}):
            return True
        else:
            return False
