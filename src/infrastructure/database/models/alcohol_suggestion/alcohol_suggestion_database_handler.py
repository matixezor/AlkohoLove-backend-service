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
        suggestions = list(suggestions_collection.find({}).skip(offset).limit(limit))
        # user_ids = suggestions[2]['user_ids']
        #
        # pipeline = [{'$project': {"id": {'$toString': "$user_ids"}, "user_ids": 1, "value": 1}}]
        # cursor = list(suggestions_collection.aggregate(pipeline))
        return list(suggestions_collection.find({}).skip(offset).limit(limit))

    @staticmethod
    async def delete_suggestion(collection: Collection[AlcoholSuggestion], suggestion_id: ObjectId) -> None:
        collection.delete_one({'_id': suggestion_id})

    @staticmethod
    async def count_suggestions(
            suggestions_collection: Collection[AlcoholSuggestion],
    ) -> int:
        return suggestions_collection.count_documents({})
