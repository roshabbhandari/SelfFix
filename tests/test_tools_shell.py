from tools import run_shell


def test_run_shell_allows_python_version_command(tmp_path):
    result = run_shell(str(tmp_path), "python --version")
    assert "exit code 0" in result
    assert "Python" in result


def test_run_shell_rejects_disallowed_command(tmp_path):
    result = run_shell(str(tmp_path), "echo hello")
    assert "not allowed" in result
