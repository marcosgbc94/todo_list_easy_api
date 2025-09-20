from typing import List
from core.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.user_entity import UserEntity
from data.repositories.user_repository import UserRepository

class GetUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, session: AsyncSession) -> Result[List[UserEntity]]:
        return await self.user_repository.get_users(session=session)