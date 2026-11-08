from types import SimpleNamespace

import pytest

from ai_assistant import AIResumeAssistant


class FakeModel:
    def __init__(self, text):
        self.text = text
        self.prompt = None

    def generate_content(self, prompt):
        self.prompt = prompt
        return SimpleNamespace(text=self.text)


def test_improve_professional_summary_uses_role_and_preserves_source_context():
    assistant = AIResumeAssistant(api_key=None)
    fake_model = FakeModel(
        "Software engineer with experience building embedded applications."
    )
    assistant.enabled = True
    assistant.model = fake_model

    result = assistant.improve_professional_summary(
        summary="I build embedded applications.",
        target_role="Embedded Software Engineer",
    )

    assert result.startswith("Software engineer")
    assert "Embedded Software Engineer" in fake_model.prompt
    assert "I build embedded applications." in fake_model.prompt
    assert "Do not invent" in fake_model.prompt


def test_improve_professional_summary_rejects_empty_input():
    assistant = AIResumeAssistant(api_key=None)

    with pytest.raises(ValueError, match="summary is required"):
        assistant.improve_professional_summary("   ")


def test_improve_professional_summary_reports_missing_provider_configuration():
    assistant = AIResumeAssistant(api_key=None)
    assistant.enabled = False
    assistant.model = None

    with pytest.raises(RuntimeError, match="AI writing is not configured"):
        assistant.improve_professional_summary("I build embedded applications.")
