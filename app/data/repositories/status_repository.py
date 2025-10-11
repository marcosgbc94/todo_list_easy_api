from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.result import Result
from app.core.error_list import ErrorCode
from app.domain.entities.status_entity import StatusEntity
from app.domain.ports.i_status_repository import IStatusRepository
from app.data.models.status_model import StatusModel

class StatusRepository(IStatusRepository):
    async def create_status(self, session: AsyncSession, status_data: StatusEntity) -> Result[StatusEntity]:
        new_status = StatusModel(**status_data.__dict__)
        session.add(new_status)
        try:
            await session.commit()
            await session.refresh(new_status)
            return Result.ok(StatusEntity(**new_status.__dict__))
        except IntegrityError:
            await session.rollback()
            return Result.fail("El estado ya existe", ErrorCode.STATUS_ALREADY_EXISTS)

    async def get_status_by_id(self, session: AsyncSession, status_id: int) -> Result[StatusEntity]:
        result = await session.get(StatusModel, status_id)
        if not result:
            return Result.fail("Estado no encontrado", ErrorCode.STATUS_NOT_FOUND)
        return Result.ok(StatusEntity(**result.__dict__))

    async def get_all_status(self, session: AsyncSession) -> Result[List[StatusEntity]]:
        result = await session.execute(select(StatusModel))
        statuses = result.scalars().all()
        status_entities = [StatusEntity(**status.__dict__) for status in statuses]
        return Result.ok(status_entities)

    async def update_status(self, session: AsyncSession, status_id: int, status_data: StatusEntity) -> Result[StatusEntity]:
        status_to_update = await session.get(StatusModel, status_id)
        if not status_to_update:
            return Result.fail("Estado no encontrado", ErrorCode.STATUS_NOT_FOUND)

        status_to_update.name = status_data.name
        status_to_update.color = status_data.color
        status_to_update.updated_at = status_data.updated_at
        status_to_update.updated_by = status_data.updated_by

        try:
            await session.commit()
            await session.refresh(status_to_update)
            return Result.ok(StatusEntity(**status_to_update.__dict__))
        except IntegrityError:
            await session.rollback()
            return Result.fail("El nombre del estado ya existe", ErrorCode.STATUS_ALREADY_EXISTS)

    async def delete_status(self, session: AsyncSession, status_id: int) -> Result:
        status = await session.get(StatusModel, status_id)
        if not status:
            return Result.fail("Estado no encontrado", ErrorCode.STATUS_NOT_FOUND)

        try:
            await session.delete(status)
            await session.commit()
            return Result.ok()
        except IntegrityError:
            await session.rollback()
            # Este error ocurre cuando una foreign key constraint falla.
            return Result.fail(
                ErrorCode.RESOURCE_IN_USE
            )