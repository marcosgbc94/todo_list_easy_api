# tests/conftest.py

import pytest
import pytest_asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.settings import settings
from app.data.datasource.database import database

# Forzar el entorno de pruebas
settings.ENVIRONMENT = "test"

# Motor que apunta al servicio de la base de datos de pruebas
test_engine = create_async_engine(settings.TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)

async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[database.get_session_database] = override_get_session

@pytest_asyncio.fixture(scope="function", autouse=True)
async def manage_tables():
    async with test_engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(database.Base.metadata.drop_all)

# --- ¡ESTA ES LA FIXTURE QUE FALTABA! ---
@pytest_asyncio.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Proporciona una sesión de base de datos limpia para cada prueba.
    """
    async with TestSessionLocal() as session:
        yield session
# ----------------------------------------

@pytest_asyncio.fixture(scope="function")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client