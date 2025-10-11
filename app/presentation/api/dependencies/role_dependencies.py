from typing import Annotated, TypeAlias
from fastapi import Depends
from app.domain.services.role_service import RoleService
from app.presentation.api.dependencies.core_dependencies import DataBaseSessionDependency, RoleRepositoryDependency

def get_role_service(repo: RoleRepositoryDependency, session: DataBaseSessionDependency) -> RoleService:
    return RoleService(role_repository=repo, db_session=session)

RoleServiceDependency: TypeAlias = Annotated[RoleService, Depends(get_role_service)]