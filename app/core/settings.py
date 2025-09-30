from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Configuración General
    API_NAME: str
    ENVIRONMENT: str
    API_SECRET_KEY: str
    MAX_DB_CONNECTION_WAIT: int
    OBSERVABILITY_ENABLED: bool = True
    API_PORT: int

    # --- Configuración de JWT ---
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Base de Datos de Desarrollo
    DB: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str

    TEST_DB_USER: str
    TEST_DB_PASSWORD: str
    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_NAME: str

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def TEST_DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{self.TEST_DB_USER}:{self.TEST_DB_PASSWORD}@{self.TEST_DB_HOST}:{self.TEST_DB_PORT}/{self.TEST_DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()