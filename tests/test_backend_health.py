# AI Optimized by Skills Agent: FastAPI smoke tests verify the Sprint 1 backend skeleton boots.
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
BACKEND_SRC = ROOT / "backend" / "src"
sys.path.insert(0, str(BACKEND_SRC))

from app.main import create_app  # noqa: E402


def test_health_endpoint_returns_service_metadata() -> None:
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "quick-career-api",
        "version": "0.1.0",
    }


def test_workflow_routers_are_registered_under_api_prefix() -> None:
    route_paths = {route.path for route in create_app().routes}

    assert "/api/jobs/" in route_paths
    assert "/api/resumes/" in route_paths
    assert "/api/optimizations/" in route_paths
    assert "/api/applications/" in route_paths
    assert "/api/metrics/" in route_paths
