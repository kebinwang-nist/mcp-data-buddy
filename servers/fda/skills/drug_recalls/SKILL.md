---
name: fda-drug-recalls
description: Query openFDA drug recall enforcement reports (api.fda.gov/drug/enforcement). Use it for drug recalls since 2012 by recalling firm, product, reason, classification (Class I, II or III), status, distribution and report date.
---

# openFDA: Drug recalls (enforcement reports)

## Overview

- API: `https://api.fda.gov` (openFDA, Elasticsearch-based REST API). Docs: https://open.fda.gov/apis/drug/enforcement/. Field definitions: https://open.fda.gov/fields/drugenforcement.yaml.
- Snapshot taken 2026-11-19: 18,166 records; data last updated 2026-11-11 (`meta.last_updated`); bulk export date 2026-11-19 (download.json).
- Surface: read-only `GET`, JSON only. One endpoint; no per-record ids to look up.
- Auth: optional API key (env `OPENFDA_API_KEY`, sent as the Basic-auth username). Without a key: 240 requests/minute and 1,000/day per IP; with a key: 120,000/day. `count` with `limit=1000` needs a key.
- Disclaimer: openFDA asks users not to base medical care decisions on it and to treat all results as unvalidated; FDA may limit API access under its terms. Terms: https://open.fda.gov/terms/. License: https://open.fda.gov/license/.
- Sample record: one `limit=1` record was fetched to list the fields it returns; values were not stored.
- Coverage: `report_date` starts on 2012-06-20. Records name the recalling firm with its address, and some carry contact phone numbers or emails in text fields.

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
| `drug/enforcement` | Drug recalls (enforcement reports) | drug | 18,166 | 45 | 2026-11-11 |

## Endpoint

### drug/enforcement

**Drug recalls (enforcement reports)**

