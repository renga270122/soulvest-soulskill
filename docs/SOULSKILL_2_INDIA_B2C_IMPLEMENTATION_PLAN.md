# SoulSkill 2.0 — Global B2C SaaS: Detailed Architecture & Implementation Plan

**Decision:** B2C-first global product; phased market activation; no India-only product assumptions  
**Architecture direction:** Multi-tenant-ready modular monolith, API-first, AI-provider independent  
**Clients:** Flutter Android + responsive PWA  
**Existing baseline:** Flutter Resume Studio + Python/FastAPI API  
**Prepared:** 8 November 2026  
**Related document:** [SaaS Platform Architecture Blueprint](./SOULSKILL_2_SAAS_PLATFORM_ARCHITECTURE.md)

> This is an implementation plan and proposed design. It does not claim that authentication, RLS, billing, RAG, agents, MCP, or recruiter integrations have already been deployed.

---

## 1. Executive implementation decision

Build a globally usable B2C career and admissions product first. Prepare the data model and API boundaries for future organization tenants and recruiter products, while enabling commercial availability market by market after readiness checks. Do not put recruiter workflows into the first release.

### Confirmed product positioning

**SoulSkill — One career profile. Many opportunities.**

Help fresh graduates, job seekers, professionals between roles, job switchers and admissions aspirants create a truthful professional profile, adapt it to opportunities, prepare with confidence and manage the application journey.

### Launch principles

1. Candidate profile ownership and privacy come first.
2. The user remains in control of generated content and external sharing.
3. AI improves presentation; it never invents career or academic facts.
4. ATS insights are explainable estimates, not guarantees of selection.
5. Core access for eligible fresh graduates remains free.
6. Career Restart is low-cost and respectful; no intrusive proof of layoff is required.
7. Job-switching professionals can pay for more frequent and advanced usage.
8. AI usage and costs are metered server-side.
9. APIs and data formats are designed for future recruiter/ATS integrations.
10. Build for reliability and security before adding autonomous agents.

---

## 2. Product scope

### 2.1 User segments and first journeys

| Segment | User need | First product journey |
|---|---|---|
| Fresh graduate | First job, limited experience, confidence | Projects/education → first resume → job match → interview practice |
| Career Restart | Re-enter employment without extra financial pressure | Recover profile → role target → tailored resume → applications |
| Job switcher | Better role, growth, career transition | Existing profile → target role → tailored variants → interview preparation |
| Admissions aspirant | Master's application preparation | Academic profile → CV → SOP draft → requirements checklist |

A user can change their career goal later. Do not permanently lock a user into a segment or use employment status as a stigmatizing label.

### 2.2 B2C MVP — in scope

**Account and onboarding**
- Email/password authentication and account recovery.
- Google sign-in after Android and web redirect testing.
- Personal workspace created at registration.
- Career journey selection and target outcome.
- Progressive profile completion; allow skip and resume later.
- Clear explanation of what data is stored and used by AI.

**Career Studio**
- Canonical candidate profile.
- Resume creation and editing.
- Fresher, experienced and career-transition guidance.
- Multiple role-specific resume versions.
- Autosave and recoverable drafts.
- Resume preview.
- PDF export; DOCX export after formatting and parser validation.
- AI-assisted summary and achievement drafting with before/after review.
- Source facts and profile provenance.

**ATS and job readiness**
- Job description paste/upload.
- Requirement extraction.
- Resume readability checks.
- Evidence-based skills and experience matching.
- Missing-evidence questions and improvement plan.
- Explainable component findings and a match estimate.
- Versioned reports so changes are traceable.

**Career support**
- Basic interview preparation.
- Application tracker.
- Daily/weekly next-step guidance.
- SoulMind affirmations and opt-in Ho'oponopono-inspired reflection.
- SoulCoach career guidance with clear AI limitations.

**SaaS foundations**
- Server-side entitlements and AI credit ledger.
- Payment and subscription lifecycle abstraction.
- User data export and account deletion workflow.
- Usage and error monitoring.
- Basic admin support functions.

### 2.3 Explicitly not in first MVP

- Recruiter candidate search and recruiter workspaces.
- Public candidate directory.
- Automated scraping of job boards.
- Auto-applying to jobs.
- Universal ATS connectivity.
- Public MCP server.
- Agent swarm with autonomous actions.
- Microservices, Kubernetes, Kafka or independent vector database.
- Unlimited AI claims.
- Full admissions marketplace and live deadline aggregation.

The product data model should make future additions possible without building them before customer demand is proven.

---

## 3. Pricing and entitlement design

These are initial pricing hypotheses to validate with interviews, conversion experiments and actual AI costs. Do not hard-code them.

| Plan | Indicative offer | Access model |
|---|---:|---|
| Campus Launch | Free | Core career tools for eligible freshers/students |
| Career Restart | ₹99 / 60 days | Time-bound, affordable assisted job-search support |
| Career Growth | ₹149 / month | More frequent AI, multiple targeted resumes and advanced insights |
| Admissions | Free foundation + paid advanced support | Academic CV, SOP review and application assistance |

### Pricing experience principles

- Avoid labels such as "Unemployed Plan" in the UI; use "Career Restart".
- Use optional self-declaration; don't collect termination letters.
- Do not delete or lock a user's saved resumes when a paid plan expires.
- Show usage limits before a paid AI action.
- Give a clear reason when the user reaches a quota.
- Allow cancellation and show renewal terms transparently.
- Consider student eligibility as a policy/configuration decision, not a reason to collect unnecessary personal data.
- Store price amounts as integer currency minor units with an ISO 4217 currency code, using each currency's correct minor-unit rules and preserving price-version history.

### Entitlement engine

Create feature-based keys, for example:

- resume.active_count
- resume.pdf_exports_period
- ai.summary_rewrites_period
- ai.experience_rewrites_period
- ats.analyses_period
- job.tailoring_period
- interview.practice_minutes_period
- soulmind.guided_sessions_period
- admissions.sop_reviews_period

The backend makes the entitlement decision. Flutter displays the available features and remaining quota but cannot grant itself access.

### Usage ledger

