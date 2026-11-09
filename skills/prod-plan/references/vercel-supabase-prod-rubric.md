# Vercel And Supabase Production Rollout Rubric

Use this rubric after running `scripts/branch_prod_scope.py` and reading the changed code and config.

## Goal

Produce an unchecked production rollout checklist that is:

- branch-specific
- focused on stack settings and rollout order
- explicit about what must change in Vercel, Supabase, or adjacent provider dashboards before production traffic sees the branch

## Section Rules

### Scope

Summarize only the relevant change surfaces, for example:

- new or renamed env vars
- changed Vercel config, cron jobs, or domains
- changed Supabase migrations, policies, functions, storage, or auth settings
- changed webhooks, callbacks, or third-party integration points

### Rollout Order

Use this section when order matters. Good examples:

- [ ] Add `FOO_API_KEY` to the Vercel production environment before deploying the branch.
- [ ] Apply `supabase/migrations/20260409_add_profiles.sql` in production before enabling the UI path that writes to `profiles`.
- [ ] Run the backfill query before turning on the code path that assumes every row has `billing_customer_id`.

Weak example:

- [ ] Do the rollout in the right order.

### Vercel Production Changes

Use when the diff implies any Vercel-side update, including:

- production env vars
- `vercel.json`
- cron jobs
- domains, redirects, rewrites, or middleware consequences
- build or runtime settings
- webhook endpoints or provider callbacks that target Vercel routes

Prefer items that include:

- the exact setting or env key
- whether the change belongs in production, preview, or both
- the route, function, or behavior that depends on it
- the completion condition

### Supabase Production Changes

Use when migrations, SQL, policies, auth, functions, or storage changed.

Prefer items that include:

- the exact migration, function, bucket, or auth setting
- the order of application
- the expected schema or config state after the change
- the app or API consequence that depends on it

### Data Safety Checks

Use when data shape, integrity, or reversibility matters.

Include only checks justified by the diff, such as:

- destructive or locking migrations
- nullable to non-null transitions
- backfills
- policy changes that can lock out current users
- bucket policy or signed URL changes
- webhook idempotency or duplicate-processing risk

When SQL is required, include runnable SQL blocks.

### Post-Deploy Verification

Use the smallest verification that proves the production configuration actually works:

- open a route that depends on the new env var
- hit a changed API endpoint in production
- verify a Supabase row can be created or read under the intended role
- confirm a cron job or webhook reaches the new route
- confirm auth redirects or callback URLs land in the right production domain

### Risks / Blockers

List the blockers that prevent safe production rollout planning, such as:

- unknown secret values
- unclear production project or domain
- migration intent unclear from code
- backfill strategy missing
- provider-side callback changes with no matching owner or dashboard path

## What To Include For Common Change Types

### Env var changes

- the exact key name
- where it must be added or rotated
- the route, job, or feature that depends on it
- whether missing it would break build time, runtime, or only a conditional feature

### Migration or schema changes

- rollout order
- schema verification query
- backfill or data repair step if needed
- rollback or irreversibility warning when applicable

### RLS or auth changes

- Supabase auth setting or redirect update
- callback or site URL consequence
- user-role consequence
- post-deploy signed-in and signed-out verification

### Storage changes

- bucket or policy update
- required secrets
- upload or retrieval consequence
- signed URL, public URL, or delete-path consequence if relevant

### API, cron, or function changes

- Vercel config or deployment setting update
- linked secret or env var update
- direct verification path after deploy
- logs or metrics signal worth checking

## Output Style

- Keep every task unchecked.
- Keep the language direct and imperative.
- Prefer exact nouns over generic phrases.
- Do not add tasks unsupported by the diff or code.

## Beginner-Friendly, Ready-To-Follow Items

Write for a person who may be new to coding. Use plain words, short sentences, and explain technical terms the first time.

For every checkbox, include both `How to do it` and `How to verify it`:

- For a dashboard change, name the exact project, menu path, environment (Production or Preview), field, and value. Explain where to get a value that is not in the code.
- For a terminal command, include the complete command and say which folder and terminal to use.
- For an API check, include the full URL pattern, method, headers, and sample body. Explain each placeholder.
- For a database check, include the complete SQL and name the correct Supabase project and SQL Editor. Keep verification queries read-only unless the user is being instructed to apply a migration.
- For post-deploy checks, include exact browser steps or a copyable request, plus the expected response or visible result.

Put each instruction directly under the checkbox it belongs to. Never ask the reader to invent a command, request, query, test data, or expected result. Do not guess secrets or tell the user to paste a secret into chat. If a needed value is unknown, explain how to find it or list the missing value and owner under `Risks / Blockers`.

For the step-by-step format, give every step an exact action, where to do it, and an exact way to verify it. Keep the checkpoint question simple and ask only about the result the user can see.

Example:

````markdown
- [ ] **Check the production health route.**
  **How to do it:** Open PowerShell. Replace `PASTE_PRODUCTION_URL_HERE` with the production URL from Vercel, then paste and run:
  ```powershell
  $productionUrl = 'PASTE_PRODUCTION_URL_HERE'
  Invoke-RestMethod -Method Get -Uri "$productionUrl/api/health"
  ```
  **How to verify it:** The command returns the successful response defined by the changed route code.
````