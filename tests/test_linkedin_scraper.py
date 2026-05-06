# AI Optimized by Skills Agent: Tests cover LinkedIn filtering without live network dependency.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))

from app.schemas.linkedin import LinkedInJobFilters  # noqa: E402
from app.services.linkedin_scraper import LinkedInJobSearchService  # noqa: E402
from app.services.web_scraper import JobScrapingError  # noqa: E402


class _BlockedLinkedInJobSearchService(LinkedInJobSearchService):
    def _fetch_search_html(self, source_url: str) -> str:
        raise JobScrapingError("blocked")


# AI Optimized by Skills Agent: Fallback jobs are filtered and scored against saved profile skills.
def test_linkedin_search_fallback_filters_by_profile_skills() -> None:
    service = _BlockedLinkedInJobSearchService()

    response = service.search(
        LinkedInJobFilters(keywords=["FastAPI", "React"], location="Remote", limit=2),
        profile_skills=["FastAPI", "React", "PostgreSQL"],
    )

    assert response.source.startswith("https://www.linkedin.com/jobs/search/")
    assert response.jobs
    assert response.jobs[0].match_score >= 45
    assert "FastAPI" in response.jobs[0].matched_skills
