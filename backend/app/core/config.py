from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "root123456"
    MYSQL_DATABASE: str = "learning_system"

    MILVUS_HOST: str = "localhost"
    MILVUS_PORT: int = 19530

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: int = 0

    JWT_SECRET_KEY: str = "your-secret-key-change-this-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    XFYUN_SPARK_APP_ID: str = ""
    XFYUN_SPARK_API_SECRET: str = ""
    XFYUN_SPARK_API_KEY: str = ""
    XFYUN_SPARK_V4_URL: str = "https://spark-openai.xf-yun.com/v4/chat/completions"

    XFYUN_MULTIMODAL_APP_ID: str = ""
    XFYUN_MULTIMODAL_API_SECRET: str = ""
    XFYUN_MULTIMODAL_API_KEY: str = ""

    XFYUN_CONTENT_AUDIT_APP_ID: str = ""
    XFYUN_CONTENT_AUDIT_API_SECRET: str = ""
    XFYUN_CONTENT_AUDIT_API_KEY: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
