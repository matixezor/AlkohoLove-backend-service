from datetime import datetime
from typing import NamedTuple

from src.domain.alcohol import Alcohol


class SearchHistoryEntry(NamedTuple):
    alcohol: Alcohol
    date: datetime
