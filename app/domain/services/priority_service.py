from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.result import Result
from app.domain.entities.priority_entity import PriorityEntity
from app.domain.ports.i_priority_repository import IPriorityRepository
from datetime import datetime, timezone

class PriorityService:
    def __init__(self, priority_repository: IPriorityRepository, db_session: AsyncSession):
        self.repo = priority_repository
        self.session = db_session

    async def get_all(self) -> Result[List[PriorityEntity]]:
        return await self.repo.get_all_priorities(self.session)

    async def create(self, priority_data: PriorityEntity, user_id: int) -> Result[PriorityEntity]:
        priority_data.created_by = user_id
        priority_data.created_at = datetime.now(timezone.utc)
        return await self.repo.create_priority(self.session, priority_data)

    async def update(self, priority_id: int, priority_data: PriorityEntity, user_id: int) -> Result[PriorityEntity]:
        priority_data.updated_by = user_id
        priority_data.updated_at = datetime.now(timezone.utc)
        return await self.repo.update_priority(self.session, priority_id, priority_data)

    async def delete(self, priority_id: int) -> Result:
        return await self.repo.delete_priority(self.session, priority_id)