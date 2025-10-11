from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.result import Result
from app.core.error_list import ErrorCode
from app.domain.entities.task_entity import TaskEntity
from app.domain.ports.i_task_repository import ITaskRepository
from app.data.models.task_model import TaskModel
from app.data.models.tag_model import TagModel
from sqlalchemy.orm import selectinload
from typing import List

class TaskRepository(ITaskRepository):
    async def create_task(self, session: AsyncSession, task_data: TaskEntity) -> Result[TaskEntity]:
        new_task = TaskModel(
            user_id=task_data.user_id,
            title=task_data.title,
            description=task_data.description,
            status_id=task_data.status_id,
            priority_id=task_data.priority_id,
            due_date=task_data.due_date,
            created_at=task_data.created_at,
            created_by=task_data.created_by
        )
        session.add(new_task)
        await session.commit()
        await session.refresh(new_task)
        return Result.ok(TaskEntity(**new_task.__dict__))

    async def get_task_by_id(self, session: AsyncSession, task_id: int) -> Result[TaskEntity]:
        result = await session.execute(
            select(TaskModel).where(TaskModel.id == task_id)
        )
        task = result.scalar_one_or_none()
        if not task:
            return Result.fail("Tarea no encontrada", ErrorCode.INTERNAL_ERROR) # Deberías crear un ErrorCode.TASK_NOT_FOUND
        return Result.ok(TaskEntity(**task.__dict__))
    
    async def get_tasks_by_user_id(self, session: AsyncSession, user_id: int) -> Result[List[TaskEntity]]:
        result = await session.execute(
            select(TaskModel).where(TaskModel.user_id == user_id)
        )
        tasks = result.scalars().all()
        if not tasks:
            return Result.fail("El usuario no tiene tareas", ErrorCode.INTERNAL_ERROR) # Deberías crear un ErrorCode.TASKS_NOT_FOUND
        
        task_entities = [TaskEntity(**task.__dict__) for task in tasks]
        return Result.ok(task_entities)

    async def update_task(self, session: AsyncSession, task_data: TaskEntity) -> Result[TaskEntity]:
        task_to_update = await session.get(TaskModel, task_data.id)
        if not task_to_update:
            return Result.fail("Tarea no encontrada", ErrorCode.INTERNAL_ERROR)

        task_to_update.title = task_data.title
        task_to_update.description = task_data.description
        task_to_update.status_id = task_data.status_id
        task_to_update.priority_id = task_data.priority_id
        task_to_update.due_date = task_data.due_date
        task_to_update.updated_at = task_data.updated_at
        task_to_update.updated_by = task_data.updated_by

        await session.commit()
        await session.refresh(task_to_update)
        return Result.ok(TaskEntity(**task_to_update.__dict__))

    async def delete_task(self, session: AsyncSession, task_id: int) -> Result:
        task = await session.get(TaskModel, task_id)
        if not task:
            return Result.fail("Tarea no encontrada", ErrorCode.INTERNAL_ERROR)
        
        await session.delete(task)
        await session.commit()
        return Result.ok()
    
    async def add_tag_to_task(self, session: AsyncSession, task_id: int, tag_id: int) -> Result:
        task = await session.get(TaskModel, task_id, options=[selectinload(TaskModel.tags)])
        if not task:
            return Result.fail("Tarea no encontrada", ErrorCode.INTERNAL_ERROR) # Deberías crear un ErrorCode.TASK_NOT_FOUND
        
        tag = await session.get(TagModel, tag_id)
        if not tag:
            return Result.fail("Etiqueta no encontrada", ErrorCode.TAG_NOT_FOUND)

        if tag in task.tags:
            return Result.fail("La tarea ya tiene esta etiqueta", ErrorCode.TAG_ALREADY_EXISTS)

        task.tags.append(tag)
        await session.commit()
        return Result.ok()

    async def remove_tag_from_task(self, session: AsyncSession, task_id: int, tag_id: int) -> Result:
        task = await session.get(TaskModel, task_id, options=[selectinload(TaskModel.tags)])
        if not task:
            return Result.fail("Tarea no encontrada", ErrorCode.INTERNAL_ERROR)
        
        tag = await session.get(TagModel, tag_id)
        if not tag:
            return Result.fail("Etiqueta no encontrada", ErrorCode.TAG_NOT_FOUND)

        if tag not in task.tags:
            return Result.fail("La tarea no tiene esta etiqueta", ErrorCode.TAG_NOT_FOUND)

        task.tags.remove(tag)
        await session.commit()
        return Result.ok()