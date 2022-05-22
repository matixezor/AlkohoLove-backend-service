from pydantic import BaseModel


class ReportedErrorBase(BaseModel):
    description: str
