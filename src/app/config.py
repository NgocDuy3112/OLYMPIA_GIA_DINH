from pydantic_settings import BaseSettings, SettingsConfigDict
import os


DOTENV_PATH = '/src/configs/.env'



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV_PATH)
    BASE_URL: str
    DATABASE_URL: str
    VALKEY_ANSWERS_CACHE_URL: str



settings = Settings()