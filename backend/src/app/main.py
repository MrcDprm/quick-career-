# AI Optimized by Skills Agent: FastAPI application factory aligned with Quick-Career architecture.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.health import router as health_router
from app.core.config import settings


# AI Optimized by Skills Agent: Keeps app creation testable and ready for future route modules.
def create_app() -> FastAPI:
    app = FastAPI(
        title="Quick-Career API",
        version="0.1.0",
        description="Autonomous job analysis, CV optimization and application workflow API.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router, prefix="/api")
    return app


# AI Optimized by Skills Agent: ASGI entrypoint used by Uvicorn.
app = create_app()
