from pathlib import Path

import pytest

from tools import SandboxError, _safe_path


def test_safe_path_stays_inside_repo(tmp_path):
    target = _safe_path(str(tmp_path), "src/app.py")
    assert target == Path(tmp_path) / "src" / "app.py"


def test_safe_path_rejects_parent_escape(tmp_path):
    with pytest.raises(SandboxError):
        _safe_path(str(tmp_path), "../outside.py")
