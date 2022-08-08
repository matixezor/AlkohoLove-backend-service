from pydantic import BaseModel


class ReviewBan(BaseModel):
    reason: str
