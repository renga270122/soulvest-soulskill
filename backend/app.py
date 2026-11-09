"""Small, stateless FastAPI service for SoulSkill's first backend milestone.

This API parses user-supplied resumes in memory and performs deterministic
job-fit analysis. It does not persist files, profiles, or job descriptions.
"""
from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request
from datetime import datetime, timezone
from io import BytesIO
from typing import Any

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

try:
    from .resume_job_service import analyze_resume_for_job, parse_resume_text
except ImportError:
    from resume_job_service import analyze_resume_for_job, parse_resume_text

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
        "allow_methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "X-Request-ID"],
        "expose_headers": ["X-Request-ID"],
    }


app = FastAPI(
    title="SoulSkill API",
    description="Stateless resume import and job-fit analysis for the SoulSkill career workspace.",
    version="0.1.0",
)
app.add_middleware(CORSMiddleware, **_cors_settings())


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


class ImproveSummaryRequest(BaseModel):
    summary: str = Field(default="", max_length=4_000)
    role: str = Field(default="", max_length=160)
    experience: str = Field(default="", max_length=8_000)
    skills: list[str] = Field(default_factory=list, max_length=40)


@app.get("/")
async def root():
    return {
        "name": "SoulSkill API",
        "version": app.version,
        "health": "/health",
        "docs": "/docs",
        "capabilities": ["resume.parse", "resume.job_fit"],
        "persistence": "none",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "soulskill-api",
        "version": app.version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }



@app.post("/api/ai/improve-summary")
async def improve_professional_summary(request: ImproveSummaryRequest):
    """Improve a candidate summary without adding unsupported claims."""
    summary = request.summary.strip()
    experience = request.experience.strip()
    skills = [item.strip()[:80] for item in request.skills if item.strip()][:20]
    role = request.role.strip()

    if not summary and not experience and not skills:
        raise HTTPException(
            status_code=422,
            detail="Add a summary, work experience or skills before generating a professional introduction.",
        )

    api_key = os.getenv("GOOGLE_API_KEY", "").strip()
    if api_key:
        model = os.getenv("GOOGLE_GEMINI_MODEL", "gemini-2.0-flash").strip()
        facts = {
            "target_role": role,
            "existing_summary": summary,
            "experience_evidence": experience,
            "skills_supplied_by_candidate": skills,
        }
        prompt = (
            "Rewrite the candidate's professional resume summary in 3 to 4 concise sentences. "
            "Use only facts explicitly present in the supplied candidate data. Do not invent "
            "years, employers, degrees, certifications, achievements, metrics, seniority or skills. "
            "Do not claim proficiency beyond what the candidate supplied. If information is sparse, "
            "keep the wording appropriately modest. Use a clear, ATS-readable professional tone. "
            "Return only the revised summary. Candidate data: "
            + json.dumps(facts, ensure_ascii=False)
        )
        body = json.dumps({
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "maxOutputTokens": 220},
        }).encode("utf-8")
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            + model + ":generateContent?key=" + api_key
        )
        try:
            req = urllib.request.Request(
                url, data=body, headers={"Content-Type": "application/json"}, method="POST"
            )
            with urllib.request.urlopen(req, timeout=22) as response:
                result = json.loads(response.read().decode("utf-8"))
            improved = (
                result.get("candidates", [{}])[0]
                .get("content", {}).get("parts", [{}])[0].get("text", "").strip()
            )
            if improved:
                return {"status": "success", "improved": improved, "mode": "ai"}
        except (urllib.error.URLError, TimeoutError, ValueError, KeyError, IndexError):
            pass

    # Honest offline fallback: reorganize only the facts the candidate provided.
    clean_summary = re.sub(r"\s+", " ", summary).strip(" .")
    clean_experience = re.sub(r"\s+", " ", experience).strip(" .")
    clean_skills = ", ".join(skills[:8])
    parts = []
    if role:
        parts.append("Career-focused " + role + " professional" if clean_experience else "Aspiring " + role)
    elif clean_experience:
        parts.append("Professional with hands-on experience")
    else:
        parts.append("Motivated candidate")
    if clean_summary:
        parts.append(clean_summary[0].lower() + clean_summary[1:])
    elif clean_experience:
        parts.append(clean_experience)
    if clean_skills:
        parts.append("Skills include " + clean_skills)
    improved = ". ".join(part.strip().rstrip(".") for part in parts if part.strip()) + "."
    return {
        "status": "success",
        "improved": improved,
        "mode": "guided",
        "message": "A structured draft was created from your supplied information. Review it before use.",
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
