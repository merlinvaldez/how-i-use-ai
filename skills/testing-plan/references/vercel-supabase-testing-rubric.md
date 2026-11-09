# Vercel And Supabase Testing Rubric

Use this rubric after running `scripts/branch_test_scope.py` and reading the changed code.

## Goal

Produce an unchecked testing plan that is:

- branch-specific
- executable by a human reviewer
- precise about where to click, what to call, what SQL to run, and what outcome to expect

## Section Rules

### Scope

Summarize the changed surfaces, for example:

- changed preview routes
- changed API endpoints
- changed migrations, RLS policies, or Supabase functions
- changed environment variables

### Setup

Include only setup tasks the tester actually needs, such as:

- obtain the preview deployment URL
- sign in with a test account of the correct role
- confirm preview env vars exist in Vercel
- open the Supabase SQL Editor for the correct project or environment

### Vercel Preview Checks

Use this section when frontend routes, server-rendered pages, middleware, redirects, or static assets changed.

Good checklist item:

- [ ] Open the preview deployment URL, navigate to `/dashboard`, and confirm the updated summary cards render without hydration errors or missing data.

Weak checklist item:

- [ ] Test the dashboard.

### API And Server Checks

Use when API routes, server actions, edge functions, background jobs, or env-dependent server logic changed.

Prefer items that include:

- exact route or handler
- request method and body when relevant
- expected status code or response shape
- expected Vercel logs when server-side behavior matters

### Supabase Database Checks

Use when migrations, SQL, RLS, auth, storage, or data mutations changed.

Include the smallest exact verification that proves the branch behavior:

- run a specific migration-related query
- verify a new column or index exists
- verify RLS behavior with the correct user role
- verify an inserted or updated row appears after an app action
- verify storage upload/delete behavior and bucket access

When SQL is required, include runnable SQL blocks in the plan.

### Regression Sweep

Include only adjacent paths worth retesting because they are likely to break from the same change:

- sibling routes that share the component
- related auth flows
- read paths after a write-path change
- old behavior that the branch intentionally preserves

### Risks / Unknowns

List the blockers that prevent a fully exact plan:

- preview URL not available
- no clear test user
- no sample row identifiers
- migration intent unclear from code
- required secret or third-party dependency unavailable

## What To Include For Common Change Types

### Env var changes

- a Vercel preview-env verification step
- the app behavior that proves the env var is working
- the Supabase-side effect if the env var controls DB/auth/storage behavior

### Migration or schema changes

- a schema verification query
- one app-level mutation or read that exercises the new schema
- any backfill or nullable/default assumption worth checking

### RLS or auth changes

- signed-out access check
- signed-in access check
- role-sensitive access check when roles or policies changed

### Storage changes

- upload or create check
- retrieval or rendering check
- delete or replacement check if behavior changed

### API / function changes

- direct request check
- UI path that depends on the request
- log or error-surface check when relevant

## Output Style

- Keep every task unchecked.
- Keep the language direct and imperative.
- Prefer explicit nouns over generic phrases.
- Do not add test cases that are unsupported by the diff or code.

## Beginner-Friendly Test Item Rules

Every checkbox in the plan must be ready for a beginner to follow. Include both:

- **How to do it:** Exact click-by-click steps, or the full copyable command, API request, or SQL query. Say where to run it and which folder or project to use.
- **What success looks like:** A specific visible result or response.

Use short sentences and explain technical words the first time they appear. For API checks, include the method, URL, headers, and example body. For database checks, include the full SQL and the correct Supabase project and SQL Editor. Explain how to get any value that is not in the changed code.

Do not ask the reader to invent commands, request bodies, queries, sample data, or expected results. Do not guess URLs, accounts, secrets, or record IDs. When a needed detail is unknown, list it under `Risks / Unknowns` and say how to obtain it when known. Do not create a vague checkbox for a test that cannot yet be described.

Example:

````markdown
- [ ] **Confirm the new column exists.**
  **How to do it:** In the Supabase Dashboard for the Preview project, open SQL Editor, paste this query, and select Run:
  ```sql
  select column_name
  from information_schema.columns
  where table_name = 'example_table'
    and column_name = 'new_column';
  ```
  Replace the example names with the table and column names in the migration.
  **What success looks like:** One row appears with the new column name.
````