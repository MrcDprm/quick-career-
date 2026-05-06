"""AI Optimized by Skills Agent: API route for the final autonomous Quick-Career scenario."""
from fastapi import APIRouter, HTTPException, status

from app.schemas.autopilot import AutopilotApplyRequest, AutopilotApplyResponse
from app.services.autopilot import AutopilotApplicationService
from app.services.web_scraper import JobScrapingError

router = APIRouter(prefix="/autopilot", tags=["autopilot"])
autopilot_service = AutopilotApplicationService()


# AI Optimized by Skills Agent: Executes profile save, LinkedIn filtering, ATS CV generation and applications.
@router.post("/apply", response_model=AutopilotApplyResponse, status_code=status.HTTP_201_CREATED)
async def run_autopilot_apply(request: AutopilotApplyRequest) -> AutopilotApplyResponse:
    try:
        return await autopilot_service.run(request)
    except JobScrapingError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
