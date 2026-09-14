import pytest

import llm


def test_unknown_provider_has_clear_error(monkeypatch):
    monkeypatch.setattr(llm, "LLM_PROVIDER", "unknown")
    with pytest.raises(ValueError, match="Use 'gemini' or 'groq'"):
        llm.call_llm("system", "user")


def test_missing_gemini_key_is_reported(monkeypatch):
    monkeypatch.setattr(llm, "LLM_PROVIDER", "gemini")
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="GEMINI_API_KEY is not set"):
        llm.call_llm("system", "user")
