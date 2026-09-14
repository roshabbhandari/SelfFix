from tools import MAX_OUTPUT_CHARS, run_shell


def test_shell_output_is_bounded(tmp_path):
    result = run_shell(str(tmp_path), "python -c \"print('x' * 20000)\"")
    assert len(result) <= MAX_OUTPUT_CHARS * 2 + 100
    assert "exit code 0" in result
