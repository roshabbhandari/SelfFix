# SelfFix Provider Adapters

SelfFix currently supports more than one LLM provider, so provider-specific details should stay at the integration boundary.

## Adapter goals

Each provider integration should:

- Read credentials from the configured environment.
- Convert the provider response into the format expected by the agent loop.
- Normalize common request failures.
- Preserve useful error details without logging secrets.
- Expose a small, predictable interface to the rest of the application.

## Adding a provider

When adding another provider:

1. Keep the provider name explicit in configuration.
2. Reuse the existing action protocol.
3. Add a focused smoke test for a minimal model request.
4. Document required environment variables.
5. Verify failure behavior as well as the successful path.

This keeps the agent loop stable while provider implementations evolve independently.