Record:
- user ID and workspace ID;
- feature key;
- request ID and idempotency key;
- units consumed;
- provider/model identifier;
- input/output token counts where available;
- estimated model cost;
- success/failure/refund status;
- timestamp.

Do not store raw resume prompts and documents in billing analytics.

---

## 4. Reference deployment architecture

~~~mermaid
flowchart TB
  subgraph CLIENTS["Clients"]
    AND["Flutter Android"]
    PWA["Flutter Web / PWA"]
  end

  subgraph EDGE["Edge and identity"]
    WAF["TLS / WAF / Rate limiting"]
    AUTH["Supabase Auth"]
    API["FastAPI API v1"]
  end

  subgraph APP["SoulSkill modular backend"]
    PROFILE["Profile and Resume"]
    ATS["ATS and Match"]
    DOC["Document Processing"]
    BILL["Billing and Entitlements"]
    AI["AI Gateway"]
    SOUL["SoulCoach and SoulMind"]
  end

  subgraph DATA["Managed data services"]
    DB["PostgreSQL + RLS"]
    STORAGE["Private object storage"]
    QUEUE["Background worker / queue"]
    VECTOR["pgvector (later phase)"]
  end

  subgraph PROVIDERS["External providers"]
    LLM["LLM provider"]
    PAY["Payment provider"]
    MSG["Email / notifications"]
  end

  AND --> WAF
  PWA --> WAF
  WAF --> AUTH
  AUTH --> API
  API --> APP
  PROFILE --> DB
  PROFILE --> STORAGE
  DOC --> QUEUE
  DOC --> STORAGE
  AI --> LLM
  ATS --> DB
  AI --> VECTOR
  BILL --> PAY
  BILL --> DB
  SOUL --> DB
  API --> MSG
~~~

### Deployment choice

Start with:
- One FastAPI API deployment.
- One worker deployment when asynchronous jobs are introduced.
- Managed PostgreSQL and authentication.
- Private document storage.
- Static PWA hosting/CDN.
- Android distribution through internal testing, then public store release.
- Separate local, CI, staging and production credentials/data.

The API and worker share source modules; they do not need to become separate microservices.

### Global hosting, data residency and cross-border processing

Design a region-aware deployment model. Select the first production region based on latency, vendor availability, contractual terms, privacy/legal requirements and operational capability. Maintain an inventory of all subprocessors and data paths: authentication, API hosting, database, object storage, document parsing, LLM providers, email, analytics, monitoring, support and backups. Add explicit residency/processing-region metadata only where required by a legal or product commitment. Do not claim local or region-exclusive residency unless the full processing and backup path has been verified. A single initial region is acceptable for a controlled pilot; keep interfaces and migration practices ready for later regional partitioning.

---

## 5. Flutter application architecture

The current app uses Provider and a small set of screens. Keep Provider during the first modernization slice. Adopt feature-first MVVM with clear Views, ViewModels, Repositories and Services.

### Proposed folder structure

~~~text
soulskill_mobile/lib/
  app/
    app.dart
    router/
    bootstrap/
  core/
    config/
    network/
    errors/
    storage/
    theme/
    widgets/
    analytics/
  features/
    auth/
      data/
      domain/
      presentation/
    onboarding/
      data/
      domain/
      presentation/
    home/
    profile/
    resume_studio/
    ats_analysis/
    applications/
    soulcoach/
    soulmind/
    billing/
    settings/
  shared/
    models/
    repositories/
~~~

### Layer responsibility

| Layer | Responsibility |
|---|---|
| View | Layout, accessibility, user interaction |
| ViewModel | Screen state, validation orchestration and actions |
| Repository | Source of truth, cache, retries and error mapping |
| Service | HTTP, local storage, files and platform services |
| Domain model | Product concepts independent of transport JSON |
| API DTO | Versioned request/response format |

### Engineering rules

- Widgets must not call HTTP directly.
- No LLM or payment provider keys in Flutter.
- Server controls identity, authorization, plans and AI usage.
- Keep local draft support for offline or transient network failure.
- Cloud sync must not silently overwrite a newer version.
- Provide loading, empty, error, offline and success states for every screen.
- Preserve user input on validation or network errors.
- Add accessibility labels, scalable typography and adequate touch targets.
- Use responsive breakpoints for phone, tablet and browser layouts.
- Use a router when onboarding, authentication and deep links are implemented; avoid building a complex route tree prematurely.

### Screen order

1. Welcome and sign-in.
2. Career journey selection.
3. Goal and profile setup.
4. Personalized dashboard.
5. Career Studio.
6. Resume editor with section progress and review.
7. Resume preview/export.
8. JD input and match findings.
9. Application tracker.
10. SoulMind and SoulCoach.
11. Plans, account, privacy and settings.

---

## 6. Backend architecture and API contract

### 6.1 Incremental migration

Do not replace the existing root api_server.py in one change. It is an existing integration point and imports legacy modules. Add a versioned backend package alongside it, then migrate one route at a time with regression tests.

~~~text
backend/app/
  main.py
  core/
    config.py
    auth.py
    authorization.py
    rate_limits.py
    logging.py
  api/v1/
    router.py
    profile_routes.py
    resume_routes.py
    document_routes.py
    ats_routes.py
    application_routes.py
    ai_routes.py
    entitlement_routes.py
  domains/
    workspaces/
    profiles/
    resumes/
    documents/
    ats/
    applications/
    billing/
    ai/
    soulmind/
  integrations/
    llm/
    storage/
    payments/
    email/
  workers/
  tests/
~~~

### 6.2 Initial API surface

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/v1/me | Authenticated user and workspace summary |
| GET/PATCH | /api/v1/profile | Read/update candidate profile |
| GET/POST | /api/v1/resumes | List/create resume |
| GET/PATCH | /api/v1/resumes/{id} | Read/update owned resume |
| POST | /api/v1/resumes/{id}/versions | Create immutable version |
| POST | /api/v1/documents/upload-url | Request authorized upload |
| POST | /api/v1/documents/{id}/process | Start extraction job |
| POST | /api/v1/ats/analyze | Start or request match analysis |
| GET | /api/v1/ats/reports/{id} | Read user's match report |
| GET/POST | /api/v1/applications | List/create application tracking item |
| PATCH | /api/v1/applications/{id} | Update application status |
| GET | /api/v1/entitlements | Get plan and current feature limits |
| GET | /api/v1/usage | Get current usage summary |
| POST | /api/v1/ai/resume-summary | Create reviewed AI suggestion |
| POST | /api/v1/ai/experience-bullets | Suggest evidence-based bullets |
| POST | /api/v1/soulmind/reflection | Optional guided reflection |

