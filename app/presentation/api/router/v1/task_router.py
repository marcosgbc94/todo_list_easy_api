from fastapi import APIRouter, HTTPException
from typing import List
from app.presentation.api.dependencies.auth_dependencies import CurrentUserDependency
from app.domain.entities.task_entity import TaskEntity
from app.presentation.schemas.task_schema import TaskCreateRequest, TaskResponse, TaskUpdateRequest
from app.presentation.api.dependencies.task_dependencies import TaskServiceDependency 

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreateRequest,
    task_service: TaskServiceDependency,
    current_user: CurrentUserDependency
):
    task_entity = TaskEntity(**task_data.model_dump())
    result = await task_service.create_task_for_user(task_entity, current_user.id)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.data

@router.get("", response_model=List[TaskResponse])
async def get_my_tasks(
    task_service: TaskServiceDependency,
    current_user: CurrentUserDependency
):
    result = await task_service.get_tasks_for_user(current_user.id)
    if not result.success:
        return []
    return result.data

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdateRequest,
    task_service: TaskServiceDependency,
    current_user: CurrentUserDependency
):
    task_entity = TaskEntity(**task_data.model_dump())
    result = await task_service.update_task(task_entity, task_id, current_user.id)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.data
    
@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    task_service: TaskServiceDependency,
    current_user: CurrentUserDependency
):
    result = await task_service.delete_task(task_id, current_user.id)
    if not result.success:
        raise HTTPException(status_code=404, detail=result.error)
    return {"detail": "Tarea eliminada correctamente"}