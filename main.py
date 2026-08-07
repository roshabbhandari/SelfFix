import argparse
import json
import os

from agent import CodingAgent


def main():
    parser = argparse.ArgumentParser(description="Autonomous coding agent")
    parser.add_argument("--repo", required=True, help="Path to local git repo")
    parser.add_argument("--issue", required=True, help="Issue text, or path to a .txt/.md file containing it")
    parser.add_argument("--test-path", default="", help="Specific test file/dir to verify against")
    parser.add_argument("--log-file", default="agent_run.log", help="Where to save the run transcript")
    args = parser.parse_args()

    if os.path.isfile(args.issue):
        with open(args.issue) as f:
            issue_text = f.read()
    else:
        issue_text = args.issue

    agent = CodingAgent(repo_root=args.repo, issue_text=issue_text)
    result = agent.run_with_test_verification(test_path=args.test_path)

    with open(args.log_file, "w") as f:
        f.write("\n".join(result["log"]))

    print("\n" + "=" * 60)
    print(f"Success: {result['success']}  Tests passed: {result.get('tests_passed')}")
    print(f"Summary: {result['summary']}")
    print("=" * 60)
    print("\n--- git diff ---\n")
    print(result["diff"] or "(no changes)")

    with open("PR_DESCRIPTION.md", "w") as f:
        f.write(f"## Summary\n\n{result['summary']}\n\n")
        f.write(f"## Tests\n\nPassed: {result.get('tests_passed')}\n\n")
        f.write(f"## Diff\n\n```diff\n{result['diff']}\n```\n")

    print(f"\nFull transcript saved to {args.log_file}")
    print("PR description saved to PR_DESCRIPTION.md")


if __name__ == "__main__":
    main()