All public APIs are versioned. Use pagination, request IDs, idempotency keys for mutations, explicit timeouts and a stable error schema.

Example error:

~~~json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Please review the highlighted fields.",
    "request_id": "req_example",
    "details": []
  }
}
~~~

Do not return raw model provider errors, secrets, prompts, stack traces or private internal metadata.

### 6.3 Identity propagation and RLS

Preferred first approach to validate:
1. Flutter authenticates with Supabase Auth.
2. Flutter sends its user access token to FastAPI over HTTPS.
3. FastAPI validates signature, issuer, audience and expiry using the configured auth/JWKS approach.
4. For user-scoped database operations, forward the user JWT through a request-scoped Supabase client/PostgREST call so PostgreSQL policies evaluate auth.uid().
5. Never share mutable per-user auth state in a global Supabase client.
6. Use service credentials only for narrowly scoped system operations with explicit owner/workspace checks and audit records.

Before implementation, run a security spike proving that user context is honored end-to-end. If using direct PostgreSQL/SQLAlchemy instead of PostgREST, establish the authenticated role and JWT claims transaction-locally and test policies. Do not use service_role as the normal path for candidate CRUD.

### 6.4 Authentication and authorization

- Verified email and account recovery.
- OAuth/OIDC sign-in with PKCE where applicable.
- Request-scoped principal and workspace context.
- Server-side role and resource checks.
- Deny by default.
- Least-privilege database grants.
- Private object storage and short-lived authorized download links.
- Session revocation and logout.
- No public candidate directory in the initial product.

---

## 7. Initial data model

The first release can use a personal workspace per user and a future-ready membership structure.

| Table | Purpose |
|---|---|
| workspaces | Personal workspace now; organization workspaces later |
| workspace_members | User/workspace membership and role |
| candidate_profiles | Canonical career or academic profile |
| profile_facts | Skills, education, experience and project facts with provenance |
| profile_versions | Immutable snapshots of profile state |
| resumes | Multiple targeted resume documents |
| resume_versions | Immutable resume versions |
| documents | Uploaded/generated files and metadata |
| document_extractions | Parsed text, section map and parser version |
| job_descriptions | User-saved job requirements |
| match_reports | Explainable, versioned match analysis |
| applications | User-controlled application tracker |
| plans | Market/currency-specific plan catalog |
| subscriptions | Payment-provider reference and lifecycle |
| entitlements | Feature keys and plan limits |
| usage_ledger | AI/action usage and cost records |
| consent_records | Notice version, purpose, grant and withdrawal |
| audit_events | Security-relevant activity history |

### Database standards

- UUID identifiers.
- UTC timestamps.
- Foreign keys and check constraints.
- Index all ownership and RLS filter columns.
- Money stored as integer currency minor units with ISO 4217 currency code; never assume two decimal places.
- Soft-delete only where product/legal retention requires it; otherwise schedule verified erasure.
- Immutable versions for generated documents and match reports.
- JSONB only for structured, schema-validated document sections—not as a substitute for all relational data.
- Schema changes via version-controlled migrations.

### Multi-tenancy

Use row-level isolation in PostgreSQL initially. A personal workspace must not imply that a recruiter can access the candidate profile. Organization membership and explicit candidate share grants will be added when recruiter SaaS is built.

RLS negative tests are mandatory:
- User A cannot read, update or delete User B records.
- Anonymous caller cannot access private data.
- Manipulated UUIDs do not bypass authorization.
- Private file links cannot expose another user's files.
- A revoked access grant stops cross-workspace access.

---

## 8. Document processing and resume integrity

### Upload and parse pipeline

1. User selects or uploads a file.
2. Validate file size, extension, MIME type and file signature.
3. Scan for malware before processing.
4. Extract PDF/DOCX content.
5. Preserve page/section provenance where possible.
6. Normalize sections into structured candidate facts.
7. Show a verification screen for extracted facts.
8. Store private original file and parsed representation.
9. Generate a document draft from approved facts.
10. Render, inspect and store output as an immutable version.

### Resume data policy

A canonical profile is the source of truth. A resume is a tailored view of selected profile facts.

An AI draft may:
- Improve clarity and grammar.
- Suggest action verbs.
- Reorder or emphasize evidence.
- Explain missing information.

It must not:
- Invent employers, degrees, certifications or skills.
- Create fabricated metrics or job outcomes.
- Claim a skill based only on the job description.
- Present unsupported assertions as user facts.

Use before/after diff, source fact references and an explicit Save/Apply action.

---

## 9. ATS and job-match intelligence

Return three separate assessments:

**Document readiness**
- Text extraction quality.
- Section/heading recognition.
- Contact and link checks.
- Readability and layout warnings.

**Job alignment**
- Required and preferred skill evidence.
- Experience and project relevance.
- Transferable skill candidates.
- Missing or unclear evidence.
- Seniority/role relevance.

**Application readiness**
- Resume completeness.
- Role targeting.
- Job-specific tailoring.
- Application checklist.

### Matching pipeline

1. Parse the job description into structured requirements.
2. Normalize skill names and aliases.
3. Match explicit terms deterministically.
4. Retrieve potential transferable evidence semantically.
5. Evaluate evidence relevance with a model.
6. Validate model claims against actual profile facts.
7. Calculate component indicators using a versioned algorithm.
8. Return score range/confidence or a transparent alignment estimate, plus the factors that contributed.
9. Ask questions where evidence is missing.
10. Let the user approve suggested resume changes.

Do not call the result a universal ATS score or imply that any percentage guarantees an interview.

---

## 10. AI engineering plan

### 10.1 LLM gateway

A server-only service owns all model access. Product features call the gateway, never vendor SDKs directly.

