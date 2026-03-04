from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_ENV: str = "local"
    APP_NAME: str = "Inventory API"
    APP_VERSION: str = "0.1.0"

    POSTGRES_DB: str = "inventory"
    POSTGRES_USER: str = "inventory"
    POSTGRES_PASSWORD: str = "inventory"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL_ASYNC(self) -> str:
        # asyncpg driver for async SQLAlchemy
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


settings = Settings()
