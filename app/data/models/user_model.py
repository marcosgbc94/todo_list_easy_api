from sqlalchemy import Column, Integer, String, DateTime
from data.datasource.database import database

class UserModel(database.Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime(timezone=True), nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=True)
    updated_by = Column(Integer, nullable=True)