Core operations:
- structured generation against a Pydantic schema;
- text generation for low-risk experiences;
- embedding generation in a later RAG phase;
- model selection by task and budget;
- timeout/retry/fallback;
- token and cost metering;
- prompt versioning;
- safety and evidence validation.

Use one primary provider at first. Add another provider adapter after evaluating output quality, availability, terms and cost.

### 10.2 Existing Gemini migration

Repository inspection found:
- ai_assistant.py imports google.generativeai.
- It configures a GenerativeModel using the legacy gemini-pro identifier.
- requirements.txt pins google-generativeai==0.3.2.
- Some fallback behavior masks AI failures by generating a generic summary.

Google now recommends the Google GenAI SDK for new Python integrations and migration from its legacy library. Migrate to google-genai in a focused branch, configure the selected model through environment settings, implement structured outputs, and write provider tests before removing the legacy package.

Official migration guidance: https://ai.google.dev/gemini-api/docs/migrate

### 10.3 Initial specialist capabilities

Do not implement agents as independent autonomous personalities at the beginning. Implement bounded domain services first:

| Capability | First implementation |
|---|---|
| Profile Analyst | Structured extraction + user verification |
| Job Analyst | JD parser + requirement taxonomy |
| ATS Analyst | Deterministic scoring + LLM explanations |
| Resume Coach | Draft generation with evidence IDs |
| Interview Coach | Role-specific question generation and rubric |
| Admissions Coach | SOP/CV review against supplied program requirements |
| SoulMind Coach | Curated content selection and optional reflection |
| Quality Reviewer | Schema, provenance and unsupported-claim validation |

### 10.4 Multi-agent orchestration

Introduce LangGraph or an equivalent workflow engine only when a workflow needs multiple steps, durable checkpoints, retries or approval pauses.

Initial job-targeted resume workflow:

~~~mermaid
flowchart TD
  A["User selects resume + job"] --> B["Authenticate and authorize"]
  B --> C["Parse job requirements"]
  C --> D["Retrieve approved candidate facts"]
  D --> E["Match requirements to evidence"]
  E --> F["Build explainable analysis"]
  F --> G["Draft tailored resume"]
  G --> H["Validate facts, schema and ATS structure"]
  H --> I{"User review"}
  I -->|Approve| J["Save new resume version"]
  I -->|Edit| G
  I -->|Reject| K["Keep previous version"]
~~~

Use human approval before any persistent document change. No agent may submit applications, contact recruiters, share private profiles, send outbound messages or trigger payments without explicit user authorization.

### 10.5 RAG rollout

**Phase 1 — private candidate RAG**
- Only the signed-in user's approved documents and facts.
- Source/page/section references.
- Strict owner/workspace filters before retrieval.
- Full-text search first; add embeddings after quality tests.

**Phase 2 — curated role knowledge**
- Skills taxonomy.
- Curated role descriptions.
- Career guidance with source URLs and review dates.
- No unlicensed bulk content.

**Phase 3 — admissions knowledge**
- Official university/program sources.
- Country/program metadata.
- Publication/review timestamps and freshness checks.
- Explicit reminder to confirm deadlines and requirements at official sources.

Use PostgreSQL + pgvector as the first option if query volume and isolation needs permit. Do not build a large global index of private resumes.

### 10.6 MCP rollout

MCP is not an MVP requirement. First stabilize authenticated REST APIs, scopes, audit logs and consent.

Later expose approved tools such as:
- get_my_profile_summary;
- list_my_skills;
- get_my_match_report;
- draft_resume_for_job;
- prepare_interview_plan.

Read operations must still be scope-checked. Any tool that edits a profile, shares a document or triggers an external action requires approval. Follow the current MCP authorization specification, validate token audience and scopes, and do not pass through incoming bearer tokens to upstream services.

Official specification: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization

---

## 11. Background jobs and asynchronous workflows

Use a background worker when a task can take longer than a normal interactive request:
- document parsing;
- large export/render operations;
- embedding generation;
- long AI workflows;
- bulk import/export;
- scheduled deletion and retention jobs;
- payment reconciliation;
- webhook delivery in a later integration phase.

Each job has:
- job ID and request ID;
- user/workspace scope;
- status and progress;
- idempotency key;
- created/started/completed timestamps;
- bounded retry and timeout;
- cancellation policy;
- usage accounting;
- safe error code.

Start with a small worker and a queue abstraction. Add a managed queue or Redis/Celery when actual concurrency/retry demands justify it. Avoid introducing Kafka in the MVP.

---

## 12. Billing and global payment architecture

Use a provider adapter so the business layer is independent of one payment gateway.

Provider evaluation should include:
- Market-specific cards, bank transfers, wallets, UPI or recurring mandates where available;
- one-time payments for Career Restart;
- subscription renewals and cancellation;
- refund and dispute workflows;
- webhooks and signature verification;
- settlement, tax and invoice requirements;
- fees and merchant onboarding.

The existing repository includes Razorpay, so evaluate it for the India market. Evaluate additional global providers only when a target market requires them. Do not assume any provider is configured, approved for live use or available to the business in every country.

### Payment workflow

1. Backend validates plan and current entitlement.
2. Backend creates provider order/subscription.
3. Client completes hosted/SDK payment flow.
4. Provider sends signed webhook.
5. Backend verifies signature and durably records event.
6. Event is processed idempotently.
7. Subscription state and entitlements are updated.
8. Client refreshes authoritative entitlement state.
9. Reconciliation catches missed or delayed webhooks.

Never grant paid features based only on a client-side success callback.

---

## 13. Global privacy, safety and legal readiness

Obtain jurisdiction-specific legal review before enabling each market. A global app may be subject to privacy, consumer, advertising, accessibility, employment and data-transfer laws outside its place of incorporation. Keep a market applicability register and map legal bases, notice, rights, retention, processors, transfers and incident obligations with qualified counsel. Do not assume one global consent mechanism or one privacy policy is sufficient.

