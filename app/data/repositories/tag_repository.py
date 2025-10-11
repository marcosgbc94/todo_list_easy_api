from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.result import Result
from app.core.error_list import ErrorCode
from app.domain.entities.tag_entity import TagEntity
from app.domain.ports.i_tag_repository import ITagRepository
from app.data.models.tag_model import TagModel

class TagRepository(ITagRepository):
    async def create_tag(self, session: AsyncSession, tag_data: TagEntity) -> Result[TagEntity]:
        new_tag = TagModel(name=tag_data.name, color=tag_data.color) # Asumiendo que Tag tiene color
        session.add(new_tag)
        try:
            await session.commit()
            await session.refresh(new_tag)
            return Result.ok(TagEntity(**new_tag.__dict__))
        except IntegrityError:
            await session.rollback()
            return Result.fail("La etiqueta ya existe", ErrorCode.TAG_ALREADY_EXISTS)

    async def get_all_tags(self, session: AsyncSession) -> Result[List[TagEntity]]:
        result = await session.execute(select(TagModel))
        tags = result.scalars().all()
        tag_entities = [TagEntity(**t.__dict__) for t in tags]
        return Result.ok(tag_entities)

    async def update_tag(self, session: AsyncSession, tag_id: int, tag_data: TagEntity) -> Result[TagEntity]:
        tag_to_update = await session.get(TagModel, tag_id)
        if not tag_to_update:
            return Result.fail("Etiqueta no encontrada", ErrorCode.TAG_NOT_FOUND)

        tag_to_update.name = tag_data.name
        tag_to_update.updated_at = tag_data.updated_at
        tag_to_update.updated_by = tag_data.updated_by

        try:
            await session.commit()
            await session.refresh(tag_to_update)
            return Result.ok(TagEntity(**tag_to_update.__dict__))
        except IntegrityError:
            await session.rollback()
            return Result.fail("El nombre de la etiqueta ya existe", ErrorCode.TAG_ALREADY_EXISTS)

    async def delete_tag(self, session: AsyncSession, tag_id: int) -> Result:
        tag = await session.get(TagModel, tag_id)
        if not tag:
            return Result.fail("Etiqueta no encontrada", ErrorCode.TAG_NOT_FOUND)

        try:
            await session.delete(tag)
            await session.commit()
            return Result.ok()
        except IntegrityError:
            await session.rollback()
            return Result.fail(
                "No se puede eliminar la etiqueta porque está en uso por una o más tareas.",
                ErrorCode.INTERNAL_ERROR
            )