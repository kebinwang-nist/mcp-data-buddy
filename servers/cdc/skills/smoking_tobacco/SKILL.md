---
name: cdc-smoking-tobacco
description: Query CDC open data (data.cdc.gov, Socrata SODA API) for the Smoking & Tobacco Use category. Use it for adult smoking prevalence by state and year from the Behavioral Risk Factor Surveillance System (BRFSS), 1995-2011 (current smokers, every-day and some-day smokers, former smokers and never smokers).
---

# CDC open data: Smoking & Tobacco Use

## Overview

- Portal: `https://data.cdc.gov` (Socrata). Category browse page: `https://data.cdc.gov/browse?category=Smoking+%26+Tobacco+Use`.
- Catalog snapshot taken 2026-11-09: 3 public assets in the category: 3 datasets, 0 filtered views, 0 maps, 0 charts.
- Excluded (not public or no API endpoint): none.
- Common tags (number of assets): `brfss` (3), `current smokers` (3), `former smoker` (2), `non-smoker` (2), `adults` (1).
- Surface: read-only `GET`. Each dataset and filtered view has its own data endpoint keyed by a 4x4 id (e.g. `j8jk-5ztv`). Maps and charts have no data endpoint of their own; query their parent dataset instead.
- Auth: none for reads. An optional Socrata app token in header `X-App-Token` raises the throttling limit; without one, heavy use from one IP may get HTTP 429. No key for this API exists in this project.
- Types: Socrata column types are `text`, `number`, `calendar_date` (floating timestamp, returned as `2024-10-04T00:00:00.000`), `point` (GeoJSON `{"type":"Point","coordinates":[lon,lat]}`), `url` (`{"url": ...}`), `checkbox` (boolean). In JSON output, numbers come back as strings. Null fields are omitted from a row object rather than returned as `null`.
- Topics and tags: each section's `Topics` and `Tags` lines come from the dataset's intro page (`/d/{id}`, "About this Dataset"), read from `/api/views/{id}.json`. `Sample row fields` lists the field names one `$limit=1` row returned; values were not stored.
- Freshness: all three datasets are BRFSS snapshots last updated in 2013 and stop at 2011. For later years, use the BRFSS portal or the NCHS / Vaccinations categories, not this one.

## Endpoints per asset

Replace `{id}` with the asset id from the index.

