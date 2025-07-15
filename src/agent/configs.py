from dotenv import load_dotenv
import os


load_dotenv(dotenv_path="/src/configs/.env",verbose=True, override=True)


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
BASE_URL = os.getenv("BASE_URL")
REQUEST_TIMEOUT_SECONDS = os.getenv("REQUEST_TIMEOUT_SECONDS")
RATE_LIMIT_URI = os.getenv("RATE_LIMIT_URI")