from typing import List, Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.datasource.database import database
from app.data.models.audit_mixin import AuditMixin 

class StatusModel(database.Base, AuditMixin):
    __tablename__ = 'status'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    color: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    tasks: Mapped[List["Task"]] = relationship("Task", back_populates="status_type")

    def __repr__(self):
        return f"<Status(id={self.id}, name='{self.name}')>"