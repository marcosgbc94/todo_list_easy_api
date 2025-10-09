from typing import Annotated, TypeAlias
from fastapi import Depends
from app.domain.services.task_service import TaskService
from app.presentation.api.dependencies.core_dependencies import DataBaseSessionDependency, TaskRepositoryDependency

# Proveedor de servicio de Tareas
def get_task_service(repository: TaskRepositoryDependency, session: DataBaseSessionDependency) -> TaskService:
    return TaskService(task_repository=repository, database_session=session)

TaskServiceDependency: TypeAlias = Annotated[TaskService, Depends(get_task_service)]