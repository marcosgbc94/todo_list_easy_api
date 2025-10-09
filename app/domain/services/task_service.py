from typing import List
from app.core.result import Result
from app.domain.entities.task_entity import TaskEntity
from app.domain.ports.i_task_repository import ITaskRepository
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

class TaskService:
    def __init__(self, task_repository: ITaskRepository, database_session: AsyncSession):
        self.repo = task_repository
        self.session = database_session

    async def create_task_for_user(self, task_data: TaskEntity, user_id: int) -> Result[TaskEntity]:
        task_data.user_id = user_id
        task_data.created_by = user_id
        task_data.created_at = datetime.now(timezone.utc)
        # Aquí podrías añadir validaciones de negocio, por ejemplo:
        # if not task_data.title:
        #     return Result.fail("El título es obligatorio", ErrorCode.PARAMS_NOT_FOUND)
        return await self.repo.create_task(self.session, task_data)

    async def get_tasks_for_user(self, user_id: int) -> Result[List[TaskEntity]]:
        return await self.repo.get_tasks_by_user_id(self.session, user_id)

    async def update_task(self, task_data: TaskEntity, task_id: int, user_id: int) -> Result[TaskEntity]:
        # Verificación de que el usuario es dueño de la tarea
        result = await self.repo.get_task_by_id(self.session, task_id)
        if not result.success or result.data.user_id != user_id:
             return Result.fail("No autorizado para modificar esta tarea", ErrorCode.INTERNAL_ERROR) # Deberías crear un ErrorCode.UNAUTHORIZED

        task_data.id = task_id
        task_data.updated_by = user_id
        task_data.updated_at = datetime.now(timezone.utc)
        return await self.repo.update_task(self.session, task_data)

    async def delete_task(self, task_id: int, user_id: int) -> Result:
        # Verificación de que el usuario es dueño de la tarea
        result = await self.repo.get_task_by_id(self.session, task_id)
        if not result.success or result.data.user_id != user_id:
             return Result.fail("No autorizado para eliminar esta tarea", ErrorCode.INTERNAL_ERROR)

        return await self.repo.delete_task(self.session, task_id)