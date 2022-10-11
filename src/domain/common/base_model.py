from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    pass

    class Config:
        anystr_strip_whitespace = True
