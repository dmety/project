from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )
    
    VITE_API_BASE_URL: Optional[str] = None
    
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000

    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "248650"
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
    XFYUN_SPARK_V4_URL: str = "https://spark-api-open.xf-yun.com/v1/chat/completions"

    XFYUN_MULTIMODAL_APP_ID: str = ""
    XFYUN_MULTIMODAL_API_SECRET: str = ""
    XFYUN_MULTIMODAL_API_KEY: str = ""

    XFYUN_CONTENT_AUDIT_APP_ID: str = ""
    XFYUN_CONTENT_AUDIT_API_SECRET: str = ""
    XFYUN_CONTENT_AUDIT_API_KEY: str = ""

    XFYUN_IFLYCODE_APP_ID: str = ""
    XFYUN_IFLYCODE_API_SECRET: str = ""
    XFYUN_IFLYCODE_API_KEY: str = ""


settings = Settings()

# 打印配置（调试用）
print("="*50)
print("讯飞星火配置:")
print(f"APP_ID: {settings.XFYUN_SPARK_APP_ID}")
print(f"API_KEY: {settings.XFYUN_SPARK_API_KEY[:10] if settings.XFYUN_SPARK_API_KEY else ''}...")
print(f"API_URL: {settings.XFYUN_SPARK_V4_URL}")
print("="*50)
