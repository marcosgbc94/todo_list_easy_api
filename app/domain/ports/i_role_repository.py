from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.result import Result
from app.domain.entities.role_entity import RoleEntity

class IRoleRepository(ABC):
    @abstractmethod
    async def create_role(self, session: AsyncSession, role: RoleEntity) -> Result[RoleEntity]:
        raise NotImplementedError

    @abstractmethod
    async def get_all_roles(self, session: AsyncSession) -> Result[List[RoleEntity]]:
        raise NotImplementedError

    @abstractmethod
    async def delete_role(self, session: AsyncSession, role_id: int) -> Result:
        raise NotImplementedError

    @abstractmethod
    async def assign_role_to_user(self, session: AsyncSession, user_id: int, role_id: int) -> Result:
        raise NotImplementedError

    @abstractmethod
    async def revoke_role_from_user(self, session: AsyncSession, user_id: int, role_id: int) -> Result:
        raise NotImplementedError