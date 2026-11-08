# FastAPI Server for SoulSkill Mobile App
# Provides REST endpoints for Flutter Android app

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from datetime import datetime
import os
from io import BytesIO
from resume_job_service import analyze_resume_for_job, parse_resume_text

# Import existing modules
from ai_assistant import AIResumeAssistant, ATSOptimizer
from ai_advanced import AdvancedAIAssistant, ResumeScoring
from ats_optimizer_pro import EnterpriseATSOptimizer
from template_config import TEMPLATES
from industry_config import INDUSTRY_OPTIONS
from job_examples import get_examples_for_role, get_all_job_roles
from advanced_features import ResumeImporter, KeywordHighlighter, ResumeLengthOptimizer

app = FastAPI(
    title="SoulSkill API",
    description="Backend API for SoulSkill Mobile App",
    version="1.0.0"
)

# Enable CORS for mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ DATA MODELS ============

class ResumeData(BaseModel):
    """Resume data structure"""
    name: str
    email: str
    phone: str
    location: str
    professional_summary: Optional[str] = None
    work_experience: List[Dict[str, str]] = []
    education: List[Dict[str, str]] = []
    skills: List[str] = []
    projects: List[Dict[str, str]] = []
    certifications: Optional[List[str]] = None
    industry: Optional[str] = None
    template_style: str = "modern"

class JobDescription(BaseModel):
    """Job description for matching"""
    title: str
    description: str
    company: str

class ATSCheckRequest(BaseModel):
    """ATS optimization check request"""
    resume_content: str
    job_description: Optional[str] = None

# ============ HEALTH CHECK ============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }

# ============ JOB ROLES & EXAMPLES ============

