from tools import read_file, write_file


def test_write_and_read_file(tmp_path):
    root = str(tmp_path)
    assert write_file(root, "nested/value.txt", "hello") == "OK: wrote 5 chars to nested/value.txt"
    assert read_file(root, "nested/value.txt") == "hello"


def test_read_missing_file_returns_error(tmp_path):
    result = read_file(str(tmp_path), "missing.txt")
    assert result.startswith("ERROR: file not found:")
