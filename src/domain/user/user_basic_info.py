from pydantic import BaseModel


class FollowUserBasicInfo(BaseModel):
    username: str
