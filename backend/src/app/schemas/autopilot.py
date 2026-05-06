"""AI Optimized by Skills Agent: Schemas for the full profile-to-application autopilot workflow."""
from pydantic import BaseModel, Field

from app.schemas.application import ApplicationSubmissionSummary, SubmissionMode
from app.schemas.export import GeneratedResumeResponse
from app.schemas.linkedin import LinkedInJobFilters, LinkedInJobListing, LinkedInJobSearchResponse
from app.schemas.optimization import OptimizationRunResponse
from app.schemas.profile import CandidateProfileRequest, CandidateProfileResponse


# AI Optimized by Skills Agent: Request stores profile data and runs filtered LinkedIn applications in sequence.
class AutopilotApplyRequest(BaseModel):
    profile: CandidateProfileRequest
    filters: LinkedInJobFilters = Field(default_factory=LinkedInJobFilters)
    max_applications: int = Field(default=3, ge=1, le=10)
    submission_mode: SubmissionMode = SubmissionMode.MOCK


# AI Optimized by Skills Agent: One result per job keeps the ordered application trail inspectable.
class AutopilotApplicationResult(BaseModel):
    job: LinkedInJobListing
    optimization: OptimizationRunResponse
    generated_resume: GeneratedResumeResponse
    submission: ApplicationSubmissionSummary


# AI Optimized by Skills Agent: Full workflow response proves that profile, scraping, CV and apply stages completed.
class AutopilotApplyResponse(BaseModel):
    profile: CandidateProfileResponse
    search: LinkedInJobSearchResponse
    applications: list[AutopilotApplicationResult]
    total_applications: int
    summary: str
