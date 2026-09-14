import pytest

import llm


def test_missing_groq_key_is_reported(monkeypatch):
    monkeypatch.setattr(llm, "LLM_PROVIDER", "groq")
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    with pytest.raises(RuntimeError, match="GROQ_API_KEY is not set"):
        llm.call_llm("system", "user")
