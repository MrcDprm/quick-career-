# AI Optimized by Skills Agent: Tests cover real LinkedIn Easy Apply parsing without live network dependency.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))

from app.schemas.linkedin import LinkedInJobFilters  # noqa: E402
from app.services.linkedin_scraper import LinkedInJobSearchService  # noqa: E402

FAKE_LINKEDIN_SEARCH_HTML = """
<li>
  <div class="base-card job-search-card" data-entity-urn="urn:li:jobPosting:12345">
    <a href="https://www.linkedin.com/jobs/view/12345"></a>
    <h3 class="base-search-card__title">FastAPI React Developer</h3>
    <h4 class="base-search-card__subtitle">Gerçek LinkedIn Şirketi</h4>
    <span class="job-search-card__location">Türkiye</span>
  </div>
</li>
"""

FAKE_LINKEDIN_DETAIL_HTML = """
<section>
  <div class="description__text">
    FastAPI, React, PostgreSQL ve otomasyon tecrübesi arıyoruz.
    Application Process: Easy Apply on LinkedIn.
  </div>
</section>
"""


class _FakeLinkedInJobSearchService(LinkedInJobSearchService):
    # AI Optimized by Skills Agent: Avoids real network while preserving guest endpoint behavior.
    def _fetch_search_html(self, source_url: str) -> str:
        return FAKE_LINKEDIN_SEARCH_HTML

    # AI Optimized by Skills Agent: Supplies real-detail-like text for skill overlap scoring.
    def _fetch_job_detail_html(self, job_id: str) -> str:
        return FAKE_LINKEDIN_DETAIL_HTML


# AI Optimized by Skills Agent: Real Easy Apply cards are parsed, enriched and scored against profile skills.
def test_linkedin_search_filters_easy_apply_real_cards_by_profile_skills() -> None:
    service = _FakeLinkedInJobSearchService()

    response = service.search(
        LinkedInJobFilters(keywords=["FastAPI", "React"], location="Türkiye", limit=2),
        profile_skills=["FastAPI", "React", "PostgreSQL"],
    )

    assert response.source.startswith("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search")
    assert "f_AL=true" in response.source
    assert response.jobs
    assert response.jobs[0].easy_apply is True
    assert response.jobs[0].linkedin_job_id == "12345"
    assert response.jobs[0].match_score >= 45
    assert "FastAPI" in response.jobs[0].matched_skills
