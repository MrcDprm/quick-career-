"""AI Optimized by Skills Agent: Candidate profile schemas for saved personal career data."""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


# AI Optimized by Skills Agent: Contact details are stored separately from career evidence for clean CV rendering.
class PersonalInfo(BaseModel):
    full_name: str = Field(..., min_length=2)
    email: str | None = None
    phone: str | None = None
    location: str | None = None
    links: list[str] = Field(default_factory=list)


# AI Optimized by Skills Agent: Education records feed the ATS-friendly CV education section.
class EducationEntry(BaseModel):
    school: str
    degree: str
    field: str | None = None
    start_year: int | None = None
    end_year: int | None = None


# AI Optimized by Skills Agent: Experience records provide role evidence for tailored bullets.
class ExperienceEntry(BaseModel):
    title: str
    company: str
    start_year: int | None = None
    end_year: int | None = None
    highlights: list[str] = Field(default_factory=list)


# AI Optimized by Skills Agent: Certifications make ATS keyword coverage explicit.
class CertificationEntry(BaseModel):
    name: str
    issuer: str | None = None
    year: int | None = None


# AI Optimized by Skills Agent: Project evidence helps when professional experience is thin.
class ProjectEntry(BaseModel):
    name: str
    description: str
    technologies: list[str] = Field(default_factory=list)


# AI Optimized by Skills Agent: Complete saved profile used by scraping, matching, CV and application automation.
class CandidateProfileRequest(BaseModel):
    personal: PersonalInfo
    summary: str = Field(..., min_length=20)
    skills: list[str] = Field(default_factory=list)
    education: list[EducationEntry] = Field(default_factory=list)
    certifications: list[CertificationEntry] = Field(default_factory=list)
    experiences: list[ExperienceEntry] = Field(default_factory=list)
    projects: list[ProjectEntry] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)


# AI Optimized by Skills Agent: Stored profile response gives the frontend a stable profile id.
class CandidateProfileResponse(CandidateProfileRequest):
    id: UUID
    created_at: datetime
    updated_at: datetime
