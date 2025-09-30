from app.core.settings import settings
from app.data.datasource.database import database
from app.utils.utils import check_database_status, create_tables_database

async def init_startup() -> bool:
    database_conected = await check_database_status(database=database, max_wait_seconds=settings.MAX_DB_CONNECTION_WAIT)
    if not database_conected:
        raise RuntimeError("No se pudo conectar a la base de datos")
    return await create_tables_database(is_dev_environment=settings.ENVIRONMENT, database=database)

def get_app_name() -> str:
    return settings.API_NAME