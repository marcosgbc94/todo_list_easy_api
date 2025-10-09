from pydantic import BaseModel, ConfigDict
from typing import Optional
import datetime

orm_config = ConfigDict(from_attributes=True)

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status_id: int
    priority_id: int
    due_date: Optional[datetime.datetime] = None

class TaskCreateRequest(TaskBase):
    pass

class TaskUpdateRequest(TaskBase):
    pass

class TaskResponse(TaskBase):
    model_config = orm_config
    
    id: int
    user_id: int
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None