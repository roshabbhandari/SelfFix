import os
import subprocess
import shlex
from pathlib import Path

ALLOWED_COMMANDS = {"pytest", "python", "python3", "ls", "cat", "git"}
MAX_OUTPUT_CHARS = 6000
COMMAND_TIMEOUT = 60


class SandboxError(Exception):
    pass


def _safe_path(repo_root: str, rel_path: str) -> Path:
    root = Path(repo_root).resolve()
    target = (root / rel_path).resolve()
    if not str(target).startswith(str(root)):
        raise SandboxError(f"Path escapes repo root: {rel_path}")
    return target


def read_file(repo_root: str, path: str) -> str:
    target = _safe_path(repo_root, path)
    if not target.exists():
        return f"ERROR: file not found: {path}"
    try:
        return target.read_text()
    except Exception as e:
        return f"ERROR reading {path}: {e}"


def write_file(repo_root: str, path: str, content: str) -> str:
    target = _safe_path(repo_root, path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return f"OK: wrote {len(content)} chars to {path}"


def list_files(repo_root: str, pattern: str = "**/*.py") -> list:
    root = Path(repo_root).resolve()
    ignore_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv"}
    results = []
    for p in root.glob(pattern):
        if any(part in ignore_dirs for part in p.parts):
            continue
        if p.is_file():
            results.append(str(p.relative_to(root)))
    return sorted(results)


def search_codebase(repo_root: str, query: str, max_matches: int = 30) -> str:
    root = Path(repo_root).resolve()
    ignore_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv"}
    matches = []
    for p in root.rglob("*.py"):
        if any(part in ignore_dirs for part in p.parts):
            continue
        try:
            lines = p.read_text().splitlines()
        except Exception:
            continue
        for i, line in enumerate(lines, start=1):
            if query.lower() in line.lower():
                rel = p.relative_to(root)
                matches.append(f"{rel}:{i}: {line.strip()}")
                if len(matches) >= max_matches:
                    return "\n".join(matches)
    return "\n".join(matches) if matches else "No matches found."


def run_shell(repo_root: str, command: str) -> str:
    parts = shlex.split(command)
    if not parts:
        return "ERROR: empty command"
    if parts[0] not in ALLOWED_COMMANDS:
        return f"ERROR: command '{parts[0]}' not allowed. Allowed: {sorted(ALLOWED_COMMANDS)}"

    try:
        result = subprocess.run(
            parts,
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT,
        )
        output = f"$ {command}\n[exit code {result.returncode}]\n"
        output += result.stdout[-MAX_OUTPUT_CHARS:]
        if result.stderr:
            output += "\n--- stderr ---\n" + result.stderr[-MAX_OUTPUT_CHARS:]
        return output
    except subprocess.TimeoutExpired:
        return f"ERROR: command timed out after {COMMAND_TIMEOUT}s"
    except Exception as e:
        return f"ERROR running command: {e}"


def run_tests(repo_root: str, test_path: str = "") -> dict:
    cmd = ["pytest", "-q"]
    if test_path:
        cmd.append(test_path)
    try:
        result = subprocess.run(
            cmd,
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=COMMAND_TIMEOUT,
        )
        return {
            "passed": result.returncode == 0,
            "output": (result.stdout + "\n" + result.stderr)[-MAX_OUTPUT_CHARS:],
        }
    except subprocess.TimeoutExpired:
        return {"passed": False, "output": "ERROR: tests timed out"}
    except Exception as e:
        return {"passed": False, "output": f"ERROR running tests: {e}"}


def git_diff(repo_root: str) -> str:
    result = subprocess.run(
        ["git", "diff"], cwd=repo_root, capture_output=True, text=True
    )
    return result.stdout
