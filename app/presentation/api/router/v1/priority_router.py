from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.domain.entities.priority_entity import PriorityEntity
from app.presentation.schemas.priority_schema import PriorityCreateRequest, PriorityResponse, PriorityUpdateRequest
from app.presentation.api.dependencies.priority_dependencies import PriorityServiceDependency
from app.presentation.api.dependencies.auth_dependencies import CurrentUserDependency, require_role
from app.presentation.api.responses import handle_result
from app.core.error_list import ErrorCode

router = APIRouter(prefix="/priorities", tags=["priorities"])

@router.get("", response_model=List[PriorityResponse])
async def get_all_priorities(
    priority_service: PriorityServiceDependency,
    current_user: CurrentUserDependency
):
    result = await priority_service.get_all()
    priorities = handle_result(result)
    return [PriorityResponse(**p.__dict__) for p in priorities]

@router.post("", response_model=PriorityResponse, status_code=201, dependencies=[Depends(require_role(["admin"]))])
async def create_priority(
    priority_data: PriorityCreateRequest,
    priority_service: PriorityServiceDependency,
    current_user: CurrentUserDependency
):
    priority_entity = PriorityEntity(**priority_data.model_dump())
    result = await priority_service.create(priority_entity, current_user.id)
    priority = handle_result(result)
    return PriorityResponse(**priority.__dict__)

@router.put("/{priority_id}", response_model=PriorityResponse, dependencies=[Depends(require_role(["admin"]))])
async def update_priority(
    priority_id: int,
    priority_data: PriorityUpdateRequest,
    priority_service: PriorityServiceDependency,
    current_user: CurrentUserDependency
):
    priority_entity = PriorityEntity(**priority_data.model_dump())
    result = await priority_service.update(priority_id, priority_entity, current_user.id)
    priority = handle_result(result)
    return PriorityResponse(**priority.__dict__)

@router.delete("/{priority_id}", status_code=204, dependencies=[Depends(require_role(["admin"]))])
async def delete_priority(
    priority_id: int,
    priority_service: PriorityServiceDependency
):
    result = await priority_service.delete(priority_id)

    if not result.success and result.code == ErrorCode.RESOURCE_IN_USE:
        raise HTTPException(status_code=409, detail=result.error)

    handle_result(result)
    return None