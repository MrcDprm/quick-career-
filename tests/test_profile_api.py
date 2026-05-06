# AI Optimized by Skills Agent: Tests cover saved personal profile data required by the final scenario.
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))

from app.main import create_app  # noqa: E402


# AI Optimized by Skills Agent: Profile endpoint stores personal info, education, certificates and skills.
def test_save_profile_and_fetch_latest() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/profile/",
        json={
            "personal": {
                "full_name": "Demo Candidate",
                "email": "candidate@example.com",
                "links": ["https://linkedin.com/in/demo"],
            },
            "summary": "Developer focused on FastAPI, React and workflow automation.",
            "skills": ["FastAPI", "React", "PostgreSQL"],
            "education": [{"school": "Demo University", "degree": "Computer Engineering"}],
            "certifications": [{"name": "FastAPI Foundations"}],
            "experiences": [
                {
                    "title": "Software Developer",
                    "company": "Demo Labs",
                    "highlights": ["Built APIs", "Automated reporting"],
                }
            ],
            "projects": [{"name": "Quick-Career", "description": "ATS CV automation"}],
            "languages": ["Turkish", "English"],
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["personal"]["full_name"] == "Demo Candidate"
    assert payload["skills"] == ["FastAPI", "React", "PostgreSQL"]

    latest = client.get("/api/profile/latest")

    assert latest.status_code == 200
    assert latest.json()["id"] == payload["id"]
