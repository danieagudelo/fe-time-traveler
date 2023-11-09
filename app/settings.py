import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    ROOT_PATH = "" if os.getenv("MACHINE") == "DEV" else "/time-traveler"

    # CORS Settings
    ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS")
    ALLOW_CREDENTIALS = os.getenv("ALLOW_CREDENTIALS")
    ALLOW_METHODS = os.getenv("ALLOW_METHODS")
    ALLOW_HEADERS = os.getenv("ALLOW_HEADERS")

    # postgres
    CONNECTION_NAME = os.getenv("POSTGRES_CONNECTION_NAME")
    DB_SOCKET_DIR = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    DB_NAME = os.getenv("POSTGRES_DB")
    USERNAME = os.getenv("POSTGRES_USER")
    PASSWORD = os.getenv("POSTGRES_PASS")
    DB_PORT = os.getenv("DB_PORT")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")

    # google
    GOOGLE_SECRET = os.getenv("GOOGLE_SECRET")
