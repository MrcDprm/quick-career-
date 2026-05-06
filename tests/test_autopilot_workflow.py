# AI Optimized by Skills Agent: Tests prove profile-to-LinkedIn-to-ATS-CV-to-application workflow.
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))

from app.api.routes import autopilot as autopilot_route  # noqa: E402
from app.main import create_app  # noqa: E402
from app.services.autopilot import AutopilotApplicationService  # noqa: E402
from app.services.linkedin_scraper import LinkedInJobSearchService  # noqa: E402
from app.services.web_scraper import JobScrapingError  # noqa: E402


class _BlockedLinkedInJobSearchService(LinkedInJobSearchService):
    def _fetch_search_html(self, source_url: str) -> str:
        raise JobScrapingError("blocked")


# AI Optimized by Skills Agent: End-to-end API test uses LinkedIn fallback if public scraping is blocked.
def test_autopilot_apply_creates_ats_applications() -> None:
    autopilot_route.autopilot_service = AutopilotApplicationService(
        linkedin=_BlockedLinkedInJobSearchService()
    )
    client = TestClient(create_app())
    response = client.post(
        "/api/autopilot/apply",
        json={
            "profile": {
                "personal": {
                    "full_name": "Demo Candidate",
                    "email": "candidate@example.com",
                    "links": ["https://linkedin.com/in/demo"],
                },
                "summary": "Full stack developer with FastAPI, React and PostgreSQL experience.",
                "skills": ["FastAPI", "React", "PostgreSQL", "automation"],
                "education": [{"school": "Demo University", "degree": "Computer Engineering"}],
                "certifications": [{"name": "React TypeScript"}],
                "experiences": [
                    {
                        "title": "Software Developer",
                        "company": "Demo Labs",
                        "highlights": ["Built FastAPI services", "Created React dashboards"],
                    }
                ],
                "projects": [{"name": "Quick-Career", "description": "Automated ATS CV generation"}],
                "languages": ["Turkish", "English"],
            },
            "filters": {
                "keywords": ["FastAPI", "React", "PostgreSQL"],
                "location": "Remote",
                "limit": 2,
                "minimum_skill_matches": 1,
            },
            "max_applications": 2,
            "submission_mode": "mock",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["total_applications"] >= 1
    first_application = payload["applications"][0]
    assert "## Core Skills" in first_application["generated_resume"]["content"]
    assert first_application["submission"]["status"] == "submitted"
