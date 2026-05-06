"""AI Optimized by Skills Agent: Lightweight web scraping for job posts without extra dependencies."""
from html.parser import HTMLParser
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


# AI Optimized by Skills Agent: Raised when a job URL cannot be fetched or converted to text.
class JobScrapingError(Exception):
    pass


# AI Optimized by Skills Agent: HTML parser extracts ATS-relevant text blocks from job pages.
class _JobHTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._capture_stack: list[str] = []
        self._chunks: list[str] = []

    # AI Optimized by Skills Agent: Capture common semantic job content tags while ignoring script/style noise.
    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"title", "h1", "h2", "h3", "p", "li"}:
            self._capture_stack.append(tag)

    # AI Optimized by Skills Agent: Pops only matching tags to keep malformed pages from breaking extraction.
    def handle_endtag(self, tag: str) -> None:
        if self._capture_stack and self._capture_stack[-1] == tag:
            self._capture_stack.pop()

    # AI Optimized by Skills Agent: Normalizes whitespace early so downstream AI prompts stay compact.
    def handle_data(self, data: str) -> None:
        if not self._capture_stack:
            return
        cleaned = " ".join(data.split())
        if cleaned:
            self._chunks.append(cleaned)

    # AI Optimized by Skills Agent: De-duplicates adjacent repeated fragments common in job boards.
    def text(self) -> str:
        seen: set[str] = set()
        ordered_chunks: list[str] = []
        for chunk in self._chunks:
            if chunk.lower() in seen:
                continue
            seen.add(chunk.lower())
            ordered_chunks.append(chunk)
        return "\n".join(ordered_chunks)


# AI Optimized by Skills Agent: Fetches and extracts job description text from public HTTP(S) pages.
class JobScraperService:
    def scrape(self, source_url: str) -> str:
        parsed = urlparse(source_url)
        if parsed.scheme not in {"http", "https"}:
            raise JobScrapingError("Only http and https job URLs are supported.")

        request = Request(
            source_url,
            headers={
                "User-Agent": "Quick-Career-Hackathon/1.0 (+https://github.com/MrcDprm/quick-career-)"
            },
        )

        try:
            with urlopen(request, timeout=8) as response:
                content_type = response.headers.get("content-type", "")
                body = response.read(500_000)
        except (OSError, URLError) as exc:
            raise JobScrapingError(f"Could not fetch job URL: {source_url}") from exc

        if "html" not in content_type and content_type:
            raise JobScrapingError("Job URL did not return an HTML page.")

        html = body.decode("utf-8", errors="ignore")
        extractor = _JobHTMLTextExtractor()
        extractor.feed(html)
        extracted = extractor.text()

        if len(extracted) < 40:
            raise JobScrapingError("Could not extract enough job text from the URL.")

        return extracted[:20_000]
