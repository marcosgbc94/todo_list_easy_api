from fastapi import APIRouter, HTTPException
from typing import List
from app.presentation.api.dependencies.auth_dependencies import CurrentUserDependency
from app.domain.entities.task_entity import TaskEntity
from app.presentation.schemas.task_schema import TaskCreateRequest, TaskResponse, TaskUpdateRequest, TaskTagRequest
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

@router.post("/{task_id}/tags", status_code=204)
async def add_tag_to_task(
    task_id: int,
    request: TaskTagRequest,
    task_service: TaskServiceDependency,
    current_user: CurrentUserDependency
):
    result = await task_service.add_tag(task_id, request.tag_id, current_user.id)
    if not result.success:
        raise HTTPException(status_code=404, detail=result.error)
    return {"detail": "Tag agregado correctamente a tarea"}

@router.delete("/{task_id}/tags/{tag_id}", status_code=204)
async def remove_tag_from_task(
    task_id: int,
    tag_id: int,
    task_service: TaskServiceDependency,
    current_user: CurrentUserDependency
):
    result = await task_service.remove_tag(task_id, tag_id, current_user.id)
    if not result.success:
        raise HTTPException(status_code=404, detail=result.error)
    return {"detail": "Tag removido correctamente de tarea"}