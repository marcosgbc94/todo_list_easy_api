from core.result import Result
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.user_entity import UserEntity
from data.repositories.user_repository import UserRepository

class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, session: AsyncSession, user_id: int) -> Result[UserEntity]:
        return await self.user_repository.get_user_by_id(session, user_id)