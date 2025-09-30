from typing import Annotated, TypeAlias
from fastapi import Depends
from app.domain.services.user_service import UserService
from app.presentation.api.dependencies.core_dependencies import DataBaseSessionDependency, UserRepositoryDependency

# Provedor de servicio
def get_user_service(repository: UserRepositoryDependency, session: DataBaseSessionDependency) -> UserService:
    return UserService(user_repository=repository, database_session=session)

UserServiceDependency: TypeAlias = Annotated[UserService, Depends(get_user_service)]