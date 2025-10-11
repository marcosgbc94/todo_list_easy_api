from fastapi import APIRouter, HTTPException, Depends 
from typing import List
from app.domain.entities.status_entity import StatusEntity
from app.presentation.schemas.status_schema import StatusCreateRequest, StatusResponse, StatusUpdateRequest
from app.presentation.api.dependencies.status_dependencies import StatusServiceDependency
from app.presentation.api.dependencies.auth_dependencies import CurrentUserDependency, require_role
from app.core.error_list import ErrorCode

router = APIRouter(prefix="/status", tags=["status"])

@router.get("", response_model=List[StatusResponse])
async def get_all_status(status_service: StatusServiceDependency, current_user: CurrentUserDependency):
    result = await status_service.get_all()
    return result.data

@router.post("", response_model=StatusResponse, status_code=201)
async def create_status(
    status_data: StatusCreateRequest,
    status_service: StatusServiceDependency,
    current_user: CurrentUserDependency,
):
    status_entity = StatusEntity(**status_data.model_dump())
    result = await status_service.create(status_entity, current_user.id)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.data

@router.put("/{status_id}", response_model=StatusResponse)
async def update_status(
    status_id: int,
    status_data: StatusUpdateRequest,
    status_service: StatusServiceDependency,
    current_user: CurrentUserDependency,
):
    status_entity = StatusEntity(**status_data.model_dump())
    result = await status_service.update(status_id, status_entity, current_user.id)
    if not result.success:
        if result.code == ErrorCode.STATUS_NOT_FOUND:
            raise HTTPException(status_code=404, detail=result.error)
        raise HTTPException(status_code=400, detail=result.error)
    return result.data

@router.delete("/{status_id}", status_code=204)
async def delete_status(
    status_id: int, status_service: StatusServiceDependency, current_user: CurrentUserDependency, _ = Depends(require_role(["admin"]))
):
    result = await status_service.delete(status_id)
    if not result.success:
        if result.code == ErrorCode.STATUS_NOT_FOUND:
            raise HTTPException(status_code=404, detail=result.error)
        else:
            raise HTTPException(status_code=409, detail=result.error)
    return None