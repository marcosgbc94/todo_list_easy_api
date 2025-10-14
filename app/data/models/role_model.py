from typing import List, Optional
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.datasource.database import database
from app.data.models.audit_mixin import AuditMixin

class RoleModel(database.Base, AuditMixin): 
    __tablename__ = 'role'
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    users: Mapped[List["UserModel"]] = relationship("UserModel", secondary="user_role", back_populates="roles", lazy="raise_on_sql")

    def __repr__(self):
        return f"<Role(id={self.id}, name='{self.name}')>"