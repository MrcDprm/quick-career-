"""AI Optimized by Skills Agent: Real LinkedIn Easy Apply job discovery adapter."""
from dataclasses import dataclass, field
from html.parser import HTMLParser
from urllib.error import URLError
from urllib.parse import parse_qs, urlencode, urljoin, urlparse
from urllib.request import Request, urlopen

from app.schemas.linkedin import LinkedInJobFilters, LinkedInJobListing, LinkedInJobSearchResponse
from app.services.web_scraper import JobScrapingError

LINKEDIN_GUEST_SEARCH_URL = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search"
LINKEDIN_GUEST_DETAIL_URL = "https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}"


# AI Optimized by Skills Agent: Internal card shape keeps parser state separate from API schemas.
@dataclass
class _ParsedJobCard:
    job_id: str
    title_chunks: list[str] = field(default_factory=list)
    company_chunks: list[str] = field(default_factory=list)
    location_chunks: list[str] = field(default_factory=list)
    text_chunks: list[str] = field(default_factory=list)
    source_url: str | None = None


# AI Optimized by Skills Agent: Parser extracts real LinkedIn guest search cards and their job ids.
class _LinkedInJobSearchParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self._base_url = base_url
        self._card: _ParsedJobCard | None = None
        self._card_depth = 0
        self._field_name: str | None = None
        self._field_depth = 0
        self._cards: list[_ParsedJobCard] = []

    # AI Optimized by Skills Agent: Starts a card only when LinkedIn exposes a real job posting URN.
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get("class") or ""
        href = attrs_dict.get("href")
        entity_urn = attrs_dict.get("data-entity-urn") or ""

        if "urn:li:jobPosting:" in entity_urn:
            job_id = entity_urn.rsplit(":", maxsplit=1)[-1]
            self._card = _ParsedJobCard(job_id=job_id)
            self._card_depth = 1
            self._field_name = None
            self._field_depth = 0
            return

        if self._card is None:
            return

        self._card_depth += 1
        if href and "/jobs/view/" in href:
            self._card.source_url = urljoin(self._base_url, href)

        next_field = self._field_from_class(class_name)
        if next_field:
            self._field_name = next_field
            self._field_depth = 1
        elif self._field_name:
            self._field_depth += 1

    # AI Optimized by Skills Agent: Closes nested fields before flushing the completed LinkedIn card.
    def handle_endtag(self, tag: str) -> None:
        if self._card is None:
            return

        if self._field_name:
            self._field_depth -= 1
            if self._field_depth <= 0:
                self._field_name = None
                self._field_depth = 0

        self._card_depth -= 1
        if self._card_depth <= 0:
            self._flush_card()

    # AI Optimized by Skills Agent: Captures both full card text and class-specific title/company/location text.
    def handle_data(self, data: str) -> None:
        if self._card is None:
            return

        cleaned = " ".join(data.split())
        if not cleaned:
            return

        self._card.text_chunks.append(cleaned)
        if self._field_name == "title":
            self._card.title_chunks.append(cleaned)
        elif self._field_name == "company":
            self._card.company_chunks.append(cleaned)
        elif self._field_name == "location":
            self._card.location_chunks.append(cleaned)

    # AI Optimized by Skills Agent: Normalizes parsed cards into listing contracts marked as Easy Apply.
    def listings(self, filters: LinkedInJobFilters) -> list[LinkedInJobListing]:
        listings: list[LinkedInJobListing] = []
        for card in self._cards:
            raw_text = _compact_text(" ".join(card.text_chunks))
            if len(raw_text) < 12:
                continue

            title = _compact_text(" ".join(card.title_chunks)) or _fallback_title(filters)
            company = _compact_text(" ".join(card.company_chunks)) or "LinkedIn"
            location = _compact_text(" ".join(card.location_chunks)) or filters.location or "Uzaktan"
            listings.append(
                LinkedInJobListing(
                    linkedin_job_id=card.job_id,
                    title=title,
                    company=company,
                    location=location,
                    source_url=card.source_url or f"https://www.linkedin.com/jobs/view/{card.job_id}",
                    raw_text=raw_text,
                    keywords=filters.keywords,
                    easy_apply=filters.easy_apply_only,
                )
            )
        return listings

    # AI Optimized by Skills Agent: Maps LinkedIn public card classes into stable semantic fields.
    def _field_from_class(self, class_name: str) -> str | None:
        if "base-search-card__title" in class_name:
            return "title"
        if "base-search-card__subtitle" in class_name:
            return "company"
        if "job-search-card__location" in class_name:
            return "location"
        return None

    # AI Optimized by Skills Agent: Saves one completed job card and resets parser state.
    def _flush_card(self) -> None:
        if self._card is not None:
            self._cards.append(self._card)
        self._card = None
        self._card_depth = 0
        self._field_name = None
        self._field_depth = 0


