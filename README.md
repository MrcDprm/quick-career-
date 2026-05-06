# Quick-Career

Quick-Career is an autonomous FastAPI + React system that analyzes job posts, optimizes CVs and prepares applications to reduce repetitive job-search work by at least 50 percent.

Current MVP supports pasted job text, public job URL scraping, candidate general briefing, keyword-based skill highlighting, ATS-friendly Markdown CV generation, export, automatic submission and efficiency metrics.

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
