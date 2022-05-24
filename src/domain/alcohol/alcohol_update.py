from pydantic import BaseModel, Extra, root_validator


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

    @root_validator(pre=True)
    def any_of(cls, values: dict):
        if not any(values.values()):
            raise ValueError('At least one value needs to be provided')
        return values

    class Config:
        extra = Extra.allow
