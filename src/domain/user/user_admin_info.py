from datetime import datetime

from src.domain.user import User


class UserAdminInfo(User):
    is_banned: bool
    is_admin: bool
    last_login: datetime | None = None
    created_on: datetime
    is_verified: bool
    verification_code: str | None = None
    reset_password_code: str | None = None
    change_info_code: str | None = None
    delete_account_code: str | None = None
