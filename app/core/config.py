import os
from dotenv import load_dotenv
from typing import List

# Load environment variables from .env file
load_dotenv()


class Settings:
    """
    Configuration settings for the Expense Tracker API.
    Loads values from environment variables with sensible defaults.
    """

    # Project
    PROJECT_NAME: str = "Expense Tracker API"
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "change_me_in_env")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", 7))

    # Server
    SERVER_HOST: str = os.getenv("SERVER_HOST", "http://localhost:8000")
    BACKEND_CORS_ORIGINS: List[str] = os.getenv("BACKEND_CORS_ORIGINS", "*").split(",")

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./expense_tracker.db" )


# Instantiate a single settings object to be used throughout the app
settings = Settings()
