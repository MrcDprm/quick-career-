// AI Optimized by Skills Agent: App shell mirrors the roadmap workflow without implementing feature internals yet.
import { AppShell } from "./components/AppShell";
import { workflowSteps } from "./types/workflowMetadata";

// AI Optimized by Skills Agent: Responsive first screen gives the team a usable skeleton for Sprint 1.
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
    </AppShell>
  );
}
