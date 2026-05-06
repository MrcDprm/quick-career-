"""AI Optimized by Skills Agent: Job post schemas for text and URL-based analysis."""
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


# AI Optimized by Skills Agent: Validates pasted job text before it enters AI orchestration.
class JobAnalyzeRequest(BaseModel):
    source_type: Literal["text", "url"] = "text"
    raw_text: str = ""
    source_url: str | None = None

    # AI Optimized by Skills Agent: Allows URL scraping while keeping short text submissions invalid.
    @model_validator(mode="after")
    def require_text_or_url(self) -> "JobAnalyzeRequest":
        if self.source_type == "url":
            if not self.source_url:
                raise ValueError("source_url is required when source_type is url.")
            return self

        if len(self.raw_text.strip()) < 20:
            raise ValueError("raw_text must contain at least 20 characters.")
        return self


# AI Optimized by Skills Agent: Structured contract shared by job analysis, match scoring and frontend reports.
class JobAnalysisSummary(BaseModel):
    title: str
    role: str
    seniority: str
    required_skills: list[str]
    preferred_skills: list[str] = []
    keywords: list[str]
    responsibilities: list[str] = []
    red_flags: list[str] = []


class JobPostResponse(BaseModel):
    id: UUID
    source_type: Literal["text", "url"]
    source_url: str | None = None
    raw_text: str
    analysis: JobAnalysisSummary
    trace_id: UUID
    created_at: datetime
