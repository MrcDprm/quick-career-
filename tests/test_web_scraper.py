# AI Optimized by Skills Agent: Tests cover deterministic HTML-to-job-text extraction helpers.
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))

from app.services.web_scraper import _JobHTMLTextExtractor  # noqa: E402


# AI Optimized by Skills Agent: Verifies scraper extracts ATS-relevant visible job content.
def test_html_text_extractor_keeps_job_content() -> None:
    parser = _JobHTMLTextExtractor()
    parser.feed(
        """
        <html>
          <head><title>Backend Developer</title></head>
          <body>
            <h1>Backend Developer</h1>
            <p>We need Python, FastAPI and PostgreSQL experience.</p>
            <ul><li>Own automation APIs</li></ul>
            <script>ignore me</script>
          </body>
        </html>
        """
    )

    text = parser.text()
    assert "Backend Developer" in text
    assert "FastAPI" in text
    assert "ignore me" not in text
