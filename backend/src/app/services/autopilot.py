"""AI Optimized by Skills Agent: End-to-end LinkedIn-to-ATS-CV-to-application workflow."""

from app.schemas.application import ApplicationSubmissionRequest
from app.schemas.autopilot import (
    AutopilotApplicationResult,
    AutopilotApplyRequest,
    AutopilotApplyResponse,
)
from app.schemas.export import ExportFormat, ExportRequest
from app.schemas.optimization import OptimizationRequest
from app.services.application_submission import ApplicationSubmissionService
from app.services.cv_optimizer import CVOptimizerService
from app.services.document_export import DocumentExportService
from app.services.linkedin_scraper import LinkedInJobSearchService
from app.services.profile_store import CandidateProfileService, candidate_profile_service


# Reasoning by Skills Agent:
# 1. Save the user's complete personal profile first so every later artifact has one source of truth.
# 2. Search LinkedIn/public jobs with filters, then rank by overlap with saved skills.
# 3. For each suitable job, generate an ATS CV from all available profile data, not just a short CV text.
# 4. Export the generated ATS Markdown and immediately submit the application package in sequence.
# 5. Return the entire trace so the demo can show automation and manual-work reduction clearly.


# AI Optimized by Skills Agent: Coordinates profile storage, job scraping, ATS generation and submissions.
class AutopilotApplicationService:
    def __init__(
        self,
        *,
        profiles: CandidateProfileService | None = None,
        linkedin: LinkedInJobSearchService | None = None,
        optimizer: CVOptimizerService | None = None,
        exporter: DocumentExportService | None = None,
        submissions: ApplicationSubmissionService | None = None,
    ) -> None:
        self._profiles = profiles or candidate_profile_service
        self._linkedin = linkedin or LinkedInJobSearchService()
        self._optimizer = optimizer or CVOptimizerService()
        self._exporter = exporter or DocumentExportService()
        self._submissions = submissions or ApplicationSubmissionService()

    # AI Optimized by Skills Agent: Runs the user's desired scenario from profile input to ordered applications.
    async def run(self, request: AutopilotApplyRequest) -> AutopilotApplyResponse:
        profile = self._profiles.save(request.profile)
        resume_text = self._profiles.to_resume_text(profile)
        candidate_brief = self._profiles.to_candidate_brief(profile)
        search = self._linkedin.search(request.filters, profile.skills)
        applications: list[AutopilotApplicationResult] = []

        for job in search.jobs[: request.max_applications]:
            if request.filters.easy_apply_only and not job.easy_apply:
                continue

            optimization = await self._optimizer.optimize(
                OptimizationRequest(
                    target_role=job.title,
                    resume_text=resume_text,
                    job_keywords=job.keywords or request.filters.keywords or profile.skills,
                    candidate_brief=candidate_brief,
                    candidate_name=profile.personal.full_name,
                )
            )
            generated_resume = self._exporter.export(
                ExportRequest(
                    optimization_run_id=optimization.id,
                    format=ExportFormat.MARKDOWN,
                    candidate_name=profile.personal.full_name,
                    target_role=job.title,
                    optimized_summary=optimization.application_brief,
                    optimized_skills=optimization.highlighted_skills,
                    ats_resume_markdown=optimization.ats_resume_markdown,
                )
            )
            submission = self._submissions.submit(
                ApplicationSubmissionRequest(
                    optimization_run_id=optimization.id,
                    target=f"{job.company} - {job.title}",
                    candidate_email=profile.personal.email,
                    resume_file_name=generated_resume.file_name,
                    cover_letter=optimization.application_brief,
                    mode=request.submission_mode,
                )
            )
            applications.append(
                AutopilotApplicationResult(
                    job=job,
                    optimization=optimization,
                    generated_resume=generated_resume,
                    submission=submission,
                )
            )

        return AutopilotApplyResponse(
            profile=profile,
            search=search,
            applications=applications,
            total_applications=len(applications),
            summary=(
                f"{profile.personal.full_name} profili kaydedildi, {len(search.jobs)} LinkedIn Kolay Başvuru ilanı "
                f"filtrelendi ve {len(applications)} ATS uyumlu başvuru paketi gönderildi."
            ),
        )
