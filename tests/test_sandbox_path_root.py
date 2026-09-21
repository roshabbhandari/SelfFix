from tools import is_path_allowed

def test_sandbox_allows_root_path():
    assert is_path_allowed("/workspace/project", "/workspace/project") is True
