from io import BytesIO

from docx import Document
from fastapi.testclient import TestClient

from backend.app import app

client = TestClient(app)


def test_health_has_privacy_headers():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.headers["cache-control"] == "no-store"
    assert response.headers["x-content-type-options"] == "nosniff"


def test_parse_txt_resume_extracts_fields_and_marks_review_required():
    content = (
        "Jane Doe\njane@example.com | +1 415 555 0100\n"
        "PROFESSIONAL SUMMARY\nExperienced engineering manager leading embedded teams.\n"
        "WORK EXPERIENCE\nEngineering Manager | Acme Systems\nLed firmware delivery and cross-functional teams.\n"
        "EDUCATION\nB.E. Electronics\nExample University\n"
        "SKILLS\nC++, Python, Embedded Linux, RTOS"
    )
    response = client.post(
        "/api/resume/parse",
        files={"file": ("jane_resume.txt", content.encode("utf-8"), "text/plain")},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["resume"]["fullName"] == "Jane Doe"
    assert payload["resume"]["email"] == "jane@example.com"
    assert "Engineering Manager" in payload["resume"]["experienceRole"]
    assert payload["review_required"] is True
    assert payload["storage"] == "not_saved"


def test_parse_docx_resume():
    document = Document()
    document.add_paragraph("Alex Morgan")
    document.add_paragraph("alex@example.com")
    document.add_heading("Skills", level=1)
    document.add_paragraph("Python, SQL, Leadership")
    stream = BytesIO()
    document.save(stream)

    response = client.post(
        "/api/resume/parse",
        files={"file": ("alex_resume.docx", stream.getvalue(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
    )
    assert response.status_code == 200
    assert "Python" in response.json()["resume"]["skills"]


def test_parse_rejects_unsupported_extension():
    response = client.post(
        "/api/resume/parse",
        files={"file": ("resume.exe", b"nope", "application/octet-stream")},
    )
    assert response.status_code == 415


def test_job_fit_is_transparent_and_does_not_add_missing_skills():
    resume = {
        "name": "Jane Doe",
        "professional_summary": "Embedded engineering manager with firmware experience.",
        "experience_description": "Led embedded Linux firmware delivery.\nDebugged UART and SPI interfaces.",
        "skills": ["C++", "Embedded Linux", "UART", "SPI"],
    }
    job_description = (
        "We need an embedded engineering manager with C++, Python, FreeRTOS, "
        "device drivers, UART and SPI debugging experience for cross-functional teams."
    )
    response = client.post(
        "/api/resume/job-fit",
        json={
            "resume": resume,
            "job_description": job_description,
            "target_role": "Senior Embedded Engineering Manager",
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["keyword_match_percent"] > 0
    assert "uart" in payload["matched_keywords"]
    assert "python" in payload["missing_keywords"]
    assert "Python" not in payload["tailored_resume"]["skills"]
    assert payload["tailored_resume"]["target_role"] == "Senior Embedded Engineering Manager"
    assert "not an ATS pass probability" in payload["score_explanation"]


def test_job_fit_validates_short_job_description():
    response = client.post(
        "/api/resume/job-fit",
        json={"resume": {"name": "Jane Doe"}, "job_description": "Too short"},
    )
    assert response.status_code == 422


def test_upload_rejects_empty_txt():
    response = client.post(
        "/api/resume/parse",
        files={"file": ("empty.txt", b"", "text/plain")},
    )
    assert response.status_code == 400
