# AI Optimized by Skills Agent: Minimal health route for skeleton verification and CI smoke tests.
from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


# AI Optimized by Skills Agent: Returns static service metadata without touching external systems.
@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    return HealthResponse(status="ok", service="quick-career-api", version="0.1.0")
