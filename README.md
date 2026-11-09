# How I Use AI

**I use AI to grow my capacity while keeping the parts of the work that help me think and learn.**

This repo is an open look at how I use AI harnesses, skills, plugins, and MCPs as an entrepreneur, software engineer, learner, and inventor. If a skill or workflow here is useful to you, feel free to copy it and ask your agent of choice to install it in your workflow.

| [01 · Harnesses](#01--harnesses) | [02 · Skills](#02--skills) | [03 · Plugins & MCPs](#03--plugins--mcps) |
| :--- | :--- | :--- |
| **Where I work** | **How I work** | **What I connect** |
| Codex in VS Code for hands-on development. Antigravity for longer refactors. | Reusable instructions for learning, building software, and pursuing business opportunities. | Access to the repos, databases, and applications I already use. |

## 01 · Harnesses

| **Codex in VS Code** | **Google Antigravity IDE + Superpowers** |
| :--- | :--- |
| **Hands-on software development.** I use Codex alongside my codebase to inspect changes, write specs, and implement user story tickets step by step. [Codex IDE extension](https://developers.openai.com/codex/ide/) | **Long-running refactors.** I spend time talking through the requirements with Superpowers before the refactor starts. When it’s complete, I run end-to-end tests. [Antigravity IDE](https://antigravity.google/docs/getting-started) · [Superpowers](https://github.com/obra/superpowers) |

## 02 · Skills

When I want to repeat a workflow, I write down how I want the agent to approach it, what it should produce, and how I’ll check the result.

To reuse a skill, copy its entire folder, including any scripts, references, and assets, and ask your agent to install it. The public copies use your own CRM, account, and template settings where my local versions depend on private workspace details. [Agent Skills documentation for Codex](https://developers.openai.com/codex/skills/)

### Software Engineering

| When I want to… | I reach for… |
| :--- | :--- |
| Understand a code path or learn a concept through a small build | [`teach-me`](skills/teach-me/) · [`question`](skills/question/) · [`quickstart-me`](skills/quickstart-me/) |
| See what I got wrong and work through the fix myself | [`correct-me`](skills/correct-me/) |
| Define how a feature should behave and build it in steps | [`spec`](skills/spec/) · [`implement`](skills/implement/) |
| Know what to test and verify before a release | [`testing-plan`](skills/testing-plan/) · [`prod-plan`](skills/prod-plan/) |
| Keep repo docs and product plans aligned with the work | [`branch-doc-sync`](skills/branch-doc-sync/) · [`notion-product-plan`](skills/notion-product-plan/) |

> **In practice · Deploying the VoteFeed Senate feed**
>
> I created a user story and tickets in Notion, then used `spec` to make a plan for each ticket and `implement` to code it step by step. After each implementation step, I manually tested the expected behavior before committing the code.

### Business Development

| When I want to… | I reach for… |
| :--- | :--- |
| Decide whether an RFP is worth pursuing and what I’d propose | [`evaluate-rfp`](skills/evaluate-rfp/) |
| Find companies with verified public contract awards | [`find-awarded-primes`](skills/find-awarded-primes/) |
| Draft a follow-up based on the email conversation and CRM stage | [`outreach`](skills/outreach/) |
| Show a potential partner where my team could contribute | [`intro-presentation`](skills/intro-presentation/) |

> **In practice · Preparing for a teaming meeting**
>
> I use public award records to see who holds a contract, then read the scope to identify where my team might contribute. That research shapes what I pitch in our introduction meetings.

## 03 · Plugins & MCPs

| Connection | What I use it for | Official resource |
| :--- | :--- | :--- |
| **GitHub** | Trace work across issues, branches, and code changes. | [GitHub MCP Server](https://github.com/github/github-mcp-server) |
| **Supabase** | Inspect schemas and verify that the data matches what I see in the app. | [Supabase MCP](https://supabase.com/docs/guides/ai-tools/mcp) |
| **Vercel** | Check deployments and prepare for releases. | [Vercel MCP](https://vercel.com/docs/agent-resources/vercel-mcp) |
| **Browser tools** | Test interactions, compare layouts, and capture screenshots for review. | [ChatGPT browser extension](https://learn.chatgpt.com/docs/chrome-extension) |
| **Notion** | Write user stories, organize tickets, and track business relationships. | [Notion MCP](https://www.notion.com/help/notion-mcp) |
| **Gmail** | Read the conversation before drafting a reply or updating the CRM. | [Gmail plugin](https://openai.com/business/plugins/gmail/) |
| **Google Drive & Slides** | Find source material and build editable procurement and teaming decks. | [Google Drive plugin setup](https://help.openai.com/en/articles/10929079-google-workspace-admin-managed-setup) |

For plugin installation and discovery, see the [ChatGPT and Codex plugin guide](https://learn.chatgpt.com/docs/plugins).
