from pydantic import BaseModel, validator


class AlcoholFilters(BaseModel):
    kind: str
    type: list[str] | None
    color: list[str] | None
    country: list[str] | None

    @validator('kind')
    def validate_kind(cls, value: str) -> str:
        if not value:
            raise ValueError('Kind filter must be provided')
        return value
