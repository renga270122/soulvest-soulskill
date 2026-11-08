# SoulSkill 2.0 — Sprint 1 Audit & Recovery Plan

**Repository:** [renga270122/soulvest-soulskill](https://github.com/renga270122/soulvest-soulskill)  
**Base branch:** `main`  
**Audit branch:** `chore/soulskill-2.0-sprint-1-audit`  
**Product direction:** Modern Android-first experience; Resume Studio MVP  
**Audit date:** 2026-11-08

## Executive summary

The repository contains a feature-rich Streamlit/Python resume-builder codebase and a partial Flutter project directory. However, the current `main` branch does **not** contain the Flutter application source or Android platform project. The `soulskill_mobile/` directory currently has setup/documentation files, `pubspec.yaml`, a generated plugin metadata file, a build log, and a smoke test that imports `package:soulskill_mobile/main.dart`; there is no tracked `lib/` or `android/` directory.

Therefore, do not begin the visual redesign by assuming the Flutter app is intact. First recover the missing source from a local working copy, another branch, release artifact, or backup. If recovery is impossible, reconstruct the Flutter MVP against the existing FastAPI contract while preserving the Streamlit application.

## Repository facts verified on 2026-11-08

- Default branch: `main`; repository is public.
- Only one branch was returned by the branch search: `main`.
- `soulskill_mobile/` has 13 tracked entries; no `lib/` or `android/` source tree.

- GitHub path-specific commit history queries for `soulskill_mobile/lib/main.dart` and `soulskill_mobile/android/app/src/main/AndroidManifest.xml` returned no commits. The branch search returned only `main`; no tracked Flutter source was found in the searched repository history. Recovery therefore likely requires a local workspace, backup, or external artifact.
- `soulskill_mobile/pubspec.yaml` declares Flutter, `http`, `shared_preferences`, and `provider`; Dart SDK constraint is `>=3.1.0 <4.0.0`.
- `soulskill_mobile/test/widget_test.dart` imports `package:soulskill_mobile/main.dart`, but the corresponding source is absent from the current branch.
- `soulskill_mobile/build_error.log` records prior compile errors in `lib/screens/resume_form_page.dart`: `onChanged` was supplied to `InputDecoration` rather than a text field, plus a malformed collection-if/null-coalescing expression requiring correction.
- Root `api_server.py` and `api.py` both create FastAPI applications. These are separate app definitions and expose overlapping but non-identical routes/contracts. Select and document one canonical API entry point before connecting a rebuilt client.
- Root `requirements.txt` includes Streamlit, FastAPI, Uvicorn, Pydantic, AI/document and data packages. `soulskill_mobile/api_requirements.txt` also exists and should be compared before deployment.
- Root `database.py` supports JSON fallback plus optional PostgreSQL/MongoDB. It silently falls back to local JSON when DB setup fails. This is not a safe production persistence strategy.
- Root `auth.py` imports Streamlit and relies on `st.session_state`, so it is not a reusable stateless authentication service for a Flutter API. It uses a static default password salt if an environment variable is absent.
- Root `.github/workflows/test.yml` references `test_app.py` and `test_e2e.py`; its E2E job expects Playwright. The workflow has not been executed as part of this read-only GitHub audit.

## Sprint 1 goal

Establish a reproducible, buildable Flutter + FastAPI development baseline and produce an evidence-based design/implementation plan for the Resume Studio MVP. No production database migration, destructive cleanup, or Streamlit replacement is in scope.

## Work items

| ID | Priority | Task | Acceptance criteria |
|---|---|---|---|
| S1-01 | P0 | Recover Flutter source | Locate original `lib/`, `android/`, assets and lockfile; restore to a dedicated branch; confirm source provenance. If not recoverable, explicitly approve a clean Flutter scaffold. |
| S1-02 | P0 | Establish reproducible Android build | Pin Flutter/Dart toolchain; `flutter pub get`, `flutter analyze`, `flutter test` and debug APK build all pass. |
| S1-03 | P0 | Select canonical backend | Choose `api.py` or `api_server.py`; document how to run it; avoid two competing production app entry points. |
| S1-04 | P0 | Define API contract | Document resume schema, request/response examples, error format, upload limits and API base URL configuration. Add contract tests for client-consumed endpoints. |
| S1-05 | P1 | Separate API auth from Streamlit auth | Implement stateless API authentication and authorization; do not reuse Streamlit session state. Protect all per-user resume operations with authenticated user identity, not a caller-supplied email. |
| S1-06 | P1 | Persistence readiness | Define one production database strategy; remove silent production JSON fallback; add migrations, user ownership and backup plan before multi-user launch. |
| S1-07 | P1 | Design system specification | Document typography, color tokens, spacing, radii, buttons, input states, cards and navigation for the modern SoulSkill visual direction. |
| S1-08 | P1 | Resume Studio UX specification | Define dashboard, create/import flow, section editor, autosave state, live preview, template selection, ATS feedback and PDF export. |
| S1-09 | P2 | CI verification | Run existing workflow; separate Python and Flutter jobs; ensure paths and test commands match tracked files. |
| S1-10 | P2 | Dependency/security review | Identify outdated packages, generated artifacts accidentally tracked, secret/config risks and upload validation needs. |

## Sprint 1 exit criteria

1. Original Flutter source recovered or a replacement scaffold explicitly selected.
2. Flutter debug build, analyzer and tests pass in a documented environment.
3. One canonical FastAPI app is selected and starts successfully.
4. Client/API contract is documented and covered by tests.
5. Authentication and persistence gaps have prioritized remediation plans.
6. Resume Studio MVP wireframe and design tokens are ready for implementation.
7. CI runs the relevant Python and Flutter checks.

## Resume Studio MVP — proposed scope

1. **Home:** welcome/profile summary, resume status, primary create/import action, recent documents.
2. **My Resume:** create, edit, duplicate, rename, delete and manage versions.
3. **Structured editor:** contact, summary, experience, education, skills, projects and certifications.
4. **Live preview:** mobile-friendly preview and page-aware PDF preview.
5. **AI assistance:** improve summary and experience bullets; suggest skills; require user review before applying generated text.
6. **ATS review:** explain score and recommendations; avoid guaranteeing job outcomes.
7. **Export:** PDF first; DOCX only after layout fidelity is tested.
8. **Persistence:** local draft support initially; authenticated cloud sync only after API identity/ownership is fixed.

Out of MVP: job board, career mentor, interview simulator, payments/subscription changes, collaboration and broad career-learning modules.

## Recommended architecture guardrails

- Flutter remains the Android client; do not migrate to React/Capacitor for the Android app.
- Keep existing Streamlit deployment available while the mobile product is rebuilt.
- Reuse pure Python AI/business logic behind service functions; do not make Flutter depend on Streamlit modules or session state.
- The API owns AI credentials, authorization, validation and persistence.
- Flutter owns presentation, form state, offline draft UX and API integration.
- Use environment-based API configuration; emulator localhost and physical-device URLs must not be hard-coded into release builds.
- Do not store LLM/API secrets in the APK.
- Add tests for resume serialization, ownership checks, AI endpoint validation, offline drafts and PDF generation.

## Immediate developer commands

From a restored Flutter project:

```bash
cd soulskill_mobile
flutter doctor -v
flutter --version
dart --version
flutter pub get
flutter analyze
flutter test
flutter build apk --debug
```

For the selected FastAPI entry point (after dependencies are installed):

```bash
python -m pip install -r requirements.txt
uvicorn <selected_module>:app --host 127.0.0.1 --port 8000
```

Use a local `.env` file excluded from Git. Never commit production credentials or signing keys.

## Audit limitations

This audit inspected repository metadata, the recursive tree, key configuration/source files and the committed mobile build log using GitHub. It did not run code, install dependencies, build an APK, execute tests, inspect deployment secrets, or validate the live service. Those checks belong to the next execution stage in a real development environment.
