from typing import Annotated, TypeAlias
from app.data.repositories.task_repository import TaskRepository
from app.domain.ports.i_task_repository import ITaskRepository
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.datasource.database import database
from app.domain.ports.i_user_repository import IUserRepository
from app.data.repositories.user_repository import UserRepository
from app.domain.ports.i_status_repository import IStatusRepository
from app.data.repositories.status_repository import StatusRepository
from app.domain.ports.i_priority_repository import IPriorityRepository
from app.data.repositories.priority_repository import PriorityRepository
from app.domain.ports.i_tag_repository import ITagRepository
from app.data.repositories.tag_repository import TagRepository
from app.domain.ports.i_role_repository import IRoleRepository
from app.data.repositories.role_repository import RoleRepository

DataBaseSessionDependency: TypeAlias = Annotated[AsyncSession, Depends(database.get_session_database)]

def get_user_repository() -> IUserRepository:
    return UserRepository()

UserRepositoryDependency: TypeAlias = Annotated[IUserRepository, Depends(get_user_repository)]

def get_task_repository() -> ITaskRepository:
    return TaskRepository()

TaskRepositoryDependency: TypeAlias = Annotated[ITaskRepository, Depends(get_task_repository)]

def get_status_repository() -> IStatusRepository:
    return StatusRepository()

StatusRepositoryDependency: TypeAlias = Annotated[IStatusRepository, Depends(get_status_repository)]

def get_priority_repository() -> IPriorityRepository:
    return PriorityRepository()

PriorityRepositoryDependency: TypeAlias = Annotated[IPriorityRepository, Depends(get_priority_repository)]

def get_tag_repository() -> ITagRepository:
    return TagRepository()

TagRepositoryDependency: TypeAlias = Annotated[ITagRepository, Depends(get_tag_repository)]

def get_role_repository() -> IRoleRepository:
    return RoleRepository()

RoleRepositoryDependency: TypeAlias = Annotated[IRoleRepository, Depends(get_role_repository)]