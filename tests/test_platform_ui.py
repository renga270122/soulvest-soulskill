import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_ui_components_module_loads():
    spec = importlib.util.spec_from_file_location("ui_components", ROOT / "ui_components.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "render_platform_nav")
    assert hasattr(module, "render_readiness_score")
    assert hasattr(module, "render_journey_timeline")
