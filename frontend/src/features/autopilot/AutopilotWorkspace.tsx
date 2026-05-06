// AI Optimized by Skills Agent: Profile capture and LinkedIn autonomous application workspace.
import { useMemo, useState } from "react";

import {
  runAutopilotApply,
  type AutopilotApplyResponse,
  type CandidateProfilePayload,
} from "../../api/autopilot";
import "./autopilotWorkspace.css";

// AI Optimized by Skills Agent: Splits comma/newline text into stable profile arrays.
function splitList(value: string) {
  return value
    .split(/[,\n]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

// AI Optimized by Skills Agent: Builds a rich profile object from compact hackathon form fields.
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
      degree: "Education / Training",
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
      description: `Project evidence for ${entry}`,
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
  fullName: "Demo Candidate",
  email: "candidate@example.com",
  phone: "+90 555 000 00 00",
  location: "Istanbul, Turkey",
  links: "https://github.com/demo, https://linkedin.com/in/demo",
  summary:
    "Full stack developer focused on FastAPI, React, PostgreSQL and workflow automation for business teams.",
  skills: "Python, FastAPI, React, TypeScript, PostgreSQL, automation, API ownership",
  education: "Computer Engineering, AI-Augmented Development Training",
  certifications: "FastAPI Foundations, React TypeScript, SQL for Developers",
  currentTitle: "Software Developer",
  currentCompany: "Demo Labs",
  experienceHighlights:
    "Built FastAPI services\nCreated React dashboards\nReduced repetitive reporting work with automation",
  projects: "Quick-Career, Workflow Automation Dashboard",
  languages: "Turkish, English",
  jobKeywords: "Python, FastAPI, React, PostgreSQL, automation",
  linkedinSearchUrl: "",
  maxApplications: 2,
};

// AI Optimized by Skills Agent: Usable first-screen workflow for profile save and autonomous applications.
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
        },
        max_applications: form.maxApplications,
        submission_mode: "mock",
      });
      setResult(response);
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Autopilot workflow failed.");
    } finally {
      setIsRunning(false);
    }
  }

  return (
    <section className="autopilot-workspace" aria-label="LinkedIn autonomous application workflow">
      <header className="autopilot-header">
        <div>
          <p className="eyebrow">Final workflow</p>
          <h2>Profile to LinkedIn applications</h2>
          <p>
            Save personal info, education, certifications, skills and experience, then scrape filtered
            LinkedIn jobs and apply with ATS-friendly CVs.
          </p>
        </div>
        <button type="button" disabled={isRunning} onClick={handleRunAutopilot}>
          {isRunning ? "Running" : "Run autopilot"}
        </button>
      </header>

      <div className="autopilot-grid">
        <form className="profile-form">
          <label>
            Full name
            <input value={form.fullName} onChange={(event) => updateField("fullName", event.target.value)} />
          </label>
          <label>
            Email
            <input value={form.email} onChange={(event) => updateField("email", event.target.value)} />
          </label>
          <label>
            Phone
            <input value={form.phone} onChange={(event) => updateField("phone", event.target.value)} />
          </label>
          <label>
            Location
            <input value={form.location} onChange={(event) => updateField("location", event.target.value)} />
          </label>
          <label className="wide">
            Links
            <textarea value={form.links} onChange={(event) => updateField("links", event.target.value)} />
          </label>
          <label className="wide">
            General briefing
            <textarea value={form.summary} onChange={(event) => updateField("summary", event.target.value)} />
          </label>
          <label className="wide">
            Skills
            <textarea value={form.skills} onChange={(event) => updateField("skills", event.target.value)} />
          </label>
          <label>
            Education
            <textarea value={form.education} onChange={(event) => updateField("education", event.target.value)} />
          </label>
          <label>
            Certifications
            <textarea
              value={form.certifications}
              onChange={(event) => updateField("certifications", event.target.value)}
            />
          </label>
          <label>
            Current title
            <input
              value={form.currentTitle}
              onChange={(event) => updateField("currentTitle", event.target.value)}
            />
          </label>
          <label>
            Current company
            <input
              value={form.currentCompany}
              onChange={(event) => updateField("currentCompany", event.target.value)}
            />
          </label>
          <label className="wide">
            Experience highlights
            <textarea
              value={form.experienceHighlights}
              onChange={(event) => updateField("experienceHighlights", event.target.value)}
            />
          </label>
          <label>
            Projects
            <textarea value={form.projects} onChange={(event) => updateField("projects", event.target.value)} />
          </label>
          <label>
            Languages
            <textarea value={form.languages} onChange={(event) => updateField("languages", event.target.value)} />
          </label>
          <label className="wide">
            LinkedIn search URL
            <input
              value={form.linkedinSearchUrl}
              placeholder="Optional public LinkedIn jobs search URL"
              onChange={(event) => updateField("linkedinSearchUrl", event.target.value)}
            />
          </label>
          <label>
            Job keywords
            <textarea
              value={form.jobKeywords}
              onChange={(event) => updateField("jobKeywords", event.target.value)}
            />
          </label>
          <label>
            Max applications
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
            <p className="eyebrow">Saved profile preview</p>
            <h3>{profilePreview.personal.full_name}</h3>
            <p>{profilePreview.summary}</p>
            <strong>{profilePreview.skills.length} skills ready</strong>
          </section>

          {error ? (
            <section className="autopilot-error" role="alert">
              <strong>API unavailable</strong>
              <p>{error}</p>
            </section>
          ) : null}

          {result ? (
            <section>
              <p className="eyebrow">Applications</p>
              <h3>{result.total_applications} submitted</h3>
              <p>{result.summary}</p>
              <div className="application-results">
                {result.applications.map((application) => (
                  <article key={application.submission.receipt}>
                    <strong>{application.job.title}</strong>
                    <span>{application.job.company}</span>
                    <small>{application.optimization.highlighted_skills.join(", ")}</small>
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
