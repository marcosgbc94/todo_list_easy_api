from fastapi import status
from fastapi import HTTPException
from .error_list import ErrorCode

ERROR_MAP = {
    ErrorCode.USER_NOT_FOUND: HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado."
    ),
    ErrorCode.USERS_NOT_FOUND: HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="No se encontraron usuarios."
    ),
    ErrorCode.USER_ALREADY_EXISTS: HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="El nombre de usuario o el correo electrónico ya existen."
    ),
    ErrorCode.USER_BAD_CREDENTIALS: HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales incorrectas."
    ),
    ErrorCode.FORBIDDEN: HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="No tienes permisos para realizar esta acción."
    ),
    ErrorCode.PARAMS_NOT_FOUND: HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Faltan parámetros en la petición."
    ),
    ErrorCode.STATUS_NOT_FOUND: HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Estado no encontrado."
    ),
    ErrorCode.PRIORITY_NOT_FOUND: HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Prioridad no encontrada."
    ),
    ErrorCode.TAG_NOT_FOUND: HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Etiqueta no encontrada."
    ),
    ErrorCode.ROLE_NOT_FOUND: HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Rol no encontrado."
    ),
    ErrorCode.RESOURCE_IN_USE: HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail="El recurso no se puede eliminar porque está en uso."
    ),
    ErrorCode.INTERNAL_ERROR: HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Error interno del servidor."
    ),
}