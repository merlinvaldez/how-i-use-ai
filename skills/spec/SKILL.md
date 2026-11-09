---
name: spec
description: Create a reviewable Markdown feature spec in a project's specs folder, describing desired user behavior and an ordered, beginner-friendly implementation checklist. Use when the user asks to plan a feature or change before coding; do not use for implementation-only requests.
---

# Spec

Turn the user's feature idea into a Markdown plan they can read, review, and later hand to an AI for implementation.

1. Read the request and any linked ticket, mockup, or relevant project files. Trace just enough of the current behavior to make the plan accurate. Treat examples and mockup numbers as illustrations unless the user says otherwise.
2. If a missing product choice would materially change the user's experience or the implementation steps, ask the user before settling it in the spec. Use the multiple-choice question UI (`request_user_input` when available, otherwise `request_user_input_async`) with 2–3 clear, mutually exclusive options and a brief tradeoff for each. Put the recommended option first. Group up to three related questions in one prompt. A preselected option is not an answer; use the response the user actually submits. If the UI is unavailable, ask a concise question in the conversation. For optional choices that remain unanswered, state the assumption in the spec; do not invent an answer to a choice that blocks an accurate plan.
3. Create or update one clearly named `.md` file in the project's `specs/` folder. Create the folder if needed. If the user supplied an image, save a durable copy in `specs/assets/` when accessible and embed it with a relative Markdown path.
4. Start with **Desired user behavior**. Describe what people can see and do, including the important loading, empty, and error states. Use everyday language and concrete examples. Record any remaining assumptions or open decisions clearly.
5. Follow with **Implementation steps**, in the order the work should happen. Give each step a short outcome and a checklist of code work. Explain what should change and why in plain language a novice developer can follow. Name likely files or parts of the app only when helpful; avoid low-level design instructions unless correctness depends on them.
6. End with **How to check it works**: a short checklist of observable user flows and important edge cases. Keep checks specific enough that the user or an implementing AI can tell when the work is done.

Keep the plan proportional to the request. Separate user behavior from code tasks. Use unchecked `- [ ]` boxes for work that has not been done; do not imply the plan is already implemented. Preserve existing project conventions and call out dependencies or current behavior that affect the feature. Do not change app code, deploy, or update an external ticket when the user asked only for a spec.
