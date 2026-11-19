---
name: fda-drug-ndc
description: Query the openFDA National Drug Code directory (api.fda.gov/drug/ndc). Use it to look up drug products and packages by NDC, brand or generic name, labeler, dosage form, route, active ingredients and strengths, and marketing category and dates.
---

# openFDA: National Drug Code directory (NDC)

## Overview

- API: `https://api.fda.gov` (openFDA, Elasticsearch-based REST API). Docs: https://open.fda.gov/apis/drug/ndc/. Field definitions: https://open.fda.gov/fields/drugndc.yaml.
- Snapshot taken 2026-11-19: 138,538 records; data last updated 2026-11-18 (`meta.last_updated`); bulk export date 2026-11-19 (download.json).
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
| `drug/ndc` | National Drug Code directory (NDC) | drug | 138,538 | 36 | 2026-11-18 |

## Endpoint

### drug/ndc

**National Drug Code directory (NDC)**

- Endpoint: `GET https://api.fda.gov/drug/ndc.json`
- Records: 138,538. Last updated: 2026-11-18. Probe status: 200.
- Sample record fields (limit=1): `product_ndc`, `generic_name`, `labeler_name`, `brand_name`, `active_ingredients.name`, `active_ingredients.strength`, `finished`, `packaging.package_ndc`, `packaging.description`, `packaging.marketing_start_date`, `packaging.sample`, `listing_expiration_date`, `openfda.manufacturer_name`, `openfda.rxcui`, `openfda.spl_set_id`, `openfda.is_original_packager`, `openfda.unii`, `marketing_category`, `dosage_form`, `spl_id`, `product_type`, `route`, `marketing_start_date`, `product_id`, `application_number`, `brand_name_base`, `pharm_class`
- Also returned by the API (not in the field definitions): `labeler_name`
- Example queries (run on 2026-11-19):

  ```
  # Products named Advil (200, 66 records)
  GET https://api.fda.gov/drug/ndc.json?search=brand_name:"Advil"&limit=1
  # Dosage forms of metformin products (200, 5 terms)
  GET https://api.fda.gov/drug/ndc.json?search=generic_name:"metformin"&count=dosage_form.exact&limit=5
  # Manufacturers with the most products first marketed in 2025 (200, 5 terms)
  GET https://api.fda.gov/drug/ndc.json?search=marketing_start_date:[20250101+TO+20251231]&count=openfda.manufacturer_name.exact&limit=5
  ```

