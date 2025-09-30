from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.core.security import create_access_token
from app.presentation.api.dependencies.user_dependencies import UserServiceDependency
from app.presentation.schemas.user_auth_schema import UserAuthResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/token", response_model=UserAuthResponse)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    user_service: UserServiceDependency
):
    result = await user_service.authenticate_user(
        username=form_data.username, 
        password=form_data.password
    )
    
    user = result.data

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": str(user.id)})

    return UserAuthResponse(
        access_token=access_token, 
        token_type="bearer"
    )