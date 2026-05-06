// AI Optimized by Skills Agent: App shell mirrors the roadmap workflow without implementing feature internals yet.
const workflowSteps = [
  "Job Analysis",
  "Resume Parsing",
  "Match Scoring",
  "Autonomous CV Optimization",
  "Document Export",
  "Automatic Application",
  "Efficiency Metrics",
];

// AI Optimized by Skills Agent: Responsive first screen gives the team a usable skeleton for Sprint 1.
export function App() {
  return (
    <main className="app-shell">
      <section className="intro">
        <p className="eyebrow">Quick-Career MVP</p>
        <h1>Autonomous career workflow skeleton</h1>
        <p>
          Analyze job posts, optimize CVs, prepare applications and prove at least 50 percent
          repetitive-work reduction.
        </p>
      </section>

      <section className="workflow" aria-label="Quick-Career workflow">
        {workflowSteps.map((step, index) => (
          <article className="workflow-card" key={step}>
            <span>{String(index + 1).padStart(2, "0")}</span>
            <h2>{step}</h2>
          </article>
        ))}
      </section>
    </main>
  );
}
