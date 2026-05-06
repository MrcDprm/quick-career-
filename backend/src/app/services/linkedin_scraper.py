"""AI Optimized by Skills Agent: LinkedIn/public job discovery adapter with deterministic fallback."""
from html.parser import HTMLParser
from urllib.error import URLError
from urllib.parse import quote_plus, urljoin
from urllib.request import Request, urlopen

from app.schemas.linkedin import LinkedInJobFilters, LinkedInJobListing, LinkedInJobSearchResponse
from app.services.web_scraper import JobScrapingError


# AI Optimized by Skills Agent: Parser extracts visible job card-like text and LinkedIn job links.
class _LinkedInJobSearchParser(HTMLParser):
    def __init__(self, base_url: str) -> None:
        super().__init__()
        self._base_url = base_url
        self._capture = False
        self._current_href: str | None = None
        self._chunks: list[str] = []
        self._cards: list[tuple[str, str | None]] = []

    # AI Optimized by Skills Agent: Captures anchors/list items commonly used in public job search HTML.
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        href = attrs_dict.get("href")
        class_name = attrs_dict.get("class") or ""
        if tag in {"a", "li", "div"} and ("job" in class_name.lower() or (href and "/jobs/view/" in href)):
            self._capture = True
            self._current_href = urljoin(self._base_url, href) if href else self._current_href

    # AI Optimized by Skills Agent: Flushes a captured card once the related element closes.
    def handle_endtag(self, tag: str) -> None:
        if self._capture and tag in {"a", "li", "div"}:
            text = " ".join(" ".join(self._chunks).split())
            if len(text) >= 12:
                self._cards.append((text, self._current_href))
            self._capture = False
            self._current_href = None
            self._chunks = []

    # AI Optimized by Skills Agent: Keeps parser output compact for deterministic filtering.
    def handle_data(self, data: str) -> None:
        if self._capture:
            cleaned = " ".join(data.split())
            if cleaned:
                self._chunks.append(cleaned)

    # AI Optimized by Skills Agent: Converts raw cards to normalized listings with conservative field guesses.
    def listings(self, filters: LinkedInJobFilters) -> list[LinkedInJobListing]:
        listings: list[LinkedInJobListing] = []
        for index, (text, href) in enumerate(self._cards):
            parts = [part.strip() for part in text.split(" · ") if part.strip()]
            title = parts[0] if parts else self._fallback_title(filters, index)
            company = parts[1] if len(parts) > 1 else "LinkedIn Company"
            location = parts[2] if len(parts) > 2 else (filters.location or "Remote")
            listings.append(
                LinkedInJobListing(
                    title=title,
                    company=company,
                    location=location,
                    source_url=href or self._fallback_url(filters, index),
                    raw_text=text,
                    keywords=filters.keywords,
                )
            )
        return listings

    # AI Optimized by Skills Agent: Fallback naming keeps malformed search pages demo-safe.
    def _fallback_title(self, filters: LinkedInJobFilters, index: int) -> str:
        keyword = filters.keywords[0] if filters.keywords else "Software Developer"
        return f"{keyword} Role {index + 1}"

    # AI Optimized by Skills Agent: Fallback URL remains a LinkedIn-style public search target.
    def _fallback_url(self, filters: LinkedInJobFilters, index: int) -> str:
        keyword = quote_plus(filters.keywords[0] if filters.keywords else "software developer")
        return f"https://www.linkedin.com/jobs/search/?keywords={keyword}&position={index + 1}"


