# SoulSkill Backend — Core API

This folder is an independently deployable FastAPI service for the first
mid-career workflow: import an existing resume, compare it with a target job,
and produce transparent, fact-preserving tailoring guidance.

## Included in this milestone

- GET /health — service health.
- POST /api/resume/parse — extract selectable text from PDF, DOCX and TXT.
- POST /api/resume/job-fit — compare existing resume evidence with a job description.
- Uploads and request bodies are processed in memory and are not persisted.
- Missing skills and qualifications are never inserted into the tailored resume.

Scanned PDFs are not OCR-processed in this milestone. The user is asked to provide
a text-based PDF, DOCX or TXT file. The upload ceiling is 4 MB to leave headroom
under serverless request-body limits.

## Run locally

From the repository root:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r backend/requirements-dev.txt
    uvicorn backend.app:app --reload --port 8000

Then open http://127.0.0.1:8000/docs.

## Test

    pytest tests/test_resume_job_service.py tests/test_backend_api.py -q

## Vercel project

Create a separate Vercel project linked to this repository with:

- Project name: soulskill-api
- Root Directory: backend
- Framework preset: FastAPI (or Python, if auto-detected)
- Install Command: default (pip install -r requirements.txt)

The app.py file is the FastAPI entrypoint. Configure SOULSKILL_ENV=production.
For direct cross-origin browser access, set SOULSKILL_CORS_ORIGINS to the exact
front-end origins. The preferred PWA integration is a same-origin Vercel rewrite
from the Flutter project to this API project.

## Security and rollout boundary

This is a staging/pilot API, not a production SaaS backend. It has no authentication,
rate limiting, account ownership, cloud database, resume history or AI provider.
Do not upload highly sensitive documents until authentication, abuse controls,
privacy notices, deletion and retention policies have been implemented. Never
place provider credentials in Flutter or in a public repository.