Engineering controls:
- Plain-language privacy notice with specific purposes.
- Separate explanation for profile storage, AI processing, analytics and recruiter sharing.
- Data minimization and optional fields.
- Purpose-specific consent/authorization records where applicable.
- Easy withdrawal where consent is the applicable basis.
- User access, correction, export and erasure request workflows.
- Retention schedule for original documents, extracted text, embeddings, generated artifacts, operational logs and backups.
- Processor/subprocessor inventory and contractual review.
- Documented data residency/cross-border data paths.
- TLS and encryption at rest.
- Least-privilege staff/admin access.
- Incident detection and response procedures.
- Child/minor safeguards; establish intended age eligibility and handling with counsel before student marketing.
- No public candidate discoverability by default.
- Consent to use AI must not be conflated with permission to share data with a recruiter.

Official reference:
- Gazette/MeitY DPDP Rules 2025: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa
- MeitY Rules portal: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa
- Government summary of phased implementation: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190014&lang=2&reg=3

SoulMind must be opt-in and supportive. It is not a mental-health diagnostic or treatment service. Do not imply that rejection or unemployment is caused by a person's mindset, and do not claim that affirmations guarantee employment.

---

## 14. Security and release gates

No public release handling real resumes without all of the following:

**Identity/data**
- Token signature, issuer, audience and expiry validation.
- RLS on every exposed table.
- Negative cross-user access tests.
- Private storage access controls.
- Service secrets server-only.
- User export/deletion workflow tested.

**Files**
- MIME/signature/size validation.
- Malware scanning.
- Rate and storage quotas.
- Signed URL expiry.
- Document parser time and memory limits.

**AI**
- Provider keys server-side.
- Prompt-injection tests for uploaded documents and job descriptions.
- Output schema validation.
- Unsupported claim detection.
- RAG tenant/user filtering.
- Cost and rate limits.
- Human approval for edits and external actions.

**Payments**
- Signed webhook verification.
- Idempotent event handling.
- Reconciliation job.
- Negative tests for duplicate, delayed and failed events.

**Operations**
- Backups and restore test.
- Error alerts and incident response.
- API and worker health checks.
- Audit events for sensitive operations.
- No raw candidate documents in normal application logs.

---

## 15. Repository work plan and implementation tickets

Implement in small pull requests, each with tests and review.

### Sprint 0 — baseline and local reliability

**SS-001: Inventory current application**
- Map Flutter screens, models, provider and API endpoints.
- Record what works and what does not.
- Identify duplicate/legacy backend modules.
- Preserve Streamlit behavior.

Acceptance:
- Existing Flutter analyzer and widget tests pass.
- Existing Python tests pass.
- Feature branch remains isolated.
- No unreviewed destructive refactor.

**SS-002: Fix environment-specific API configuration**
- Browser development uses the configured localhost API host.
- Android emulator uses emulator host mapping.
- Physical-device development uses an explicit LAN URL.
- Production always uses HTTPS.
- Add GET /health readiness check and frontend connection error classification.

Acceptance:
- Chrome can call local API health endpoint.
- Android emulator can call API with its configured base URL.
- Missing backend displays actionable error rather than generic Failed to fetch.
- No secret is compiled into client builds.

**SS-003: Backend configuration and CORS**
- Centralize settings in environment-backed configuration.
- Replace allow_origins=["*"] with explicit local/staging/production origins.
- Do not combine wildcard origin with credentials.
- Add request IDs and structured error mapping.

Acceptance:
- Local browser origin works.
- Unapproved production origin is rejected by browser CORS.
- Backend unit tests verify allowed/disallowed origin configuration.

### Sprint 1 — design system and identity

**SS-010: Figma product design foundation**
- Personas and user journeys.
- Design tokens, typography, spacing, colors, iconography.
- Component library and accessibility rules.
- Onboarding and dashboard wireframes.
- Android and responsive web prototypes.

Acceptance:
- All primary flows have mobile layouts.
- Responsive behavior specified at phone/tablet/desktop widths.
- Loading/empty/error/offline states included.
- Design file is connected to implementation handoff.

**SS-011: Auth and onboarding**
- Email signup/login.
- Email verification and recovery.
- Google sign-in after platform redirect validation.
- Career-stage and target-goal setup.
- Private personal workspace creation.

Acceptance:
- User can register, verify, sign in/out and recover account.
- Reopening app retains valid session.
- Anonymous user cannot read/write private profile.
- Onboarding can be resumed after exit.

### Sprint 2 — data foundation and profile

**SS-020: Supabase project and migrations**
- Create separate development/staging projects.
- Enable only required API exposure.
- Version migrations in repository.
- Establish RLS and storage policies.
- Create owner/profile/workspace schema.

Acceptance:
- Clean local/staging database can be recreated from migrations.
- pgTAP/SQL tests prove positive and negative row access.
- No client has service role key.
- Storage access follows profile ownership.

**SS-021: Candidate profile API and Flutter repository**
- Authenticated profile read/update.
- Profile facts and structured sections.
- Offline draft cache and conflict strategy.
- Profile version snapshots.

Acceptance:
- User A cannot access User B profile.
- Cloud save/reload works.
- Offline edit is not silently lost.
- Conflict resolution presents versions rather than overwriting invisibly.

### Sprint 3 — Resume Studio productization

**SS-030: Resume data model and versions**
- Canonical profile to resume mapping.
- Create/update/list resumes.
- Immutable resume versions.
- Target-role metadata.

**SS-031: Resume editor redesign**
- Progressive section wizard or grouped sections.
- Fresher and experienced variants.
- Examples and contextual hints.
- Completion indicator and review checklist.
- Save state and version history.

**SS-032: Export and document processing**
- PDF export.
- DOCX export after quality test.
- Upload parser and extraction provenance.
- Private storage, file validation and malware scanning.

Acceptance for Sprint 3:
- A user can create, edit, preview, export and reopen their resume.
- Generated output contains only approved profile facts.
- Export is readable in common PDF/DOCX parsers.
- Failed exports can be retried without duplicate charge.
- User can retain older versions.

### Sprint 4 — AI gateway and ATS intelligence

**SS-040: Migrate Google GenAI integration**
- Replace legacy google-generativeai use with google-genai.
- Model selected from server configuration.
- Pydantic request/response schemas.
- Provider timeout/error handling.
- Unit tests with mocked provider.

