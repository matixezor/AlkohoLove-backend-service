from pydantic import BaseModel, validator


class PropertyOut(BaseModel):
    name: str
    metadata: dict


class Property(BaseModel):
    bsonType: list[str]
    description: str


class UpdateProperty(Property):
    pass

    @validator('bsonType')
    def check_null_in_type(cls, value: list[str]) -> list[str]:
        if 'null' not in value:
            raise ValueError('New properties should be nullable')
        return value


class CreateProperty(Property):
    bsonType: str | list[str]


class CreatePropertyKind(BaseModel):
    enum: list[str]

    @validator('enum')
    def check_only_one_value_provided(cls, value: list[str]) -> list[str]:
        if len(value) != 1:
            raise ValueError('Invalid kind enum value!')
        return value
