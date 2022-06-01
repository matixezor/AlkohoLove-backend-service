from typing import TypedDict


class AlcoholFilter(TypedDict):
    _id: str
    color: list[str]
    country: list[str]
    type: list[str]
