import pymongo
from bson import ObjectId
from bson.int64 import Int64
from pymongo.database import Database
from pymongo.errors import WriteError, OperationFailure
from pymongo.collection import Collection, ReturnDocument

from src.domain.alcohol_filter import AlcoholFilters
from src.domain.alcohol import AlcoholCreate, AlcoholUpdate
from src.infrastructure.exceptions.validation_exceptions import ValidationErrorException
from src.infrastructure.database.models.alcohol_category import AlcoholCategoryDatabaseHandler


class AlcoholDatabaseHandler:
    @staticmethod
    def prepare_filters(filters: AlcoholFilters | None) -> list[dict]:
        if not filters:
            return []

        filters = filters.dict(exclude_none=True)
        _filters = []

        if filters.get('kind', None):
            _filters.append({'kind': filters.pop('kind')})
        for key, values in filters.items():
            _filters.append({key: {'$in': values}})

        return _filters

    @staticmethod
    def prepare_find_filters(filters: AlcoholFilters | None) -> dict:
        filters = AlcoholDatabaseHandler.prepare_filters(filters)
        return {
            key: value for dictionary in filters
            for key, value in dictionary.items()
        } if filters else {}

    @staticmethod
    def prepare_aggregate_filters(phrase: str, filters: AlcoholFilters | None) -> list[dict]:
        aggregated_filters = []
        filters = AlcoholDatabaseHandler.prepare_filters(filters)

        if filters:
            aggregated_filters.extend(filters)

        aggregated_filters.append(
            {
                '$or': [
                    {
                        '$text': {'$search': phrase}
                    },
                    {
                        'name': {'$regex': phrase, '$options': 'i'}
                    }
                ]
            }
        )

        return aggregated_filters

    @staticmethod
    async def get_alcohol_by_barcode(collection: Collection, barcode: list[str]) -> dict | None:
        return collection.find_one({'barcode': {'$in': barcode}})

    @staticmethod
    async def get_alcohol_by_name(collection: Collection, name: str) -> dict | None:
        return collection.find_one({'name': name})

    @staticmethod
    async def get_alcohol_by_id(collection: Collection, alcohol_id: str) -> dict | None:
        return collection.find_one({'_id': ObjectId(alcohol_id)})

    @staticmethod
    async def add_alcohol(collection: Collection, payload: AlcoholCreate):
        payload = payload.dict() | {'avg_rating': float(0), 'rate_count': Int64(0), 'rate_value': Int64(0)}
        try:
            return collection.insert_one(payload)
        except WriteError as ex:
            raise ValidationErrorException(ex.args[0])

    @staticmethod
    async def search_alcohols(
            collection: Collection,
            limit: int,
            offset: int,
            phrase: str | None,
            filters: AlcoholFilters | None
    ) -> tuple[list[dict], int]:
        if phrase:
            aggregate_filters = AlcoholDatabaseHandler.prepare_aggregate_filters(phrase, filters)
            return await AlcoholDatabaseHandler.get_alcohols_by_phrase(collection, limit, offset, aggregate_filters)
        else:
            find_filters = AlcoholDatabaseHandler.prepare_find_filters(filters)
            db_alcohols = await AlcoholDatabaseHandler.get_alcohols(collection, limit, offset, find_filters)
            total = await AlcoholDatabaseHandler.count_alcohols(collection, find_filters)
            return db_alcohols, total

    @staticmethod
    async def get_alcohols_by_phrase(
            collection: Collection,
            limit: int,
            offset: int,
            filters: list[dict]
    ) -> tuple[list[dict], int]:
        """
        The aggregation firstly matches records by filters if any are provided
        Then it performs an `or` operation where the operations are as follows:
        * full text search on text indexed fields i.e. `kind`, `type`, `color` and `keywords`
        * case-insensitive regex on indexed field name
        If the result comes from the full text search, then the score field is added.
        Therefore, we filter the results by score:
         * greater than 5.5 - results that are matched by one keyword or just the color are not reliable
         * null - results from regex do not have this field
         Then we paginate the results and aggregate total count
        """
        result = list(collection.aggregate([
            {
                '$match': {
                    '$and': filters
                }
            },
            {
                '$addFields': {'score': {'$meta': 'textScore'}}
            },
            {
                '$match': {
                    '$or': [
                        {'score': {'$gt': 5.5}},
                        {'score': None}
                    ]
                }
            },
            {'$sort': {'score': -1}},
            {
                '$facet': {
                    'alcohols': [{'$skip': offset}, {'$limit': limit}],
                    'totalCount': [{'$count': 'total'}]
                }
            },
            {'$unwind': '$totalCount'}
        ]))

        total = 0
        # unwrap the results and get the total count
        if result:
            result = result.pop()
            total = result['totalCount']['total']
            result = result['alcohols']

        return result, total

    @staticmethod
    async def get_alcohols(
            collection: Collection,
            limit: int,
            offset: int,
            filters: dict
    ) -> list[dict]:
        return list(collection.find(filters).sort('name', pymongo.ASCENDING).skip(offset).limit(limit))

    @staticmethod
    async def get_alcohols_created_by_user(
            collection: Collection,
            limit: int,
            offset: int,
            username: str
    ) -> list[dict]:
        return list(collection.find({'username': username}).skip(offset).limit(limit))

    @staticmethod
    async def count_alcohols_created_by_user(collection: Collection, username: str) -> int:
        return collection.count_documents(filter={'username': {'$eq': username}})

    @staticmethod
    async def count_alcohols(collection: Collection, filters: dict) -> int:
        return collection.count_documents(filters) if filters else collection.estimated_document_count()

    @staticmethod
    async def delete_alcohol(collection: Collection, alcohol_id: ObjectId) -> None:
        collection.delete_one({'_id': alcohol_id})

    @staticmethod
    async def update_alcohol(collection: Collection, alcohol_id: ObjectId, payload: AlcoholUpdate) -> dict | None:
        try:
            return collection.find_one_and_update(
                {'_id': alcohol_id},
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

    @staticmethod
    async def revert_by_removal(collection: Collection, name: str) -> None:
        collection.find_one_and_delete({'name': name})
