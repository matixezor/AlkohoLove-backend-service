from pydantic import BaseModel

from src.domain.page_info import PageInfo


class ReportedErrorBase(BaseModel):
    error_id: int
    user_id: int
    description: str | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class PaginatedReportedErrorInfo(BaseModel):
    reported_errors: list[ReportedErrorBase]
    page_info: PageInfo
