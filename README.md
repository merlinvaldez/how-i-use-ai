# How I Use AI

**I use AI to grow my capacity while keeping the parts of the work that help me think and learn.**

This repo is an open look at how I use AI harnesses, skills, plugins, and MCPs as an entrepreneur, software engineer, learner, and inventor. If a skill or workflow here is useful to you, feel free to copy it and ask your agent of choice to install it.

| [01 · Harnesses](#01--harnesses) | [02 · Skills](#02--skills) | [03 · Plugins & MCPs](#03--plugins--mcps) |
| :--- | :--- | :--- |
| The applications I use for agentic AI work. | The repeatable processes I’ve set up to increase my capacity. | My work and context live across apps. These are the ones I’ve connected to my agents. |

## 01 · Harnesses

### Codex in VS Code

I use Codex alongside my codebase to inspect changes, write specs, and implement user story tickets step by step. [Codex IDE extension](https://developers.openai.com/codex/ide/)

### Google Antigravity IDE + Superpowers

For long-running refactors, I spend time talking through the requirements with Superpowers before the work starts. Once the refactor is complete, I run end-to-end tests. [Antigravity IDE](https://antigravity.google/docs/getting-started) · [Superpowers](https://github.com/obra/superpowers)

## 02 · Skills

When I want to repeat a workflow, I write down how I want the agent to approach it, what it should produce, and how I’ll check the result. To reuse a skill, copy its whole folder so the scripts, references, and assets come with it. [Codex skill setup](https://developers.openai.com/codex/skills/)

### Software Engineering

**In practice · Deploying the VoteFeed Senate feed**

I created a user story and tickets in Notion, then used `spec` to make a plan for each ticket and `implement` to code it step by step. After each step, I tested the expected behavior by hand before committing the code.

| When I want to… | I use… |
| :--- | :--- |
| Understand a code path or learn a concept through a small build | [`teach-me`](skills/teach-me/) · [`question`](skills/question/) · [`quickstart-me`](skills/quickstart-me/) |
| See what I got wrong and work through the fix myself | [`correct-me`](skills/correct-me/) |
| Define how a feature should behave and build it in steps | [`spec`](skills/spec/) · [`implement`](skills/implement/) |
| Know what to test and verify before a release | [`testing-plan`](skills/testing-plan/) · [`prod-plan`](skills/prod-plan/) |
| Keep repo docs and product plans aligned with the work | [`branch-doc-sync`](skills/branch-doc-sync/) · [`notion-product-plan`](skills/notion-product-plan/) |

### Business Development

**In practice · Preparing for a teaming meeting**

I use public award records to see who holds a contract, then read the scope to identify where my team could contribute. That research shapes what I pitch in our introduction meetings.

| When I want to… | I use… |
| :--- | :--- |
| Decide whether an RFP is worth pursuing and what I’d propose | [`evaluate-rfp`](skills/evaluate-rfp/) |
| Find companies with verified public contract awards | [`find-awarded-primes`](skills/find-awarded-primes/) |
| Draft a follow-up based on the email conversation and CRM stage | [`outreach`](skills/outreach/) |
| Show a potential partner where my team could contribute | [`intro-presentation`](skills/intro-presentation/) |

## 03 · Plugins & MCPs

| Connection | What I use it for |
| :--- | :--- |
| [GitHub](https://github.com/github/github-mcp-server) | Trace work across issues, branches, and code changes. |
| [Supabase](https://supabase.com/docs/guides/ai-tools/mcp) | Inspect schemas and verify that the data matches what I see in the app. |
| [Vercel](https://vercel.com/docs/agent-resources/vercel-mcp) | Check deployments and prepare for releases. |
| [Browser tools](https://learn.chatgpt.com/docs/chrome-extension) | Test interactions, compare layouts, and capture screenshots for review. |
| [Notion](https://www.notion.com/help/notion-mcp) | Write user stories, organize tickets, and track business relationships. |
| [Gmail](https://openai.com/business/plugins/gmail/) | Read the conversation before drafting a reply or updating the CRM. |
| [Google Drive & Slides](https://help.openai.com/en/articles/10929079-google-workspace-admin-managed-setup) | Find source material and build editable procurement and teaming decks. |
