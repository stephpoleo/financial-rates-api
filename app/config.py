"""
Configuración de la aplicación con Pydantic Settings.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración de la aplicación."""

    # Base de datos
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/financial_rates"

    # API Keys
    BANXICO_API_KEY: str = ""
    ALPHA_VANTAGE_API_KEY: str = ""

    # Aplicación
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "INFO"

    # Scheduler
    ENABLE_SCHEDULER: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    """Obtiene la configuración cacheada."""
    return Settings()


# Instancia global para acceso directo
settings = get_settings()
