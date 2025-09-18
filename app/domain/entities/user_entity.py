from typing import Optional
from core.security import hash_password

class UserEntity:
    def __init__(self, username: str, email: str, password: Optional[str] = None, id: Optional[int] = None, password_hash: Optional[str] = None):
        self.id = id
        self.username = username
        self.email = email

        if password:
            self.password_hash = self._set_password(password=password)
        elif password_hash:
            self.password_hash = password_hash
        else:
            self.password = None
            self.password_hash = None

    def _set_password(self, password: str):
        self.password_hash = hash_password(password)
