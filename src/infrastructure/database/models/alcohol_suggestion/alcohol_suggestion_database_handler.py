from bson import ObjectId
from pymongo.collection import Collection

from src.infrastructure.database.models.alcohol_suggestion.alcohol_suggestion import AlcoholSuggestion
from src.infrastructure.database.models.socials.followers import Followers
from src.infrastructure.database.models.socials.following import Following
from src.infrastructure.database.models.user import User, UserDatabaseHandler


class AlcoholSuggestionDatabaseHandler:

    @staticmethod
    async def get_suggestions(
            suggestions_collection: Collection[AlcoholSuggestion],
            limit: int,
            offset: int,
    ) -> list[dict]:
        return list(suggestions_collection.find({}).skip(offset).limit(limit))

    @staticmethod
    async def delete_suggestion(collection: Collection[AlcoholSuggestion], suggestion_id: str) -> None:
        collection.delete_one({'_id': ObjectId(suggestion_id)})

    @staticmethod
    async def count_suggestions(
            suggestions_collection: Collection[AlcoholSuggestion],
    ) -> int:
        return suggestions_collection.count_documents({})

    @staticmethod
    async def get_suggestion_by_id(
            collection: Collection[AlcoholSuggestion],
            suggestion_id: str
    ) -> list[dict] | None:
        return collection.find_one({'_id': ObjectId(suggestion_id)})
