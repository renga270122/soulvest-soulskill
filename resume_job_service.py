"""Compatibility exports for the canonical backend resume service.

The FastAPI deployment runs with backend/ as its project root. Keeping
these imports preserves existing Streamlit and test callers at repository root.
"""
from backend.resume_job_service import analyze_resume_for_job, parse_resume_text

__all__ = ["analyze_resume_for_job", "parse_resume_text"]
