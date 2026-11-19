---
name: fda-food-adverse-events
description: Query openFDA food adverse event reports (CAERS, api.fda.gov/food/event). Use it for reactions and outcomes reported for foods, dietary supplements and cosmetics, by product, industry, consumer age and gender, and report date.
---

# openFDA: Food, dietary supplement and cosmetic adverse events (CAERS)

## Overview

- API: `https://api.fda.gov` (openFDA, Elasticsearch-based REST API). Docs: https://open.fda.gov/apis/food/event/. Field definitions: https://open.fda.gov/fields/foodevent.yaml.
- Snapshot taken 2026-11-19: 151,589 records; data last updated 2026-07-07 (`meta.last_updated`); bulk export date 2026-11-18 (download.json).
- Surface: read-only `GET`, JSON only. One endpoint; no per-record ids to look up.
- Auth: optional API key (env `OPENFDA_API_KEY`, sent as the Basic-auth username). Without a key: 240 requests/minute and 1,000/day per IP; with a key: 120,000/day. `count` with `limit=1000` needs a key.
- Disclaimer: openFDA asks users not to base medical care decisions on it and to treat all results as unvalidated; FDA may limit API access under its terms. Terms: https://open.fda.gov/terms/. License: https://open.fda.gov/license/.
- Sample record: one `limit=1` record was fetched to list the fields it returns; values were not stored.
- Freshness: `meta.last_updated` is older than the drug endpoints (see the snapshot line). Reports go back to 1999 (`date_created`).

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
| `food/event` | Food, dietary supplement and cosmetic adverse events (CAERS) | food | 151,589 | 12 | 2026-07-07 |

## Endpoint

### food/event

**Food, dietary supplement and cosmetic adverse events (CAERS)**

- Endpoint: `GET https://api.fda.gov/food/event.json`
- Records: 151,589. Last updated: 2026-07-07. Probe status: 200.
- Sample record fields (limit=1): `report_number`, `outcomes`, `date_created`, `reactions`, `date_started`, `consumer.age`, `consumer.age_unit`, `consumer.gender`, `products.role`, `products.name_brand`, `products.industry_code`, `products.industry_name`
- Example queries (run on 2026-11-19):

  ```
  # Reports by product industry (200, 5 terms)
  GET https://api.fda.gov/food/event.json?count=products.industry_name.exact&limit=5
  # Top reactions reported for cosmetics (200, 5 terms)
  GET https://api.fda.gov/food/event.json?search=products.industry_name:"Cosmetics"&count=reactions.exact&limit=5
  # Reports by outcome (200, 13 terms)
  GET https://api.fda.gov/food/event.json?count=outcomes.exact
  # Reports created in 2025 (200, 6,308 records)
  GET https://api.fda.gov/food/event.json?search=date_created:[20250101+TO+20251231]&limit=1
  ```

| Field | Type | Exact | Description | Possible values |
|---|---|---|---|---|
| `consumer.age` | string |  | The reported age of the consumer at the time of the adverse event report, expressed in the unit in the field `age_unit`. |  |
| `consumer.age_unit` | string |  | Encodes the unit in which the age of the consumer is expressed. | `Day(s)`: age is expressed in days; `Week(s)`: age is expressed in weeks; `Month(s)`: age is expressed in months; `Year(s)`: age is expressed in years; `Decade(s)`: age is expressed in decades; `Not Available`: Unknown |
| `consumer.gender` | string |  | The reported gender of the consumer. | `Female`: Female; `Male`: Male; `Not Available`: Unknown |
| `date_created` | date |  | Date the report was received by FDA. |  |
| `date_started` | date |  | Date of the adverse event (when it was considered to have started). |  |
| `outcomes` | string[] | yes | The outcome or consequence of the adverse event. | `NON-SERIOUS INJURIES/ ILLNESS`: The outcome wasn’t serious; `OTHER SERIOUS (IMPORTANT MEDICAL EVENTS)`: The outcome included non-specified serious medical events; `VISITED A HEALTH CARE PROVIDER`: The adverse event was serious enough to c… |
| `products.industry_code` | string |  | The FDA industry code for the product. Results in this endpoint are generally limited to products tagged with industry codes related to human food and nutritional supplements or cosmetics. | `2`: Whole Grain/Milled Grain Prod/Starch; `3`: Bakery Prod/Dough/Mix/Icing; `4`: Macaroni/Noodle Prod; `5`: Cereal Prep/Breakfast Food; `7`: Snack Food Item; `9`: Milk/Butter/Dried Milk Prod; `12`: Cheese/Cheese Prod; `13`: Ice Cream Prod… |
| `products.industry_name` | string | yes | The FDA industry name associated with the product. |  |
| `products.name_brand` | string | yes | The reported brand name of the product. |  |
| `products.role` | string | yes | The reported role of the product in the adverse event report. | `Suspect`: The product was suspected of causing the adverse event; `Concomitant`: The product was not suspected of causing the adverse event, but was being consumed or used at the same time when the adverse event started; `Not Available`:… |
| `reactions` | string[] | yes | MedDRA terms for the reactions. Note that these terms are encoded in British English. For instance, *diarrhea* is recorded as `DIARRHOEA` | see MedDRA (http://www.meddra.org/) |
| `report_number` | string |  | The report number. |  |

## Usage tips

- Pick the field by question:
  - Product: `products.name_brand`, `products.industry_name` (e.g. `Cosmetics`, `Vit/Min/Prot/Unconv Diet(Human/Animal)` for dietary supplements), `products.role` (`SUSPECT` or `CONCOMITANT`).
  - Effect: `reactions` (MedDRA terms), `outcomes` (`Hospitalization`, `Death`, `Visited Emergency Room`, ...).
  - Consumer: `consumer.age` with `consumer.age_unit`, `consumer.gender`.
- Cosmetics are included: they are the second-largest industry (52,219 reports), after dietary supplements (54,906).
- `reactions.exact` has case variants of the same term (`Ovarian cancer` / `OVARIAN CANCER`, `Diarrhoea` / `DIARRHOEA`); add up the variants when ranking reactions.
- `products.name_brand` is often `EXEMPTION 4` (39,396 reports): the brand was withheld under FOIA exemption 4 (confidential business information).
- `.exact` is case-sensitive and matches the whole value. In drug/label, `openfda.brand_name.exact:"Tylenol"` returns no matches, while plain `openfda.brand_name:"tylenol"` returns 112 labels.
- A misspelled field name returns "No matches found!", the same as a search with no hits. fda_get_dataset adds a hint when a field is not in the table above.
- Counting a date field returns every date in the result, whatever the `limit`. Narrow the search to a date range first.
- Pass `fields` to fda_get_dataset to return only the paths you need, e.g. `fields=["openfda.brand_name", "boxed_warning"]`.
