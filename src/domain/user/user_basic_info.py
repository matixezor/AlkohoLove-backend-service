from pydantic import BaseModel


class UserBasicInfo(BaseModel):
    username: str
