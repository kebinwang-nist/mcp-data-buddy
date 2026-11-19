---
name: fda-drug-shortages
description: Query openFDA drug shortages (api.fda.gov/drug/shortages). Use it for current, resolved and to-be-discontinued drug shortages by generic name, company, therapeutic category, dosage form, shortage reason and availability.
---

# openFDA: Drug shortages

## Overview

- API: `https://api.fda.gov` (openFDA, Elasticsearch-based REST API). Docs: https://open.fda.gov/apis/drug/shortages/. Field definitions: https://open.fda.gov/fields/drugshortages.yaml.
- Snapshot taken 2026-11-19: 1,585 records; data last updated 2026-11-19 (`meta.last_updated`); bulk export date 2026-11-19 (download.json).
- Surface: read-only `GET`, JSON only. One endpoint; no per-record ids to look up.
- Auth: optional API key (env `OPENFDA_API_KEY`, sent as the Basic-auth username). Without a key: 240 requests/minute and 1,000/day per IP; with a key: 120,000/day. `count` with `limit=1000` needs a key.
- Disclaimer: openFDA asks users not to base medical care decisions on it and to treat all results as unvalidated; FDA may limit API access under its terms. Terms: https://open.fda.gov/terms/. License: https://open.fda.gov/license/.
- Sample record: one `limit=1` record was fetched to list the fields it returns; values were not stored.
- One record per product presentation (package) in a shortage, not per drug: `generic_name:"lidocaine"` returns many records. Records include the company's `contact_info`, usually a phone number.

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
| `drug/shortages` | Drug shortages | drug | 1,585 | 40 | 2026-11-19 |

## Endpoint

### drug/shortages

**Drug shortages**

- Endpoint: `GET https://api.fda.gov/drug/shortages.json`
- Records: 1,585. Last updated: 2026-11-19. Probe status: 200.
- Sample record fields (limit=1): `update_type`, `initial_posting_date`, `package_ndc`, `generic_name`, `contact_info`, `availability`, `openfda.application_number`, `openfda.brand_name`, `openfda.generic_name`, `openfda.manufacturer_name`, `openfda.product_ndc`, `openfda.product_type`, `openfda.route`, `openfda.substance_name`, `openfda.rxcui`, `openfda.spl_id`, `openfda.spl_set_id`, `openfda.package_ndc`, `openfda.unii`, `update_date`, `therapeutic_category`, `dosage_form`, `presentation`, `company_name`, `status`
- Also returned by the API (not in the field definitions): `openfda.application_number`, `openfda.generic_name`
- Example queries (run on 2026-11-19):

  ```
  # Shortages by status (200, 3 terms)
  GET https://api.fda.gov/drug/shortages.json?count=status
  # Therapeutic categories of current shortages (200, 5 terms)
  GET https://api.fda.gov/drug/shortages.json?search=status:"Current"&count=therapeutic_category&limit=5
  # Shortage records for lidocaine (200, 87 records)
  GET https://api.fda.gov/drug/shortages.json?search=generic_name:"lidocaine"&limit=1
  ```