# AI Optimized by Skills Agent: Lightweight text parser turns LinkedIn detail HTML into ATS keyword input.
class _VisibleTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []

    # AI Optimized by Skills Agent: Keeps detail extraction dependency-free for backend tests.
    def handle_data(self, data: str) -> None:
        cleaned = " ".join(data.split())
        if cleaned:
            self._chunks.append(cleaned)

    # AI Optimized by Skills Agent: Returns compact text for matching and CV tailoring.
    def text(self) -> str:
        return _compact_text(" ".join(self._chunks))


# AI Optimized by Skills Agent: Service fetches real LinkedIn Easy Apply jobs and ranks them by profile fit.
class LinkedInJobSearchService:
    # AI Optimized by Skills Agent: Searches only Easy Apply results and never replaces failures with fake jobs.
    def search(self, filters: LinkedInJobFilters, profile_skills: list[str]) -> LinkedInJobSearchResponse:
        search_url = self._normalize_search_url(filters.linkedin_search_url, filters)
        html = self._fetch_search_html(search_url)
        jobs = self._parse_search_results(search_url, html, filters)
        jobs = self._enrich_job_details(jobs, filters)
        filtered = self._filter_and_score(jobs, filters, profile_skills)

        if not filtered:
            raise JobScrapingError(
                "LinkedIn Kolay Başvuru ilanları bulundu ancak profil yetenekleriyle yeterli eşleşme yakalanamadı."
            )

        return LinkedInJobSearchResponse(source=search_url, filters=filters, jobs=filtered[: filters.limit])

    # AI Optimized by Skills Agent: Forces user-provided LinkedIn URLs through the public Easy Apply guest endpoint.
    def _normalize_search_url(self, source_url: str | None, filters: LinkedInJobFilters) -> str:
        if not source_url:
            return self._build_search_url(filters)

        query = parse_qs(urlparse(source_url).query)
        keywords = _first_query_value(query, "keywords") or " ".join(filters.keywords) or "software developer"
        location = _first_query_value(query, "location") or filters.location or "Remote"
        remote = _first_query_value(query, "f_WT")
        experience = _first_query_value(query, "f_E") or filters.experience_level
        start = _first_query_value(query, "start") or "0"

        normalized_query: dict[str, str] = {
            "keywords": keywords,
            "location": location,
            "start": start,
        }
        if filters.easy_apply_only:
            normalized_query["f_AL"] = "true"
        if filters.remote_only or remote:
            normalized_query["f_WT"] = remote or "2"
        if experience:
            normalized_query["f_E"] = experience

        return f"{LINKEDIN_GUEST_SEARCH_URL}?{urlencode(normalized_query)}"

    # AI Optimized by Skills Agent: Builds a public LinkedIn guest search URL from user filters.
    def _build_search_url(self, filters: LinkedInJobFilters) -> str:
        query: dict[str, str] = {
            "keywords": " ".join(filters.keywords) if filters.keywords else "software developer",
            "location": filters.location or "Remote",
            "start": "0",
        }
        if filters.easy_apply_only:
            query["f_AL"] = "true"
        if filters.remote_only:
            query["f_WT"] = "2"
        if filters.experience_level:
            query["f_E"] = filters.experience_level
        return f"{LINKEDIN_GUEST_SEARCH_URL}?{urlencode(query)}"

    # AI Optimized by Skills Agent: Fetches raw LinkedIn Easy Apply search HTML from the guest endpoint.
    def _fetch_search_html(self, source_url: str) -> str:
        return self._fetch_url(source_url, "LinkedIn Kolay Başvuru arama sonucu çekilemedi")

    # AI Optimized by Skills Agent: Fetches individual posting details so matching uses real job descriptions.
    def _fetch_job_detail_html(self, job_id: str) -> str:
        return self._fetch_url(
            LINKEDIN_GUEST_DETAIL_URL.format(job_id=job_id),
            "LinkedIn ilan detayı çekilemedi",
        )

    # AI Optimized by Skills Agent: Shared network helper keeps LinkedIn request headers consistent.
    def _fetch_url(self, source_url: str, error_prefix: str) -> str:
        request = Request(
            source_url,
            headers={
                "User-Agent": "Quick-Career-Hackathon/1.0 (+https://github.com/MrcDprm/quick-career-)",
                "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
            },
        )
        try:
            with urlopen(request, timeout=10) as response:
                body = response.read(1_200_000)
        except (OSError, URLError) as exc:
            raise JobScrapingError(f"{error_prefix}: {source_url}") from exc
        return body.decode("utf-8", errors="ignore")

    # AI Optimized by Skills Agent: Parses real LinkedIn cards and fails loudly when the public result is empty.
    def _parse_search_results(
        self,
        source_url: str,
        scraped_text: str,
        filters: LinkedInJobFilters,
    ) -> list[LinkedInJobListing]:
        parser = _LinkedInJobSearchParser(source_url)
        parser.feed(scraped_text)
        listings = parser.listings(filters)
        if not listings:
            raise JobScrapingError("LinkedIn Kolay Başvuru filtresine uygun gerçek ilan bulunamadı.")
        return listings

    # AI Optimized by Skills Agent: Adds detail-page text to each real listing without inventing fallback data.
    def _enrich_job_details(
        self,
        jobs: list[LinkedInJobListing],
        filters: LinkedInJobFilters,
    ) -> list[LinkedInJobListing]:
        enriched_jobs: list[LinkedInJobListing] = []
        for job in jobs[: max(filters.limit * 3, filters.limit)]:
            if job.linkedin_job_id:
                try:
                    detail_html = self._fetch_job_detail_html(job.linkedin_job_id)
                except JobScrapingError:
                    detail_html = ""
                detail_text = self._parse_visible_text(detail_html) if detail_html else ""
                if detail_text:
                    job.raw_text = _compact_text(f"{job.raw_text} {detail_text}")
                    job.easy_apply = filters.easy_apply_only or _mentions_easy_apply(detail_text)
            enriched_jobs.append(job)
        return enriched_jobs

    # AI Optimized by Skills Agent: Converts detail HTML to compact text for match scoring and keyword extraction.
    def _parse_visible_text(self, html: str) -> str:
        parser = _VisibleTextParser()
        parser.feed(html)
        return parser.text()

    # AI Optimized by Skills Agent: Scores Easy Apply listings by actual job text and candidate skill overlap.
    def _filter_and_score(
        self,
        jobs: list[LinkedInJobListing],
        filters: LinkedInJobFilters,
        profile_skills: list[str],
    ) -> list[LinkedInJobListing]:
        normalized_profile_skills = [skill.lower() for skill in profile_skills]
        scored_jobs: list[LinkedInJobListing] = []
        for job in jobs:
            if filters.easy_apply_only and not job.easy_apply:
                continue

            haystack = f"{job.title} {job.company} {job.raw_text}".lower()
            matched = [
                skill
                for skill, normalized in zip(profile_skills, normalized_profile_skills)
                if normalized and normalized in haystack
            ]
            if len(matched) < filters.minimum_skill_matches:
                continue

            job.matched_skills = _unique(matched)
            job.keywords = self._extract_job_keywords(job, filters, profile_skills)
            job.match_score = min(98, 45 + (len(job.matched_skills) * 12))
            scored_jobs.append(job)
        return sorted(scored_jobs, key=lambda item: item.match_score, reverse=True)

    # AI Optimized by Skills Agent: Prioritizes keywords actually present in the job post for ATS CV generation.
    def _extract_job_keywords(
        self,
        job: LinkedInJobListing,
        filters: LinkedInJobFilters,
        profile_skills: list[str],
    ) -> list[str]:
        haystack = f"{job.title} {job.raw_text}".lower()
        candidates = _unique([*filters.keywords, *profile_skills])
        present = [keyword for keyword in candidates if keyword.lower() in haystack]
        return present or filters.keywords or profile_skills[:8]


# AI Optimized by Skills Agent: Text compaction prevents noisy LinkedIn whitespace from leaking into the UI.
def _compact_text(value: str) -> str:
    return " ".join(value.split())


# AI Optimized by Skills Agent: Fallback title only names the query when a real card omits title text.
def _fallback_title(filters: LinkedInJobFilters) -> str:
    return filters.keywords[0] if filters.keywords else "LinkedIn Kolay Başvuru İlanı"


# AI Optimized by Skills Agent: Query helper keeps optional user LinkedIn URLs deterministic.
def _first_query_value(query: dict[str, list[str]], key: str) -> str | None:
    values = query.get(key)
    if not values:
        return None
    return values[0]


# AI Optimized by Skills Agent: Deduplicates keywords while preserving user/profile ordering.
def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    unique_values: list[str] = []
    for value in values:
        normalized = value.strip().lower()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        unique_values.append(value.strip())
    return unique_values


# AI Optimized by Skills Agent: Detects explicit Easy Apply wording from LinkedIn detail pages when present.
def _mentions_easy_apply(value: str) -> bool:
    normalized = value.lower()
    return "easy apply" in normalized or "kolay başvuru" in normalized
