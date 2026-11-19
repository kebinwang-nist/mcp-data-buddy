---
name: cdc-respiratory-viruses
description: Query CDC open data (data.cdc.gov, Socrata SODA API) for the Coronavirus and Other Respiratory Viruses category. Use it for daily emergency department visit shares for COVID-19, influenza, RSV and acute respiratory illness by state (NSSP), imputed weekly RSV hospitalization counts by state for 2018-2024, and a SARS-CoV-2 serology test comparison panel.
---

# CDC open data: Coronavirus and Other Respiratory Viruses

## Overview

- Portal: `https://data.cdc.gov` (Socrata). Category browse page: `https://data.cdc.gov/browse?category=Coronavirus+and+Other+Respiratory+Viruses`.
- Catalog snapshot taken 2026-11-09: 3 public assets in the category: 3 datasets, 0 filtered views, 0 maps, 0 charts.
- Excluded (not public or no API endpoint): none.
- Common tags (number of assets): `nssp` (2), `antibodies` (1), `covid-19` (1), `hospitalization` (1), `hospitalization rate` (1), `hospitalizations` (1), `immunoassays` (1), `ncird-corvd` (1), `neutralization assay` (1), `rate` (1), `respiratory` (1), `respiratory disease` (1), `respiratory illness` (1), `respiratory syncytial virus` (1), `rsv` (1), `rsvnet` (1), `sars-cov-2` (1), `serological tests` (1), `surveillance` (1).
- Surface: read-only `GET`. Each dataset and filtered view has its own data endpoint keyed by a 4x4 id (e.g. `hhvg-83jq`). Maps and charts have no data endpoint of their own; query their parent dataset instead.
- Auth: none for reads. An optional Socrata app token in header `X-App-Token` raises the throttling limit; without one, heavy use from one IP may get HTTP 429. No key for this API exists in this project.
- Types: Socrata column types are `text`, `number`, `calendar_date` (floating timestamp, returned as `2024-10-04T00:00:00.000`), `point` (GeoJSON `{"type":"Point","coordinates":[lon,lat]}`), `url` (`{"url": ...}`), `checkbox` (boolean). In JSON output, numbers come back as strings. Null fields are omitted from a row object rather than returned as `null`.
- Topics and tags: each section's `Topics` and `Tags` lines come from the dataset's intro page (`/d/{id}`, "About this Dataset"), read from `/api/views/{id}.json`. `Sample row fields` lists the field names one `$limit=1` row returned; values were not stored.
- Freshness: `vjzj-u7u8` (NSSP emergency department visits) is updated daily from September 2022. `whhs-7a5d` (imputed RSV hospitalizations) covers 2018-2024 and is no longer updated, and `hhvg-83jq` is a one-off 2023 study.

## Endpoints per asset

Replace `{id}` with the asset id from the index.

| Purpose | Endpoint |
|---|---|
| Rows as JSON (SODA 2.1, SoQL params) | `GET https://data.cdc.gov/resource/{id}.json` |
| Rows as CSV / GeoJSON | `GET https://data.cdc.gov/resource/{id}.csv`, `.geojson` |
| Column + view metadata | `GET https://data.cdc.gov/api/views/{id}.json` |
| Full export (no row limit) | `GET https://data.cdc.gov/api/views/{id}/rows.csv?accessType=DOWNLOAD` |
| Human page | `https://data.cdc.gov/d/{id}` |
| Catalog search (this category) | `GET https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&categories=Coronavirus%20and%20Other%20Respiratory%20Viruses&limit=100` |

## Query parameters (SoQL)

All optional, passed on `/resource/{id}.json`. URL-encode values (spaces as `%20`, `'` as `%27`).

| Param | Meaning | Example |
|---|---|---|
| `$select` | Columns or expressions | `$select=col_a,col_b` / `$select=count(*) as n` |
| `$where` | Filter (SoQL condition) | `$where=upper(col_a)='X' AND date_col >= '2026-10-01'` |
| `$order` | Sort, `ASC`/`DESC` allowed | `$order=date_col DESC` |
| `$group` | Group by (with aggregates in `$select`) | `$select=col_a,count(*)&$group=col_a` |
| `$having` | Filter on aggregates | `$having=count(*) > 10` |
| `$limit` | Max rows; **default 1000** | `$limit=50000` |
| `$offset` | Rows to skip, for paging (use with a stable `$order`) | `$offset=1000` |
| `$q` | Full-text search across text columns | `$q=influenza` |
| `<field>=<value>` | Simple equality filter | `col_a=X` |

SoQL notes:

