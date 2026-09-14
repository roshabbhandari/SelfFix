from agent import CodingAgent


def test_log_appends_and_returns_entries(tmp_path):
    agent = CodingAgent(str(tmp_path), "issue")
    agent._log("hello")
    agent._log("world")
    assert agent.log == ["hello", "world"]


def test_agent_starts_with_empty_transcript(tmp_path):
    agent = CodingAgent(str(tmp_path), "issue")
    assert agent.transcript == []
