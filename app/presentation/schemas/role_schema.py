from pydantic import BaseModel, ConfigDict
from typing import Optional

orm_config = ConfigDict(from_attributes=True)

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreateRequest(RoleBase):
    pass

class RoleResponse(RoleBase):
    model_config = orm_config
    id: int

class UserRoleRequest(BaseModel):
    user_id: int
    role_id: int