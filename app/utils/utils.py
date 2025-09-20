from data.datasource.database import Database
from datetime import datetime, timezone

async def check_database_status(database: Database, max_wait_seconds: int = 30):
    return await database.check_connection(max_wait_seconds=max_wait_seconds)

async def create_tables_database(is_dev_environment: bool, database: Database) -> bool:
    if not is_dev_environment:
        return False
    await database.create_tables()
    return True

async def get_time_now() -> datetime:
    return datetime.now(timezone.utc)