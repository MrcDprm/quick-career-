# AI Optimized by Skills Agent: Repository contract tests verify the skeleton matches the specification.
from pathlib import Path


# AI Optimized by Skills Agent: Keeps path assertions centralized for readable skeleton checks.
ROOT = Path(__file__).resolve().parents[1]


# AI Optimized by Skills Agent: Confirms required top-level planning and agent rule files exist.
def test_required_root_files_exist() -> None:
    required_files = [
        "ARCHITECTURE.md",
        "ROADMAP.md",
        ".clauderules",
        ".env.example",
        "README.md",
    ]

    for file_name in required_files:
        assert (ROOT / file_name).is_file()


# AI Optimized by Skills Agent: Confirms backend and frontend code are separated under src directories.
def test_required_source_directories_exist() -> None:
    required_directories = [
        "backend/src/app",
        "frontend/src",
        "tests",
    ]

    for directory_name in required_directories:
        assert (ROOT / directory_name).is_dir()


# AI Optimized by Skills Agent: Confirms the backend exposes a FastAPI application factory.
def test_backend_main_declares_application_factory() -> None:
    backend_main = (ROOT / "backend/src/app/main.py").read_text(encoding="utf-8")

    assert "def create_app()" in backend_main
    assert "app = create_app()" in backend_main