**SS-041: Evidence-aware resume assistance**
- Summary rewrite.
- Experience bullet improvement.
- Before/after diff.
- Provenance IDs and missing info.
- User approval before apply/save.

**SS-042: Job description and match engine**
- Parse JD into required/preferred qualifications.
- Normalize skills.
- Keyword and synonym matching.
- Evidence mapping.
- Explainable match report.
- Version scoring algorithm.

Acceptance:
- Malformed model response never updates user data.
- Unsupported AI facts are rejected or surfaced.
- Match report identifies evidence and gaps.
- No universal ATS guarantee or false precision.
- Usage ledger records successful and failed requests correctly.

### Sprint 5 — SoulCoach, SoulMind and applications

**SS-050: SoulMind**
- Curated affirmations by career stage.
- Guided Ho'oponopono-inspired reflection.
- Optional journal entries.
- Notification opt-in and quiet hours.
- Privacy and delete controls.

**SS-051: SoulCoach**
- Career-plan suggestions.
- Interview question generation.
- Practice response feedback.
- Supportive tone and non-clinical boundaries.

**SS-052: Application tracker**
- Company, role, link, stage and notes.
- Next follow-up date.
- User-controlled status updates.
- Export application history.

Acceptance:
- Reflection data is private.
- No diagnostic claims or guaranteed outcomes.
- Notifications are opt-in and user-controlled.
- Application data is exportable/deletable.

### Sprint 6 — monetization and launch readiness

**SS-060: Plans and entitlement service**
- Configurable plan catalog.
- Free plan.
- One-time Career Restart purchase.
- Monthly Career Growth subscription.
- AI quotas and feature access.

**SS-061: Payment provider integration**
- Sandbox payment.
- Verified webhook flow.
- Idempotent state transitions.
- Refund/cancellation handling.
- Reconciliation.

**SS-062: Production readiness**
- Privacy/legal review.
- Security review and RLS penetration tests.
- Backup/restore test.
- Monitoring and alerting.
- Play Store/PWA release readiness.

Acceptance:
- Payment confirmation cannot be forged by the client.
- Duplicate webhook cannot double-grant entitlements.
- User can cancel and see expiry/renewal status.
- Plan expiry does not destroy saved documents.
- Public launch gate is signed off.

### Post-MVP — recruiter SaaS and integrations

**SS-100: Organization workspaces and memberships**  
**SS-110: Candidate permission/share grants and audit**  
**SS-120: Recruiter job management and match workflow**  
**SS-130: Versioned partner API and webhooks**  
**SS-140: Selected ATS connectors**  
**SS-150: MCP server with OAuth, scopes and human approval**  
**SS-160: Career profile interoperability/export adapters**

Do not begin recruiter search until consent, access control, audit and retention are reviewed.

---

## 16. Test and quality strategy

### Flutter
- Unit tests for profile/resume models and repositories.
- Widget tests for onboarding, editor and preview.
- Integration tests for login, save/reload, export and error states.
- Responsive web tests.
- Accessibility checks and keyboard navigation on web.

### Backend
- Unit tests for domain services and entitlement calculations.
- API tests for auth, ownership and validation.
- RLS tests for all CRUD operations.
- Contract tests for OpenAPI and Flutter DTO compatibility.
- Integration tests for storage, AI provider and payment sandbox.
- Background worker idempotency and retry tests.

### AI evaluation
Build a versioned golden set with synthetic profiles:
- Fresher with coursework and projects.
- Experienced engineer.
- Career switcher.
- Long employment gap.
- Non-technical applicant.
- Academic/admissions profile.
- Sparse and ambiguous data.
- Adversarial job description asking the model to ignore instructions.

Measure:
- factual support / unsupported claims;
- relevance and helpfulness;
- skill extraction precision/recall;
- citation/provenance coverage;
- output schema pass rate;
- latency and cost per request;
- user edit/acceptance rate.

Do not use real private resumes in evaluation without explicit permission and a reviewed retention/processor setup.

---

## 17. Delivery gates and release milestones

| Gate | Deliverable | Exit condition |
|---|---|---|
| G0 | Baseline stable | Flutter/Python test suites green; API config fixed |
| G1 | UX foundation | Onboarding and dashboard prototype reviewed |
| G2 | Identity and data | Auth + RLS + negative isolation tests pass |
| G3 | Resume MVP | Cloud save, versioning, preview and export work |
| G4 | AI/ATS | Structured outputs and evidence validation pass |
| G5 | Retention | SoulMind, SoulCoach and application tracker validated |
| G6 | Monetization | Sandbox payment, webhook and entitlements pass |
| G7 | Public B2C launch | Security, privacy, support and restore gates signed off |

Timelines should be estimated only after confirming available engineering hours and which environments/accounts have already been provisioned. A small team should complete each gate in reviewable increments rather than parallelizing all platform features.

---

## 18. Immediate next actions

1. Review the architecture and implementation plan documents in the product branch.
2. Confirm whether the current Supabase account/project already exists; do not create production credentials inside this documentation change.
3. Fix the browser API base URL and local CORS configuration so the current AI summary test is reliable.
4. Create Figma pages and design tokens, then approve onboarding and home dashboard.
5. Run the Supabase/RLS identity propagation spike before committing to a data-access pattern.
6. Create the first database migration only after the ownership and RLS tests are agreed.
7. Migrate one AI endpoint to the new Google GenAI SDK and a typed output contract.
8. Keep every implementation step in a small feature branch and pull request.

### Open decisions to resolve before implementation

| Decision | Recommended default |
|---|---|
| Auth provider | Supabase Auth |
| Database | Supabase-hosted PostgreSQL with RLS |
| Data access | User-scoped JWT to RLS-protected Data API or verified transaction-scoped DB role; prove with test spike |
| First AI provider | Google GenAI, subject to quality, cost, terms and privacy review |
| Agent framework | No agent framework for first AI endpoint; evaluate LangGraph for the first multi-step workflow |
| Vector search | Full-text first, pgvector when validated |
| Payment | Evaluate Razorpay first, behind provider adapter |
| Figma | Figma source of truth; editable file requires workspace connection |
| Launch cohort | Small invited pilot in the first operationally ready market(s); India is a practical candidate, not a product limit |

