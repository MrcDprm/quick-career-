# AI Optimized by Skills Agent: Placeholder service for future Job Analysis Agent orchestration.
from datetime import datetime, timezone
from uuid import UUID, uuid4

from pydantic import BaseModel

from app.schemas.job import JobAnalysisSummary, JobAnalyzeRequest, JobPostResponse
from app.services.ai import AIProvider, get_ai_provider
from app.services.traceability import AITraceabilityService


class JobNotFoundError(LookupError):
    pass


class _StoredJob(BaseModel):
    response: JobPostResponse


class JobAnalysisService:
    def __init__(
        self,
        *,
        provider: AIProvider | None = None,
        traceability: AITraceabilityService | None = None,
    ) -> None:
        self._provider = provider or get_ai_provider()
        self._traceability = traceability or AITraceabilityService()
        self._jobs: dict[UUID, _StoredJob] = {}

    async def analyze(self, request: JobAnalyzeRequest) -> JobPostResponse:
        ai_output = await self._provider.generate_json(
            task="job_analysis",
            system_prompt="Extract structured role, seniority, skills, keywords and responsibilities.",
            user_payload=request.model_dump(),
            schema_name="JobAnalysisSummary",
        )
        analysis = JobAnalysisSummary.model_validate(ai_output)
        trace = self._traceability.record(
            agent_type="job_analysis",
            provider="mock",
            model="mock",
            prompt_version="job-analysis-v1",
            input_text=request.raw_text,
            output_text=analysis.model_dump_json(),
            summary=f"Analyzed job post for {analysis.role}.",
        )
        response = JobPostResponse(
            id=uuid4(),
            source_type=request.source_type,
            source_url=request.source_url,
            raw_text=request.raw_text,
            analysis=analysis,
            trace_id=trace.id,
            created_at=datetime.now(timezone.utc),
        )
        self._jobs[response.id] = _StoredJob(response=response)
        return response

    def get(self, job_id: UUID) -> JobPostResponse:
        stored = self._jobs.get(job_id)
        if stored is None:
            raise JobNotFoundError(f"Job post '{job_id}' was not found.")
        return stored.response
