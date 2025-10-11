from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.result import Result
from app.domain.entities.tag_entity import TagEntity

class ITagRepository(ABC):
    @abstractmethod
    async def create_tag(self, session: AsyncSession, tag: TagEntity) -> Result[TagEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_tags(self, session: AsyncSession) -> Result[List[TagEntity]]:
        raise NotImplementedError

    @abstractmethod
    async def update_tag(self, session: AsyncSession, tag_id: int, tag_data: TagEntity) -> Result[TagEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete_tag(self, session: AsyncSession, tag_id: int) -> Result:
        raise NotImplementedError