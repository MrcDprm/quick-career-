# AI Optimized by Skills Agent: Provider tests keep AI calls mockable without external credentials.
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from app.core.config import Settings  # noqa: E402
from app.schemas.job import JobAnalysisSummary  # noqa: E402
from app.schemas.resume import ResumeProfileSummary  # noqa: E402
from app.services.ai import MockAIProvider, UnsupportedAIProviderError, get_ai_provider  # noqa: E402


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


def test_get_ai_provider_returns_mock_provider_for_mock_config() -> None:
    provider = get_ai_provider(Settings(ai_provider="mock"))

    assert isinstance(provider, MockAIProvider)


def test_get_ai_provider_rejects_unsupported_provider() -> None:
    with pytest.raises(UnsupportedAIProviderError, match="Unsupported AI provider"):
        get_ai_provider(Settings(ai_provider="openai"))


@pytest.mark.anyio
async def test_mock_provider_returns_schema_valid_job_analysis() -> None:
    provider = MockAIProvider()

    payload = await provider.generate_json(
        task="job_analysis",
        system_prompt="Extract job requirements.",
        user_payload={"raw_text": "Python FastAPI backend role"},
        schema_name="JobAnalysisSummary",
    )

    analysis = JobAnalysisSummary.model_validate(payload)
    assert analysis.title == "Backend Developer"
    assert "FastAPI" in analysis.required_skills


@pytest.mark.anyio
async def test_mock_provider_returns_schema_valid_resume_profile() -> None:
    provider = MockAIProvider()

    payload = await provider.generate_json(
        task="resume_parsing",
        system_prompt="Extract candidate profile.",
        user_payload={"owner_name": "Erdem"},
        schema_name="ResumeProfileSummary",
    )

    profile = ResumeProfileSummary.model_validate(payload)
    assert profile.owner_name == "Erdem"
    assert "Python" in profile.skills
