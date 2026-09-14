from agent import CodingAgent


def test_dispatch_finish_returns_finish_marker(tmp_path):
    agent = CodingAgent(str(tmp_path), "issue")
    result = agent._dispatch({"tool": "finish", "args": {"summary": "done"}})
    assert result == "FINISH"


def test_dispatch_unknown_tool_returns_error(tmp_path):
    agent = CodingAgent(str(tmp_path), "issue")
    result = agent._dispatch({"tool": "unknown", "args": {}})
    assert "unknown tool" in result
