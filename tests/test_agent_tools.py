from agent import CodingAgent


def test_dispatch_read_file(tmp_path):
    (tmp_path / "value.py").write_text("answer = 42\n")
    agent = CodingAgent(str(tmp_path), "issue")
    assert agent._dispatch({"tool": "read_file", "args": {"path": "value.py"}}) == "answer = 42\n"


def test_dispatch_write_file(tmp_path):
    agent = CodingAgent(str(tmp_path), "issue")
    result = agent._dispatch({"tool": "write_file", "args": {"path": "value.py", "content": "x = 1\n"}})
    assert result == "OK: wrote 6 chars to value.py"
    assert (tmp_path / "value.py").read_text() == "x = 1\n"
