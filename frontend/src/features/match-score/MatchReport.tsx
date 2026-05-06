// AI Optimized by Skills Agent: Match report UI displays fit score, strengths and gaps for Ceyda's QC-006 scope.
import "./matchReport.css";

export type MatchReportData = {
  score: number;
  role: string;
  strongMatches: string[];
  missingSkills: string[];
  priorities: string[];
};

type MatchReportProps = {
  report: MatchReportData;
  isLoading?: boolean;
  errorMessage?: string;
  onRetry?: () => void;
};

// AI Optimized by Skills Agent: Keeps scoring display readable while backend scoring evolves independently.
function getScoreLabel(score: number) {
  if (score >= 80) {
    return "Güçlü eşleşme";
  }

  if (score >= 55) {
    return "Umut vadeden eşleşme";
  }

  return "Hedefleme gerekiyor";
}

// AI Optimized by Skills Agent: Reusable list section prevents repeated markup across gaps and strengths.
function InsightList({ title, items }: { title: string; items: string[] }) {
  return (
    <section className="match-panel" aria-label={title}>
      <h3>{title}</h3>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

// AI Optimized by Skills Agent: Feature-complete state handling covers loading, error and populated reports.
export function MatchReport({ report, isLoading = false, errorMessage, onRetry }: MatchReportProps) {
  if (isLoading) {
    return <section className="match-report status">İlan ve CV uyumu analiz ediliyor...</section>;
  }

  if (errorMessage) {
    return (
      <section className="match-report status" role="alert">
        <p>{errorMessage}</p>
        {onRetry ? (
          <button type="button" onClick={onRetry}>
            Tekrar dene
          </button>
        ) : null}
      </section>
    );
  }

  return (
    <section className="match-report" aria-label="Eşleşme raporu">
      <header className="match-summary">
        <div>
          <p className="match-eyebrow">Hedef rol</p>
          <h2>{report.role}</h2>
        </div>
        <div className="score-card" aria-label={`Eşleşme skoru yüzde ${report.score}`}>
          <strong>{report.score}%</strong>
          <span>{getScoreLabel(report.score)}</span>
        </div>
      </header>

      <div className="match-grid">
        <InsightList title="Güçlü eşleşmeler" items={report.strongMatches} />
        <InsightList title="Eksik yetenekler" items={report.missingSkills} />
        <InsightList title="Optimizasyon öncelikleri" items={report.priorities} />
      </div>
    </section>
  );
}
