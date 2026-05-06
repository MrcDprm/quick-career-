# AI Optimized by Skills Agent: Deterministic mock provider supports tests and reliable hackathon demos.
from typing import Any

from app.schemas.application import ApplicationSubmissionSummary
from app.schemas.job import JobAnalysisSummary
from app.schemas.metrics import EfficiencyMetricSummary
from app.schemas.optimization import OptimizationDiffItem
from app.schemas.resume import ResumeProfileSummary
from app.services.ai.base import AIProvider


# AI Optimized by Skills Agent: Schema-mapped payloads keep mock AI safe for endpoint contract tests.
def _schema_payload(schema_name: str, user_payload: dict[str, Any]) -> dict[str, Any]:
    payloads: dict[str, dict[str, Any]] = {
        "JobAnalysisSummary": {
            "title": "Backend Developer",
            "required_skills": ["Python", "FastAPI", "PostgreSQL"],
            "keywords": ["api", "automation", "backend"],
        },
        "ResumeProfileSummary": {
            "owner_name": user_payload.get("owner_name", "Demo Candidate"),
            "skills": ["Python", "React", "SQL"],
            "experience_years": 2,
        },
        "OptimizationDiffItem": {
            "section": "summary",
            "before": "Software developer with general project experience.",
            "after": "Backend developer focused on FastAPI automation and measurable delivery.",
        },
        "ApplicationSubmissionSummary": {
            "target": user_payload.get("target", "Demo Company"),
            "status": "submitted",
            "receipt": "mock-submission-receipt",
        },
        "EfficiencyMetricSummary": {
            "workflow_name": user_payload.get("workflow_name", "golden_path"),
            "manual_steps": 58,
            "automated_steps": 12,
            "reduction_percent": 79.31,
        },
    }
    return payloads.get(
        schema_name,
        {
            "task": user_payload.get("task", "mock_generation"),
            "schema_name": schema_name,
            "provider": "mock",
            "input_keys": sorted(user_payload.keys()),
            "summary": "Mock AI response generated for skeleton verification.",
        },
    )


# AI Optimized by Skills Agent: Simple provider returns predictable schema-valid payloads for demos and tests.
class MockAIProvider(AIProvider):
    async def generate_json(
        self,
        *,
        task: str,
        system_prompt: str,
        user_payload: dict,
        schema_name: str,
    ) -> dict:
        payload = _schema_payload(schema_name, user_payload)

        validators = {
            "JobAnalysisSummary": JobAnalysisSummary,
            "ResumeProfileSummary": ResumeProfileSummary,
            "OptimizationDiffItem": OptimizationDiffItem,
            "ApplicationSubmissionSummary": ApplicationSubmissionSummary,
            "EfficiencyMetricSummary": EfficiencyMetricSummary,
        }
        schema = validators.get(schema_name)
        if schema is None:
            return payload
        return schema.model_validate(payload).model_dump()
