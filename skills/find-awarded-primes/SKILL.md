---
name: find-awarded-primes
description: Query city, state, and federal open award datasets from a contract name, number, link, company, or contact; verify active primes, enrich subcontracting contacts, and present selectable leads for the user's Notion Sales CRM.
---

# Find awarded primes

Turn a procurement or organization clue into evidence-backed subcontracting prospects. Research first, present an interactive shortlist, and add only the records the user selects. This skill does not send outreach or create email drafts.

## Resolve the seed

Accept contract titles, solicitation/contract numbers, award URLs, agency names, company names, or a person's name/business phone/link. Treat “contact name/number” as a possible typo for “contract” when the surrounding context supports it. Resolve identifiers through live sources before searching by related scope. Ask one focused question only if multiple plausible identities would materially change the search; continue independent research meanwhile.

For a specific procurement, find its actual awardees first, including multiple lots or pool members. Do not silently replace a missing award with similar awards. For a company/contact seed, resolve the legal organization and find its relevant active government awards. Broaden to related primes only as a clearly labeled separate group. Start in the seed's jurisdiction; search NYC, NYS, and federal sources when the seed spans them or the user requests a broad search.

## Research awards and contacts

Read [sources.md](references/sources.md) for jurisdiction routing and evidence rules. Use live official records, APIs, downloads, and browser tools as available; re-check current documentation before constructing API requests. Follow pagination. Search engine snippets are discovery aids, not sufficient evidence for a final claim. Report inaccessible sources and search coverage rather than implying completeness.

Open-data queries are part of the research, not an optional substitute for browsing. Read [open-data-queries.md](references/open-data-queries.md) and query relevant NYC, NYS and federal datasets directly through supported APIs or official downloadable data. For a cross-jurisdiction search, cover all three levels; for a specific jurisdiction's contract, query its relevant datasets and mark other levels out of scope. Use portal catalog discovery to identify additional official award datasets when the named sources have coverage gaps. Do not rely exclusively on search-engine results or manually browsed notices. Record actual query filters, pagination, dataset freshness and failures in the evidence manifest and UI coverage summary.

Default output is up to 15 relevant organization/opportunity prospects, with actual awardees for a specific procurement taking precedence over that limit; disclose truncation and offer continuation. Do not impose a recent-award cutoff on active multi-year contracts. Deduplicate modifications and repeated notices into one award history; preserve distinct task orders and lots when material.

Use America/New_York's current date. Label activity as:
- **Active — verified:** official current status, or a current base/exercised term without contradictory closure evidence. Show the basis and checked date.
- **Awarded — starts later:** confirmed award with a future start.
- **Activity unconfirmed:** award confirmed, but term/status is missing, stale, conflicting, or depends on an unexercised option.
- **Ended/closed:** past term without a verified extension, termination, cancellation, or closeout.

Put verified active awards in the main list. Keep uncertain/future awards separately labeled and selectable, never silently call them active. If none are verified, say so. A vendor registration, plan-holder entry, bid submission, proposed award, or payment alone does not prove an active contract. A pool/vehicle award does not prove a funded task order or subcontracting availability.

Research the prime's public business contacts: named project/practice lead when verified, then subcontracting/supplier-diversity or small-business liaison, partnerships/business development, then a relevant general business channel. Verify current employer and role. Capture public email, business phone, contact form, supplier portal, and professional profile where available, each with its source and checked date. Label generic channels and role relevance. Never generate email addresses from naming patterns or present an agency procurement officer as the prime's contact. Missing contact details do not erase a verified award; label the gap.

Record facts separately from a suggested subcontracting angle. If assessing fit to the user’s organization, retrieve the current approved capability statement before making capability claims; otherwise describe the contract scope and potential support as a hypothesis. Never equate the prime's award value with the user's potential deal value.

## Present a selectable UI

Read [selection-ui.md](references/selection-ui.md). Always use the user's preferred selectable vendor-card report: company checkboxes, prominent contract amounts and dates, visible awarded scope, documented services, potential subcontracting opportunities, published contacts, and source links. Use the bundled card renderer and template rather than dense dossiers or per-company accordions. Keep essential comparisons visible. Put historical and unconfirmed awards in separate collapsed groups. Use Select all active vendors and one bottom selection tray with counts, selected names, Clear, and Add N selected leads to Notion. Preserve this presentation unless the user requests a different format. Save full evidence in a durable manifest; include checked date, coverage, value meaning, material gaps and truthful CRM duplicate state. Never use demonstration records in a real search.

The **Add selected to Sales CRM** action sends a follow-up containing the manifest path, run ID, and selected stable prospect IDs. That submitted action is the user's authorization to add those selected prospects; do not ask for redundant confirmation. Selection changes alone are not authorization. No browser-side Notion credentials or direct writes. Keep the manifest available across turns; if it is missing, recover the selected records from evidence or ask for the missing selection rather than guessing.

## Add selected leads

Read [crm.md](references/crm.md). Re-fetch the live schema, check duplicates, revalidate material facts if the results are stale, then create or safely enrich only the selected organization/opportunity records. Preserve prior outreach history and nonempty conflicting fields. Verify saved pages before reporting success. Report partial failures per record and reconcile uncertain write results before retries.

Finish with the selected-record counts (created, enriched, already present, failed) and returned Notion links. Do not claim an import happened when only the selector was rendered.
