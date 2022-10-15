from datetime import datetime

from src.domain.alcohol import Alcohol
from src.domain.common.base_model import BaseModel


class SearchHistoryEntry(BaseModel):
    alcohol: Alcohol
    date: datetime
