// AI Optimized by Skills Agent: Otonom optimizasyon izleme ekranı manuel onay kapısı olmadan inceleme sağlar.
import { useMemo, useState } from "react";

import {
  createOptimization,
  type OptimizationRequest,
  type OptimizationRunResponse,
} from "../../api/optimizations";

const demoRequest: OptimizationRequest = {
  target_role: "Backend Geliştirici",
  resume_text:
    "Python ve SQL deneyimine sahip yazılım geliştirici. Operasyon ekipleri için dahili araçlar ve React panoları geliştirdi.",
  job_keywords: ["Python", "FastAPI", "PostgreSQL", "otomasyon", "API sahipliği"],
  candidate_brief:
    "Aday API sahipliği, iş akışı otomasyonu ve net paydaş iletişimini öne çıkarmak istiyor.",
  candidate_name: "Demo Aday",
};

const demoRun: OptimizationRunResponse = {
  id: "demo-finalized-run",
  status: "finalized",
  target_role: "Backend Geliştirici",
  match_score_before: 58,
  match_score_after: 84,
  diff: [
    {
      section: "summary",
      before:
        "Python ve SQL deneyimine sahip yazılım geliştirici. Dahili araçlar ve React panoları geliştirdi.",
      after:
        "Python, FastAPI, PostgreSQL ve iş akışı otomasyonu odağında ölçülebilir API teslimatı yapan backend geliştirici.",
      reason: "Açılış profilini hedef rol dili ve yüksek değerli backend anahtar kelimeleriyle hizalar.",
    },
    {
      section: "skills",
      before: "Python, SQL, React, dahili araçlar",
      after: "Python, FastAPI, PostgreSQL, API sahipliği, otomasyon, React",
      reason: "İlan açısından kritik anahtar kelimeleri en görünür yetenek alanına taşır.",
    },
    {
      section: "experience",
      before: "Dahili araçlar geliştirdi ve ekiplere panolarda destek oldu.",
      after:
        "Tekrarlanan devir teslimleri azaltan ve operasyon görünürlüğünü artıran API otomasyon iş akışları geliştirdi.",
      reason: "Genel sorumlulukları sonuç odaklı kanıta dönüştürür.",
    },
  ],
  highlighted_skills: ["Python", "FastAPI", "PostgreSQL", "otomasyon", "API sahipliği"],
  ats_resume_markdown:
    "# Demo Aday\n\n## Hedef Rol\nBackend Geliştirici\n\n## Profesyonel Özet\nBackend Geliştirici profili hedef ilana göre uyarlandı.\n\n## Temel Yetenekler\n- Python\n- FastAPI\n- PostgreSQL\n- otomasyon\n- API sahipliği\n",
  application_brief:
    "Genel bilgilendirme: adayın ilanla en güçlü eşleşen yetenekleri Python, FastAPI, PostgreSQL, otomasyon ve API sahipliği.",
};

// AI Optimized by Skills Agent: API durumlarını Türkçe ve jüri tarafından okunabilir etiketlere çevirir.
function statusLabel(status: OptimizationRunResponse["status"]) {
  const labels: Record<OptimizationRunResponse["status"], string> = {
    draft: "Taslak",
    optimizing: "Optimize ediliyor",
    finalized: "Tamamlandı",
    exported: "Çıktı alındı",
    submitted: "Gönderildi",
    failed: "Başarısız",
  };
  return labels[status];
}

// AI Optimized by Skills Agent: Diff bölüm adlarını Türkçeleştirir.
function sectionLabel(section: string) {
  const labels: Record<string, string> = {
    summary: "Özet",
    skills: "Yetenekler",
    experience: "Deneyim",
  };
  return labels[section] ?? section;
}

