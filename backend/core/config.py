# config.py
from pydantic_settings import BaseSettings

class Config(BaseSettings):
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "mydatabase"
    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DEBUG: bool = True
    FRONTEND_URL: str = "http://localhost:5173"
    TOKEN_TYPE: str = "bearer"

    class Config:
        env_file = ".env"

config = Config()