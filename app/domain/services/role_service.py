from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.result import Result
from app.domain.entities.role_entity import RoleEntity
from app.domain.ports.i_role_repository import IRoleRepository
from datetime import datetime, timezone

class RoleService:
    def __init__(self, role_repository: IRoleRepository, db_session: AsyncSession):
        self.repo = role_repository
        self.session = db_session

    async def get_all(self) -> Result[List[RoleEntity]]:
        return await self.repo.get_all_roles(self.session)

    async def create(self, role_data: RoleEntity, user_id: int) -> Result[RoleEntity]:
        role_data.created_by = user_id
        role_data.created_at = datetime.now(timezone.utc)
        return await self.repo.create_role(self.session, role_data)

    async def delete(self, role_id: int) -> Result:
        return await self.repo.delete_role(self.session, role_id)

    async def assign_to_user(self, user_id: int, role_id: int) -> Result:
        return await self.repo.assign_role_to_user(self.session, user_id, role_id)

    async def revoke_from_user(self, user_id: int, role_id: int) -> Result:
        return await self.repo.revoke_role_from_user(self.session, user_id, role_id)