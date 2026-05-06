# AI Optimized by Skills Agent: Tests prove QC-010 automatic submission API behavior.
import sys
from pathlib import Path
from uuid import uuid4

from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))

from app.main import app  # noqa: E402


# AI Optimized by Skills Agent: Covers autonomous mock submission and receipt retrieval.
def test_submit_application_returns_receipt() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/applications/submit",
        json={
            "optimization_run_id": str(uuid4()),
            "target": "Example Software Team",
            "resume_file_name": "quick-career-full-stack-developer.md",
            "cover_letter": "I am aligned with the role requirements and ready to contribute.",
            "mode": "mock",
        },
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["status"] == "submitted"
    assert payload["receipt"].startswith("QC-SUB-")

    receipt_response = client.get(f"/api/applications/{payload['id']}")

    assert receipt_response.status_code == 200
    assert receipt_response.json()["id"] == payload["id"]


# AI Optimized by Skills Agent: Incomplete packages are rejected without introducing a manual approval gate.
def test_submit_application_rejects_incomplete_package() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/applications/submit",
        json={
            "optimization_run_id": str(uuid4()),
            "target": "Example Software Team",
            "resume_file_name": "quick-career.md",
            "cover_letter": "",
            "mode": "mock",
        },
    )

    assert response.status_code == 422
