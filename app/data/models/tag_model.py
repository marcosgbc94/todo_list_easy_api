from typing import List

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.datasource.database import database
from app.data.models.audit_mixin import AuditMixin 

class TagModel(database.Base, AuditMixin):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)

    tasks: Mapped[List["TaskModel"]] = relationship("TaskModel", secondary="tasktag", back_populates="tags", lazy="raise_on_sql")

    def __repr__(self):
        return f"<Tag(id={self.id}, name='{self.name}')>"