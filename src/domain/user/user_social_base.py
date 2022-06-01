from pydantic import BaseModel


class UserSocialBase(BaseModel):
    username: str
