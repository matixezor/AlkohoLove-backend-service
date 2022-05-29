import typing
from datetime import datetime

from src.domain.alcohol import Alcohol


class SearchHistoryEntry(typing.NamedTuple):
    alcohol: Alcohol
    date: datetime
