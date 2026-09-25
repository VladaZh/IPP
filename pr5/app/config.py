from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    DB: PostgresDsn
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = Config()
