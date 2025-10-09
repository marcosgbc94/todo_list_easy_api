from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.result import Result
from app.domain.entities.task_entity import TaskEntity

class ITaskRepository(ABC):
    @abstractmethod
    async def create_task(self, session: AsyncSession, task: TaskEntity) -> Result[TaskEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_task_by_id(self, session: AsyncSession, task_id: int) -> Result[TaskEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_tasks_by_user_id(self, session: AsyncSession, user_id: int) -> Result[List[TaskEntity]]:
        raise NotImplementedError

    @abstractmethod
    async def update_task(self, session: AsyncSession, task: TaskEntity) -> Result[TaskEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete_task(self, session: AsyncSession, task_id: int) -> Result:
        raise NotImplementedError