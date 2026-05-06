# AI Optimized by Skills Agent: Placeholder route module for job analysis endpoints.
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.job import JobAnalyzeRequest, JobPostResponse
from app.services.job_analysis import JobAnalysisService, JobNotFoundError

router = APIRouter(prefix="/jobs", tags=["jobs"])
job_analysis_service = JobAnalysisService()


@router.get("/")
async def jobs_route_status() -> dict[str, str]:
    return {"module": "jobs", "status": "ready"}


@router.post("/analyze", response_model=JobPostResponse, status_code=status.HTTP_201_CREATED)
async def analyze_job(request: JobAnalyzeRequest) -> JobPostResponse:
    return await job_analysis_service.analyze(request)


@router.get("/{job_id}", response_model=JobPostResponse)
async def get_job(job_id: UUID) -> JobPostResponse:
    try:
        return job_analysis_service.get(job_id)
    except JobNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
