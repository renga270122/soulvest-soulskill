# SoulSkill 2.0 — SaaS Product & Platform Architecture Blueprint

**Status:** Initial architecture proposal  
**Product:** SoulSkill by Soulvest.ai  
**Repository branch:** \`product/soulskill-2-platform-foundation\`  
**Architecture style:** Modular monolith, multi-tenant SaaS, API-first, AI-provider independent  
**Primary clients:** Flutter Android app and responsive PWA  
**Initial market:** India, designed for international expansion

---

## 1. Product vision

SoulSkill is an AI-powered Career and Admissions Companion. It helps individuals build a portable professional profile, create evidence-based application documents, understand job and admissions requirements, prepare for interviews, and maintain confidence during career transitions.

Long-term ambition: become a trusted career identity and opportunity platform that can serve job seekers, students, recruiters, employers, universities, and recruitment technology partners.

### Product principles

1. **Candidate first:** The individual owns their profile and controls when it is shared.
2. **Evidence before generation:** AI may improve how facts are communicated, but must not invent qualifications, employers, projects, grades, skills, achievements, or metrics.
3. **Explainable intelligence:** ATS and matching results show the evidence and reasoning behind recommendations. No promise of interview or job selection.
4. **Accessible pricing:** Core career access is free for fresh graduates; Career Restart is low-cost; job-switching professionals pay a modest premium. Recruiter and enterprise products use separate SaaS plans.
5. **Interoperability:** Candidate data should be portable and exportable; integrations use documented APIs, webhooks, and supported standards.
6. **Privacy by design:** Personal candidate data is private by default. Cross-user or recruiter access requires an explicit, revocable permission or a valid application workflow.
7. **Human agency:** Users review and approve generated documents and consequential actions.

---

## 2. Customer segments and products

### Individual / B2C

| Journey | Initial plan concept | Main capabilities |
|---|---|---|
| Campus Launch | Free for eligible fresh graduates | Resume/CV, basic ATS readiness, projects, skills, cover letters, basic interview preparation, SoulMind |
| Career Restart | Affordable time-bound package | Resume tailoring, job matching, application support, interview coaching, SoulCoach and SoulMind |
| Career Growth | Affordable subscription | Multiple resume variants, advanced matching, LinkedIn guidance, career transition and interview practice |
| Admissions | Free foundation plus affordable add-ons | Academic CV, SOP support, application checklist, course and university research |

Plan entitlements, price, expiry, quotas and eligibility must be stored as configuration and database records, not hard-coded into Flutter screens.

Avoid intrusive layoff verification. Use respectful, optional self-declaration. Do not remove access to a user's own saved documents merely because a paid entitlement expires.

### Recruiter / B2B

Recruiter SaaS is a separate product surface, not merely an extra tab in the job-seeker app.

Potential capabilities:
- Organization and recruiter workspaces.
- Role-based access for recruiters, hiring managers and workspace admins.
- Candidate profiles shared with the organization by the candidate or through a documented application flow.
- Job requirement intake and structured job descriptions.
- Candidate-to-role matching with explanations.
- Interview pipeline and collaboration.
- ATS integrations, API access and webhooks.
- Audit history, usage metering and organization billing.

Do not build a public candidate directory by default. Recruiter discovery must be opt-in and controlled by candidate visibility settings and consent.

### Platform / partner SaaS

Provide a developer-facing integration product:
- Versioned REST API and OpenAPI specification.
- Webhooks for candidate-authorized events and workflow updates.
- OAuth 2.0 / OpenID Connect authorization for connected applications.
- Scoped API credentials for approved server-to-server use.
- Connector adapters for selected ATS and HR platforms.
- MCP server for authorized agentic access to SoulSkill capabilities.
- Sandbox tenant, test users and integration documentation.

No architecture can guarantee universal compatibility or adoption by all recruiters and ATS providers. Each integration needs technical validation, access approval, commercial agreement where applicable, and ongoing compatibility testing.

---

## 3. SaaS architecture principles

### Start with a modular monolith

Use a well-structured FastAPI application with separate domain modules. Deploy the API and background worker independently when needed, while keeping a single repository and shared domain contracts initially.

Do not start with microservices, Kafka, Kubernetes, or a collection of independently deployed agents. Those increase operational complexity before traffic and team size justify them.

### Logical platform planes

**Control plane**
- Tenant and organization provisioning.
- Identity and membership management.
- Plan catalog, billing and subscription lifecycle.
- Entitlements, AI credits, rate limits and usage metering.
- Feature flags and configuration.
- Integration registration and API credentials.
- Platform administration and audit controls.

**Product/data plane**
- Candidate profiles and profile versions.
- Resumes, academic CVs, SOPs and supporting documents.
- Job descriptions, admissions requirements and opportunity records.
- ATS analyses and match explanations.
- Applications and user activity.
- Private knowledge indexes and RAG retrieval.
- AI workflow runs and generated artifacts.

**Integration plane**
- Public versioned API.
- Webhooks and event delivery.
- ATS / HR connector adapters.
- MCP server and OAuth authorization.
- Import/export formats and developer portal.

The control plane may initially be implemented as modules in the same backend. The logical separation should exist in code, permissions and data ownership even before separate deployments.

---

## 4. Reference architecture

\`\`\`mermaid
flowchart TB
    subgraph CLIENTS["Client applications"]
      A["Flutter Android"]
      W["Responsive PWA"]
      R["Recruiter workspace"]
      D["Developer portal / partner systems"]
    end

    subgraph EDGE["Edge and identity"]
      CDN["CDN / WAF / rate limits"]
      AUTH["Identity provider / OAuth / OIDC"]
      API["Versioned API gateway"]
    end

    subgraph APP["SoulSkill modular application"]
      TEN["Tenant and membership"]
      PROF["Career profile and documents"]
      CAREER["Career Studio and applications"]
      ATS["ATS and matching"]
      BILL["Billing and entitlements"]
      INTEG["Integration registry"]
      ADMIN["Administration and audit"]
    end

    subgraph AI["AI platform"]
      GATE["Model/provider gateway"]
      ORCH["Workflow orchestrator"]
      RET["RAG retrieval service"]
      AG["Bounded specialist agents"]
      GUARD["Policy, evidence and output guardrails"]
    end

    subgraph DATA["Data and asynchronous processing"]
      PG["PostgreSQL"]
      VEC["pgvector / hybrid search"]
      OBJ["Private object storage"]
      Q["Background jobs / queue"]
      OBS["Metrics, traces and audit events"]
    end

    subgraph EXT["External ecosystem"]
      LLM["LLM providers"]
      MCP["SoulSkill MCP server"]
      ATSX["External ATS / HR platforms"]
      PAY["Payment provider"]
      MAIL["Email / notification provider"]
    end

    A --> CDN
    W --> CDN
    R --> CDN
    D --> CDN
    CDN --> AUTH
    AUTH --> API
    API --> APP
    APP --> AI
    APP --> DATA
    GATE --> LLM
    ORCH --> AG
    AG --> RET
    GUARD --> ORCH
    RET --> VEC
    PROF --> OBJ
    PROF --> PG
    CAREER --> Q
    BILL --> PAY
    INTEG --> ATSX
    MCP --> API
    APP --> OBS
\`\`\`

---

## 5. Multi-tenant data isolation

### Tenant model

Support both individual workspaces and organization workspaces.

- A person has a private personal workspace.
- A recruiter or employer has an organization tenant.
- A user can belong to multiple organizations with different roles.
- A candidate profile remains owned by the individual.
- An organization receives only the candidate information shared with it through explicit consent or an application process.
- A partner integration receives only the scopes and records authorized for that integration.

Do not model every record with one generic \`tenant_id\` and assume that this alone captures sharing. Separate record ownership, organization ownership and share grants.

### Core entity model

| Entity | Purpose |
|---|---|
| users / identities | Authentication identity |
| personal_workspaces | Individual's private workspace |
| organizations | Recruiter, employer, university or partner tenant |
| memberships | User-to-organization membership and role |
| candidate_profiles | Canonical individual career / academic profile |
| profile_versions | Immutable or versioned snapshots of profile facts |
| documents | Resumes, CVs, SOPs, certificates and source files |
| document_sections | Parsed structured content with provenance |
| skills / experiences / education | Normalized career facts and evidence references |
| jobs / admissions_programs | Opportunities and requirements |
| match_reports | Versioned explanation of profile-to-requirement analysis |
| applications | Candidate-controlled application tracking |
| share_grants | Explicit permissions for another user or organization |
| subscriptions / entitlements | Plan, limits, expiry and access rules |
| usage_events / credit_ledger | AI and product usage metering |
| integration_connections | External platform connection metadata |
| webhook_endpoints / deliveries | Partner event subscriptions and delivery history |
| ai_workflows / agent_runs | Workflow state, trace identifiers and safe metadata |
| audit_events | Security-sensitive activity history |

### Row Level Security

Use a shared PostgreSQL schema initially, with explicit ownership columns and Postgres Row Level Security (RLS).

Every organization-owned table must enforce organization membership and role. Every candidate-owned table must enforce owner access. Cross-boundary access must be evaluated through a specific share grant or application permission.

Rules:
- Deny by default.
- Enforce both reads and writes.
- Use database policies as a second line of defense, not just application query filters.
- Never expose service-role credentials to Flutter or browser code.
- Test RLS with positive and negative tests for every role.
- Consider separate schemas or databases only for customers with contractual isolation requirements.

### Cross-workspace access

A recruiter must not gain access to a candidate's full personal workspace just because a resume was shared.

Create a scoped share grant with:
- candidate user/profile ID;
- recipient organization or specific recruiter;
- permitted fields/documents;
- purpose;
- granted_at and expires_at;
- revoked_at;
- source workflow (application, share link, direct invitation);
- consent notice/version;
- audit trail.

---

## 6. Identity, authorization and security

Recommended first implementation:
- Supabase Auth for email/password and supported social sign-in.
- Add secure email verification and password reset.
- Use OAuth/OIDC for third-party integrations.
- Use PKCE for public mobile/browser clients.
- Add organization RBAC: owner, admin, recruiter, hiring_manager, interviewer, billing_admin, integration_admin.
- Add candidate privacy controls and session/device management.
- Add rate limits at API and tenant levels.
- Encrypt sensitive tokens and integration secrets at rest using a managed key service.
- TLS for all production traffic.
- Keep LLM provider keys and payment secrets server-side.
- Redact personal data from application logs and agent traces.
- Provide account export and deletion workflows.
- Establish data-retention rules for uploaded documents, prompts, embeddings, generated artifacts and audit events.
- Complete a privacy/security review before public launch.

MCP and partner integrations must use explicit scopes, token audience validation and authorization on every request. Never forward a user's incoming access token to a downstream service.

---

## 7. SaaS billing, plans and entitlements

### Entitlement engine

Do not make plan checks as scattered \`if plan == ...\` conditions in Flutter. Implement a server-side entitlement service.

Example entitlement keys:
- \`resume.active_count\`
- \`resume.pdf_exports_monthly\`
- \`ai.summary_rewrites_monthly\`
- \`ats.analyses_monthly\`
- \`job.tailoring_monthly\`
- \`interview.sessions_monthly\`
- \`soulmind.guided_sessions\`
- \`recruiter.seats\`
- \`recruiter.active_jobs\`
- \`integrations.api_requests_monthly\`

The API returns the user's current entitlements and remaining allowances. The UI explains limits before an action is run.

### Billing lifecycle

Model:
- plans and price versions;
- subscriptions;
- one-time purchases;
- payment provider customer references;
- invoices / receipts;
- payment webhook events;
- entitlements and feature grants;
- trials, refunds, grace periods and expiry;
- AI credit ledger and usage events.

Start with the payment provider that best supports the initial India launch, behind a payment abstraction. Add international payment providers when expanding to more markets. Verify payment webhooks server-side and make event handling idempotent.

Recruiter SaaS can later use seats, job volume, API usage and integration tiers. Avoid setting final price points until cost and willingness-to-pay are tested.

---

## 8. API-first integration architecture

### Public API

Use FastAPI with OpenAPI documentation and a stable, versioned public surface.

Example route groups:
- \`/api/v1/auth/*\` (identity provider callbacks where necessary)
- \`/api/v1/me/*\`
- \`/api/v1/profiles/*\`
- \`/api/v1/documents/*\`
- \`/api/v1/jobs/*\`
- \`/api/v1/matches/*\`
- \`/api/v1/applications/*\`
- \`/api/v1/organizations/*\`
- \`/api/v1/recruiter/*\`
- \`/api/v1/integrations/*\`
- \`/api/v1/entitlements/*\`

API requirements:
- OpenAPI contract checked in CI.
- Pagination, filtering and sorting conventions.
- Idempotency keys for write operations.
- Consistent error response schema.
- Request correlation IDs.
- Rate limits and quotas.
- OAuth scopes and role checks.
- Backward compatibility and deprecation policy.
- Sandbox environment and sample data.
- API changelog and partner documentation.

### Webhooks

Event examples:
- \`profile.share_granted\`
- \`profile.share_revoked\`
- \`candidate.application_created\`
- \`candidate.application_updated\`
- \`job.created\`
- \`match.report_ready\`
- \`document.export_ready\`

Webhook deliveries must be signed, retried with backoff, idempotently consumable, replayable by authorized administrators, and visible in an integration log.

### ATS connector strategy

Do not attempt to integrate with every ATS at launch.

Build a connector adapter interface:
- authentication;
- import job;
- export candidate profile;
- submit application only where explicitly supported and authorized;
- map external IDs;
- refresh tokens;
- reconcile status;
- retry transient failures;
- audit data movement.

Prioritize a small number of partner integrations based on customer demand and accessible partner APIs. Provide CSV and standardized JSON exports as fallbacks.

### Candidate data portability

Create a canonical internal career profile and adapters for external standards. Evaluate the HR Open Standards Trusted Career Profile (TCP) as an interoperability target for skills, employment, education and credentials. Keep SoulSkill's internal model independent of a single external schema and version all import/export mappings.

---

## 9. LLM platform

### Model gateway

All model calls go through a server-side provider adapter. Product services must not call a provider SDK directly.

Responsibilities:
- provider and model routing;
- prompt version management;
- typed structured output validation;
- token and cost metering;
- timeout, retry and fallback policy;
- sensitive information minimization;
- prompt-injection defenses;
- content and policy checks;
- evaluation hooks and trace correlation.

Support one primary provider for the first release and a second adapter after model quality, cost and operational requirements justify it. Provider independence is an architectural boundary, not a reason to run every provider at once.

### Structured outputs

Define Pydantic response schemas for:
- resume improvements;
- evidence mapping;
- job requirement extraction;
- skill-gap reports;
- ATS findings;
- career plans;
- SOP suggestions;
- SoulCoach responses.

The AI must return claims linked to source evidence where applicable. If a required fact is missing, ask the user rather than invent it.

---

## 10. RAG architecture

Use RAG where retrieval materially improves factual grounding. Do not use RAG as a substitute for deterministic business logic.

### Initial knowledge collections

1. **Candidate-private knowledge:** user's own profile facts, documents and approved notes.
2. **Product knowledge:** SoulSkill help, feature documentation, policies and onboarding information.
3. **Career knowledge:** licensed or public career guidance, skill taxonomies and role information with source attribution.
4. **Admissions knowledge:** university and program requirements, indexed with URL/source, country, program, effective date and review timestamp.
5. **Recruiter knowledge:** organization-owned job descriptions and hiring documents, isolated to that organization.

### Pipeline

1. Upload with explicit user action and malware/file validation.
2. Extract text and structured metadata.
3. Preserve source document and page/section location.
4. Chunk by semantic section, not arbitrary fixed windows alone.
5. Generate embeddings through a versioned embedding provider.
6. Store embeddings plus ownership, tenant, access scope, source and freshness metadata.
7. Retrieve using tenant/user filters before ranking.
8. Combine lexical and vector retrieval where useful.
9. Re-rank and enforce access checks.
10. Provide citations or source references for factual responses.

### Vector storage

Start with PostgreSQL + pgvector if workload and isolation needs are met. Keep embeddings in the same security boundary as the source records, or ensure retrieval performs a mandatory ownership filter before any result is returned.

Never place a user's resume content into a global vector index without a clear, consented product purpose and strict retrieval isolation.

RAG sources must have provenance and freshness. Admissions deadlines, visa rules and job openings can become stale; show the source and last-checked date and ask users to confirm critical requirements on the official site.

---

## 11. Multi-agent orchestration

### Recommended starting point

Use LangGraph for stateful, multi-step workflows where checkpoints, retries and human approval are useful. Keep each agent narrow and use deterministic services for rules, calculations and database changes.

Do not create an autonomous agent swarm that can freely edit profiles, submit applications, message recruiters or purchase services.

### Proposed agents

| Agent | Responsibility | Allowed tools |
|---|---|---|
| Intake / Router | Classify user goal and choose workflow | Read profile metadata, route task |
| Profile Analyst | Extract and normalize candidate evidence | Read authorized profile/docs |
| Job Analyst | Parse job requirements | Job parser, approved source retrieval |
| ATS Analyst | Map evidence to requirements and explain gaps | Matching engine, read-only profile |
| Resume Coach | Draft truthful, role-specific improvements | Draft document, never overwrite without approval |
| Admissions Coach | Assist academic CV/SOP against selected program criteria | Program RAG, draft document |
| Interview Coach | Generate role-specific practice and feedback | Approved profile and job context |
| SoulMind Coach | Offer supportive affirmations and reflection | Curated content and opt-in user preferences |
| Quality / Policy Reviewer | Check unsupported claims, privacy and output format | Validation and policy services |

### Workflow example: job-specific resume

\`\`\`mermaid
flowchart TD
    A["User selects job and resume"] --> B["Validate access and consent"]
    B --> C["Parse job description"]
    C --> D["Retrieve candidate evidence"]
    D --> E["Map requirements to evidence"]
    E --> F["Calculate deterministic match findings"]
    F --> G["Draft resume improvements"]
    G --> H["Validate truthfulness and ATS structure"]
    H --> I{"User approval"}
    I -->|Approve| J["Save new resume version"]
    I -->|Edit| G
    I -->|Reject| K["Keep original unchanged"]
    J --> L["Export and record usage"]
\`\`\`

### Agent safety

- Define tool allowlists per agent.
- Enforce tenant and user context outside the model.
- Validate every tool input and output.
- Human approval before profile overwrite, external submission, recruiter sharing, payment or outbound messages.
- Restrict agent budgets, turn counts and execution time.
- Make workflows resumable and idempotent.
- Store traces with personal data redacted or minimized.
- Evaluate quality and safety with curated test datasets before releases.

---

## 12. MCP strategy

MCP is an additional integration interface for AI clients and assistants. It does not replace the public REST API, webhooks or native ATS connectors.

### SoulSkill MCP server (future product capability)

Potential read tools:
- \`get_candidate_profile\`
- \`list_candidate_skills\`
- \`get_resume_versions\`
- \`get_job_match_report\`
- \`list_candidate_applications\`

Potential draft tools:
- \`draft_resume_for_job\`
- \`draft_cover_letter\`
- \`prepare_interview_plan\`

Sensitive operations must require explicit consent/approval:
- share candidate profile with an organization;
- update candidate data;
- submit an application;
- send a message;
- change billing or subscription.

Expose resources and prompts where appropriate, with scopes and tenant context. Apply OAuth authorization, audience validation, per-tool permissions, audit logging and rate limits. Do not pass through upstream bearer tokens.

### MCP as a consumer

SoulSkill's internal orchestrator may also consume trusted third-party MCP servers to access approved tools. Start with a small allowlist and explicit user authorization. Treat all external tool outputs as untrusted input.

MCP adoption should be phased after the core API and authorization model are stable.

---

## 13. Background processing and reliability

Long-running operations should not hold open a mobile HTTP request.

Use asynchronous jobs for:
- PDF/DOCX extraction;
- document scanning and parsing;
- embedding generation;
- large RAG ingestion;
- complex multi-agent workflows;
- report export;
- bulk recruiter imports;
- webhook deliveries.

A job should have status, progress, retry policy, timeout, cancellation rules, correlation ID, tenant scope and usage accounting.

Begin with a simple worker architecture. Introduce Redis/Celery or a managed queue when concurrent workloads and retry needs justify it. Keep job interfaces independent of the queue implementation.

---

## 14. Observability, governance and quality

Measure:
- API availability and latency;
- tenant-level error rate;
- document extraction quality;
- RAG retrieval quality and citation coverage;
- resume/ATS suggestion acceptance;
- unsupported-claim rate;
- agent completion and human intervention rate;
- model latency, tokens and cost by feature/plan;
- payment and webhook reliability;
- data-access policy violations.

Use OpenTelemetry-compatible instrumentation and an error monitoring service. Redact candidate data, secrets and document contents from logs and traces. Tracing is for debugging and quality control, not for collecting unnecessary personal information.

Create golden test sets for fresher, experienced, career-switching and academic applicant profiles, including adversarial and incomplete inputs.

---

## 15. Recommended technology choices

| Area | Initial recommendation | Rationale |
|---|---|---|
| Mobile / Web | Flutter + Dart | Preserve current app and share UI code |
| Backend | Python + FastAPI + Pydantic | Existing backend skills and API foundation |
| Database | PostgreSQL | Relational model for profiles, tenants, jobs and billing |
| Authentication | Supabase Auth initially | Faster launch; support OIDC patterns |
| Authorization | PostgreSQL RLS + application RBAC | Defense in depth |
| Vector retrieval | pgvector | Keep initial RAG stack simple |
| Object storage | Private S3-compatible storage / Supabase Storage | Documents with signed access |
| LLM gateway | Provider adapter around official SDKs | Control cost and avoid lock-in |
| Orchestration | LangGraph for complex stateful workflows | Explicit state, checkpoints and approvals |
| MCP | Official MCP SDK / specification-compatible server | Agent ecosystem integration |
| Async jobs | Worker + queue abstraction | Reliable document and AI processing |
| Payments | Payment adapter; India provider first | Local launch, future provider options |
| CI/CD | GitHub Actions | Existing repository workflow |
| Monitoring | OpenTelemetry + error monitoring | Operations and AI workflow visibility |
| Design | Figma + FigJam | Shared design source of truth |

Do not add a vector database, dedicated search cluster, microservices platform or a second agent framework until measurable requirements justify them.

---

## 16. Delivery roadmap

### Phase 0 — Architecture and product foundation
- Approve product requirements and user journeys.
- Define design tokens and Figma file structure.
- Define candidate profile schema and tenant model.
- Create API conventions and threat model.
- Define initial pricing and entitlements.

### Phase 1 — Secure B2C SaaS foundation
- Authentication and onboarding.
- Personal workspace and candidate profile.
- Multi-tenant-ready data schema and RLS.
- Resume Studio migration from local-only storage to user-owned cloud records.
- Plan catalog and entitlement checks.
- PDF/DOCX export and account data export.

### Phase 2 — AI career intelligence
- Model gateway and modern provider SDK.
- Resume and job description structured parsing.
- Evidence-based ATS analysis.
- Basic RAG over candidate documents and curated role knowledge.
- Resume improvement workflow with user approval.
- AI usage ledger and cost controls.

### Phase 3 — SoulMind and SoulCoach
- Curated affirmations and Ho'oponopono reflections.
- Optional personalization with clear privacy controls.
- Interview practice and feedback.
- Career restart guidance and application tracking.

### Phase 4 — Admissions
- Academic CV and SOP workflows.
- Program requirement knowledge base.
- Source attribution and freshness checks.
- Admissions application tracker.

### Phase 5 — Recruiter SaaS
- Organization workspaces and RBAC.
- Candidate consent/share workflows.
- Recruiter job intake and candidate matching.
- Recruiter billing, seat management and audit logs.

### Phase 6 — Integration platform
- Public API v1 and developer portal.
- Webhooks and sandbox.
- First selected ATS connectors.
- Candidate profile export adapter for HR Open Standards Trusted Career Profile.
- OAuth-protected MCP server and partner MCP tools.

### Phase 7 — Scale and enterprise readiness
- Higher-volume worker and retrieval infrastructure.
- Customer-specific retention and isolation options.
- SSO / enterprise provisioning as needed.
- Security audits, operational playbooks and disaster recovery.
- International pricing and localization.

---

## 17. Non-negotiable release gates

No production release that handles real candidate or recruiter data should proceed without:
- RLS and cross-tenant isolation tests;
- authentication and authorization tests;
- secure secret handling;
- file upload validation and malware controls;
- privacy notice, consent and deletion workflows;
- prompt injection and tool abuse tests;
- AI unsupported-claim tests;
- cost and rate limits;
- backup and restore exercise;
- API compatibility tests;
- incident response and audit trail.

Recruiter integrations and AI automation must never silently expose candidate data or take consequential actions without the required authorization.

---

## 18. First implementation slice

The first engineering slice should be deliberately small and verifiable:

1. Add architecture and product documentation.
2. Create a Figma design system and onboarding prototype.
3. Define PostgreSQL migrations for users, workspaces, organizations, memberships and candidate profiles.
4. Add RLS policies and automated isolation tests.
5. Add authenticated profile APIs.
6. Connect Flutter onboarding and home dashboard to authenticated profile state.
7. Retain the current local draft as a resilient offline draft until cloud sync is verified.

Do not implement all agents, MCP, recruiter workflows and billing at once. Establish the security, data and product foundation first; then add AI capabilities in measurable increments.

---

## 19. Architecture decisions to record

| ID | Decision | Status |
|---|---|---|
| ADR-001 | Multi-tenant SaaS with personal and organization workspaces | Proposed |
| ADR-002 | Modular monolith before microservices | Proposed |
| ADR-003 | Candidate profile ownership remains with the individual | Proposed |
| ADR-004 | REST APIs and webhooks are the primary partner integration surface | Proposed |
| ADR-005 | MCP is complementary, not a replacement for REST/ATS connectors | Proposed |
| ADR-006 | PostgreSQL + RLS as initial data isolation boundary | Proposed |
| ADR-007 | RAG retrieval is metadata-filtered by user, tenant and access scope | Proposed |
| ADR-008 | LangGraph for stateful multi-agent workflows after initial AI gateway | Proposed |
| ADR-009 | Human approval for external sharing and consequential actions | Proposed |
| ADR-010 | Provider-independent LLM gateway with one primary provider initially | Proposed |

**Approval note:** These are recommended architectural decisions for review, not implemented infrastructure. Do not treat the presence of this document as evidence that authentication, billing, RLS, MCP, RAG or integrations are already deployed.
