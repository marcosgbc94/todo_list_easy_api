from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.result import Result
from app.domain.entities.status_entity import StatusEntity

class IStatusRepository(ABC):
    @abstractmethod
    async def create_status(self, session: AsyncSession, status: StatusEntity) -> Result[StatusEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_status_by_id(self, session: AsyncSession, status_id: int) -> Result[StatusEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_status(self, session: AsyncSession) -> Result[List[StatusEntity]]:
        raise NotImplementedError

    @abstractmethod
    async def update_status(self, session: AsyncSession, status_id: int, status_data: StatusEntity) -> Result[StatusEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete_status(self, session: AsyncSession, status_id: int) -> Result:
        raise NotImplementedError