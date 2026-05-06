# AI Optimized by Skills Agent: Initial resume schema module reserved for parsed candidate profile contracts.
from pydantic import BaseModel


# AI Optimized by Skills Agent: Minimal placeholder represents the parsed CV profile surface.
class ResumeProfileSummary(BaseModel):
    owner_name: str | None = None
    skills: list[str]
    experience_years: int | None = None
