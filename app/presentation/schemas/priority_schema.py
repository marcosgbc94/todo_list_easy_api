from pydantic import BaseModel, ConfigDict
from typing import Optional

orm_config = ConfigDict(from_attributes=True)

class PriorityBase(BaseModel):
    name: str
    color: Optional[str] = None

class PriorityCreateRequest(PriorityBase):
    pass

class PriorityUpdateRequest(PriorityBase):
    pass

class PriorityResponse(PriorityBase):
    model_config = orm_config
    id: int