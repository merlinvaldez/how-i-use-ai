---
name: prod-plan
description: Guide a beginner through a branch-aware production rollout with exact steps and verification for every task. Use for Vercel and Supabase changes before release; Codex must not perform production mutations.
---

# Prod Plan

Use this skill to coach the user through a pre-production rollout, not to perform the rollout for them. Focus on the changes that must happen in Vercel, Supabase, and adjacent production settings before the branch can ship safely.

## Non-Execution Rule

- Never perform rollout work for the user.
- Never edit files, apply patches, deploy, promote Vercel deployments, apply migrations, run production SQL, create or delete cron jobs, set secrets, rotate keys, or mutate production systems.
- You may run read-only discovery commands, inspect repo files, compare branches, read Vercel/Supabase metadata, and use dry-run style checks when they do not change repo-tracked files or remote production state.
- If the user asks you to execute a rollout step, refuse the mutation and instead give the exact step for the user to run, plus the expected verification result.
- Treat all SQL, CLI commands, dashboard actions, and provider changes as instructions for the user to perform manually unless the user switches to a different non-prod skill/task.

## Teach-Me Rollout Flow

- By default, deliver the complete end-to-end rollout plan in one response, covering every production task supported by the branch delta through post-deploy verification.
- Do not stop after Part 1 or wait at a checkpoint for an ordinary request to plan a rollout.
- Use the part-by-part flow only when the user explicitly asks for a guided walkthrough, step-by-step coaching, or a specific part such as `Part 1`.
- Each part should include:
  - `Goal`
  - `Concept`
  - `Steps`
  - `Output` with exact command, SQL, or dashboard action for the user to run
  - `Checkpoint question`
  - `Docs`
  - `Verify`
- Keep explanations practical and beginner-friendly, but preserve production rigor.
- Use exact names for env vars, project IDs, table names, function names, cron names, routes, and expected outputs whenever they can be inferred.

## Default Behavior

- Default the base branch to `main`.
- If `main` is missing locally, fall back to `origin/main`, then `master`, then `origin/master`.
- Compare from the merge base to `HEAD`, then include staged, unstaged, and untracked worktree changes.
- Produce the rollout guidance in chat unless the user explicitly asks for a file.
- Provide the complete rollout checklist by default. Start with `Part 1` only when the user explicitly requests a staged walkthrough or a specific part.
- Assume the primary stack is Vercel plus Supabase, but tailor the checklist to the repository and changed files in front of you.

## Workflow

1. Establish scope.
   - Identify the repo root and current branch.
   - Run `python <skill-dir>/scripts/branch_prod_scope.py --repo <repo-root> --base main`.
   - Read the report before opening files manually.

2. Confirm the real production surface.
   - Open the changed code, config, migration, SQL, env template, and deployment files that affect runtime behavior.
   - Confirm which Vercel project settings, production environment variables, domains, cron jobs, webhooks, auth redirects, Supabase migrations, RLS policies, functions, buckets, or secrets are actually impacted.
   - Do not rely on file names alone when the code or config makes the intent obvious.

3. Resolve deployment context.
   - If `.vercel/project.json` exists, use it to orient the checklist toward the linked Vercel project.
   - If Vercel tools are available, prefer reading the linked project, production deployment, and logs directly instead of guessing.
   - If live Vercel access is unavailable, still write exact manual dashboard steps.
   - If Supabase CLI files or config exist, use them to infer the production project surfaces that need updates.

4. Build the rollout parts.
   - Use [references/vercel-supabase-prod-rubric.md](references/vercel-supabase-prod-rubric.md) for required sections and checklist style.
   - Include only tasks that materially follow from the branch delta.
   - Include exact env key names, config paths, SQL, dashboards, routes, functions, buckets, callback URLs, and expected outcomes whenever they can be inferred from the code.
   - Order the parts so the user can safely execute one production step at a time.

5. Close with sequencing and blockers.
   - Call out rollout order when it matters, for example env vars before deploy, migrations before traffic, backfills before feature enablement, or redirect/domain changes before auth cutover.
   - Call out missing production values, unknown project IDs, missing preview or prod URLs, unclear backfill strategy, missing secrets, or ambiguous migration safety.
   - If a risky change is visible but the repository does not reveal enough detail to prescribe the final production step, say what still needs clarification instead of guessing.

## Required Output Shape

For an explicitly requested guided, part-by-part rollout, output one part at a time using this shape:

1. `Goal`
2. `Concept`
3. `Steps`
4. `Output`
5. `Checkpoint question`
6. `Docs`
7. `Verify`

For the default full checklist, and whenever the user explicitly asks for it, organize it under these headings when they apply:

1. `## Scope`
2. `## Rollout Order`
3. `## Vercel Production Changes`
4. `## Supabase Production Changes`
5. `## Data Safety Checks`
6. `## Post-Deploy Verification`
7. `## Risks / Blockers`

