from typing import Annotated, TypeAlias
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.security import decode_access_token
from app.domain.entities.user_entity import UserEntity
from app.presentation.api.dependencies.user_dependencies import UserServiceDependency

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: UserServiceDependency
) -> UserEntity:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se logró validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None or payload.get("sub") is None:
        raise credentials_exception
    
    user_id = int(payload.get("sub"))
    result = await user_service.get_user_by_id(user_id)

    if not result.success or not result.data:
        raise credentials_exception
        
    return result.data

CurrentUserDependency: TypeAlias = Annotated[UserEntity, Depends(get_current_user)]