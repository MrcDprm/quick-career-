"""AI Optimized by Skills Agent: Automatic application submission service for QC-010."""
from uuid import UUID, uuid4

from app.schemas.application import (
    ApplicationSubmissionRequest,
    ApplicationSubmissionSummary,
    SubmissionMode,
    SubmissionStatus,
)


# AI Optimized by Skills Agent: Raised when the autonomous package is missing required send data.
class ApplicationSubmissionError(Exception):
    pass


# AI Optimized by Skills Agent: Service submits complete optimized packages through MVP adapters.
class ApplicationSubmissionService:
    def __init__(self) -> None:
        self._submissions: dict[UUID, ApplicationSubmissionSummary] = {}

    # AI Optimized by Skills Agent: Runs without a manual approval gate once package completeness is validated.
    def submit(self, request: ApplicationSubmissionRequest) -> ApplicationSubmissionSummary:
        self._validate_package(request)
        submission_id = uuid4()
        receipt = self._create_receipt(submission_id, request)
        submission = ApplicationSubmissionSummary(
            id=submission_id,
            optimization_run_id=request.optimization_run_id,
            target=request.target,
            status=SubmissionStatus.SUBMITTED,
            mode=request.mode,
            receipt=receipt,
        )
        self._submissions[submission_id] = submission
        return submission

    # AI Optimized by Skills Agent: Fetches submission receipts for UI and traceability.
    def get(self, submission_id: UUID) -> ApplicationSubmissionSummary | None:
        return self._submissions.get(submission_id)

    # AI Optimized by Skills Agent: Guards automation quality without adding a manual consent checkpoint.
    def _validate_package(self, request: ApplicationSubmissionRequest) -> None:
        if not request.resume_file_name.strip():
            raise ApplicationSubmissionError("Resume file name is required for submission.")
        if not request.cover_letter.strip():
            raise ApplicationSubmissionError("Cover letter is required for submission.")
        if request.mode == SubmissionMode.EMAIL and not request.candidate_email:
            raise ApplicationSubmissionError("Candidate email is required for email submission mode.")

    # AI Optimized by Skills Agent: Deterministic receipt supports tests and hackathon demo reliability.
    def _create_receipt(self, submission_id: UUID, request: ApplicationSubmissionRequest) -> str:
        return (
            f"QC-SUB-{str(submission_id)[:8]} submitted to {request.target} "
            f"via {request.mode.value} adapter."
        )
