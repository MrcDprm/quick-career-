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
          İş ilanlarını analiz et, CV'leri optimize et, başvuru paketlerini hazırla ve tekrarlı işleri
          en az yüzde 50 azalttığını ölçülebilir şekilde göster.
        </p>
      </section>

      <section className="workflow" aria-label="Quick-Career iş akışı">
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
            target: "Demo Şirket Backend Ekibi",
            resumeFileName: "quick-career-backend-gelistirici.md",
            coverLetter:
              "Aday, FastAPI, PostgreSQL ve API sahipliği deneyimiyle backend otomasyon rolüyle güçlü şekilde eşleşiyor.",
            mode: "platform",
          }}
          receipt={{
            status: "submitted",
            receipt: "QC-SUB-demo Demo Şirket Backend Ekibi hedefine platform adaptörüyle gönderildi.",
          }}
          onSubmit={() => undefined}
        />
      </section>

      <section className="demo-section">
        <EfficiencyDashboard
          metrics={[
            {
              workflowName: "İlanı oku ve özetle",
              manualSteps: 8,
              automatedSteps: 1,
              manualMinutes: 10,
              automatedMinutes: 1,
            },
            {
              workflowName: "ATS uyumlu CV optimize et",
              manualSteps: 20,
              automatedSteps: 4,
              manualMinutes: 30,
              automatedMinutes: 7,
            },
            {
              workflowName: "Başvuru bilgilendirme notu hazırla",
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
