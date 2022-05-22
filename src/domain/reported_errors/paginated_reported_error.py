from pydantic import BaseModel

from src.domain.common import PageInfo
from src.domain.reported_errors import ReportedError


class PaginatedReportedErrorInfo(BaseModel):
    reported_errors: list[ReportedError]
    page_info: PageInfo
