from pydantic import BaseModel


class Flavour(BaseModel):
    flavour_id: int
    flavour_name: str

    class Config:
        orm_mode = True


class AllFlavours(BaseModel):
    flavour: list[Flavour]


class FlavourCreate(BaseModel):
    flavour_name: str

    class Config:
        orm_mode = True
