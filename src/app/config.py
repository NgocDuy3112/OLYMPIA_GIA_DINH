from pydantic_settings import BaseSettings, SettingsConfigDict


DOTENV_PATH = '/src/configs/.env'



class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=DOTENV_PATH)
    BASE_URL: str
    DATABASE_URL: str
    VALKEY_CACHE_URL: str
    VALKEY_PUBSUB_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int



settings = Settings()