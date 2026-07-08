"""
Career Readiness scoring service for SoulSkill 2.0.
Combines multiple career signals into a weighted readiness score.
"""

from typing import Dict, Tuple


READINESS_WEIGHTS = {
    "resume_quality": 0.20,
    "ats_compatibility": 0.20,
    "technical_skills": 0.15,
    "soft_skills": 0.15,
    "emotional_intelligence": 0.10,
    "interview_readiness": 0.10,
    "career_planning": 0.10,
}


def clamp_score(value: float) -> int:
    """Clamp score to 0-100 and normalize to int."""
    return max(0, min(100, int(round(value))))


def calculate_career_readiness_score(metrics: Dict[str, float]) -> Tuple[int, Dict[str, int], Dict[str, str]]:
    """
    Calculate weighted career readiness score.

    Args:
        metrics: Dict of metric_name -> score (0-100)

    Returns:
        (overall_score, normalized_breakdown, insights)
    """
    normalized = {}
    weighted_total = 0.0

    for key, weight in READINESS_WEIGHTS.items():
        score = clamp_score(float(metrics.get(key, 0)))
        normalized[key] = score
        weighted_total += score * weight

    overall_score = clamp_score(weighted_total)

    highest_area = max(normalized, key=normalized.get)
    lowest_area = min(normalized, key=normalized.get)

    insights = {
        "strength": f"Strongest area: {highest_area.replace('_', ' ').title()} ({normalized[highest_area]}%).",
        "focus": f"Best next focus: {lowest_area.replace('_', ' ').title()} ({normalized[lowest_area]}%).",
        "tone": "You have a solid foundation. Focused improvements this week can meaningfully lift readiness.",
    }

    return overall_score, normalized, insights
