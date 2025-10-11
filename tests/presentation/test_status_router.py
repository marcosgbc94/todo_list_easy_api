import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.data.models.user_model import UserModel
from app.data.models.role_model import RoleModel
from app.data.models.user_role_model import UserRoleModel
from app.core.security import hash_password

# --- Fixtures de Ayuda ---

@pytest.fixture
async def admin_user(db_session: AsyncSession):
    """Crea un usuario y un rol 'admin', y se lo asigna."""
    # Crear rol
    admin_role = RoleModel(name="admin", description="Administrador del sistema")
    db_session.add(admin_role)
    await db_session.flush()

    # Crear usuario
    user = UserModel(
        username="testadmin",
        email="admin@example.com",
        password_hash=hash_password("adminpass")
    )
    db_session.add(user)
    await db_session.flush()

    # Asignar rol
    user_role = UserRoleModel(user_id=user.id, role_id=admin_role.id)
    db_session.add(user_role)
    await db_session.commit()

    await db_session.refresh(user)
    return user

@pytest.fixture
async def admin_auth_headers(async_client: AsyncClient, admin_user: UserModel):
    """Obtiene un token de autenticación para el usuario admin."""
    response = await async_client.post(
        "/auth/token",
        data={"username": "testadmin", "password": "adminpass"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- Pruebas del Router ---

@pytest.mark.asyncio
async def test_create_status_success(async_client: AsyncClient, admin_auth_headers: dict):
    """Prueba la creación exitosa de un estado."""
    response = await async_client.post(
        "/status",
        json={"name": "Nuevo Estado", "color": "#FF0000"},
        headers=admin_auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Nuevo Estado"
    assert data["id"] is not None

@pytest.mark.asyncio
async def test_get_all_status(async_client: AsyncClient, admin_auth_headers: dict):
    """Prueba obtener todos los estados."""
    # Primero creamos uno para asegurarnos de que la lista no esté vacía
    await async_client.post("/status", json={"name": "Estado 1"}, headers=admin_auth_headers)

    response = await async_client.get("/status", headers=admin_auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["name"] == "Estado 1"

@pytest.mark.asyncio
async def test_update_status(async_client: AsyncClient, admin_auth_headers: dict):
    """Prueba actualizar un estado existente."""
    # Crear estado
    create_response = await async_client.post("/status", json={"name": "Original"}, headers=admin_auth_headers)
    status_id = create_response.json()["id"]

    # Actualizar
    update_response = await async_client.put(
        f"/status/{status_id}",
        json={"name": "Actualizado", "color": "#00FF00"},
        headers=admin_auth_headers
    )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Actualizado"

@pytest.mark.asyncio
async def test_delete_status(async_client: AsyncClient, admin_auth_headers: dict):
    """Prueba eliminar un estado."""
    # Crear estado
    create_response = await async_client.post("/status", json={"name": "Para Borrar"}, headers=admin_auth_headers)
    status_id = create_response.json()["id"]

    # Eliminar
    delete_response = await async_client.delete(f"/status/{status_id}", headers=admin_auth_headers)
    assert delete_response.status_code == 204

    # Verificar que ya no existe (esto debería dar 404)
    # Necesitamos una forma de obtener un estado por ID para verificar,
    # pero por ahora confiamos en el 204.

@pytest.mark.asyncio
async def test_delete_status_forbidden_for_non_admin(async_client: AsyncClient, db_session: AsyncSession):
    """Prueba que un usuario sin rol de admin no puede eliminar."""
    # Crear un usuario normal
    normal_user = UserModel(username="normaluser", email="user@example.com", password_hash=hash_password("userpass"))
    db_session.add(normal_user)
    await db_session.commit()

    # Obtener su token
    login_res = await async_client.post("/auth/token", data={"username": "normaluser", "password": "userpass"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Intentar eliminar (asumiendo que el status con ID 1 existe o no)
    response = await async_client.delete("/status/1", headers=headers)
    assert response.status_code == 403 # Forbidden