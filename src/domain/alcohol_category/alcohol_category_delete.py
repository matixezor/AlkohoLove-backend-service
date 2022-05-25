from pydantic import BaseModel


class AlcoholCategoryDelete(BaseModel):
    properties: list[str]
