from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.result import Result
from app.domain.entities.tag_entity import TagEntity
from app.domain.ports.i_tag_repository import ITagRepository
from datetime import datetime, timezone

class TagService:
    def __init__(self, tag_repository: ITagRepository, db_session: AsyncSession):
        self.repo = tag_repository
        self.session = db_session

    async def get_all(self) -> Result[List[TagEntity]]:
        return await self.repo.get_all_tags(self.session)

    async def create(self, tag_data: TagEntity, user_id: int) -> Result[TagEntity]:
        tag_data.created_by = user_id
        tag_data.created_at = datetime.now(timezone.utc)
        return await self.repo.create_tag(self.session, tag_data)

    async def update(self, tag_id: int, tag_data: TagEntity, user_id: int) -> Result[TagEntity]:
        tag_data.updated_by = user_id
        tag_data.updated_at = datetime.now(timezone.utc)
        return await self.repo.update_tag(self.session, tag_id, tag_data)

    async def delete(self, tag_id: int) -> Result:
        return await self.repo.delete_tag(self.session, tag_id)