from bson import ObjectId
from pymongo.collection import Collection, ReturnDocument

from src.infrastructure.database.database_config import db
from src.infrastructure.database.models.alcohol_category import AlcoholCategory
from src.domain.alcohol_category import AlcoholCategoryUpdate, AlcoholCategoryDelete, AlcoholCategoryCreate

alcohol_categories_collection: Collection[AlcoholCategory] = db.alcohol_categories


class AlcoholCategoryDatabaseHandler:
    @staticmethod
    async def check_if_category_exist(name: str) -> bool:
        return True if alcohol_categories_collection.find_one({'title': name}) else False

    @staticmethod
    async def get_all_categories() -> list[AlcoholCategory]:
        return list(alcohol_categories_collection.find({}))

    @staticmethod
    async def get_categories(limit: int, offset: int) -> list[AlcoholCategory]:
        return list(alcohol_categories_collection.find({}).skip(offset).limit(limit))

    @staticmethod
    async def count_categories() -> int:
        return alcohol_categories_collection.estimated_document_count()

    @staticmethod
    async def get_category_by_id(category_id: str) -> AlcoholCategory | None:
        return alcohol_categories_collection.find_one({'_id': ObjectId(category_id)})

    @staticmethod
    async def update_category(existing: AlcoholCategory, payload: AlcoholCategoryUpdate) -> AlcoholCategory | None:
        payload = payload.dict()
        properties = existing['properties'] | payload['properties']
        required = existing.get('required', []) + list(payload['properties'].keys())
        return alcohol_categories_collection.find_one_and_update(
            {'_id': existing['_id']},
            {'$set': {'properties': properties, 'required': required}},
            return_document=ReturnDocument.AFTER
        )

    @staticmethod
    async def add_category(payload: AlcoholCategoryCreate) -> None:
        alcohol_categories_collection.insert_one(payload.dict(exclude_none=True))

    @staticmethod
    async def remove_properties(existing: AlcoholCategory, payload: AlcoholCategoryDelete) -> AlcoholCategory | None:
        unset_properties = [f'properties.{field}' for field in payload.properties]
        return alcohol_categories_collection.find_one_and_update(
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
    async def revert(original: AlcoholCategory) -> None:
        alcohol_categories_collection.find_one_and_replace({'_id': original['_id']}, original)

    @staticmethod
    async def revert_by_removal(name: str) -> None:
        alcohol_categories_collection.find_one_and_delete({'title': name})
