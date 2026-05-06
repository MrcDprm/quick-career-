# AI Optimized by Skills Agent: Initial resume schema module reserved for parsed candidate profile contracts.
from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class ResumeUploadRequest(BaseModel):
    source_type: Literal["text", "file"] = "text"
    raw_text: str = Field(min_length=20)
    file_name: str | None = None
    owner_name: str | None = None


class ResumeExperience(BaseModel):
    title: str
    company: str
    years: int | None = None
    highlights: list[str] = []


# AI Optimized by Skills Agent: Parsed profile surface used by matching, optimization and submission.
class ResumeProfileSummary(BaseModel):
    owner_name: str | None = None
    summary: str
    experiences: list[ResumeExperience] = []
    education: list[str] = []
    skills: list[str]
    projects: list[str] = []
    languages: list[str] = []
    experience_years: int | None = None


class ResumeProfileResponse(BaseModel):
    id: UUID
    source_type: Literal["text", "file"]
    file_name: str | None = None
    profile: ResumeProfileSummary
    trace_id: UUID
    created_at: datetime
