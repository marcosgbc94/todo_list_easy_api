from typing import List
from app.core.error_list import ErrorCode
from app.domain.entities.user_entity import UserEntity
from fastapi import APIRouter, HTTPException
from app.presentation.schemas.user_schema import UserCreateRequest, UserCreateResponse, UserResponse, UserUpdateRequest, UserUpdateResponse
from app.presentation.api.dependencies.user_dependencies import UserServiceDependency
from app.presentation.api.dependencies.auth_dependencies import CurrentUserDependency


router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserResponse])
async def get_users(
    user_service: UserServiceDependency, 
    current_user: CurrentUserDependency
):
    result = await user_service.get_all_users()

    # Comprobar errores
    if not result.success:
        if result.code == ErrorCode.USERS_NOT_FOUND:
            raise HTTPException(status_code=404, detail=result.error)
        else:
            raise HTTPException(status_code=500, detail="Error interno")
    
    users = result.data
    
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
async def get_user_by_id(
    user_id: int, 
    user_service: UserServiceDependency,
    current_user: CurrentUserDependency
):
    result = await user_service.get_user_by_id(user_id=user_id)

    # Comprobar errores

    if not result.success:
        if result.code == ErrorCode.USER_NOT_FOUND:
            raise HTTPException(status_code=404, detail=result.error)
        else:
            raise HTTPException(status_code=500, detail="Error interno")
    
    user = result.data

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

@router.get("/username/{username}", response_model=UserResponse)
async def get_user_by_username(
    username: str, 
    user_service: UserServiceDependency,
    current_user: CurrentUserDependency
):
    result = await user_service.get_user_by_username(username=username)

    # Comprobar errores
    if not result.success:
        if result.code == ErrorCode.USER_NOT_FOUND:
            raise HTTPException(status_code=404, detail=result.error)
        else:
            raise HTTPException(status_code=500, detail="Error interno")
    
    user = result.data

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
async def create_user(
    user_data: UserCreateRequest, 
    user_service: UserServiceDependency,
    current_user: CurrentUserDependency
):
    # Mapeo de Schema a Entidad
    user_entity_mapped = UserEntity(
        username=user_data.username,
        email=user_data.email,
        password=user_data.password
    )

    # Obtener datos en formato UserModel (Model)
    result = await user_service.create_new_user(user_data=user_entity_mapped, performed_by_id=current_user.id)

    # Comprobar errores
    if not result.success:
        if result.code in (ErrorCode.USER_ALREADY_EXISTS, ErrorCode.PARAMS_NOT_FOUND):
            raise HTTPException(status_code=400, detail=result.error)
        else:
            raise HTTPException(status_code=500, detail="Error interno")
        
    user = result.data
   
    return UserCreateResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        created_at=user.created_at,
        created_by=user.created_by
    )

@router.put("/{user_id}", response_model=UserUpdateResponse)
async def update_user_by_id(
    user_id: int, 
    user_update: UserUpdateRequest, 
    user_service: UserServiceDependency,
    current_user: CurrentUserDependency
):
    # Convierte los datos nuevos a entidad
    user_entity_mapper = UserEntity(
        id=user_id,
        username=user_update.username,
        email=user_update.email,
        password=user_update.password
    )

    # Actualiza y obtiene los datos en formato UserModel (Model)
    result = await user_service.update_existing_user(user_id=user_id, user_data=user_entity_mapper, performed_by_id=current_user.id)

    # Comprobar errores
    if not result.success:
        if result.code in (ErrorCode.USER_ALREADY_EXISTS, ErrorCode.PARAMS_NOT_FOUND):
            raise HTTPException(status_code=400, detail=result.error)
        else:
            raise HTTPException(status_code=500, detail="Error interno")
        
    user = result.data
    
    return UserUpdateResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        updated_at=user.updated_at,
        updated_by=user.updated_by
    )

@router.delete("/{user_id}")
async def delete_user(
    user_id: int, 
    user_service: UserServiceDependency,
    current_user: CurrentUserDependency
):
    result = await user_service.delete_user_by_id(user_id=user_id)
    
    if not result.success:
        if result.code == ErrorCode.USER_NOT_FOUND:
            raise HTTPException(status_code=404, detail=result.error)
        else:
            raise HTTPException(status_code=500, detail="Error interno")
    
    return {"detail": "Usuario eliminado correctamente"}