- String literals use single quotes, and comparison is case-sensitive. Casing is often inconsistent within a column, so match text with `upper(col) = 'X'` or `upper(col) like '%X%'`, and group by `upper(col)`.
- Dates: compare `calendar_date` columns with ISO literals, e.g. `date_col between '2026-10-01' and '2026-10-31T23:59:59'`. Compute relative dates ("last 7 days") yourself and pass literals.
- Count rows with `$select=count(*)`. Aggregates: `count`, `sum`, `avg`, `min`, `max`; `date_trunc_ym(col)` for month buckets.
- Errors: HTTP 400 with `{"errorCode": "query.soql.no-such-column", ...}` for a bad field name; use the field names (not display names) from the column tables below.
- Geo: `within_circle(location, lat, lon, meters)` works on `point` columns.

## Endpoint index

Queryable assets (datasets and filtered views). Rows were counted and each endpoint was called with `$limit=1` on 2026-11-09.

| # | Id | Name | Type | Parent | Rows | Cols | Data updated | Update frequency | Status |
|---|---|---|---|---|---|---|---|---|---|
| 1 | [`hhvg-83jq`](#hhvg-83jq) | Examination of SARS-CoV-2 serological test results from multiple commercial and laboratory platforms with an in-house serum panel | dataset |  | 204 | 14 | 2023-12-13 |  | 200 |
| 2 | [`whhs-7a5d`](#whhs-7a5d) | Imputed Hospitalization Rate for RSV at the State Level | dataset |  | 14,258 | 6 | 2026-05-13 | Not updated | 200 |
| 3 | [`vjzj-u7u8`](#vjzj-u7u8) | NSSP Emergency Department Respiratory Daily | dataset |  | 311,584 | 4 | 2026-11-09 |  | 200 |

## Datasets and filtered views

### hhvg-83jq

**Examination of SARS-CoV-2 serological test results from multiple commercial and laboratory platforms with an in-house serum panel** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/hhvg-83jq.json`
- Metadata: `GET https://data.cdc.gov/api/views/hhvg-83jq.json`; page: https://data.cdc.gov/d/hhvg-83jq
- Topics: Category: Coronavirus and Other Respiratory Viruses
- Tags: `sars-cov-2`, `covid-19`, `serological tests`, `immunoassays`, `antibodies`, `neutralization assay`, `ncird-corvd`
- Rows: 204. Data updated: 2023-12-13. Probe status: 200.
- Source: Coronavirus and Other Respiratory Viruses Laboratory Branch (CRVLB), Coronavirus and Other Respiratory Viruses Division (CORVD), National Center for Immunization and Respiratory Diseases (NCIRD).
- Description: Severe acute respiratory syndrome (SARS) coronavirus 2 (SARS-CoV-2) is a novel human coronavirus that was identified in 2019. SARS-CoV-2 infection results in an acute, severe respiratory disease called coronavirus disease 2019 (COVID-19). The emergence and rapid spread of SARS-CoV-2 has led to a global public health crisis, which continues to affect populations across the globe. Real time reverse transcription polymerase chain reaction (rRT-PCR) is the reference standard test for COVID-19 diagnosis. Serological tests are valuable tools for serosurveillance programs and establishing correlates…
- Sample row fields ($limit=1): `sample`, `pcr_confirmed`, `abbott_reactivity`, `ortho_reactivity`, `elisa_full_spike_reactivity`, `abbott_s_c_values`, `abbott_s_c_values_log10`, `ortho_index_values`, `ortho_index_values_log10`, `elisa_s_t_values`, `elisa_s_t_values_log10`, `mnt_titer`, `mnt_titer_log10`, `svnt_inhibition`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `sample` | Sample # | number | Sample Number |
| `pcr_confirmed` | PCR confirmed | text | Laboratory confirmed negative or positive for SARS-CoV-2 by rRT-PCR result |
| `abbott_reactivity` | Abbott Reactivity | text | Reactive or Nonreactive for SARS-CoV-2 result |
| `ortho_reactivity` | Ortho Reactivity | text | Reactive or Nonreactive for SARS-CoV-2 result |
| `elisa_full_spike_reactivity` | In-House CDC ELISA Reactivity | text | Reactive or Nonreactive for SARS-CoV-2 result |
| `abbott_s_c_values` | Abbott S/C Values | number | Numeric Index (S/C) value of SARS-CoV-2 reactivity |
| `abbott_s_c_values_log10` | Abbott S/C Values (Log10) | number | Numeric Index (S/C) value of SARS-CoV-2 reactivity log10 scale |
| `ortho_index_values` | Ortho Index Values | number | Numeric Index value of SARS-CoV-2 reactivity |
| `ortho_index_values_log10` | Ortho Index Values (Log10) | number | Numeric Index value of SARS-CoV-2 reactivity log10 scale |
| `elisa_s_t_values` | In-House CDC ELISA S/T Values | number | Numeric signal to threshold (S/T) value of SARS-CoV-2 reactivity |
| `elisa_s_t_values_log10` | In-House CDC ELISA S/T Values (Log10) | number | Numeric signal to threshold (S/T) value of SARS-CoV-2 reactivity log10 scale |
| `mnt_titer` | mNT TITER | number | Numeric value of neutralzing antibodies against SARS-CoV-2 |
| `mnt_titer_log10` | mNT TITER (Log10) | number | Numeric value of neutralzing antibodies against SARS-CoV-2 log10 scale |
| `svnt_inhibition` | sVNT % Inhibition | number | Percent inhibition rate of neutralizing antibodies against SARS-CoV-2 RBD |

### whhs-7a5d

**Imputed Hospitalization Rate for RSV at the State Level** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/whhs-7a5d.json`
- Metadata: `GET https://data.cdc.gov/api/views/whhs-7a5d.json`; page: https://data.cdc.gov/d/whhs-7a5d
- Topics: Category: Coronavirus and Other Respiratory Viruses
- Tags: `rsv`, `rsvnet`, `nssp`, `hospitalization rate`, `surveillance`, `respiratory disease`, `respiratory syncytial virus`, `respiratory illness`, `hospitalizations`, `hospitalization`, `rate`
- Rows: 14,258. Data updated: 2026-05-13. Probe status: 200.
- Update frequency: Not updated.
- Source: NCIRD/CORVD
- Description: Weekly imputed RSV hospital admission rates per 100,000 population from 47 states plus DC from 2018-2024 are described. Rates were estimated by combining values from RSV-Net with those from NSSP and NHSN to obtain combined time series of RSV hospital admissions counts. States with overlapping values in both sets underwent interpolation and extrapolation procedures for estimates throughout the time series. These states were then used to impute values for states that did not have surveillance data within RSV-Net. Calculated RSV hospital admission rates (either interpolated, extrapolated, or imp…
- Sample row fields ($limit=1): `state`, `week`, `state_abb`, `nssp`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `state` | State | text | State name |
| `week` | Epi Week Start Date | calendar_date | Date for start of the MMWR epidemiological week (Sunday) |
| `state_abb` | State Abbreviation | text | State 2-letter abbreviation |
| `nssp` | NSSP RSV Count | number | Estimated counts of RSV hospital admissions based on NSSP's % ED visits due to RSV and COVID and NHSN's counts of COVID hospital admissions |
| `rsvnet` | RSVNet RSV Count | number | Estimated counts of RSV hospital admissions based on RSV-Net rates per 100k people and state populations |
| `interpolated_extrapolated` | Calculated Counts | number | Value of RSV hospital admission counts obtained from interpolation, extrapolation, or imputation methods using other count totals |

### vjzj-u7u8

**NSSP Emergency Department Respiratory Daily** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/vjzj-u7u8.json`
- Metadata: `GET https://data.cdc.gov/api/views/vjzj-u7u8.json`; page: https://data.cdc.gov/d/vjzj-u7u8
- Topics: Category: Coronavirus and Other Respiratory Viruses
- Tags: `nssp`, `respiratory`
- Rows: 311,584. Data updated: 2026-11-09. Probe status: 200.
- Description: NSSP Emergency Department Respiratory Daily. This dataset provides the percentage of emergency department patient visits for the specified pathogen of all ED patient visits for the specified geographic part of the country that were observed for the given day from data submitted to the National Syndromic Surveillance Program (NSSP). For additional information, please see: Companion Guide: NSSP Emergency Department Data on Respiratory Illness While the data are stratified by day, updated data are available once per week each Wednesday.
- Sample row fields ($limit=1): `date`, `pathogen`, `geography`, `percent_visits`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | date | calendar_date |  |
| `pathogen` | pathogen | text |  |
| `geography` | geography | text |  |
| `percent_visits` | percent_visits | number |  |

## Usage tips

- Pick the dataset by question:
  - Percent of ED visits for a pathogen by day and place: `vjzj-u7u8`. `pathogen` is `ARI`, `COVID`, `Influenza` or `RSV`; `geography` is a state name, `District of Columbia` or `United States`.
  - Weekly RSV hospital admission counts by state (47 states plus DC, 2018-2024): `whhs-7a5d`, with `nssp`, `rsvnet` and `interpolated_extrapolated` estimates side by side.
  - SARS-CoV-2 antibody test results of a serum panel (Abbott, Ortho, in-house ELISA, neutralization): `hhvg-83jq`.
- Examples:

  ```
  # Maryland COVID share of ED visits, last 14 days (compute the date)
  GET https://data.cdc.gov/resource/vjzj-u7u8.json?$where=geography='Maryland' AND pathogen='COVID' AND date >= '2026-10-26'&$order=date
  # National share by pathogen on the latest day
  GET https://data.cdc.gov/resource/vjzj-u7u8.json?$where=geography='United States'&$order=date DESC&$limit=4
  ```
