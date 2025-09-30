from fastapi import FastAPI
from app.core.settings import settings
from contextlib import asynccontextmanager
from app.core.exceptions import ExceptionHandler
from app.core.common import init_startup, get_app_name
from app.core.logging_config import setup_logging
from app.presentation.api.router.v1 import user_router, auth_router
from app.core.observability import setup_otel_providers, instrument_app

setup_logging()

if settings.OBSERVABILITY_ENABLED:
    setup_otel_providers()

app = FastAPI(title=get_app_name())

app.include_router(user_router.router)
app.include_router(auth_router.router)
ExceptionHandler.register(app)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_startup()
    yield

if settings.OBSERVABILITY_ENABLED:
    instrument_app(app)