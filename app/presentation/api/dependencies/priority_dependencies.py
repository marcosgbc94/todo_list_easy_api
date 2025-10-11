from typing import Annotated, TypeAlias
from fastapi import Depends
from app.domain.services.priority_service import PriorityService
from app.presentation.api.dependencies.core_dependencies import DataBaseSessionDependency, PriorityRepositoryDependency

def get_priority_service(repo: PriorityRepositoryDependency, session: DataBaseSessionDependency) -> PriorityService:
    return PriorityService(priority_repository=repo, db_session=session)

PriorityServiceDependency: TypeAlias = Annotated[PriorityService, Depends(get_priority_service)]