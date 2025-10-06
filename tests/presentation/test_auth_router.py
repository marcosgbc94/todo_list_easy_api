import pytest
from httpx import AsyncClient
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import hash_password
from app.data.models.user_model import UserModel

# Crear un usuario de prueba
@pytest.fixture(scope="function")
async def test_user(db_session: AsyncSession):
    user = UserModel(
        username="testuser",
        email="test@example.com",
        password_hash=hash_password("password123"),
        created_at=datetime.now(timezone.utc),
        created_by=1
    )
    db_session.add(user)
    await db_session.commit()
    return user

# Login con el usuario creado
@pytest.mark.asyncio
async def test_login_success(async_client: AsyncClient, test_user: UserModel):
    response = await async_client.post(
        "/auth/token",
        data={"username": "testuser", "password": "password123"}
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"