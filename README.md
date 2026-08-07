# Autonomous Coding Agent

A minimal ReAct-style agent that reads a local git repo, plans a fix for an
issue, edits files, runs the test suite, and retries on failure — until it
converges or hits a retry limit. Provider-agnostic: point it at OpenAI,
Claude, Gemini, or Groq via one environment variable.

## How it works

1. You give it a repo path and an issue description.
2. Each step, the LLM outputs ONE JSON action (`read_file`, `write_file`,
   `search_codebase`, `run_shell`, `run_tests`, or `finish`).
3. The agent executes that action and feeds the result back as the next
   observation — a standard ReAct loop.
4. Once the agent calls `finish`, the real test suite is run for
   verification. If it fails, the failure output is fed back to the agent
   and it tries again (up to `MAX_TEST_RETRIES`).
5. A git diff and a `PR_DESCRIPTION.md` are produced at the end.

## Safety / sandboxing

- `run_shell` only allows an explicit command allowlist (`pytest`, `python`,
  `ls`, `cat`, `git`) — no arbitrary shell execution.
- All file paths are resolved and checked against the repo root, so the
  agent can't write outside the target repo.
- Commands run with a timeout and truncated output to keep context bounded.
- For untrusted repos, run this inside a Docker container or VM as an
  extra layer — the allowlist reduces risk but isn't a full sandbox.

## Setup

```bash
pip install -r requirements.txt --break-system-packages
cp .env.example .env   # fill in the provider you want + its API key
export $(cat .env | xargs)
```

## Usage

```bash
python main.py --repo /path/to/target/repo --issue "add() returns wrong result, should sum not subtract" --test-path tests/test_calculator.py
```

`--issue` also accepts a path to a `.txt`/`.md` file containing the issue text
(handy for pointing it at an actual GitHub issue body).

Output:
- `agent_run.log` — full step-by-step transcript (thoughts + tool calls)
- `PR_DESCRIPTION.md` — summary + diff, ready to paste into a PR
- stdout — live progress as the agent works

## Extending this

- **Real GitHub integration**: use `PyGithub` to pull the issue body
  automatically and open a PR with `PR_DESCRIPTION.md` at the end of `main.py`.
- **Better repo indexing**: swap `search_codebase`'s substring search for
  embedding-based retrieval over function/class summaries (same pattern as
  a RAG memory store) so the agent scales to large repos.
- **True sandboxing**: run `run_shell`/`run_tests` inside a per-run Docker
  container instead of a subprocess allowlist.
- **Multi-language support**: extend `list_files`/`search_codebase` beyond
  `*.py` using `tree-sitter` for language-aware parsing.
