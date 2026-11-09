"""FastAPI service for SoulSkill's career workspace.

Resume import/job-fit remain stateless. Authenticated account and profile
endpoints use Supabase Auth and user-scoped PostgREST access.
"""
from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from io import BytesIO
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from .resume_job_service import analyze_resume_for_job, parse_resume_text
    from .profile_api import router as profile_router
except ImportError:
    from resume_job_service import analyze_resume_for_job, parse_resume_text
    from profile_api import router as profile_router

MAX_UPLOAD_BYTES = 4 * 1024 * 1024
MAX_RESUME_JSON_CHARS = 80_000


def _cors_settings() -> dict[str, Any]:
    env = os.getenv("SOULSKILL_ENV", "development").strip().lower()
    origins = [
        value.strip().rstrip("/")
        for value in os.getenv("SOULSKILL_CORS_ORIGINS", "").split(",")
        if value.strip()
    ]
    local_regex = r"^https?://(localhost|127\.0\.0\.1)(:\d+)?$"
    return {
        "allow_origins": origins,
        "allow_origin_regex": local_regex if env not in {"production", "prod"} and not origins else None,
        "allow_credentials": False,
        "allow_methods": ["GET", "POST", "PATCH", "OPTIONS"],
        "allow_headers": ["Authorization", "Content-Type", "X-Request-ID"],
        "expose_headers": ["X-Request-ID"],
    }


app = FastAPI(
    title="SoulSkill API",
    description="Career workspace APIs, resume import and explainable job-fit analysis.",
    version="0.2.0",
)
app.add_middleware(CORSMiddleware, **_cors_settings())
app.include_router(profile_router)


@app.middleware("http")
async def privacy_headers(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    return response


class JobFitRequest(BaseModel):
    resume: dict[str, Any]
    job_description: str = Field(min_length=50, max_length=20_000)
    target_role: str | None = Field(default=None, max_length=160)


@app.get("/")
async def root():
    return {
        "name": "SoulSkill API",
        "version": app.version,
        "health": "/health",
        "docs": "/docs",
        "capabilities": [
            "resume.parse",
            "resume.job_fit",
            "account.me",
            "profile.read",
            "profile.update",
        ],
        "persistence": "candidate profile only; resume import remains stateless",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "soulskill-api",
        "version": app.version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/resume/parse")
async def parse_resume_upload(file: UploadFile = File(...)):
    """Extract selectable text from PDF/DOCX/TXT, without saving the upload."""
    filename = (file.filename or "").strip()
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in {"pdf", "docx", "txt"}:
        raise HTTPException(status_code=415, detail="Upload a PDF, DOCX or TXT resume.")

    content = await file.read(MAX_UPLOAD_BYTES + 1)
    await file.close()
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="Resume file must be 4 MB or smaller.")
    if not content:
        raise HTTPException(status_code=400, detail="The selected resume file is empty.")

    try:
        if extension == "pdf":
            from pypdf import PdfReader
            reader = PdfReader(BytesIO(content))
            if reader.is_encrypted and not reader.decrypt(""):
                raise HTTPException(
                    status_code=422,
                    detail="This PDF is password protected. Upload an unlocked copy.",
                )
            extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif extension == "docx":
            from docx import Document
            document = Document(BytesIO(content))
            paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
            tables = [
                " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                for table in document.tables
                for row in table.rows
            ]
            extracted = "\n".join(paragraphs + tables)
        else:
            extracted = content.decode("utf-8-sig")
    except HTTPException:
        raise
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=422, detail="The TXT file must use UTF-8 encoding.") from exc
    except Exception as exc:
        raise HTTPException(
            status_code=422,
            detail="We could not read this file. Try a text-based PDF, DOCX or TXT file.",
        ) from exc

    if not extracted.strip():
        raise HTTPException(
            status_code=422,
            detail="No selectable text was found. This may be a scanned PDF; use a text-based file.",
        )

    try:
        parsed = parse_resume_text(extracted)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {
        "status": "success",
        "filename": filename,
        "resume": parsed,
        "review_required": True,
        "message": "Review the extracted fields and correct anything interpreted incorrectly.",
        "storage": "not_saved",
    }


@app.post("/api/resume/job-fit")
async def analyze_resume_job_fit(request: JobFitRequest):
    """Compare a resume to a job description without inventing qualifications."""
    try:
        encoded_resume = json.dumps(request.resume, ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail="Resume data must be valid JSON.") from exc
    if len(encoded_resume) > MAX_RESUME_JSON_CHARS:
        raise HTTPException(status_code=413, detail="Resume content is too large to analyze.")

    try:
        result = analyze_resume_for_job(
            request.resume,
            request.job_description,
            request.target_role or "",
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    return {"status": "success", **result}
