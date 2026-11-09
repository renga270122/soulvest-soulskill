# SoulSkill — Product & Engineering Roadmap

## Product goal
Build a trustworthy, accessible career platform for mid-career and early-career candidates, with a separate recruiter workspace. Help candidates present verifiable evidence of skills and impact, tailor applications to a role, and manage their search. Help recruiters discover and assess candidates with consent-based, explainable tools.

No feature should promise an interview, job, ATS pass, or hiring outcome.

## Candidate experience
1. Resume workspace: multiple resumes, structured work history, education, projects, certifications, skills, languages, links, achievements, measurable outcomes, career gaps/context (optional).
2. Import: PDF, DOCX and TXT parsing; editable extraction review; preserve original file only with explicit consent.
3. AI writing assistant: summary, achievement bullets, role-specific tailoring, cover letters, recruiter messages, LinkedIn sections, interview practice. Suggestions must be editable, evidence-grounded, and clearly labelled as AI-generated.
4. Job alignment: job-description parsing, must-have/preferred distinction, evidence-backed match and gap report, keyword/context coverage, formatting checks, no fake ATS score.
5. Documents: accessible templates, PDF/DOCX/TXT/HTML exports, print preview, versioned snapshots.
6. Career toolkit: application pipeline, reminders, interview preparation, STAR answer practice, email templates, profile checklist.
7. Candidate account: secure authentication, cloud sync, export/delete account data, consent and visibility controls.

## Recruiter workspace
1. Verified recruiter/company accounts and organisation tenancy.
2. Job creation and structured requirements.
3. Candidate discovery only for candidates who explicitly opt in to recruiter visibility.
4. Search/filter by skills, experience, location preference, notice period and role relevance.
5. Explainable candidate-job matching that shows supporting resume evidence and gaps; no protected-trait inference or automated rejection.
6. Shortlists, notes, interview stages, candidate communication and audit history.
7. Candidate data access, retention, consent withdrawal and deletion controls.

## Engineering architecture
- Flutter client for PWA and Android.
- FastAPI service for authentication, resume/document APIs, AI orchestration and recruiter workflows.
- PostgreSQL for production data, migrations and tenant-aware access controls.
- Object storage for uploaded files with private access, size/type validation, malware scanning and retention policy.
- AI provider keys only on the server; structured outputs validated before use.
- Observability, rate limiting, audit logs, backups, error reporting and CI/CD.
- Local-first drafts remain available; cloud sync is explicit and authenticated.

## Release sequence
### Foundation (current branch)
- Multi-entry resume model and legacy draft migration.
- Resume import with review and error handling.
- Resume preview, accessible templates and export.
- Strong model/service tests and Flutter CI.

### Candidate beta
- AI writing tools, role-tailoring and evidence-based job analysis.
- Resume versions, multiple resumes, application pipeline and interview toolkit.
- Secure account/session lifecycle, cloud sync and data export/delete.

### Recruiter beta
- Organisation tenancy, recruiter roles and job postings.
- Candidate opt-in/visibility settings, search, shortlist and workflow.
- Explainability, audit trail, privacy controls and abuse prevention.

### Production readiness
- Threat modelling, privacy review, accessibility review, performance/load tests.
- Automated dependency/security scans, backups/restore drills and incident response.
- Real-device Android testing, PWA install/offline/update testing.
- Legal review for privacy, employment and data protection obligations in target markets.

## Non-negotiable quality gates
- No recruiter-facing candidate data without explicit candidate consent.
- No insecure demo authentication or email-only authorisation.
- No API secrets in the Flutter app.
- No claim that keyword coverage is an ATS score or hiring probability.
- No unsupported AI-generated credentials, dates, achievements or skills.
- User can inspect, edit, export and delete their own data.
- Every release passes analysis, unit/widget tests, build checks and security review.

## Known blockers discovered in the legacy backend
- Legacy auth module imports Streamlit and uses a local file/password scheme; it is not suitable as FastAPI production authentication.
- Some API routes accept HTTP bearer credentials without verifying identity/ownership in the route implementation.
- Resume storage includes JSON/local and database modes; production requires a defined PostgreSQL schema, migrations, ownership constraints and tenant isolation.
- Resume parser heuristic extraction is a best-effort import aid, not reliable semantic parsing.
- Existing endpoints and models must be audited before exposing cloud sync, recruiter search or public profile visibility.
