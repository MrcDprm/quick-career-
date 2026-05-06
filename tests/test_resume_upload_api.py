# AI Optimized by Skills Agent: Resume API tests define the profile contract used by optimization work.
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from app.main import create_app  # noqa: E402


def test_upload_resume_returns_structured_profile_and_trace_id() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/resumes/upload",
        json={
            "source_type": "text",
            "owner_name": "Erdem",
            "raw_text": "Erdem is a software developer with Python, FastAPI and SQL experience.",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["profile"]["owner_name"] == "Erdem"
    assert "FastAPI" in payload["profile"]["skills"]
    assert payload["profile"]["experiences"][0]["title"] == "Software Developer"
    assert payload["trace_id"]
    assert "raw_text" not in payload


def test_get_resume_returns_previously_parsed_profile() -> None:
    client = TestClient(create_app())
    created = client.post(
        "/api/resumes/upload",
        json={
            "source_type": "text",
            "raw_text": "Candidate has backend API delivery experience with Python and databases.",
        },
    ).json()

    response = client.get(f"/api/resumes/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_upload_resume_rejects_too_short_or_empty_input() -> None:
    client = TestClient(create_app())

    response = client.post("/api/resumes/upload", json={"raw_text": "short"})

    assert response.status_code == 422


def test_get_resume_returns_404_for_unknown_id() -> None:
    client = TestClient(create_app())

    response = client.get("/api/resumes/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
