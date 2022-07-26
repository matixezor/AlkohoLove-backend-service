from functools import cache

from bson import ObjectId
from pymongo.collection import Collection, ReturnDocument

from src.infrastructure.database.models.alcohol_category import AlcoholCategory
from src.domain.alcohol_category import AlcoholCategoryUpdate, AlcoholCategoryDelete, AlcoholCategoryCreate


class AlcoholCategoryDatabaseHandler:
    @staticmethod
    async def check_if_category_exist(collection: Collection[AlcoholCategory], name: str) -> bool:
        return True if collection.find_one({'title': name}) else False

    @staticmethod
    async def get_all_categories(collection: Collection[AlcoholCategory]) -> list[AlcoholCategory]:
        return list(collection.find({}))

    @staticmethod
    async def get_categories(
            collection: Collection[AlcoholCategory],
            limit: int,
            offset: int
    ) -> list[AlcoholCategory]:
        return list(collection.find({}).skip(offset).limit(limit))

    @staticmethod
    async def count_categories(collection: Collection[AlcoholCategory]) -> int:
        return collection.estimated_document_count()

    @staticmethod
    async def get_category_by_id(
            collection: Collection[AlcoholCategory],
            category_id: ObjectId
    ) -> AlcoholCategory | None:
        return collection.find_one({'_id': category_id})

    @staticmethod
    async def update_category(
            collection: Collection[AlcoholCategory],
            existing: AlcoholCategory,
            payload: AlcoholCategoryUpdate
    ) -> AlcoholCategory | None:
        payload = payload.dict()
        properties = existing['properties'] | payload['properties']
        required = existing.get('required', []) + list(payload['properties'].keys())
        return collection.find_one_and_update(
            {'_id': existing['_id']},
            {'$set': {'properties': properties, 'required': required}},
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    async def add_category(collection: Collection[AlcoholCategory], payload: AlcoholCategoryCreate) -> None:
        collection.insert_one(payload.dict(exclude_none=True))

    @staticmethod
    async def remove_properties(
            collection: Collection[AlcoholCategory],
            existing: AlcoholCategory,
            payload: AlcoholCategoryDelete
    ) -> AlcoholCategory | None:
        unset_properties = [f'properties.{field}' for field in payload.properties]
        return collection.find_one_and_update(
            {'_id': existing['_id']},
            [
                {'$unset': unset_properties},
                {'$set': {
                    'required': {
                        '$filter': {
                            'input': '$required',
                            'cond': {'$not': {'$in': ['$$this', payload.properties]}}
                        }
                    }
                }},
                {
                    '$set': {
                        'required': {
                            '$cond': [
                                {'$eq': ['$required', []]},
                                '$$REMOVE',
                                '$required'
                            ]
                        }
                    }
                }
            ],
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    async def revert(collection: Collection[AlcoholCategory], original: AlcoholCategory) -> None:
        collection.find_one_and_replace({'_id': original['_id']}, original)

    @staticmethod
    async def revert_by_removal(collection: Collection[AlcoholCategory], name: str) -> None:
        collection.find_one_and_delete({'title': name})

    @staticmethod
    @cache
    def get_category_by_title(collection: Collection[AlcoholCategory], title: str) -> AlcoholCategory | None:
        return collection.find_one({'title': title})
