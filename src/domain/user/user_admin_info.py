from datetime import datetime

from src.domain.user import User


class UserAdminInfo(User):
    is_banned: bool
    is_admin: bool
    last_login: datetime | None = None
    created_on: datetime
