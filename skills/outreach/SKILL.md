---
name: outreach
description: Create sales CRM leads and draft the user's outreach using Notion Outreach Step and Gmail conversation history, save personalized replies, and update outreach progress.
---

# Outreach

Use this skill for drafting initial outreach, stage-based follow-ups, and replies for sales CRM leads, and updating their Outreach Step accordingly. The current request controls recipients, scope, and whether output belongs in chat or Gmail Drafts. Completing a lead-specific draft includes the corresponding Outreach Step update unless the user requests drafting only. This skill does not itself authorize sending emails, changing unrelated CRM properties, or creating automations.

## Find or create the lead

Create a lead when the user explicitly requests creation, or when a lead-specific outreach task has no matching record in the Sales CRM. First fetch the current schema and search existing records using organization, contact email, and the specific opportunity/project. Reuse an existing matching record; several opportunities at one organization may legitimately have separate records. If the user explicitly requests a separate record, honor that distinction. Flag ambiguous matches rather than creating an accidental duplicate.

Create new records in this CRM data source, using a clear account/opportunity title, Status=`Lead` unless the user specifies another status, and supported Company, Email, Type, and source URL values from the request or verified sources. Do not invent contacts, deal values, or dates. Leave unsupported optional properties blank. Populate the page body with concise relevant context and verified conversation/source links, reading Notion's Markdown specification before writing content.

For creation without completed outreach, leave Outreach Step blank; do not claim contact occurred. After a finished draft is saved, set the numbered step and next Due Date according to the progress rules below. If an existing substantive reply is confirmed, use `Responded`. Keep Last Contact based on an actually sent message, never draft creation. Fetch the created page to verify its identity and properties, and include its returned Notion URL in the completion report.

## Context and sources

- Notion Sales CRM: use the data source supplied by the user. Confirm its schema before writing.
- Gmail: use the connected work account selected by the user. Confirm the account before drafting.
- Fetch the current CRM schema and selected account pages. Outreach Step, Status, Due Date, and Last Contact are distinct properties. Preserve the current option spelling.
- Read full relevant Gmail threads, including separate replies or alternate contacts. Match the specific account/deal using contacts, organization, project identifiers, and existing email links. Shared domains alone do not establish a match. Paginate searches where needed.
- Distinguish sent messages from unsent drafts. A CRM stage can have been advanced before its message was sent; reconcile discrepancies before writing another follow-up. Report unresolved matches or inaccessible sources rather than assuming no response.
- Use fetched Notion page URLs, including `/p/`, and Work Gmail account-specific message links when reporting evidence.

## Select the message

Treat Outreach Step as the recorded progress, then confirm it against the conversation:

| Current step | Appropriate message when requested |
|---|---|
| Blank or initial outreach | Introduce relevant services with a specific, modest ask based on the organization and supported facts. |
| 1 of 3 | Stage 2: briefly check whether they reviewed the previous message and capabilities statement, express interest in connecting and learning about their work, and invite a referral to the appropriate contact. |
| 2 of 3 | Stage 3: politely pause follow-ups, say the user will reconnect later, and invite a referral to another contact. |
| 3 of 3 | Do not repeat the closing follow-up by default. Inspect sent/draft evidence and report that the sequence is complete; draft further outreach only within the user's requested scope. |
| Responded or substantive reply found | Draft a contextual reply addressing what they actually said or requested, rather than an unanswered-outreach template. |
| Undelivered or Did not Respond | Inspect the failure or prior history. Report contact correction or re-engagement needs; do not blindly reuse a sequence message. |

Out-of-office notices, delivery errors/bounces, newsletters, and generic notifications are not substantive replies. Flag these with message links, any return date, and replacement contact. Do not tell a recipient they never responded if the thread contains a genuine reply.

## Capabilities statement for initial outreach

Attach the user's current capabilities statement to the first outreach email (`1 of 3`). Find the maintained document in the user's available files or connected Drive, using existing sent attachments as supporting evidence of the correct artifact. Verify the actual file and version rather than inventing a path or assuming an old attachment is current. If several versions exist, use the clearly maintained current version; if the choice is unresolved or the file is unavailable, ask for the document/location and report the attachment as incomplete.

Mention the attachment naturally in the initial email. Use Gmail's supported attachment mechanism and verify the saved draft contains the PDF with the expected filename, alongside the correct recipient and message. If attachment creation fails, report the failure and do not advance Outreach Step or reset Due Date until the complete initial draft is verified. Follow-ups do not require reattaching the statement unless requested or the conversation calls for it.

## Voice and approved closing example

For initial outreach, introduce the user personally after the greeting with their approved name, role, and organization. Follow with a brief, recipient-specific reason for reaching out. Prefer this personal introduction over opening with “We’re reaching out from…” or a company-only introduction. Use “I” for the user’s introduction and personal ask, then “we” and “our” when describing the collective’s services and experience. Do not repeat the introduction in established conversations or routine follow-ups.

