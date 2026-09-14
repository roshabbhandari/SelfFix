from tools import search_codebase


def test_search_codebase_finds_case_insensitive_matches(tmp_path):
    (tmp_path / "app.py").write_text("def RunTask():\n    return True\n")
    result = search_codebase(str(tmp_path), "runtask")
    assert "app.py:1:" in result
    assert "RunTask" in result


def test_search_codebase_reports_no_match(tmp_path):
    (tmp_path / "app.py").write_text("value = 10\n")
    assert search_codebase(str(tmp_path), "missing") == "No matches found."
