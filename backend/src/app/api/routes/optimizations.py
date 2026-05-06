"""AI Optimized by Skills Agent: Routes for autonomous CV optimization and reviewable diffs."""
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.optimization import (
    OptimizationDiffResponse,
    OptimizationRequest,
    OptimizationRunResponse,
)
from app.services.cv_optimizer import CVOptimizerService, OptimizationNotFoundError

router = APIRouter(prefix="/optimizations", tags=["optimizations"])
optimizer_service = CVOptimizerService()


# AI Optimized by Skills Agent: Keeps module health visible for skeleton and smoke checks.
@router.get("/")
async def optimizations_route_status() -> dict[str, str]:
    return {"module": "optimizations", "status": "ready"}


# AI Optimized by Skills Agent: Starts autonomous optimization and returns a reviewable diff immediately.
@router.post("/", response_model=OptimizationRunResponse, status_code=status.HTTP_201_CREATED)
async def create_optimization(request: OptimizationRequest) -> OptimizationRunResponse:
    return await optimizer_service.optimize(request)


# AI Optimized by Skills Agent: Provides the diff payload needed by the frontend trace/review screen.
@router.get("/{optimization_run_id}/diff", response_model=OptimizationDiffResponse)
async def get_optimization_diff(optimization_run_id: UUID) -> OptimizationDiffResponse:
    try:
        return optimizer_service.get_diff(optimization_run_id)
    except OptimizationNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
