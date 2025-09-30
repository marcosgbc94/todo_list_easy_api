from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import settings
import asyncio

class Database:
    def __init__(self):
        # Usamos create_async_engine con asyncpg (Postgres) o el driver que corresponda
        db_url = self.get_db_url()
        self.engine = create_async_engine(db_url, echo=True)
        self.SessionLocal = sessionmaker(
            bind=self.engine,
            class_=AsyncSession, # Para sesiones asíncronas
            expire_on_commit=False
        )
        self.Base = declarative_base()
        self.is_connected = False

    # Determina que URL de base de datos usar, producción o testing
    def get_db_url(self) -> str:
        return settings.DATABASE_URL

    # Dependencia para FastAPI
    async def get_session_database(self):
        async with self.SessionLocal() as session:
            yield session  # yield para usar con Depends en FastAPI

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(self.Base.metadata.create_all)

    async def check_connection(self, max_wait_seconds: int = 30) -> bool:
        start = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start < max_wait_seconds:
            try:
                async with self.engine.connect() as conn:
                    self.is_connected = True
                    return True
            except Exception:
                await asyncio.sleep(0.5)
        self.is_connected = False
        return False


database = Database()