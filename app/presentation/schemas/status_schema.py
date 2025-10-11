from pydantic import BaseModel, ConfigDict
from typing import Optional

orm_config = ConfigDict(from_attributes=True)

class StatusBase(BaseModel):
    name: str
    color: Optional[str] = None

class StatusCreateRequest(StatusBase):
    pass

class StatusUpdateRequest(StatusBase):
    pass

class StatusResponse(StatusBase):
    model_config = orm_config
    id: int