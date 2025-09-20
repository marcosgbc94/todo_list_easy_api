from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

# Respuesta User por get
class UserResponse(BaseModel):
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
    id: int
    username: str
    email: EmailStr
    updated_at: Optional[datetime] = None
    updated_by: Optional[int] = None

class Config:
    orm_mode = True
