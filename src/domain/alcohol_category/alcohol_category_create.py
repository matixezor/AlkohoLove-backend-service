from pydantic import validator, BaseModel, root_validator

from src.domain.alcohol_category.alcohol_category_property import CreateProperty, CreatePropertyKind


class AlcoholCategoryCreate(BaseModel):
    properties: dict[str, CreateProperty | CreatePropertyKind]
    required: list[str] | None = None
    title: str

    @root_validator(pre=True)
    def validate_root(cls, values: dict):
        required = [key for key in values['properties'].keys() if key != 'kind']
        if required:
            values['required'] = required
        return values

    @validator('properties')
    def validate_properties(cls, value: dict[str, CreateProperty]) -> dict[str, CreateProperty]:
        if 'kind' not in list(value.keys()):
            raise ValueError('New category kind should be specified in properties')
        return value
