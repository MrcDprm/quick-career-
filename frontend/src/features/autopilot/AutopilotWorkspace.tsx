// AI Optimized by Skills Agent: Profil kaydı ve LinkedIn Kolay Başvuru otomasyon çalışma alanı.
import { useMemo, useState } from "react";

import {
  runAutopilotApply,
  type AutopilotApplyResponse,
  type CandidateProfilePayload,
} from "../../api/autopilot";
import "./autopilotWorkspace.css";

// AI Optimized by Skills Agent: Virgül/satır sonu ayrımlı metni kararlı profil listelerine çevirir.
function splitList(value: string) {
  return value
    .split(/[,\n]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

// AI Optimized by Skills Agent: Hackathon form alanlarından eksiksiz aday profili üretir.
function buildProfile(form: ProfileFormState): CandidateProfilePayload {
  const skills = splitList(form.skills);
  return {
    personal: {
      full_name: form.fullName,
      email: form.email,
      phone: form.phone,
      location: form.location,
      links: splitList(form.links),
    },
    summary: form.summary,
    skills,
    education: splitList(form.education).map((entry) => ({
      school: entry,
      degree: "Eğitim / Sertifika",
    })),
    certifications: splitList(form.certifications).map((entry) => ({ name: entry })),
    experiences: [
      {
        title: form.currentTitle,
        company: form.currentCompany,
        highlights: splitList(form.experienceHighlights),
      },
    ],
    projects: splitList(form.projects).map((entry) => ({
      name: entry,
      description: `${entry} için proje kanıtı`,
      technologies: skills,
    })),
    languages: splitList(form.languages),
  };
}

type ProfileFormState = {
  fullName: string;
  email: string;
  phone: string;
  location: string;
  links: string;
  summary: string;
  skills: string;
  education: string;
  certifications: string;
  currentTitle: string;
  currentCompany: string;
  experienceHighlights: string;
  projects: string;
  languages: string;
  jobKeywords: string;
  linkedinSearchUrl: string;
  maxApplications: number;
};

const initialForm: ProfileFormState = {
  fullName: "Demo Aday",
  email: "candidate@example.com",
  phone: "+90 555 000 00 00",
  location: "İstanbul, Türkiye",
  links: "https://github.com/demo, https://linkedin.com/in/demo",
  summary:
    "FastAPI, React, PostgreSQL ve iş akışı otomasyonu üzerine çalışan full stack geliştirici.",
  skills: "Python, FastAPI, React, TypeScript, PostgreSQL, otomasyon, API sahipliği",
  education: "Bilgisayar Mühendisliği, AI Destekli Geliştirme Eğitimi",
  certifications: "FastAPI Temelleri, React TypeScript, Geliştiriciler için SQL",
  currentTitle: "Yazılım Geliştirici",
  currentCompany: "Demo Labs",
  experienceHighlights:
    "FastAPI servisleri geliştirdi\nReact panoları oluşturdu\nOtomasyonla tekrarlı raporlama işlerini azalttı",
  projects: "Quick-Career, İş Akışı Otomasyon Panosu",
  languages: "Türkçe, İngilizce",
  jobKeywords: "Python, FastAPI, React, PostgreSQL, automation",
  linkedinSearchUrl: "",
  maxApplications: 2,
};

// AI Optimized by Skills Agent: Profil kaydı, gerçek ilan çekme, ATS CV ve başvuru akışını tek ekranda çalıştırır.
export function AutopilotWorkspace() {
  const [form, setForm] = useState<ProfileFormState>(initialForm);
  const [result, setResult] = useState<AutopilotApplyResponse | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const profilePreview = useMemo(() => buildProfile(form), [form]);

  function updateField<TField extends keyof ProfileFormState>(field: TField, value: ProfileFormState[TField]) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  async function handleRunAutopilot() {
    setIsRunning(true);
    setError(null);

    try {
      const response = await runAutopilotApply({
        profile: profilePreview,
        filters: {
          keywords: splitList(form.jobKeywords),
          location: form.location,
          remote_only: false,
          limit: form.maxApplications,
          linkedin_search_url: form.linkedinSearchUrl || undefined,
          minimum_skill_matches: 1,
          easy_apply_only: true,
        },
        max_applications: form.maxApplications,
        submission_mode: "platform",
      });
      setResult(response);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Otomatik başvuru akışı başarısız oldu.");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <section className="autopilot-workspace" aria-label="LinkedIn Kolay Başvuru otomasyon akışı">
      <header className="autopilot-header">
        <div>
          <p className="eyebrow">Final akış</p>
          <h2>Profil bilgilerini LinkedIn başvurularına dönüştür</h2>
          <p>
            Kişisel bilgileri, eğitimleri, sertifikaları, yetenekleri ve deneyimleri kaydet; yalnızca LinkedIn
            Kolay Başvuru ilanlarını çek ve her ilana göre ATS uyumlu CV paketi hazırla.
          </p>
        </div>
        <button type="button" disabled={isRunning} onClick={handleRunAutopilot}>
          {isRunning ? "Çalışıyor" : "Otomatik akışı çalıştır"}
        </button>
      </header>

      <div className="autopilot-grid">
        <form className="profile-form" aria-label="Aday profil formu">
          <label>
            Ad Soyad
            <input value={form.fullName} onChange={(event) => updateField("fullName", event.target.value)} />
          </label>
          <label>
            E-posta
            <input value={form.email} onChange={(event) => updateField("email", event.target.value)} />
          </label>
          <label>
            Telefon
            <input value={form.phone} onChange={(event) => updateField("phone", event.target.value)} />
          </label>
          <label>
            Konum
            <input value={form.location} onChange={(event) => updateField("location", event.target.value)} />
          </label>
          <label className="wide">
            Bağlantılar
            <textarea value={form.links} onChange={(event) => updateField("links", event.target.value)} />
          </label>
          <label className="wide">
            Genel bilgilendirme
            <textarea value={form.summary} onChange={(event) => updateField("summary", event.target.value)} />
          </label>
          <label className="wide">
            Yetenekler
            <textarea value={form.skills} onChange={(event) => updateField("skills", event.target.value)} />
          </label>
          <label>
            Eğitimler
            <textarea value={form.education} onChange={(event) => updateField("education", event.target.value)} />
          </label>
          <label>
            Sertifikalar
            <textarea
              value={form.certifications}
              onChange={(event) => updateField("certifications", event.target.value)}
            />
          </label>
          <label>
            Mevcut unvan
            <input
              value={form.currentTitle}
              onChange={(event) => updateField("currentTitle", event.target.value)}
            />
          </label>
          <label>
            Mevcut şirket
            <input
              value={form.currentCompany}
              onChange={(event) => updateField("currentCompany", event.target.value)}
            />
          </label>
          <label className="wide">
            Deneyim öne çıkanları
            <textarea
              value={form.experienceHighlights}
              onChange={(event) => updateField("experienceHighlights", event.target.value)}
            />
          </label>
          <label>
            Projeler
            <textarea value={form.projects} onChange={(event) => updateField("projects", event.target.value)} />
          </label>
          <label>
            Diller
            <textarea value={form.languages} onChange={(event) => updateField("languages", event.target.value)} />
          </label>
          <label className="wide">
            LinkedIn ilan arama URL'i
            <input
              value={form.linkedinSearchUrl}
              placeholder="Boş bırakılırsa anahtar kelimelerle gerçek Kolay Başvuru ilanları çekilir"
              onChange={(event) => updateField("linkedinSearchUrl", event.target.value)}
            />
          </label>
          <label>
            İlan anahtar kelimeleri
            <textarea
              value={form.jobKeywords}
              onChange={(event) => updateField("jobKeywords", event.target.value)}
            />
          </label>
          <label>
            Maksimum başvuru
            <input
              type="number"
              min={1}
              max={10}
              value={form.maxApplications}
              onChange={(event) => updateField("maxApplications", Number(event.target.value))}
            />
          </label>
        </form>

        <aside className="autopilot-preview">
          <section>
            <p className="eyebrow">Kayıtlı profil önizlemesi</p>
            <h3>{profilePreview.personal.full_name}</h3>
            <p>{profilePreview.summary}</p>
            <strong>{profilePreview.skills.length} yetenek hazır</strong>
          </section>

          {error ? (
            <section className="autopilot-error" role="alert">
              <strong>API'ye ulaşılamadı</strong>
              <p>{error}</p>
            </section>
          ) : null}

          {result ? (
            <section>
              <p className="eyebrow">Başvurular</p>
              <h3>{result.total_applications} başvuru gönderildi</h3>
              <p>{result.summary}</p>
              <div className="application-results">
                {result.applications.map((application) => (
                  <article key={application.submission.receipt}>
                    <strong>{application.job.title}</strong>
                    <span>{application.job.company}</span>
                    <small>
                      {application.job.easy_apply ? "Kolay Başvuru" : "Kolay Başvuru değil"} ·{" "}
                      {application.optimization.highlighted_skills.join(", ")}
                    </small>
                    <a href={application.job.source_url} target="_blank" rel="noreferrer">
                      İlanı aç
                    </a>
                    <p>{application.submission.receipt}</p>
                  </article>
                ))}
              </div>
            </section>
          ) : null}
        </aside>
      </div>
    </section>
  );
}
