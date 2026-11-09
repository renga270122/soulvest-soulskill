"""Evidence-preserving resume parsing and job-fit analysis for SoulSkill.

This module is deterministic: it never invents qualifications, skills, dates,
employers, metrics, or achievements.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import Any

MAX_RESUME_CHARS = 80_000
STOP_WORDS = {
    "about", "above", "across", "after", "again", "against", "also", "among",
    "and", "any", "are", "around", "with", "within", "without", "will", "would",
    "should", "could", "have", "having", "been", "being", "from", "that", "this",
    "they", "them", "their", "there", "these", "those", "then", "than", "into",
    "onto", "over", "under", "such", "your", "you", "our", "who", "what", "when",
    "where", "which", "while", "work", "working", "role", "team", "company",
    "candidate", "responsibilities", "responsibility", "required", "requirements",
    "preferred", "strong", "good", "ability", "skills", "experience", "years",
    "knowledge", "understanding", "including", "using", "etc", "must", "plus",
    "looking", "seeking", "support", "ensure", "develop", "provide", "business",
    "solutions", "environment", "opportunity", "join", "ideal",
}
SKILL_PHRASES = (
    "embedded c", "embedded c++", "c++", "c#", "python", "java", "javascript",
    "typescript", "dart", "flutter", "react", "angular", "node.js", "sql",
    "postgresql", "mysql", "mongodb", "aws", "amazon web services", "azure",
    "google cloud", "docker", "kubernetes", "linux", "embedded linux", "rtos",
    "freertos", "stm32", "arm cortex", "device drivers", "driver development",
    "firmware development", "firmware", "board bring-up", "uart", "spi", "i2c",
    "can bus", "bluetooth low energy", "ble", "internet of things", "iot",
    "continuous integration", "continuous deployment", "ci/cd", "jenkins",
    "github actions", "git", "cmake", "unit testing", "integration testing",
    "google test", "gtest", "static analysis", "code review", "debugging",
    "system design", "data structures", "algorithms", "machine learning",
    "deep learning", "generative ai", "large language models", "llm",
    "prompt engineering", "data analysis", "power bi", "tableau", "excel",
    "project management", "product management", "stakeholder management",
    "agile", "scrum", "leadership", "communication", "customer service",
    "salesforce", "crm", "seo", "digital marketing", "financial analysis",
    "accounting", "recruitment", "human resources", "patient care",
    "curriculum development", "quality assurance", "regulatory compliance",
)
SECTION_ALIASES = {
    "summary": {"summary", "professional summary", "profile", "career objective", "objective", "about me"},
    "experience": {"experience", "work experience", "professional experience", "employment history", "work history"},
    "education": {"education", "academic background", "qualifications", "academic qualifications"},
    "skills": {"skills", "technical skills", "key skills", "core competencies", "competencies"},
    "projects": {"projects", "key projects", "personal projects"},
    "certifications": {"certifications", "certificates", "licenses"},
}


def _plain(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (str, int, float)):
        return str(value).strip()
    return ""


def parse_resume_text(text: str) -> dict[str, Any]:
    """Extract a conservative first-pass profile from selectable resume text."""
    if not text or not text.strip():
        raise ValueError("No readable text was found in the resume.")
    if len(text) > MAX_RESUME_CHARS:
        raise ValueError("The extracted resume text is too long to process.")

    lines = [re.sub(r"\s+", " ", line).strip() for line in text.replace("\r", "\n").split("\n")]
    lines = [line for line in lines if line]
    sections: dict[str, list[str]] = {key: [] for key in SECTION_ALIASES}
    active_section: str | None = None
    header_lookup = {
        re.sub(r"[^a-z ]", "", alias.lower()): section
        for section, aliases in SECTION_ALIASES.items()
        for alias in aliases
    }

    for line in lines:
        normalized = re.sub(r"[^a-z ]", "", line.lower()).strip()
        header = header_lookup.get(normalized)
        if header:
            active_section = header
            continue
        if active_section:
            sections[active_section].append(line)

    joined = "\n".join(lines)
    email_match = re.search(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", joined, re.I)
    phone_match = re.search(r"(?<!\w)(?:\+\d{1,3}[\s.-]?)?(?:\(?\d{2,5}\)?[\s.-]?)?\d[\d\s.-]{6,}\d(?!\w)", joined)

    ignored_headers = {alias for aliases in SECTION_ALIASES.values() for alias in aliases}
    name = ""
    for line in lines[:7]:
        normalized = re.sub(r"[^a-z ]", "", line.lower()).strip()
        if (len(line.split()) <= 5 and len(line) >= 3 and "@" not in line
                and not any(char.isdigit() for char in line)
                and normalized not in ignored_headers
                and not re.search(r"\b(resume|curriculum vitae|linkedin|github)\b", line, re.I)):
            name = line
            break

    def clean_section(section_name: str) -> str:
        return "\n".join(sections[section_name]).strip()

    experience_lines = sections["experience"]
    experience_role = ""
    company = ""
    if experience_lines:
        first = experience_lines[0].strip("•*- ")
        parts = [part.strip() for part in re.split(r"\s+[|•]\s+", first) if part.strip()]
        if parts:
            experience_role = parts[0][:120]
        if len(parts) > 1:
            company = parts[1][:120]

    education_lines = sections["education"]
    degree = education_lines[0][:180] if education_lines else ""
    institution = education_lines[1][:180] if len(education_lines) > 1 else ""
    skills_text = clean_section("skills")
    skills = [item.strip(" •-*") for item in re.split(r"[,;|\n•]", skills_text) if item.strip(" •-*")]
    skills = list(dict.fromkeys(skills))[:60]

    return {
        "fullName": name,
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0).strip() if phone_match else "",
        "location": "",
        "professionalSummary": clean_section("summary"),
        "experienceRole": experience_role,
        "company": company,
        "experienceDescription": "\n".join(experience_lines[1:]).strip() if experience_role and experience_lines else clean_section("experience"),
        "degree": degree,
        "institution": institution,
        "educationDetails": clean_section("education"),
        "skills": ", ".join(skills),
        "extractedTextLength": len(text),
        "needsReview": True,
    }


def _resume_text(resume: dict[str, Any]) -> str:
    parts: list[str] = []
    for key in (
        "name", "full_name", "fullName", "target_role", "targetRole", "email", "phone",
        "location", "professional_summary", "professionalSummary", "summary",
        "experience_role", "experienceRole", "company", "experience_description",
        "experienceDescription", "degree", "institution", "education_details",
        "educationDetails", "skills",
    ):
        value = resume.get(key)
        if isinstance(value, str) and value.strip():
            parts.append(value.strip())

    for key in ("work_experience", "work_history", "education", "projects", "certifications"):
        values = resume.get(key, [])
        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict):
                    parts.extend(_plain(value) for value in item.values() if _plain(value))
                elif _plain(item):
                    parts.append(_plain(item))
    if isinstance(resume.get("skills"), list):
        parts.extend(_plain(item) for item in resume["skills"] if _plain(item))
    return "\n".join(parts)


def _contains_term(text: str, term: str) -> bool:
    if term in {"c++", "c#", "ci/cd", "node.js", "i2c", "spi", "uart", "ble", "iot", "llm"}:
        return term in text
    return bool(re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", text))


def _job_terms(job_description: str) -> list[str]:
    text = job_description.lower()
    terms: list[str] = []
    for phrase in SKILL_PHRASES:
        if _contains_term(text, phrase):
            terms.append(phrase)
    word_counts = Counter(
        word for word in re.findall(r"[a-z][a-z0-9+#./-]{2,}", text)
        if word not in STOP_WORDS and not word.isdigit()
    )
    for word, frequency in word_counts.most_common(50):
        if frequency >= 2 or len(word) >= 7:
            if word not in terms:
                terms.append(word)
    return terms[:30]


def analyze_resume_for_job(
    resume: dict[str, Any], job_description: str, target_role: str = ""
) -> dict[str, Any]:
    """Return explainable keyword alignment and a fact-preserving tailored draft."""
    job_description = (job_description or "").strip()
    if len(job_description) < 50:
        raise ValueError("Paste a complete job description (at least 50 characters).")
    if len(job_description) > 20_000:
        raise ValueError("The job description is too long. Keep it under 20,000 characters.")

    source_text = _resume_text(resume)
    if not source_text.strip():
        raise ValueError("Add or import resume content before analyzing job fit.")

    source_lower = source_text.lower()
    keywords = _job_terms(job_description)
    matched = [term for term in keywords if _contains_term(source_lower, term)]
    missing = [term for term in keywords if term not in matched]
    coverage = round((len(matched) / len(keywords)) * 100) if keywords else 0

    skills_value = resume.get("skills", [])
    if isinstance(skills_value, str):
        skills = [item.strip() for item in re.split(r"[,;|\n]", skills_value) if item.strip()]
    elif isinstance(skills_value, list):
        skills = [_plain(item) for item in skills_value if _plain(item)]
    else:
        skills = []

    skills_sorted = sorted(
        enumerate(skills),
        key=lambda entry: (
            -sum(1 for term in matched if _contains_term(entry[1].lower(), term)),
            entry[0],
        ),
    )
    ordered_skills = [entry[1] for entry in skills_sorted]

    experience = _plain(resume.get("experience_description") or resume.get("experienceDescription"))
    if not experience:
        work = resume.get("work_experience") or resume.get("work_history") or []
        if work and isinstance(work, list) and isinstance(work[0], dict):
            experience = _plain(work[0].get("description"))

    bullets = [line.strip(" •\t-*") for line in re.split(r"[\n•]+", experience) if line.strip(" •\t-*")]
    ranked_bullets = sorted(
        enumerate(bullets),
        key=lambda entry: (
            -sum(1 for term in matched if _contains_term(entry[1].lower(), term)),
            entry[0],
        ),
    )
    prioritized_experience = "\n".join(entry[1] for entry in ranked_bullets) if bullets else experience

    recommendations: list[str] = []
    if missing:
        recommendations.append(
            "Review the job terms not found in your resume. Add a term only when it accurately describes your skills or experience."
        )
    if not _plain(resume.get("professional_summary") or resume.get("professionalSummary") or resume.get("summary")):
        recommendations.append("Add a short professional summary based on your real experience and target role.")
    if not skills:
        recommendations.append("Add a focused skills section using skills you can confidently discuss in an interview.")
    if experience and not re.search(r"\d+%|\b\d+\s*(?:users|customers|projects|devices|teams|hours|days|months|years)\b", experience, re.I):
        recommendations.append("Where you have reliable evidence, add the scale or outcome of your work. Do not estimate or invent metrics.")
    if not recommendations:
        recommendations.append("Your resume contains several of the job's key terms. Review every section for accuracy and relevance before applying.")

    current_role = target_role.strip() or _plain(resume.get("target_role") or resume.get("targetRole"))
    summary = _plain(resume.get("professional_summary") or resume.get("professionalSummary") or resume.get("summary"))
    profile_fields = [
        resume.get("name") or resume.get("full_name") or resume.get("fullName"),
        resume.get("email"),
        resume.get("phone"),
        summary,
        experience,
        resume.get("education"),
        skills,
    ]
    profile_completeness = round(sum(bool(value) for value in profile_fields) / len(profile_fields) * 100)

    tailored_resume = {
        "target_role": current_role,
        "professional_summary": summary,
        "experience_description": prioritized_experience,
        "skills": ordered_skills,
    }
    return {
        "keyword_match_percent": coverage,
        "matched_keyword_count": len(matched),
        "total_keyword_count": len(keywords),
        "matched_keywords": matched,
        "missing_keywords": missing,
        "profile_completeness_percent": profile_completeness,
        "recommendations": recommendations,
        "tailored_resume": tailored_resume,
        "score_explanation": "Keyword coverage is a comparison of terms found in this job description and your resume text. It is not an ATS pass probability or a promise of interview calls.",
        "fact_integrity": "Only existing resume content is reordered. Missing skills and qualifications are never added automatically.",
    }
