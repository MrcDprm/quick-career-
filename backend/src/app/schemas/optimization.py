"""AI Optimized by Skills Agent: Schemas for autonomous CV optimization and reviewable diffs."""
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, Field


# AI Optimized by Skills Agent: Status values support the autonomous optimization lifecycle.
class OptimizationStatus(StrEnum):
    DRAFT = "draft"
    OPTIMIZING = "optimizing"
    FINALIZED = "finalized"
    EXPORTED = "exported"
    SUBMITTED = "submitted"
    FAILED = "failed"


# AI Optimized by Skills Agent: Request starts optimization against an analyzed job context.
class OptimizationRequest(BaseModel):
    job_post_id: UUID | None = None
    target_role: str = Field(..., min_length=2)
    resume_text: str = Field(..., min_length=40)
    job_keywords: list[str] = Field(default_factory=list)
    candidate_brief: str = Field(
        default="",
        description="General candidate information used to tailor the ATS resume and application note.",
    )
    candidate_name: str = "Quick-Career Candidate"


# AI Optimized by Skills Agent: Captures autonomous before/after changes for trace UI.
class OptimizationDiffItem(BaseModel):
    section: str
    before: str
    after: str
    reason: str


# AI Optimized by Skills Agent: Response exposes status and scoring for the optimization run.
class OptimizationRunResponse(BaseModel):
    id: UUID
    status: OptimizationStatus
    target_role: str
    match_score_before: int
    match_score_after: int
    diff: list[OptimizationDiffItem]
    highlighted_skills: list[str] = []
    ats_resume_markdown: str = ""
    application_brief: str = ""


# AI Optimized by Skills Agent: Dedicated diff response keeps review UI payloads focused.
class OptimizationDiffResponse(BaseModel):
    optimization_run_id: UUID
    status: OptimizationStatus
    diff: list[OptimizationDiffItem]
