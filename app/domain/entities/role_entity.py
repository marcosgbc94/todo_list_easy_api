from typing import Optional
import datetime

class RoleEntity:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        created_at: Optional[datetime.datetime] = None,
        created_by: Optional[int] = None,
        updated_at: Optional[datetime.datetime] = None,
        updated_by: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.description = description
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by