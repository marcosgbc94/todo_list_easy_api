from fastapi import HTTPException
from data.repositories.user_repository import UserRepository
from domain.entities.user_entity import UserEntity
from sqlalchemy.ext.asyncio import AsyncSession

class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, session: AsyncSession, user_data: UserEntity) -> UserEntity:
        if not user_data or not user_data.password:
            raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
        
        user_data.password_hash = UserEntity.set_password(user_data.password)
        user_data.created_at = UserEntity.get_datetime_now()
        user_data.created_by = 1

        return await self.user_repository.create_user(session, user_data)