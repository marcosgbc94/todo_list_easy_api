from typing import Optional
import datetime

class StatusEntity:
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
        color: Optional[str] = None,
        created_at: Optional[datetime.datetime] = None,
        created_by: Optional[int] = None,
        updated_at: Optional[datetime.datetime] = None,
        updated_by: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.color = color
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by