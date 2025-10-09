from typing import Annotated, TypeAlias
from app.data.repositories.task_repository import TaskRepository
from app.domain.ports.i_task_repository import ITaskRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.datasource.database import database
from app.domain.ports.i_user_repository import IUserRepository
from app.data.repositories.user_repository import UserRepository

DataBaseSessionDependency: TypeAlias = Annotated[AsyncSession, Depends(database.get_session_database)]

def get_user_repository() -> IUserRepository:
    return UserRepository()

UserRepositoryDependency: TypeAlias = Annotated[IUserRepository, Depends(get_user_repository)]

def get_task_repository() -> ITaskRepository:
    return TaskRepository()

TaskRepositoryDependency: TypeAlias = Annotated[ITaskRepository, Depends(get_task_repository)]