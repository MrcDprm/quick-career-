// AI Optimized by Skills Agent: Dashboard proves repetitive-work reduction against manual baselines.
import "./efficiencyDashboard.css";

export type EfficiencyMetric = {
  workflowName: string;
  manualSteps: number;
  automatedSteps: number;
  manualMinutes: number;
  automatedMinutes: number;
};

type EfficiencyDashboardProps = {
  metrics: EfficiencyMetric[];
};

// AI Optimized by Skills Agent: Shared formula mirrors ARCHITECTURE.md reduction calculation.
function calculateReduction(manualEffort: number, automatedEffort: number) {
  if (manualEffort <= 0) {
    return 0;
  }

  return Math.round(((manualEffort - automatedEffort) / manualEffort) * 100);
}

// AI Optimized by Skills Agent: Aggregates dashboard totals for the hackathon success criterion.
function summarize(metrics: EfficiencyMetric[]) {
  const manualSteps = metrics.reduce((total, metric) => total + metric.manualSteps, 0);
  const automatedSteps = metrics.reduce((total, metric) => total + metric.automatedSteps, 0);
  const manualMinutes = metrics.reduce((total, metric) => total + metric.manualMinutes, 0);
  const automatedMinutes = metrics.reduce((total, metric) => total + metric.automatedMinutes, 0);

  return {
    manualSteps,
    automatedSteps,
    manualMinutes,
    automatedMinutes,
    stepReduction: calculateReduction(manualSteps, automatedSteps),
    timeReduction: calculateReduction(manualMinutes, automatedMinutes),
  };
}

// AI Optimized by Skills Agent: Renders time and step reduction in a dense, jury-readable surface.
export function EfficiencyDashboard({ metrics }: EfficiencyDashboardProps) {
  const summary = summarize(metrics);
  const targetReached = summary.timeReduction >= 50 && summary.stepReduction >= 50;

  return (
    <section className="efficiency-dashboard" aria-label="Efficiency metrics dashboard">
      <header className="efficiency-header">
        <div>
          <p className="efficiency-eyebrow">Efficiency proof</p>
          <h2>{targetReached ? "50%+ target reached" : "Target in progress"}</h2>
        </div>
        <div className="reduction-score">
          <strong>{summary.timeReduction}%</strong>
          <span>time reduction</span>
        </div>
      </header>

      <div className="summary-grid">
        <article>
          <span>Manual time</span>
          <strong>{summary.manualMinutes} min</strong>
        </article>
        <article>
          <span>Automated time</span>
          <strong>{summary.automatedMinutes} min</strong>
        </article>
        <article>
          <span>Step reduction</span>
          <strong>{summary.stepReduction}%</strong>
        </article>
      </div>

      <div className="metric-table" role="table" aria-label="Workflow efficiency metrics">
        <div className="metric-row metric-head" role="row">
          <span>Workflow</span>
          <span>Manual</span>
          <span>Automated</span>
          <span>Reduction</span>
        </div>
        {metrics.map((metric) => (
          <div className="metric-row" role="row" key={metric.workflowName}>
            <span>{metric.workflowName}</span>
            <span>
              {metric.manualMinutes} min / {metric.manualSteps} steps
            </span>
            <span>
              {metric.automatedMinutes} min / {metric.automatedSteps} steps
            </span>
            <strong>{calculateReduction(metric.manualMinutes, metric.automatedMinutes)}%</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
