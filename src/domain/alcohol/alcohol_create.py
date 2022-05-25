from pydantic import validator

from src.domain.alcohol import AlcoholBase


class AlcoholCreate(AlcoholBase):
    pass

    @validator('barcode')
    def barcode_validator(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError('Barcode must be provided')
        return value