| Purpose | Endpoint |
|---|---|
| Rows as JSON (SODA 2.1, SoQL params) | `GET https://data.cdc.gov/resource/{id}.json` |
| Rows as CSV / GeoJSON | `GET https://data.cdc.gov/resource/{id}.csv`, `.geojson` |
| Column + view metadata | `GET https://data.cdc.gov/api/views/{id}.json` |
| Full export (no row limit) | `GET https://data.cdc.gov/api/views/{id}/rows.csv?accessType=DOWNLOAD` |
| Human page | `https://data.cdc.gov/d/{id}` |
| Catalog search (this category) | `GET https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&categories=Smoking%20%26%20Tobacco%20Use&limit=100` |

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
| 1 | [`j8jk-5ztv`](#j8jk-5ztv) | BRFSS Prevalence And Trends Data: Tobacco Use - Adults Who Are Current Smokers for 1995-2010 | dataset |  | 875 | 6 | 2013-08-01 |  | 200 |
| 2 | [`8zak-ewtm`](#8zak-ewtm) | BRFSS Prevalence and Trends Data: Tobacco Use - Four Level Smoking Data for 1995-2010 | dataset |  | 876 | 7 | 2013-08-02 |  | 200 |
| 3 | [`ya9m-pyut`](#ya9m-pyut) | BRFSS Prevalence and Trends Data: Tobacco Use - Four Level Smoking Data for 2011 | dataset |  | 55 | 7 | 2013-09-05 |  | 200 |

## Datasets and filtered views

### j8jk-5ztv

**BRFSS Prevalence And Trends Data: Tobacco Use - Adults Who Are Current Smokers for 1995-2010** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/j8jk-5ztv.json`
- Metadata: `GET https://data.cdc.gov/api/views/j8jk-5ztv.json`; page: https://data.cdc.gov/d/j8jk-5ztv
- Topics: Category: Smoking & Tobacco Use
- Tags: `brfss`, `current smokers`, `adults`
- Rows: 875. Data updated: 2013-08-01. Probe status: 200.
- Source: Behavioral Risk Factor Surveillance System (BRFSS)
- Description: Percentages are weighted to population characteristics. Data are not available if it did not meet BRFSS stability requirements.For more information on these requirements, as well as risk factors and calculated variables, see the Technical Documents and Survey Data for a specific year - http://www.cdc.gov/brfss/annual_data/annual_data.htm.Recommended citation: Centers for Disease Control and Prevention (CDC). Behavioral Risk Factor Surveillance System. Atlanta, Georgia: U.S. Department of Health and Human Services, Centers for Disease Control and Prevention, [appropriate year].
- Sample row fields ($limit=1): `year`, `state`, `condition`, `yes`, `no`, `location_1`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `state` | State | text |  |
| `condition` | Condition | text |  |
| `yes` | Yes | number |  |
| `no` | No | number |  |
| `location_1` | Location 1 | location |  |

### 8zak-ewtm

**BRFSS Prevalence and Trends Data: Tobacco Use - Four Level Smoking Data for 1995-2010** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8zak-ewtm.json`
- Metadata: `GET https://data.cdc.gov/api/views/8zak-ewtm.json`; page: https://data.cdc.gov/d/8zak-ewtm
- Topics: Category: Smoking & Tobacco Use
- Tags: `brfss`, `current smokers`, `former smoker`, `non-smoker`
- Rows: 876. Data updated: 2013-08-02. Probe status: 200.
- Source: Behavioral Risk Factor Surveillance System (BRFSS)
- Description: Percentages are weighted to population characteristics. Data are not available if it did not meet BRFSS stability requirements.For more information on these requirements, as well as risk factors and calculated variables, see the Technical Documents and Survey Data for a specific year - http://www.cdc.gov/brfss/annual_data/annual_data.htm.Recommended citation: Centers for Disease Control and Prevention (CDC). Behavioral Risk Factor Surveillance System. Atlanta, Georgia: U.S. Department of Health and Human Services, Centers for Disease Control and Prevention, [appropriate year].
- Sample row fields ($limit=1): `year`, `state`, `smoke_everyday`, `smoke_some_days`, `former_smoker`, `never_smoked`, `location_1`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `state` | State | text |  |
| `smoke_everyday` | Smoke everyday | number |  |
| `smoke_some_days` | Smoke some days | number |  |
| `former_smoker` | Former smoker | number |  |
| `never_smoked` | Never smoked | number |  |
| `location_1` | Location 1 | location |  |

### ya9m-pyut

**BRFSS Prevalence and Trends Data: Tobacco Use - Four Level Smoking Data for 2011** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ya9m-pyut.json`
- Metadata: `GET https://data.cdc.gov/api/views/ya9m-pyut.json`; page: https://data.cdc.gov/d/ya9m-pyut
- Topics: Category: Smoking & Tobacco Use
- Tags: `brfss`, `current smokers`, `former smoker`, `non-smoker`
- Rows: 55. Data updated: 2013-09-05. Probe status: 200.
- Source: Behavioral Risk Factor Surveillance System (BRFSS)
- Description: The 2011 BRFSS data reflects a change in weighting methodology (raking) and the addition of cell phone only respondents. Shifts in observed prevalence from 2010 to 2011 for BRFSS measures will likely reflect the new methods of measuring risk factors, rather than true trends in risk-factor prevalence. A break in trend lines after 2010 is used to reflect this change in methodolgy. Percentages are weighted to population characteristics. Data are not available if it did not meet BRFSS stability requirements.For more information on these requirements, as well as risk factors and calculated variabl…
- Sample row fields ($limit=1): `year`, `state`, `smoke_everyday`, `smoke_some_days`, `former_smoker`, `never_smoked`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `state` | State | text |  |
| `smoke_everyday` | Smoke everyday | number |  |
| `smoke_some_days` | Smoke some days | number |  |
| `former_smoker` | Former smoker | number |  |
| `never_smoked` | Never smoked | number |  |
| `location_1` | Location 1 | location |  |

## Usage tips

- Pick the dataset by question:
  - Share of adults who currently smoke, 1995-2010: `j8jk-5ztv` (`yes` / `no` percentages).
  - Four-level smoking status (`smoke_everyday`, `smoke_some_days`, `former_smoker`, `never_smoked`), 1995-2010: `8zak-ewtm`; 2011 only: `ya9m-pyut`.
- The values are weighted percentages (0-100), one row per `state` and `year`. 2011 uses a new BRFSS weighting method (raking plus cell phones), so don't read the 2010 to 2011 change as a trend.
- `state` holds full names and also the aggregates `Nationwide (States and DC)` and `Nationwide (States, DC, and Territories)`, plus territories such as `Guam` and `Puerto Rico`. Exclude the `Nationwide` rows when ranking states.
- Examples:

  ```
  # Maryland four-level smoking status by year
  GET https://data.cdc.gov/resource/8zak-ewtm.json?$where=state='Maryland'&$order=year
  # States with the highest current-smoking share in 2010
  GET https://data.cdc.gov/resource/j8jk-5ztv.json?$where=year=2010 AND state not like 'Nationwide%'&$order=yes DESC&$limit=10
  ```
