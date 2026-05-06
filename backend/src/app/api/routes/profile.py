"""AI Optimized by Skills Agent: Routes for saving and reusing candidate career profiles."""
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.profile import CandidateProfileRequest, CandidateProfileResponse
from app.services.profile_store import CandidateProfileNotFoundError, candidate_profile_service

router = APIRouter(prefix="/profile", tags=["profile"])
profile_service = candidate_profile_service


# AI Optimized by Skills Agent: Saves personal info, education, certificates, skills and experience.
@router.post("/", response_model=CandidateProfileResponse, status_code=status.HTTP_201_CREATED)
async def save_profile(request: CandidateProfileRequest) -> CandidateProfileResponse:
    return profile_service.save(request)


# AI Optimized by Skills Agent: Retrieves the latest saved profile for the frontend workspace.
@router.get("/latest", response_model=CandidateProfileResponse | None)
async def get_latest_profile() -> CandidateProfileResponse | None:
    return profile_service.latest()


# AI Optimized by Skills Agent: Retrieves a specific saved candidate profile by id.
@router.get("/{profile_id}", response_model=CandidateProfileResponse)
async def get_profile(profile_id: UUID) -> CandidateProfileResponse:
    try:
        return profile_service.get(profile_id)
    except CandidateProfileNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
