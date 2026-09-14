import agent


def test_run_finishes_when_model_returns_finish(tmp_path, monkeypatch):
    monkeypatch.setattr(
        agent,
        "call_llm",
        lambda system_prompt, user_prompt: '{"tool":"finish","thought":"done","args":{"summary":"fixed"}}',
    )
    monkeypatch.setattr(agent, "git_diff", lambda repo_root: "diff")

    result = agent.CodingAgent(str(tmp_path), "issue").run()

    assert result["success"] is True
    assert result["summary"] == "fixed"
    assert result["diff"] == "diff"
