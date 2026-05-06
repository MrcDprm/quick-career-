"""AI Optimized by Skills Agent: Autonomous CV optimization service for QC-007."""
from uuid import UUID, uuid4

from app.schemas.optimization import (
    OptimizationDiffItem,
    OptimizationDiffResponse,
    OptimizationRequest,
    OptimizationRunResponse,
    OptimizationStatus,
)


# Reasoning by Skills Agent:
# 1. Keep the first diff API deterministic so frontend work and tests are not blocked by paid AI calls.
# 2. Use job keywords to create explainable before/after changes instead of opaque text rewriting.
# 3. Combine the candidate's general briefing with CV text so the output is not a generic rewrite.
# 4. Generate ATS-friendly Markdown with plain headings, keyword-aligned skills and measurable bullets.
# 5. Persist runs in a simple in-memory store for hackathon MVP speed; database persistence can replace it later.


# AI Optimized by Skills Agent: Raised when a requested optimization run is not available in the demo store.
class OptimizationNotFoundError(Exception):
    pass


# AI Optimized by Skills Agent: Service creates reviewable autonomous CV diffs without external dependencies.
class CVOptimizerService:
    def __init__(self) -> None:
        self._runs: dict[UUID, OptimizationRunResponse] = {}

    # AI Optimized by Skills Agent: Generates deterministic changes that simulate target-role CV rewriting.
    async def optimize(self, request: OptimizationRequest) -> OptimizationRunResponse:
        optimization_id = uuid4()
        keywords = request.job_keywords or [request.target_role, "FastAPI", "React", "automation"]
        highlighted_skills = self._highlight_skills(request.resume_text, request.candidate_brief, keywords)
        score_before = self._score_resume(request.resume_text, keywords)
        score_after = min(98, score_before + 20 + min(len(highlighted_skills), 10))
        diff = self._build_diff(request, keywords, highlighted_skills)
        ats_resume = self._build_ats_resume(request, highlighted_skills)

        run = OptimizationRunResponse(
            id=optimization_id,
            status=OptimizationStatus.FINALIZED,
            target_role=request.target_role,
            match_score_before=score_before,
            match_score_after=score_after,
            diff=diff,
            highlighted_skills=highlighted_skills,
            ats_resume_markdown=ats_resume,
            application_brief=self._build_application_brief(request, highlighted_skills),
        )
        self._runs[optimization_id] = run
        return run

    # AI Optimized by Skills Agent: Returns a focused diff payload for review and automation trace screens.
    def get_diff(self, optimization_run_id: UUID) -> OptimizationDiffResponse:
        run = self._runs.get(optimization_run_id)
        if run is None:
            raise OptimizationNotFoundError(f"Optimization run {optimization_run_id} was not found.")

        return OptimizationDiffResponse(
            optimization_run_id=run.id,
            status=run.status,
            diff=run.diff,
        )

    # AI Optimized by Skills Agent: Keyword coverage gives a stable MVP match score without LLM variance.
    def _score_resume(self, resume_text: str, keywords: list[str]) -> int:
        normalized_resume = resume_text.lower()
        matches = sum(1 for keyword in keywords if keyword.lower() in normalized_resume)
        if not keywords:
            return 50

        return max(35, min(88, round((matches / len(keywords)) * 70) + 18))

    # AI Optimized by Skills Agent: Diff entries target the fields users care about in a CV rewrite.
    def _build_diff(
        self,
        request: OptimizationRequest,
        keywords: list[str],
        highlighted_skills: list[str],
    ) -> list[OptimizationDiffItem]:
        keyword_text = ", ".join(keywords[:6])
        skill_text = ", ".join(highlighted_skills[:8])
        return [
            OptimizationDiffItem(
                section="summary",
                before=request.resume_text[:180],
                after=(
                    f"{request.target_role} candidate with experience aligned to {skill_text}. "
                    "Optimized for the target job requirements and measurable impact."
                ),
                reason="Aligns the opening summary with the target role and highest-value keywords.",
            ),
            OptimizationDiffItem(
                section="skills",
                before="Existing skill order from uploaded CV",
                after=skill_text or keyword_text,
                reason="Moves job-critical keywords into the most visible skills section.",
            ),
            OptimizationDiffItem(
                section="experience",
                before="Generic responsibility-focused bullets",
                after="Rewritten impact bullets emphasize automation, ownership and role-specific outcomes.",
                reason="Turns repeated responsibilities into evidence that matches the job post.",
            ),
        ]

    # AI Optimized by Skills Agent: Matches job keywords against CV and briefing text to prioritize real strengths.
    def _highlight_skills(
        self,
        resume_text: str,
        candidate_brief: str,
        keywords: list[str],
    ) -> list[str]:
        combined_text = f"{resume_text} {candidate_brief}".lower()
        matched = [keyword for keyword in keywords if keyword.lower() in combined_text]
        remaining = [keyword for keyword in keywords if keyword not in matched]
        return (matched + remaining)[:10]

    # AI Optimized by Skills Agent: Builds a parser-friendly ATS CV with plain headings and no decorative layout.
    def _build_ats_resume(self, request: OptimizationRequest, highlighted_skills: list[str]) -> str:
        skills = "\n".join(f"- {skill}" for skill in highlighted_skills)
        brief = request.candidate_brief.strip() or "Candidate has provided role-relevant background."
        return (
            f"# {request.candidate_name}\n\n"
            f"## Target Role\n{request.target_role}\n\n"
            "## Professional Summary\n"
            f"{request.target_role} profile tailored to the job posting. {brief}\n\n"
            "## Core Skills\n"
            f"{skills}\n\n"
            "## Experience Highlights\n"
            f"- Applied {', '.join(highlighted_skills[:3])} to deliver role-relevant outcomes.\n"
            "- Reduced repetitive work through automation, structured documentation and ownership.\n"
            "- Communicated progress clearly for technical and non-technical stakeholders.\n\n"
            "## ATS Notes\n"
            "- Plain section headings, keyword-aligned skills and concise bullet points are used.\n"
        )

    # AI Optimized by Skills Agent: Produces the general application note the user wanted to send.
    def _build_application_brief(self, request: OptimizationRequest, highlighted_skills: list[str]) -> str:
        return (
            f"General application note for {request.target_role}: "
            f"the candidate's strongest aligned skills are {', '.join(highlighted_skills[:5])}. "
            "The attached ATS-friendly CV emphasizes these capabilities for the target posting."
        )
