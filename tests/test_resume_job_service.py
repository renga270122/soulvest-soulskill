import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from resume_job_service import analyze_resume_for_job, parse_resume_text


def test_parse_resume_text_extracts_profile_sections():
    parsed = parse_resume_text(
        "Jane Doe\njane@example.com | +1 415 555 0100\n"
        "PROFESSIONAL SUMMARY\nEmbedded software engineer building firmware.\n"
        "WORK EXPERIENCE\nSenior Engineer | Acme Systems\nBuilt device drivers and tested firmware.\n"
        "EDUCATION\nB.E. Electronics\nExample University\n"
        "SKILLS\nC++, Python, Embedded Linux, RTOS"
    )

    assert parsed["fullName"] == "Jane Doe"
    assert parsed["email"] == "jane@example.com"
    assert "Embedded software engineer" in parsed["professionalSummary"]
    assert "device drivers" in parsed["experienceDescription"]
    assert parsed["skills"] == "C++, Python, Embedded Linux, RTOS"


def test_job_analysis_is_explainable_and_never_adds_missing_skills():
    resume = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "professional_summary": "Embedded software engineer with firmware experience.",
        "experience_description": "Built firmware for embedded Linux devices.\nDebugged UART and SPI interfaces.",
        "skills": ["C++", "Embedded Linux", "UART", "SPI"],
        "education": [{"degree": "B.E. Electronics"}],
    }
    job_description = (
        "We need an embedded firmware engineer with C++, Python, FreeRTOS, "
        "device drivers, UART and SPI debugging experience."
    )

    result = analyze_resume_for_job(resume, job_description, "Senior Firmware Engineer")

    assert result["keyword_match_percent"] > 0
    assert "uart" in result["matched_keywords"]
    assert "python" in result["missing_keywords"]
    assert "Python" not in result["tailored_resume"]["skills"]
    assert result["tailored_resume"]["target_role"] == "Senior Firmware Engineer"
    assert "not an ATS pass probability" in result["score_explanation"]


def test_job_analysis_requires_resume_and_meaningful_job_description():
    try:
        analyze_resume_for_job({}, "This is a valid job description but no profile content.")
    except ValueError as error:
        assert "resume content" in str(error).lower()
    else:
        raise AssertionError("Expected missing-resume validation")

    try:
        analyze_resume_for_job({"name": "Jane"}, "short")
    except ValueError as error:
        assert "complete job description" in str(error).lower()
    else:
        raise AssertionError("Expected job-description validation")
