from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.result import Result
from app.domain.entities.priority_entity import PriorityEntity

class IPriorityRepository(ABC):
    @abstractmethod
    async def create_priority(self, session: AsyncSession, priority: PriorityEntity) -> Result[PriorityEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_priorities(self, session: AsyncSession) -> Result[List[PriorityEntity]]:
        raise NotImplementedError

    @abstractmethod
    async def update_priority(self, session: AsyncSession, priority_id: int, priority_data: PriorityEntity) -> Result[PriorityEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete_priority(self, session: AsyncSession, priority_id: int) -> Result:
        raise NotImplementedError