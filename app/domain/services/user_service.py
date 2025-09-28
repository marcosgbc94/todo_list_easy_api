from typing import List, Optional
from core.security import verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from core.result import Result
from core.error_list import ErrorCode
from domain.entities.user_entity import UserEntity
from domain.ports.i_user_repository import IUserRepository

class UserService:
    def __init__(self, user_repository: IUserRepository, database_session: AsyncSession):
        self.repo = user_repository
        self.session = database_session

    async def authenticate_user(self, username: str, password: str) -> Result[UserEntity]:
        result = await self.repo.get_user_by_username(self.session, username)
        if not result.success or not result.data:
            return Result.fail("Usuario no encontrado", ErrorCode.USER_NOT_FOUND)
        
        user = result.data
        
        if not verify_password(password, user.password_hash):
            return Result.fail("Error de credenciales", ErrorCode.USER_BAD_CREDENTIALS)
            
        return Result.ok(user)

    async def get_all_users(self) -> Result[List[UserEntity]]:
        return await self.repo.get_users(session=self.session)

    async def get_user_by_id(self, user_id: int) -> Result[UserEntity]:
        return await self.repo.get_user_by_id(session=self.session, user_id=user_id)

    async def get_user_by_username(self, username: str) -> Result[UserEntity]:
        return await self.repo.get_user_by_username(session=self.session, username=username)

    async def create_new_user(self, user_data: UserEntity, performed_by_id: int) -> Result[UserEntity]:
        if not user_data or not user_data.password:
            return Result.fail("Faltan parámetros", ErrorCode.PARAMS_NOT_FOUND)
        
        if not performed_by_id:
            return Result.fail("Usuario no logueado", ErrorCode.USER_NOT_LOGIN)
        
        user_data.password_hash = UserEntity.set_password(user_data.password)
        user_data.created_at = UserEntity.get_datetime_now()
        user_data.created_by = performed_by_id

        return await self.repo.create_user(self.session, user_data)

    async def update_existing_user(self, user_id: int, user_data: UserEntity, performed_by_id: int) -> Result[UserEntity]:
        user_data.id = user_id
        if not user_data.password:
            return Result.fail("Faltan parámetros", ErrorCode.PARAMS_NOT_FOUND)
        
        if not performed_by_id:
            return Result.fail("Usuario no logueado", ErrorCode.USER_NOT_LOGIN)
        
        user_data.password_hash = UserEntity.set_password(user_data.password)
        user_data.updated_at = UserEntity.get_datetime_now()
        user_data.updated_by = performed_by_id

        return await self.repo.update_user_by_id(session=self.session, user_data=user_data)

    async def delete_user_by_id(self, user_id: int) -> Result:
        return await self.repo.delete_user_by_id(session=self.session, user_id=user_id)