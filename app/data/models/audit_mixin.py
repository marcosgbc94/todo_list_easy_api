import datetime
from typing import Optional
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

class AuditMixin:
    """Mixin para campos de auditoría comunes."""
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now)
    created_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime(timezone=True), default=datetime.datetime.now, onupdate=datetime.datetime.now, nullable=True)
    updated_by: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    def __repr__(self):
        display_attr = getattr(self, 'name', None) or getattr(self, 'title', None) or getattr(self, 'id', None)
        return f"<{self.__class__.__name__}({display_attr})>"