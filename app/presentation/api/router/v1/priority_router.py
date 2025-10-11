from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.domain.entities.priority_entity import PriorityEntity
from app.presentation.schemas.priority_schema import PriorityCreateRequest, PriorityResponse, PriorityUpdateRequest
from app.presentation.api.dependencies.priority_dependencies import PriorityServiceDependency
from app.presentation.api.dependencies.auth_dependencies import CurrentUserDependency, require_role
from app.core.error_list import ErrorCode

router = APIRouter(prefix="/priorities", tags=["priorities"])

@router.get("", response_model=List[PriorityResponse])
async def get_all_priorities(
    priority_service: PriorityServiceDependency, 
    current_user: CurrentUserDependency
):
    result = await priority_service.get_all()
    return result.data

@router.post("", response_model=PriorityResponse, status_code=201)
async def create_priority(
    priority_data: PriorityCreateRequest,
    priority_service: PriorityServiceDependency,
    current_user: CurrentUserDependency,
    _ = Depends(require_role(["admin"]))
):
    priority_entity = PriorityEntity(**priority_data.model_dump())
    result = await priority_service.create(priority_entity, current_user.id)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.data

@router.put("/{priority_id}", response_model=PriorityResponse)
async def update_priority(
    priority_id: int,
    priority_data: PriorityUpdateRequest,
    priority_service: PriorityServiceDependency,
    current_user: CurrentUserDependency,
    _ = Depends(require_role(["admin"]))
):
    priority_entity = PriorityEntity(**priority_data.model_dump())
    result = await priority_service.update(priority_id, priority_entity, current_user.id)
    if not result.success:
        if result.code == ErrorCode.PRIORITY_NOT_FOUND:
            raise HTTPException(status_code=404, detail=result.error)
        raise HTTPException(status_code=400, detail=result.error)
    return result.data

@router.delete("/{priority_id}", status_code=204)
async def delete_priority(
    priority_id: int, 
    priority_service: PriorityServiceDependency, 
    current_user: CurrentUserDependency,
    _ = Depends(require_role(["admin"]))
):
    result = await priority_service.delete(priority_id)
    if not result.success:
        if result.code == ErrorCode.PRIORITY_NOT_FOUND:
            raise HTTPException(status_code=404, detail=result.error)
        else:
            raise HTTPException(status_code=409, detail=result.error)
    return None