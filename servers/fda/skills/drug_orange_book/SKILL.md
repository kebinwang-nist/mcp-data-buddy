---
name: fda-drug-orange-book
description: Query the openFDA Orange Book (api.fda.gov/drug/orangebook). Use it for approved drug products with therapeutic equivalence (TE) codes, reference listed drugs, and the patents and exclusivities that protect an application, with expiration dates.
---

# openFDA: Orange Book (approved drug products with therapeutic equivalence evaluations)

## Overview

- API: `https://api.fda.gov` (openFDA, Elasticsearch-based REST API). Docs: https://open.fda.gov/apis/drug/orangebook/. Field definitions: https://open.fda.gov/fields/drugorangebook.yaml.
- Snapshot taken 2026-11-19: 48,990 records; data last updated 2026-11-19 (`meta.last_updated`); bulk export date 2026-11-19 (download.json).
- Surface: read-only `GET`, JSON only. One endpoint; no per-record ids to look up.
- Auth: optional API key (env `OPENFDA_API_KEY`, sent as the Basic-auth username). Without a key: 240 requests/minute and 1,000/day per IP; with a key: 120,000/day. `count` with `limit=1000` needs a key.
- Disclaimer: openFDA asks users not to base medical care decisions on it and to treat all results as unvalidated; FDA may limit API access under its terms. Terms: https://open.fda.gov/terms/. License: https://open.fda.gov/license/.
- Sample record: one `limit=1` record was fetched to list the fields it returns; values were not stored.

## Query parameters

| Param | Meaning | Example |
|---|---|---|
| `search` | Filter records: `field:term`, joined with `AND` / `OR` / `NOT`. Omit to match all records. | `search=serious:1+AND+receivedate:[20250101+TO+20251231]` |
| `count` | Count records per distinct value of one field instead of returning records. Returns `[{"term": ..., "count": n}]` (date fields: `{"time": ..., "count": n}`), most frequent first. | `count=patient.reaction.reactionmeddrapt.exact` |
| `limit` | Records (or count terms) to return. Max 1000; default here 10 for records and 100 for count. `count` with `limit=1000` needs an API key. | `limit=100` |
| `skip` | Records to skip, for paging. Max 25000; not allowed with `count`. | `skip=100` |
| `sort` | Sort records: `field:asc` or `field:desc`. | `sort=report_date:desc` |

Search notes:

- `field:term` matches a word in the field; quote phrases: `field:"two words"`. Combine terms with `AND`, `OR` and `NOT`, and group them with parentheses.
- Ranges: `field:[A TO B]` (inclusive). Dates are `YYYYMMDD` strings, e.g. `report_date:[20250101 TO 20251231]`.
- `_exists_:field` / `_missing_:field` match records where the field is present or absent.
- `field.exact` matches or counts the whole value, case-sensitively (`openfda.brand_name.exact:"TYLENOL"`). The plain field matches words case-insensitively. Count on `.exact` to get whole values instead of single words.
- No hits returns HTTP 404 `NOT_FOUND` "No matches found!", which is an empty result, not an error. A misspelled field name returns the same 404, so check field names in the table.
- HTTP 500 with `parse_exception` in the details is a search syntax error. "Text fields are not optimised" on a count means: count `<field>.exact` instead. "Nothing to count" on a `.exact` field can mean the field has no `.exact` variant; retry without `.exact`. The Exact column below is a guide, not a guarantee.
- With `fda_get_dataset`, write spaces as spaces, not `+`; the tool encodes them. A literal `+` breaks the query.

## Endpoint index

| Id | Name | Category | Records | Fields | Last updated |
|---|---|---|---|---|---|
| `drug/orangebook` | Orange Book (approved drug products with therapeutic equivalence evaluations) | drug | 48,990 | 27 | 2026-11-19 |

## Endpoint

### drug/orangebook

**Orange Book (approved drug products with therapeutic equivalence evaluations)**

- Endpoint: `GET https://api.fda.gov/drug/orangebook.json`
- Records: 48,990. Last updated: 2026-11-19. Probe status: 200.
- Sample record fields (limit=1): `approval_date`, `product_number`, `products.active_ingredients.name`, `products.active_ingredients.strength`, `products.brand_name`, `products.application_name`, `products.application_type`, `products.application_number`, `products.therapeutic_equivalence_codes`, `products.reference_listed_drug`, `products.reference_standard`, `products.marketing_status`, `products.application_full_name`, `products.dosage_form`, `products.route`
- Also returned by the API (not in the field definitions): `products.marketing_status`
- Example queries (run on 2026-11-19):

  ```
  # Orange Book entries for Lipitor (200, 4 records)
  GET https://api.fda.gov/drug/orangebook.json?search=products.brand_name:"LIPITOR"&limit=1
  # Products by application type (200, 2 terms)
  GET https://api.fda.gov/drug/orangebook.json?count=products.application_type
  # Applications with a patent expiring in 2027 (200, 635 records)
  GET https://api.fda.gov/drug/orangebook.json?search=patents.expiration_date:[20270101+TO+20271231]&limit=1
  ```

