from tools import is_path_allowed


def test_sandbox_allows_nested_paths_inside_root():
    assert is_path_allowed("/workspace/project/file.txt", "/workspace/project") is True
