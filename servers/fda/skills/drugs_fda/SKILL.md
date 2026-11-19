---
name: fda-drugs-fda
description: Query openFDA Drugs@FDA (api.fda.gov/drug/drugsfda). Use it for FDA-approved drug applications (NDA, ANDA, BLA) with their sponsor, products, marketing status, and submission history such as original approvals, supplements and approval dates.
---

# openFDA: Drugs@FDA approvals

## Overview

- API: `https://api.fda.gov` (openFDA, Elasticsearch-based REST API). Docs: https://open.fda.gov/apis/drug/drugsfda/. Field definitions: https://open.fda.gov/fields/drugsfda.yaml.
- Snapshot taken 2026-11-19: 29,468 records; data last updated 2026-11-18 (`meta.last_updated`); bulk export date 2026-11-19 (download.json).
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
| `drug/drugsfda` | Drugs@FDA approvals | drug | 29,468 | 43 | 2026-11-18 |

## Endpoint

### drug/drugsfda

**Drugs@FDA approvals**

- Endpoint: `GET https://api.fda.gov/drug/drugsfda.json`
- Records: 29,468. Last updated: 2026-11-18. Probe status: 200.
- Sample record fields (limit=1): `submissions.submission_type`, `submissions.submission_number`, `submissions.submission_status`, `submissions.submission_status_date`, `submissions.submission_class_code`, `submissions.submission_class_code_description`, `application_number`, `sponsor_name`, `openfda.application_number`, `openfda.brand_name`, `openfda.generic_name`, `openfda.manufacturer_name`, `openfda.product_ndc`, `openfda.product_type`, `openfda.route`, `openfda.substance_name`, `openfda.rxcui`, `openfda.spl_id`, `openfda.spl_set_id`, `openfda.package_ndc`, `openfda.nui`, `openfda.pharm_class_pe`, `openfda.pharm_class_epc`, `openfda.unii`, `products.product_number`, `products.reference_drug`, `products.brand_name`, `products.active_ingredients.name`, `products.active_ingredients.strength`, `products.reference_standard`, `products.dosage_form`, `products.route`, `products.marketing_status`
- Also returned by the API (not in the field definitions): `openfda.product_type`
- Example queries (run on 2026-11-19):

  ```
  # Applications for Lipitor (200, 1 records)
  GET https://api.fda.gov/drug/drugsfda.json?search=openfda.brand_name:"lipitor"&limit=1
  # Sponsors with the most original submissions dated 2025 (200, 5 terms)
  GET https://api.fda.gov/drug/drugsfda.json?search=submissions.submission_type:"ORIG"+AND+submissions.submission_status_date:[20250101+TO+20251231]&count=sponsor_name&limit=5
  # Products by marketing status (200, 4 terms)
  GET https://api.fda.gov/drug/drugsfda.json?count=products.marketing_status
  ```

