from backend.app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_summary_improvement_can_create_a_first_summary_from_candidate_facts(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    response = client.post(
        "/api/ai/improve-summary",
        json={
            "summary": "",
            "role": "Junior Python Developer",
            "experience": "",
            "skills": ["Python", "SQL", "Git"],
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "guided"
    assert "Junior Python Developer" in payload["improved"]
    assert "Python" in payload["improved"]
    assert "SQL" in payload["improved"]


def test_summary_improvement_requires_candidate_evidence():
    response = client.post(
        "/api/ai/improve-summary",
        json={"summary": "", "role": "", "experience": "", "skills": []},
    )
    assert response.status_code == 422


def test_summary_improvement_preserves_candidate_facts_in_fallback(monkeypatch):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    response = client.post(
        "/api/ai/improve-summary",
        json={
            "summary": "I build test automation for embedded products.",
            "role": "QA Engineer",
            "experience": "Created Python test scripts.",
            "skills": ["Python", "Google Test"],
        },
    )
    assert response.status_code == 200
    summary = response.json()["improved"]
    assert "Python" in summary
    assert "Google Test" in summary
    assert "10 years" not in summary
