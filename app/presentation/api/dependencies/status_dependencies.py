from typing import Annotated, TypeAlias
from fastapi import Depends
from app.domain.services.status_service import StatusService
from app.presentation.api.dependencies.core_dependencies import DataBaseSessionDependency, StatusRepositoryDependency

def get_status_service(repo: StatusRepositoryDependency, session: DataBaseSessionDependency) -> StatusService:
    return StatusService(status_repository=repo, db_session=session)

StatusServiceDependency: TypeAlias = Annotated[StatusService, Depends(get_status_service)]