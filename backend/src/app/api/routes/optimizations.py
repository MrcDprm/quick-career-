"""AI Optimized by Skills Agent: Routes for autonomous CV optimization and reviewable diffs."""
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.optimization import (
    OptimizationDiffResponse,
    OptimizationRequest,
    OptimizationRunResponse,
)
from app.schemas.export import ExportRequest, GeneratedResumeResponse
from app.services.cv_optimizer import CVOptimizerService, OptimizationNotFoundError
from app.services.document_export import DocumentExportError, DocumentExportService

router = APIRouter(prefix="/optimizations", tags=["optimizations"])
optimizer_service = CVOptimizerService()
document_export_service = DocumentExportService()


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


# AI Optimized by Skills Agent: Exports a final optimized CV artifact without waiting for manual approval.
@router.post("/{optimization_run_id}/export", response_model=GeneratedResumeResponse)
async def export_optimization(
    optimization_run_id: UUID,
    request: ExportRequest,
) -> GeneratedResumeResponse:
    if request.optimization_run_id != optimization_run_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Path optimization id must match request optimization id.",
        )

    try:
        return document_export_service.export(request)
    except DocumentExportError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
