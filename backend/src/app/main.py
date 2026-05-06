# AI Optimized by Skills Agent: FastAPI application factory aligned with Quick-Career architecture.
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes.applications import router as applications_router
from app.api.routes.health import router as health_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.metrics import router as metrics_router
from app.api.routes.optimizations import router as optimizations_router
from app.api.routes.resumes import router as resumes_router
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
    app.include_router(jobs_router, prefix="/api")
    app.include_router(resumes_router, prefix="/api")
    app.include_router(optimizations_router, prefix="/api")
    app.include_router(applications_router, prefix="/api")
    app.include_router(metrics_router, prefix="/api")
    return app


# AI Optimized by Skills Agent: ASGI entrypoint used by Uvicorn.
app = create_app()
