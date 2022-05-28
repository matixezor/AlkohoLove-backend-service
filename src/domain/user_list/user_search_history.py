from datetime import datetime

from pydantic import BaseModel
from src.domain.alcohol import Alcohol


class UserSearchHistoryEntry(BaseModel):
    alcohol: Alcohol
    date: datetime
