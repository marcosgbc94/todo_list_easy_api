from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.domain.entities.status_entity import StatusEntity
from app.presentation.schemas.status_schema import StatusCreateRequest, StatusResponse, StatusUpdateRequest
from app.presentation.api.dependencies.status_dependencies import StatusServiceDependency
from app.presentation.api.dependencies.auth_dependencies import CurrentUserDependency, require_role
from app.presentation.api.responses import handle_result
from app.core.error_list import ErrorCode

router = APIRouter(prefix="/status", tags=["status"])

@router.get("", response_model=List[StatusResponse])
async def get_all_status(
    status_service: StatusServiceDependency,
    current_user: CurrentUserDependency
):
    result = await status_service.get_all()
    statuses = handle_result(result)
    return [StatusResponse(**status.__dict__) for status in statuses]

@router.post("", response_model=StatusResponse, status_code=201, dependencies=[Depends(require_role(["admin"]))])
async def create_status(
    status_data: StatusCreateRequest,
    status_service: StatusServiceDependency,
    current_user: CurrentUserDependency
):
    status_entity = StatusEntity(**status_data.model_dump())
    result = await status_service.create(status_entity, current_user.id)
    status = handle_result(result)
    return StatusResponse(**status.__dict__)

@router.put("/{status_id}", response_model=StatusResponse, dependencies=[Depends(require_role(["admin"]))])
async def update_status(
    status_id: int,
    status_data: StatusUpdateRequest,
    status_service: StatusServiceDependency,
    current_user: CurrentUserDependency
):
    status_entity = StatusEntity(**status_data.model_dump())
    result = await status_service.update(status_id, status_entity, current_user.id)
    status = handle_result(result)
    return StatusResponse(**status.__dict__)

@router.delete("/{status_id}", status_code=204, dependencies=[Depends(require_role(["admin"]))])
async def delete_status(
    status_id: int,
    status_service: StatusServiceDependency
):
    result = await status_service.delete(status_id)

    if not result.success and result.code == ErrorCode.RESOURCE_IN_USE:
        raise HTTPException(status_code=409, detail=result.error)

    handle_result(result)
    return None