| Field | Type | Exact | Description | Possible values |
|---|---|---|---|---|
| `availability` | string |  | Availability Information |  |
| `change_date` | date |  | Date of change for the presentation |  |
| `company_name` | string | yes | Company name that makes this drug product. |  |
| `contact_info` | string | yes | Contact information |  |
| `discontinued_date` | date |  | Date the presentation was discontinued |  |
| `dosage_form` | string | yes | The drug’s dosage form. There is no standard, but values may include terms like `tablet` or `solution for injection`. |  |
| `generic_name` | string | yes | Generic name(s) of the drug product. |  |
| `initial_posting_date` | date |  | Date the presentation was added to the public website |  |
| `openfda.brand_name` | string[] | yes | Brand or trade name of the drug product. |  |
| `openfda.dosage_form` | string[] | yes | The drug’s dosage form. There is no standard, but values may include terms like `tablet` or `solution for injection`. |  |
| `openfda.is_original_packager` | string[] | yes | Whether or not the drug has been repackaged for distribution. |  |
| `openfda.manufacturer_name` | string[] | yes | Name of manufacturer or company that makes this drug product, corresponding to the labeler code segment of the NDC. |  |
| `openfda.nui` | string[] | yes | Unique identifier applied to a drug concept within the National Drug File Reference Terminology (NDF-RT). | see NDF-RT (https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NDFRT/) |
| `openfda.original_packager_product_ndc` | string[] | yes | This ndc identifies the original packager. |  |
| `openfda.package_ndc` | string[] | yes | This number, known as the NDC, identifies the labeler, product, and trade package size. The first segment, the labeler code, is assigned by the FDA. A labeler is any firm that manufactures (including repackers or relabelers), or distribute… |  |
| `openfda.pharm_class_cs` | string[] | yes | Chemical structure classification of the drug product’s pharmacologic class. Takes the form of the classification, followed by `[Chemical/Ingredient]` (such as `Thiazides [Chemical/Ingredient]` or `Antibodies, Monoclonal [Chemical/Ingredie… |  |
| `openfda.pharm_class_epc` | string[] | yes | Established pharmacologic class associated with an approved indication of an active moiety (generic drug) that the FDA has determined to be scientifically valid and clinically meaningful. Takes the form of the pharmacologic class, followed… |  |
| `openfda.pharm_class_moa` | string[] | yes | Mechanism of action of the drug—molecular, subcellular, or cellular functional activity—of the drug’s established pharmacologic class. Takes the form of the mechanism of action, followed by `[MoA]` (such as `Calcium Channel Antagonists [Mo… |  |
| `openfda.pharm_class_pe` | string[] | yes | Physiologic effect or pharmacodynamic effect—tissue, organ, or organ system level functional activity—of the drug’s established pharmacologic class. Takes the form of the effect, followed by `[PE]` (such as `Increased Diuresis [PE]` or `De… |  |
| `openfda.product_ndc` | string[] | yes | The labeler manufacturer code and product code segments of the NDC number, separated by a hyphen. |  |
| `openfda.product_type` | string[] | yes | Type of drug product |  |
| `openfda.route` | string[] | yes | The route of administation of the drug product. | see Route of administration (http://www.fda.gov/ForIndustry/DataStandards/StructuredProductLabeling/ucm162034.htm) |
| `openfda.rxcui` | string[] | yes | The RxNorm Concept Unique Identifier. RxCUI is a unique number that describes a semantic concept about the drug product, including its ingredients, strength, and dose forms. | see RxNorm and RxCUI documentation (https://www.nlm.nih.gov/research/umls/rxnorm/docs/2012/rxnorm_doco_full_2012-3.html) |
| `openfda.spl_id` | string[] | yes | Unique identifier for a particular version of a Structured Product Label for a product. Also referred to as the document ID. |  |
| `openfda.spl_set_id` | string[] | yes | Unique identifier for the Structured Product Label for a product, which is stable across versions of the label. Also referred to as the set ID. |  |
| `openfda.substance_name` | string[] | yes | The list of active ingredients of a drug product. |  |
| `openfda.unii` | string[] | yes | Unique Ingredient Identifier, which is a non-proprietary, free, unique, unambiguous, non-semantic, alphanumeric identifier based on a substance’s molecular structure and/or descriptive information. | see Unique Ingredient Identifiers (http://fdasis.nlm.nih.gov/srs/srs.jsp) |
| `openfda.upc` | string[] | yes | Universal Product Code | see Universal Product Code (https://en.wikipedia.org/wiki/Universal_Product_Code) |
| `package_ndc` | string |  | This number, known as the NDC, identifies the labeler, product, and trade package size. The first segment, the labeler code, is assigned by the FDA. A labeler is any firm that manufactures (including repackers or relabelers), or distribute… |  |
| `presentation` | string | yes | Drug name, form, strength, and NDC number |  |
| `proprietary_name` | string | yes | Brand or trade name of the drug product. |  |
| `related_info` | string | yes | Specific availability information for the presentation |  |
| `related_info_link` | string |  | FDA resources and links |  |
| `resolved_note` | string |  | Information related to the resolved status of the presentation |  |
| `shortage_reason` | string | yes | Reason for shortage of the presentation |  |
| `status` | string |  | Presentation shortage status |  |
| `strength` | string[] | yes | Drug strength |  |
| `therapeutic_category` | string[] | yes | Therapeutic category |  |
| `update_date` | date |  | Date of update for the presentation |  |
| `update_type` | string |  | Type of update |  |

## Usage tips

- Pick the field by question:
  - Drug: `generic_name`, `proprietary_name`, `openfda.brand_name`, `presentation`, `package_ndc`, `company_name`.
  - State: `status` is `Current`, `To Be Discontinued` or `Resolved`; `availability`, `shortage_reason`, `resolved_note`.
  - Grouping: `therapeutic_category` (`Anesthesia`, `Pediatric`, `Psychiatry`, ...).
- **Dates are `MM/DD/YYYY` strings** (`update_date`, `initial_posting_date`, `change_date`, `discontinued_date`). Search one day as `update_date:"10/06/2026"`, and ranges as `update_date:[10/01/2026 TO 10/31/2026]` or `update_date:[2026-10-01 TO 2026-10-31]`. The `YYYYMMDD` form used by the other endpoints returns no matches here. `count=update_date` still returns `YYYYMMDD` time buckets.
- Count `therapeutic_category` and `status` without `.exact` (`therapeutic_category.exact` returns "Nothing to count").
- `.exact` is case-sensitive and matches the whole value. In drug/label, `openfda.brand_name.exact:"Tylenol"` returns no matches, while plain `openfda.brand_name:"tylenol"` returns 112 labels.
- A misspelled field name returns "No matches found!", the same as a search with no hits. fda_get_dataset adds a hint when a field is not in the table above.
- Counting a date field returns every date in the result, whatever the `limit`. Narrow the search to a date range first.
- Pass `fields` to fda_get_dataset to return only the paths you need, e.g. `fields=["openfda.brand_name", "boxed_warning"]`.
