from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_USER_PASS: SecretStr
    DB_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Создаём объект настроек
env_config = Settings()