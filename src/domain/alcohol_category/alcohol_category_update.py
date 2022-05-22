from pydantic import BaseModel

from src.domain.alcohol_category.alcohol_category_property import UpdateProperty


class AlcoholCategoryUpdate(BaseModel):
    properties: dict[str, UpdateProperty]
