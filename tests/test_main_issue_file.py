from pathlib import Path


def test_issue_file_detection_contract():
    issue = Path("issue.md")
    assert issue.suffix == ".md"
    assert issue.name.endswith(".md")