| Field | Type | Exact | Description | Possible values |
|---|---|---|---|---|
| `active_ingredients.name` | string | yes | The names of the active, medicinal ingredients in the drug product. |  |
| `active_ingredients.strength` | string |  | The strength of the active, medicinal ingredients in the drug product. |  |
| `application_number` | string |  | This corresponds to the NDA, ANDA, or BLA number reported by the labeler for products which have the corresponding Marketing Category designated. If the designated Marketing Category is OTC Monograph Final or OTC Monograph Not Final, then… |  |
| `brand_name` | string | yes | Brand or trade name of the drug product. |  |
| `brand_name_base` | string | yes | The base of the brand name excluding its suffix. |  |
| `brand_name_suffix` | string | yes | A suffix to the proprietary name, a value here should be appended to the ProprietaryName field to obtain the complete name of the product. This suffix is often used to distinguish characteristics of a product such as extended release (“XR”… |  |
| `dea_schedule` | string |  | This is the assigned DEA Schedule number as reported by the labeler. Values are CI, CII, CIII, CIV, and CV. | `1`: CI; `2`: CII; `3`: CIII; `4`: CIV; `5`: CV |
| `dosage_form` | string | yes | The drug’s dosage form. There is no standard, but values may include terms like `tablet` or `solution for injection`. |  |
| `finished` | string |  | Details whether the product is finished or not. FDA does not review and approve unfinished products. Therefore, all products in this file are considered unapproved. |  |
| `generic_name` | string | yes | Generic name(s) of the drug product. |  |
| `listing_expiration_date` | date |  | This is the date when the listing record will expire if not updated or certified by the firm. |  |
| `marketing_category` | string |  | Product types are broken down into several potential Marketing Categories, such as NDA/ANDA/BLA, OTC Monograph, or Unapproved Drug. |  |
| `marketing_end_date` | date |  | This is the date the product will no longer be available on the market. |  |
| `marketing_start_date` | date |  | This is the date that the labeler indicates was the start of its marketing of the drug product. |  |
| `openfda.is_original_packager` | string | yes | Whether or not the drug has been repackaged for distribution. |  |
| `openfda.manufacturer_name` | string | yes | Name of manufacturer or company that makes this drug product, corresponding to the labeler code segment of the NDC. |  |
| `openfda.nui` | string | yes | Unique identifier applied to a drug concept within the National Drug File Reference Terminology (NDF-RT). |  |
| `openfda.pharm_class_cs` | string | yes | Chemical structure classification of the drug product’s pharmacologic class. Takes the form of the classification, followed by `[Chemical/Ingredient]` (such as `Thiazides [Chemical/Ingredient]` or `Antibodies, Monoclonal [Chemical/Ingredie… |  |
| `openfda.pharm_class_epc` | string | yes | Established pharmacologic class associated with an approved indication of an active moiety (generic drug) that the FDA has determined to be scientifically valid and clinically meaningful. Takes the form of the pharmacologic class, followed… |  |
| `openfda.pharm_class_moa` | string | yes | Mechanism of action of the drug—molecular, subcellular, or cellular functional activity—of the drug’s established pharmacologic class. Takes the form of the mechanism of action, followed by `[MoA]` (such as `Calcium Channel Antagonists [Mo… |  |
| `openfda.pharm_class_pe` | string | yes | Physiologic effect or pharmacodynamic effect—tissue, organ, or organ system level functional activity—of the drug’s established pharmacologic class. Takes the form of the effect, followed by `[PE]` (such as `Increased Diuresis [PE]` or `De… |  |
| `openfda.rxcui` | string | yes | The RxNorm Concept Unique Identifier. RxCUI is a unique number that describes a semantic concept about the drug product, including its ingredients, strength, and dose forms. |  |
| `openfda.spl_set_id` | string | yes | Unique identifier for the Structured Product Label for a product, which is stable across versions of the label. Also referred to as the set ID. |  |
| `openfda.unii` | string | yes | Unique Ingredient Identifier, which is a non-proprietary, free, unique, unambiguous, non-semantic, alphanumeric identifier based on a substance’s molecular structure and/or descriptive information. |  |
| `openfda.upc` | string | yes | Universal Product Code |  |
| `packaging.description` | string | yes | A description of the size and type of packaging in sentence form. Multilevel packages will have the descriptions concatenated together. |  |
| `packaging.marketing_end_date` | date |  | This is the date the product will no longer be available on the market. |  |
| `packaging.marketing_start_date` | date |  | This is the date that the labeler indicates was the start of its marketing of the drug product. |  |
| `packaging.package_ndc` | string |  | This number, known as the NDC, identifies the labeler, product, and trade package size. The first segment, the labeler code, is assigned by the FDA. A labeler is any firm that manufactures (including repackers or relabelers), or distribute… |  |
| `packaging.sample` | string |  | Indicates whether this is a sample packaging or not. |  |
| `pharm_class` | string | yes | These are the reported pharmacological class categories corresponding to the SubstanceNames listed above. |  |
| `product_id` | string |  | ProductID is a concatenation of the NDC product code and SPL documentID. |  |
| `product_ndc` | string |  | The labeler manufacturer code and product code segments of the NDC number, separated by a hyphen. |  |
| `product_type` | string | yes | Type of drug product |  |
| `route` | string | yes | The route of administation of the drug product. |  |
| `spl_id` | string |  | Unique identifier for a particular version of a Structured Product Label for a product. Also referred to as the document ID. |  |

## Usage tips

- Pick the field by question:
  - Look up a product: `product_ndc` (labeler-product, e.g. `0573-0133` for an Advil product), `brand_name`, `generic_name`, `labeler_name` (returned by the API but not in the field definitions; `labeler_name.exact` counts work).
  - Packages: `packaging.package_ndc`, `packaging.description`.
  - Ingredients and form: `active_ingredients.name`, `active_ingredients.strength`, `dosage_form`, `route`.
  - Regulatory: `marketing_category` (`ANDA`, `OTC MONOGRAPH DRUG`, `NDA`, `BLA`, `UNAPPROVED HOMEOPATHIC`, ...), `product_type` (`HUMAN PRESCRIPTION DRUG`, `HUMAN OTC DRUG`, ...), `dea_schedule`, `marketing_start_date`.
- Count `marketing_category` without `.exact` (`.exact` returns "Nothing to count"); `product_type.exact` and `dosage_form.exact` work.
- `marketing_start_date` sorted ascending starts at `19000101`, so ignore implausibly old dates.
- `.exact` is case-sensitive and matches the whole value. In drug/label, `openfda.brand_name.exact:"Tylenol"` returns no matches, while plain `openfda.brand_name:"tylenol"` returns 112 labels.
- A misspelled field name returns "No matches found!", the same as a search with no hits. fda_get_dataset adds a hint when a field is not in the table above.
- Counting a date field returns every date in the result, whatever the `limit`. Narrow the search to a date range first.
- Pass `fields` to fda_get_dataset to return only the paths you need, e.g. `fields=["openfda.brand_name", "boxed_warning"]`.
