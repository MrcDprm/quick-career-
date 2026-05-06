// AI Optimized by Skills Agent: Autonomous trace UI focuses on inspection, not manual approval gates.
import { useMemo, useState } from "react";

import {
  createOptimization,
  type OptimizationRequest,
  type OptimizationRunResponse,
} from "../../api/optimizations";

const demoRequest: OptimizationRequest = {
  target_role: "Backend Developer",
  resume_text:
    "Software developer with Python and SQL experience. Built internal tools and supported React dashboards for operational teams.",
  job_keywords: ["Python", "FastAPI", "PostgreSQL", "automation", "API ownership"],
  candidate_brief:
    "The candidate wants to emphasize API ownership, workflow automation and clear stakeholder communication.",
  candidate_name: "Demo Candidate",
};

const demoRun: OptimizationRunResponse = {
  id: "demo-finalized-run",
  status: "finalized",
  target_role: "Backend Developer",
  match_score_before: 58,
  match_score_after: 84,
  diff: [
    {
      section: "summary",
      before:
        "Software developer with Python and SQL experience. Built internal tools and supported React dashboards.",
      after:
        "Backend Developer candidate focused on Python, FastAPI, PostgreSQL and workflow automation with measurable API delivery.",
      reason: "Aligns the opening profile with target role language and high-value backend keywords.",
    },
    {
      section: "skills",
      before: "Python, SQL, React, internal tools",
      after: "Python, FastAPI, PostgreSQL, API ownership, automation, React",
      reason: "Moves job-critical keywords into the most visible skills area.",
    },
    {
      section: "experience",
      before: "Built internal tools and helped teams with dashboards.",
      after:
        "Delivered API automation workflows that reduced repeated handoffs and improved operational visibility.",
      reason: "Rewrites generic responsibilities as outcome-oriented evidence.",
    },
  ],
  highlighted_skills: ["Python", "FastAPI", "PostgreSQL", "automation", "API ownership"],
  ats_resume_markdown:
    "# Demo Candidate\n\n## Target Role\nBackend Developer\n\n## Professional Summary\nBackend Developer profile tailored to the job posting.\n\n## Core Skills\n- Python\n- FastAPI\n- PostgreSQL\n- automation\n- API ownership\n",
  application_brief:
    "General application note: the candidate's strongest aligned skills are Python, FastAPI, PostgreSQL, automation and API ownership.",
};

function statusLabel(status: OptimizationRunResponse["status"]) {
  const labels: Record<OptimizationRunResponse["status"], string> = {
    draft: "Draft",
    optimizing: "Optimizing",
    finalized: "Finalized",
    exported: "Exported",
    submitted: "Submitted",
    failed: "Failed",
  };
  return labels[status];
}

export function OptimizationReview() {
  const [run, setRun] = useState<OptimizationRunResponse>(demoRun);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const scoreGain = run.match_score_after - run.match_score_before;
  const optimizedSections = useMemo(() => run.diff.map((item) => item.section).join(", "), [run.diff]);

  async function handleRunOptimization() {
    setIsLoading(true);
    setError(null);

    try {
      const nextRun = await createOptimization(demoRequest);
      setRun(nextRun);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Optimization request failed.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="optimization-page">
      <section className="page-header">
        <div>
          <p className="eyebrow">QC-008</p>
          <h1>Optimization Trace</h1>
          <p>
            Autonomous CV rewrite completed for a backend role with inspectable field-level changes.
          </p>
        </div>
        <button className="primary-action" disabled={isLoading} onClick={handleRunOptimization}>
          {isLoading ? "Running" : "Run"}
        </button>
      </section>

      <section className="score-strip" aria-label="Optimization score summary">
        <div>
          <span>Status</span>
          <strong>{statusLabel(run.status)}</strong>
        </div>
        <div>
          <span>Before</span>
          <strong>{run.match_score_before}</strong>
        </div>
        <div>
          <span>After</span>
          <strong>{run.match_score_after}</strong>
        </div>
        <div>
          <span>Gain</span>
          <strong>+{scoreGain}</strong>
        </div>
      </section>

      {error ? (
        <section className="alert" role="alert">
          <strong>API unavailable</strong>
          <span>{error}</span>
        </section>
      ) : null}

      <div className="review-layout">
        <section className="diff-section" aria-labelledby="diff-heading">
          <div className="section-heading">
            <p className="eyebrow">Diff</p>
            <h2 id="diff-heading">Applied Changes</h2>
          </div>

          <div className="diff-list">
            {run.diff.map((item) => (
              <article className="diff-card" key={item.section}>
                <header>
                  <span>{item.section}</span>
                  <p>{item.reason}</p>
                </header>
                <div className="diff-columns">
                  <div>
                    <h3>Before</h3>
                    <p>{item.before}</p>
                  </div>
                  <div>
                    <h3>After</h3>
                    <p>{item.after}</p>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </section>

        <aside className="trace-panel" aria-label="Automation trace">
          <section>
            <p className="eyebrow">Trace</p>
            <h2>Automation Log</h2>
            <ol className="trace-list">
              <li>
                <span>1</span>
                <p>Job keywords loaded</p>
              </li>
              <li>
                <span>2</span>
                <p>Resume profile matched</p>
              </li>
              <li>
                <span>3</span>
                <p>Diff generated</p>
              </li>
              <li>
                <span>4</span>
                <p>Run finalized</p>
              </li>
            </ol>
          </section>

          <section>
            <p className="eyebrow">Package</p>
            <h2>Export Readiness</h2>
            <dl className="package-summary">
              <div>
                <dt>Run</dt>
                <dd>{run.id}</dd>
              </div>
              <div>
                <dt>Role</dt>
                <dd>{run.target_role}</dd>
              </div>
              <div>
                <dt>Sections</dt>
                <dd>{optimizedSections}</dd>
              </div>
              <div>
                <dt>Highlighted skills</dt>
                <dd>{run.highlighted_skills.join(", ")}</dd>
              </div>
            </dl>
          </section>

          <section>
            <p className="eyebrow">Application Brief</p>
            <h2>General Note</h2>
            <p>{run.application_brief}</p>
          </section>
        </aside>
      </div>

      <section className="ats-preview" aria-label="ATS friendly CV preview">
        <div className="section-heading">
          <p className="eyebrow">ATS CV</p>
          <h2>Generated Resume</h2>
        </div>
        <pre>{run.ats_resume_markdown}</pre>
      </section>
    </section>
  );
}
