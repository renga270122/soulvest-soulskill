import re

import pytest

from api_server import _build_cors_settings


def test_development_defaults_allow_only_local_browser_origins():
    settings = _build_cors_settings({"SOULSKILL_ENV": "development"})

    pattern = settings["allow_origin_regex"]
    assert pattern is not None
    assert re.fullmatch(pattern, "http://localhost:55749")
    assert re.fullmatch(pattern, "http://127.0.0.1:3000")
    assert not re.fullmatch(pattern, "https://untrusted.example")
    assert settings["allow_origins"] == []
    assert settings["allow_credentials"] is False


def test_production_requires_explicit_trusted_origin_configuration():
    with pytest.raises(RuntimeError, match="SOULSKILL_CORS_ORIGINS"):
        _build_cors_settings({"SOULSKILL_ENV": "production"})


def test_production_accepts_comma_separated_explicit_origins():
    settings = _build_cors_settings(
        {
            "SOULSKILL_ENV": "production",
            "SOULSKILL_CORS_ORIGINS": (
                "https://app.soulskill.example, https://www.soulskill.example/"
            ),
        }
    )

    assert settings["allow_origins"] == [
        "https://app.soulskill.example",
        "https://www.soulskill.example",
    ]
    assert settings["allow_origin_regex"] is None
    assert settings["allow_credentials"] is False


def test_explicit_origin_regex_can_be_used_for_production():
    settings = _build_cors_settings(
        {
            "SOULSKILL_ENV": "production",
            "SOULSKILL_CORS_ORIGIN_REGEX": r"^https://([a-z0-9-]+\\.)?soulskill\\.example$",
        }
    )

    assert settings["allow_origin_regex"] == (
        r"^https://([a-z0-9-]+\\.)?soulskill\\.example$"
    )
