# AI Optimized by Skills Agent: Placeholder route module for resume upload and parsing endpoints.
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.resume import ResumeProfileResponse, ResumeUploadRequest
from app.services.resume_parser import ResumeNotFoundError, ResumeParserService

router = APIRouter(prefix="/resumes", tags=["resumes"])
resume_parser_service = ResumeParserService()


@router.get("/")
async def resumes_route_status() -> dict[str, str]:
    return {"module": "resumes", "status": "ready"}


@router.post("/upload", response_model=ResumeProfileResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(request: ResumeUploadRequest) -> ResumeProfileResponse:
    return await resume_parser_service.parse(request)


@router.get("/{resume_id}", response_model=ResumeProfileResponse)
async def get_resume(resume_id: UUID) -> ResumeProfileResponse:
    try:
        return resume_parser_service.get(resume_id)
    except ResumeNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
