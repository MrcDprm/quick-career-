# AI Optimized by Skills Agent: Health response schema keeps smoke tests typed and stable.
from pydantic import BaseModel


# AI Optimized by Skills Agent: Minimal response model for `GET /api/health`.
class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