| Field | Type | Exact | Description | Possible values |
|---|---|---|---|---|
| `application_number` | string |  | This corresponds to the NDA, ANDA, or BLA number reported by the labeler for products which have the corresponding Marketing Category designated. If the designated Marketing Category is OTC Monograph Final or OTC Monograph Not Final, then… |  |
| `openfda.application_number` | string[] | yes | This corresponds to the NDA, ANDA, or BLA number reported by the labeler for products which have the corresponding Marketing Category designated. If the designated Marketing Category is OTC Monograph Final or OTC Monograph Not Final, then… |  |
| `openfda.brand_name` | string[] | yes | Brand or trade name of the drug product. |  |
| `openfda.generic_name` | string[] | yes | Generic name(s) of the drug product. |  |
| `openfda.manufacturer_name` | string[] | yes | Name of manufacturer or company that makes this drug product, corresponding to the labeler code segment of the NDC. |  |
| `openfda.nui` | string[] | yes | Unique identifier applied to a drug concept within the National Drug File Reference Terminology (NDF-RT). | see NDF-RT (https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NDFRT/) |
| `openfda.package_ndc` | string[] | yes | This number, known as the NDC, identifies the labeler, product, and trade package size. The first segment, the labeler code, is assigned by the FDA. A labeler is any firm that manufactures (including repackers or relabelers), or distribute… |  |
| `openfda.pharm_class_cs` | string[] | yes | Chemical structure classification of the drug product’s pharmacologic class. Takes the form of the classification, followed by `[Chemical/Ingredient]` (such as `Thiazides [Chemical/Ingredient]` or `Antibodies, Monoclonal [Chemical/Ingredie… |  |
| `openfda.pharm_class_epc` | string[] | yes | Established pharmacologic class associated with an approved indication of an active moiety (generic drug) that the FDA has determined to be scientifically valid and clinically meaningful. Takes the form of the pharmacologic class, followed… |  |
| `openfda.pharm_class_moa` | string[] | yes | Mechanism of action of the drug—molecular, subcellular, or cellular functional activity—of the drug’s established pharmacologic class. Takes the form of the mechanism of action, followed by `[MoA]` (such as `Calcium Channel Antagonists [Mo… |  |
| `openfda.pharm_class_pe` | string[] | yes | Physiologic effect or pharmacodynamic effect—tissue, organ, or organ system level functional activity—of the drug’s established pharmacologic class. Takes the form of the effect, followed by `[PE]` (such as `Increased Diuresis [PE]` or `De… |  |
| `openfda.product_ndc` | string[] | yes | The labeler manufacturer code and product code segments of the NDC number, separated by a hyphen. |  |
| `openfda.route` | string[] | yes | The route of administation of the drug product. | see Route of administration (http://www.fda.gov/ForIndustry/DataStandards/StructuredProductLabeling/ucm162034.htm) |
| `openfda.rxcui` | string[] | yes | The RxNorm Concept Unique Identifier. RxCUI is a unique number that describes a semantic concept about the drug product, including its ingredients, strength, and dose forms. | see RxNorm and RxCUI documentation (https://www.nlm.nih.gov/research/umls/rxnorm/docs/2012/rxnorm_doco_full_2012-3.html) |
| `openfda.spl_id` | string[] | yes | Unique identifier for a particular version of a Structured Product Label for a product. Also referred to as the document ID. |  |
| `openfda.spl_set_id` | string[] | yes | Unique identifier for the Structured Product Label for a product, which is stable across versions of the label. Also referred to as the set ID. |  |
| `openfda.substance_name` | string[] | yes | The list of active ingredients of a drug product. |  |
| `openfda.unii` | string[] | yes | Unique Ingredient Identifier, which is a non-proprietary, free, unique, unambiguous, non-semantic, alphanumeric identifier based on a substance’s molecular structure and/or descriptive information. | see Unique Ingredient Identifiers (http://fdasis.nlm.nih.gov/srs/srs.jsp) |
| `products.active_ingredients.name` | string | yes | The names of the active, medicinal ingredients in the drug product. |  |
| `products.active_ingredients.strength` | string |  | The strength of the active, medicinal ingredients in the drug product. |  |
| `products.brand_name` | string[] | yes | Brand or trade name of the drug product. |  |
| `products.dosage_form` | string | yes | The drug’s dosage form. There is no standard, but values may include terms like `tablet` or `solution for injection`. |  |
| `products.marketing_status` | string |  | Indicates how a drug product is sold in the United States. | `1`: Prescription; `2`: Discontinued; `3`: None (Tentative Approval); `4`: Over-the-counter |
| `products.product_number` | string |  | A product number is assigned to each drug product associated with an NDA (New Drug Application), ANDA (Abbreviated New Drug Application) and Biologic License Application (BLA) . If a drug product is available in multiple strengths, there a… |  |
| `products.reference_drug` | string |  | Indicates whether the drug product is a reference drug. |  |
| `products.reference_standard` | string |  | Indicates whether the drug product is a reference standard. |  |
| `products.route` | string | yes | The route of administation of the drug product. |  |
| `products.te_code` | string |  | The coding system for therapeutic equivalence evaluations allows users to determine whether FDA has evaluated a particular approved product as therapeutically equivalent to other pharmaceutically equivalent products (first letter) and to p… |  |
| `sponsor_name` | string | yes | The company that submitted an application to FDA for approval to market the drug product in the United States. |  |
| `submissions.application_docs.date` | date |  | The date of publication of the applications document. |  |
| `submissions.application_docs.id` | date |  | The id of the applications document. |  |
| `submissions.application_docs.title` | string |  | The title of the applications document. |  |
| `submissions.application_docs.type` | date |  | The type of the applications document. |  |
| `submissions.application_docs.url` | string |  | The url to access the applications document. |  |
| `submissions.review_priority` | string |  | Pending. |  |
| `submissions.submission_class_code` | string |  | The Submission Classification Code, previously known as the Chemistry Classification Code, is assigned as a “Type” code. |  |
| `submissions.submission_class_code_description` | string |  | The Submission Classification Code, previously known as the Chemistry Classification Code, is assigned as a “Type” code. This is a full description of the classification code. |  |
| `submissions.submission_number` | string |  | A unique identifier for each submission under that application. |  |
| `submissions.submission_property_type.code` | string |  | The code indicating the submission property type. |  |
| `submissions.submission_public_notes` | string |  | Publicly available notes regarding the submission. |  |
| `submissions.submission_status` | string |  | The current status of this submission. |  |
| `submissions.submission_status_date` | date |  | The date the status was applied to the submission. |  |
| `submissions.submission_type` | string |  | The type of the individual submission. Used in combination with submission_number. |  |

## Usage tips

- Pick the field by question:
  - Application: `application_number` (prefix `NDA`, `ANDA` or `BLA`), `sponsor_name`.
  - Products: `products.brand_name`, `products.active_ingredients.name`, `products.dosage_form`, `products.route`, `products.marketing_status` (`Prescription`, `Over-the-counter`, `Discontinued`, `None (Tentative Approval)`), `products.te_code`.
  - History: `submissions.submission_type` (`ORIG` original, `SUPPL` supplement), `submissions.submission_status` (`AP` approved, `TA` tentative approval), `submissions.submission_status_date`, `submissions.application_docs.url` (letters, labels, reviews).
- Count `sponsor_name` and `submissions.submission_type` without `.exact`: although the field definitions mark `sponsor_name` as exact, `.exact` returns "Nothing to count".
- `submissions` is a list, so `submissions.submission_type:"ORIG" AND submissions.submission_status_date:[...]` can match the two terms in different submissions of one application. Check the returned submissions when the pairing matters.
- `.exact` is case-sensitive and matches the whole value. In drug/label, `openfda.brand_name.exact:"Tylenol"` returns no matches, while plain `openfda.brand_name:"tylenol"` returns 112 labels.
- A misspelled field name returns "No matches found!", the same as a search with no hits. fda_get_dataset adds a hint when a field is not in the table above.
- Counting a date field returns every date in the result, whatever the `limit`. Narrow the search to a date range first.
- Pass `fields` to fda_get_dataset to return only the paths you need, e.g. `fields=["openfda.brand_name", "boxed_warning"]`.
