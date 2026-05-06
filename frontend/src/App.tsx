// AI Optimized by Skills Agent: App shell mirrors the roadmap workflow without implementing feature internals yet.
import { AppShell } from "./components/AppShell";
import { ApplicationSubmissionPanel } from "./features/application-submit";
import { AutopilotWorkspace } from "./features/autopilot";
import { EfficiencyDashboard } from "./features/metrics-dashboard";
import { OptimizationReview } from "./features/optimization-review";
import { workflowSteps } from "./types/workflowMetadata";

export function App() {
  return (
    <AppShell>
      <section className="intro">
        <p>
          Analyze job posts, optimize CVs, prepare applications and prove at least 50 percent
          repetitive-work reduction.
        </p>
      </section>

      <section className="workflow" aria-label="Quick-Career workflow">
        {workflowSteps.map((step, index) => (
          <article className="workflow-card" key={step.stage}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <h2>{step.label}</h2>
            <p>{step.description}</p>
          </article>
        ))}
      </section>

      <AutopilotWorkspace />

      <OptimizationReview />

      <section className="demo-section">
        <ApplicationSubmissionPanel
          applicationPackage={{
            target: "Demo Company Backend Team",
            resumeFileName: "quick-career-backend-developer.md",
            coverLetter:
              "The candidate matches the backend automation role with FastAPI, PostgreSQL and API ownership experience.",
            mode: "mock",
          }}
          receipt={{
            status: "submitted",
            receipt: "QC-SUB-demo submitted to Demo Company Backend Team via mock adapter.",
          }}
          onSubmit={() => undefined}
        />
      </section>

      <section className="demo-section">
        <EfficiencyDashboard
          metrics={[
            {
              workflowName: "Read and summarize job post",
              manualSteps: 8,
              automatedSteps: 1,
              manualMinutes: 10,
              automatedMinutes: 1,
            },
            {
              workflowName: "Optimize ATS CV",
              manualSteps: 20,
              automatedSteps: 4,
              manualMinutes: 30,
              automatedMinutes: 7,
            },
            {
              workflowName: "Prepare application note",
              manualSteps: 12,
              automatedSteps: 2,
              manualMinutes: 20,
              automatedMinutes: 2,
            },
          ]}
        />
      </section>
    </AppShell>
  );
}
