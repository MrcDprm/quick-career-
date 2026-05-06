"""AI Optimized by Skills Agent: API route for the final autonomous Quick-Career scenario."""
from fastapi import APIRouter, status

from app.schemas.autopilot import AutopilotApplyRequest, AutopilotApplyResponse
from app.services.autopilot import AutopilotApplicationService

router = APIRouter(prefix="/autopilot", tags=["autopilot"])
autopilot_service = AutopilotApplicationService()


# AI Optimized by Skills Agent: Executes profile save, LinkedIn filtering, ATS CV generation and applications.
@router.post("/apply", response_model=AutopilotApplyResponse, status_code=status.HTTP_201_CREATED)
async def run_autopilot_apply(request: AutopilotApplyRequest) -> AutopilotApplyResponse:
    return await autopilot_service.run(request)
