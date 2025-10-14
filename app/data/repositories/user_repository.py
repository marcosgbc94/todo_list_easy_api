from app.domain.ports.i_user_repository import IUserRepository
from app.core.error_list import ErrorCode
from app.core.result import Result
from sqlalchemy import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.domain.entities.user_entity import UserEntity
from app.data.models.user_model import UserModel
from sqlalchemy.orm import selectinload
from app.domain.entities.role_entity import RoleEntity

class UserRepository(IUserRepository):
    async def get_users(self, session: AsyncSession) -> Result[List[UserEntity]]:
        result = await session.execute(select(UserModel))
        users = result.scalars().all()

        if not users:
            return Result.fail("Ningún usuario registrado", ErrorCode.USERS_NOT_FOUND)
        
        # Se convierte salida UserModel a UserEntity
        user_entities = [
            UserEntity(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at,
                created_by=user.created_by,
                updated_at=user.updated_at,
                updated_by=user.updated_by
            )
            for user in users
        ]

        return Result.ok(user_entities)

    async def get_user_by_id(self, session: AsyncSession, user_id: int) -> Result[UserEntity]:
        result = await session.execute(
            select(UserModel)
            .where(UserModel.id == user_id)
            .options(selectinload(UserModel.roles))
        )
        user = result.scalar_one_or_none()  # devuelve el primer registro o None

        if not user:
            return Result.fail("Usuario no existe", ErrorCode.USER_NOT_FOUND)
        
        user_entity = UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            created_by=user.created_by,
            updated_at=user.updated_at,
            updated_by=user.updated_by,
        )
        
        # Se convierte los RoleModel a RoleEntity
        if user.roles:
            user_entity.roles = [
                RoleEntity(
                    id=role.id,
                    name=role.name,
                    description=role.description
                ) for role in user.roles
            ]

        return Result.ok(user_entity)

    async def get_user_by_username(self, session: AsyncSession, username: str) -> Result[UserEntity]:
        result = await session.execute(
            select(UserModel)
            .where(UserModel.username == username)
            .options(selectinload(UserModel.roles))
        )
        user = result.scalar_one_or_none()  # devuelve el primer registro o None
        
        if not user:
            return Result.fail("Usuario no existe", ErrorCode.USER_NOT_FOUND)
        
        user_entity = UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            created_by=user.created_by,
            updated_at=user.updated_at,
            updated_by=user.updated_by,
        )

        if user.roles:
            user_entity.roles = [
                RoleEntity(
                    id=role.id,
                    name=role.name,
                    description=role.description
                ) for role in user.roles
            ]

        return Result.ok(user_entity)

    async def create_user(self, session: AsyncSession, user_data: UserEntity) -> Result[UserEntity]:
        # Mapeo del entity al modelo
        user = UserModel(
            username=user_data.username,
            email=user_data.email,
            password_hash=user_data.password_hash,
            created_at=user_data.created_at,
            created_by=user_data.created_by
        )
        session.add(user)

        try:
            await session.commit()
            await session.refresh(user)
        except IntegrityError as e:
            await session.rollback()

            if getattr(e.orig, 'pgcode', None) == '23505':
                return Result.fail("Usuario ya existe", ErrorCode.USER_ALREADY_EXISTS)
            else:
                return Result.fail("Error interno", ErrorCode.INTERNAL_ERROR)

        return Result.ok(
            UserEntity(
                id=user.id,
                username=user.username,
                email=user.email,
                created_at=user.created_at,
                created_by=user.created_by,
                updated_at=user.updated_at,
                updated_by=user.updated_by
            )
        )

    async def update_user_by_id(self, session: AsyncSession, user_data: UserEntity) -> Result[UserEntity]:
        user_model_mapped = await session.get(UserModel, user_data.id)
        if not user_model_mapped:
            return Result.fail("Usuario no existe", ErrorCode.USER_NOT_FOUND)

        user_model_mapped.username = user_data.username
        user_model_mapped.email = user_data.email
        user_model_mapped.password_hash = user_data.password_hash    
        user_model_mapped.updated_at = user_data.updated_at
        user_model_mapped.updated_by = user_data.updated_by
        
        try:
            await session.commit()
            await session.refresh(user_model_mapped)
        except IntegrityError as e:
            await session.rollback()
            
            if "unique constraint" in str(e.orig).lower() or getattr(e.orig, "pgcode", None) == "23505":
                return Result.fail("Usuario ya existe", ErrorCode.USER_ALREADY_EXISTS)
            else:
                return Result.fail("Error interno", ErrorCode.INTERNAL_ERROR)
        
        return Result.ok(
            UserEntity(
                id=user_model_mapped.id,
                username=user_model_mapped.username,
                email=user_model_mapped.email,
                created_at=user_model_mapped.created_at,
                created_by=user_model_mapped.created_by,
                updated_at=user_model_mapped.updated_at,
                updated_by=user_model_mapped.updated_by
            )
        )
    
    async def delete_user_by_id(self, session: AsyncSession, user_id: int) -> Result:
        user = await session.get(UserModel, user_id)
        if not user:
            return Result.fail("Usuario no encontrado", ErrorCode.USER_NOT_FOUND)
        
        try:
            await session.delete(user)
            await session.commit()
        except IntegrityError as e:
            await session.rollback()

            return Result.fail("Error interno", ErrorCode.INTERNAL_ERROR)
        
        return Result.ok()
    