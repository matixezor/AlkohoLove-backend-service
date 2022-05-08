from pydantic import BaseModel

from src.domain.user import User
from src.domain.page_info import PageInfo


class ReportedErrorBase(BaseModel):
    error_id: int
    user_id: int
    description: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class ReportedError(ReportedErrorBase):
    user: User


class PaginatedReportedErrorInfo(BaseModel):
    reported_errors: list[ReportedError]
    page_info: PageInfo


class ReportedErrorCreate(BaseModel):
    description: str