# AI Optimized by Skills Agent: Service scrapes LinkedIn search pages and filters listings against profile skills.
class LinkedInJobSearchService:
    # AI Optimized by Skills Agent: Finds suitable jobs and falls back to deterministic demo listings if blocked.
    def search(self, filters: LinkedInJobFilters, profile_skills: list[str]) -> LinkedInJobSearchResponse:
        search_url = filters.linkedin_search_url or self._build_search_url(filters)
        try:
            html = self._fetch_search_html(search_url)
            jobs = self._parse_search_results(search_url, html, filters)
        except JobScrapingError:
            jobs = self._fallback_jobs(filters)

        filtered = self._filter_and_score(jobs, filters, profile_skills)
        return LinkedInJobSearchResponse(source=search_url, filters=filters, jobs=filtered[: filters.limit])

    # AI Optimized by Skills Agent: Builds a public LinkedIn search URL from user filters.
    def _build_search_url(self, filters: LinkedInJobFilters) -> str:
        keywords = quote_plus(" ".join(filters.keywords) if filters.keywords else "software developer")
        location = quote_plus(filters.location or "Remote")
        remote = "&f_WT=2" if filters.remote_only else ""
        return f"https://www.linkedin.com/jobs/search/?keywords={keywords}&location={location}{remote}"

    # AI Optimized by Skills Agent: Fetches raw search HTML so job links/cards can be parsed before fallback.
    def _fetch_search_html(self, source_url: str) -> str:
        request = Request(
            source_url,
            headers={
                "User-Agent": "Quick-Career-Hackathon/1.0 (+https://github.com/MrcDprm/quick-career-)"
            },
        )
        try:
            with urlopen(request, timeout=8) as response:
                body = response.read(800_000)
        except (OSError, URLError) as exc:
            raise JobScrapingError(f"Could not fetch LinkedIn search URL: {source_url}") from exc
        return body.decode("utf-8", errors="ignore")

    # AI Optimized by Skills Agent: Parses visible job search text into normalized listings.
    def _parse_search_results(
        self,
        source_url: str,
        scraped_text: str,
        filters: LinkedInJobFilters,
    ) -> list[LinkedInJobListing]:
        parser = _LinkedInJobSearchParser(source_url)
        parser.feed(scraped_text)
        listings = parser.listings(filters)
        if listings:
            return listings
        return [
            LinkedInJobListing(
                title=filters.keywords[0] if filters.keywords else "Software Developer",
                company="LinkedIn Public Result",
                location=filters.location or "Remote",
                source_url=source_url,
                raw_text=scraped_text,
                keywords=filters.keywords,
            )
        ]

    # AI Optimized by Skills Agent: Fallback jobs keep the end-to-end demo working without LinkedIn login.
    def _fallback_jobs(self, filters: LinkedInJobFilters) -> list[LinkedInJobListing]:
        base_keywords = filters.keywords or ["Python", "FastAPI", "React", "automation"]
        location = filters.location or "Remote"
        return [
            LinkedInJobListing(
                title=f"{base_keywords[0]} Backend Developer",
                company="Demo LinkedIn Company",
                location=location,
                source_url="https://www.linkedin.com/jobs/search/",
                raw_text=(
                    f"{base_keywords[0]} Backend Developer role requiring "
                    f"{', '.join(base_keywords)}, API ownership and ATS-friendly communication."
                ),
                keywords=base_keywords,
            ),
            LinkedInJobListing(
                title="Full Stack Automation Engineer",
                company="Workflow Systems",
                location=location,
                source_url="https://www.linkedin.com/jobs/search/",
                raw_text="Full Stack Automation Engineer with React, FastAPI, PostgreSQL and workflow automation.",
                keywords=["React", "FastAPI", "PostgreSQL", "automation"],
            ),
        ]

    # AI Optimized by Skills Agent: Scores listings by overlap between profile skills and job keywords/text.
    def _filter_and_score(
        self,
        jobs: list[LinkedInJobListing],
        filters: LinkedInJobFilters,
        profile_skills: list[str],
    ) -> list[LinkedInJobListing]:
        normalized_profile_skills = [skill.lower() for skill in profile_skills]
        scored_jobs: list[LinkedInJobListing] = []
        for job in jobs:
            haystack = f"{job.title} {job.raw_text} {' '.join(job.keywords)}".lower()
            matched = [
                skill
                for skill, normalized in zip(profile_skills, normalized_profile_skills)
                if normalized and normalized in haystack
            ]
            if len(matched) < filters.minimum_skill_matches:
                continue
            job.matched_skills = matched
            job.match_score = min(98, 45 + (len(matched) * 12))
            scored_jobs.append(job)
        return sorted(scored_jobs, key=lambda item: item.match_score, reverse=True)
