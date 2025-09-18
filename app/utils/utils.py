from data.datasource.database import Database

async def check_database_status(database: Database, max_wait_seconds: int = 30):
    return await database.check_connection(max_wait_seconds=max_wait_seconds)

def create_tables_database(is_dev_environment: bool, database: Database) -> bool:
    if not is_dev_environment:
        return False
    database.create_tables()
    return True