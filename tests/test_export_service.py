# AI Optimized by Skills Agent: Tests prove QC-009 export service creates final resume artifacts.
import sys
from pathlib import Path
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend" / "src"))

from app.schemas.export import ExportFormat, ExportRequest
from app.services.document_export import DocumentExportService


# AI Optimized by Skills Agent: Verifies Markdown is generated as the canonical MVP export content.
def test_document_export_service_generates_markdown_resume() -> None:
    optimization_id = uuid4()
    service = DocumentExportService()

    result = service.export(
        ExportRequest(
            optimization_run_id=optimization_id,
            format=ExportFormat.MARKDOWN,
            candidate_name="Ada Lovelace",
            target_role="Full Stack Developer",
            optimized_summary="Builds automation products with FastAPI and React.",
            optimized_skills=["FastAPI", "React", "PostgreSQL"],
        )
    )

    assert result.optimization_run_id == optimization_id
    assert result.file_name.endswith(".md")
    assert result.is_final is True
    assert "FastAPI" in result.content
