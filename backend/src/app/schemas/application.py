# AI Optimized by Skills Agent: Initial application schema module for automatic submission contracts.
from pydantic import BaseModel


# AI Optimized by Skills Agent: Minimal submission receipt contract for adapter outputs.
class ApplicationSubmissionSummary(BaseModel):
    target: str
    status: str
    receipt: str | None = None
