import json
from pydantic import BaseModel, Extra, root_validator

from src.infrastructure.common.scalar_utils import parse_float


class AlcoholUpdate(BaseModel):
    name: str | None
    kind: str | None
    type: str | None
    alcohol_by_volume: float | None
    description: str | None
    color: str | None
    manufacturer: str | None
    country: str | None
    region: str | None
    food: list[str] | None
    finish: list[str] | None
    aroma: list[str] | None
    taste: list[str] | None
    barcode: list[str] | None
    keywords: list[str] | None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate_to_json

    @classmethod
    def validate_to_json(cls, value):
        if isinstance(value, str):
            return cls(**json.loads(value))
        return value

    @root_validator(pre=True)
    def validate_root(cls, values: dict):
        excluded = ('avg_count', 'rate_count', 'rate_value')
        if any(key in list(values.keys()) for key in excluded):
            raise ValueError(f'Invalid payload. Attempted to update excluded fields: {excluded}')
        required_fields = cls.__fields__.keys()
        for key, value in values.items():
            if key not in required_fields and isinstance(value, str):
                values[key] = parse_float(value)
        return values

    class Config:
        extra = Extra.allow
