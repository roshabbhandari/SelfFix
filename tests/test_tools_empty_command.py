from tools import run_shell


def test_run_shell_rejects_empty_command(tmp_path):
    assert run_shell(str(tmp_path), "") == "ERROR: empty command"


def test_run_shell_rejects_unknown_command(tmp_path):
    result = run_shell(str(tmp_path), "not_a_real_command")
    assert "not allowed" in result
