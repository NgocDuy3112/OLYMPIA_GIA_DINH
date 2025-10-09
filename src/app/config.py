from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


load_dotenv('/src/configs/.env', override=True)



class Settings(BaseSettings):
    BASE_URL: str = os.getenv("BASE_URL")
    DATABASE_URL: str = os.getenv("DATABASE_URL")


settings = Settings()