export function OptimizationReview() {
  const [run, setRun] = useState<OptimizationRunResponse>(demoRun);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const scoreGain = run.match_score_after - run.match_score_before;
  const optimizedSections = useMemo(
    () => run.diff.map((item) => sectionLabel(item.section)).join(", "),
    [run.diff],
  );

  async function handleRunOptimization() {
    setIsLoading(true);
    setError(null);

    try {
      const nextRun = await createOptimization(demoRequest);
      setRun(nextRun);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Optimizasyon isteği başarısız oldu.");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <section className="optimization-page">
      <section className="page-header">
        <div>
          <p className="eyebrow">QC-008</p>
          <h1>Optimizasyon İz Kaydı</h1>
          <p>Backend rolü için otonom CV yeniden yazımı, alan bazlı değişikliklerle birlikte tamamlandı.</p>
        </div>
        <button className="primary-action" disabled={isLoading} onClick={handleRunOptimization}>
          {isLoading ? "Çalışıyor" : "Çalıştır"}
        </button>
      </section>

      <section className="score-strip" aria-label="Optimizasyon skor özeti">
        <div>
          <span>Durum</span>
          <strong>{statusLabel(run.status)}</strong>
        </div>
        <div>
          <span>Önce</span>
          <strong>{run.match_score_before}</strong>
        </div>
        <div>
          <span>Sonra</span>
          <strong>{run.match_score_after}</strong>
        </div>
        <div>
          <span>Kazanım</span>
          <strong>+{scoreGain}</strong>
        </div>
      </section>

      {error ? (
        <section className="alert" role="alert">
          <strong>API'ye ulaşılamadı</strong>
          <span>{error}</span>
        </section>
      ) : null}

      <div className="review-layout">
        <section className="diff-section" aria-labelledby="diff-heading">
          <div className="section-heading">
            <p className="eyebrow">Fark</p>
            <h2 id="diff-heading">Uygulanan Değişiklikler</h2>
          </div>

          <div className="diff-list">
            {run.diff.map((item) => (
              <article className="diff-card" key={item.section}>
                <header>
                  <span>{sectionLabel(item.section)}</span>
                  <p>{item.reason}</p>
                </header>
                <div className="diff-columns">
                  <div>
                    <h3>Önce</h3>
                    <p>{item.before}</p>
                  </div>
                  <div>
                    <h3>Sonra</h3>
                    <p>{item.after}</p>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </section>

        <aside className="trace-panel" aria-label="Otomasyon iz kaydı">
          <section>
            <p className="eyebrow">İz</p>
            <h2>Otomasyon Günlüğü</h2>
            <ol className="trace-list">
              <li>
                <span>1</span>
                <p>İlan anahtar kelimeleri yüklendi</p>
              </li>
              <li>
                <span>2</span>
                <p>CV profili eşleştirildi</p>
              </li>
              <li>
                <span>3</span>
                <p>Fark kaydı üretildi</p>
              </li>
              <li>
                <span>4</span>
                <p>Çalışma tamamlandı</p>
              </li>
            </ol>
          </section>

          <section>
            <p className="eyebrow">Paket</p>
            <h2>Çıktı Hazırlığı</h2>
            <dl className="package-summary">
              <div>
                <dt>Çalışma</dt>
                <dd>{run.id}</dd>
              </div>
              <div>
                <dt>Rol</dt>
                <dd>{run.target_role}</dd>
              </div>
              <div>
                <dt>Bölümler</dt>
                <dd>{optimizedSections}</dd>
              </div>
              <div>
                <dt>Öne çıkan yetenekler</dt>
                <dd>{run.highlighted_skills.join(", ")}</dd>
              </div>
            </dl>
          </section>

          <section>
            <p className="eyebrow">Başvuru Bilgisi</p>
            <h2>Genel Not</h2>
            <p>{run.application_brief}</p>
          </section>
        </aside>
      </div>

      <section className="ats-preview" aria-label="ATS uyumlu CV önizlemesi">
        <div className="section-heading">
          <p className="eyebrow">ATS CV</p>
          <h2>Oluşturulan CV</h2>
        </div>
        <pre>{run.ats_resume_markdown}</pre>
      </section>
    </section>
  );
}