@app.get("/api/job-roles")
async def get_job_roles():
    """Get all available job roles"""
    try:
        roles = get_all_job_roles()
        return {"status": "success", "roles": roles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/examples/{job_role}")
async def get_examples(job_role: str):
    """Get example content for a specific job role"""
    try:
        examples = get_examples_for_role(job_role)
        return {
            "status": "success",
            "role": job_role,
            "examples": examples
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ TEMPLATES ============

@app.get("/api/templates")
async def get_templates():
    """Get all available resume templates"""
    try:
        return {
            "status": "success",
            "templates": TEMPLATES,
            "count": len(TEMPLATES)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ INDUSTRY OPTIONS ============

@app.get("/api/industries")
async def get_industries():
    """Get all industry options"""
    try:
        return {
            "status": "success",
            "industries": INDUSTRY_OPTIONS
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ AI ASSISTANCE ============

@app.post("/api/ai/improve-summary")
async def improve_summary(request: Dict[str, str]):
    """Improve professional summary using AI"""
    try:
        summary = request.get("summary", "")
        role = request.get("role", "")
        
        if not summary:
            raise HTTPException(status_code=400, detail="Summary is required")
        
        assistant = AIResumeAssistant()
        improved = assistant.improve_professional_summary(summary)
        
        return {
            "status": "success",
            "original": summary,
            "improved": improved
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/improve-experience")
async def improve_experience(request: Dict[str, str]):
    """Improve work experience description using AI"""
    try:
        description = request.get("description", "")
        if not description:
            raise HTTPException(status_code=400, detail="Description is required")
        
        assistant = AIResumeAssistant()
        improved = assistant.improve_work_experience(description)
        
        return {
            "status": "success",
            "original": description,
            "improved": improved
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ai/suggest-skills")
async def suggest_skills(request: Dict[str, str]):
    """Suggest skills for a job role"""
    try:
        role = request.get("role", "")
        existing_skills = request.get("existing_skills", "").split(",")
        
        if not role:
            raise HTTPException(status_code=400, detail="Role is required")
        
        assistant = AIResumeAssistant()
        suggestions = assistant.suggest_skills(role, existing_skills)
        
        return {
            "status": "success",
            "role": role,
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ ATS OPTIMIZATION ============

@app.post("/api/ats/check")
async def check_ats(request: ATSCheckRequest):
    """Check ATS compatibility and get score"""
    try:
        optimizer = EnterpriseATSOptimizer()
        score = optimizer.calculate_ats_score(
            request.resume_content,
            request.job_description
        )
        
        return {
            "status": "success",
            "score": score,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ats/suggestions")
async def get_ats_suggestions(request: ATSCheckRequest):
    """Get ATS improvement suggestions"""
    try:
        optimizer = EnterpriseATSOptimizer()
        suggestions = optimizer.get_improvement_suggestions(
            request.resume_content,
            request.job_description
        )
        
        return {
            "status": "success",
            "suggestions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ KEYWORD ANALYSIS ============

@app.post("/api/keywords/analyze")
async def analyze_keywords(request: Dict[str, str]):
    """Analyze keyword match between resume and job description"""
    try:
        resume_text = request.get("resume", "")
        job_text = request.get("job_description", "")
        
        if not resume_text or not job_text:
            raise HTTPException(status_code=400, detail="Resume and job description are required")
        
        highlighter = KeywordHighlighter()
        matched, missing = highlighter.find_missing_keywords(resume_text, job_text)
        
        return {
            "status": "success",
            "matched_keywords": matched,
            "missing_keywords": missing,
            "match_percentage": (len(matched) / (len(matched) + len(missing)) * 100) if (len(matched) + len(missing)) > 0 else 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ RESUME LENGTH ============

@app.post("/api/resume/optimize-length")
async def optimize_length(request: Dict[str, str]):
    """Get recommendations for optimal resume length"""
    try:
        content = request.get("content", "")
        if not content:
            raise HTTPException(status_code=400, detail="Resume content is required")
        
        optimizer = ResumeLengthOptimizer()
        recommendations = optimizer.get_length_recommendations(content)
        
        return {
            "status": "success",
            "recommendations": recommendations,
            "word_count": len(content.split())
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ RESUME SCORING ============

@app.post("/api/resume/score")
async def score_resume(resume: ResumeData):
    """Calculate overall resume score"""
    try:
        scorer = ResumeScoring()
        resume_dict = resume.dict()
        score = scorer.calculate_resume_score(resume_dict)
        
        return {
            "status": "success",
            "score": score,
            "details": scorer.get_score_breakdown(resume_dict)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ============ SAVE & LOAD ============

@app.post("/api/resume/save")
async def save_resume(resume: ResumeData):
    """Save resume to local storage (filename will be user_id in production)"""
    try:
        resume_data = resume.dict()
        filename = f"resume_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # In production, save to database with user_id
        with open(filename, 'w') as f:
            json.dump(resume_data, f, indent=2)
        
        return {
            "status": "success",
            "message": "Resume saved successfully",
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============ RESUME IMPORT AND JOB FIT ============

class JobFitRequest(BaseModel):
    resume: Dict[str, Any]
    job_description: str
    target_role: Optional[str] = None


@app.post("/api/resume/parse")
async def parse_resume_upload(file: UploadFile = File(...)):
    """Extract selectable text from a PDF, DOCX or TXT resume without storing it."""
    filename = (file.filename or "").strip()
    extension = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if extension not in {"pdf", "docx", "txt"}:
        raise HTTPException(status_code=415, detail="Upload a PDF, DOCX or TXT resume.")

    content = await file.read(5 * 1024 * 1024 + 1)
    await file.close()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Resume file must be 5 MB or smaller.")
    if not content:
        raise HTTPException(status_code=400, detail="The selected resume file is empty.")

    try:
        if extension == "pdf":
            try:
                from pypdf import PdfReader
            except ImportError:
                from PyPDF2 import PdfReader
            reader = PdfReader(BytesIO(content))
            if reader.is_encrypted:
                try:
                    reader.decrypt("")
                except Exception:
                    raise HTTPException(status_code=422, detail="This PDF is password protected. Upload an unlocked copy.")
            extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
        elif extension == "docx":
            from docx import Document
            document = Document(BytesIO(content))
            paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
            table_text = [
                " | ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
                for table in document.tables for row in table.rows
            ]
            extracted = "\n".join(paragraphs + table_text)
        else:
            extracted = content.decode("utf-8-sig")
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=422, detail="We could not read this file. Try a text-based PDF, DOCX or TXT file.")

    if not extracted.strip():
        raise HTTPException(
            status_code=422,
            detail="No selectable text was found. This may be a scanned PDF; paste the resume text or use an OCR-ready copy.",
        )

    try:
        parsed = parse_resume_text(extracted)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))
    return {
        "status": "success",
        "filename": filename,
        "resume": parsed,
        "review_required": True,
        "message": "Review the extracted fields and correct anything that was interpreted incorrectly.",
    }


@app.post("/api/resume/job-fit")
async def analyze_resume_job_fit(request: JobFitRequest):
    """Compare a resume with a target job and return fact-preserving tailoring guidance."""
    try:
        result = analyze_resume_for_job(
            request.resume,
            request.job_description,
            request.target_role or "",
        )
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error))
    return {"status": "success", **result}

# ============ ROOT ============

@app.get("/")
async def root():
    """API documentation"""
    return {
        "name": "SoulSkill API",
        "version": "1.0.0",
        "description": "Backend API for SoulSkill Mobile App",
        "endpoints": {
            "health": "/health",
            "job_roles": "/api/job-roles",
            "templates": "/api/templates",
            "industries": "/api/industries",
            "ats_check": "POST /api/ats/check",
            "ai_improve": "POST /api/ai/*"
        },
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
