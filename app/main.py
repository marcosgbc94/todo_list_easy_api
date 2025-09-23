from fastapi import FastAPI
from core.exceptions import ExceptionHandler
from core.common import init_startup, get_app_name
from presentation.api.router.v1 import user_router, auth_router 
from prometheus_fastapi_instrumentator import Instrumentator
from core.logging_config import setup_logging

setup_logging()

# Nombre de la API
app = FastAPI(title=get_app_name())

Instrumentator().instrument(app).expose(app)

# Se incluyen los routers
app.include_router(user_router.router)
app.include_router(auth_router.router)

# Registrar los manejadores de errores
ExceptionHandler.register(app)

# Define acciones realizable cuando se ejecute la API por primera vez
@app.on_event("startup")
async def startup_event(): 
    await init_startup()