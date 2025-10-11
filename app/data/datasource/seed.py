import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.data.models import StatusModel, PriorityModel, RoleModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def seed_initial_data(db_session: AsyncSession):
    """
    Siembra la base de datos con datos iniciales si las tablas están vacías.
    """
    # --- 1. Verificar si los datos ya existen ---
    result = await db_session.execute(select(StatusModel))
    if result.scalars().first() is not None:
        logger.info("Los datos iniciales ya existen. Omitiendo la siembra.")
        return

    logger.info("Base de datos vacía. Sembrando datos iniciales...")

    # --- 2. Definir los datos por defecto ---
    default_statuses = [
        StatusModel(name="Pendiente", color="#CCCCCC"),
        StatusModel(name="En Progreso", color="#007BFF"),
        StatusModel(name="Completada", color="#28A745"),
    ]

    default_priorities = [
        PriorityModel(name="Baja", color="#28A745"),
        PriorityModel(name="Normal", color="#FFC107"),
        PriorityModel(name="Alta", color="#DC3545"),
    ]

    default_roles = [
        RoleModel(name="admin", description="Administrador con todos los permisos."),
        RoleModel(name="user", description="Usuario estándar con permisos limitados."),
    ]

    # --- 3. Añadir los datos a la sesión y guardarlos ---
    try:
        db_session.add_all(default_statuses)
        db_session.add_all(default_priorities)
        db_session.add_all(default_roles)
        await db_session.commit()
        logger.info("¡Siembra de datos completada exitosamente! ✅")
    except Exception as e:
        logger.error(f"Error durante la siembra de datos: {e}")
        await db_session.rollback()