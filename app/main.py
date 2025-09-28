from fastapi import FastAPI
from core.settings import settings
from core.exceptions import ExceptionHandler
from core.common import init_startup, get_app_name
from core.logging_config import setup_logging
from presentation.api.router.v1 import user_router, auth_router
from core.observability import setup_otel_providers, instrument_app

setup_logging()

if settings.OBSERVABILITY_ENABLED:
    setup_otel_providers()

app = FastAPI(title=get_app_name())

app.include_router(user_router.router)
app.include_router(auth_router.router)
ExceptionHandler.register(app)

@app.on_event("startup")
async def startup_event(): 
    await init_startup()

if settings.OBSERVABILITY_ENABLED:
    instrument_app(app)