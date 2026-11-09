# SoulSkill Backend — Core API

This folder contains the independently deployable FastAPI service for SoulSkill.

## Current capabilities

- `GET /health` — service health.
- `POST /api/resume/parse` — extract selectable text from PDF, DOCX and TXT in memory.
- `POST /api/resume/job-fit` — deterministic, explainable keyword alignment that never inserts missing skills.
- `GET /api/v1/me` — verified Supabase account identity.
- `GET/PATCH /api/v1/profile` — read and update the authenticated user's career profile.

Resume import and job-fit are currently stateless. The account/profile endpoints require Supabase Auth and use a new request-scoped client carrying the user's access token, so Postgres RLS evaluates the actual user identity.

## Run locally

From the repository root:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r backend/requirements-dev.txt
    uvicorn backend.app:app --reload --port 8000

Then open http://127.0.0.1:8000/docs.

## Test

    pytest tests/test_resume_job_service.py tests/test_backend_api.py tests/test_account_api.py -q

## Supabase setup

1. Create a Supabase project for the intended environment.
2. Apply the versioned migration in `supabase/migrations/` using the Supabase CLI or SQL editor.
3. Configure the API runtime with:
   - `SUPABASE_URL`
   - `SUPABASE_PUBLISHABLE_KEY` (or legacy `SUPABASE_ANON_KEY`)
4. Configure Flutter with only the Supabase project URL and publishable key. Never put a service-role/secret key in the app.
5. Enable the desired email/password and OAuth providers in Supabase Auth and verify redirect URLs for web and Android.

The migration creates personal workspaces and candidate profiles on signup. Row Level Security is enabled and grants are explicit. It is safe to apply to a fresh project; review the migration against any existing production schema before applying it to a populated project.

## Vercel project

The backend is deployed separately from the Flutter PWA:

- Project name: `soulskill-api`
- Root Directory: `backend`
- Framework preset: FastAPI (or Python, if auto-detected)
- Runtime: Python 3.12

For the protected preview API, keep the Vercel protection bypass secret server-side. The PWA same-origin proxy must forward the user's Supabase bearer token when authenticated endpoints are added.

## Security and rollout boundary

This is still a controlled preview/pilot backend, not a production SaaS service. Authentication and profile persistence are the first cloud-backed slice. Resume uploads remain stateless; no resume files or raw job descriptions are stored. Rate limiting, abuse controls, private document storage, account export/deletion workflows, consent records, billing/entitlements, production monitoring and a reviewed privacy notice remain release gates.

Do not expose provider credentials in Flutter or commit secrets to the repository.
