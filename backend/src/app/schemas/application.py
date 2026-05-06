"""AI Optimized by Skills Agent: Schemas for automatic application submission."""
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


# AI Optimized by Skills Agent: Submission adapter choices keep real platform integrations swappable.
class SubmissionMode(StrEnum):
    MOCK = "mock"
    EMAIL = "email"
    PLATFORM = "platform"


# AI Optimized by Skills Agent: Submission state values are visible in frontend receipt UI.
class SubmissionStatus(StrEnum):
    QUEUED = "queued"
    SUBMITTED = "submitted"
    FAILED = "failed"


# AI Optimized by Skills Agent: Request contains the complete optimized package needed for autonomous sending.
class ApplicationSubmissionRequest(BaseModel):
    optimization_run_id: UUID
    target: str = Field(..., min_length=2)
    candidate_email: str | None = None
    resume_file_name: str = Field(..., min_length=4)
    cover_letter: str = Field(..., min_length=20)
    mode: SubmissionMode = SubmissionMode.MOCK


# AI Optimized by Skills Agent: Receipt contract returned after adapter execution.
class ApplicationSubmissionSummary(BaseModel):
    id: UUID
    optimization_run_id: UUID
    target: str
    status: SubmissionStatus
    mode: SubmissionMode
    receipt: str | None = None
    error_message: str | None = None
