# Public award research

Use official evidence and record source URL, record/award ID, retrieval date, and which facts each source supports. Refresh routes/documentation when unavailable; no source covers all contracts or reliably supplies a prime's decision-maker email.

## NYC

- [NYC Open Data — Recent Contract Awards](https://data.cityofnewyork.us/City-Government/Recent-Contract-Awards/qyyg-4tf5/about_data), dataset `qyyg-4tf5`: explicitly query vendor, PIN, title, agency and descriptions. Metadata exposes vendor name/address, amount and notice contacts. Check publisher/coverage; its citywide-procurement description does not establish complete coverage of every agency award. Notice contacts may represent the government, and notice start/end dates must not be assumed to be contract performance dates.
- [NYC Open Data catalog](https://data.cityofnewyork.us/): discover additional official City Record, agency, contract and procurement datasets; verify publisher, parent dataset/view, dictionary and freshness before use. See [query procedure](open-data-queries.md).

- [Checkbook NYC](https://www.checkbooknyc.com/): contract/vendor history and spending. [API documentation](https://www.checkbooknyc.com/data-feeds/api): XML over HTTP POST, pagination; verify current field definitions and distinguish contracts from payments.
- [PASSPort Public](https://www.nyc.gov/site/mocs/passport/passport-public.page): vendor, contract, solicitation records; cross-reference EPIN/PIN and legal vendor identity.
- [City Record Online](https://a856-cityrecord.nyc.gov/): award notices, solicitations, hearings; distinguish proposed action from final award. Search exact identifiers and title variants.
- [MOCS procurement source directory](https://www.nyc.gov/site/mocs/resources/public-procurement-sites.page): authoritative current links and procurement plans.

Link the notice, procurement, registered contract, amendments and vendor when possible. Resolve different identifiers with agency/title/vendor evidence, not title similarity alone.

## NYS and local public authorities

- [Open Book contract search](https://wwe2.osc.state.ny.us/transparency/contracts/contractsearch.cfm): state contract and amendment records and spreadsheet downloads. Review latest amendments for term/value changes; coverage depends on OSC reporting/review requirements.
- [NYS Contract Reporter](https://www.nyscr.ny.gov/home/contracts): locate original procurement, references, scope and agency contact; verify award outcome through available award notices, agency pages or contract records. A closed solicitation is not an award.
- [OGS centralized contract awards](https://ogs.ny.gov/procurement/ogs-centralized-contracts-list): awarded contractors, vehicles and supporting vendor documents; a vehicle ceiling is not committed spending.
- [State authority procurement dataset](https://data.ny.gov/Transparency/Procurement-Report-for-State-Authorities/ehig-g5x3).
- [Local authority procurement dataset](https://data.ny.gov/Transparency/Procurement-Report-for-Local-Authorities/8w5p-k45m).
- [NYS Open Data catalog](https://data.ny.gov/): query the authority datasets through their APIs or exports and discover relevant official state-agency procurement/award datasets. Catalog entries are discovery metadata, not award evidence. Use Open Book and agency records for gaps and current amendments.

The authority datasets are annual reported histories, not live status feeds or complete municipal-government coverage. Inspect their data dictionaries and API access links before filtering. For authorities or city/county buyers with coverage gaps, use the buyer's official awards, procurement reports and board approval records. Board approval may precede execution: retain that distinction.

## Federal

- [USAspending search](https://www.usaspending.gov/search) and [API documentation](https://api.usaspending.gov/docs/endpoints): prime awards, transactions, reported subawards, downloads. The public API currently needs no authorization; verify current docs. Filter by contract award type when seeking contracts, rather than mixing grants into the results.
- [Data.gov catalog](https://catalog.data.gov/): discover additional official federal agency award datasets and downloads; resolve to the publishing agency's actual data/API, confirm federal coverage, and deduplicate USAspending/SAM mirrors. Query USAspending as the baseline federal open award dataset, not just its website search. See [query procedure](open-data-queries.md).
- [SAM contract data](https://sam.gov/contract-data): contract actions, identifiers, recipients, NAICS/PSC, dates and status. Sign-in may be required. Use current SAM routes rather than assuming legacy FPDS search works.
- [SBA subcontracting resources](https://www.sba.gov/counseling/prime-and-subcontracting/): prime directories with subcontracting plans and links to SUBNet postings.
- [GSA subcontracting resources](https://www.gsa.gov/small-business/find-opportunities): prime directories and supplier research routes.

Distinguish parent vehicles from task orders, initial awards from modifications, obligations from potential ceilings, and base/current periods from options. Reported subawards help show partnering history but are incomplete and do not prove an open opportunity. A subcontracting plan is a prospecting signal, not a promise of work.

## Contact enrichment and coverage

Prefer the prime's official team, project, supplier and contact pages, then agency vendor documents and public professional profiles. Confirm organization aliases with legal names, identifiers such as UEI where available, and domains. Capture the actual contact source; distinguish named direct channels from switchboards/forms. Preserve conflicting contact evidence as a gap rather than selecting an unsupported winner.

For each run, summarize sources searched, filters/time range, pagination/truncation, inaccessible records, and unresolved award/status matches. Never translate an unavailable search into “no awards.”
