from fastapi import APIRouter, HTTPException, Depends
from typing import List

from app.domain.entities.tag_entity import TagEntity
from app.presentation.schemas.tag_schema import TagCreateRequest, TagResponse, TagUpdateRequest
from app.presentation.api.dependencies.tag_dependencies import TagServiceDependency
from app.presentation.api.dependencies.auth_dependencies import CurrentUserDependency, require_role
from app.presentation.api.responses import handle_result
from app.core.error_list import ErrorCode

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("", response_model=List[TagResponse])
async def get_all_tags(
    tag_service: TagServiceDependency,
    current_user: CurrentUserDependency
):
    result = await tag_service.get_all()
    tags = handle_result(result)
    return [TagResponse(**tag.__dict__) for tag in tags]

@router.post("", response_model=TagResponse, status_code=201, dependencies=[Depends(require_role(["admin"]))])
async def create_tag(
    tag_data: TagCreateRequest,
    tag_service: TagServiceDependency,
    current_user: CurrentUserDependency
):
    tag_entity = TagEntity(**tag_data.model_dump())
    result = await tag_service.create(tag_entity, current_user.id)
    tag = handle_result(result)
    return TagResponse(**tag.__dict__)

@router.put("/{tag_id}", response_model=TagResponse, dependencies=[Depends(require_role(["admin"]))])
async def update_tag(
    tag_id: int,
    tag_data: TagUpdateRequest,
    tag_service: TagServiceDependency,
    current_user: CurrentUserDependency
):
    tag_entity = TagEntity(**tag_data.model_dump())
    result = await tag_service.update(tag_id, tag_entity, current_user.id)
    tag = handle_result(result)
    return TagResponse(**tag.__dict__)

@router.delete("/{tag_id}", status_code=204, dependencies=[Depends(require_role(["admin"]))])
async def delete_tag(
    tag_id: int,
    tag_service: TagServiceDependency
):
    result = await tag_service.delete(tag_id)

    if not result.success and result.code == ErrorCode.RESOURCE_IN_USE:
        raise HTTPException(status_code=409, detail=result.error)

    handle_result(result)
    return None