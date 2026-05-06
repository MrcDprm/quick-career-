# AI Optimized by Skills Agent: Placeholder service for future CV parsing and profile extraction.
from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.schemas.resume import ResumeProfileResponse, ResumeProfileSummary, ResumeUploadRequest
from app.services.ai import AIProvider, get_ai_provider
from app.services.traceability import AITraceabilityService


class ResumeNotFoundError(LookupError):
    pass


class _StoredResume(BaseModel):
    raw_text: str
    response: ResumeProfileResponse


class ResumeParserService:
    def __init__(
        self,
        *,
        provider: AIProvider | None = None,
        traceability: AITraceabilityService | None = None,
    ) -> None:
        self._provider = provider or get_ai_provider()
        self._traceability = traceability or AITraceabilityService()
        self._resumes: dict[UUID, _StoredResume] = {}

    async def parse(self, request: ResumeUploadRequest) -> ResumeProfileResponse:
        ai_output = await self._provider.generate_json(
            task="resume_parsing",
            system_prompt="Extract structured resume profile fields for matching and optimization.",
            user_payload=request.model_dump(),
            schema_name="ResumeProfileSummary",
        )
        profile = ResumeProfileSummary.model_validate(ai_output)
        trace = self._traceability.record(
            agent_type="resume_parsing",
            provider="mock",
            model="mock",
            prompt_version="resume-parsing-v1",
            input_text=request.raw_text,
            output_text=profile.model_dump_json(),
            summary=f"Parsed resume profile for {profile.owner_name or 'candidate'}.",
        )
        response = ResumeProfileResponse(
            id=uuid4(),
            source_type=request.source_type,
            file_name=request.file_name,
            profile=profile,
            trace_id=trace.id,
            created_at=datetime.now(timezone.utc),
        )
        self._resumes[response.id] = _StoredResume(raw_text=request.raw_text, response=response)
        return response

    def get(self, resume_id: UUID) -> ResumeProfileResponse:
        stored = self._resumes.get(resume_id)
        if stored is None:
            raise ResumeNotFoundError(f"Resume profile '{resume_id}' was not found.")
        return stored.response
