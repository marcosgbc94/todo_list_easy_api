from abc import ABC, abstractmethod
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from core.result import Result
from domain.entities.user_entity import UserEntity

class IUserRepository(ABC):
    @abstractmethod
    async def get_users(self, session: AsyncSession) -> Result[List[UserEntity]]:
        raise NotImplementedError

    @abstractmethod
    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> Result[UserEntity]:
        raise NotImplementedError
    
    @abstractmethod
    async def get_user_by_username(self, session: AsyncSession, username: str) -> Result[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    async def create_user(self, session: AsyncSession, user_data: UserEntity) -> Result[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    async def update_user_by_id(self, session: AsyncSession, user_data: UserEntity) -> Result[UserEntity]:
        raise NotImplementedError

    @abstractmethod
    async def delete_user_by_id(self, session: AsyncSession, user_id: int) -> Result:
        raise NotImplementedError