"""AI Optimized by Skills Agent: Schemas for autonomous resume export outputs."""
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel


# AI Optimized by Skills Agent: Supported MVP export formats for generated resumes.
class ExportFormat(StrEnum):
    MARKDOWN = "markdown"
    PDF = "pdf"
    DOCX = "docx"


# AI Optimized by Skills Agent: Request for creating an export from a finalized optimization result.
class ExportRequest(BaseModel):
    optimization_run_id: UUID
    format: ExportFormat = ExportFormat.MARKDOWN
    candidate_name: str = "Quick-Career Candidate"
    target_role: str
    optimized_summary: str
    optimized_skills: list[str]


# AI Optimized by Skills Agent: Generated resume payload returned by the export service.
class GeneratedResumeResponse(BaseModel):
    optimization_run_id: UUID
    format: ExportFormat
    file_name: str
    content: str
    is_final: bool = True
