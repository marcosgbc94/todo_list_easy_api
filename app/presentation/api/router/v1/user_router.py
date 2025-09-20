from typing import List
from domain.use_cases.user_use_cases.create_user_use_case import CreateUserUseCase
from domain.use_cases.user_use_cases.update_user_by_id_use_case import UpdateUserByIdUseCase
from domain.entities.user_entity import UserEntity
from domain.use_cases.user_use_cases.get_users_use_case import GetUsersUseCase
from domain.use_cases.user_use_cases.get_user_by_id_use_case import GetUserByIdUseCase
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from presentation.schemas.user_schema import UserCreateRequest, UserCreateResponse, UserResponse, UserUpdateRequest, UserUpdateResponse
from data.datasource.database import database
from data.repositories.user_repository import UserRepository

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserResponse])
async def get_users(database_session: Session = Depends(database.get_session_database)):
    # Obtener datos en formato UserModel (Model)
    users = await GetUsersUseCase(UserRepository).execute(session=database_session)

    # Comprobar errores
    if not users:
        raise HTTPException(status_code=404, detail="Ningún usuario registrado")
    
    # Retornar en formato UserResponse (Schema)
    return [
        UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            created_at=user.created_at,
            created_by=user.created_by,
            updated_at=user.updated_at,
            updated_by=user.updated_by
        )
        for user in users
    ]

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, database_session: Session = Depends(database.get_session_database)):
    # Obtener datos en formato UserModel (Model)
    user = await GetUserByIdUseCase(UserRepository).execute(session=database_session, user_id=user_id)

    # Comprobar errores
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no existe")
    
    # Retornar en formato UserResponse (Schema)
    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
        created_by=user.created_by,
        updated_at=user.updated_at,
        updated_by=user.updated_by
    )

@router.post("", response_model=UserCreateResponse)
async def create_user(user_data: UserCreateRequest, database_session: Session = Depends(database.get_session_database)):
    # Mapeo de Schema a Entidad
    user_entity_mapped = UserEntity(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )

    # Obtener datos en formato UserModel (Model)
    user = await CreateUserUseCase(UserRepository).execute(database_session, user_entity_mapped)

    # Comprobar errores
    if not user:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
   
    return UserCreateResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
        created_by=user.created_by
    )

@router.put("/{user_id}", response_model=UserUpdateResponse)
async def update_user_by_id(user_id: int, user_update: UserUpdateRequest, database_session: Session = Depends(database.get_session_database)):
    # Convierte los datos nuevos a entidad
    user_entity_mapper = UserEntity(
        id=user_id,
        username=user_update.username,
        email=user_update.email,
        password=user_update.password
    )

    # Actualiza y obtiene los datos en formato UserModel (Model)
    user = await UpdateUserByIdUseCase(UserRepository).execute(session=database_session, user_data=user_entity_mapper)

    # Comprobar errores
    if not user:
        raise HTTPException(status_code=400, detail="No se pudo actualizar el usuario")
    
    return UserUpdateResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        updated_at=user.updated_at,
        updated_by=user.updated_by
    )