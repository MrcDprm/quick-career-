# AI Optimized by Skills Agent: Placeholder route module for resume upload and parsing endpoints.
from fastapi import APIRouter

router = APIRouter(prefix="/resumes", tags=["resumes"])


@router.get("/")
async def resumes_route_status() -> dict[str, str]:
    return {"module": "resumes", "status": "ready"}
