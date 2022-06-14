from pydantic import validator, root_validator

from src.domain.alcohol import AlcoholBase
from src.infrastructure.common.utils import parse_float


class AlcoholCreate(AlcoholBase):
    pass

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
