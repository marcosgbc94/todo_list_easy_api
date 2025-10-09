import datetime
from typing import Optional

class TaskEntity:
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: Optional[int] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status_id: Optional[int] = None,
        priority_id: Optional[int] = None,
        due_date: Optional[datetime.datetime] = None,
        created_at: Optional[datetime.datetime] = None,
        created_by: Optional[int] = None,
        updated_at: Optional[datetime.datetime] = None,
        updated_by: Optional[int] = None,
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.status_id = status_id
        self.priority_id = priority_id
        self.due_date = due_date
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by