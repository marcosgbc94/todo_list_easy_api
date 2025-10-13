from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.domain.entities.role_entity import RoleEntity
from app.presentation.schemas.role_schema import RoleCreateRequest, RoleResponse, UserRoleRequest
from app.presentation.api.dependencies.role_dependencies import RoleServiceDependency
from app.presentation.api.dependencies.auth_dependencies import CurrentUserDependency, require_role
from app.presentation.api.responses import handle_result
from app.core.error_list import ErrorCode

router = APIRouter(prefix="/roles", tags=["roles"], dependencies=[Depends(require_role(["admin"]))])

@router.get("", response_model=List[RoleResponse])
async def get_all_roles(role_service: RoleServiceDependency):
    result = await role_service.get_all()
    roles = handle_result(result)
    return [RoleResponse(**role.__dict__) for role in roles]

@router.post("", response_model=RoleResponse, status_code=201)
async def create_role(
    role_data: RoleCreateRequest,
    role_service: RoleServiceDependency,
    current_user: CurrentUserDependency
):
    role_entity = RoleEntity(**role_data.model_dump())
    result = await role_service.create(role_entity, current_user.id)
    role = handle_result(result)
    return RoleResponse(**role.__dict__)

@router.delete("/{role_id}", status_code=204)
async def delete_role(role_id: int, role_service: RoleServiceDependency):
    result = await role_service.delete(role_id)

    if not result.success and result.code == ErrorCode.RESOURCE_IN_USE:
        raise HTTPException(status_code=409, detail=result.error)
        
    handle_result(result)
    return None

@router.post("/assign", status_code=204)
async def assign_role_to_user(request: UserRoleRequest, role_service: RoleServiceDependency):
    result = await role_service.assign_to_user(request.user_id, request.role_id)
    handle_result(result)
    return None

@router.post("/revoke", status_code=204)
async def revoke_role_from_user(request: UserRoleRequest, role_service: RoleServiceDependency):
    result = await role_service.revoke_from_user(request.user_id, request.role_id)
    handle_result(result)
    return None