from core.error_list import ErrorCode
from core.result import Result
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.user_entity import UserEntity
from data.repositories.user_repository import UserRepository

class UpdateUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, session: AsyncSession, user_data: UserEntity) -> Result[UserEntity]:
        if not user_data or not user_data.password:
            return Result.fail("Faltan parámetros", ErrorCode.PARAMS_NOT_FOUND)
        
        user_data.password_hash = UserEntity.set_password(user_data.password)
        user_data.updated_at = UserEntity.get_datetime_now()
        user_data.updated_by = 1

        return await self.user_repository.update_user_by_id(session=session, user_data=user_data)