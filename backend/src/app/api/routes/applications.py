"""AI Optimized by Skills Agent: Routes for automatic application submission."""
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.application import ApplicationSubmissionRequest, ApplicationSubmissionSummary
from app.services.application_submission import (
    ApplicationSubmissionError,
    ApplicationSubmissionService,
)

router = APIRouter(prefix="/applications", tags=["applications"])
submission_service = ApplicationSubmissionService()


# AI Optimized by Skills Agent: Keeps module health visible for skeleton and smoke checks.
@router.get("/")
async def applications_route_status() -> dict[str, str]:
    return {"module": "applications", "status": "ready"}


# AI Optimized by Skills Agent: Submits a complete optimized package through the configured adapter.
@router.post("/submit", response_model=ApplicationSubmissionSummary, status_code=status.HTTP_201_CREATED)
async def submit_application(request: ApplicationSubmissionRequest) -> ApplicationSubmissionSummary:
    try:
        return submission_service.submit(request)
    except ApplicationSubmissionError as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc


# AI Optimized by Skills Agent: Returns submission receipt and status for frontend traceability.
@router.get("/{submission_id}", response_model=ApplicationSubmissionSummary)
async def get_application_submission(submission_id: UUID) -> ApplicationSubmissionSummary:
    submission = submission_service.get(submission_id)
    if submission is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Submission was not found.")
    return submission
