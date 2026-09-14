from tools import git_diff


def test_git_diff_returns_text_for_git_repository(tmp_path):
    (tmp_path / ".git").mkdir()
    result = git_diff(str(tmp_path))
    assert isinstance(result, str)
