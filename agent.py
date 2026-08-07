import json
import re

from llm import call_llm
from tools import (
    read_file, write_file, list_files, search_codebase,
    run_shell, run_tests, git_diff,
)

MAX_ITERATIONS = 15
MAX_TEST_RETRIES = 3

TOOL_DOCS = """
You are an autonomous coding agent working inside a local git repository.
You solve a GitHub issue by exploring the code, editing files, and running tests
until they pass. You act ONE step at a time. Respond with ONLY a single JSON object,
no other text, no markdown fences.

Available tools:
- {"tool": "list_files", "args": {"pattern": "**/*.py"}}
- {"tool": "read_file", "args": {"path": "relative/path.py"}}
- {"tool": "write_file", "args": {"path": "relative/path.py", "content": "full new file content"}}
- {"tool": "search_codebase", "args": {"query": "some_function_name"}}
- {"tool": "run_shell", "args": {"command": "pytest -q tests/test_foo.py"}}
- {"tool": "run_tests", "args": {"test_path": "tests/test_foo.py"}}
- {"tool": "finish", "args": {"summary": "what you changed and why"}}

Rules:
- write_file always replaces the ENTIRE file content, so read the file first if editing.
- Call "finish" only once you believe the issue is resolved and relevant tests pass.
- If tests fail, read the error output carefully and try again with a fix.
- Think step by step, but only output the JSON action - no explanations outside the JSON.
- Include a "thought" field in every JSON response with a one-sentence rationale.
"""


class CodingAgent:
    def __init__(self, repo_root: str, issue_text: str):
        self.repo_root = repo_root
        self.issue_text = issue_text
        self.transcript = []
        self.log = []

    def _log(self, entry: str):
        self.log.append(entry)
        print(entry)

    def _parse_action(self, raw: str) -> dict:
        cleaned = re.sub(r"^```(json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", cleaned, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            raise

    def _dispatch(self, action: dict) -> str:
        tool = action.get("tool")
        args = action.get("args", {})

        if tool == "list_files":
            files = list_files(self.repo_root, args.get("pattern", "**/*.py"))
            return "\n".join(files[:200])

        if tool == "read_file":
            return read_file(self.repo_root, args["path"])

        if tool == "write_file":
            return write_file(self.repo_root, args["path"], args["content"])

        if tool == "search_codebase":
            return search_codebase(self.repo_root, args["query"])

        if tool == "run_shell":
            return run_shell(self.repo_root, args["command"])

        if tool == "run_tests":
            result = run_tests(self.repo_root, args.get("test_path", ""))
            return f"passed={result['passed']}\n{result['output']}"

        if tool == "finish":
            return "FINISH"

        return f"ERROR: unknown tool '{tool}'"

    def run(self) -> dict:
        history = [f"ISSUE TO SOLVE:\n{self.issue_text}\n"]

        for step in range(1, MAX_ITERATIONS + 1):
            user_prompt = "\n\n".join(history[-8:])  # keep context bounded
            raw = call_llm(TOOL_DOCS, user_prompt)

            try:
                action = self._parse_action(raw)
            except Exception:
                self._log(f"[step {step}] Could not parse LLM output, stopping.")
                self._log(raw)
                break

            thought = action.get("thought", "")
            tool = action.get("tool", "?")
            self._log(f"[step {step}] thought: {thought}")
            self._log(f"[step {step}] tool: {tool} args: {action.get('args', {})}")

            if tool == "finish":
                summary = action.get("args", {}).get("summary", "")
                diff = git_diff(self.repo_root)
                self._log(f"[step {step}] Agent finished: {summary}")
                return {
                    "success": True,
                    "summary": summary,
                    "diff": diff,
                    "log": self.log,
                }

            observation = self._dispatch(action)
            history.append(f"ACTION: {json.dumps(action)}\nOBSERVATION:\n{observation}")

        self._log("Reached max iterations without finishing.")
        return {
            "success": False,
            "summary": "Agent did not converge within iteration limit.",
            "diff": git_diff(self.repo_root),
            "log": self.log,
        }

    def run_with_test_verification(self, test_path: str = "") -> dict:
        """
        Runs the agent, then verifies with the real test suite. If tests fail,
        feeds the failure back to the agent and lets it try again, up to
        MAX_TEST_RETRIES times.
        """
        result = self.run()

        for attempt in range(1, MAX_TEST_RETRIES + 1):
            test_result = run_tests(self.repo_root, test_path)
            if test_result["passed"]:
                self._log(f"Tests passed after {attempt - 1} retry(ies).")
                result["tests_passed"] = True
                result["diff"] = git_diff(self.repo_root)
                return result

            self._log(f"[retry {attempt}] Tests failed, feeding error back to agent.")
            retry_prompt = (
                f"{self.issue_text}\n\n"
                f"Your previous change did not pass tests. Test output:\n"
                f"{test_result['output']}\n\n"
                f"Fix the issue."
            )
            self.issue_text = retry_prompt
            result = self.run()

        result["tests_passed"] = False
        result["diff"] = git_diff(self.repo_root)
        return result
