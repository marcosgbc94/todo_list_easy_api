from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.result import Result
from app.domain.entities.status_entity import StatusEntity
from app.domain.ports.i_status_repository import IStatusRepository
from datetime import datetime, timezone

class StatusService:
    def __init__(self, status_repository: IStatusRepository, db_session: AsyncSession):
        self.repo = status_repository
        self.session = db_session

    async def get_all(self) -> Result[List[StatusEntity]]:
        return await self.repo.get_all_status(self.session)

    async def create(self, status_data: StatusEntity, user_id: int) -> Result[StatusEntity]:
        status_data.created_by = user_id
        status_data.created_at = datetime.now(timezone.utc)
        return await self.repo.create_status(self.session, status_data)

    async def update(self, status_id: int, status_data: StatusEntity, user_id: int) -> Result[StatusEntity]:
        status_data.updated_by = user_id
        status_data.updated_at = datetime.now(timezone.utc)
        return await self.repo.update_status(self.session, status_id, status_data)

    async def delete(self, status_id: int) -> Result:
        return await self.repo.delete_status(self.session, status_id)