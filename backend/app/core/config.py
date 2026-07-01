from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    VERSION: str
    API_PREFIX: str

    ENVIRONMENT: str

    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    OPENAI_API_KEY: str = ""

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.DATABASE_USER}:"
            f"{self.DATABASE_PASSWORD}@"
            f"{self.DATABASE_HOST}:"
            f"{self.DATABASE_PORT}/"
            f"{self.DATABASE_NAME}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


settings = Settings()