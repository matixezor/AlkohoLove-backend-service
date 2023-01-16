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
            aggregated_filters.append({
                '$match': {
                    key: value for dictionary in filters
                    for key, value in dictionary.items()
                }
            })

        aggregated_filters.append(
                {
                    '$search': {
                        'index': 'tetxtSearch',
                        'compound': {
                            'should': [
                                {
                                    'text': {
                                        'query': phrase,
                                        'path': 'name',
                                        'fuzzy': {},
                                        'score': {'boost': {'value': 10}}
                                    }
                                },
                                {
                                    'text': {
                                        'query': phrase,
                                        'path': 'kind',
                                        'fuzzy': {},
                                        'score': {'boost': {'value': 8}}
                                    }
                                },
                                {
                                    'text': {
                                        'query': phrase,
                                        'path': 'type',
                                        'score': {'boost': {'value': 7}}
                                    }
                                },
                                {
                                    'text': {
                                        'query': phrase,
                                        'path': 'color',
                                        'score': {'boost': {'value': 5}}
                                    }
                                },
                                {
                                    'text': {
                                        'query': phrase,
                                        'path': 'keywords',
                                        'score': {'boost': {'value': 5}}
                                    }
                                },
                                {
                                    'autocomplete': {
                                        'query': phrase,
                                        'path': 'name',
                                        'score': {'boost': {'value': 10}}
                                    }
                                }
                            ]
                        }
                    }
                }
        )

        return aggregated_filters[::-1]

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
    async def get_alcohols_by_ids(collection: Collection, alcohol_ids: list[ObjectId]) -> list[dict] | None:
        return list(collection.find({'_id': {'$in': alcohol_ids}}))

    @staticmethod
    async def add_alcohol(collection: Collection, payload: AlcoholCreate):
        payload = payload.dict() | {
            'avg_rating': float(0),
            'rate_count': Int64(0),
            'rate_value': Int64(0),
            'rate_1_count': Int64(0),
            'rate_2_count': Int64(0),
            'rate_3_count': Int64(0),
            'rate_4_count': Int64(0),
            'rate_5_count': Int64(0)
        }
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
        alcohols_pipeline = [{'$skip': offset}]
        if limit:
            alcohols_pipeline.append({'$limit': limit})
        result = list(collection.aggregate([
            *filters,
            {
                '$addFields': {'score': {'$meta': 'searchScore'}}
            },
            {'$sort': {'score': -1}},
            {
                '$facet': {
                    'alcohols': alcohols_pipeline,
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

    @staticmethod
    async def search_values(
            field_name: str,
            collection: Collection,
            limit: int,
            offset: int,
            phrase: str | None
    ) -> list[str]:
        if phrase:
            pipeline = [
                # Match the possible documents. Always the best approach
                {'$match': {field_name: {'$regex': f'^{phrase}', '$options': 'i'}}},
                # De-normalize the array content to separate documents
                {'$unwind': f'${field_name}'},
                # Now "filter" the content to actual matches
                {'$match': {field_name: {'$regex': f'^{phrase}', '$options': 'i'}}},
                # Group the "like" terms as the "key"
                {'$group': {'_id': f'${field_name}'}},
                {'$sort': {'_id': 1}},
                {'$skip': offset},
            ]
            if limit:
                pipeline.append({'$limit': limit})
            values = list(collection.aggregate(pipeline))
        else:
            pipeline = [
                {'$unwind': f'${field_name}'},
                {'$group': {'_id': f'${field_name}'}},
                {'$sort': {'_id': 1}},
                {'$skip': offset},
            ]
            if limit:
                pipeline.append({'$limit': limit})
            values = list(collection.aggregate(pipeline))
        return [value['_id'] for value in values]

    @staticmethod
    async def get_guest_list(
            collection: Collection,
            limit: int,
            offset: int,
            alcohol_list: list[ObjectId]
    ) -> list[dict]:
        return list(collection.find({'_id': {'$in': alcohol_list}}).skip(offset).limit(limit))
