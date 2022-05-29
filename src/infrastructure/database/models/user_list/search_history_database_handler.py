from bson import ObjectId
from datetime import datetime
from pymongo.collection import Collection

from src.infrastructure.database.models.user_list.search_history import UserSearchHistory


class SearchHistoryHandler:
    @staticmethod
    async def get_user_search_history_user_id(
            limit: int,
            offset: int,
            search_history_collection: Collection,
            alcohols_collection: Collection,
            user_id: str = None,
    ) -> list[(dict, datetime)]:
        search_history = list(search_history_collection.find({'user_id': ObjectId(user_id)}, {'alcohols': 1}))

        search_history = search_history[0]['alcohols']
        alcohol_ids = [a_dict['alcohol_id'] for a_dict in search_history]
        dates = [a_dict['search_date'] for a_dict in search_history]

        alcohol = list((alcohols_collection.find({'_id': {'$in': alcohol_ids}})).skip(offset).limit(limit))

        for i in range(len(alcohol)):
            alcohol[i] = (alcohol[i], dates[i])

        return alcohol

    @staticmethod
    async def delete_alcohol_from_search_history(collection: Collection[UserSearchHistory], user_id: str,
                                                 alcohol_id: str, date: datetime) -> None:
        collection.update_many({'user_id': ObjectId(user_id)},
                               {'$pull': {'alcohols': {'alcohol_id': ObjectId(alcohol_id), 'search_date': date}}})

    @staticmethod
    async def add_alcohol_to_search_history(collection: Collection[UserSearchHistory], user_id: str,
                                            alcohol_id: str) -> None:
        collection.update_one({'user_id': ObjectId(user_id)},
                              {'$push': {
                                  'alcohols': {'alcohol_id': ObjectId(alcohol_id), 'search_date': datetime.now()}}})
