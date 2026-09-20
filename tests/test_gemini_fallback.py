from types import SimpleNamespace

from src.ai_processing import gemini_utils


def test_generate_with_fallback_switches_after_quota_error(monkeypatch):
    calls = []

    class Models:
        def generate_content(self, *, model, contents):
            calls.append(model)
            if model == "primary-model":
                raise RuntimeError("429 RESOURCE_EXHAUSTED: quota exceeded")
            return SimpleNamespace(text="ok")

    monkeypatch.setattr(
        gemini_utils,
        "client",
        SimpleNamespace(models=Models()),
    )
    monkeypatch.setattr(
        gemini_utils,
        "FALLBACK_MODELS",
        ("fallback-model",),
    )
    monkeypatch.setenv("GEMINI_MODEL", "primary-model")

    response = gemini_utils.generate_with_fallback("prompt", retry=1)

    assert response.text == "ok"
    assert calls == ["primary-model", "fallback-model"]
