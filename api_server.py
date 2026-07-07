# FastAPI Server for SoulSkill Mobile App
# Provides REST endpoints for Flutter Android app

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from datetime import datetime
import os

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
