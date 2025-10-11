from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.domain.entities.role_entity import RoleEntity
from app.presentation.schemas.role_schema import RoleCreateRequest, RoleResponse, UserRoleRequest
from app.presentation.api.dependencies.role_dependencies import RoleServiceDependency
from app.presentation.api.dependencies.auth_dependencies import CurrentUserDependency, require_role # <-- Importamos ambas
from app.core.error_list import ErrorCode

router = APIRouter(prefix="/roles", tags=["roles"], dependencies=[Depends(require_role(["admin"]))])

@router.get("", response_model=List[RoleResponse])
async def get_all_roles(role_service: RoleServiceDependency):
    result = await role_service.get_all()
    return result.data

@router.post("", response_model=RoleResponse, status_code=201)
async def create_role(
    role_data: RoleCreateRequest,
    role_service: RoleServiceDependency,
    current_user: CurrentUserDependency
):
    role_entity = RoleEntity(**role_data.model_dump())

    result = await role_service.create(role_entity, current_user.id)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.data

@router.delete("/{role_id}", status_code=204)
async def delete_role(role_id: int, role_service: RoleServiceDependency):
    result = await role_service.delete(role_id)
    if not result.success:
        if result.code == ErrorCode.ROLE_NOT_FOUND:
            raise HTTPException(status_code=404, detail=result.error)
        else:
            raise HTTPException(status_code=409, detail=result.error)
    return None

@router.post("/assign", status_code=204)
async def assign_role_to_user(request: UserRoleRequest, role_service: RoleServiceDependency):
    result = await role_service.assign_to_user(request.user_id, request.role_id)
    if not result.success:
        if result.code in [ErrorCode.USER_NOT_FOUND, ErrorCode.ROLE_NOT_FOUND]:
             raise HTTPException(status_code=404, detail=result.error)
        else:
             raise HTTPException(status_code=400, detail=result.error)
    return None

@router.post("/revoke", status_code=204)
async def revoke_role_from_user(request: UserRoleRequest, role_service: RoleServiceDependency):
    result = await role_service.revoke_from_user(request.user_id, request.role_id)
    if not result.success:
        raise HTTPException(status_code=404, detail=result.error)
    return None