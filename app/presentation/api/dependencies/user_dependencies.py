from typing import Annotated, TypeAlias
from fastapi import Depends
from data.repositories.user_repository import UserRepository
from domain.services.user_service import UserService
from presentation.api.dependencies.core_dependencies import DataBaseSessionDependency, UserRepositoryDependency

# Provedor de servicio
def get_user_service(repository: UserRepositoryDependency, session: DataBaseSessionDependency) -> UserService:
    return UserService(user_repository=repository, database_session=session)

UserServiceDependency: TypeAlias = Annotated[UserService, Depends(get_user_service)]