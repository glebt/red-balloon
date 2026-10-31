"""Configuration management using pydantic-settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # API Configuration
    anthropic_base_url: str = "https://api.anthropic.com"
    anthropic_auth_token: str
    anthropic_model: str = "claude-sonnet-4.5"

    # Application Configuration
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    photos_dir: str = "./photos"
    max_upload_size: int = 10 * 1024 * 1024  # 10MB


settings = Settings()
