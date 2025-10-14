from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.data.datasource.database import database
from app.core.settings import settings
from app.core.exceptions import ExceptionHandler
from app.core.common import init_startup, get_app_name
from app.core.logging_config import setup_logging
from app.presentation.api.router.v1 import user_router, auth_router, task_router, status_router, priority_router, tag_router, role_router
from app.core.observability import setup_otel_providers, instrument_app
from app.data.datasource.seed import seed_initial_data

setup_logging()

if settings.OBSERVABILITY_ENABLED:
    setup_otel_providers()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_startup()

    async with database.SessionLocal() as session:
        await seed_initial_data(session)

    yield

app = FastAPI(title=get_app_name(), lifespan=lifespan)

app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(task_router.router)
app.include_router(status_router.router)
app.include_router(priority_router.router)
app.include_router(tag_router.router)
app.include_router(role_router.router)

ExceptionHandler.register(app)

if settings.OBSERVABILITY_ENABLED:
    instrument_app(app)