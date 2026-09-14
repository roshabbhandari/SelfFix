from tools import run_tests


def test_run_tests_passes_for_valid_suite(tmp_path):
    (tmp_path / "test_sample.py").write_text("def test_ok():\n    assert 2 + 2 == 4\n")
    result = run_tests(str(tmp_path), "test_sample.py")
    assert result["passed"] is True


def test_run_tests_fails_for_failing_suite(tmp_path):
    (tmp_path / "test_sample.py").write_text("def test_bad():\n    assert False\n")
    result = run_tests(str(tmp_path), "test_sample.py")
    assert result["passed"] is False
