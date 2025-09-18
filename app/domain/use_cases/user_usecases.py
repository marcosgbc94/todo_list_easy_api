from typing import List
from presentation.schemas.user_schema import UserBase
from sqlalchemy.orm import Session
from domain.entities.user_entity import UserEntity
from data.repositories.user_repository import UserRepository
from presentation.schemas.user_schema import UserCreate

class GetUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, session: Session) -> List[UserBase]:
        users_data: List[UserEntity] = self.user_repository.get_users(session)
        return [
            UserBase(
                id=user.id,
                username=user.username, 
                email=user.email
            )
            for user in users_data
        ]
    
class GetUserByIdUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, session: Session, user_id: int):
        user_entity_mapped = self.user_repository.get_user_by_id(session, user_id)
        if not user_entity_mapped:
            raise Exception("Usuario no existe")

        return UserBase(
            id=user_entity_mapped.id,
            username=user_entity_mapped.username,
            email=user_entity_mapped.email
        )
    
class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def execute(self, session: Session, user_data: UserCreate):
        user_entity_mapped = UserEntity(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password
        )
        return self.user_repository.create_user(session, user_entity_mapped)