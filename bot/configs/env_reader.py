import os
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

# Проверка загрузки переменных окружения
print("Loading .env file from:", os.path.abspath(".env"))

# Создаём объект настроек
env_config = Settings()

# Выводим значения переменных окружения
print("BOT_TOKEN:", env_config.BOT_TOKEN.get_secret_value())
print("DB_HOST:", env_config.DB_HOST)
print("DB_NAME:", env_config.DB_NAME)
print("DB_USER:", env_config.DB_USER)
print("DB_USER_PASS:", env_config.DB_USER_PASS.get_secret_value())
print("DB_PORT:", env_config.DB_PORT)