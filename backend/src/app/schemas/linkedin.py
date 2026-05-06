"""AI Optimized by Skills Agent: Schemas for LinkedIn/public job discovery and filtering."""
from pydantic import BaseModel, Field


# AI Optimized by Skills Agent: User-controlled filters for LinkedIn-style job discovery.
class LinkedInJobFilters(BaseModel):
    keywords: list[str] = Field(default_factory=list)
    location: str | None = None
    remote_only: bool = False
    experience_level: str | None = None
    limit: int = Field(default=5, ge=1, le=25)
    linkedin_search_url: str | None = None
    minimum_skill_matches: int = Field(default=1, ge=0)


# AI Optimized by Skills Agent: Normalized listing contract used by matching and auto-apply workflow.
class LinkedInJobListing(BaseModel):
    title: str
    company: str
    location: str
    source_url: str
    raw_text: str
    keywords: list[str] = Field(default_factory=list)
    match_score: int = 0
    matched_skills: list[str] = Field(default_factory=list)


# AI Optimized by Skills Agent: Response keeps discovered jobs visible before applications run.
class LinkedInJobSearchResponse(BaseModel):
    source: str
    filters: LinkedInJobFilters
    jobs: list[LinkedInJobListing]
