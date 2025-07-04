from dotenv import load_dotenv
import os


load_dotenv(dotenv_path="/src/configs/.env.assistant",verbose=True, override=True)


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")