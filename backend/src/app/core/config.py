# AI Optimized by Skills Agent: Lightweight settings object avoids extra runtime dependencies in skeleton.
from dataclasses import dataclass
from os import getenv


# AI Optimized by Skills Agent: Parses comma-separated CORS origins for local frontend integration.
def _read_cors_origins() -> list[str]:
    raw_origins = getenv("BACKEND_CORS_ORIGINS", "http://localhost:5173")
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


# AI Optimized by Skills Agent: Centralizes environment-driven backend configuration.
@dataclass(frozen=True)
class Settings:
    database_url: str = getenv(
        "DATABASE_URL",
        "postgresql+psycopg://quick_career:quick_career@localhost:5432/quick_career",
    )
    ai_provider: str = getenv("AI_PROVIDER", "mock")
    export_storage_path: str = getenv("EXPORT_STORAGE_PATH", "./storage/exports")
    application_submission_mode: str = getenv("APPLICATION_SUBMISSION_MODE", "autonomous_mock")
    cors_origins: list[str] = None  # type: ignore[assignment]

    # AI Optimized by Skills Agent: Fills mutable list data safely after dataclass initialization.
    def __post_init__(self) -> None:
        object.__setattr__(self, "cors_origins", _read_cors_origins())


# AI Optimized by Skills Agent: Shared settings instance for route and service modules.
settings = Settings()
