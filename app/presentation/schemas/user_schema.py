from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

orm_config = ConfigDict(from_attributes=True)

# Respuesta User por get
class UserResponse(BaseModel):
    model_config = orm_config

    id: int
    username: str
    email: EmailStr
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

# Requerimiento al crear usuario
class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

# Respuesta al crear usuario
class UserCreateResponse(BaseModel):
    model_config = orm_config

    id: int
    username: str
    email: EmailStr
    created_at: Optional[datetime] = None
    created_by: Optional[int] = None

# Requerimiento al actualizar usuario
class UserUpdateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

# Respuesta al actualizar usuario
class UserUpdateResponse(BaseModel):
    model_config = orm_config

    id: int
    username: str
    email: EmailStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None