For full checklists:

- Use flat unchecked checkboxes only.
- Each checkbox must contain an exact action and a concrete observable result or completion condition.
- Prefer wording like "Add `STRIPE_WEBHOOK_SECRET` to the Vercel production environment before promoting the deployment" over vague wording like "check env vars."

For part-by-part rollout guidance:

- Do not use checkboxes unless the user asks for a checklist.
- Give the smallest safe next step.
- End with a checkpoint question and wait for the user before continuing.

## Planning Rules

- Never say a production task is already complete unless you actually verified it.
- Never execute production tasks; tell the user what to do manually.
- Do not tell the user to "check everything."
- Do not invent production secrets, project IDs, redirect URLs, domain names, or SQL assumptions.
- When environment variables changed, include both the Vercel production update step and the feature or server path that depends on the variable.
- When migrations, SQL, or policies changed, include the exact rollout order, the production SQL verification, and the app-level or API-level consequence.
- When auth changed, include site URL, redirect URL, callback, middleware, and session consequences when applicable.
- When storage changed, include bucket or policy setup plus upload, retrieval, signed URL, or deletion consequences when applicable.
- When cron jobs, schedules, or serverless behavior changed, include the Vercel production config step and the first verification signal after deploy.
- When webhooks or third-party callbacks changed, include both sides of the configuration if one side lives outside the repo.

## Vercel And Supabase Specific Guidance

- For Vercel, prefer explicit dashboard or config actions around production env vars, project settings, domains, cron jobs, webhooks, edge or serverless behavior, and deployment promotion.
- For Supabase, prefer exact references to migrations, SQL Editor checks, auth settings, redirect URLs, policies, functions, bucket config, and secrets only when they are justified by the diff.
- If a branch introduces a new env key that is not documented in an env template, call that out as a production blocker until the required value and owner are known.
- If a migration is destructive, irreversible, or depends on a backfill, call out the order of operations and the rollback risk explicitly.
- If direct production access is unavailable, still provide the exact manual action and the evidence that should be checked afterward.

## Helper Script

Use `scripts/branch_prod_scope.py` first. It summarizes:

- branch, base, and merge-base metadata
- committed and uncommitted changed files
- changed route and API surfaces that imply runtime impact
- changed Vercel config files and cron routes
- changed Supabase migrations, config, functions, storage, seed, and SQL surfaces
- newly referenced env vars and env template deltas
- linked Vercel project metadata when `.vercel/project.json` is present
- seed production focus areas to convert into the final checklist

Example:

```powershell
python ./scripts/branch_prod_scope.py --repo /path/to/repo --base main
```

## Trigger Examples

- "Use `$prod-plan` to compare this branch against main and tell me what I must change in Vercel and Supabase before production."
- "Make me a prod rollout checklist for this feature branch."
- "Figure out the production env vars, migrations, redirects, and stack settings I need before I deploy this."
- "Turn this branch diff into a production readiness checklist so I don't miss any Supabase or Vercel changes."
- "Use `$prod-plan` to walk me step by step through the production rollout without making changes for me."
- "Use `$prod-plan` and give me Part 1 of the production rollout."

## Beginner-Friendly, Ready-To-Follow Instructions

Write for someone who is new to coding. Use short sentences, explain technical words the first time they appear, and say where to click, what to enter, and what result to look for.

Every production rollout checkbox must include both:

- **How to do it:** Give the exact dashboard path and fields to use, or a complete command, SQL statement, or request the user can copy. Say where to run it and which project or folder to use.
- **How to verify it:** Give exact steps or a read-only command/query to confirm the change, and say what result means it worked.

Put the instructions next to the checkbox they belong to. Do not leave the user to write their own command, request body, SQL, or test data. For a browser or dashboard check, give click-by-click steps. For an API check, include the method, URL, headers, and sample body. For SQL, include the full query.

For part-by-part guidance, do not use checkboxes unless requested. Each step must still say what to do, where to do it, and how to verify it. Keep the `Checkpoint question` simple and specific. Do not ask the user to paste secret values into chat.

Explain every placeholder and how to replace it. Use values from the code when they are clear. When a value or owner is unknown, say where to get it if you know; otherwise name the missing detail under `Risks / Blockers`. Do not guess production URLs, account names, project IDs, or secrets.

Use this format for a full checklist:

````markdown
- [ ] **Confirm the production health route works.**
  **How to do it:** Open PowerShell. Replace `PASTE_PRODUCTION_URL_HERE` with the production URL from Vercel, then paste and run:
  ```powershell
  $productionUrl = 'PASTE_PRODUCTION_URL_HERE'
  Invoke-RestMethod -Method Get -Uri "$productionUrl/api/health"
  ```
  **How to verify it:** The command should return the health response shown in the changed route code, with a successful status.
````

Keep every task unchecked until you have actually verified it. This is a production plan, not evidence that a change has been made.