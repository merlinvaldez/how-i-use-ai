---
name: implement
description: Implement code changes that have already been agreed in the current conversation by recovering the latest relevant user and assistant messages, turning them into a concrete implementation brief, then inspecting the repository, editing the code, and validating the result. Use when discussion is over and the user wants Codex to "implement it," "make the change," "go ahead," "apply the patch," or otherwise translate prior chat decisions into actual code without restarting planning.
---

# Implement

## Overview

Use this skill after the conversation has converged on a concrete change. Reconstruct the approved plan from the visible thread, then implement it directly in the codebase, verify the result, and always finish by telling the user exactly how they can verify it themselves, either through frontend testing guidance or terminal commands.

## Workflow

1. Reconstruct the implementation brief.
   - Re-read the latest user request first, then scan backward through the relevant thread.
   - Extract the latest concrete requirements, constraints, accepted tradeoffs, and explicit non-goals.
   - Prefer later corrections over earlier ideas.
   - Treat user instructions as higher priority than assistant suggestions.
   - Use only chat history that is actually visible in the current thread context. If a needed decision appears missing or truncated, ask the user to restate it instead of guessing.

2. Resolve ambiguities before editing.
   - If multiple plans were discussed, choose the latest plan that the user explicitly accepted and did not later revise.
   - If the thread still contains a real contradiction or a missing decision that blocks safe implementation, ask one concise clarification question.
   - If the remaining gaps are minor and the repo makes the intended path obvious, make the smallest reasonable assumption and proceed.

3. Ground the brief in the repository.
   - Inspect the files, routes, tests, configs, and runtime surfaces that the brief implies.
   - Verify assumptions from the actual code instead of relying on earlier speculation in the chat.
   - If the thread named specific files, modules, commands, or errors, check those first.

4. Implement the agreed change.
   - Execute the approved approach directly instead of reopening brainstorming.
   - Keep scope tight to the reconstructed brief.
   - Preserve unrelated user changes already present in the worktree.
   - If the repository forces a small adaptation, stay as close as possible to the agreed direction and explain the deviation.

5. Validate the result.
   - Run the smallest meaningful checks that match the change, such as targeted tests, lint, build, or manual verification commands.
   - Separate checks you ran yourself from follow-up verification that the user should perform.
   - If full validation is not possible, run the best available checks and state what remains unverified.

6. Report back concisely.
   - Summarize what was implemented.
   - Mention the key thread decisions that drove the implementation when that context matters.
   - State the validation result and any remaining risks or follow-up work.
   - Always include concrete user verification instructions, even if your own validation passed.
   - For frontend-visible changes, include a short "how to test this in the UI" path with the route or screen to open, the interaction to perform, and the expected result.
   - For non-frontend work, or whenever a UI path is not the best fit, include exact PowerShell command(s) the user can run in the terminal.
   - Prefer exact PowerShell commands, routes, URLs, buttons to click, or UI states to inspect over generic advice.
   - If both frontend testing guidance and terminal commands are useful, include both.
   - If no automated check exists, tell the user exactly where to look and what changed behavior should confirm success.

## Decision Rules

- Let the latest explicit user instruction win.
- Let a user correction override an earlier assistant proposal.
- Let explicit scope limits override "better" but broader ideas.
- Let concrete repository facts override stale assumptions from earlier in the discussion.
- Always end with a clear "how to verify this worked" follow-up, using frontend testing guidance for UI changes or exact PowerShell commands for terminal validation.
- Do not claim the thread agreed on a plan if the visible messages do not support that claim.

## Trigger Examples

- "Use `$implement` and go make the change we just agreed on."
- "Implement the plan from above."
- "Take what we decided in this chat and apply it to the code."
- "Stop explaining and patch the repo based on the previous messages."
