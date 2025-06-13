import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Settings:
    PROJECT_NAME: str = "E-commerce Backend"
    PROJECT_VERSION: str = "1.0"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    EMAIL_USER: str = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD: str = os.getenv("EMAIL_PASSWORD")

settings = Settings()
