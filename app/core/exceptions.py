# core/exception_handler.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

class ExceptionHandler:
    @staticmethod
    def register(app: FastAPI):
        @app.exception_handler(Exception)
        async def global_exception_handler(request: Request, exc: Exception):
            detail = str(exc) if not hasattr(exc, "detail") else exc.detail
            return JSONResponse(
                status_code=500,
                content={"detail": detail}
            )

        @app.exception_handler(SQLAlchemyError)
        async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
            return JSONResponse(
                status_code=400,
                content={"detail": "Error en la base de datos: " + str(exc)}
            )
