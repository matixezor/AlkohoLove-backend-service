from pydantic import BaseModel


class Barcode(BaseModel):
    barcode: str

    class Config:
        orm_mode = True