- Endpoint: `GET https://api.fda.gov/drug/enforcement.json`
- Records: 18,166. Last updated: 2026-11-11. Probe status: 200.
- Sample record fields (limit=1): `status`, `city`, `state`, `country`, `classification`, `openfda`, `product_type`, `event_id`, `recalling_firm`, `address_1`, `address_2`, `postal_code`, `voluntary_mandated`, `initial_firm_notification`, `distribution_pattern`, `recall_number`, `product_description`, `product_quantity`, `reason_for_recall`, `recall_initiation_date`, `center_classification_date`, `termination_date`, `report_date`, `code_info`
- Also returned by the API (not in the field definitions): `postal_code`
- Example queries (run on 2026-11-19):

  ```
  # Class I drug recalls reported in 2025 (200, 49 records)
  GET https://api.fda.gov/drug/enforcement.json?search=classification:"Class+I"+AND+report_date:[20250101+TO+20251231]&limit=1
  # Firms with the most nitrosamine recalls (200, 5 terms)
  GET https://api.fda.gov/drug/enforcement.json?search=reason_for_recall:"nitrosamine"&count=recalling_firm.exact&limit=5
  # Recall reports per report date (200, 744 terms)
  GET https://api.fda.gov/drug/enforcement.json?count=report_date&limit=5
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
| `openfda.application_number` | string[] | yes | This corresponds to the NDA, ANDA, or BLA number reported by the labeler for products which have the corresponding Marketing Category designated. If the designated Marketing Category is OTC Monograph Final or OTC Monograph Not Final, then… |  |
| `openfda.brand_name` | string[] | yes | Brand or trade name of the drug product. |  |
| `openfda.generic_name` | string[] | yes | Generic name(s) of the drug product. |  |
| `openfda.is_original_packager` | string | yes | Whether or not the drug has been repackaged for distribution. |  |
| `openfda.manufacturer_name` | string[] | yes | Name of manufacturer or company that makes this drug product, corresponding to the labeler code segment of the NDC. |  |
| `openfda.nui` | string[] | yes | Unique identifier applied to a drug concept within the National Drug File Reference Terminology (NDF-RT). | see NDF-RT (https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NDFRT/) |
| `openfda.original_packager_product_ndc` | string[] | yes | This ndc identifies the original packager. |  |
| `openfda.package_ndc` | string[] | yes | This number, known as the NDC, identifies the labeler, product, and trade package size. The first segment, the labeler code, is assigned by the FDA. A labeler is any firm that manufactures (including repackers or relabelers), or distribute… |  |
| `openfda.pharm_class_cs` | string[] | yes | Chemical structure classification of the drug product’s pharmacologic class. Takes the form of the classification, followed by `[Chemical/Ingredient]` (such as `Thiazides [Chemical/Ingredient]` or `Antibodies, Monoclonal [Chemical/Ingredie… |  |
| `openfda.pharm_class_epc` | string[] | yes | Established pharmacologic class associated with an approved indication of an active moiety (generic drug) that the FDA has determined to be scientifically valid and clinically meaningful. Takes the form of the pharmacologic class, followed… |  |
| `openfda.pharm_class_moa` | string[] | yes | Mechanism of action of the drug—molecular, subcellular, or cellular functional activity—of the drug’s established pharmacologic class. Takes the form of the mechanism of action, followed by `[MoA]` (such as `Calcium Channel Antagonists [Mo… |  |
| `openfda.pharm_class_pe` | string[] | yes | Physiologic effect or pharmacodynamic effect—tissue, organ, or organ system level functional activity—of the drug’s established pharmacologic class. Takes the form of the effect, followed by `[PE]` (such as `Increased Diuresis [PE]` or `De… |  |
| `openfda.product_ndc` | string[] | yes | The labeler manufacturer code and product code segments of the NDC number, separated by a hyphen. |  |
| `openfda.product_type` | string[] | yes |  | see Type of drug product (http://www.fda.gov/ForIndustry/DataStandards/StructuredProductLabeling/ucm162063.htm) |
| `openfda.route` | string[] | yes | The route of administation of the drug product. | see Route of administration (http://www.fda.gov/ForIndustry/DataStandards/StructuredProductLabeling/ucm162034.htm) |
| `openfda.rxcui` | string[] | yes | The RxNorm Concept Unique Identifier. RxCUI is a unique number that describes a semantic concept about the drug product, including its ingredients, strength, and dose forms. | see RxNorm and RxCUI documentation (https://www.nlm.nih.gov/research/umls/rxnorm/docs/2012/rxnorm_doco_full_2012-3.html) |
| `openfda.spl_id` | string[] | yes | Unique identifier for a particular version of a Structured Product Label for a product. Also referred to as the document ID. |  |
| `openfda.spl_set_id` | string[] | yes | Unique identifier for the Structured Product Label for a product, which is stable across versions of the label. Also referred to as the set ID. |  |
| `openfda.substance_name` | string[] | yes | The list of active ingredients of a drug product. |  |
| `openfda.unii` | string[] | yes | Unique Ingredient Identifier, which is a non-proprietary, free, unique, unambiguous, non-semantic, alphanumeric identifier based on a substance’s molecular structure and/or descriptive information. | see Unique Ingredient Identifiers (http://fdasis.nlm.nih.gov/srs/srs.jsp) |
| `openfda.upc` | string[] | yes | Universal Product Code | see Universal Product Code (https://en.wikipedia.org/wiki/Universal_Product_Code) |
| `product_code` | string |  |  |  |
| `product_description` | string |  | Brief description of the product being recalled. |  |
| `product_quantity` | string |  | The amount of defective product subject to recall. |  |
| `product_type` | string | yes | The type of product being recalled. For drug queries, this will always be `Drugs`. | `Drugs`: The recalled product is a drug product.; `Devices`: The recalled product is a device product.; `Food`: The recalled product is a food product. |
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
  - Severity: `classification` is `Class I` (most serious), `Class II` or `Class III`. Search it plainly (`classification:"Class I"`) or exactly (`classification.exact:"Class I"`); `.exact:"class i"` returns no matches.
  - Why: `reason_for_recall` (free text; search words such as `"nitrosamine"`, `"sterility"`).
  - Who and what: `recalling_firm`, `product_description`, `openfda.brand_name` / `generic_name` (present only for some recalls), `distribution_pattern`.
  - Progress: `status` is `Terminated`, `Ongoing` or `Completed` (count `status.exact`); dates `recall_initiation_date`, `report_date`, `termination_date`.
- `reason_for_recall` and `product_description` are text fields: counting them returns HTTP 500 "Text fields are not optimised". Count `recalling_firm.exact` or `classification.exact` instead.
- `count=report_date` returns every report date in the result (744 dates for all records) regardless of `limit`; narrow it with a `report_date:[A TO B]` search.
- `.exact` is case-sensitive and matches the whole value. In drug/label, `openfda.brand_name.exact:"Tylenol"` returns no matches, while plain `openfda.brand_name:"tylenol"` returns 112 labels.
- A misspelled field name returns "No matches found!", the same as a search with no hits. fda_get_dataset adds a hint when a field is not in the table above.
- Counting a date field returns every date in the result, whatever the `limit`. Narrow the search to a date range first.
- Pass `fields` to fda_get_dataset to return only the paths you need, e.g. `fields=["openfda.brand_name", "boxed_warning"]`.
