"""
FastAPI Backend for SoulSkill Resume Builder
Provides REST API endpoints for resume operations
"""
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime
import uvicorn

# Import our modules
from database import get_db_manager
from auth import AuthManager, SecurityManager
from analytics import get_analytics_tracker
from resume_parser import parse_uploaded_resume

app = FastAPI(
    title="SoulSkill Resume Builder API",
    description="AI-Powered Resume Builder REST API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic Models
class ResumeCreate(BaseModel):
    full_name: str
    email: EmailStr
    phone: Optional[str] = None
    city: Optional[str] = None
    summary: Optional[str] = None
    tech_skills: Optional[str] = None
    work_entries: List[Dict] = []
    education_entries: List[Dict] = []
    template: Optional[str] = "Professional Blue"

class ResumeResponse(BaseModel):
    id: str
    data: Dict
    created_at: str
    updated_at: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AnalyticsEvent(BaseModel):
    event_name: str
    properties: Optional[Dict] = None


# Health check
@app.get("/health")
async def health_check():
    """Check API health status"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }


# Authentication endpoints
@app.post("/api/auth/login")
async def login(credentials: UserLogin):
    """Login with email/password"""
    auth = AuthManager()
    
    if auth.login_with_email(credentials.email, credentials.password):
        return {
            "success": True,
            "message": "Login successful",
            "user": auth.get_current_user()
        }
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


# Resume endpoints
@app.post("/api/resumes", response_model=dict)
async def create_resume(resume: ResumeCreate, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Create a new resume"""
    db = get_db_manager()
    
    resume_id = db.save_resume(resume.email, resume.dict())
    
    # Track analytics
    tracker = get_analytics_tracker()
    tracker.track_resume_created(resume.template, resume.email)
    
    return {
        "success": True,
        "resume_id": resume_id,
        "message": "Resume created successfully"
    }


@app.get("/api/resumes/{user_email}", response_model=List[dict])
async def get_user_resumes(user_email: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get all resumes for a user"""
    db = get_db_manager()
    
    resumes = db.get_user_resumes(user_email)
    return resumes


@app.post("/api/resumes/parse")
async def parse_resume_file(file: UploadFile = File(...)):
    """Parse uploaded resume file"""
    try:
        parsed_data = parse_uploaded_resume(file.file, api_key=None)
        
        return {
            "success": True,
            "data": parsed_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Analytics endpoints
@app.post("/api/analytics/track")
async def track_analytics(event: AnalyticsEvent, user_email: Optional[str] = None):
    """Track an analytics event"""
    tracker = get_analytics_tracker()
    tracker.track_event(event.event_name, event.properties, user_email)
    
    return {"success": True, "message": "Event tracked"}


@app.get("/api/analytics/summary")
async def get_analytics_summary(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get analytics summary (admin only)"""
    tracker = get_analytics_tracker()
    return tracker.get_analytics_summary()


# Template endpoints
@app.get("/api/templates")
async def get_templates():
    """Get available resume templates"""
    from template_config import TEMPLATES, INDIAN_TEMPLATES, US_TEMPLATES
    
    all_templates = {}
    all_templates.update(TEMPLATES)
    all_templates.update(INDIAN_TEMPLATES)
    all_templates.update(US_TEMPLATES)
    
    return {
        "success": True,
        "templates": all_templates
    }


# AI endpoints
@app.post("/api/ai/enhance")
async def enhance_content(content: dict, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Enhance resume content with AI"""
    try:
        from ai_assistant import AIResumeAssistant
        
        ai = AIResumeAssistant()
        if not ai.enabled:
            raise HTTPException(status_code=503, detail="AI service not available")
        
        enhanced = ai.enhance_content(content.get('text', ''))
        
        # Track AI usage
        tracker = get_analytics_tracker()
        tracker.track_ai_usage('enhance_content')
        
        return {
            "success": True,
            "enhanced_text": enhanced
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Run with: python api.py
    # Or: uvicorn api:app --reload --port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
