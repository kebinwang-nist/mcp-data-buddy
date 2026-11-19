---
name: fda-food-recalls
description: Query openFDA food recall enforcement reports (api.fda.gov/food/enforcement). Use it for food and dietary supplement recalls since 2012 by firm, product, reason (such as Listeria, Salmonella or undeclared allergens), classification, state and report date.
---

# openFDA: Food recalls (enforcement reports)

## Overview

- API: `https://api.fda.gov` (openFDA, Elasticsearch-based REST API). Docs: https://open.fda.gov/apis/food/enforcement/. Field definitions: https://open.fda.gov/fields/foodenforcement.yaml.
- Snapshot taken 2026-11-19: 29,609 records; data last updated 2026-11-11 (`meta.last_updated`); bulk export date 2026-11-19 (download.json).
- Surface: read-only `GET`, JSON only. One endpoint; no per-record ids to look up.
- Auth: optional API key (env `OPENFDA_API_KEY`, sent as the Basic-auth username). Without a key: 240 requests/minute and 1,000/day per IP; with a key: 120,000/day. `count` with `limit=1000` needs a key.
- Disclaimer: openFDA asks users not to base medical care decisions on it and to treat all results as unvalidated; FDA may limit API access under its terms. Terms: https://open.fda.gov/terms/. License: https://open.fda.gov/license/.
- Sample record: one `limit=1` record was fetched to list the fields it returns; values were not stored.
- Coverage: `report_date` starts on 2012-06-20. Records name the recalling firm with its address.

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
| `food/enforcement` | Food recalls (enforcement reports) | food | 29,609 | 48 | 2026-11-11 |

## Endpoint

### food/enforcement

**Food recalls (enforcement reports)**

- Endpoint: `GET https://api.fda.gov/food/enforcement.json`
- Records: 29,609. Last updated: 2026-11-11. Probe status: 200.
- Sample record fields (limit=1): `status`, `city`, `state`, `country`, `classification`, `openfda`, `product_type`, `event_id`, `recalling_firm`, `address_1`, `address_2`, `postal_code`, `voluntary_mandated`, `initial_firm_notification`, `distribution_pattern`, `recall_number`, `product_description`, `product_quantity`, `reason_for_recall`, `recall_initiation_date`, `center_classification_date`, `termination_date`, `report_date`, `code_info`, `more_code_info`
- Also returned by the API (not in the field definitions): `postal_code`
- Example queries (run on 2026-11-19):

  ```
  # Listeria recalls reported in 2025 (200, 373 records)
  GET https://api.fda.gov/food/enforcement.json?search=reason_for_recall:"listeria"+AND+report_date:[20250101+TO+20251231]&limit=1
  # States of the recalling firms in 2025 (200, 5 terms)
  GET https://api.fda.gov/food/enforcement.json?search=report_date:[20250101+TO+20251231]&count=state.exact&limit=5
  # Recalls by classification (200, 4 terms)
  GET https://api.fda.gov/food/enforcement.json?count=classification.exact
  ```

