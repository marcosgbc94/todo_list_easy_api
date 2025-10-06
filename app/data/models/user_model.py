from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.datasource.database import database
from app.data.models.audit_mixin import AuditMixin 

class UserModel(database.Base, AuditMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    
    roles: Mapped[List["Role"]] = relationship("Role", secondary="user_role", back_populates="users")
    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}')>"