---

## 19. Official technical and regulatory references

The implementation choices should be revisited against current vendor documentation before each deployment.

- Flutter application architecture: https://docs.flutter.dev/app-architecture/guide
- Supabase Flutter quickstart: https://supabase.com/docs/guides/getting-started/quickstarts/flutter
- Supabase Row Level Security: https://supabase.com/docs/guides/database/postgres/row-level-security
- Supabase database migrations: https://supabase.com/docs/guides/deployment/database-migrations
- Google GenAI SDK migration: https://ai.google.dev/gemini-api/docs/migrate
- LangGraph human-in-the-loop: https://docs.langchain.com/oss/python/langgraph/interrupts
- MCP authorization: https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization
- MeitY DPDP Rules 2025: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa
- Government summary of DPDP phased rollout: https://www.pib.gov.in/PressReleasePage.aspx?PRID=2190014&lang=2&reg=3

**End state:** A trusted, affordable global B2C career SaaS with secure personal workspaces, localized experiences, evidence-backed AI, explainable job matching and a portable career profile. Recruiter SaaS, ATS integrations, MCP and more advanced multi-agent workflows are later growth phases built on the same carefully designed foundation.


---

## 20. Global product and localization architecture

Global is the product audience and technical design target. Commercial launch is phased. Do not hard-code any one country's assumptions into data, screens, billing, AI prompts or document generation.

### 20.1 Keep country, market, locale, currency and time zone separate

Store these concepts independently:
- Country of residence: optional and collected only when required.
- Market code: server-configured commercial availability, contract, pricing and feature policy.
- Locale: BCP 47 language tag, such as en-US, en-GB, en-IN or hi-IN.
- Time zone: IANA identifier, such as America/Los_Angeles, Europe/London or Asia/Kolkata.
- Currency: ISO 4217 code attached to each price and transaction.
- Data region: server-controlled processing/storage assignment where required by legal or contractual commitments.

Language does not imply country; country does not imply currency; IP geolocation does not establish identity, tax residence, legal basis, market eligibility or payment entitlement.

### 20.2 Internationalization standards

- Use UTF-8/Unicode through database, APIs, search, exports and analytics metadata.
- Use BCP 47 language tags and a maintained CLDR-backed localization library.
- Keep UI translations separate from user-authored resume/profile content.
- Localize dates, numbers, currencies, measurements, pluralization and sorting.
- Store timestamps as UTC instants; store the user's IANA time zone for display and recurring reminders.
- Store each monetary amount as an integer currency minor-unit value plus explicit currency code. Do not assume every currency has two decimal places.
- Use international phone-number handling; preserve the original user-entered display where useful.
- Avoid fixed assumptions about first/last names, address fields, postal codes, education systems or employer formats.
- Test diacritics, long names, non-Latin scripts, font fallback and right-to-left layouts.
- Ensure generated PDF/DOCX files use fonts with the required glyph coverage and text shaping.
- Support target-market resume conventions through explicit templates: A4/Letter, section ordering, personal-data expectations, photo rules and date formats. Never assume one universal resume layout.
- The first UI language may be English, but translation extraction and locale switching should be built in from the beginning. Add professionally reviewed translations market by market.

Unicode CLDR 49 was released in October 2026 and provides locale data/rules for language identifiers, currency and number formats, dates and time zones:
- https://www.unicode.org/reports/tr35/
- https://www.unicode.org/reports/tr35/49/tr35-numbers.html
- https://www.unicode.org/reports/tr35/49/tr35-dates.html
- https://blog.unicode.org/2026/10/unicode-cldr-49-released.html

### 20.3 Market profiles

Create server-side market configuration records with:
- market code and launch state;
- supported/default locales;
- supported currencies and localized price catalog;
- payment provider and methods;
- tax/invoice and refund display requirements;
- applicable terms and privacy notice versions;
- support language/contact route;
- resume/document template variants;
- enabled features and AI provider restrictions;
- data-processing region and transfer configuration;
- age eligibility and feature restrictions;
- launch owner and last legal/operational review.

Market status values should include planned, internal_test, pilot, enabled and suspended. The backend decides market eligibility; clients cannot switch market to bypass pricing, tax or legal controls.

### 20.4 Global payment and commercial model

- Keep plan features separate from localized price points.
- Support market/currency-specific prices and preserve price history.
- Store currency-specific minor units; format using locale data.
- Display renewal interval, tax treatment, renewal amount, cancellation and refund terms clearly.
- Support one-time packages and subscriptions independently.
- Select payment provider by market, merchant eligibility and local method coverage.
- Handle refunds, disputes, subscription cancellation, retries and grace periods.
- Verify and process provider webhooks idempotently.
- Reconcile entitlement state against provider state.
- Review mobile app-store payment rules before enabling purchases in each app-store market.

The first pilot may use an India payment provider because the existing repository includes Razorpay. That is a first-market decision only; it must not be hard-coded into domain services or the global plan model.

### 20.5 Global privacy and data-transfer readiness

Maintain a jurisdiction applicability register and end-to-end data-flow map. Legal review should consider, where applicable:
- EU/EEA GDPR and its territorial scope, data subject rights and international transfers;
- UK GDPR and UK international-transfer rules;
- California CCPA/CPRA where statutory applicability conditions are met;
- Brazil LGPD and ANPD international-transfer rules;
- India DPDP Act and Rules based on phased commencement and applicability;
- other privacy, consumer, employment, children’s data and AI laws in enabled markets.

Implementation artifacts:
1. Data inventory and source-to-destination data-flow map.
2. Subprocessor register covering authentication, hosting, storage, AI, email, analytics, monitoring, support and backups.
3. Purpose, legal-basis, retention and deletion register.
4. Market-specific privacy notices and user-rights workflows.
5. Cross-border transfer assessments and contractual safeguards where required.
6. Account export, correction and erasure workflows with identity checks and legal-retention exceptions.
7. Security incident response and notification playbook.
8. AI/human-review assessment before any high-impact recruiting/admissions decisions.

