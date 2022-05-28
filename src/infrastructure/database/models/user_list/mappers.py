from src.domain.alcohol_category.alcohol_category_property import PropertyOut
from src.domain.user_list import SearchHistoryEntry
from src.infrastructure.database.models.user_list.search_history import UserSearchHistory


# def map_to_search_history(category: UserSearchHistory) -> SearchHistoryEntry:
#     return SearchHistoryEntry(
#         id=category['_id'],
#         title=category['title'],
#         required=category.get('required', None),
#         properties=[
#             PropertyOut(
#                 alcohol=_key,
#                 =_value
#             )
#             for _key, _value in category['properties'].items()
#         ]
#     )