| Field | Type | Exact | Description | Possible values |
|---|---|---|---|---|
| `address_1` | string | yes |  |  |
| `address_2` | string | yes |  |  |
| `center_classification_date` | date |  |  |  |
| `city` | string | yes | The city in which the recalling firm is located. |  |
| `classification` | string | yes | Numerical designation (I, II, or III) that is assigned by FDA to a particular product recall that indicates the relative degree of health hazard. | `Class I`: Dangerous or defective products that predictably could cause serious health problems or death. Examples include: food found to contain botulinum toxin, food with undeclared allergens, a label mix-up on a lifesaving drug, or a de… |
| `code_info` | string |  | A list of all lot and/or serial numbers, product numbers, packer or manufacturer numbers, sell or use by dates, etc., which appear on the product or its labeling. |  |
| `country` | string | yes | The country in which the recalling firm is located. |  |
| `distribution_pattern` | string |  | General area of initial distribution such as, “Distributors in 6 states: NY, VA, TX, GA, FL and MA; the Virgin Islands; Canada and Japan”. The term “nationwide” is defined to mean the fifty states or a significant portion. Note that subseq… |  |
| `event_id` | string |  | A numerical designation assigned by FDA to a specific recall event used for tracking purposes. |  |
| `initial_firm_notification` | string | yes | The method(s) by which the firm initially notified the public or their consignees of a recall. A consignee is a person or firm named in a bill of lading to whom or to whose order the product has or will be delivered. |  |
| `more_code_info` | string |  |  |  |
| `openfda.application_number` | string[] | yes |  |  |
| `openfda.brand_name` | string[] | yes |  |  |
| `openfda.dosage_form` | string[] | yes |  |  |
| `openfda.generic_name` | string[] | yes |  |  |
| `openfda.is_original_packager` | boolean | yes |  |  |
| `openfda.manufacturer_name` | string[] | yes |  |  |
| `openfda.nui` | string[] | yes |  |  |
| `openfda.original_packager_product_ndc` | string[] | yes |  |  |
| `openfda.package_ndc` | string[] | yes |  |  |
| `openfda.pharm_class_cs` | string[] | yes |  |  |
| `openfda.pharm_class_epc` | string[] | yes |  |  |
| `openfda.pharm_class_moa` | string[] | yes |  |  |
| `openfda.pharm_class_pe` | string[] | yes |  |  |
| `openfda.product_ndc` | string[] | yes |  |  |
| `openfda.product_type` | string[] | yes | The type of product being recalled. For food queries, this will always be `Food`. | `Drugs`: The recalled product is a drug product.; `Devices`: The recalled product is a device product.; `Food`: The recalled product is a food product. |
| `openfda.route` | string[] | yes |  |  |
| `openfda.rxcui` | string[] | yes |  |  |
| `openfda.rxstring` | string[] | yes |  |  |
| `openfda.rxtty` | string[] | yes |  |  |
| `openfda.spl_id` | string[] | yes |  |  |
| `openfda.spl_set_id` | string[] | yes |  |  |
| `openfda.substance_name` | string[] | yes |  |  |
| `openfda.unii` | string[] | yes |  |  |
| `openfda.upc` | string[] | yes |  |  |
| `product_code` | string |  |  |  |
| `product_description` | string |  | Brief description of the product being recalled. |  |
| `product_quantity` | string |  | The amount of defective product subject to recall. |  |
| `product_type` | string | yes |  |  |
| `reason_for_recall` | string |  | Information describing how the product is defective and violates the FD&C Act or related statutes. |  |
| `recall_initiation_date` | date |  | Date that the firm first began notifying the public or their consignees of the recall. |  |
| `recall_number` | string | yes | A numerical designation assigned by FDA to a specific recall event used for tracking purposes. |  |
| `recalling_firm` | string | yes | The firm that initiates a recall or, in the case of an FDA requested recall or FDA mandated recall, the firm that has primary responsibility for the manufacture and (or) marketing of the product to be recalled. |  |
| `report_date` | date |  | Date that the FDA issued the enforcement report for the product recall. |  |
| `state` | string | yes | The U.S. state in which the recalling firm is located. |  |
| `status` | string | yes |  | `On-Going`: A recall which is currently in progress.; `Completed`: The recall action reaches the point at which the firm has actually retrieved and impounded all outstanding product that could reasonably be expected to be recovered, or has… |
| `termination_date` | date |  |  |  |
| `voluntary_mandated` | string | yes | Describes who initiated the recall. Recalls are almost always voluntary, meaning initiated by a firm. A recall is deemed voluntary when the firm voluntarily removes or corrects marketed products or the FDA requests the marketed products be… |  |

## Usage tips

- Pick the field by question:
  - Severity: `classification` (`Class I`, `Class II`, `Class III`, `Not Yet Classified`; count `classification.exact`).
  - Why: `reason_for_recall` (free text; search words such as `"listeria"`, `"salmonella"`, `"undeclared"`).
  - Who and what: `recalling_firm`, `product_description`, `state` and `city` of the firm, `distribution_pattern`.
  - Progress: `status` (`Terminated`, `Ongoing`, `Completed`), `recall_initiation_date`, `report_date`, `termination_date`.
- `state` needs `.exact` to count: `count=state` returns HTTP 500 "Text fields are not optimised", `count=state.exact` returns 2-letter codes (`CA`, `TX`, `IL`, ...). It is the firm's state, not where the product was sold; see `distribution_pattern` for that.
- The `openfda` fields are defined but empty for food recalls.
- `.exact` is case-sensitive and matches the whole value. In drug/label, `openfda.brand_name.exact:"Tylenol"` returns no matches, while plain `openfda.brand_name:"tylenol"` returns 112 labels.
- A misspelled field name returns "No matches found!", the same as a search with no hits. fda_get_dataset adds a hint when a field is not in the table above.
- Counting a date field returns every date in the result, whatever the `limit`. Narrow the search to a date range first.
- Pass `fields` to fda_get_dataset to return only the paths you need, e.g. `fields=["openfda.brand_name", "boxed_warning"]`.
