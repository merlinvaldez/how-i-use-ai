# Sales CRM import

Destination: the Notion Sales CRM data source supplied by the user. Confirm the destination and fetch its live schema on every import. Discover available Notion fetch/query/create/update tools and their current parameter schemas. Read `notion://docs/enhanced-markdown-spec` before writing page bodies.

## Match before writing

Search by legal/trading company name, email, contract/solicitation ID and opportunity. Same organization alone is not a duplicate. Default to one record per company + opportunity; consolidate multiple lots/awards for the same sales conversation in its body. Separate genuinely different opportunities. Include contacts as roles within that lead rather than creating one lead per person by default.

For an exact existing company/opportunity match, link it and add new verified research only where useful. Do not reset Status, outreach stages, dates, owner, existing notes or relationships. Do not overwrite conflicting nonempty contact fields; append a sourced alternative to the body and report it. If the match is ambiguous, mark it for resolution and continue other selected records.

## New-record mapping

| Current property | Value |
|---|---|
| Name | Prime company — specific contract/project |
| Company | Verified prime legal/trading organization |
| Status | Lead |
| Type | Subcontract |
| Email / Phone | Best verified business channel; distinguish general channel in body |
| URL (`userDefined:URL` in current tool schema) | Best official award/contract record; retain company/contact URLs in body |
| Outreach Step / Last Contact | Blank: research/import does not establish outreach |
| Due Date / Expected Close | Blank unless user supplied a date |
| Estimated Value | Blank unless the user's own potential subcontract value is supported; never copy prime award value |
| Priority / Account Owner / Tickets | Set only with supported user instruction; preserve on existing records |
| Added / buttons / formulas / read-only fields | Leave system-managed |

Use live property names/types and existing options; do not alter the CRM schema to fit an import. Save additional verified detail in page content. If a property disappeared, preserve its information in the body and report the mapping limitation.

## Page content

Include concise, source-linked sections:
- **Lead summary:** prime, opportunity, buyer, why this could be a subcontracting conversation; distinguish hypothesis from confirmed demand.
- **Award details:** legal awardee, jurisdiction/agency, contract and solicitation IDs, lots/task orders/parent vehicle, scope, original/current/maximum value with labels, currency, award/start/current-end dates, exercised extensions, status basis, checked date. Unknown facts stay unknown.
- **People and channels:** recommended contact, role and employer verification, email, phone, professional profile, supplier registration/contact form; alternate contacts and why each is relevant. Source and checked date for each.
- **Suggested approach:** specific question/service area to discuss, inferred fit explicitly labeled; no invented capabilities, budgets or commitments.
- **Evidence and gaps:** original user seed, official links, limitations, conflicting records, missing contact or active-term evidence.
- **Import provenance:** run ID, prospect ID and import date to reconcile retries.

Include enough evidence in Notion that the lead remains useful without its local manifest. Do not paste large raw API responses.

Read back each written page and properties. On a timeout or uncertain response, query by company/opportunity and import provenance before retrying creation. Report created/enriched/already-present/failed separately with fetched page URLs. No sending, draft creation, supplier registration, or follow-up scheduling is implied by selecting a CRM import.