| Field | Type | Exact | Description | Possible values |
|---|---|---|---|---|
| `approval_date` | date |  | The date the product was approved as stated in the FDA approval letter to the applicant. |  |
| `approved_prior_to_1982` | boolean |  | Products approved prior to the January 1, 1982 contain the phrase: "Approved prior to Jan 1, 1982". |  |
| `exclusivity.exclusivity_code` | string |  | Code to designate exclusivity granted by the FDA to a drug product. |  |
| `exclusivity.exclusivity_code_definition` | string |  | The definition of the exclusivity code. |  |
| `exclusivity.exclusivity_expiration_date` | date |  | The date the exclusivity expires. |  |
| `patents.drug_product_flag` | boolean |  | Patents submitted on FDA Form 3542 and listed after August 18, 2003 may have a drug product flag indicating the sponsor submitted the patent as claiming the drug product. |  |
| `patents.drug_substance_flag` | boolean |  | Patents submitted on FDA Form 3542 and listed after August 18, 2003 may have a drug substance flag indicating the sponsor submitted the patent as claiming the drug substance. |  |
| `patents.expiration_date` | date |  | The date the patent expires as submitted by the applicant holder including applicable extensions. |  |
| `patents.patent_delist_flag` | boolean |  | The flag is set to 'Y' when an applicant holder has requested a patent to be delisted but the patent cannot be delisted. |  |
| `patents.patent_number` | string |  | Patent numbers as submitted by the applicant holder for patents covered by the statutory provisions. May repeat for multiple applications and multiple products. Includes pediatric exclusivity granted by the agency. |  |
| `patents.patent_submission_date` | date |  | The date on which the FDA receives patent information from the applicant holder. Patent submission date data is included for patents submitted after 2013. |  |
| `patents.patent_use_code` | string |  | A code to designate a method of use that covers the approved indication or use of a drug product. |  |
| `patents.patent_use_code_definition` | string |  | The definition of the patent use code. |  |
| `product_number` | string |  | The FDA assigned number to identify the application products. Each strength is a separate product. May repeat for multiple part products. |  |
| `products.active_ingredients.name` | string | yes | The names of the active, medicinal ingredients in the drug product. |  |
| `products.active_ingredients.strength` | string |  | The strength of the active, medicinal ingredients in the drug product. |  |
| `products.application_full_name` | string | yes | The full name of the firm holding legal responsibility for the new drug application. |  |
| `products.application_name` | string | yes | Name of the Applicant for the drug product. |  |
| `products.application_number` | string |  | The FDA assigned number to the application. |  |
| `products.application_type` | string |  | The type of new drug application approval. |  |
| `products.brand_name` | string | yes | Brand or trade name of the drug product. |  |
| `products.dosage_form` | string | yes | The drug’s dosage form. There is no standard, but values may include terms like `tablet` or `solution for injection`. |  |
| `products.product_type` | string | yes | The group or category of approved drugs. |  |
| `products.reference_listed_drug` | boolean |  | The RLD is a drug product approved under section 505(c) of the FD&C Act for which FDA has made a finding of safety and effectiveness. In the electronic Orange Book, an RLD is identified by “RLD” in the RLD column. |  |
| `products.reference_standard` | boolean |  | A highly purified compound that is well characterized. |  |
| `products.route` | string | yes | The route of administration of the drug product. |  |
| `products.therapeutic_equivalence_codes` | string[] | yes | The TE Code indicates the therapeutic equivalence rating of generic to innovator Rx products. |  |

## Usage tips

- Pick the field by question:
  - Product: `products.brand_name` (uppercase, e.g. `LIPITOR`), `products.active_ingredients.name`, `products.dosage_form`, `products.route`, `products.application_number`, `products.application_type` (`A` ANDA, `N` NDA).
  - Equivalence: `products.therapeutic_equivalence_codes` (TE codes such as `AB`), `products.reference_listed_drug`, `products.reference_standard`.
  - Protection: `patents.patent_number`, `patents.expiration_date`, `patents.patent_use_code`, `exclusivity.exclusivity_code`, `exclusivity.exclusivity_expiration_date`.
- `products.marketing_status` is returned by the API but is not in the field definitions.
- `patents` and `exclusivity` are lists: a date range on `patents.expiration_date` matches applications with at least one patent in the range.
- `.exact` is case-sensitive and matches the whole value. In drug/label, `openfda.brand_name.exact:"Tylenol"` returns no matches, while plain `openfda.brand_name:"tylenol"` returns 112 labels.
- A misspelled field name returns "No matches found!", the same as a search with no hits. fda_get_dataset adds a hint when a field is not in the table above.
- Counting a date field returns every date in the result, whatever the `limit`. Narrow the search to a date range first.
- Pass `fields` to fda_get_dataset to return only the paths you need, e.g. `fields=["openfda.brand_name", "boxed_warning"]`.
