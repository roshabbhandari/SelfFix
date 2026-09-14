from tools import list_files


def test_list_files_returns_python_files(tmp_path):
    (tmp_path / "a.py").write_text("x = 1")
    (tmp_path / "b.txt").write_text("text")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "c.py").write_text("x = 2")

    assert list_files(str(tmp_path)) == ["a.py", "pkg/c.py"]


def test_list_files_ignores_virtualenv(tmp_path):
    ignored = tmp_path / ".venv"
    ignored.mkdir()
    (ignored / "hidden.py").write_text("x = 1")
    assert list_files(str(tmp_path)) == []
