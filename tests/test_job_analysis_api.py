# AI Optimized by Skills Agent: Job analysis API tests define the contract consumed by match and UI work.
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from app.main import create_app  # noqa: E402
from app.schemas.job import JobAnalyzeRequest  # noqa: E402
from app.services.job_analysis import JobAnalysisService  # noqa: E402


class _FakeScraper:
    def scrape(self, source_url: str) -> str:
        return (
            "Senior Backend Developer role requiring Python, FastAPI, PostgreSQL, "
            "API ownership and workflow automation."
        )


def test_analyze_job_returns_structured_analysis_and_trace_id() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/jobs/analyze",
        json={
            "source_type": "text",
            "raw_text": "We need a Python FastAPI backend developer for API automation work.",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["analysis"]["role"] == "Backend Developer"
    assert "FastAPI" in payload["analysis"]["required_skills"]
    assert payload["trace_id"]
    assert payload["raw_text"].startswith("We need")


def test_get_job_returns_previously_analyzed_job() -> None:
    client = TestClient(create_app())
    created = client.post(
        "/api/jobs/analyze",
        json={
            "source_type": "text",
            "raw_text": "Backend role for Python services and PostgreSQL integration.",
        },
    ).json()

    response = client.get(f"/api/jobs/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_analyze_job_rejects_empty_or_too_short_input() -> None:
    client = TestClient(create_app())

    response = client.post("/api/jobs/analyze", json={"raw_text": "too short"})

    assert response.status_code == 422


def test_analyze_job_can_scrape_url_source_with_fake_scraper() -> None:
    service = JobAnalysisService(scraper=_FakeScraper())

    response = TestClient(create_app())
    assert response

    created = service.analyze(
        JobAnalyzeRequest(source_type="url", source_url="https://example.com/job")
    )

    import asyncio

    payload = asyncio.run(created)
    assert payload.source_type == "url"
    assert "FastAPI" in payload.raw_text


def test_get_job_returns_404_for_unknown_id() -> None:
    client = TestClient(create_app())

    response = client.get("/api/jobs/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
