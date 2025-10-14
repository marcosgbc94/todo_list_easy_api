import datetime
from typing import List, Optional

from sqlalchemy import Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.datasource.database import database
from app.data.models.audit_mixin import AuditMixin 

class TaskModel(database.Base, AuditMixin):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status_id: Mapped[int] = mapped_column(Integer, ForeignKey('status.id'))
    priority_id: Mapped[int] = mapped_column(Integer, ForeignKey('priority.id'))
    due_date: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)

    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="tasks", lazy="raise_on_sql")
    status_type: Mapped["StatusModel"] = relationship("StatusModel", back_populates="tasks", lazy="raise_on_sql")
    priority_level: Mapped["PriorityModel"] = relationship("PriorityModel", back_populates="tasks", lazy="raise_on_sql")
    tags: Mapped[List["TagModel"]] = relationship("TagModel", secondary="tasktag", back_populates="tasks", lazy="raise_on_sql")

    def __repr__(self):
        return f"<Task(id={self.id}, title='{self.title}', user_id={self.user_id})>"