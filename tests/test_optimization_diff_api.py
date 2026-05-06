# AI Optimized by Skills Agent: Tests prove QC-007 optimization diff API behavior.
import sys
from pathlib import Path

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))

from app.main import app  # noqa: E402


# AI Optimized by Skills Agent: Covers autonomous optimization creation and reviewable diff retrieval.
def test_create_optimization_and_fetch_diff() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/optimizations/",
        json={
            "target_role": "Full Stack Developer",
            "resume_text": "Built FastAPI services and React interfaces for automation workflows.",
            "job_keywords": ["FastAPI", "React", "PostgreSQL", "automation"],
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "finalized"
    assert payload["match_score_after"] > payload["match_score_before"]
    assert len(payload["diff"]) >= 3

    diff_response = client.get(f"/api/optimizations/{payload['id']}/diff")

    assert diff_response.status_code == 200
    diff_payload = diff_response.json()
    assert diff_payload["optimization_run_id"] == payload["id"]
    assert diff_payload["diff"][0]["section"] == "summary"
