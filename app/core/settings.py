from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_NAME: str
    ENVIRONMENT: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    API_SECRET_KEY: str
    MAX_DB_CONNECTION_WAIT: int

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"

settings = Settings()