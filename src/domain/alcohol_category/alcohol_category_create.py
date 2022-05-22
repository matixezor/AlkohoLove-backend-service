from pydantic import validator, BaseModel

from src.domain.alcohol_category.alcohol_category_property import CreateProperty, CreatePropertyKind


class AlcoholCategoryCreate(BaseModel):
    properties: dict[str, CreateProperty | CreatePropertyKind]
    required: list[str] | None
    title: str

    @validator('properties')
    def validate_properties(cls, value: dict[str, CreateProperty]) -> dict[str, CreateProperty]:
        if 'kind' not in list(value.keys()):
            raise ValueError('New category kind should be specified in properties')
        return value
