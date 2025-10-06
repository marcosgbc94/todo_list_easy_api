from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.data.datasource.database import database
from app.data.models.audit_mixin import AuditMixin 

class UserRoleModel(database.Base, AuditMixin):
    __tablename__ = 'user_role'

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), primary_key=True)
    role_id: Mapped[int] = mapped_column(Integer, ForeignKey('role.id'), primary_key=True)

    user: Mapped["User"] = relationship("User", backref="user_roles_link")
    role: Mapped["Role"] = relationship("Role", backref="role_users_link")

    def __repr__(self):
        return f"<UserRole(user_id={self.user_id}, role_id={self.role_id})>"