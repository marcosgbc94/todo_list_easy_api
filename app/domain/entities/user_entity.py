from typing import Optional
from app.core.security import hash_password
from datetime import datetime, timezone
from typing import Optional
from app.core.security import hash_password

class UserEntity:
    def __init__(
        self,
        id: Optional[int] = None,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: Optional[str] = None,
        password_hash: Optional[str] = None,
        created_at: Optional[datetime] = None,
        created_by: Optional[int] = None,
        updated_at: Optional[datetime] = None,
        updated_by: Optional[int] = None,
    ):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.password_hash = password_hash
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by

    @staticmethod
    def set_password(password: str) -> str:
        return hash_password(password=password)

    @staticmethod
    def get_datetime_now() -> datetime:
        return datetime.now(timezone.utc)