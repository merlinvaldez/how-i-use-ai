# Documentation Update Rubric

Use this rubric after running `scripts/branch_doc_delta.py`.

## Choose the target files

Edit the smallest existing doc surface that fully explains the branch change.

- Use the root `README*` for project-level setup, quickstart, scripts, architecture summaries, high-level features, and contribution workflow.
- Use package or subdirectory `README*` files when the change is scoped to one package, app, service, or tool.
- Use `docs/` pages for feature behavior, API contracts, routing, deployment, operations, migration notes, and troubleshooting.
- Use env template files for configuration keys and placeholder values, not for long explanations that belong in prose docs.

## Update README files when

- install or bootstrap steps changed
- run, build, test, lint, seed, or deploy commands changed
- the project gained or removed a major feature worth surfacing
- repo structure or service boundaries changed enough that onboarding text is now stale
- required configuration or third-party services changed

## Update docs pages when

- a feature's behavior, request shape, response shape, or routing changed
- deployment or operational steps changed
- a migration path, data flow, or troubleshooting path changed
- the branch introduces a new subsystem that needs more than a short README paragraph

## Update env templates when

- a required env var was added
- an env var was renamed or removed
- a variable changed from optional to required, or the reverse
- the variable's meaning changed enough that comments or example values are now misleading

## Env template rules

- Prefer existing template files such as `.env.example`, `.env.sample`, `.env.template`, `example.env`, or app-specific variants.
- Keep values fake and safe: `your-api-key-here`, `http://localhost:3000`, `postgres://user:pass@localhost:5432/app`.
- Preserve comments and ordering unless reordering materially improves clarity.
- If no example env file exists, either create the repo's natural equivalent or document the variables in README/config docs.

## Avoid weak updates

- Do not add vague bullets like "updated docs" or "improved setup".
- Do not copy diff text directly into docs without checking the current branch state.
- Do not document internal refactors that do not change user-facing behavior or operator workflow.
- Do not add secrets, private URLs, or personal machine paths.
