from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.core.security import create_access_token
from app.presentation.api.dependencies.user_dependencies import UserServiceDependency
from app.presentation.schemas.user_auth_schema import UserAuthResponse
from app.presentation.api.responses import handle_result

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
  
    user = handle_result(result)
    
    access_token = create_access_token(data={"sub": str(user.id)})

    return UserAuthResponse(
        access_token=access_token, 
        token_type="bearer"
    )