Write warmly, directly, and briefly. Follow the recipient's existing greeting/name from the thread; do not invent names. Use `¡Hola [Name]!` and `Saludos,` where consistent with the user's prior messages. End email drafts with the closing greeting (normally `Saludos,`) but do not add the user's name, title, logo, contact details, booking link, or any signature block; the user adds their own signature. This applies to chat examples and saved Gmail drafts. Use the approved public-facing business name. Do not add unsupported capabilities, promises, or timelines.

Use this stage 2 example as a starting point and adapt it to the conversation. Mention the capabilities statement only if it was previously shared. Keep this a warm check-in; do not add a service pitch or procurement questions unless requested:

> ¡Hola [Name]!
>
> I just wanted to check in and see if you had a chance to review my previous message and our capabilities statement.
>
> I’d welcome the opportunity to connect and learn more about your work and whether our services could be helpful. If there’s someone else I should reach out to, I’d appreciate any guidance.
>
> Thank you for your time!
>
> Saludos,

Adapt this stage 3 example to the greeting, organization, and conversation:

> ¡Hola [Name]!
>
> I understand this may be a busy time of year, so I’ll pause my follow-ups for now and reconnect at a later date.
>
> If there’s someone else at [Organization] I should connect with about our services or upcoming opportunities, please let me know. I’d appreciate any guidance.
>
> Thank you for your time!
>
> Saludos,

Preserve the existing thread subject for replies.

## Review and delivery

- For any request to draft outreach for multiple contacts, first provide one generalized, copy-ready draft in chat and wait for the user to approve it or request edits before creating or revising Gmail drafts or changing their CRM outreach progress. Apply the approved wording across the batch with appropriate greetings and conversation-specific adjustments. Approval already given for the current wording and batch satisfies this requirement; do not ask again. For a single-contact request, provide a preview first only when requested.
- If the user requests drafts in Gmail, create personalized unsent replies in the existing conversations using the appropriate sent message as `reply_message_id`. Set the actual external recipient explicitly when replying to the user's sent message.
- Check for existing matching drafts before creating duplicates. Preserve unrelated drafts; revise a matching draft only when the user's request supports doing so.
- Verify saved drafts have the expected recipient, content, subject, and thread. Report count, failures, and a link to Work Gmail Drafts. Never equate draft creation with sending.
- Sending requires explicit user authorization.

## Update outreach progress

After saving and verifying a finished lead-specific Gmail draft, update the matching Notion account's Outreach Step to the drafted stage: initial outreach = `1 of 3`, stage 2 follow-up = `2 of 3`, stage 3 closing follow-up = `3 of 3`. This reflects the user's chosen workflow, in which the stage advances when the draft is prepared. Do not advance stages for a generic example, an unapproved batch, a failed draft save, or when the user requests drafting only. A chat-only example awaiting approval does not change the CRM.

If a substantive human reply is confirmed, set Outreach Step to `Responded` instead of advancing the sequence, including when drafting a reply to that message. Automatic replies and delivery errors do not justify `Responded`. Never overwrite an existing `Responded` value with a numbered stage unless explicitly requested.

Whenever a numbered outreach step is completed, also set Due Date to seven business days after that step's completion date. This schedules the next step relative to the preceding completed outreach step, not relative to an old due date. Under the user's draft-first workflow, use the date the finished draft is saved; when recording an already sent step, use its actual sent date. Use America/New_York calendar dates, start counting on the following day, and count Monday through Friday (the convention used in this workflow), unless the user specifies a holiday calendar or another date. A draft prepared Friday October 9, 2026 therefore sets Due Date to Tuesday October 20, 2026. Do not reset dates when merely re-reading a record or reporting an existing step. For a revision of the same draft, preserve the existing due date unless the user requests rescheduling. Responded is not a numbered sequence step; preserve its due date unless a follow-up date is requested.

Fetch the current schema before updates and use its exact option names. Write Due Date as a date-only property (`date:Due Date:start`, `date:Due Date:is_datetime=0`), clearing a previous range end if necessary. Verify each saved value and report the draft count, Outreach Step changes, and next due dates, including any failures. Preserve Status and Last Contact unless the user requests those changes. Keep sent-versus-drafted evidence explicit: a numbered stage alone is not proof an email was sent.

If the user requests CRM updates, apply only the named scope and verify saved values. For Lost/Did not Respond transitions, first confirm the final-stage email was actually sent and no substantive response arrived; unsent drafts or failed email checks are insufficient. For due dates, state the counting convention and use America/New_York dates. When asked for a list, include Notion account and relevant Gmail links.
