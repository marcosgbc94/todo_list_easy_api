# datasource/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from core.settings import settings

class Database:
    def __init__(self):
        self.engine = create_engine(settings.DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()
        self.is_connected = False

    def get_session_database(self):
        if not self.is_connected:
            return False
        
        database_session: Session = self.SessionLocal()
        try:
            yield database_session
        finally:
            database_session.close()

    def create_tables(self):
        if not self.is_connected:
            return False
        
        self.Base.metadata.create_all(bind=self.engine) # Crea las tablas en la BD

    async def check_connection(self, max_wait_seconds: int = 30) -> bool:
        import time
        start = time.time()
        while time.time() - start < max_wait_seconds:
            try:
                with self.engine.connect() as conn:
                    self.is_connected = True
                    return True
            except Exception:
                time.sleep(0.5)
        self.is_connected = False
        return False

database = Database()