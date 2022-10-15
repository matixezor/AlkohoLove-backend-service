import json

from pydantic import validator, root_validator

from src.domain.alcohol import AlcoholBase
from src.infrastructure.common.scalar_utils import parse_float


class AlcoholCreate(AlcoholBase):
    pass

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    @root_validator(pre=True)
    def convert_string_values_to_float(cls, values: dict):
        required_fields = cls.__fields__.keys()
        for key, value in values.items():
            if key not in required_fields and isinstance(value, str):
                values[key] = parse_float(value)
        return values

    @validator('barcode')
    def barcode_validator(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError('Barcode must be provided')
        return value
