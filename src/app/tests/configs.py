from dotenv import load_dotenv
import os


load_dotenv(dotenv_path="/src/configs/.env", verbose=True, override=True)


URL = os.environ.get("URL")