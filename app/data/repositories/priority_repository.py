from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.result import Result
from app.core.error_list import ErrorCode
from app.domain.entities.priority_entity import PriorityEntity
from app.domain.ports.i_priority_repository import IPriorityRepository
from app.data.models.priority_model import PriorityModel

class PriorityRepository(IPriorityRepository):
    async def create_priority(self, session: AsyncSession, priority_data: PriorityEntity) -> Result[PriorityEntity]:
        new_priority = PriorityModel(**priority_data.__dict__)
        session.add(new_priority)
        try:
            await session.commit()
            await session.refresh(new_priority)
            return Result.ok(PriorityEntity(**new_priority.__dict__))
        except IntegrityError:
            await session.rollback()
            return Result.fail("La prioridad ya existe", ErrorCode.PRIORITY_ALREADY_EXISTS)

    async def get_all_priorities(self, session: AsyncSession) -> Result[List[PriorityEntity]]:
        result = await session.execute(select(PriorityModel))
        priorities = result.scalars().all()
        priority_entities = [PriorityEntity(**p.__dict__) for p in priorities]
        return Result.ok(priority_entities)

    async def update_priority(self, session: AsyncSession, priority_id: int, priority_data: PriorityEntity) -> Result[PriorityEntity]:
        priority_to_update = await session.get(PriorityModel, priority_id)
        if not priority_to_update:
            return Result.fail("Prioridad no encontrada", ErrorCode.PRIORITY_NOT_FOUND)

        priority_to_update.name = priority_data.name
        priority_to_update.color = priority_data.color
        priority_to_update.updated_at = priority_data.updated_at
        priority_to_update.updated_by = priority_data.updated_by

        try:
            await session.commit()
            await session.refresh(priority_to_update)
            return Result.ok(PriorityEntity(**priority_to_update.__dict__))
        except IntegrityError:
            await session.rollback()
            return Result.fail("El nombre de la prioridad ya existe", ErrorCode.PRIORITY_ALREADY_EXISTS)

    async def delete_priority(self, session: AsyncSession, priority_id: int) -> Result:
        priority = await session.get(PriorityModel, priority_id)
        if not priority:
            return Result.fail("Prioridad no encontrada", ErrorCode.PRIORITY_NOT_FOUND)

        try:
            await session.delete(priority)
            await session.commit()
            return Result.ok()
        except IntegrityError:
            await session.rollback()
            # Este error ocurre cuando una foreign key constraint falla.
            return Result.fail(
                ErrorCode.RESOURCE_IN_USE 
            )