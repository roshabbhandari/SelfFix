# SelfFix Decision Loop

SelfFix follows a ReAct-style loop where an issue is converted into a sequence of constrained actions.

## Loop

1. Read the current task and repository context.
2. Choose one supported action.
3. Execute the action against the repository sandbox.
4. Record the observation.
5. Re-evaluate the issue using the new evidence.
6. Repeat until the change is verified or the retry budget is exhausted.

## Important rule

The model should prefer evidence-producing actions before making broad edits. Reading a file, searching the codebase, and running focused tests should reduce uncertainty before a write.

## Completion

A successful run should finish with a clear summary of the change and verification result. A failed run should preserve the useful test output so the next iteration can act on concrete evidence instead of guessing.