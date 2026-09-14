import subprocess
import sys
from pathlib import Path


def test_main_requires_repo_and_issue():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [sys.executable, "main.py"],
        cwd=root,
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "--repo" in result.stderr
    assert "--issue" in result.stderr
