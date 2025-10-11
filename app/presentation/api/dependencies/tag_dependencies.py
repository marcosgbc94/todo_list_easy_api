from typing import Annotated, TypeAlias
from fastapi import Depends
from app.domain.services.tag_service import TagService
from app.presentation.api.dependencies.core_dependencies import DataBaseSessionDependency, TagRepositoryDependency

def get_tag_service(repo: TagRepositoryDependency, session: DataBaseSessionDependency) -> TagService:
    return TagService(tag_repository=repo, db_session=session)

TagServiceDependency: TypeAlias = Annotated[TagService, Depends(get_tag_service)]