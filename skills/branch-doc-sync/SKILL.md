---
name: branch-doc-sync
description: Update repository documentation so it matches the delta between the current git branch and a base branch, usually `main`. Use when code, config, commands, setup steps, features, routes, APIs, or environment variables changed and `README*`, `docs/**/*.md`, `.env.example`, `example.env`, or similar documentation files need to be refreshed before review or merge.
---

# Branch Doc Sync

Use this skill to bring repository docs back in sync with the current branch. Treat the git diff as the starting point, then confirm the real branch state in the code before editing any docs.

## Workflow

1. Establish the comparison range.
   - Default the base branch to `main`.
   - If `main` does not exist locally, try `origin/main`, then `master`, then `origin/master`.
   - Compare from the merge base to `HEAD`, not from the live base branch tip.
   - If the working tree is dirty, inspect those files too because the user may want docs synced to local branch state, not just committed changes.

2. Generate the branch report.
   - Run `python <skill-dir>/scripts/branch_doc_delta.py --repo <repo-root> --base main`.
   - Read the report before opening files manually.
   - Use `--json` only when you need to feed the output into another script or structured analysis.

3. Read the code and existing docs.
   - Open the changed source/config files that actually affect setup, behavior, commands, interfaces, or configuration.
   - Open the existing README, docs pages, and env template files that the report flags as likely targets.
   - Prefer editing existing docs over creating new files unless the repository clearly lacks a natural home for the new information.

4. Update the right docs.
   - Update `README*` files when installation, startup, scripts, architecture summaries, feature lists, CLI usage, or developer workflow changed.
   - Update `docs/**/*.md` or equivalent long-form docs when feature behavior, API contracts, routing, deployment, operations, or troubleshooting guidance changed.
   - Update `.env.example`, `example.env`, `.env.sample`, `.env.template`, and similar files when required environment variables were added, removed, renamed, or had their documented meaning changed.
   - Use [references/update-rubric.md](references/update-rubric.md) when choosing which doc targets to edit.

5. Verify before finishing.
   - Reconcile the edited docs with the current branch state, not just the diff hunks.
   - Keep placeholder env values obviously fake and non-secret.
   - If a change affects docs but the exact value or behavior is still ambiguous, report the ambiguity instead of guessing.

## Update Rules

- Do not rewrite unrelated prose just because a file was touched.
- Do not invent new features, defaults, commands, or configuration keys.
- Keep edits local to the documentation surfaces that changed.
- Preserve repo-specific terminology and formatting conventions unless they are now incorrect.
- For env templates, never copy secrets from `.env`, CI settings, cloud dashboards, or personal shell profiles.
- When no documentation change is needed, say so explicitly and explain why the branch delta is documentation-neutral.

## Helper Script

Use `scripts/branch_doc_delta.py` as the first pass. It reports:

- branch/base/merge-base metadata
- changed files in the branch delta
- uncommitted local files worth considering
- existing documentation targets in the repo
- existing env template targets
- env variable references added in the branch diff
- env keys that appear to be missing from example env files
- high-level follow-up suggestions

Example:

```powershell
python ./scripts/branch_doc_delta.py --repo /path/to/repo --base main
```

## Common Requests

- "Use `$branch-doc-sync` to compare this branch to main and update the README."
- "Sync the docs for this feature branch before I open a PR."
- "Figure out which documentation changed with this branch and fix the stale files."
- "Refresh `.env.example` and the setup docs based on the current branch."

## Output Expectations

When you use this skill:

- say which base branch you compared against
- name the docs you changed
- call out env keys you added or removed from example env files
- note any unresolved documentation gaps or assumptions
