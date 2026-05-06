# AI Optimized by Skills Agent: Initial job schema module reserved for JobPost and JobAnalysis contracts.
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


# AI Optimized by Skills Agent: Validates pasted job text before it enters AI orchestration.
class JobAnalyzeRequest(BaseModel):
    source_type: Literal["text", "url"] = "text"
    raw_text: str = Field(min_length=20)
    source_url: str | None = None


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
