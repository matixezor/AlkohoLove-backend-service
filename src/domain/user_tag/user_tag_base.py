from pydantic import BaseModel


class UserTagBase(BaseModel):
    tag_name: str
