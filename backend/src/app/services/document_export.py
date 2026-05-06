"""AI Optimized by Skills Agent: Document export service for optimized CV outputs."""

from app.schemas.export import ExportFormat, ExportRequest, GeneratedResumeResponse


# AI Optimized by Skills Agent: Raised when an export request cannot produce a final artifact.
class DocumentExportError(Exception):
    pass


# AI Optimized by Skills Agent: Creates deterministic MVP document content without filesystem side effects.
class DocumentExportService:
    # AI Optimized by Skills Agent: Generates final content after autonomous optimization completes.
    def export(self, request: ExportRequest) -> GeneratedResumeResponse:
        if not request.optimized_summary.strip():
            raise DocumentExportError("Optimized summary is required before export.")

        content = self._render_markdown(request)
        extension = "md" if request.format == ExportFormat.MARKDOWN else request.format.value

        return GeneratedResumeResponse(
            optimization_run_id=request.optimization_run_id,
            format=request.format,
            file_name=f"quick-career-{request.target_role.lower().replace(' ', '-')}.{extension}",
            content=content,
            is_final=True,
        )

    # AI Optimized by Skills Agent: Markdown is the canonical source used by later PDF/DOCX adapters.
    def _render_markdown(self, request: ExportRequest) -> str:
        skills = "\n".join(f"- {skill}" for skill in request.optimized_skills)
        return (
            f"# {request.candidate_name}\n\n"
            f"## Target Role\n{request.target_role}\n\n"
            f"## Optimized Summary\n{request.optimized_summary}\n\n"
            f"## Targeted Skills\n{skills}\n"
        )
