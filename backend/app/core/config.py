from functools import cached_property
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "IncidentPilot"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "postgresql+psycopg://incidentpilot:incidentpilot@localhost:5432/incidentpilot"
    redis_url: str = "redis://localhost:6379/0"
    qwen_api_key: str = ""
    qwen_base_url: str = "https://dashscope-intl.aliyuncs.com/compatible-mode/v1"
    qwen_model: str = "qwen-plus"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    demo_mode: bool = True

    @cached_property
    def cors_origins_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

settings = Settings()
