from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "sqlite:///./todo_app.db"  # Default to SQLite for development

    # JWT settings
    jwt_secret_key: str = "your-super-secret-jwt-key-here-make-it-long-and-random"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 10080  # 7 days

    # Better Auth settings (for compatibility with frontend)
    better_auth_secret: str = "your-better-auth-secret-key-here"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # Debug Mode
    debug: bool = False

    # Logging level
    log_level: str = "info"

    # OpenAI API Key
    openai_api_key: Optional[str] = None

    class Config:
        env_file = ".env"


settings = Settings()