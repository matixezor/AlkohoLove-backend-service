from bson import ObjectId
from datetime import datetime
from pymongo.collection import Collection

from src.domain.user_list import SearchHistoryEntry
from src.infrastructure.database.models.user_list.search_history import UserSearchHistory


class SearchHistoryHandler:
    @staticmethod
    async def get_user_search_history_user_id(
            limit: int,
            offset: int,
            search_history_collection: Collection,
            alcohols_collection: Collection,
            user_id: ObjectId = None,
    ) -> list[SearchHistoryEntry]:
        search_history = search_history_collection.find_one({'user_id': user_id}, {'alcohols': 1})
        search_history = search_history['alcohols']
        alcohol_ids = []
        for a_dict in search_history:
            alcohol_ids.append(a_dict['alcohol_id'])
        alcohol_list = list((alcohols_collection.find({'_id': {'$in': alcohol_ids}})).skip(offset).limit(limit))
        alcohols = []
        for i in range(len(alcohol_list)):
            alcohol = next((item for item in search_history if item['alcohol_id'] == alcohol_list[i]['_id']), None)
            alcohols.append(SearchHistoryEntry(alcohol=alcohol_list[i], date=alcohol['search_date']))
        alcohols.sort(key=lambda search_history_entry: search_history_entry.date, reverse=True)
        return alcohols

    @staticmethod
    async def delete_alcohol_from_search_history(collection: Collection[UserSearchHistory], user_id: ObjectId,
                                                 alcohol_id: ObjectId) -> None:
        collection.update_many({'user_id': user_id},
                               {'$pull': {'alcohols': {'alcohol_id': alcohol_id}}})

    @staticmethod
    async def add_alcohol_to_search_history(collection: Collection[UserSearchHistory], user_id: ObjectId,
                                            alcohol_id: ObjectId) -> None:
        collection.update_one({'user_id': user_id}, {'$pull': {'alcohols': {'alcohol_id': alcohol_id}}})
        collection.update_one({'user_id': user_id},
                              {'$push': {'alcohols': {'alcohol_id': alcohol_id, 'search_date': datetime.now()}}})

    @staticmethod
    async def count_alcohols_in_search_history(
            search_history_collection: Collection[UserSearchHistory],
            alcohols_collection: Collection,
            user_id: ObjectId
    ) -> int:
        alcohols = search_history_collection.find_one({'user_id': user_id}, {'alcohols': 1})
        alcohols = alcohols['alcohols']
        alcohol_ids = []
        for a_dict in alcohols:
            alcohol_ids.append(a_dict['alcohol_id'])
        return len(list(alcohols_collection.find({'_id': {'$in': alcohol_ids}})))
