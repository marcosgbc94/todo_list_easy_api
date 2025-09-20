from asyncpg import UniqueViolationError
from sqlalchemy import select
from typing import List
from fastapi import HTTPException
from psycopg2.errors import UniqueViolation
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from domain.entities.user_entity import UserEntity
from data.models.user_model import UserModel

class UserRepository:
    async def get_users(session: AsyncSession) -> List[UserEntity]:
        result = await session.execute(select(UserModel))
        users = result.scalars().all()
        
        # Se convierte salida UserModel a UserEntity
        return [
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

    async def get_user_by_id(session: AsyncSession, user_id: int) -> UserEntity:
        result = await session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user = result.scalar_one_or_none()  # devuelve el primer registro o None

        if not user:
            return None
        
        return UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            created_by=user.created_by,
            updated_at=user.updated_at,
            updated_by=user.updated_by
        )

    async def create_user(session: AsyncSession, user_data: UserEntity) -> UserEntity:
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
                raise HTTPException(
                    status_code=400,
                    detail="Usuario o correo ya existe"
                )
            raise HTTPException(
                status_code=500,
                detail="Error interno de la base de datos"
            )

        return UserEntity(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            created_by=user.created_by,
            updated_at=user.updated_at,
            updated_by=user.updated_by
        )

    async def update_user_by_id(session: AsyncSession, user_data: UserEntity):
        user_model_mapped = await session.get(UserModel, user_data.id)
        if not user_model_mapped:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

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
                raise HTTPException(status_code=400, detail="Usuario o correo ya existe")
            raise HTTPException(status_code=500, detail="Error interno de la base de datos")
        
        return UserEntity(
            id=user_model_mapped.id,
            username=user_model_mapped.username,
            email=user_model_mapped.email,
            created_at=user_model_mapped.created_at,
            created_by=user_model_mapped.created_by,
            updated_at=user_model_mapped.updated_at,
            updated_by=user_model_mapped.updated_by
        )