from typing import List
from core.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.user_entity import UserEntity
from data.repositories.user_repository import UserRepository

class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, session: AsyncSession, user_id: int) -> Result:
        return await self.user_repository.delete_user_by_id(session=session, user_id=user_id)