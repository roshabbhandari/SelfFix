import agent


def test_run_stops_after_iteration_limit(tmp_path, monkeypatch):
    monkeypatch.setattr(
        agent,
        "call_llm",
        lambda system_prompt, user_prompt: '{"tool":"unknown","thought":"retry","args":{}}',
    )
    monkeypatch.setattr(agent, "git_diff", lambda repo_root: "")

    result = agent.CodingAgent(str(tmp_path), "issue").run()

    assert result["success"] is False
    assert "iteration limit" in result["summary"]
