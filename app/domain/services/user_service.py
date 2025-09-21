from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from core.result import Result
from core.error_list import ErrorCode
from domain.entities.user_entity import UserEntity
from domain.ports.i_user_repository import IUserRepository

class UserService:
    def __init__(self, user_repository: IUserRepository, database_session: AsyncSession):
        self.repo = user_repository
        self.session = database_session

    async def get_all_users(self) -> Result[List[UserEntity]]:
        return await self.repo.get_users(session=self.session)

    async def get_user_by_id(self, user_id: int) -> Result[UserEntity]:
        return await self.repo.get_user_by_id(session=self.session, user_id=user_id)

    async def create_new_user(self, user_data: UserEntity) -> Result[UserEntity]:
        if not user_data or not user_data.password:
            return Result.fail("Faltan parámetros", ErrorCode.PARAMS_NOT_FOUND)
        
        user_data.password_hash = UserEntity.set_password(user_data.password)
        user_data.created_at = UserEntity.get_datetime_now()
        user_data.created_by = 1  # Placeholder

        return await self.repo.create_user(self.session, user_data)

    async def update_existing_user(self, user_id: int, user_data: UserEntity) -> Result[UserEntity]:
        user_data.id = user_id
        if not user_data.password:
            return Result.fail("Faltan parámetros", ErrorCode.PARAMS_NOT_FOUND)
        
        user_data.password_hash = UserEntity.set_password(user_data.password)
        user_data.updated_at = UserEntity.get_datetime_now()
        user_data.updated_by = 1  # Placeholder

        return await self.repo.update_user_by_id(session=self.session, user_data=user_data)

    async def delete_user_by_id(self, user_id: int) -> Result:
        return await self.repo.delete_user_by_id(session=self.session, user_id=user_id)