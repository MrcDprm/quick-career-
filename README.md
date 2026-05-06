# Quick-Career

Quick-Career is an autonomous FastAPI + React system that analyzes job posts, optimizes CVs and prepares applications to reduce repetitive job-search work by at least 50 percent.

Current MVP supports saved personal profiles, education/certification/skills/experience capture, real public LinkedIn Easy Apply job scraping with filters, candidate briefing, keyword-based skill highlighting, ATS-friendly Markdown CV generation, export, sequential automatic submission and efficiency metrics.

## Final Demo Scenario

1. Save a candidate profile with personal info, education, certificates, skills, experience, projects and languages.
2. Provide LinkedIn job filters or a public LinkedIn jobs search URL; the backend normalizes it to Easy Apply only.
3. Run `/api/autopilot/apply`.
4. The system filters only LinkedIn Easy Apply jobs, creates an ATS-friendly CV for each job and submits applications in order.

## Project Layout

```text
quick-career/
  ARCHITECTURE.md
  ROADMAP.md
  .clauderules
  backend/
  frontend/
  tests/
```

## Local Skeleton

Backend:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --app-dir src
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Repository checks:

```bash
pytest tests
```
