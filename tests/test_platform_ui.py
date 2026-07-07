import importlib
import importlib.util
import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def test_ui_components_module_loads():
    spec = importlib.util.spec_from_file_location("ui_components", ROOT / "ui_components.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    assert hasattr(module, "render_platform_nav")
    assert hasattr(module, "render_readiness_score")
    assert hasattr(module, "render_journey_timeline")


def test_app_enhanced_imports_with_fallback_panel_helpers(monkeypatch):
    fake_ui_components = types.ModuleType("ui_components")
    fake_ui_components.apply_platform_styles = lambda: None
    fake_ui_components.render_foundation_summary = lambda: None
    fake_ui_components.render_journey_timeline = lambda: None
    fake_ui_components.render_metric_card = lambda *args, **kwargs: None
    fake_ui_components.render_module_card = lambda *args, **kwargs: None
    fake_ui_components.render_placeholder_panel = lambda *args, **kwargs: None
    fake_ui_components.render_platform_nav = lambda *args, **kwargs: None
    fake_ui_components.render_readiness_score = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, "ui_components", fake_ui_components)
    sys.modules.pop("app_enhanced", None)

    app_module = importlib.import_module("app_enhanced")

    assert callable(app_module.render_assessment_panel)
    assert callable(app_module.render_coaching_panel)
    assert callable(app_module.render_eq_panel)
    assert callable(app_module.render_monetization_panel)
