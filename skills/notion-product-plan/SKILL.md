---
name: notion-product-plan
description: Turn a rough product idea into a polished Notion product brief plus supporting planning pages and a matching repo README. Use when Codex should convert a startup, app, marketplace, or feature concept into the user's established Notion product-doc style, especially when asked to mirror existing workspace pages such as VoteFeed.org or StringPhone.ai, create related Dev or Research subpages, and sync the repo README with the current V1 framing.
---

# Notion Product Plan

## Overview

Turn a rough product idea into a reusable product brief that lives both in Notion and in the repo documentation.

Use Notion as the source of truth for the product brief, then update `README.md` so the repo reflects the same framing, user flow, and scope.

## Workflow

### 1. Build Context First

- Read the user request carefully and infer the product name, target user, pain point, primary workflow, and likely V1 scope.
- Inspect the current repo before writing anything. Read `README.md` first. If the repo is small, also inspect the top-level layout.
- Treat a minimal or placeholder README as replaceable unless the user says otherwise.
- Make reasonable assumptions and proceed. Ask a question only when blocked by missing information that would materially change the output.

### 2. Find The User's Existing Notion Style

- Use the Notion tools to search the workspace for analogous product pages.
- Prefer the exact reference pages named by the user. If none are named, look for the user's established startup or product docs.
- Fetch the most relevant pages and extract the reusable structure:
  - opening pitch section
  - phased MVP sections
  - stretch ideas
  - linked project-management subpages
  - level of detail and tone
- Mirror the user's style without copying irrelevant technical sections from the reference page.

### 3. Create Or Adapt The Notion Page Safely

- Prefer duplicating a similar existing product page when that is the easiest way to preserve placement, icon style, and linked project-management structure.
- If duplicating:
  - rename the main page immediately
  - rename obvious child pages that should carry over
  - replace reused content with the new product content
- Preserve child pages and databases.
- If Notion warns that a page edit would delete child pages or databases, do not delete them by default.
- Keep those children by preserving their `<page>` or `<database>` blocks, or switch from full-page replacement to targeted `update_content` edits.
- Create supporting subpages when useful, especially:
  - `<Product Name> Dev`
  - `<Product Name> Research Notes`

### 4. Use A Standard Product-Brief Shape

Default to a section order like this unless the user's existing style strongly suggests a better variant:

- `30 Second Pitch`
- `MVP V1 Features`
- `MVP V2 Features`
- `Stretch Features`
- `Core User Flow`
- `Key Product Questions`
- `Initial Public Data Sources`
- `Project Management System`

For stronger product pages:

- keep the pitch crisp and outcome-focused
- phrase V1 around the smallest credible workflow
- use V2 and Stretch to separate likely next steps from nice-to-haves
- write user-facing language first and defer technical schema details unless the user asks for them

### 5. Draft Supporting Pages When They Help

Create or adapt a dev page when the product page links to execution work.

Include lightweight sections such as:

- current focus
- initial milestones
- open questions
- linked project-management databases if they already exist

Create or adapt a research page when the product depends on external systems, public data, certifications, or market nuance.

Include lightweight sections such as:

- initial public data sources
- inputs to extract or normalize
- research questions

### 6. Sync The Repo README

Update `README.md` after the Notion brief is stable.

Keep it concise and product-facing. A good default README includes:

- product one-liner
- short product paragraph
- core user flow
- V1 scope
- optional V2 ideas
- current status

Keep terminology aligned with the Notion page. Do not let the repo and Notion drift into different product definitions within the same run.

### 7. Close With Concrete Outputs

Return:

- links to the created or updated Notion pages
- a short summary of the README changes
- any important assumptions made
- any notable preserved child pages or databases if duplication was used

## Notion Editing Notes

- Use Notion tools for real page creation and editing, not placeholder prose.
- Fetch `notion://docs/enhanced-markdown-spec` when complex Notion markdown or advanced blocks are needed.
- Use toggles, details blocks, and linked subpages when they match the user's existing style.
- When top-level page creation is awkward because the Notion API requires a parent, duplication of an existing top-level product page is the preferred fallback.

## Quality Bar

- Prefer practical shipping behavior over abstract brainstorming.
- Write as if the page is going to be used immediately by the founder.
- Keep the output structured, scannable, and close to the user's existing product voice.
- Optimize for "this is ready to work from" rather than "this is a loose brainstorm."
