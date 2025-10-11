from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.result import Result
from app.core.error_list import ErrorCode
from app.domain.entities.role_entity import RoleEntity
from app.domain.ports.i_role_repository import IRoleRepository
from app.data.models.role_model import RoleModel
from app.data.models.user_model import UserModel
from app.data.models.user_role_model import UserRoleModel

class RoleRepository(IRoleRepository):
    async def create_role(self, session: AsyncSession, role_data: RoleEntity) -> Result[RoleEntity]:
        new_role = RoleModel(**role_data.__dict__)
        session.add(new_role)
        try:
            await session.commit()
            await session.refresh(new_role)
            return Result.ok(RoleEntity(**new_role.__dict__))
        except IntegrityError:
            await session.rollback()
            return Result.fail("El rol ya existe", ErrorCode.ROLE_ALREADY_EXISTS)

    async def get_all_roles(self, session: AsyncSession) -> Result[List[RoleEntity]]:
        result = await session.execute(select(RoleModel))
        roles = result.scalars().all()
        return Result.ok([RoleEntity(**role.__dict__) for role in roles])

    async def delete_role(self, session: AsyncSession, role_id: int) -> Result:
        role = await session.get(RoleModel, role_id)
        if not role:
            return Result.fail("Rol no encontrado", ErrorCode.ROLE_NOT_FOUND)

        try:
            await session.delete(role)
            await session.commit()
            return Result.ok()
        except IntegrityError:
            await session.rollback()
            return Result.fail(
                "No se puede eliminar el rol porque está asignado a uno o más usuarios.",
                ErrorCode.INTERNAL_ERROR
            )

    async def assign_role_to_user(self, session: AsyncSession, user_id: int, role_id: int) -> Result:
        user = await session.get(UserModel, user_id)
        if not user:
            return Result.fail("Usuario no encontrado", ErrorCode.USER_NOT_FOUND)

        role = await session.get(RoleModel, role_id)
        if not role:
            return Result.fail("Rol no encontrado", ErrorCode.ROLE_NOT_FOUND)

        user_role = UserRoleModel(user_id=user_id, role_id=role_id)
        session.add(user_role)
        try:
            await session.commit()
            return Result.ok()
        except IntegrityError:
            await session.rollback()
            return Result.fail("El usuario ya tiene este rol asignado", ErrorCode.ROLE_ALREADY_EXISTS)

    async def revoke_role_from_user(self, session: AsyncSession, user_id: int, role_id: int) -> Result:
        stmt = delete(UserRoleModel).where(
            UserRoleModel.user_id == user_id,
            UserRoleModel.role_id == role_id
        )
        result = await session.execute(stmt)
        if result.rowcount == 0:
            return Result.fail("El usuario no tiene este rol asignado", ErrorCode.ROLE_NOT_FOUND)

        await session.commit()
        return Result.ok()