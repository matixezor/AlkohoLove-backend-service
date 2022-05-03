from pydantic import BaseModel

from src.domain.page_info import PageInfo
from src.domain.user import User


class ReportedErrorBase(BaseModel):
    error_id: int
    description: str

    class Config:
        orm_mode = True
        # allow_population_by_field_name = True


class ReportedError(ReportedErrorBase):
    user: User


class PaginatedReportedErrorInfo(BaseModel):
    reported_errors: list[ReportedError]
    page_info: PageInfo


class ReportedErrorCreate(BaseModel):
    description: str
    user_id: int
