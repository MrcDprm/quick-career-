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

FAKE_LINKEDIN_SEARCH_HTML = """
<li>
  <div class="base-card job-search-card" data-entity-urn="urn:li:jobPosting:67890">
    <a href="https://www.linkedin.com/jobs/view/67890"></a>
    <h3 class="base-search-card__title">FastAPI React Developer</h3>
    <h4 class="base-search-card__subtitle">Gerçek LinkedIn Şirketi</h4>
    <span class="job-search-card__location">Remote</span>
  </div>
</li>
"""

FAKE_LINKEDIN_DETAIL_HTML = """
<section>
  FastAPI, React, PostgreSQL ve automation deneyimi isteyen gerçek Easy Apply ilan açıklaması.
  Application Process: Easy Apply on LinkedIn.
</section>
"""


class _FakeLinkedInJobSearchService(LinkedInJobSearchService):
    # AI Optimized by Skills Agent: Keeps autopilot tests on the real parser path without live LinkedIn calls.
    def _fetch_search_html(self, source_url: str) -> str:
        return FAKE_LINKEDIN_SEARCH_HTML

    # AI Optimized by Skills Agent: Supplies Easy Apply detail text for ATS keyword targeting.
    def _fetch_job_detail_html(self, job_id: str) -> str:
        return FAKE_LINKEDIN_DETAIL_HTML


# AI Optimized by Skills Agent: End-to-end API test uses real-card parsing and ATS generation.
def test_autopilot_apply_creates_ats_applications() -> None:
    autopilot_route.autopilot_service = AutopilotApplicationService(
        linkedin=_FakeLinkedInJobSearchService()
    )
    client = TestClient(create_app())
    response = client.post(
        "/api/autopilot/apply",
        json={
            "profile": {
                "personal": {
                    "full_name": "Demo Aday",
                    "email": "candidate@example.com",
                    "links": ["https://linkedin.com/in/demo"],
                },
                "summary": "FastAPI, React ve PostgreSQL deneyimine sahip full stack geliştirici.",
                "skills": ["FastAPI", "React", "PostgreSQL", "automation"],
                "education": [{"school": "Demo Üniversitesi", "degree": "Bilgisayar Mühendisliği"}],
                "certifications": [{"name": "React TypeScript"}],
                "experiences": [
                    {
                        "title": "Yazılım Geliştirici",
                        "company": "Demo Labs",
                        "highlights": ["Built FastAPI services", "Created React dashboards"],
                    }
                ],
                "projects": [{"name": "Quick-Career", "description": "Otomatik ATS CV üretimi"}],
                "languages": ["Türkçe", "İngilizce"],
            },
            "filters": {
                "keywords": ["FastAPI", "React", "PostgreSQL"],
                "location": "Remote",
                "limit": 2,
                "minimum_skill_matches": 1,
                "easy_apply_only": True,
            },
            "max_applications": 2,
            "submission_mode": "mock",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["total_applications"] >= 1
    first_application = payload["applications"][0]
    assert "## Temel Yetenekler" in first_application["generated_resume"]["content"]
    assert first_application["submission"]["status"] == "submitted"
