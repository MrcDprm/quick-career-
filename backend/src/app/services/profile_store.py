"""AI Optimized by Skills Agent: In-memory candidate profile storage for the hackathon MVP."""
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.schemas.profile import CandidateProfileRequest, CandidateProfileResponse


# AI Optimized by Skills Agent: Raised when a requested candidate profile does not exist.
class CandidateProfileNotFoundError(Exception):
    pass


# AI Optimized by Skills Agent: Stores one or more candidate profiles until PostgreSQL persistence is added.
class CandidateProfileService:
    def __init__(self) -> None:
        self._profiles: dict[UUID, CandidateProfileResponse] = {}
        self._latest_profile_id: UUID | None = None

    # AI Optimized by Skills Agent: Saves the complete personal data surface used by ATS generation.
    def save(self, request: CandidateProfileRequest) -> CandidateProfileResponse:
        now = datetime.now(timezone.utc)
        profile = CandidateProfileResponse(
            id=uuid4(),
            created_at=now,
            updated_at=now,
            **request.model_dump(),
        )
        self._profiles[profile.id] = profile
        self._latest_profile_id = profile.id
        return profile

    # AI Optimized by Skills Agent: Reads a stored profile for later autonomous application workflows.
    def get(self, profile_id: UUID) -> CandidateProfileResponse:
        profile = self._profiles.get(profile_id)
        if profile is None:
            raise CandidateProfileNotFoundError(f"Candidate profile {profile_id} was not found.")
        return profile

    # AI Optimized by Skills Agent: Gives the UI a quick way to reload the last saved profile.
    def latest(self) -> CandidateProfileResponse | None:
        if self._latest_profile_id is None:
            return None
        return self._profiles[self._latest_profile_id]

    # AI Optimized by Skills Agent: Converts structured profile data into optimizer-ready CV text.
    def to_resume_text(self, profile: CandidateProfileRequest | CandidateProfileResponse) -> str:
        sections = [
            profile.personal.full_name,
            profile.summary,
            "Skills: " + ", ".join(profile.skills),
            "Education: "
            + "; ".join(
                f"{entry.degree} {entry.field or ''} at {entry.school}".strip()
                for entry in profile.education
            ),
            "Certifications: "
            + "; ".join(
                f"{entry.name} {f'({entry.issuer})' if entry.issuer else ''}".strip()
                for entry in profile.certifications
            ),
            "Experience: "
            + "; ".join(
                f"{entry.title} at {entry.company}: {', '.join(entry.highlights)}"
                for entry in profile.experiences
            ),
            "Projects: "
            + "; ".join(
                f"{entry.name}: {entry.description} using {', '.join(entry.technologies)}"
                for entry in profile.projects
            ),
            "Languages: " + ", ".join(profile.languages),
        ]
        return "\n".join(section for section in sections if section.strip())

    # AI Optimized by Skills Agent: Briefing summarizes all profile data for application-note generation.
    def to_candidate_brief(self, profile: CandidateProfileRequest | CandidateProfileResponse) -> str:
        return (
            f"{profile.personal.full_name} profile summary: {profile.summary}. "
            f"Skills: {', '.join(profile.skills)}. "
            f"Certifications: {', '.join(cert.name for cert in profile.certifications)}. "
            f"Education: {', '.join(entry.school for entry in profile.education)}."
        )


# AI Optimized by Skills Agent: Shared singleton keeps saved profile state consistent across route modules.
candidate_profile_service = CandidateProfileService()
