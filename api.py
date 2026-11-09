"""
FastAPI Backend for SoulSkill Resume Builder
Provides REST API endpoints for resume operations
"""
from fastapi import FastAPI, HTTPException, Depends, File, UploadFile, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.gzip import GZipMiddleware
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime
import hmac
import hashlib
import json
import os
import io
import uvicorn

# Import our modules
from database import get_db_manager
from auth import AuthManager, SecurityManager
from analytics import get_analytics_tracker
from resume_parser import parse_uploaded_resume
from payment_handler import PaymentHandler, SubscriptionManager, PRICING_PLANS

app = FastAPI(
    title="SoulSkill Resume Builder API",
    description="AI-Powered Resume Builder REST API",
    version="1.0.0"
)


def _get_allowed_origins() -> List[str]:
    origins_env = os.getenv("API_ALLOWED_ORIGINS", "*")
    origins = [origin.strip() for origin in origins_env.split(",") if origin.strip()]
    return origins or ["*"]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Compress larger payloads to reduce bandwidth and improve mobile performance.
app.add_middleware(GZipMiddleware, minimum_size=1000)

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


class PaymentOrderRequest(BaseModel):
    plan_id: str
    user_email: EmailStr


class PaymentVerifyRequest(BaseModel):
    plan_id: str
    user_email: EmailStr
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str


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
async def get_user_resumes(
    user_email: str,
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """Get all resumes for a user"""
    db = get_db_manager()

    resumes = db.get_user_resumes(user_email)
    return resumes[offset:offset + limit]


@app.post("/api/resumes/parse")
async def parse_resume_file(file: UploadFile = File(...)):
    """Parse uploaded resume file"""
    try:
        filename = (file.filename or '').lower()
        if not filename.endswith(('.pdf', '.docx', '.txt')):
            raise HTTPException(status_code=415, detail="Unsupported file format. Upload PDF, DOCX, or TXT.")
        contents = await file.read()
        if not contents:
            raise HTTPException(status_code=400, detail="The uploaded file is empty.")
        if len(contents) > 10 * 1024 * 1024:
            raise HTTPException(status_code=413, detail="Resume file must be 10 MB or smaller.")
        stream = io.BytesIO(contents)
        stream.name = file.filename
        parsed_data = parse_uploaded_resume(stream, api_key=None)
        
        return {
            "success": True,
            "data": parsed_data
        }
    except HTTPException:
        raise
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


# Payment endpoints
@app.post("/api/payments/order")
async def create_payment_order(request: PaymentOrderRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Create payment order for selected plan."""
    if request.plan_id not in PRICING_PLANS or request.plan_id == 'free':
        raise HTTPException(status_code=400, detail="Invalid paid plan selected")

    plan = PRICING_PLANS[request.plan_id]
    amount = plan['price_monthly'] if request.plan_id == 'premium_monthly' else plan['price_yearly']

    payment = PaymentHandler()
    order = payment.create_order(
        amount=amount,
        notes={
            'plan_id': request.plan_id,
            'user_email': request.user_email,
        },
    )

    if not order.get('success'):
        raise HTTPException(status_code=503, detail=order.get('error', 'Unable to create payment order'))

    return {
        'success': True,
        'order': order,
        'plan_id': request.plan_id,
    }


@app.post("/api/payments/verify")
async def verify_payment(request: PaymentVerifyRequest, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify Razorpay payment signature and activate subscription."""
    if request.plan_id not in PRICING_PLANS or request.plan_id == 'free':
        raise HTTPException(status_code=400, detail="Invalid paid plan selected")

    payment = PaymentHandler()
    verified = payment.verify_payment(
        request.razorpay_order_id,
        request.razorpay_payment_id,
        request.razorpay_signature,
    )
    if not verified:
        raise HTTPException(status_code=400, detail="Payment signature verification failed")

    db = get_db_manager()
    subscription = SubscriptionManager(db)
    duration = 1 if request.plan_id == 'premium_monthly' else 12
    subscription.activate_subscription(
        request.user_email,
        request.plan_id,
        request.razorpay_payment_id,
        duration_months=duration,
    )

    return {
        'success': True,
        'message': 'Payment verified and subscription activated',
    }


@app.post("/api/payments/webhook")
async def razorpay_webhook(request: Request):
    """Process Razorpay webhook events with signature verification."""
    webhook_secret = os.getenv('RAZORPAY_WEBHOOK_SECRET', '')
    if not webhook_secret:
        raise HTTPException(status_code=503, detail='Webhook secret not configured')

    raw_body = await request.body()
    signature = request.headers.get('x-razorpay-signature', '')
    expected = hmac.new(
        webhook_secret.encode('utf-8'),
        raw_body,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=401, detail='Invalid webhook signature')

    payload = json.loads(raw_body.decode('utf-8'))
    event = payload.get('event', '')

    if event == 'payment.captured':
        payment_entity = payload.get('payload', {}).get('payment', {}).get('entity', {})
        notes = payment_entity.get('notes', {})
        user_email = notes.get('user_email')
        plan_id = notes.get('plan_id')

        if user_email and plan_id in PRICING_PLANS and plan_id != 'free':
            db = get_db_manager()
            subscription = SubscriptionManager(db)
            duration = 1 if plan_id == 'premium_monthly' else 12
            subscription.activate_subscription(
                user_email,
                plan_id,
                payment_entity.get('id', ''),
                duration_months=duration,
            )

    return {'success': True, 'event': event}


@app.get("/api/subscription/{user_email}")
async def get_subscription(user_email: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current subscription details for user."""
    db = get_db_manager()
    subscription = SubscriptionManager(db)
    return {
        'success': True,
        'subscription': subscription.get_user_subscription(user_email),
    }


if __name__ == "__main__":
    # Run with: python api.py
    # Or: uvicorn api:app --reload --port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
