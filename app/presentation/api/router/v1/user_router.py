from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from presentation.schemas.user_schema import UserCreate, UserBase
from data.datasource.database import database
from data.repositories.user_repository import UserRepository
from domain.use_cases.user_usecases import GetUsersUseCase, GetUserByIdUseCase, CreateUserUseCase

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", response_model=List[UserBase])
def get_users(database_session: Session = Depends(database.get_session_database)):
    user_usecase = GetUsersUseCase(UserRepository).execute(database_session)
    if not user_usecase:
        raise HTTPException(status_code=404, detail="Ningún usuario registrado")
    return user_usecase

@router.get("/{user_id}", response_model=UserBase)
def get_user_by_id(user_id: int, database_session: Session = Depends(database.get_session_database)):
    user_usecase = GetUserByIdUseCase(UserRepository).execute(database_session, user_id)
    if not user_usecase:
        raise HTTPException(status_code=404, detail="Usuario no existe")
    return user_usecase

@router.post("", response_model=UserBase)
def create_user(user_data: UserCreate, database_session: Session = Depends(database.get_session_database)):
    user_usecase = CreateUserUseCase(UserRepository).execute(database_session, user_data)
    if not user_usecase:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
    return user_usecase