Official starting references (not legal advice; confirm applicability with qualified counsel):
- EU GDPR application: https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/application-gdpr_en
- EU individual rights: https://commission.europa.eu/law/law-topic/data-protection/information-individuals_en
- EU international transfers: https://commission.europa.eu/law/law-topic/data-protection/international-dimension-data-protection/rules-international-data-transfers_en
- UK ICO international transfers, updated January 2026: https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/international-transfers/a-guide-to-international-transfers/
- California DOJ CCPA information, updated August 2026: https://www.oag.ca.gov/privacy/ccpa
- Brazil ANPD international transfers: https://www.gov.br/anpd/pt-br/assuntos/assuntos-internacionais/transferencia-internacional-de-dados
- India MeitY DPDP Rules and enforcement timeline: https://www.meity.gov.in/documents/act-and-policies/digital-personal-data-protection-rules-2025-gDOxUjMtQWa

The European Commission explains that GDPR can apply to non-EU businesses offering services to people in the EU or monitoring their behavior. EEA transfers need an applicable transfer mechanism/safeguard. California CCPA/CPRA obligations depend on statutory scope and thresholds. Brazil ANPD publishes rules on international transfers. Build controls to support applicable obligations; do not claim blanket compliance merely because the architecture includes privacy features.

### 20.6 Global accessibility target

Target WCAG 2.2 AA for responsive web experiences and equivalent accessibility principles on Android:
- keyboard operability and visible focus;
- screen-reader labels and semantic navigation;
- scalable text and responsive reflow;
- sufficient contrast and no color-only status indications;
- accessible validation and error announcements;
- captions/transcripts for audio;
- reduced-motion support;
- plain-language explanations of AI outputs, automated suggestions and privacy controls.

WCAG 2.2 is a W3C Recommendation: https://www.w3.org/TR/wcag/

### 20.7 Market launch checklist

Enable a market only when:
- product language and support are ready;
- resume/document templates are reviewed for local conventions;
- payment, tax, invoicing, refund and subscription flows are tested;
- terms and privacy notices are reviewed by counsel;
- vendor availability and AI processor terms are validated;
- storage region and cross-border transfers are documented;
- accessibility and right-to-left needs are tested where relevant;
- support and incident response have an operational owner;
- store distribution requirements are satisfied.

### 20.8 Globalization work tickets

**GLOB-001 — Locale and market foundation**
- Add locale, country, time zone, market and data-region concepts as separate fields.
- Add server-side market profile configuration.
- Add currency/date/number formatting utilities.
- Acceptance: changing locale does not silently alter currency, market or account access.

**GLOB-002 — Internationalized Flutter UX**
- Extract hard-coded text into translation resources.
- Add locale selection and fallback behavior.
- Test long labels, Unicode, non-Latin scripts and RTL layouts.
- Acceptance: onboarding and resume screens render correctly with expanded text and supported scripts.

**GLOB-003 — Currency-aware billing model**
- Add market-specific localized price catalog.
- Store amount as currency minor units plus explicit currency.
- Acceptance: INR, USD, EUR and a zero-decimal currency can be represented without schema changes.

**GLOB-004 — Market-specific privacy/support controls**
- Version privacy notices and terms by market.
- Register subprocessors and data-processing regions.
- Add localized support routing.
- Acceptance: a market cannot be enabled until required legal/operational checks are approved.

**GLOB-005 — Document conventions**
- Support A4/Letter page profiles.
- Localized dates and international contact fields.
- Unicode font and text-shaping tests.
- Acceptance: PDF/DOCX exports pass visual and text extraction tests for every language claimed as supported.

### 20.9 Global readiness acceptance criteria

- Country, market, locale, currency, time zone and data region are stored independently.
- Monetary display is locale-aware; stored amounts retain explicit currency codes.
- UTC timestamps display correctly across time zones and daylight-saving changes.
- Names, addresses and contact details do not assume one national pattern.
- At least one non-Latin sample profile renders in Android, web, PDF and DOCX.
- Long translated labels do not overflow primary screens.
- UI copy can be translated without changing application logic.
- RTL support is not advertised until it is tested.
- Market plan/payment/legal configuration is server-driven.
- Subprocessor and international transfer maps exist for every enabled market.
- Privacy rights and deletion workflows are tested in staging.
- Accessibility checks include keyboard, screen reader, contrast and text scaling.

### 20.10 Global launch roadmap update

| Phase | Scope | Release outcome |
|---|---|---|
| 0 | Baseline, API configuration, global design tokens | Stable foundation |
| 1 | Auth, personal workspace, locale/market fields and profile | Secure B2C identity |
| 2 | Resume Studio, versioning, document storage/export | Candidate product |
| 3 | LLM gateway, evidence-aware AI, ATS | Career intelligence |
| 4 | Applications, SoulCoach and SoulMind | Retention and user value |
| 5 | Pricing, entitlements and first market payment provider | Paid B2C pilot |
| 6 | Legal, privacy, security, support and store checks | First public market |
| 7 | Additional locale, payment and legal enablement | Global expansion |
| 8 | Recruiter SaaS, partner APIs, ATS connectors and MCP | Platform ecosystem |

The first operational pilot can be in India if it is the most practical cohort, but India is not a product or data-model constraint.

### 20.11 Global architecture decisions

| ID | Decision | Status |
|---|---|---|
| G-001 | Global B2C product; phased market activation | Proposed |
| G-002 | B2C first; recruiter SaaS later | Confirmed |
| G-003 | Country, market, locale, currency, time zone and data region are distinct | Proposed |
| G-004 | Unicode/CLDR-backed formatting and BCP 47 locales | Proposed |
| G-005 | UTC persistence and IANA time-zone identifiers | Proposed |
| G-006 | Currency-aware minor-unit money storage | Proposed |
| G-007 | Market-specific plans, providers, taxes and legal notices | Proposed |
| G-008 | Jurisdiction-specific privacy and cross-border assessment per market | Proposed |
| G-009 | WCAG 2.2 AA as responsive web accessibility target | Proposed |
| G-010 | No universal compliance or residency claims without validation | Proposed |
