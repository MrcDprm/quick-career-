# Quick-Career

Quick-Career is a FastAPI + React tool I built for my own job search. It reads job posts, compares them with my profile and prepares a tailored, ATS-friendly CV for each one.

What it does:
- Stores a candidate profile: education, certificates, skills, experience, projects and languages
- Pulls job posts from a public LinkedIn job search URL, with filters
- Highlights the skills each post asks for and shows which ones the profile covers
- Generates an ATS-friendly CV in Markdown for each post and exports it
- Tracks how much time the process saves

The last step, sending the prepared applications one by one, was an experiment for personal use.

## Demo Scenario

1. Save a candidate profile.
2. Give a LinkedIn job search URL or a set of filters.
3. Call `/api/autopilot/apply`.
4. The system picks the matching posts, creates a tailored CV for each and runs the application steps in order.

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
