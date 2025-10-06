from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.datasource.database import database
from app.data.models.audit_mixin import AuditMixin 

class TaskTagModel(database.Base, AuditMixin):
    __tablename__ = 'tasktag'

    task_id: Mapped[int] = mapped_column(Integer, ForeignKey('task.id'), primary_key=True)
    tag_id: Mapped[int] = mapped_column(Integer, ForeignKey('tag.id'), primary_key=True)

    task: Mapped["Task"] = relationship("Task", backref="task_tags_link")
    tag: Mapped["Tag"] = relationship("Tag", backref="tag_tasks_link")

    def __repr__(self):
        return f"<TaskTag(task_id={self.task_id}, tag_id={self.tag_id})>"