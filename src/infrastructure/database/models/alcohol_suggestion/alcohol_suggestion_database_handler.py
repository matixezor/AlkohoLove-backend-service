from bson import ObjectId
from pymongo.collection import Collection

from src.domain.user import User
from src.domain.alcohol_suggestion.alcohol_suggestion_create import AlcoholSuggestionCreate
from src.infrastructure.database.models.alcohol_suggestion.alcohol_suggestion import AlcoholSuggestion


class AlcoholSuggestionDatabaseHandler:

    @staticmethod
    async def get_suggestions(
            suggestions_collection: Collection[AlcoholSuggestion],
            limit: int,
            offset: int,
    ) -> list[dict]:
        return list(suggestions_collection.find({}).skip(offset).limit(limit))

    @staticmethod
    async def delete_suggestion(collection: Collection[AlcoholSuggestion], suggestion_id: ObjectId) -> None:
        collection.delete_one({'_id': suggestion_id})

    @staticmethod
    async def count_suggestions(
            suggestions_collection: Collection[AlcoholSuggestion],
    ) -> int:
        return suggestions_collection.count_documents({})

    @staticmethod
    async def get_suggestion_by_id(
            collection: Collection[AlcoholSuggestion],
            suggestion_id: ObjectId
    ) -> dict | None:
        return collection.find_one({'_id': suggestion_id})

    @staticmethod
    async def get_suggestion_by_barcode(
            collection: Collection[AlcoholSuggestion],
            barcode: str
    ) -> dict | None:
        return collection.find_one({'barcode': barcode})

    @staticmethod
    async def append_to_suggestion(
            alcohol_collection: Collection[AlcoholSuggestion],
            user_collection: Collection[User],
            user_id: ObjectId,
            description: str | None,
            suggestion: AlcoholSuggestion
    ) -> None:
        username = user_collection.find_one({'_id': user_id})
        if suggestion['descriptions']:
            if description is not None:
                alcohol_collection.update_one({'_id': suggestion['_id']},
                                              {'$push': {'user_ids': user_id, 'descriptions': description,
                                                         'usernames': username}})
            else:
                alcohol_collection.update_one({'_id': suggestion['_id']},
                                              {'$push': {'user_ids': user_id, 'descriptions': [description],
                                                         'usernames': username}})
        else:
            alcohol_collection.update_one({'_id': suggestion['_id']},
                                          {'$push': {'user_ids': user_id}, 'usernames': username})

    @staticmethod
    async def create_suggestion(
            suggestions_collection: Collection[AlcoholSuggestion],
            user_collection: Collection[User],
            user_id: ObjectId,
            payload: AlcoholSuggestionCreate
    ) -> None:
        if payload.description:
            descriptions = [payload.description]
        else:
            descriptions = None
        username = user_collection.find_one({'_id': user_id})
        db_suggestions = AlcoholSuggestion(
            **payload.dict(),
            descriptions=descriptions,
            usernames=[username],
            user_ids=[user_id]
        )
        suggestions_collection.insert_one(db_suggestions)
