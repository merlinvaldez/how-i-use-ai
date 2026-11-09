# Query city, state and federal open award data

Use read-only data requests. No new paid subscriptions, API-key creation or account setup is implied. If a source needs unavailable credentials, use its public supported export/UI or report the access gap while continuing other sources. Do not claim a query ran unless results or a concrete failure were observed.

## Source selection

| Level | Required relevant baseline | Expand coverage with |
|---|---|---|
| NYC | Recent Contract Awards `qyyg-4tf5` on `data.cityofnewyork.us`, plus Checkbook contracts API | Official NYC Open Data procurement/City Record/agency datasets, PASSPort and agency award records |
| NYS | State authority `ehig-g5x3` and local authority `8w5p-k45m` on `data.ny.gov` when the buyer is an authority or the search is broad | NYS catalog discovery, Open Book exports, OGS and agency awards; do not treat authority reports as all state-agency contracts |
| Federal | USAspending contract-award API or official filtered downloads | SAM public award data where accessible; official federal agency award datasets discovered through Data.gov |

For a known state-agency procurement, prioritize agency/Open Book records rather than forcing unrelated authority searches. For a broad company/service search, query both authority datasets. Explicitly mark sources not applicable, unavailable, searched with no matches, or partially searched. Never imply that querying all three levels covers every public contract.

## Socrata portals: inspect, filter, paginate

1. Retrieve current metadata via `https://<portal>/api/views/<dataset-id>.json` or the dataset's official API documentation. Confirm title, publisher, description, update time, field identifiers/types and view/parent relationships. Check dictionaries for date and amount semantics. Fields can change.
2. Use the dataset-supported query API. Public SODA resource routes such as `https://<portal>/resource/<dataset-id>.json` may accept URL-encoded `$select`, `$where`, `$order`, `$limit`, `$offset` and `$q`. Verify availability rather than assuming anonymous access. Current [SODA3 documentation](https://dev.socrata.com/docs/queries/) describes POST queries and app-token/authentication requirements; do not assume those rules or payloads are identical to legacy resource routes.
3. Match exact contract/PIN/vendor identifiers first, then normalized legal/trading names and title/description keywords. Use field-specific filters where available; combine relevant text fields without relying on a single exact title. Use current schema names, not display labels. Escape SoQL string literals and URL-encode request parameters through the HTTP client; never interpolate seed text into shell code.
4. Request only needed columns, with stable ordering and pagination. Count matching rows when supported; continue until exhausted or disclose the explicit cap, retrieved count and next page/offset. A result display limit must not silently become the search limit. For large datasets use a supported filtered export.
5. Preserve raw matched records or sufficient field-level evidence in the durable run manifest, including record IDs, query URL/body without credentials, dataset URL, data update timestamp, retrieved timestamp and pages/counts. Avoid embedding a whole unrelated dataset in the manifest.

For `qyyg-4tf5`, fields verified on 2026-10-15 include `request_id`, `pin`, `vendor_name`, `vendor_address`, `agency_name`, `short_title`, `contract_amount`, `type_of_notice_description`, `contact_name`, `contact_phone`, `email`, `start_date`, `end_date`, `additional_description_1`, `additional_description_2`, `additional_description_3`, `document_links`. Verify them again at use. The contact fields do not establish employer/role, and the generic date names do not establish a contract term.

## USAspending structured queries

Read the current endpoint-specific request schema linked from [API documentation](https://api.usaspending.gov/docs/endpoints). Use `/api/v2/search/spending_by_award/` for contract-recipient/award discovery, `/api/v2/awards/<AWARD_ID>/` for detail, transaction endpoints for amendments/actions and `/api/v2/subawards/` for reported partners when useful. Use supported download endpoints if a large result set is more practical as CSV.

Apply contract award-type filters, then exact award/recipient identifiers or relevant keywords, agencies, NAICS/PSC, place of performance and dates as appropriate to the seed. Recipient headquarters location and performance location answer different questions. Do not exclude an active multi-year award merely because it was signed before a recent window. Inspect current performance period/options and modifications before declaring activity. Paginate with the endpoint's documented mechanism and retain canonical award IDs to deduplicate actions and mirrors. Reported subawards are historical evidence, not open subcontract requests.

## Dataset discovery and reconciliation

Search NYC/NYS/Data.gov catalogs using the seed's buyer, contract/award/procurement terms and service scope. Inspect official publisher resources before querying; do not invent dataset IDs or API schemas. Prefer maintained base datasets to community-created filtered views, and do not count several views of one dataset as independent corroboration. If discovery APIs are unavailable, use catalog UI/search and follow through to actual datasets/downloads.

Merge the same award across dataset, notice and payment sources using jurisdiction + agency + contract/award ID, and corroborating vendor identity. Keep original identifiers, lots and task orders. Different numbers without a verified crosswalk are possible matches, not automatic merges. Maintain the strongest current activity evidence and disclose conflicts. Enrich prime business contacts separately from procurement notice contacts.

## Coverage record

In the manifest add an `open_data_queries` array, one entry per dataset/query, with: level, portal, dataset ID/title/publisher, dataset URL, metadata checked time, data last updated (or unknown), filters/request, pages retrieved, matched/retrieved counts when available, truncation/continuation, outcome and access/error notes. Summarize this in the UI's coverage text. Store award-specific evidence links in each prospect and carry relevant provenance into selected Notion leads. Never expose credentials in the manifest, UI or CRM.
