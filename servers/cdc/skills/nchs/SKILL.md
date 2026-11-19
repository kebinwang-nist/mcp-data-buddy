---
name: cdc-nchs
description: Query CDC open data (data.cdc.gov, Socrata SODA API) for the National Center for Health Statistics (NCHS) category. Use it for deaths and mortality (provisional and final counts by cause, age, sex, race and place, drug overdose, excess and COVID-19 deaths, life expectancy), births and fertility, health survey estimates (NHIS, NHANES, Household Pulse, Rapid Surveys), health care use and insurance, and the Health, United States (DQS) tables.
---

# CDC open data: National Center for Health Statistics

## Overview

- Portal: `https://data.cdc.gov` (Socrata). Category browse page: `https://data.cdc.gov/browse?category=National+Center+for+Health+Statistics`.
- Catalog snapshot taken 2026-11-09: 207 public assets in the category: 205 datasets, 0 filtered views, 0 maps, 2 charts.
- Excluded (not public or no API endpoint): 80 assets: 80 `href` (no API endpoint).
- Common tags (number of assets): `nchs` (120), `united states` (114), `mortality` (105), `deaths` (92), `nvss` (91), `covid-19` (75), `provisional` (71), `coronavirus` (63), `age` (55), `all causes` (53), `age group` (46), `race` (38), `sdoh-access-to-health-care` (37), `sex` (37), `state` (37), `hispanic origin` (35), `health us` (34), `weekly` (33), `sdoh-use-of-health-care` (27), `sdoh-poverty-income` (24).
- Surface: read-only `GET`. Each dataset and filtered view has its own data endpoint keyed by a 4x4 id (e.g. `8xy9-ubqz`). Maps and charts have no data endpoint of their own; query their parent dataset instead.
- Auth: none for reads. An optional Socrata app token in header `X-App-Token` raises the throttling limit; without one, heavy use from one IP may get HTTP 429. No key for this API exists in this project.
- Types: Socrata column types are `text`, `number`, `calendar_date` (floating timestamp, returned as `2024-10-04T00:00:00.000`), `point` (GeoJSON `{"type":"Point","coordinates":[lon,lat]}`), `url` (`{"url": ...}`), `checkbox` (boolean). In JSON output, numbers come back as strings. Null fields are omitted from a row object rather than returned as `null`.
- Topics and tags: each section's `Topics` and `Tags` lines come from the dataset's intro page (`/d/{id}`, "About this Dataset"), read from `/api/views/{id}.json`. `Sample row fields` lists the field names one `$limit=1` row returned; values were not stored.
- Freshness: still updated in 2026: provisional COVID-19 deaths by week and state `r8kw-7aab`, percent of deaths for COVID-19, influenza and RSV `4bc2-bbpq` / `53g5-jf7x`, VSRR drug overdose deaths `xkb8-kh2a` (state) and `gb4e-yj24` (county), maternal deaths `e2d5-ggg7`, quarterly VSRR birth and mortality indicators, NHIS summary statistics and the `DQS` (Health, United States) tables. Most `AH` ("ad hoc") datasets and many COVID-19 datasets stopped between 2020 and 2023. Check "Data updated" in the index.
- Not in the index: 80 `href` assets (links to external files, 66 of them restricted-use research data) have no API endpoint and were left out.

## Endpoints per asset

Replace `{id}` with the asset id from the index.

| Purpose | Endpoint |
|---|---|
| Rows as JSON (SODA 2.1, SoQL params) | `GET https://data.cdc.gov/resource/{id}.json` |
| Rows as CSV / GeoJSON | `GET https://data.cdc.gov/resource/{id}.csv`, `.geojson` |
| Column + view metadata | `GET https://data.cdc.gov/api/views/{id}.json` |
| Full export (no row limit) | `GET https://data.cdc.gov/api/views/{id}/rows.csv?accessType=DOWNLOAD` |
| Human page | `https://data.cdc.gov/d/{id}` |
| Catalog search (this category) | `GET https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&categories=National%20Center%20for%20Health%20Statistics&limit=100` |

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
| 1 | [`8xy9-ubqz`](#8xy9-ubqz) | Access and Use of Telemedicine During COVID-19 | dataset |  | 798 | 11 | 2021-08-06 | irregular | 200 |
| 2 | [`6vqh-esgs`](#6vqh-esgs) | AH County of Occurrence COVID-19 Death Counts, 2020 Provisional | dataset |  | 3,142 | 9 | 2021-06-15 | irregular | 200 |
| 3 | [`75vb-d79q`](#75vb-d79q) | AH County of Residence COVID-19 Deaths Counts, 2020 Provisional | dataset |  | 3,139 | 9 | 2021-06-03 | irregular | 200 |
| 4 | [`ite7-j2w7`](#ite7-j2w7) | AH COVID-19 Death Counts by County and Week, 2020-present | dataset |  | 534,140 | 13 | 2023-04-05 | irregular | 200 |
| 5 | [`g4z9-a9d3`](#g4z9-a9d3) | AH Cumulative Provisional COVID-19 Death Counts by Place of Death and Age Group from 2/1/2020 to 7/18/2020 | dataset |  | 3,968 | 11 | 2020-07-24 | irregular | 200 |
| 6 | [`mwk9-wnfr`](#mwk9-wnfr) | AH Cumulative Provisional COVID-19 Deaths by Sex, Race, and Age from 1/1/2020 to 7/28/2020 | dataset |  | 120 | 23 | 2020-07-29 | irregular | 200 |
| 7 | [`sf7h-sajc`](#sf7h-sajc) | AH Cumulative Provisional Death Counts by Sex, Race, and Age from 1/1/2020 to 7/4/2020 | dataset |  | 120 | 23 | 2020-08-04 | irregular | 200 |
| 8 | [`4ueh-89p9`](#4ueh-89p9) | AH Deaths by Educational Attainment, 2019-2020 | dataset |  | 763 | 8 | 2021-12-03 | irregular | 200 |
| 9 | [`w56u-89fn`](#w56u-89fn) | AH Deaths by Week, Sex, and Age for 2018-2020 | dataset |  | 9,891 | 9 | 2021-03-25 | irregular | 200 |
| 10 | [`chcz-j2du`](#chcz-j2du) | AH Deaths by Year, Sex, and Age for 2015-2020 | dataset |  | 378 | 7 | 2021-03-25 | irregular | 200 |
| 11 | [`m74n-4hbs`](#m74n-4hbs) | AH Excess Deaths by Sex, Age, and Race and Hispanic Origin | dataset |  | 174,637 | 20 | 2023-04-26 | irregular | 200 |
| 12 | [`w4jm-mysj`](#w4jm-mysj) | AH Monthly COVID-19 Deaths, by Census Region, Age, Place, and Race and Hispanic Origin, 2020 Provisional | dataset |  | 2,430 | 11 | 2020-10-12 | irregular | 200 |
| 13 | [`ezfr-g6hf`](#ezfr-g6hf) | AH Monthly Provisional Counts of Deaths by Age Group and HHS region for Select Causes of Death, 2019-2021 | dataset |  | 3,410 | 36 | 2021-08-25 | irregular | 200 |
| 14 | [`r5pw-bk5t`](#r5pw-bk5t) | AH Monthly Provisional Counts of Deaths for Select Causes of Death by Age, and Race and Hispanic Origin | dataset |  | 1,800 | 23 | 2021-08-03 | irregular | 200 |
| 15 | [`65mz-jvh5`](#65mz-jvh5) | AH Monthly Provisional Counts of Deaths for Select Causes of Death by Sex, Age, and Race and Hispanic Origin | dataset |  | 3,960 | 24 | 2021-10-13 | irregular | 200 |
| 16 | [`aie4-agrk`](#aie4-agrk) | AH Monthly Provisional COVID-19 Deaths, by Census Region, Age, and Race and Hispanic Origin | dataset |  | 4,024 | 11 | 2020-09-11 | irregular | 200 |
| 17 | [`2na8-fe6s`](#2na8-fe6s) | AH Provisional Cancer Death Counts by Month and Year, 2020-2021 | dataset |  | 2,816 | 29 | 2021-11-23 | irregular | 200 |
| 18 | [`dnhi-s2bf`](#dnhi-s2bf) | AH Provisional COVID-19 Death Counts by Quarter and County | dataset |  | 18,876 | 12 | 2021-10-06 | irregular | 200 |
| 19 | [`siwp-yg6m`](#siwp-yg6m) | AH Provisional COVID-19 Death Counts by Week, Race, and Age, United States 2020-2023 | dataset |  | 14,000 | 11 | 2023-05-10 | irregular | 200 |
| 20 | [`tdmv-axfy`](#tdmv-axfy) | AH Provisional COVID-19 Deaths and Contributing Conditions by Sex, Race and Hispanic Origin, and Age, 2020 | dataset |  | 80 | 32 | 2021-04-15 | irregular | 200 |
| 21 | [`mawz-airi`](#mawz-airi) | AH Provisional COVID-19 Deaths by Age, United States, Week 40 2020 through Week 39 2021 | dataset |  | 10 | 8 | 2021-11-10 | irregular | 200 |
| 22 | [`xmrr-rw5u`](#xmrr-rw5u) | AH Provisional COVID-19 Deaths by County and Age for 2020 | dataset |  | 40,820 | 14 | 2021-04-28 | irregular | 200 |
| 23 | [`3ts8-hsrw`](#3ts8-hsrw) | AH Provisional COVID-19 Deaths by Educational Attainment, Race, Sex, and Age | dataset |  | 224 | 9 | 2021-02-03 | irregular | 200 |
| 24 | [`9xc7-3a4q`](#9xc7-3a4q) | AH Provisional COVID-19 Deaths by HHS Region, Race, Age 65plus | dataset |  | 64,750 | 14 | 2022-10-28 | irregular | 200 |
| 25 | [`q85u-gmyc`](#q85u-gmyc) | AH Provisional COVID-19 Deaths by HHS Region, Race, and Age Group, 2020-2021 | dataset |  | 28,776 | 14 | 2021-08-26 | irregular | 200 |
| 26 | [`k5dc-apj8`](#k5dc-apj8) | AH Provisional COVID-19 Deaths by HHS Region, Race, and Age, 2015 to date | dataset |  | 456,896 | 14 | 2022-03-23 | irregular | 200 |
| 27 | [`xy7w-35q7`](#xy7w-35q7) | AH Provisional COVID-19 Deaths by HHS Region, Race, and Age, 2015-2021 | dataset |  | 110,323 | 13 | 2021-09-15 | irregular | 200 |
| 28 | [`mqmc-4b9n`](#mqmc-4b9n) | AH Provisional COVID-19 Deaths by Hospital Referral Region | dataset |  | 138,618 | 21 | 2023-11-16 | irregular | 200 |
| 29 | [`ypxr-mz8e`](#ypxr-mz8e) | AH Provisional COVID-19 Deaths by Quarter, County and Age for 2020 | dataset |  | 125,600 | 15 | 2022-06-17 | irregular | 200 |
| 30 | [`i6ej-9eac`](#i6ej-9eac) | AH Provisional COVID-19 Deaths by Race and Educational Attainment | dataset |  | 72 | 7 | 2021-02-02 | irregular | 200 |
| 31 | [`s9qn-46pq`](#s9qn-46pq) | AH Provisional COVID-19 Deaths By Race, Age, and Sex from 3/1/2020 to 7/31/2020 | dataset |  | 98 | 8 | 2021-02-01 | irregular | 200 |
| 32 | [`ikd3-vynf`](#ikd3-vynf) | AH Provisional COVID-19 Deaths by Week and Age | dataset |  | 43,460 | 11 | 2021-08-02 | irregular | 200 |
| 33 | [`6mjs-pnrx`](#6mjs-pnrx) | AH Provisional COVID-19 Deaths by Week and Age | dataset |  | 50 | 7 | 2022-08-30 | irregular | 200 |
| 34 | [`g7hk-rc8d`](#g7hk-rc8d) | AH Provisional COVID-19 Deaths by Week, Place of Death, and Age | dataset |  | 4,800 | 9 | 2021-06-08 | irregular | 200 |
| 35 | [`9z9x-g48e`](#9z9x-g48e) | AH Provisional COVID-19 Deaths by Week, Sex, and Race and Hispanic Origin | dataset |  | 1,456 | 12 | 2021-09-30 | irregular | 200 |
| 36 | [`7873-6w4v`](#7873-6w4v) | AH Provisional COVID-19 Deaths Counts by Health Service Area | dataset |  | 950 | 7 | 2021-03-09 | irregular | 200 |
| 37 | [`qdcb-uzft`](#qdcb-uzft) | AH Provisional Diabetes Death Counts for 2020 | dataset |  | 226 | 16 | 2020-10-21 | irregular | 200 |
| 38 | [`jqg8-ycmh`](#jqg8-ycmh) | AH Quarterly Excess Deaths by State, Sex, Age, and Race | dataset |  | 494,237 | 25 | 2023-09-08 | irregular | 200 |
| 39 | [`3sh4-uqpm`](#3sh4-uqpm) | AH Sickle Cell Disease Provisional Death Counts 2019-2021 | dataset |  | 129 | 8 | 2021-03-05 | irregular | 200 |
| 40 | [`aewi-gwni`](#aewi-gwni) | Asthma in children younger than age 18, by selected characteristics: United States. | dataset |  | 1,300 | 22 | 2025-06-18 | R/P1Y | 200 |
| 41 | [`wibz-pb5q`](#wibz-pb5q) | Biennial Overview of Post-acute and Long-term Care in the United States: Data from the National Post-acute and Long-term Care Study | dataset |  | 30,208 | 14 | 2026-10-19 | irregular | 200 |
| 42 | [`hk9y-quqm`](#hk9y-quqm) | Conditions Contributing to COVID-19 Deaths, by State and Age, Provisional 2020-2023 | dataset |  | 621,000 | 14 | 2023-09-27 | irregular | 200 |
| 43 | [`q3t8-zr7t`](#q3t8-zr7t) | COVID-19 Hospital Data from the National Hospital Care Survey | dataset |  | 42,132 | 10 | 2024-07-29 | R/P2M | 200 |
| 44 | [`3em4-f5qt`](#3em4-f5qt) | Data2010 | dataset |  | 963,433 | 25 | 2025-09-11 |  | 200 |
| 45 | [`9j2v-jamp`](#9j2v-jamp) | Death rates for suicide, by sex, race, Hispanic origin, and age: United States | dataset |  | 6,390 | 13 | 2021-06-07 | R/P1Y | 200 |
| 46 | [`dmzy-x2ad`](#dmzy-x2ad) | Delay or nonreceipt of needed medical care, prescription drugs, or dental care during the past 12 months due to cost: United States | dataset |  | 5,082 | 16 | 2022-04-28 | R/P1Y | 200 |
| 47 | [`jwta-jxbg`](#jwta-jxbg) | Distribution of COVID-19 Deaths and Populations, by Jurisdiction, Age, and Race and Hispanic Origin | dataset |  | 3,710 | 13 | 2023-09-27 | irregular | 200 |
| 48 | [`daba-4vfq`](#daba-4vfq) | DQS Birth and fertility rates, by age group, race, and Hispanic origin of mother: United States | dataset |  | 1,296 | 25 | 2026-06-03 | Annual R/P1Y | 200 |
| 49 | [`6tn6-vc33`](#6tn6-vc33) | DQS Cholesterol in adults age 20 and older, by selected characteristics: United States | dataset |  | 1,440 | 25 | 2025-08-25 | R/P1Y | 200 |
| 50 | [`8miz-siyd`](#8miz-siyd) | DQS Community hospital beds, by state: United States | dataset |  | 2,340 | 24 | 2026-09-23 | R/P1Y | 200 |
| 51 | [`7aq9-prdf`](#7aq9-prdf) | DQS Death rates for heart disease, by sex, race, Hispanic origin, and age: United States | dataset |  | 1,435 | 25 | 2026-05-18 | R/P1Y | 200 |
| 52 | [`h3hw-hzvg`](#h3hw-hzvg) | DQS Death rates for malignant neoplasms, by sex, race, Hispanic origin, and age: United States | dataset |  | 1,743 | 25 | 2026-05-28 | R/P1Y | 200 |
| 53 | [`w26f-tf3h`](#w26f-tf3h) | DQS Death rates for suicide, by sex, race, Hispanic origin, and age: United States | dataset |  | 1,386 | 25 | 2026-06-16 | R/P1Y | 200 |
| 54 | [`p4r5-qsgs`](#p4r5-qsgs) | DQS Delay or nonreceipt of needed medical care, prescription drugs, or dental care during the past 12 months due to cost: United States(Archived) | dataset |  | 4,278 | 21 | 2024-11-05 | R/P1Y | 200 |
| 55 | [`yib5-h3pw`](#yib5-h3pw) | DQS Dentists, by state: United States. | dataset |  | 2,496 | 24 | 2026-01-13 | R/P1Y | 200 |
| 56 | [`rdjz-vn2n`](#rdjz-vn2n) | DQS Drug overdose death rates, by drug type, sex, age, race, and Hispanic origin: United States | dataset |  | 3,738 | 25 | 2026-08-03 | R/P1Y | 200 |
| 57 | [`6vwk-ensg`](#6vwk-ensg) | DQS Estimate of Emergency Department Visits in the United States Footnotes | dataset |  | 13 | 6 | 2026-01-26 | R/P1Y | 200 |
| 58 | [`e4ec-z5aa`](#e4ec-z5aa) | DQS Estimate of Emergency Department Visits in the United States, 2016-2022 | dataset |  | 6,776 | 25 | 2025-06-09 | R/P1Y | 200 |
| 59 | [`wd75-kcmv`](#wd75-kcmv) | DQS Fetal, late fetal, and perinatal mortality rates, by detailed race and Hispanic origin of mother United States | dataset |  | 528 | 25 | 2025-06-09 | R/P1Y | 200 |
| 60 | [`7siw-u4fz`](#7siw-u4fz) | DQS Health care employment and wages, by selected occupations: United States | dataset |  | 2,444 | 25 | 2026-09-08 | R/P1Y | 200 |
| 61 | [`4q35-rqzk`](#4q35-rqzk) | DQS Hospital admission, average length of stay, outpatient visits, and outpatient surgery by type of ownership and size of hospital: United States | dataset |  | 2,254 | 25 | 2026-07-10 | R/P1Y | 200 |
| 62 | [`va5e-efw9`](#va5e-efw9) | DQS Hypertension in adults age 20 and older, by selected characteristics: United States. | dataset |  | 480 | 25 | 2025-08-25 | R/P1Y | 200 |
| 63 | [`pjb2-jvdr`](#pjb2-jvdr) | DQS Infant mortality rates, by race and Hispanic origin of mother, state, and territory: United States and U.S. dependent areas (Archived) | dataset |  | 1,710 | 22 | 2024-03-06 | R/P1Y | 200 |
| 64 | [`j7ym-uwqy`](#j7ym-uwqy) | DQS Infant, neonatal, and postneonatal mortality rates, by detailed race and Hispanic origin of mother: United States | dataset |  | 360 | 25 | 2026-06-04 | R/P1Y | 200 |
| 65 | [`a92y-5zud`](#a92y-5zud) | DQS Initial injury-related visits to hospital emergency departments, by sex, age, and intent and mechanism of injury: United States (Archived) | dataset |  | 1,480 | 25 | 2025-05-15 | R/P1Y | 200 |
| 66 | [`hdja-ybdg`](#hdja-ybdg) | DQS Medicaid coverage among persons under age 65, by selected characteristics: United States (Archived) | dataset |  | 1,944 | 21 | 2025-03-17 | R/P1Y | 200 |
| 67 | [`s57w-7gbe`](#s57w-7gbe) | DQS National health spending: United States | dataset |  | 1,755 | 25 | 2026-06-08 | R/P1Y | 200 |
| 68 | [`sz5x-j2c3`](#sz5x-j2c3) | DQS National Post-acute and Long-term Care Providers | dataset |  | 608 | 25 | 2026-08-19 | R/P2Y | 200 |
| 69 | [`6pdm-py4x`](#6pdm-py4x) | DQS National Post-acute and Long-term Care Users | dataset |  | 397 | 25 | 2026-04-16 | R/P2Y | 200 |
| 70 | [`iqm3-hbev`](#iqm3-hbev) | DQS NHANES Footnotes | dataset |  | 30 | 5 | 2026-05-28 | R/P2Y | 200 |
| 71 | [`6rvp-rahv`](#6rvp-rahv) | DQS NHANES Select Chronic Conditions Prevalence Estimates | dataset |  | 1,140 | 25 | 2026-05-28 | R/P2Y | 200 |
| 72 | [`v7tk-n6v3`](#v7tk-n6v3) | DQS NHANES Select Infectious Diseases Prevalence Estimates | dataset |  | 340 | 25 | 2026-05-28 | R/P2Y | 200 |
| 73 | [`8ekv-ep3s`](#8ekv-ep3s) | DQS NHANES Select Mean Dietary Intake Estimates | dataset |  | 4,284 | 25 | 2026-05-28 | R/P2Y | 200 |
| 74 | [`36ue-xht5`](#36ue-xht5) | DQS NHANES Select Oral Health Prevalence Estimates | dataset |  | 1,160 | 25 | 2026-05-28 | R/P2Y | 200 |
| 75 | [`gj3i-hsbz`](#gj3i-hsbz) | DQS NHIS Adult Summary Health Statistics | dataset |  | 30,576 | 25 | 2026-08-27 | R/P1Y | 200 |
| 76 | [`gpsd-ru5i`](#gpsd-ru5i) | DQS NHIS Adult Summary Statistics Footnotes | dataset |  | 80 | 5 | 2026-08-31 | R/P1Y | 200 |
| 77 | [`7ctq-myvs`](#7ctq-myvs) | DQS NHIS Child Summary Health Statistics | dataset |  | 8,918 | 25 | 2026-09-09 | Annual R/P1Y | 200 |
| 78 | [`mk5r-qxdg`](#mk5r-qxdg) | DQS NHIS Child Summary Statistics Footnotes | dataset |  | 42 | 5 | 2026-08-31 |  | 200 |
| 79 | [`v728-xui5`](#v728-xui5) | DQS NHIS Functioning difficulties Footnotes | dataset |  | 19 | 5 | 2026-10-13 | Annual (R/P1Y) | 200 |
| 80 | [`btv3-srcc`](#btv3-srcc) | DQS NHIS Functioning difficulties in adults age 18 and older by selected characteristics United States | dataset |  | 2,268 | 25 | 2026-10-13 | R/P1Y | 200 |
| 81 | [`be57-s94j`](#be57-s94j) | DQS Normal weight, overweight, and obesity among adults aged 20 and over, by selected characteristics: United States (Archived) | dataset |  | 2,352 | 25 | 2025-06-23 | R/P1Y | 200 |
| 82 | [`83mw-v57c`](#83mw-v57c) | DQS NPALS Footnotes | dataset |  | 27 | 5 | 2026-03-25 |  | 200 |
| 83 | [`mzhq-xsdd`](#mzhq-xsdd) | DQS NVSS Footnotes | dataset |  | 8 | 5 | 2026-03-18 |  | 200 |
| 84 | [`ga7k-kycn`](#ga7k-kycn) | DQS NVSS Low birthweight live births, by state: United States. | dataset |  | 520 | 26 | 2026-01-28 | R/P1Y | 200 |
| 85 | [`uzn2-cq9f`](#uzn2-cq9f) | DQS Obesity in children and adolescents aged 2–19 years, by selected characteristics: United States (Archived) | dataset |  | 693 | 25 | 2025-08-29 | R/P1Y | 200 |
| 86 | [`gu48-2cs8`](#gu48-2cs8) | DQS Personal healthcare spending: United States | dataset |  | 1,365 | 25 | 2026-06-08 | R/P1Y | 200 |
| 87 | [`kusj-ex57`](#kusj-ex57) | DQS prescription medication use in the past 30 days, by sex, race and Hispanic origin, and age group: United States | dataset |  | 1,296 | 25 | 2026-08-03 | R/P2Y | 200 |
| 88 | [`mtgp-t7vw`](#mtgp-t7vw) | DQS Use of selected substances in the past 30 days among 12th graders, 10th graders, and 8th graders, by sex and race: United States. | dataset |  | 6,951 | 25 | 2026-08-19 | Annual R/P1Y | 200 |
| 89 | [`gebw-t5b7`](#gebw-t5b7) | DQS Visits to physician offices, hospital outpatient departments, and hospital emergency departments, by age, sex, and race: United States (Archived) | dataset |  | 1,938 | 25 | 2025-05-14 | R/P1Y | 200 |
| 90 | [`95ax-ymtc`](#95ax-ymtc) | Drug overdose death rates, by drug type, sex, age, race, and Hispanic origin: United States | dataset |  | 6,228 | 15 | 2022-04-28 | R/P1Y | 200 |
| 91 | [`gypc-kpgn`](#gypc-kpgn) | Drug Use Data from Selected Hospitals | dataset |  | 8,481 | 10 | 2026-08-10 | R/P2M | 200 |
| 92 | [`v2g4-wqg2`](#v2g4-wqg2) | Early Model-based Provisional Estimates of Drug Overdose, Suicide, and Transportation-related Deaths | dataset |  | 46,665 | 13 | 2022-02-04 | irregular | 200 |
| 93 | [`ycxr-emue`](#ycxr-emue) | Estimates of Emergency Department Visits in the United States from 2016-2022 | dataset |  | 6,776 | 12 | 2024-07-25 | irregular | 200 |
| 94 | [`xkkf-xrst`](#xkkf-xrst) | Excess Deaths Associated with COVID-19 | dataset |  | 56,700 | 14 | 2023-09-27 | irregular | 200 |
| 95 | [`2m93-xvra`](#2m93-xvra) | Health conditions among children under age 18, by selected characteristics: United States | dataset |  | 2,744 | 16 | 2021-10-20 | R/P1Y | 200 |
| 96 | [`3q3z-9ucr`](#3q3z-9ucr) | Healthy People 2020 Final Progress by Population Group Chart and Table | dataset |  | 7,482 | 12 | 2022-05-04 | irregular | 200 |
| 97 | [`x749-vh2i`](#x749-vh2i) | Healthy People 2020 Final Progress Table | dataset |  | 1,111 | 11 | 2021-03-24 | irregular | 200 |
| 98 | [`f3a8-hmpp`](#f3a8-hmpp) | Healthy People 2020 Foundation Health Measures | dataset |  | 378 | 10 | 2022-01-26 | irregular | 200 |
| 99 | [`fdpm-fddm`](#fdpm-fddm) | Healthy People 2020 Overview of Health Disparities | dataset |  | 2,030 | 22 | 2022-03-08 | irregular | 200 |
| 100 | [`gjsp-ircr`](#gjsp-ircr) | HUS_Footnote_Look_Up_ASTHCH | dataset |  | 10 | 2 | 2024-09-27 |  | 200 |
| 101 | [`8pt5-q6wp`](#8pt5-q6wp) | Indicators of Anxiety or Depression Based on Reported Frequency of Symptoms During Last 7 Days | dataset |  | 16,794 | 14 | 2024-10-04 | R/P2W | 200 |
| 102 | [`jb9g-gnvr`](#jb9g-gnvr) | Indicators of Health Insurance Coverage at the Time of Interview | dataset |  | 16,056 | 16 | 2024-10-04 | R/P2W | 200 |
| 103 | [`xb3p-q62w`](#xb3p-q62w) | Indicators of Reduced Access to Care Due to the Coronavirus Pandemic During Last 4 Weeks | dataset |  | 7,118 | 14 | 2021-07-14 | irregular | 200 |
| 104 | [`nfuu-hu6j`](#nfuu-hu6j) | Infant, neonatal, postneonatal, fetal, and perinatal mortality rates, by detailed race and Hispanic origin of mother: United States | dataset |  | 2,688 | 12 | 2022-04-27 |  | 200 |
| 105 | [`w4cs-jspc`](#w4cs-jspc) | Initial injury-related visits to hospital emergency departments, by sex, age, and intent and mechanism of injury: United States | dataset |  | 1,880 | 13 | 2022-04-28 | R/P1Y | 200 |
| 106 | [`mnaa-qctp`](#mnaa-qctp) | Lack of Social Connection | dataset |  | 5,460 | 16 | 2024-10-04 | R/P1M | 200 |
| 107 | [`3j26-kg6d`](#3j26-kg6d) | Long-term Care and COVID-19 | dataset |  | 830 | 13 | 2022-09-12 | irregular | 200 |
| 108 | [`qgkx-mswu`](#qgkx-mswu) | Loss of Work Due to Illness from COVID-19 | dataset |  | 57 | 10 | 2021-08-06 | irregular | 200 |
| 109 | [`km5s-4339`](#km5s-4339) | Medicaid coverage among persons under age 65, by selected characteristics: United States | dataset |  | 1,917 | 14 | 2022-04-28 | R/P1Y | 200 |
| 110 | [`yni7-er2q`](#yni7-er2q) | Mental Health Care in the Last 4 Weeks | dataset |  | 10,404 | 15 | 2022-11-28 | R/P2W | 200 |
| 111 | [`bxq8-mugm`](#bxq8-mugm) | Monthly Counts of Deaths by Select Causes, 2014-2019 | dataset |  | 72 | 21 | 2021-02-03 | R/P1M | 200 |
| 112 | [`9dzk-mvmi`](#9dzk-mvmi) | Monthly Provisional Counts of Deaths by Select Causes, 2020-2023 | dataset |  | 45 | 31 | 2023-09-27 | R/P1W | 200 |
| 113 | [`6rkc-nb2q`](#6rkc-nb2q) | NCHS - Age-adjusted Death Rates for Selected Major Causes of Death | dataset |  | 595 | 3 | 2020-09-08 | irregular | 200 |
| 114 | [`yt7u-eiyg`](#yt7u-eiyg) | NCHS - Birth Rates for Females by Age Group: United States | dataset |  | 632 | 3 | 2020-01-27 |  | 200 |
| 115 | [`6tkz-y37d`](#6tkz-y37d) | NCHS - Birth Rates for Unmarried Women by Age, Race, and Hispanic Origin: United States | dataset |  | 1,068 | 4 | 2017-08-23 |  | 200 |
| 116 | [`rg8a-czmp`](#rg8a-czmp) | NCHS - Birth Rates for Women Aged 15-17, 17-18, and 15-19: United States, 1960-2015 | dataset |  | 168 | 3 | 2017-08-15 |  | 200 |
| 117 | [`e6fc-ccez`](#e6fc-ccez) | NCHS - Births and General Fertility Rates: United States | dataset |  | 110 | 4 | 2020-01-27 |  | 200 |
| 118 | [`g6qk-ngsf`](#g6qk-ngsf) | NCHS - Births to Unmarried Women by Age Group: United States | dataset |  | 469 | 3 | 2017-08-23 |  | 200 |
| 119 | [`v6ab-adf5`](#v6ab-adf5) | NCHS - Childhood Mortality Rates | dataset |  | 476 | 3 | 2020-09-08 | irregular | 200 |
| 120 | [`w9j2-ggv5`](#w9j2-ggv5) | NCHS - Death rates and life expectancy at birth | dataset |  | 1,071 | 5 | 2020-09-08 | irregular | 200 |
| 121 | [`pbkm-d27e`](#pbkm-d27e) | NCHS - Drug Poisoning Mortality by County: United States | dataset |  | 53,387 | 8 | 2017-04-11 |  | 200 |
| 122 | [`rpvx-m2md`](#rpvx-m2md) | NCHS - Drug Poisoning Mortality by County: United States | dataset |  | 59,584 | 12 | 2023-04-20 |  | 200 |
| 123 | [`p56q-jrxg`](#p56q-jrxg) | NCHS - Drug Poisoning Mortality by County: United States | dataset |  | 56,448 | 7 | 2018-01-22 |  | 200 |
| 124 | [`xbxb-epbu`](#xbxb-epbu) | NCHS - Drug Poisoning Mortality by State: United States | dataset |  | 2,862 | 19 | 2018-06-04 |  | 200 |
| 125 | [`jx6g-fdh6`](#jx6g-fdh6) | NCHS - Drug Poisoning Mortality by State: United States | dataset |  | 2,703 | 18 | 2017-08-25 |  | 200 |
| 126 | [`44rk-q6r2`](#44rk-q6r2) | NCHS - Drug Poisoning Mortality by State: United States | dataset |  | 3,180 | 19 | 2020-09-08 |  | 200 |
| 127 | [`epev-k6ss`](#epev-k6ss) | NCHS - Infant and neonatal mortality rates: United States, 1915-2013 | dataset |  | 198 | 3 | 2016-06-22 |  | 200 |
| 128 | [`ddsk-zebd`](#ddsk-zebd) | NCHS - Infant Mortality Rates, by Race: United States, 1915-2013 | dataset |  | 198 | 3 | 2016-06-22 |  | 200 |
| 129 | [`nt65-c7a7`](#nt65-c7a7) | NCHS - Injury Mortality: United States | dataset |  | 98,280 | 17 | 2018-06-12 |  | 200 |
| 130 | [`vc9m-u7tv`](#vc9m-u7tv) | NCHS - Injury Mortality: United States | dataset |  | 98,280 | 16 | 2018-03-07 |  | 200 |
| 131 | [`bi63-dtpu`](#bi63-dtpu) | NCHS - Leading Causes of Death: United States | dataset |  | 10,868 | 6 | 2019-10-24 |  | 200 |
| 132 | [`s54h-bixi`](#s54h-bixi) | NCHS - Natality Measures for Females by Hispanic Origin Subgroup: United States | dataset |  | 151 | 5 | 2020-01-27 |  | 200 |
| 133 | [`89yk-m38d`](#89yk-m38d) | NCHS - Natality Measures for Females by Race and Hispanic Origin: United States | dataset |  | 470 | 5 | 2020-01-27 |  | 200 |
| 134 | [`jvf6-ix4w`](#jvf6-ix4w) | NCHS - Nonmarital Birth Rates, by Age Group for All Women Age 15-44: United States, 1970-2013 | dataset |  | 1,494 | 4 | 2015-12-02 |  | 200 |
| 135 | [`isx2-c2ii`](#isx2-c2ii) | NCHS - Percent Distribution of Births for Females by Age Group: United States | dataset |  | 688 | 3 | 2020-01-27 |  | 200 |
| 136 | [`hzd8-r9mj`](#hzd8-r9mj) | NCHS - Percent Distribution of Births to Unmarried Women by Age Group: United States | dataset |  | 230 | 3 | 2017-08-23 |  | 200 |
| 137 | [`vdpk-qzpr`](#vdpk-qzpr) | NCHS - Potentially Excess Deaths from the Five Leading Causes of Death | dataset |  | 205,920 | 13 | 2017-08-15 |  | 200 |
| 138 | [`7pcd-2tnr`](#7pcd-2tnr) | NCHS - Pregnancy and Live Birth Rates, by Marital Status and Race and Hispanic Origin: United States, 1990-2010 | dataset |  | 190 | 5 | 2015-12-02 |  | 200 |
| 139 | [`hdy7-e2a3`](#hdy7-e2a3) | NCHS - Pregnancy Rates, by Age for Hispanic Women: United States, 1990-2010 | dataset |  | 190 | 5 | 2015-12-02 |  | 200 |
| 140 | [`3h58-x6cd`](#3h58-x6cd) | NCHS - Teen Birth Rates for Age Group 15-19 in the United States by County | dataset |  | 56,466 | 9 | 2022-04-08 |  | 200 |
| 141 | [`e8kx-wbww`](#e8kx-wbww) | NCHS - Teen Birth Rates for Females by Age Group, Race, and Hispanic Origin: United States | dataset |  | 896 | 4 | 2020-01-27 |  | 200 |
| 142 | [`mc4y-cbbv`](#mc4y-cbbv) | NCHS - Top Five Leading Causes of Death: United States, 1990, 1950, 2000 | dataset |  | 15 | 3 | 2020-09-08 | irregular | 200 |
| 143 | [`y268-sna3`](#y268-sna3) | NCHS - U.S. and State Trends on Teen Births | dataset |  | 4,680 | 8 | 2022-05-09 |  | 200 |
| 144 | [`jqwm-z2g9`](#jqwm-z2g9) | NCHS - VSRR Quarterly provisional estimates for infant mortality | dataset |  | 168 | 10 | 2026-10-29 | R/P3M | 200 |
| 145 | [`76vv-a7x8`](#76vv-a7x8) | NCHS - VSRR Quarterly provisional estimates for selected birth indicators | dataset |  | 1,000 | 8 | 2026-09-17 | R/P3M | 200 |
| 146 | [`489q-934x`](#489q-934x) | NCHS - VSRR Quarterly provisional estimates for selected indicators of mortality | dataset |  | 924 | 69 | 2026-06-23 | R/P3M | 200 |
| 147 | [`p89x-xx88`](#p89x-xx88) | NCHS Rapid Surveys System | dataset |  | 6,279 | 8 | 2026-02-26 | R/P3M | 200 |
| 148 | [`i667-sjhg`](#i667-sjhg) | NHANES Select Chronic Conditions Prevalence Estimates | dataset |  | 950 | 12 | 2023-02-27 | R/P1Y | 200 |
| 149 | [`pqn7-e45s`](#pqn7-e45s) | NHANES Select Infectious Diseases Prevalence Estimates | dataset |  | 340 | 12 | 2023-02-27 | R/P1Y | 200 |
| 150 | [`8wmh-yzz9`](#8wmh-yzz9) | NHANES Select Mean Dietary Intake Estimates | dataset |  | 3,570 | 13 | 2023-02-27 | R/P1Y | 200 |
| 151 | [`ggsw-596z`](#ggsw-596z) | NHANES Select Oral Health Prevalence Estimates | dataset |  | 1,160 | 14 | 2023-02-27 | R/P1Y | 200 |
| 152 | [`krhz-spsc`](#krhz-spsc) | NHIS Adult 3-Year Summary Health Statistics | dataset |  | 7,599 | 7 | 2025-09-18 | R/P1Y | 200 |
| 153 | [`25m4-6qqq`](#25m4-6qqq) | NHIS Adult Summary Health Statistics | dataset |  | 30,499 | 8 | 2026-08-27 |  | 200 |
| 154 | [`wxz7-ekz9`](#wxz7-ekz9) | NHIS Child Summary Health Statistics | dataset |  | 8,918 | 7 | 2026-08-27 |  | 200 |
| 155 | [`trpk-sp8z`](#trpk-sp8z) | NHIS Interactive Biannual Early Release Estimates | dataset |  | 5,634 | 9 | 2026-05-28 | R/P6M | 200 |
| 156 | [`wpti-gvdi`](#wpti-gvdi) | NHIS Interactive Quarterly Early Release Estimates | dataset |  | 528 | 8 | 2025-06-24 | R/P3M | 200 |
| 157 | [`5pqj-rvh4`](#5pqj-rvh4) | NHIS Teen | dataset |  | 3,400 | 22 | 2024-09-03 |  | 200 |
| 158 | [`3nzu-udr9`](#3nzu-udr9) | Normal weight, overweight, and obesity among adults aged 20 and over, by selected characteristics: United States | dataset |  | 3,360 | 16 | 2022-04-28 | R/P1Y | 200 |
| 159 | [`9gay-j69q`](#9gay-j69q) | Obesity among children and adolescents aged 2–19 years, by selected characteristics: United States | dataset |  | 840 | 16 | 2022-04-28 | R/P1W | 200 |
| 160 | [`kk8c-wtm4`](#kk8c-wtm4) | Physician Experiences Related to COVID-19 from the National Ambulatory Medical Care Survey | dataset |  | 160 | 11 | 2023-01-12 | irregular | 200 |
| 161 | [`jfbs-8cpp`](#jfbs-8cpp) | Population Group Estimates used in the Healthy People 2020 Overview of Health Disparities | dataset |  | 6,978 | 10 | 2022-03-08 | irregular | 200 |
| 162 | [`gsea-w83j`](#gsea-w83j) | Post-COVID Conditions | dataset |  | 18,639 | 16 | 2024-10-04 | irregular | 200 |
| 163 | [`367e-pucc`](#367e-pucc) | Preliminary Estimates of Visits to Health Centers in the United States, January 2022-December 2025 | dataset |  | 6,208 | 11 | 2026-06-30 | Monthly | 200 |
| 164 | [`28df-2bwy`](#28df-2bwy) | Prevalence of Selected Measures Among Adults Aged 20 and Over: United States, 1999-2000 through 2017-2018 | dataset |  | 360 | 6 | 2020-12-16 | irregular | 200 |
| 165 | [`yrur-wghw`](#yrur-wghw) | Provisional COVID-19 death counts and rates by month, jurisdiction of residence, and demographic characteristics | dataset |  | 71,280 | 13 | 2026-09-17 | R/P1W | 200 |
| 166 | [`dmnu-8erf`](#dmnu-8erf) | Provisional COVID-19 death counts and rates, by jurisdiction of residence and demographic characteristics | dataset |  | 177,309 | 13 | 2023-10-26 | irregular | 200 |
| 167 | [`3apk-4u4f`](#3apk-4u4f) | Provisional COVID-19 Death Counts by Age in Years, 2020-2023 | dataset |  | 174 | 7 | 2023-06-28 | irregular | 200 |
| 168 | [`r8kw-7aab`](#r8kw-7aab) | Provisional COVID-19 Death Counts by Week Ending Date and State | dataset |  | 24,138 | 17 | 2026-11-05 | R/P1W | 200 |
| 169 | [`kn79-hsxy`](#kn79-hsxy) | Provisional COVID-19 Death Counts in the United States by County | dataset |  | 3,089 | 10 | 2023-06-28 | irregular | 200 |
| 170 | [`mpx5-t7tu`](#mpx5-t7tu) | Provisional COVID-19 death counts, rates, and percent of total deaths, by jurisdiction of residence | dataset |  | 45,565 | 14 | 2026-09-17 | R/P1W | 200 |
| 171 | [`k8wy-p9cg`](#k8wy-p9cg) | Provisional COVID-19 Deaths by County, and Race and Hispanic Origin | dataset |  | 3,687 | 21 | 2023-09-27 | irregular | 200 |
| 172 | [`tpcp-uiv5`](#tpcp-uiv5) | Provisional COVID-19 Deaths by HHS Region, Race, and Age | dataset |  | 194,040 | 14 | 2023-09-27 | irregular | 200 |
| 173 | [`4va6-ph5s`](#4va6-ph5s) | Provisional COVID-19 Deaths by Place of Death and Age | dataset |  | 218,700 | 17 | 2023-09-27 | irregular | 200 |
| 174 | [`uggs-hy5q`](#uggs-hy5q) | Provisional COVID-19 Deaths by Place of Death and State | dataset |  | 22,842 | 15 | 2023-06-28 | irregular | 200 |
| 175 | [`ks3g-spdg`](#ks3g-spdg) | Provisional COVID-19 Deaths by Race and Hispanic Origin, and Age | dataset |  | 6,489 | 13 | 2023-09-27 | irregular | 200 |
| 176 | [`9bhg-hcku`](#9bhg-hcku) | Provisional COVID-19 Deaths by Sex and Age | dataset |  | 137,700 | 16 | 2023-09-27 | irregular | 200 |
| 177 | [`9hdi-ekmb`](#9hdi-ekmb) | Provisional COVID-19 Deaths by Week and County Social Vulnerability Index | dataset |  | 780 | 10 | 2023-09-27 | irregular | 200 |
| 178 | [`hkhc-f7hg`](#hkhc-f7hg) | Provisional COVID-19 Deaths by Week and Urbanicity | dataset |  | 585 | 11 | 2023-09-27 | irregular | 200 |
| 179 | [`vsak-wrfu`](#vsak-wrfu) | Provisional COVID-19 Deaths by Week, Sex, and Age | dataset |  | 6,552 | 8 | 2023-06-28 | irregular | 200 |
| 180 | [`pj7m-y5uh`](#pj7m-y5uh) | Provisional COVID-19 Deaths: Distribution of Deaths by Race and Hispanic Origin | dataset |  | 10,600 | 16 | 2023-09-27 | irregular | 200 |
| 181 | [`nr4s-juj3`](#nr4s-juj3) | Provisional COVID-19 Deaths: Focus on Ages 0-18 Years | dataset |  | 29 | 8 | 2023-06-28 | irregular | 200 |
| 182 | [`hc4f-j6nb`](#hc4f-j6nb) | Provisional Death Counts for Coronavirus Disease (COVID-19) | dataset |  | 93 | 14 | 2020-04-30 | irregular | 200 |
| 183 | [`ynw2-4viq`](#ynw2-4viq) | Provisional Death Counts for Influenza, Pneumonia, and COVID-19 | dataset |  | 50,400 | 17 | 2023-11-02 | irregular | 200 |
| 184 | [`8hzs-zshh`](#8hzs-zshh) | Provisional drug overdose death counts for specific drugs | dataset |  | 11,088 | 9 | 2026-07-15 | R/P6M | 200 |
| 185 | [`dtm2-meqi`](#dtm2-meqi) | Provisional Drug Overdose Deaths by Urban/Rural Classification Scheme for 12 month-ending December 2018-December 2020 | dataset |  | 150 | 8 | 2021-08-10 | irregular | 200 |
| 186 | [`4bc2-bbpq`](#4bc2-bbpq) | Provisional Percent of Deaths for COVID-19, Influenza, and RSV | dataset |  | 144 | 3 | 2026-11-06 | R/P1W | 200 |
| 187 | [`53g5-jf7x`](#53g5-jf7x) | Provisional Percent of Deaths for COVID-19, Influenza, and RSV by Select Characteristics | dataset |  | 22,080 | 17 | 2026-11-06 | R/P1W | 200 |
| 188 | [`th9n-ghnr`](#th9n-ghnr) | Reduced Access to Care During COVID-19 | dataset |  | 1,710 | 11 | 2021-08-06 | irregular | 200 |
| 189 | [`h7xa-837u`](#h7xa-837u) | Telemedicine Use in the Last 4 Weeks | dataset |  | 3,344 | 15 | 2022-11-28 | R/P2W | 200 |
| 190 | [`5h56-n989`](#5h56-n989) | U.S. Life Expectancy at Birth by State and Census Tract - 2010-2015 | dataset |  | 73,121 | 6 | 2020-03-09 | irregular | 200 |
| 191 | [`a5a8-jsrq`](#a5a8-jsrq) | U.S. State Life Expectancy by Sex, 2018 | dataset |  | 156 | 5 | 2022-02-03 | irregular | 200 |
| 192 | [`ncvk-7amm`](#ncvk-7amm) | U.S. State Life Expectancy by Sex, 2019 | dataset |  | 156 | 5 | 2022-02-03 | irregular | 200 |
| 193 | [`ss2j-8ajj`](#ss2j-8ajj) | U.S. State Life Expectancy by Sex, 2020 | dataset |  | 156 | 5 | 2022-09-01 | irregular | 200 |
| 194 | [`it4f-frdc`](#it4f-frdc) | U.S. State Life Expectancy by Sex, 2021 | dataset |  | 153 | 5 | 2024-09-11 | irregular | 200 |
| 195 | [`xt86-xqxz`](#xt86-xqxz) | Visits to physician offices, hospital outpatient departments, and hospital emergency departments, by age, sex, and race: United States | dataset |  | 3,570 | 16 | 2021-06-03 |  | 200 |
| 196 | [`hmz2-vwda`](#hmz2-vwda) | VSRR - State and National Provisional Counts for Live Births, Deaths, and Infant Deaths | dataset |  | 1,980 | 6 | 2024-12-11 | R/P3M | 200 |
| 197 | [`gb4e-yj24`](#gb4e-yj24) | VSRR Provisional County-Level Drug Overdose Death Counts | dataset |  | 235,800 | 17 | 2026-10-14 |  | 200 |
| 198 | [`xkb8-kh2a`](#xkb8-kh2a) | VSRR Provisional Drug Overdose Death Counts | dataset |  | 87,543 | 12 | 2026-10-14 | R/P1M | 200 |
| 199 | [`e2d5-ggg7`](#e2d5-ggg7) | VSRR Provisional Maternal Death Counts and Rates | dataset |  | 870 | 12 | 2026-07-16 | R/P3M | 200 |
| 200 | [`u6jv-9ijr`](#u6jv-9ijr) | Weekly Counts of Death by Jurisdiction and Select Causes of Death | dataset |  | 481,140 | 15 | 2023-09-27 | irregular | 200 |
| 201 | [`y5bj-9g5w`](#y5bj-9g5w) | Weekly Counts of Deaths by Jurisdiction and Age | dataset |  | 269,016 | 11 | 2023-09-27 | irregular | 200 |
| 202 | [`qfhf-uhaa`](#qfhf-uhaa) | Weekly Counts of Deaths by Jurisdiction, and Race and Hispanic Origin | dataset |  | 985,608 | 15 | 2023-09-27 | irregular | 200 |
| 203 | [`3yf8-kanr`](#3yf8-kanr) | Weekly Counts of Deaths by State and Select Causes, 2014-2019 | dataset |  | 16,902 | 30 | 2021-01-21 | irregular | 200 |
| 204 | [`9cpv-whbv`](#9cpv-whbv) | Weekly counts of deaths from all causes by jurisdiction, 2015-2019 | dataset |  | 65,382 | 8 | 2024-09-23 | R/P4Y | 200 |
| 205 | [`muzy-jte6`](#muzy-jte6) | Weekly Provisional Counts of Deaths by State and Select Causes, 2020-2023 | dataset |  | 10,476 | 35 | 2023-09-27 | irregular | 200 |

Maps and charts (no data endpoint; query the parent):

| Id | Name | Type | Built on | Updated |
|---|---|---|---|---|
| `32c3-mvuz` | Deaths by Race and Hispanic Origin, Ages 0-18 Years | chart | `nr4s-juj3` (Provisional COVID-19 Deaths: Focus on Ages 0-18 Years) | 2026-09-10 |
| `xa4b-4pzv` | Deaths by Sex, Ages 0-18 years | chart | `nr4s-juj3` (Provisional COVID-19 Deaths: Focus on Ages 0-18 Years) | 2026-09-10 |

Map/chart topics and tags:

- `32c3-mvuz`: Category: National Center for Health Statistics; Tags: none
- `xa4b-4pzv`: Category: National Center for Health Statistics; Tags: none

## Datasets and filtered views

### 8xy9-ubqz

**Access and Use of Telemedicine During COVID-19** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8xy9-ubqz.json`
- Metadata: `GET https://data.cdc.gov/api/views/8xy9-ubqz.json`; page: https://data.cdc.gov/d/8xy9-ubqz
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `rands`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-use-of-health-care`
- Rows: 798. Data updated: 2021-08-06. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DRM
- Description: The Research and Development Survey (RANDS) is a platform designed for conducting survey question evaluation and statistical research. RANDS is an ongoing series of surveys from probability-sampled commercial survey panels used for methodological research at the National Center for Health Statistics (NCHS). RANDS estimates are generated using an experimental approach that differs from the survey design approaches generally used by NCHS, including possible biases from different response patterns and sampling frames as well as increased variability from lower sample sizes. Use of the RANDS plat…
- Sample row fields ($limit=1): `round`, `indicator`, `group`, `subgroup`, `sample_size`, `response`, `percent`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `round` | Round | number | Data collection period; Round 1 occurred June 9, 2020–July 6, 2020, Round 2 occurred August 3, 2020–August 20, 2020, and Round 3 occurred May 17, 2021–June 30, 2021 |
| `indicator` | Indicator | text | Indicators include 1) provider offers telemedicine, 2) scheduled one or more telemedicine appointments, and 3) provider offered telemedicine prior to pandemic. |
| `group` | Group | text | Estimates were reported at the national level (total) and by age group, race and Hispanic origin, sex, education level, urbanization, and selected chronic conditions. |
| `subgroup` | Subgroup | text | Subcategories for each group |
| `sample_size` | Sample Size | number | Sample size |
| `response` | Response | text | Survey question response for each indicator |
| `percent` | Percent | number | Percent estimate |
| `standard_error` | Standard Error | number | Standard error estimate |
| `suppression` | Suppression | text | Identifies percent and standard error estimates that did not meet NCHS Data Presentation Standards for Proportions |
| `significant_1` | Significant 1 | number | Indicator for significance testing of difference from Round 1 where a value of 0 indicates the estimates are not statistically significantly different at the 5% significance level and a value of 1 indicates that the estimates are statistic… |
| `significant_2` | Significant 2 | number | Indicator for significance testing of difference from Round 2 where a value of 0 indicates the estimates are not statistically significantly different at the 5% significance level and a value of 1 indicates that the estimates are statistic… |

### 6vqh-esgs

**AH County of Occurrence COVID-19 Death Counts, 2020 Provisional** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/6vqh-esgs.json`
- Metadata: `GET https://data.cdc.gov/api/views/6vqh-esgs.json`; page: https://data.cdc.gov/d/6vqh-esgs
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `mortality`, `covid-19`, `county`, `nchs`, `coronavirus`, `all causes`, `nvss`, `provisional`, `yearly`, `united states`
- Rows: 3,142. Data updated: 2021-06-15. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional count of deaths involving coronavirus disease 2019 (COVID-19) by United States county of occurrence, from January 1, 2020 through December 31, 2020.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `state`, `county`, `fips_code`, `covid_19_deaths`, `footnote`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | text | Date of analysis |
| `start_date` | Start Date | text | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `state` | State | text | State name |
| `county` | County of Occurrence | text | County name |
| `fips_code` | Fips Code | text | FIPS County Code |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19, coded to ICD-code U07.1 |
| `total_deaths` | Total Deaths | number | Deaths from all causes |
| `footnote` | Footnote | text | Suppressed counts 1-9 |

### 75vb-d79q

**AH County of Residence COVID-19 Deaths Counts, 2020 Provisional** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/75vb-d79q.json`
- Metadata: `GET https://data.cdc.gov/api/views/75vb-d79q.json`; page: https://data.cdc.gov/d/75vb-d79q
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `mortality`, `covid-19`, `county`, `nchs`, `coronavirus`, `yearly`, `all causes`, `nvss`, `provisional`, `united states`
- Rows: 3,139. Data updated: 2021-06-03. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional count of deaths involving coronavirus disease 2019 (COVID-19) by United States county of residence, from January 1, 2020 through December 31, 2020.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `state`, `county`, `fips_code`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Data as of |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `state` | State | text | State name |
| `county` | County of Residence | text | County name |
| `fips_code` | Fips Code | number | FIPS County Code |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19, coded to ICD-code U07.1 |
| `total_deaths` | Total Deaths | number | Deaths from all causes |
| `footnote` | Footnote | text | Suppressed counts 1-9 |

### ite7-j2w7

**AH COVID-19 Death Counts by County and Week, 2020-present** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ite7-j2w7.json`
- Metadata: `GET https://data.cdc.gov/api/views/ite7-j2w7.json`; page: https://data.cdc.gov/d/ite7-j2w7
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `mortality`, `covid-19`, `county`, `nchs`, `coronavirus`, `all causes`, `nvss`, `provisional`, `weekly`, `united states`, `sdoh-environmental`
- Rows: 534,140. Data updated: 2023-04-05. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional count of deaths involving COVID-19 by United States county of occurrence, by week of death.
- Sample row fields ($limit=1): `data_as_of`, `mmwr_week`, `week_ending_date`, `jurisdiction_of_occurrence`, `state`, `county`, `stfips`, `cofips`, `fips_code`, `urban_rural_code`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `mmwr_week` | MMWR Week | number | MMWR week number |
| `week_ending_date` | Week-Ending Date | calendar_date | Week-ending date |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text | Jurisdiction of occurrence |
| `state` | State | text | State name |
| `county` | County | text | County name |
| `stfips` | STFIPS | number | State FIPS code |
| `cofips` | COFIPS | number | County FIPS code |
| `fips_code` | FIPS Code | number | FIPS code |
| `urban_rural_code` | Urban Rural Code | text | Urban rural code |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19, coded to ICD-code U07.1 |
| `total_deaths` | Total Deaths | number | Deaths from all causes |
| `footnote` | Footnote | text | Suppressed counts 1-9 |

### g4z9-a9d3

**AH Cumulative Provisional COVID-19 Death Counts by Place of Death and Age Group from 2/1/2020 to 7/18/2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/g4z9-a9d3.json`
- Metadata: `GET https://data.cdc.gov/api/views/g4z9-a9d3.json`; page: https://data.cdc.gov/d/g4z9-a9d3
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `place of death`, `age group`, `age`, `all causes`, `covid-19`, `coronavirus`, `pneumonia`, `state`, `puerto rico`
- Rows: 3,968. Data updated: 2020-07-24. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Deaths involving coronavirus disease 2019 (COVID-19) and pneumonia reported to NCHS by jurisdiction of occurrence, place of death, and age group.
- Sample row fields ($limit=1): `data_as_of`, `start_week`, `end_week`, `hhs_region`, `state`, `place_of_death`, `age_group`, `all_deaths_involving_covid`, `deaths_from_all_causes`, `deaths_involving_pneumonia`, `deaths_involving_covid_19`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Date of analysis |
| `start_week` | Start week | calendar_date | First week-ending date of data period |
| `end_week` | End Week | calendar_date | Last week-ending date of data period |
| `hhs_region` | HHS Region | number | HHS Region |
| `state` | State | text | State |
| `place_of_death` | Place of Death | text | Place Of Death |
| `age_group` | Age group | text | Age group |
| `all_deaths_involving_covid` | All Deaths involving COVID-19 (U07.1) | number | All Deaths involving COVID-19 (U07.1) |
| `deaths_from_all_causes` | Deaths from All Causes | number | Deaths from All Causes |
| `deaths_involving_pneumonia` | Deaths involving Pneumonia, with or without COVID-19, excluding Influenza deaths (J12.0–J18.9) | number | "Deaths involving Pneumonia, with or without COVID-19, excluding Influenza deaths (J12.0–J18.9)" |
| `deaths_involving_covid_19` | Deaths involving COVID-19 and Pneumonia, excluding Influenza (U07.1 and J12.0–J18.9) | number | Deaths involving COVID-19 and Pneumonia, excluding Influenza (U07.1 and J12.0–J18.9) |

### mwk9-wnfr

**AH Cumulative Provisional COVID-19 Deaths by Sex, Race, and Age from 1/1/2020 to 7/28/2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/mwk9-wnfr.json`
- Metadata: `GET https://data.cdc.gov/api/views/mwk9-wnfr.json`; page: https://data.cdc.gov/d/mwk9-wnfr
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `sex`, `race`, `hispanic origin`, `age group`, `age`, `all causes`, `causes of death`, `covid-19`, `coronavirus`, `natural cause`, `septicemia`, `cancer`, `diabetes`, `alzheimer disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `respiratory disease`, `kidney disease`, `diseases of heart`, `cerebrovascular disease`
- Rows: 120. Data updated: 2020-07-29. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Cumulative provisional counts of deaths sex, race/Hispanic origin, age group, and by select underlying causes of death. The dataset also includes provisional counts of death for COVID-19, coded to ICD-10 code U07.1 as an underlying or multiple cause of death. Includes deaths that occurred between January 1, 2020 to July 28, 2020.
- Sample row fields ($limit=1): `data_as_of`, `sex`, `race_ethnicity`, `age_group`, `year`, `mmwrweek`, `analysis_period_start_date`, `analysis_period_end_date`, `allcause`, `naturalcause`, `septicemia_a40_a41`, `malignant_neoplasms_c00_c97`, `diabetes_mellitus_e10_e14`, `alzheimer_disease_g30`, `influenza_and_pneumonia_j09`, `chronic_lower_respiratory`, `other_diseases_of_respiratory`, `nephritis_nephrotic_syndrome`, `symptoms_signs_and_abnormal`, `diseases_of_heart_i00_i09`, `cerebrovascular_diseases`, `covid_19_u071_multiple_cause`, `covid_19_u071_underlying`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Data of analysis |
| `sex` | Sex | text | Sex |
| `race_ethnicity` | Race/Ethnicity | text | Race or Hispanic Origin Group |
| `age_group` | Age group | text | Age group |
| `year` | Year | number | Year |
| `mmwrweek` | MMWRWeek | number | MMWR Week Number |
| `analysis_period_start_date` | Analysis Period Start Date | calendar_date | First date of data period |
| `analysis_period_end_date` | Analysis Period End Date | calendar_date | Last date of data period |
| `allcause` | AllCause | number | AllCause |
| `naturalcause` | NaturalCause | number | NaturalCause (A00-R99) |
| `septicemia_a40_a41` | Septicemia (A40-A41) | number | Septicemia (A40-A41) |
| `malignant_neoplasms_c00_c97` | Malignant neoplasms (C00-C97) | number | Malignant neoplasms (C00-C97) |
| `diabetes_mellitus_e10_e14` | Diabetes mellitus (E10-E14) | number | Diabetes mellitus (E10-E14) |
| `alzheimer_disease_g30` | Alzheimer disease (G30) | number | Alzheimer disease (G30) |
| `influenza_and_pneumonia_j09` | Influenza and pneumonia (J09-J18) | number | Influenza and pneumonia (J10-J18) |
| `chronic_lower_respiratory` | Chronic lower respiratory diseases (J40-J47) | number | Chronic lower respiratory diseases (J40-J47) |
| `other_diseases_of_respiratory` | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) | number | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) |
| `nephritis_nephrotic_syndrome` | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) | number | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) |
| `symptoms_signs_and_abnormal` | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) | number | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) |
| `diseases_of_heart_i00_i09` | Diseases of heart (I00-I09,I11,I13,I20-I51) | number | Diseases of heart (I00-I09,I11,I13,I20-I51) |
| `cerebrovascular_diseases` | Cerebrovascular diseases (I60-I69) | number | Cerebrovascular diseases (I60-I69) |
| `covid_19_u071_multiple_cause` | COVID-19 (U071, Multiple Cause of Death) | number | COVID-19 (U071, Multiple Cause of Death) |
| `covid_19_u071_underlying` | COVID-19 (U071, Underlying Cause of Death) | number | COVID-19 (U071,Underlying Cause of Death) |

### sf7h-sajc

**AH Cumulative Provisional Death Counts by Sex, Race, and Age from 1/1/2020 to 7/4/2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/sf7h-sajc.json`
- Metadata: `GET https://data.cdc.gov/api/views/sf7h-sajc.json`; page: https://data.cdc.gov/d/sf7h-sajc
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `weekly`, `sex`, `race`, `hispanic origin`, `age group`, `age`, `all causes`, `causes of death`, `covid-19`, `coronavirus`, `natural cause`, `septicemia`, `cancer`, `diabetes`, `alzheimer disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `respiratory disease`, `kidney disease`, `diseases of heart`, `cerebrovascular disease`
- Rows: 120. Data updated: 2020-08-04. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Cumulative provisional counts of deaths sex, race/Hispanic origin, age group, and by select underlying causes of death. The dataset also includes provisional counts of death for COVID-19, coded to ICD-10 code U07.1 as an underlying or multiple cause of death. Includes deaths that occurred between January 1, 2020 to July 4, 2020.
- Sample row fields ($limit=1): `analysisdate`, `sex`, `race_ethnicity`, `age_group`, `year`, `mmwrweek`, `analysis_period_start_date`, `analysis_period_end_date`, `allcause`, `naturalcause`, `septicemia_a40_a41`, `malignant_neoplasms_c00_c97`, `diabetes_mellitus_e10_e14`, `alzheimer_disease_g30`, `influenza_and_pneumonia_j09`, `chronic_lower_respiratory`, `other_diseases_of_respiratory`, `nephritis_nephrotic_syndrome`, `symptoms_signs_and_abnormal`, `diseases_of_heart_i00_i09`, `cerebrovascular_diseases`, `covid_19_u071_multiple_cause`, `covid_19_u071_underlying`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `analysisdate` | Data as of | calendar_date | Date of analysis |
| `sex` | Sex | text | Sex |
| `race_ethnicity` | Race/Ethnicity | text | Race or Hispanic Origin Group |
| `age_group` | Age group | text | Age group |
| `year` | Year | number | Year |
| `mmwrweek` | MMWRWeek | number | MMWR Week Number |
| `analysis_period_start_date` | Analysis Period Start Date | calendar_date | First date of data period |
| `analysis_period_end_date` | Analysis Period End Date | calendar_date | Last date of data period |
| `allcause` | AllCause | number | AllCause |
| `naturalcause` | NaturalCause | number | NaturalCause (A00-R99) |
| `septicemia_a40_a41` | Septicemia (A40-A41) | number | Septicemia (A40-A41) |
| `malignant_neoplasms_c00_c97` | Malignant neoplasms (C00-C97) | number | Malignant neoplasms (C00-C97) |
| `diabetes_mellitus_e10_e14` | Diabetes mellitus (E10-E14) | number | Diabetes mellitus (E10-E14) |
| `alzheimer_disease_g30` | Alzheimer disease (G30) | number | Alzheimer disease (G30) |
| `influenza_and_pneumonia_j09` | Influenza and pneumonia (J09-J18) | number | Influenza and pneumonia (J10-J18) |
| `chronic_lower_respiratory` | Chronic lower respiratory diseases (J40-J47) | number | Chronic lower respiratory diseases (J40-J47) |
| `other_diseases_of_respiratory` | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) | number | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) |
| `nephritis_nephrotic_syndrome` | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) | number | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) |
| `symptoms_signs_and_abnormal` | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) | number | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) |
| `diseases_of_heart_i00_i09` | Diseases of heart (I00-I09,I11,I13,I20-I51) | number | Diseases of heart (I00-I09,I11,I13,I20-I51) |
| `cerebrovascular_diseases` | Cerebrovascular diseases (I60-I69) | number | Cerebrovascular diseases (I60-I69) |
| `covid_19_u071_multiple_cause` | COVID-19 (U071, Multiple Cause of Death) | number | COVID-19 (U071, Multiple Cause of Death) |
| `covid_19_u071_underlying` | COVID-19 (U071, Underlying Cause of Death) | number | COVID-19 (U071,Underlying Cause of Death) |

### 4ueh-89p9

**AH Deaths by Educational Attainment, 2019-2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/4ueh-89p9.json`
- Metadata: `GET https://data.cdc.gov/api/views/4ueh-89p9.json`; page: https://data.cdc.gov/d/4ueh-89p9
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `covid-19`, `education`, `race`, `age`, `sex`, `nchs`, `nvss`, `mortality`, `united states`, `yearly`, `coronavirus`, `hispanic origin`, `age group`, `provisional`, `all causes`, `sdoh-high-school`, `sdoh-higher-education`
- Rows: 763. Data updated: 2021-12-03. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Deaths by educational attainment, race, sex, and age group for deaths occurring in the United States. Data are final for 2019 and provisional for 2020. The dataset includes annual counts of death for total deaths and for COVID-19, coded to ICD-10 code U07.1 as an underlying or multiple cause of death.
- Sample row fields ($limit=1): `data_as_of`, `year`, `education_level`, `race_or_hispanic_origin`, `sex`, `age_group`, `total_deaths`, `covid_19_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date |  |
| `year` | Year | text |  |
| `education_level` | Education Level | text |  |
| `race_or_hispanic_origin` | Race or Hispanic Origin | text |  |
| `sex` | Sex | text |  |
| `age_group` | Age Group | text |  |
| `total_deaths` | Total Deaths | number |  |
| `covid_19_deaths` | COVID-19 Deaths | number |  |

### w56u-89fn

**AH Deaths by Week, Sex, and Age for 2018-2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/w56u-89fn.json`
- Metadata: `GET https://data.cdc.gov/api/views/w56u-89fn.json`; page: https://data.cdc.gov/d/w56u-89fn
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `deaths`, `mortality`, `united states`, `weekly`, `sex`, `age`, `age group`, `all causes`
- Rows: 9,891. Data updated: 2021-03-25. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Death counts by age, sex, and week for years 2018-2020. Data for 2018 and 2019 are final. Data for 2020 are provisional.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `mmwr_year`, `mmwr_week`, `week_ending_date`, `sex`, `age_group`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `mmwr_year` | MMWR Year | text |  |
| `mmwr_week` | MMWR Week | number |  |
| `week_ending_date` | Week Ending Date | calendar_date |  |
| `sex` | Sex | text |  |
| `age_group` | Age Group | text |  |
| `total_deaths` | Total Deaths | number |  |

### chcz-j2du

**AH Deaths by Year, Sex, and Age for 2015-2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/chcz-j2du.json`
- Metadata: `GET https://data.cdc.gov/api/views/chcz-j2du.json`; page: https://data.cdc.gov/d/chcz-j2du
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `deaths`, `mortality`, `united states`, `yearly`, `age`, `age group`, `sex`, `all causes`
- Rows: 378. Data updated: 2021-03-25. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Death counts by age and sex for years 2015-2020. Data for 2015-2019 are final. Data for 2020 are provisional.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `year`, `sex`, `age_group`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `year` | Year | text |  |
| `sex` | Sex | text |  |
| `age_group` | Age Group | text |  |
| `total_deaths` | Total Deaths | number |  |

### m74n-4hbs

**AH Excess Deaths by Sex, Age, and Race and Hispanic Origin** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/m74n-4hbs.json`
- Metadata: `GET https://data.cdc.gov/api/views/m74n-4hbs.json`; page: https://data.cdc.gov/d/m74n-4hbs
- Topics: Category: National Center for Health Statistics
- Tags: `excess deaths`, `covid-19`, `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `weekly`, `age`, `age group`, `race`, `hispanic origin`, `sex`, `all causes`, `coronavirus`
- Rows: 174,637. Data updated: 2023-04-26. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Weekly data on the number of deaths from all causes by sex, age group, and race/Hispanic origin group for the United States. Counts of deaths in more recent weeks can be compared with counts from earlier years (2015-2019) to determine if the number is higher than expected.
- Sample row fields ($limit=1): `analysisdate`, `time_period`, `mmwryear`, `mmwrweek`, `weekending`, `raceethnicity`, `sex`, `agegroup`, `deaths_weighted`, `covid19_weighted`, `deaths_unweighted`, `covid19_unweighted`, `average_number_of_deaths`, `average_number_of_deaths_1`, `geography`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `analysisdate` | AnalysisDate | calendar_date | Date of analysis |
| `time_period` | Time Period | text | Time period |
| `mmwryear` | MMWRyear | text | MMWR year |
| `mmwrweek` | MMWRweek | number | MMWR week |
| `weekending` | Weekending | calendar_date | Week ending date |
| `raceethnicity` | RaceEthnicity | text | Race or Hispanic Origin group |
| `sex` | Sex | text | Sex |
| `agegroup` | AgeGroup | text | Age group |
| `deaths_weighted` | Deaths (weighted) | number | Deaths (weighted) |
| `covid19_weighted` | COVID19 (weighted) | number | COVID19 (weighted) |
| `deaths_unweighted` | Deaths (unweighted) | number | Deaths (unweighted) |
| `covid19_unweighted` | COVID19 (unweighted) | number | COVID19 (unweighted) |
| `average_number_of_deaths` | Average number of deaths (weighted) | number | Average number of deaths (weighted) |
| `average_number_of_deaths_1` | Average number of deaths (unweighted) | number | Average number of deaths (unweighted) |
| `number_above_average_weighted` | Number above average (weighted) | number | Number above average (weighted) |
| `percent_above_average_weighted` | Percent above average (weighted) | number | Percent above average (weighted) |
| `number_above_average` | Number above average (unweighted) | number | Number above average (unweighted) |
| `percent_above_average` | Percent above average (unweighted) | number | Percent above average (unweighted) |
| `footnote` | Footnote | text | Footnote |
| `geography` | Geography | text | Geography |

### w4jm-mysj

**AH Monthly COVID-19 Deaths, by Census Region, Age, Place, and Race and Hispanic Origin, 2020 Provisional** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/w4jm-mysj.json`
- Metadata: `GET https://data.cdc.gov/api/views/w4jm-mysj.json`; page: https://data.cdc.gov/d/w4jm-mysj
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `monthly`, `age group`, `age`, `race`, `hispanic origin`, `sex`, `covid-19`, `coronavirus`, `place of death`, `census region`
- Rows: 2,430. Data updated: 2020-10-12. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Deaths involving coronavirus disease 2019 (COVID-19) by month of death, region, age, place of death, and race and Hispanic origin: May-August 2020.
- Sample row fields ($limit=1): `date_of_death_year`, `date_of_death_month`, `region`, `agegroup`, `raceethnicity`, `covid_19_u071_multiple_cause`, `sex`, `place_of_death`, `analysisdate`, `note`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date_of_death_year` | Date Of Death Year | text |  |
| `date_of_death_month` | Date Of Death Month | text |  |
| `region` | Region | text |  |
| `agegroup` | AgeGroup | text |  |
| `raceethnicity` | RaceEthnicity | text |  |
| `covid_19_u071_multiple_cause` | COVID-19 (U071, Multiple Cause of Death) | number |  |
| `sex` | Sex | text |  |
| `place_of_death` | Place Of Death | text |  |
| `analysisdate` | AnalysisDate | text |  |
| `note` | Note | text |  |
| `flag_cov19mcod` | flag_cov19mcod | text |  |

### ezfr-g6hf

**AH Monthly Provisional Counts of Deaths by Age Group and HHS region for Select Causes of Death, 2019-2021** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ezfr-g6hf.json`
- Metadata: `GET https://data.cdc.gov/api/views/ezfr-g6hf.json`; page: https://data.cdc.gov/d/ezfr-g6hf
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `monthly`, `age`, `age group`, `all causes`, `causes of death`, `covid-19`, `coronavirus`, `natural cause`, `septicemia`, `cancer`, `diabetes`, `alzheimer disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `respiratory disease`, `kidney disease`, `diseases of heart`, `cerebrovascular disease`, `hhs region`
- Rows: 3,410. Data updated: 2021-08-25. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional counts of deaths by the month the deaths occurred, by age group and HHS region, for select underlying causes of death for 2019-2020. The dataset also includes monthly provisional counts of death for COVID-19, coded to ICD-10 code U07.1 as an underlying or multiple cause of death.
- Sample row fields ($limit=1): `date_of_death_year`, `date_of_death_month`, `hhsregion`, `agegroup`, `allcause`, `naturalcause`, `septicemia_a40_a41`, `malignant_neoplasms_c00_c97`, `alzheimer_disease_g30`, `influenza_and_pneumonia_j09`, `other_diseases_of_respiratory`, `symptoms_signs_and_abnormal`, `diseases_of_heart_i00_i09`, `covid_19_u071_multiple_cause`, `covid_19_u071_underlying`, `analysisdate`, `flag_diab`, `flag_clrd`, `flag_nephr`, `flag_stroke`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date_of_death_year` | Date Of Death Year | number | Death Year |
| `date_of_death_month` | Date Of Death Month | number | Death Month |
| `hhsregion` | HHSRegion | text | HHS Region |
| `agegroup` | AgeGroup | text | Age Group |
| `allcause` | AllCause | number | All Cause |
| `naturalcause` | NaturalCause | number | Natural Cause (A00-R99) |
| `septicemia_a40_a41` | Septicemia (A40-A41) | number | Septicemia (A40-A41) |
| `malignant_neoplasms_c00_c97` | Malignant neoplasms (C00-C97) | number | Malignant neoplasms (C00-C97) |
| `diabetes_mellitus_e10_e14` | Diabetes mellitus (E10-E14) | number | Diabetes mellitus (E10-E14) |
| `alzheimer_disease_g30` | Alzheimer disease (G30) | number | Alzheimer disease (G30) |
| `influenza_and_pneumonia_j09` | Influenza and pneumonia (J09-J18) | number | Influenza and pneumonia (J09-J18) |
| `chronic_lower_respiratory` | Chronic lower respiratory diseases (J40-J47) | number | Chronic lower respiratory diseases (J40-J47) |
| `other_diseases_of_respiratory` | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) | number | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) |
| `nephritis_nephrotic_syndrome` | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) | number | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) |
| `symptoms_signs_and_abnormal` | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) | number | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) |
| `diseases_of_heart_i00_i09` | Diseases of heart (I00-I09,I11,I13,I20-I51) | number | Diseases of heart (I00-I09,I11,I13,I20-I51) |
| `cerebrovascular_diseases` | Cerebrovascular diseases (I60-I69) | number | Cerebrovascular diseases (I60-I69) |
| `covid_19_u071_multiple_cause` | COVID-19 (U071, Multiple Cause of Death) | number | COVID-19 (U071, Multiple Cause of Death) |
| `covid_19_u071_underlying` | COVID-19 (U071, Underlying Cause of Death) | number | COVID-19 (U071, Underlying Cause of Death) |
| `analysisdate` | AnalysisDate | calendar_date | Date of analysis |
| `note` | Note | text | Note about incomplete data |
| `flag_allcause` | flag_allcause | text | Suppressed (counts 1-9) for All causes of death |
| `flag_natcause` | flag_natcause | text | Suppressed (counts 1-9) for Natural causes of death |
| `flag_sept` | flag_sept | text | Suppressed (counts 1-9) for Septicemia |
| `flag_neopl` | flag_neopl | text | Suppressed (counts 1-9) for Malignant eoplasms |
| `flag_diab` | flag_diab | text | Suppressed (counts 1-9) for Diabetes mellitis |
| `flag_alz` | flag_alz | text | Suppressed (counts 1-9) for Alzheimer disease |
| `flag_inflpn` | flag_inflpn | text | Suppressed (counts 1-9) for Influenza and pneumonia |
| `flag_clrd` | flag_clrd | text | Suppressed (counts 1-9) for Chronic lower respiratory diseases |
| `flag_otherresp` | flag_otherresp | text | Suppressed (counts 1-9) for Other diseases of respiratory system |
| `flag_nephr` | flag_nephr | text | Suppressed (counts 1-9) for Nephritis, nephrotic syndrome and nephrosis |
| `flag_otherunk` | flag_otherunk | text | Suppressed (counts 1-9) for Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified |
| `flag_hd` | flag_hd | text | Suppressed (counts 1-9) for Diseases of heart |
| `flag_stroke` | flag_stroke | text | Suppressed (counts 1-9) for Cerebrovascular diseases |
| `flag_cov19mcod` | flag_cov19mcod | text | Suppressed (counts 1-9) for COVID-19 (U071, Multiple Cause of Death) |
| `flag_cov19ucod` | flag_cov19ucod | text | Suppressed (counts 1-9) for COVID-19 (U071, Underlying Cause of Death) |

### r5pw-bk5t

**AH Monthly Provisional Counts of Deaths for Select Causes of Death by Age, and Race and Hispanic Origin** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/r5pw-bk5t.json`
- Metadata: `GET https://data.cdc.gov/api/views/r5pw-bk5t.json`; page: https://data.cdc.gov/d/r5pw-bk5t
- Topics: Category: National Center for Health Statistics
- Tags: `age`, `race`, `hispanic origin`, `monthly`, `nchs`, `nvss`, `age group`, `united states`, `mortality`, `coronavirus`, `covid-19`, `all causes`, `provisional`, `causes of death`, `deaths`, `natural cause`, `septicemia`, `cancer`, `diabetes`, `alzheimer disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `respiratory disease`, `kidney disease`, `diseases of heart`, `cerebrovascular disease`
- Rows: 1,800. Data updated: 2021-08-03. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional counts of deaths by the month the deaths occurred, by age group and race/ethnicity, for select underlying causes of death for 2020-2021. Final data is provided for 2019. The dataset also includes monthly provisional counts of death for COVID-19, coded to ICD-10 code U07.1 as an underlying or multiple cause of death.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `jurisdiction_of_occurrence`, `year`, `month`, `race_and_hispanic_origin`, `age_group`, `all_cause`, `natural_cause`, `septicemia`, `malignant_neoplasms`, `diabetes_mellitus`, `alzheimer_disease`, `influenza_and_pneumonia`, `chronic_lower_respiratory`, `other_diseases_of_respiratory`, `nephritis_nephrotic_syndrome`, `symptoms_signs_and_abnormal`, `diseases_of_heart`, `cerebrovascular_diseases`, `covid_19_multiple_cause_of`, `covid_19_underlying_cause`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Data as of |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text |  |
| `year` | Year | text | Death Year |
| `month` | Month | number | Death Month |
| `race_and_hispanic_origin` | Race and Hispanic Origin Group | text | Race and Hispanic Origin Group |
| `age_group` | Age Group | text | Age Group |
| `all_cause` | All Cause | number | All Cause |
| `natural_cause` | Natural Cause | number | Natural Cause (A00-R99) |
| `septicemia` | Septicemia | number | Septicemia (A40-A41) |
| `malignant_neoplasms` | Malignant Neoplasms | number | Malignant neoplasms (C00-C97) |
| `diabetes_mellitus` | Diabetes Mellitus | number | Diabetes mellitus (E10-E14) |
| `alzheimer_disease` | Alzheimer Disease | number | Alzheimer disease (G30) |
| `influenza_and_pneumonia` | Influenza and Pneumonia | number | Influenza and pneumonia (J09-J18) |
| `chronic_lower_respiratory` | Chronic Lower Respiratory Diseases | number | Chronic lower respiratory diseases (J40-J47) |
| `other_diseases_of_respiratory` | Other Diseases of Respiratory System | number | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) |
| `nephritis_nephrotic_syndrome` | Nephritis, Nephrotic Syndrome, and Nephrosis | number | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) |
| `symptoms_signs_and_abnormal` | Symptoms, Signs, and Abnormal Clinical and Laboratory Findings, Not Elsewhere Classified | number | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) |
| `diseases_of_heart` | Diseases of Heart | number | Diseases of heart (I00-I09,I11,I13,I20-I51) |
| `cerebrovascular_diseases` | Cerebrovascular Diseases | number | Cerebrovascular diseases (I60-I69) |
| `covid_19_multiple_cause_of` | COVID-19 (Multiple Cause of Death) | number | COVID-19 (U071, Multiple Cause of Death) |
| `covid_19_underlying_cause` | COVID-19 (Underlying Cause of Death) | number | COVID-19 (U071, Underlying Cause of Death) |

### 65mz-jvh5

**AH Monthly Provisional Counts of Deaths for Select Causes of Death by Sex, Age, and Race and Hispanic Origin** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/65mz-jvh5.json`
- Metadata: `GET https://data.cdc.gov/api/views/65mz-jvh5.json`; page: https://data.cdc.gov/d/65mz-jvh5
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `mortality`, `monthly`, `age group`, `sex`, `race`, `nchs`, `nvss`, `provisional`, `deaths`, `united states`, `age`, `hispanic origin`, `causes of death`, `all causes`, `coronavirus`, `natural cause`, `septicemia`, `cancer`, `diabetes`, `alzheimer disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `respiratory disease`, `kidney disease`, `diseases of heart`, `cerebrovascular disease`
- Rows: 3,960. Data updated: 2021-10-13. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional counts of deaths by the month the deaths occurred, by age group, sex, and race/ethnicity, for select underlying causes of death for 2020-2021. Final data are provided for 2019. The dataset also includes monthly provisional counts of death for COVID-19, coded to ICD-10 code U07.1 as an underlying or multiple cause of death.
- Sample row fields ($limit=1): `analysisdate`, `date_of_death_year`, `date_of_death_month`, `start_date`, `end_date`, `jurisdiction_of_occurrence`, `sex`, `race_ethnicity`, `agegroup`, `allcause`, `naturalcause`, `septicemia_a40_a41`, `malignant_neoplasms_c00_c97`, `diabetes_mellitus_e10_e14`, `alzheimer_disease_g30`, `influenza_and_pneumonia_j09`, `chronic_lower_respiratory`, `other_diseases_of_respiratory`, `nephritis_nephrotic_syndrome`, `symptoms_signs_and_abnormal`, `diseases_of_heart_i00_i09`, `cerebrovascular_diseases`, `covid_19_u071_multiple_cause`, `covid_19_u071_underlying`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `analysisdate` | AnalysisDate | text | Date of analysis |
| `date_of_death_year` | Date Of Death Year | number | Death Year |
| `date_of_death_month` | Date Of Death Month | number | Death Month |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text |  |
| `sex` | Sex | text | Sex |
| `race_ethnicity` | Race/Ethnicity | text | Race and Hispanic Origin |
| `agegroup` | AgeGroup | text | Age Group |
| `allcause` | AllCause | number | All Cause |
| `naturalcause` | NaturalCause | number | Natural Cause (A00-R99) |
| `septicemia_a40_a41` | Septicemia (A40-A41) | number | Septicemia (A40-A41) |
| `malignant_neoplasms_c00_c97` | Malignant neoplasms (C00-C97) | number | Malignant neoplasms (C00-C97) |
| `diabetes_mellitus_e10_e14` | Diabetes mellitus (E10-E14) | number | Diabetes mellitus (E10-E14) |
| `alzheimer_disease_g30` | Alzheimer disease (G30) | number | Alzheimer disease (G30) |
| `influenza_and_pneumonia_j09` | Influenza and pneumonia (J09-J18) | number | Influenza and pneumonia (J09-J18) |
| `chronic_lower_respiratory` | Chronic lower respiratory diseases (J40-J47) | number | Chronic lower respiratory diseases (J40-J47) |
| `other_diseases_of_respiratory` | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) | number | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) |
| `nephritis_nephrotic_syndrome` | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) | number | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) |
| `symptoms_signs_and_abnormal` | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) | number | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) |
| `diseases_of_heart_i00_i09` | Diseases of heart (I00-I09,I11,I13,I20-I51) | number | Diseases of heart (I00-I09,I11,I13,I20-I51) |
| `cerebrovascular_diseases` | Cerebrovascular diseases (I60-I69) | number | Cerebrovascular diseases (I60-I69) |
| `covid_19_u071_multiple_cause` | COVID-19 (U071, Multiple Cause of Death) | number | COVID-19 (U071, Multiple Cause of Death) |
| `covid_19_u071_underlying` | COVID-19 (U071, Underlying Cause of Death) | number | COVID-19 (U071, Underlying Cause of Death) |

### aie4-agrk

**AH Monthly Provisional COVID-19 Deaths, by Census Region, Age, and Race and Hispanic Origin** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/aie4-agrk.json`
- Metadata: `GET https://data.cdc.gov/api/views/aie4-agrk.json`; page: https://data.cdc.gov/d/aie4-agrk
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `monthly`, `age group`, `age`, `race`, `hispanic origin`, `sex`, `covid-19`, `coronavirus`, `place of death`, `united states`, `census region`
- Rows: 4,024. Data updated: 2020-09-11. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Deaths involving coronavirus disease 2019 (COVID-19) by month of death, region, age, place of death, and race and Hispanic origin.
- Sample row fields ($limit=1): `data_as_of`, `date_of_death_year`, `date_of_death_month`, `region`, `agegroup`, `raceethnicity`, `covid_19_u071_multiple_cause`, `sex`, `place_of_death`, `note1`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date |  |
| `date_of_death_year` | Date Of Death Year | number |  |
| `date_of_death_month` | Date Of Death Month | text |  |
| `region` | Region | text |  |
| `agegroup` | AgeGroup | text |  |
| `raceethnicity` | RaceEthnicity | text |  |
| `covid_19_u071_multiple_cause` | COVID-19 (U071, Multiple Cause of Death) | number |  |
| `sex` | Sex | text |  |
| `place_of_death` | Place Of Death | text |  |
| `note1` | Note1 | text |  |
| `note2` | Note2 | text |  |

### 2na8-fe6s

**AH Provisional Cancer Death Counts by Month and Year, 2020-2021** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/2na8-fe6s.json`
- Metadata: `GET https://data.cdc.gov/api/views/2na8-fe6s.json`; page: https://data.cdc.gov/d/2na8-fe6s
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `deaths`, `mortality`, `united states`, `monthly`, `sex`, `age`, `age group`, `cancer`, `race`, `hispanic origin`
- Rows: 2,816. Data updated: 2021-11-23. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional death counts of malignant neoplasms (cancer) by month and year, and other selected demographics, for 2020-2021. Data are based on death certificates for U.S. residents.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `country`, `year`, `month`, `sex`, `age_group`, `race_and_hispanic_origin`, `malignant_neoplasms_c00_c97`, `malignant_neoplasms_of_lip`, `malignant_neoplasm_of`, `malignant_neoplasm_of_stomach`, `malignant_neoplasms_of_colon`, `malignant_neoplasms_of_liver`, `malignant_neoplasm_of_pancreas`, `malignant_neoplasm_of_larynx`, `malignant_neoplasms_of_trachea`, `malignant_melanoma_of_skin`, `malignant_neoplasm_of_breast`, `malignant_neoplasm_of_cervix`, `malignant_neoplasms_of_corpus`, `malignant_neoplasm_of_ovary`, `malignant_neoplasm_of_prostate`, `malignant_neoplasms_of_kidney`, `malignant_neoplasm_of_bladder`, `malignant_neoplasms_of`, `malignant_neoplasms_of_1`, `all_other_and_unspecified`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `country` | Country | text | Jurisdiction of occurrence |
| `year` | Year | text | Year of reporting |
| `month` | Month | number | Month of reporting |
| `sex` | Sex | text | Sex |
| `age_group` | Age Group | text | Age group |
| `race_and_hispanic_origin` | Race and Hispanic Origin | text | Race and Hispanic Origin Group |
| `malignant_neoplasms_c00_c97` | Malignant neoplasms (C00-C97) | number | Malignant neoplasms (C00-C97) |
| `malignant_neoplasms_of_lip` | Malignant neoplasms of lip, oral cavity and pharynx (C00-C14) | number | Malignant neoplasms of lip, oral cavity and pharynx (C00-C14) |
| `malignant_neoplasm_of` | Malignant neoplasm of esophagus (C15) | number | Malignant neoplasm of esophagus (C15) |
| `malignant_neoplasm_of_stomach` | Malignant neoplasm of stomach (C16) | number | Malignant neoplasm of stomach (C16) |
| `malignant_neoplasms_of_colon` | Malignant neoplasms of colon, rectum and anus (C18-C21) | number | Malignant neoplasms of colon, rectum and anus (C18-C21) |
| `malignant_neoplasms_of_liver` | Malignant neoplasms of liver and intrahepatic bile ducts (C22) | number | Malignant neoplasms of liver and intrahepatic bile ducts (C22) |
| `malignant_neoplasm_of_pancreas` | Malignant neoplasm of pancreas (C25) | number | Malignant neoplasm of pancreas (C25) |
| `malignant_neoplasm_of_larynx` | Malignant neoplasm of larynx (C32) | number | Malignant neoplasm of larynx (C32) |
| `malignant_neoplasms_of_trachea` | Malignant neoplasms of trachea, bronchus and lung (C33-C34) | number | Malignant neoplasms of trachea, bronchus and lung (C33-C34) |
| `malignant_melanoma_of_skin` | Malignant melanoma of skin (C43) | number | Malignant melanoma of skin (C43) |
| `malignant_neoplasm_of_breast` | Malignant neoplasm of breast (C50) | number | Malignant neoplasm of breast (C50) |
| `malignant_neoplasm_of_cervix` | Malignant neoplasm of cervix uteri (C53) | number | Malignant neoplasm of cervix uteri (C53) |
| `malignant_neoplasms_of_corpus` | Malignant neoplasms of corpus uteri and uterus, part unspecified (C54-C55) | number | Malignant neoplasms of corpus uteri and uterus, part unspecified (C54-C55) |
| `malignant_neoplasm_of_ovary` | Malignant neoplasm of ovary (C56) | number | Malignant neoplasm of ovary (C56) |
| `malignant_neoplasm_of_prostate` | Malignant neoplasm of prostate (C61) | number | Malignant neoplasm of prostate (C61) |
| `malignant_neoplasms_of_kidney` | Malignant neoplasms of kidney and renal pelvis (C64-C65) | number | Malignant neoplasms of kidney and renal pelvis (C64-C65) |
| `malignant_neoplasm_of_bladder` | Malignant neoplasm of bladder (C67) | number | Malignant neoplasm of bladder (C67) |
| `malignant_neoplasms_of` | Malignant neoplasms of meninges, brain and other parts of central nervous system (C70-C72) | number | Malignant neoplasms of meninges, brain and other parts of central nervous system (C70-C72) |
| `malignant_neoplasms_of_1` | Malignant neoplasms of lymphoid, hematopoietic and related tissue (C81-C96) | number | Malignant neoplasms of lymphoid, hematopoietic and related tissue (C81-C96) |
| `all_other_and_unspecified` | All other and unspecified malignant neoplasms (C17,C23-C24,C26-C31,C37-C41,C44-C49,C51-C52,C57-C60,C62-C63,C66,C68-C69,C73-C80,C97) | number | All other and unspecified malignant neoplasms (C17,C23-C24,C26-C31,C37-C41,C44-C49,C51-C52,C57-C60,C62-C63,C66,C68-C69,C73-C80,C97) |

### dnhi-s2bf

**AH Provisional COVID-19 Death Counts by Quarter and County** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/dnhi-s2bf.json`
- Metadata: `GET https://data.cdc.gov/api/views/dnhi-s2bf.json`; page: https://data.cdc.gov/d/dnhi-s2bf
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `deaths`, `mortality`, `provisional`, `united states`, `county`, `quarterly`, `covid-19`, `coronavirus`, `all causes`
- Rows: 18,876. Data updated: 2021-10-06. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional counts of deaths involving coronavirus disease 2019 (COVID-19) by quarter and county of residence, in the United States, 2020-2021.
- Sample row fields ($limit=1): `data_as_of`, `year`, `quarter`, `state_of_residence`, `county_of_residence`, `fips_state`, `fips_county`, `fips_code`, `urban_rural_code`, `covid_19_deaths`, `footnote`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Analysis Date |
| `year` | Year | text | Year of reporting |
| `quarter` | Quarter | number | Quarter of reporting |
| `state_of_residence` | State of Residence | text | State of Residence |
| `county_of_residence` | County of Residence | text | County of Residence |
| `fips_state` | FIPS State | text | FIPS state code |
| `fips_county` | FIPS County | text | FIPS county code |
| `fips_code` | FIPS Code | text | FIPS state and county code |
| `urban_rural_code` | Urban Rural Code | text | Urban-rural classification is based on the 2013 National Center for Health Statistics Urban-Rural Classification Scheme for Counties |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-10 code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `footnote` | Footnote | text | Suppressed counts (1-9) |

### siwp-yg6m

**AH Provisional COVID-19 Death Counts by Week, Race, and Age, United States 2020-2023** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/siwp-yg6m.json`
- Metadata: `GET https://data.cdc.gov/api/views/siwp-yg6m.json`; page: https://data.cdc.gov/d/siwp-yg6m
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `weekly`, `age`, `age group`, `race`, `hispanic origin`, `coronavirus`, `covid-19`, `all causes`, `children`
- Rows: 14,000. Data updated: 2023-05-10. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional deaths involving COVID-19 reported to NCHS by MMWR week, race and Hispanic origin, and age group. Deaths occurred in the United States. Age groups: 0-4, 5-11, 12-17, 18-29, 30-39, 40-49, 50-64, 65-74, and 75+ years
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `year`, `mmwr_week`, `week_ending_date`, `jurisdiction_of_occurrence`, `race_and_hispanic_origin`, `age_group`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `year` | Year | text | Year of reporting |
| `mmwr_week` | MMWR Week | text | MMWR week of reporting |
| `week_ending_date` | Week-Ending Date | calendar_date | Week-ending date for the week of reporting |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text | Jurisdiction of occurrence |
| `race_and_hispanic_origin` | Race and Hispanic Origin Group | text | Race and Hispanic origin group |
| `age_group` | Age Group | text | Age group |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-10 code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |

### tdmv-axfy

**AH Provisional COVID-19 Deaths and Contributing Conditions by Sex, Race and Hispanic Origin, and Age, 2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/tdmv-axfy.json`
- Metadata: `GET https://data.cdc.gov/api/views/tdmv-axfy.json`; page: https://data.cdc.gov/d/tdmv-axfy
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `mortality`, `deaths`, `united states`, `provisional`, `health conditions`, `covid-19`, `coronavirus`, `sex`, `age`, `age group`, `race`, `hispanic origin`, `septicemia`, `cancer`, `diabetes`, `alzheimer disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `respiratory disease`, `kidney disease`, `circulatory disease`, `hypertensive disease`, `cerebrovascular disease`
- Rows: 80. Data updated: 2021-04-15. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: This dataset shows health conditions and contributing causes mentioned in conjunction with deaths involving coronavirus disease 2019 (COVID-19), by sex, race and Hispanic origin, and age group, for 2020.
- Sample row fields ($limit=1): `data_as_of`, `jurisdiction_of_occurrence`, `year`, `sex`, `race_and_hispanic_origin`, `age_group`, `covid_u071_multiple_cause`, `alzheimer_disease`, `other_diseases_of_respiratory`, `circulatory_diseases`, `flag_sept`, `flag_neopl`, `flag_diab`, `flag_inflpn`, `flag_clrd`, `flag_nephr`, `flag_otherunk`, `flag_hypt`, `flag_stroke`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of Analysis |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text |  |
| `year` | Year | text |  |
| `sex` | Sex | text |  |
| `race_and_hispanic_origin` | Race and Hispanic Origin | text |  |
| `age_group` | Age Group | text |  |
| `covid_u071_multiple_cause` | COVID (U071, Multiple Cause of Death) | number | COVID-19 (U071, Multiple Cause of Death) |
| `septicemia` | Septicemia | number | Septicemia (A40-A41) |
| `malignant_neoplasms` | Malignant Neoplasms | number | Malignant neoplasms (C00-C97) |
| `diabetes_mellitus` | Diabetes Mellitus | number | Diabetes mellitus (E10-E14) |
| `alzheimer_disease` | Alzheimer Disease | number | Alzheimer disease (G30) |
| `influenza_and_pneumonia` | Influenza and Pneumonia | number | Influenza and pneumonia (J09-J18) |
| `chronic_lower_respiratory` | Chronic Lower Respiratory Diseases | number | Chronic lower respiratory diseases (J40-J47) |
| `other_diseases_of_respiratory` | Other Diseases of Respiratory System | number | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) |
| `nephritis_nephrotic_syndrom` | Nephritis, Nephrotic Syndrom, and Nephrosis | number | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) |
| `symptoms_signs_and_abnormal` | Symptoms, Signs, and Abnormal Clinical and Laboratory Findings, Not Elsewhere Classified | number | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) |
| `circulatory_diseases` | Circulatory Diseases | number | Circulatory Diseases (I00-I15, I20-I52, I60-I99) |
| `hypertensive_diseases` | Hypertensive Diseases | number | Hypertensive Diseases (I10-I15) |
| `cerebrovascular_diseases` | Cerebrovascular Diseases | number | Cerebrovascular diseases (I60-I69) |
| `flag_covid` | flag_covid | text | Suppressed (counts 1-9) for COVID-19 (U071, Multiple Cause of Death) |
| `flag_sept` | flag_sept | text | Suppressed (counts 1-9) for Septicemia |
| `flag_neopl` | flag_neopl | text | Suppressed (counts 1-9) for Malignant neoplasms |
| `flag_diab` | flag_diab | text | Suppressed (counts 1-9) for Diabetes mellitis |
| `flag_alz` | flag_alz | text | Suppressed (counts 1-9) for Alzheimer disease |
| `flag_inflpn` | flag_inflpn | text | Suppressed (counts 1-9) for Influenza and pneumonia |
| `flag_clrd` | flag_clrd | text | Suppressed (counts 1-9) for Chronic lower respiratory diseases |
| `flag_otherresp` | flag_otherresp | text | Suppressed (counts 1-9) for Other diseases of respiratory system |
| `flag_nephr` | flag_nephr | text | Suppressed (counts 1-9) for Nephritis, nephrotic syndrome and nephrosis |
| `flag_otherunk` | flag_otherunk | text | Suppressed (counts 1-9) for Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified |
| `flag_circ` | flag_circ | text | Suppressed (counts 1-9) for Circulatory Diseases |
| `flag_hypt` | flag_hypt | text | Suppressed (counts 1-9) for Hypertensive Diseases |
| `flag_stroke` | flag_stroke | text | Suppressed (counts 1-9) for Cerebrovascular diseases |

### mawz-airi

**AH Provisional COVID-19 Deaths by Age, United States, Week 40 2020 through Week 39 2021** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/mawz-airi.json`
- Metadata: `GET https://data.cdc.gov/api/views/mawz-airi.json`; page: https://data.cdc.gov/d/mawz-airi
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `deaths`, `mortality`, `provisional`, `united states`, `coronavirus`, `covid-19`, `age group`, `age`, `all causes`
- Rows: 10. Data updated: 2021-11-10. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional deaths involving coronavirus disease 2019 (COVID-19) reported to NCHS by age group among United States residents, from MMWR Week 40 2020 through MMWR Week 39 2021. Age groups: 0-4, 5-11, 12-15, 16-17, 18-24, 25-39, 40-49, 50-64, 65-74, and 75+ years
- Sample row fields ($limit=1): `data_as_of`, `year`, `start_week`, `end_week`, `jurisdiction_of_residence`, `age_group`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Analysis date |
| `year` | Year | text | Year of reporting |
| `start_week` | Start Week | calendar_date | First week-ending date of reporting period |
| `end_week` | End Week | calendar_date | Last week-ending date of reporting period |
| `jurisdiction_of_residence` | Jurisdiction of Residence | text | Jurisdiction of residence |
| `age_group` | Age Group | text | Age group |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-10 code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |

### xmrr-rw5u

**AH Provisional COVID-19 Deaths by County and Age for 2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/xmrr-rw5u.json`
- Metadata: `GET https://data.cdc.gov/api/views/xmrr-rw5u.json`; page: https://data.cdc.gov/d/xmrr-rw5u
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `mortality`, `deaths`, `yearly`, `county`, `age`, `age group`, `covid-19`, `coronavirus`, `all causes`, `provisional`, `united states`, `sdoh-environmental`
- Rows: 40,820. Data updated: 2021-04-28. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional counts of deaths involving coronavirus disease 2019 (COVID-19) by United States county of residence and age group, from January 1, 2020 through December 31, 2020.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `year`, `state`, `county`, `fips_state`, `fips_county`, `fips_code`, `urban_rural_code`, `age_group`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `year` | Year | text |  |
| `state` | State | text |  |
| `county` | County | text |  |
| `fips_state` | FIPS State | text |  |
| `fips_county` | FIPS County | text |  |
| `fips_code` | FIPS Code | text |  |
| `urban_rural_code` | Urban Rural Code | text |  |
| `age_group` | Age Group | text |  |
| `covid_19_deaths` | COVID-19 Deaths | number |  |
| `total_deaths` | Total Deaths | number |  |
| `footnote` | Footnote | text |  |

### 3ts8-hsrw

**AH Provisional COVID-19 Deaths by Educational Attainment, Race, Sex, and Age** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3ts8-hsrw.json`
- Metadata: `GET https://data.cdc.gov/api/views/3ts8-hsrw.json`; page: https://data.cdc.gov/d/3ts8-hsrw
- Topics: Category: National Center for Health Statistics
- Tags: `education`, `race`, `age`, `sex`, `covid-19`, `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `age group`, `hispanic origin`, `coronavirus`, `all causes`, `sdoh-high-school`, `sdoh-higher-education`
- Rows: 224. Data updated: 2021-02-03. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional counts of deaths in the United States by educational attainment, race, sex, and age group. The dataset includes cumulative provisional counts of death for COVID-19, coded to ICD-10 code U07.1 as an underlying or multiple cause of death.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `education_level`, `race_or_hispanic_origin`, `sex`, `age_group`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `education_level` | Education Level | text |  |
| `race_or_hispanic_origin` | Race or Hispanic Origin | text |  |
| `sex` | Sex | text |  |
| `age_group` | Age Group | text |  |
| `covid_19_deaths` | COVID-19 Deaths | number |  |
| `total_deaths` | Total Deaths | number |  |

### 9xc7-3a4q

**AH Provisional COVID-19 Deaths by HHS Region, Race, Age 65plus** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/9xc7-3a4q.json`
- Metadata: `GET https://data.cdc.gov/api/views/9xc7-3a4q.json`; page: https://data.cdc.gov/d/9xc7-3a4q
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `race`, `hispanic origin`, `age`, `deaths`, `nchs`, `nvss`, `provisional`, `coronavirus`, `age group`, `weekly`, `all causes`, `mortality`, `united states`, `hhs region`
- Rows: 64,750. Data updated: 2022-10-28. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Deaths involving coronavirus disease 2019 (COVID-19) reported to NCHS by time-period, HHS region, race and Hispanic origin, and age groups (<65, 65-74. 75-84, 85+, and 65+). United States death counts include the 50 states, plus the District of Columbia and New York City. The ten (10) United States Department of Health and Human Services (HHS) regions include the following jurisdictions. Region 1: Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont; Region 2: New Jersey, New York, New York City; Region 3: Delaware, District of Columbia, Maryland, Pennsylvania, Virginia, We…
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `group`, `year`, `mmwr_week`, `week_ending_date`, `hhs_region`, `race_and_hispanic_origin`, `age_group`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `group` | Group | text |  |
| `year` | Year | text |  |
| `month` | Month | number |  |
| `mmwr_week` | MMWR Week | number |  |
| `week_ending_date` | Week-Ending Date | calendar_date |  |
| `hhs_region` | HHS Region | number |  |
| `race_and_hispanic_origin` | Race and Hispanic Origin Group | text |  |
| `age_group` | Age Group | text |  |
| `covid_19_deaths` | COVID-19 Deaths | number |  |
| `total_deaths` | Total Deaths | number |  |
| `footnote` | Footnote | text |  |

### q85u-gmyc

**AH Provisional COVID-19 Deaths by HHS Region, Race, and Age Group, 2020-2021** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/q85u-gmyc.json`
- Metadata: `GET https://data.cdc.gov/api/views/q85u-gmyc.json`; page: https://data.cdc.gov/d/q85u-gmyc
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `mortality`, `deaths`, `provisional`, `coronavirus`, `covid-19`, `united states`, `hhs region`, `weekly`, `monthly`, `yearly`, `puerto rico`, `age`, `age group`, `race`, `hispanic origin`, `all causes`
- Rows: 28,776. Data updated: 2021-08-26. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional deaths involving coronavirus disease 2019 (COVID-19) reported to NCHS by time-period (week, month, year), HHS region, race and Hispanic origin, and age group (0-24, 25-64, 65+ years) for 2020-2021. United States death counts include the 50 states, plus the District of Columbia and New York City. The ten (10) United States Department of Health and Human Services (HHS) regions include the following jurisdictions. Region 1: Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont; Region 2: New Jersey, New York, New York City, Puerto Rico; Region 3: Delaware, District…
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `group`, `year`, `mmwr_week`, `week_ending_date`, `hhs_region`, `race_and_hispanic_origin`, `age_group`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `group` | Group | text | Time period of reporting |
| `year` | Year | text | Year of reporting |
| `month` | Month | text | Month of reporting |
| `mmwr_week` | MMWR Week | number | MMWR week of reporting |
| `week_ending_date` | Week-Ending Date | calendar_date | Week-ending date for the week of reporting |
| `hhs_region` | HHS Region | text | HHS Region |
| `race_and_hispanic_origin` | Race and Hispanic Origin Group | text | Race and Hispanic Origin Group |
| `age_group` | Age Group | text | Age Group |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `footnote` | Footnote | text | Suppressed counts (1-9) |

### k5dc-apj8

**AH Provisional COVID-19 Deaths by HHS Region, Race, and Age, 2015 to date** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/k5dc-apj8.json`
- Metadata: `GET https://data.cdc.gov/api/views/k5dc-apj8.json`; page: https://data.cdc.gov/d/k5dc-apj8
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `race`, `hispanic origin`, `age`, `deaths`, `nchs`, `nvss`, `provisional`, `coronavirus`, `age group`, `weekly`, `all causes`, `mortality`, `united states`, `puerto rico`, `hhs region`, `children`
- Rows: 456,896. Data updated: 2022-03-23. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Deaths from all causes and deaths involving coronavirus disease 2019 (COVID-19) reported to NCHS by time-period, HHS region, race and Hispanic origin, and age group. United States death counts include the 50 states, plus the District of Columbia and New York City. The ten (10) United States Department of Health and Human Services (HHS) regions include the following jurisdictions. Region 1: Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont; Region 2: New Jersey, New York, New York City, Puerto Rico; Region 3: Delaware, District of Columbia, Maryland, Pennsylvania, Virgini…
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `group`, `year`, `mmwr_week`, `week_ending_date`, `hhs_region`, `race_and_hispanic_origin`, `age_group`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `group` | Group | text |  |
| `year` | Year | text |  |
| `month` | Month | text |  |
| `mmwr_week` | MMWR Week | number |  |
| `week_ending_date` | Week-Ending Date | calendar_date |  |
| `hhs_region` | HHS Region | text |  |
| `race_and_hispanic_origin` | Race and Hispanic Origin Group | text |  |
| `age_group` | Age Group | text |  |
| `covid_19_deaths` | COVID-19 Deaths | number |  |
| `total_deaths` | Total Deaths | number |  |
| `footnote` | Footnote | text |  |

### xy7w-35q7

**AH Provisional COVID-19 Deaths by HHS Region, Race, and Age, 2015-2021** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/xy7w-35q7.json`
- Metadata: `GET https://data.cdc.gov/api/views/xy7w-35q7.json`; page: https://data.cdc.gov/d/xy7w-35q7
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `deaths`, `mortality`, `united states`, `hhs region`, `age`, `age group`, `race`, `hispanic origin`, `weekly`, `all causes`, `covid-19`, `coronavirus`
- Rows: 110,323. Data updated: 2021-09-15. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional deaths involving coronavirus disease 2019 (COVID-19) and deaths from all causes reported to NCHS by week the death occurred, HHS region of occurrence, race and Hispanic origin, and age group (0-24, 25-64, 65+ years), from 2015-2021. United States death counts include the 50 states, plus the District of Columbia and New York City. The ten (10) United States Department of Health and Human Services (HHS) regions include the following jurisdictions. Region 1: Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont; Region 2: New Jersey, New York, New York City; Region…
- Sample row fields ($limit=1): `analysisdate`, `hhs_region`, `raceethnicity`, `agegroup`, `mmwryear`, `mmwrweek`, `weekendingdate`, `covid_19_u071_multiple_cause`, `covid_19_u071_underlying`, `flag_allcause`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `analysisdate` | AnalysisDate | calendar_date | Date of analysis |
| `hhs_region` | HHS Region | text | HHS Region |
| `raceethnicity` | RaceEthnicity | text | Race and Hispanic Origin Group |
| `agegroup` | AgeGroup | text | Age Group |
| `mmwryear` | MMWRyear | text | MMWR Year |
| `mmwrweek` | MMWRweek | number | MMWR Week |
| `weekendingdate` | WeekEndingDate | calendar_date | Week-Ending Date |
| `allcause` | AllCause | number | Deaths from all causes of death |
| `covid_19_u071_multiple_cause` | COVID-19 (U071, Multiple Cause of Death) | number | COVID-19 (U071, Multiple Cause of Death) |
| `covid_19_u071_underlying` | COVID-19 (U071,Underlying Cause of Death) | number | COVID-19 (U071, Underlying Cause of Death) |
| `flag_allcause` | flag_allcause | text | Suppressed (counts 1-9) for All causes of death |
| `flag_covidmcod` | flag_covidmcod | text | Suppressed (counts 1-9) for COVID-19 (U071, Multiple Cause of Death) |
| `flag_coviducod` | flag_coviducod | text | Suppressed (counts 1-9) for COVID-19 (U071, Underlying Cause of Death) |

### mqmc-4b9n

**AH Provisional COVID-19 Deaths by Hospital Referral Region** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/mqmc-4b9n.json`
- Metadata: `GET https://data.cdc.gov/api/views/mqmc-4b9n.json`; page: https://data.cdc.gov/d/mqmc-4b9n
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `deaths`, `mortality`, `covid-19`, `coronavirus`, `hospital referral region`, `all causes`, `nvss`, `weekly`, `provisional`, `united states`, `sdoh-access-to-health-care`
- Rows: 138,618. Data updated: 2023-11-16. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional count of deaths involving coronavirus disease 2019 (COVID-19) in the United States by week of death and by hospital referral region (HRR). HRR is determined by county of occurrence. Weekly weighted counts of deaths from all causes and due to COVID-19 are provided by HRR overall and for decedents 65 years and older. The weighted counts by HRRs are based on published methods for aggregating county-level data to HRRs. More detail about aggregating to HRRs from counties can be found in the following: https://github.com/Dartmouth-DAC/covid-19-hrr-mapping https://dartmouthatlas.org/covi…
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `mmwr_year`, `mmwr_week`, `week_ending_date`, `hrr_name`, `hrr_number`, `state`, `total_deaths`, `covid_19_deaths`, `covid_19_deaths_over_65_years`, `covid_19_deaths_65_to_74_years`, `covid_19_deaths_75_to_84_years`, `covid_19_deaths_over_85_years`, `footnote`, `accuracy_index`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date | First week included |
| `end_date` | End Date | calendar_date | Last week included |
| `mmwr_year` | MMWR Year | text | Year |
| `mmwr_week` | MMWR Week | number | MMWR Week number |
| `week_ending_date` | Week Ending Date | calendar_date | Week ending date |
| `hrr_name` | HRR Name | text | Hospital Referral Regions (HRR) Name |
| `hrr_number` | HRR Number | number | Hospital Referral Regions (HRR) Number |
| `state` | State | text | State |
| `total_deaths` | Total Deaths | number | Total Deaths |
| `covid_19_deaths` | COVID-19 Deaths | number | COVID-19 Deaths |
| `total_deaths_over_65_years` | Total Deaths over 65 years | number | Total Deaths over 65 years |
| `covid_19_deaths_over_65_years` | COVID-19 Deaths over 65 years | number | COVID-19 Deaths over 65 years |
| `total_deaths_65_to_74_years` | Total Deaths 65 to 74 years | number | Total number of deaths among 65 to 74 years |
| `covid_19_deaths_65_to_74_years` | COVID-19 Deaths 65 to 74 years | number | COVID-19 deaths among 65 to 74 years |
| `total_deaths_75_to_84_years` | Total Deaths 75 to 84 years | number | Total deaths among 75 to 84 years |
| `covid_19_deaths_75_to_84_years` | COVID-19 Deaths 75 to 84 years | number | COVID-19 deaths among 75 to 84 years |
| `total_deaths_over_85_years` | Total Deaths over 85 years | number | Total deaths among 85 years and older |
| `covid_19_deaths_over_85_years` | COVID-19 Deaths over 85 years | number | COVID-19 deaths among 85 years and older |
| `footnote` | Footnote | text | Footnote |
| `accuracy_index` | Accuracy_index | number | A weighted average of the proportions of the county populations that fall within an HRR |

### ypxr-mz8e

**AH Provisional COVID-19 Deaths by Quarter, County and Age for 2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ypxr-mz8e.json`
- Metadata: `GET https://data.cdc.gov/api/views/ypxr-mz8e.json`; page: https://data.cdc.gov/d/ypxr-mz8e
- Topics: Category: National Center for Health Statistics
- Tags: `nvss`, `nchs`, `provisional`, `mortality`, `deaths`, `quarterly`, `county`, `united states`, `covid-19`, `coronavirus`, `all causes`, `age group`, `age`, `sdoh-environmental`
- Rows: 125,600. Data updated: 2022-06-17. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional counts of deaths involving coronavirus disease 2019 (COVID-19) by United States county of residence and age group, for 2020 by quarter.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `year`, `quarter`, `state`, `county`, `fips_state`, `fips_county`, `fips_code`, `urban_rural_code`, `age_group`, `covid_19_deaths`, `footnote`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `year` | Year | text |  |
| `quarter` | Quarter | number |  |
| `state` | State | text |  |
| `county` | County | text |  |
| `fips_state` | FIPS State | text |  |
| `fips_county` | FIPS County | text |  |
| `fips_code` | FIPS Code | text |  |
| `urban_rural_code` | Urban Rural Code | text |  |
| `age_group` | Age Group | text |  |
| `covid_19_deaths` | COVID-19 Deaths | number |  |
| `total_deaths` | Total Deaths | number |  |
| `footnote` | Footnote | text |  |

### i6ej-9eac

**AH Provisional COVID-19 Deaths by Race and Educational Attainment** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/i6ej-9eac.json`
- Metadata: `GET https://data.cdc.gov/api/views/i6ej-9eac.json`; page: https://data.cdc.gov/d/i6ej-9eac
- Topics: Category: National Center for Health Statistics
- Tags: `race`, `education`, `covid-19`, `deaths`, `hispanic origin`, `coronavirus`, `all causes`, `nchs`, `nvss`, `provisional`, `mortality`, `united states`, `sdoh-high-school`, `sdoh-higher-education`
- Rows: 72. Data updated: 2021-02-02. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional counts of deaths in the United States by race and educational attainment. The dataset includes cumulative provisional counts of death for COVID-19, coded to ICD-10 code U07.1 as an underlying or multiple cause of death.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `education_level`, `race_or_hispanic_origin`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `education_level` | Education Level | text |  |
| `race_or_hispanic_origin` | Race or Hispanic Origin | text |  |
| `covid_19_deaths` | COVID-19 Deaths | number |  |
| `total_deaths` | Total Deaths | number |  |

### s9qn-46pq

**AH Provisional COVID-19 Deaths By Race, Age, and Sex from 3/1/2020 to 7/31/2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/s9qn-46pq.json`
- Metadata: `GET https://data.cdc.gov/api/views/s9qn-46pq.json`; page: https://data.cdc.gov/d/s9qn-46pq
- Topics: Category: National Center for Health Statistics
- Tags: `race`, `age`, `sex`, `deaths`, `covid-19`, `nchs`, `nvss`, `mortality`, `provisional`, `united states`, `age group`, `hispanic origin`, `coronavirus`, `all causes`
- Rows: 98. Data updated: 2021-02-01. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional counts of deaths in the United States by age group, sex, and race/ethnicity, from March-July 2020. The dataset includes cumulative provisional counts of death for COVID-19, coded to ICD-10 code U07.1 as an underlying or multiple cause of death.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `race_or_hispanic_origin`, `sex`, `age_group`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `race_or_hispanic_origin` | Race or Hispanic Origin | text |  |
| `sex` | Sex | text |  |
| `age_group` | Age Group | text |  |
| `covid_19_deaths` | COVID-19 Deaths | number |  |
| `total_deaths` | Total Deaths | number |  |

### ikd3-vynf

**AH Provisional COVID-19 Deaths by Week and Age** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ikd3-vynf.json`
- Metadata: `GET https://data.cdc.gov/api/views/ikd3-vynf.json`; page: https://data.cdc.gov/d/ikd3-vynf
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `deaths`, `mortality`, `united states`, `state`, `weekly`, `covid-19`, `coronavirus`, `all causes`, `age`, `age group`
- Rows: 43,460. Data updated: 2021-08-02. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Deaths involving coronavirus disease 2019 (COVID-19) reported to NCHS by jurisdiction of occurrence, week, and age group.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `mmwr_year`, `mmwr_week`, `week_ending_date`, `state`, `age_group`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `mmwr_year` | MMWR Year | text |  |
| `mmwr_week` | MMWR Week | number |  |
| `week_ending_date` | Week-Ending Date | calendar_date |  |
| `state` | State | text |  |
| `age_group` | Age Group | text |  |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `footnote` | Footnote | text |  |

### 6mjs-pnrx

**AH Provisional COVID-19 Deaths by Week and Age** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/6mjs-pnrx.json`
- Metadata: `GET https://data.cdc.gov/api/views/6mjs-pnrx.json`; page: https://data.cdc.gov/d/6mjs-pnrx
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `deaths`, `mortality`, `provisional`, `united states`, `weekly`, `covid-19`, `coronavirus`, `all causes`
- Rows: 50. Data updated: 2022-08-30. Probe status: 200.
- Update frequency: irregular.
- Description: Provisional counts of deaths involving coronavirus disease 2019 (COVID-19) by week and age group, in the United States.
- Sample row fields ($limit=1): `data_as_of`, `state`, `mmwr_week`, `end_week`, `age_group`, `total_deaths`, `covid_19_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Analysis Date |
| `state` | State | text | State of Occurrence |
| `mmwr_week` | MMWR Week | number | MMWR Week |
| `end_week` | End Week | calendar_date | End Week |
| `age_group` | Age Group | text | Age Group |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `covid_19_deaths` | COVID-19 Deaths | number | COVID-19 Deaths |

### g7hk-rc8d

**AH Provisional COVID-19 Deaths by Week, Place of Death, and Age** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/g7hk-rc8d.json`
- Metadata: `GET https://data.cdc.gov/api/views/g7hk-rc8d.json`; page: https://data.cdc.gov/d/g7hk-rc8d
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `weekly`, `place of death`, `age group`, `age`, `covid-19`, `coronavirus`
- Rows: 4,800. Data updated: 2021-06-08. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional death counts of COVID-19 deaths by place of death, week, and age. Data source: National Center for Health Statistics National Vital Statistics System. Provisional data for 2020-2021.
- Sample row fields ($limit=1): `data_as_of`, `start_week`, `end_week`, `mmwr_week_number`, `week_ending_date`, `jurisdiction_of_occurrence`, `place_of_death`, `age_group`, `covid_19_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Date of analysis |
| `start_week` | Start Date | calendar_date | First date of data period |
| `end_week` | End Date | calendar_date | Last date of data period |
| `mmwr_week_number` | MMWR Week | number | MMWR week of reporting |
| `week_ending_date` | Week Ending Date | calendar_date | Week-ending date for the week of reporting |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text | Jurisdiction of occurrence |
| `place_of_death` | Place Of Death | text | Place of death |
| `age_group` | Age Group | text | Age group |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-10 code U07.1) |

### 9z9x-g48e

**AH Provisional COVID-19 Deaths by Week, Sex, and Race and Hispanic Origin** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/9z9x-g48e.json`
- Metadata: `GET https://data.cdc.gov/api/views/9z9x-g48e.json`; page: https://data.cdc.gov/d/9z9x-g48e
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `deaths`, `mortality`, `covid-19`, `coronavirus`, `all causes`, `sex`, `weekly`, `united states`, `race`, `hispanic origin`
- Rows: 1,456. Data updated: 2021-09-30. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Deaths involving coronavirus disease 2019 (COVID-19) reported to NCHS by week, sex, and race and Hispanic origin. Deaths occurred in the United States.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `mmwr_year`, `mmwr_week`, `week_ending_date`, `jurisdiction_of_occurrence`, `sex`, `race_and_hispanic_origin`, `covid_19_underlying_cause`, `covid_19_multiple_cause_of`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `mmwr_year` | MMWR Year | text |  |
| `mmwr_week` | MMWR Week | number |  |
| `week_ending_date` | Week-Ending Date | calendar_date |  |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text |  |
| `sex` | Sex | text |  |
| `race_and_hispanic_origin` | Race and Hispanic Origin Group | text |  |
| `covid_19_underlying_cause` | COVID-19 (Underlying Cause of Death) | number |  |
| `covid_19_multiple_cause_of` | COVID-19 (Multiple Cause of Death) | number |  |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |

### 7873-6w4v

**AH Provisional COVID-19 Deaths Counts by Health Service Area** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/7873-6w4v.json`
- Metadata: `GET https://data.cdc.gov/api/views/7873-6w4v.json`; page: https://data.cdc.gov/d/7873-6w4v
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `deaths`, `health service area`, `nchs`, `mortality`, `coronavirus`, `yearly`, `nvss`, `all causes`, `provisional`, `united states`
- Rows: 950. Data updated: 2021-03-09. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional count of deaths involving coronavirus disease 2019 (COVID-19) in the United States by health service area. Health service area is determined by the decedent's county of residence.
- Sample row fields ($limit=1): `data_as_of`, `year`, `hsa_nci`, `hsa_description`, `total_deaths`, `covid19_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Data as of |
| `year` | Year | text | Year of death |
| `hsa_nci` | HSA_NCI | number | Health Service Area (NCI modified) |
| `hsa_description` | Health.Service.Area.Description | text | Health Service Area Description |
| `total_deaths` | Total Number of Deaths | number | Total Number of Deaths |
| `covid19_deaths` | Number of COVID19 Deaths | number | Number of COVID19 Deaths |
| `suppress` | Footnote | text | Suppressed counts 1-9 |

### qdcb-uzft

**AH Provisional Diabetes Death Counts for 2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/qdcb-uzft.json`
- Metadata: `GET https://data.cdc.gov/api/views/qdcb-uzft.json`; page: https://data.cdc.gov/d/qdcb-uzft
- Topics: Category: National Center for Health Statistics
- Tags: `diabetes`, `covid-19`, `mortality`, `nchs`, `nvss`, `provisional`, `deaths`, `united states`, `monthly`, `age group`, `sex`, `coronavirus`, `causes of death`, `age`, `chronic lower respiratory disease`, `kidney disease`, `chronic liver disease`, `cirrhosis`, `obesity`, `major cardiovascular diseases`, `hypertensive disease`
- Rows: 226. Data updated: 2020-10-21. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional death counts of diabetes, coronavirus disease 2019 (COVID-19) and other select causes of death, by month, sex, and age.
- Sample row fields ($limit=1): `data_as_of`, `death_year`, `death_month`, `agegroup`, `sex`, `covid19`, `diabetes_uc`, `diabetes_mc`, `c19plusdiabetes`, `c19plushypertensived`, `c19plusmcvd`, `c19plushypertensive_mcvd`, `c19pluschroniclowerresp`, `c19pluskidneydisease`, `c19pluschronicliver`, `c19plusobesity`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | text | Data as of |
| `death_year` | Date_Of_Death_Year | text | Date of death year |
| `death_month` | Date_Of_Death_Month | text | Date of death month |
| `agegroup` | AgeGroup | text | Age group |
| `sex` | Sex | text | Sex |
| `covid19` | COVID19 | number | Deaths with COVID-19 (U071) as underlying or contributing cause |
| `diabetes_uc` | Diabetes.uc | number | Deaths with diabetes (E10–E14) as underlying cause |
| `diabetes_mc` | Diabetes.mc | number | Deaths with diabetes (E10–E14) as underlying or contributing cause |
| `c19plusdiabetes` | C19PlusDiabetes | number | Deaths with COVID-19 (U071) and diabetes (E10–E14) |
| `c19plushypertensived` | C19PlusHypertensiveDiseases | number | Deaths with COVID-19 (U071) and hypertensive disease (I10–I15) |
| `c19plusmcvd` | C19PlusMajorCardiovascularDiseases | number | Deaths with COVID-19 (U071) and major cardiovascular diseases (I00–I78) |
| `c19plushypertensive_mcvd` | C19PlusHypertensiveDiseasesAndMCVD | number | Deaths with COVID-19 (U071), hypertensive disease (I10–I15), and major cardiovascular diseases (I00–I78) |
| `c19pluschroniclowerresp` | C19PlusChronicLowerRespiratoryDisease | number | Deaths with COVID-19 (U071) and chronic lower respiratory disease (J40–J47) |
| `c19pluskidneydisease` | C19PlusKidneyDisease | number | Deaths with COVID-19 (U071) and kidney disease (N00–N07, N17–N19, and N25–N27) |
| `c19pluschronicliver` | C19PlusChronicLiverDiseaseAndCirrhosis | number | Deaths with COVID-19 (U071) and chronic liver disease and cirrhosis (K70, K73–K74) |
| `c19plusobesity` | C19PlusObesity | number | Deaths with COVID-19 (U071) and obesity (E66) |

### jqg8-ycmh

**AH Quarterly Excess Deaths by State, Sex, Age, and Race** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/jqg8-ycmh.json`
- Metadata: `GET https://data.cdc.gov/api/views/jqg8-ycmh.json`; page: https://data.cdc.gov/d/jqg8-ycmh
- Topics: Category: National Center for Health Statistics
- Tags: `excess deaths`, `covid-19`, `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `weekly`, `age`, `age group`, `race`, `hispanic origin`, `sex`, `all causes`, `coronavirus`, `state`
- Rows: 494,237. Data updated: 2023-09-08. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Quarterly data on the number of deaths from all causes by state (of occurrence), sex, age group, and race/Hispanic origin group for the United States. Counts of deaths in more recent time periods can be compared with counts from earlier years (2015-2019) to determine if the number is higher than expected. Annual and cumulative counts (from Quarter 2, 2020 through the most recent quarter) are also shown.
- Sample row fields ($limit=1): `state`, `statename`, `raceethnicity`, `sex`, `agegroup`, `year`, `quarter`, `yearquarter`, `start_date`, `end_date`, `deaths_weighted`, `covid19_weighted`, `deaths_unweighted`, `covid19_unweighted`, `time_period`, `average_number_of_deaths`, `average_number_of_deaths_1`, `analysisdate`, `type`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `state` | State | text | Jurisdiction of Occurrence Abbreviation |
| `statename` | StateName | text | Jurisdiction of Occurrence Name |
| `raceethnicity` | RaceEthnicity | text | Race or Hispanic Origin group |
| `sex` | Sex | text | Sex |
| `agegroup` | AgeGroup | text | Age Group |
| `year` | Year | number | Year |
| `quarter` | Quarter | text | Quarter |
| `yearquarter` | YearQuarter | text | Year and Quarter |
| `start_date` | Start Date | calendar_date | Start Date |
| `end_date` | End Date | calendar_date | End Date |
| `deaths_weighted` | Deaths (weighted) | number | Deaths (weighted) |
| `covid19_weighted` | COVID19 (weighted) | number | COVID19 (weighted) |
| `deaths_unweighted` | Deaths (unweighted) | number | Deaths (unweighted) |
| `covid19_unweighted` | COVID19 (unweighted) | number | COVID19 (unweighted) |
| `time_period` | Time Period | text | Time Period |
| `average_number_of_deaths` | Average number of deaths (weighted) | number | Average number of deaths (weighted) |
| `average_number_of_deaths_1` | Average number of deaths (unweighted) | number | Average number of deaths (unweighted) |
| `number_above_average_weighted` | Number above average (weighted) | number | Number above average (weighted) |
| `percent_above_average_weighted` | Percent above average (weighted) | number | Percent above average (weighted) |
| `number_above_average` | Number above average (unweighted) | number | Number above average (unweighted) |
| `percent_above_average` | Percent above average (unweighted) | number | Percent above average (unweighted) |
| `analysisdate` | AnalysisDate | calendar_date | Date of analysis |
| `suppression` | Suppression | text | Data suppression flag |
| `footnote` | Footnote | text | Footnote |
| `type` | Type | text | Type of estimate - quarterly, annual, or cumulative |

### 3sh4-uqpm

**AH Sickle Cell Disease Provisional Death Counts 2019-2021** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3sh4-uqpm.json`
- Metadata: `GET https://data.cdc.gov/api/views/3sh4-uqpm.json`; page: https://data.cdc.gov/d/3sh4-uqpm
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `quarterly`, `race`, `hispanic origin`, `age group`, `age`, `covid-19`, `coronavirus`, `sickle cell disease`
- Rows: 129. Data updated: 2021-03-05. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Provisional death counts of sickle cell disease and coronavirus disease 2019 (COVID-19), by quarter, age, and race or Hispanic origin from 2019 through Quarter 1, 2021.
- Sample row fields ($limit=1): `data_as_of`, `date_of_death_year`, `quarter`, `race_or_hispanic_origin`, `age_group`, `scd_underlying`, `scd_multi`, `scd_and_covid_19`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | text | Data of analysis |
| `date_of_death_year` | Date of Death Year | text | Date of death year |
| `quarter` | Quarter | number | Data of death quarter |
| `race_or_hispanic_origin` | Race or Hispanic Origin | text | Race or Hispanic origin |
| `age_group` | Age Group | text | Age group |
| `scd_underlying` | SCD_Underlying | number | Deaths with Sickle Cell Disease listed as underlying cause of death |
| `scd_multi` | SCD_Multi | number | Deaths with Sickle Cell Disease listed as underlying or contributing cause of death |
| `scd_and_covid_19` | SCD and COVID-19 | number | Deaths with Sickle Cell Disease and COVID-19 |

### aewi-gwni

**Asthma in children younger than age 18, by selected characteristics: United States.** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/aewi-gwni.json`
- Metadata: `GET https://data.cdc.gov/api/views/aewi-gwni.json`; page: https://data.cdc.gov/d/aewi-gwni
- Topics: Category: National Center for Health Statistics
- Tags: `asthma`, `asthma attack`, `immune system diseases`, `respiratory tract diseases`, `lung diseases`, `bronchial diseases`, `respiratory hypersensitivity`, `children`, `adolescents`, `age group`, `race`, `race and hispanic origin`, `sex`, `health insurance status`, `poverty level`, `american indian and alaska native`, `asian`, `black`, `native hawaiian or other pacific islander`, `white`, `hispanic`, `non-hispanic`, `female`, `male`, `private health insurance`, `medicaid`, `uninsured`, `national health interview survey`, `nhis`, `health us`, `sdoh-poverty-income`, `sdoh-access-to-health-care`
- Rows: 1,300. Data updated: 2025-06-18. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on asthma in children younger than age 18 in the United States, by selected characteristics. Data are from Health, United States. Source: National Center for Health Statistics, National Health Interview Survey.
- Sample row fields ($limit=1): `hus_year`, `hus_short_name`, `indicator`, `panel_num`, `panel`, `unit_num`, `unit`, `stub_name_num`, `stub_name_order`, `stub_name`, `stub_label_num`, `stub_label_order`, `stub_label`, `year_num`, `year`, `age_num`, `age`, `flag`, `footnote_id_list`, `footnote_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `hus_year` | HUS_YEAR | number | Health, United States vintage year (Key) |
| `hus_short_name` | HUS_SHORT_NAME | text | Health, United States dataset name abbreviation (Key) |
| `indicator` | INDICATOR | text | Measure being estimated. |
| `panel_num` | PANEL_NUM | number | Numeric code for levels of PANEL that may be used for easier coding or formatting of the PANEL variable. |
| `panel` | PANEL | text | Submeasures of INDICATOR. Datasets may have multiple panels. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_name_order` | STUB_NAME_ORDER | number | Numeric code for ordering of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `stub_label_order` | STUB_LABEL_ORDER | number | Numeric code for ordering of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `year` | YEAR | number | Data year or range of data years pertaining to the estimate. |
| `age_num` | AGE_NUM | number | Numeric code for levels of AGE that may be used for easier coding or formatting of the AGE variable. |
| `age` | AGE | text | Age group pertaining to the estimate. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `se` | SE | number | Calculated standard error of the estimate. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnote table linked to this file for more information. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | Footnotes associated with each estimate |
| `footnote_list` | FOOTNOTE_LIST | text | Dataset specific list of footnotes associated with each estimate. |

### wibz-pb5q

**Biennial Overview of Post-acute and Long-term Care in the United States: Data from the National Post-acute and Long-term Care Study** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/wibz-pb5q.json`
- Metadata: `GET https://data.cdc.gov/api/views/wibz-pb5q.json`; page: https://data.cdc.gov/d/wibz-pb5q
- Topics: Category: National Center for Health Statistics
- Tags: `sdoh-use-of-health-care`, `sdoh-access-to-health-care`, `long-term care`, `residential care communities`, `adult day services centers`, `medicaid`, `healthcare`, `activities of daily living`, `diagnoses`, `nurse staffing`, `post-acute care`
- Rows: 30,208. Data updated: 2026-10-19. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DHCS
- Description: The NCHS National Post-acute and Long-term Care Study (NPALS) collects data on post-acute and long-term care providers every two years. The goal is to monitor post-acute and long-term care settings with reliable, accurate, relevant, and timely statistical information to support and inform policy, research, and practice. These data tables provide an overview of the geographic, organizational, staffing, service provision, and user characteristics of paid, regulated long-term and post-acute care providers in the United States. The settings include adult day services centers, home health agencies…
- Sample row fields ($limit=1): `table`, `select_setting`, `value_type`, `survey_year`, `geography`, `select_measure`, `levels_of_measure`, `footnote_value_cell`, `footnote_measure_subscript`, `value_with_footnote`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `table` | Table | number | Corresponds to table number in www.cdc.gov/nchs/npals/webtables/overview.htm |
| `select_setting` | Select Setting | text | Indicates the post-acute or long-term care setting |
| `value_type` | Value type | text | Describes whether the estimate is a number, percentage, or ratio |
| `survey_year` | Survey Year | text | Year in which the survey was conducted. |
| `geography` | Geography | text | Describes the geographic level of values in terms of national or the applicable US state |
| `select_measure` | Select Measure | text | Label for the measure or variable name |
| `levels_of_measure` | Levels of Measure | text | The response options of the measure |
| `value` | Value | number | The estimate of the measure |
| `se` | SE | number | SE = standard error of the estimate |
| `low_95_ci` | Low 95% CI | number | Lower limit of 95% confidence interval |
| `high_95_ci` | High 95% CI | number | Higher limit of 95% confidence interval |
| `footnote_value_cell` | Footnote-Value cell | text | Applicable footnotes for the value |
| `footnote_measure_subscript` | Footnote-Measure Subscript | text | Applicable footnotes describing the measure |
| `value_with_footnote` | Value with Footnote | text | Value with footnote |

### hk9y-quqm

**Conditions Contributing to COVID-19 Deaths, by State and Age, Provisional 2020-2023** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/hk9y-quqm.json`
- Metadata: `GET https://data.cdc.gov/api/views/hk9y-quqm.json`; page: https://data.cdc.gov/d/hk9y-quqm
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `coronavirus`, `covid-19`, `health conditions`, `mortality`, `deaths`, `age group`, `provisional`, `nvss`, `united states`, `puerto rico`, `state`, `monthly`, `yearly`, `age`, `respiratory disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `adult respiratory distress syndrome`, `respiratory failure`, `respiratory arrest`, `circulatory disease`, `hypertensive disease`, `ischemic heart disease`, `cardiac arrest`, `cardiac arrhythmia`, `heart failure`, `cerebrovascular disease`, `septicemia`, `cancer`, `diabetes`, `obesity`, `alzheimer disease`, `dementia`, `renal failure`, `injury`
- Rows: 621,000. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. This dataset shows health conditions and contributing causes mentioned in conjunction with deaths involving coronavirus disease 2019 (COVID-19) by age group and jurisdiction of occurrence. 2022 and 2023 data are provisional. Estimates for 2020 and 2021 are based on final data.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `group`, `state`, `condition_group`, `condition`, `icd10_codes`, `age_group`, `covid_19_deaths`, `number_of_mentions`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date | First week-ending date of data period |
| `end_date` | End Date | calendar_date | Last week-ending date of data period |
| `group` | Group | text | Time-period indicator for record: by Month, by Year, Total |
| `year` | Year | number | Year in which death occurred |
| `month` | Month | number | Month in which death occurred. |
| `state` | State | text | Jurisdiction of occurrence |
| `condition_group` | Condition Group | text | Condition Group |
| `condition` | Condition | text | Condition contributing to deaths involving COVID-19 |
| `icd10_codes` | ICD10_codes | text | ICD-10 code for condition |
| `age_group` | Age Group | text | Age group |
| `covid_19_deaths` | COVID-19 Deaths | number | COVID 19 Deaths |
| `number_of_mentions` | Number of Mentions | number | Number of mentions |
| `flag` | Flag | text | Counts less than 10 supressed. |

### q3t8-zr7t

**COVID-19 Hospital Data from the National Hospital Care Survey** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/q3t8-zr7t.json`
- Metadata: `GET https://data.cdc.gov/api/views/q3t8-zr7t.json`; page: https://data.cdc.gov/d/q3t8-zr7t
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `hospital encounters`, `screenings`, `ventilator use`, `intubation`, `mortality`, `respiratory illness`, `inpatient`, `emergency department`
- Rows: 42,132. Data updated: 2024-07-29. Probe status: 200.
- Update frequency: R/P2M.
- Source: NCHS/DHCS
- Description: The National Hospital Care Survey (NHCS) collects data on patient care in hospital-based settings to describe patterns of health care delivery and utilization in the United States. Settings currently include inpatient and emergency departments (ED). Additionally, the NHCS contributes data that may inform public health emergencies as the survey is designed to capture emerging diseases and viruses that require hospitalizations, including COVID-19 encounters. The 2020 - 2023 NHCS are not yet fully operational so it is important to note that these data are not nationally representative. The data…
- Sample row fields ($limit=1): `figure`, `setting`, `time`, `start_time`, `end_time`, `value`, `measure`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `figure` | Figure | text | Corresponds to Figures reported on https://www.cdc.gov/nchs/covid19/nhcs.htm |
| `setting` | Setting | text | ED = Emergency Department, IP = Inpatient |
| `indicator` | Indicator | text |  |
| `group` | Group | text |  |
| `subgroup` | Subgroup | text |  |
| `time` | Time | number | Reporting Period |
| `start_time` | Start_Time | calendar_date | Week starting date |
| `end_time` | End_Time | calendar_date | Week ending date |
| `value` | Value | number |  |
| `measure` | Measure | text |  |

### 3em4-f5qt

**Data2010** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3em4-f5qt.json`
- Metadata: `GET https://data.cdc.gov/api/views/3em4-f5qt.json`; page: https://data.cdc.gov/d/3em4-f5qt
- Topics: Category: National Center for Health Statistics
- Tags: `data2010`, `healthy people 2010`
- Rows: 963,433. Data updated: 2025-09-11. Probe status: 200.
- Description: An interactive database of historical data from Healthy People 2010, the 3rd iteration of the Healthy People initiative. These data were archived and will not be updated.
- Sample row fields ($limit=1): `foc`, `o`, `focusdesc`, `objective_desc`, `begyear`, `endyear`, `fipscode`, `state`, `population_group`, `population`, `estimate_num`, `estimate_label`, `stderr`, `period`, `target`, `lhi`, `ageadj`, `crosssign`, `unit`, `source`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `foc` | Focus_area_code | text | Focus Area code |
| `o` | Objective_code | text | Objective Code |
| `focusdesc` | focusDesc | text | Focus Area description |
| `objective_desc` | objective_desc | text | Objective Description |
| `begyear` | BegYear | number | Survey start year |
| `endyear` | EndYear | number | Survey end year |
| `fipscode` | FIPSCode | number | Federal Information Processing System (FIPS) Code |
| `state` | STATE | text | State |
| `population_group` | Population_group | text | Population group |
| `population` | population | text | population |
| `estimate_num` | Estimate_num | number | Estimate - numeric value |
| `estimate_label` | Estimate_label | text | Estimate - text value showing DNA, DNC, DSU labels when applicable |
| `stderr` | StdErr | number | Standard error |
| `lowerci` | LowerCI | number | Confidence Interval lower limit |
| `upperci` | UpperCI | number | Confidence Interval upper limit |
| `period` | Period | text | Period label showing start and end range |
| `target` | TARGET | number | Objective National target |
| `lhi` | lhi | text | Leading Health Indicator group |
| `ageadj` | ageadj | number | Boolean flag for age-adjusted estimate |
| `crosssign` | flag_no_target | number | Flag |
| `unit` | unit | text | unit |
| `source` | source | text | Data Source |
| `footnote1` | footnote1 | text | footnote1 |
| `footnote2` | footnote2 | text | footnote2 |
| `footnote3` | footnote3 | text | footnote3 |

### 9j2v-jamp

**Death rates for suicide, by sex, race, Hispanic origin, and age: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/9j2v-jamp.json`
- Metadata: `GET https://data.cdc.gov/api/views/9j2v-jamp.json`; page: https://data.cdc.gov/d/9j2v-jamp
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `suicide`, `injury`, `mental health`, `alaskan natives`, `american natives`, `african americans`, `death`, `hispanic americans`, `mortality`, `sex`, `european continental ancestry group`, `asian continental ancestry group`, `continental population groups`, `age`, `health us`, `health status and determinants`
- Rows: 6,390. Data updated: 2021-06-07. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DAE
- Description: Data on death rates for suicide, by selected population characteristics. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder (https://www.cdc.gov/nchs/hus/contents2019.htm) for critical information about measures, definitions, and changes over time. SOURCE: NCHS, National Vital Statistics System (NVSS); Grove RD, Hetzel AM. Vital statistics rates in the United States, 1940–1960. National Center for Health Statistics. 1968; numerator data from NVSS annual public-use Mortality Files; denominator data from U.S. Census Bureau national population estimates; and Murph…
- Sample row fields ($limit=1): `indicator`, `unit`, `unit_num`, `stub_name`, `stub_name_num`, `stub_label`, `stub_label_num`, `year`, `year_num`, `age`, `age_num`, `estimate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | INDICATOR | text | Measure being estimated. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `year` | YEAR | text | Data year or range of data years pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `age` | AGE | text | Age group pertaining to the estimate. |
| `age_num` | AGE_NUM | number | Numeric code for levels of AGE that may be used for easier coding or formatting of the AGE variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnotes in the source table (Excel) for more information. |

### dmzy-x2ad

**Delay or nonreceipt of needed medical care, prescription drugs, or dental care during the past 12 months due to cost: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/dmzy-x2ad.json`
- Metadata: `GET https://data.cdc.gov/api/views/dmzy-x2ad.json`; page: https://data.cdc.gov/d/dmzy-x2ad
- Topics: Category: National Center for Health Statistics
- Tags: `alaskan natives`, `american natives`, `african americans`, `dental care`, `hispanic americans`, `health insurance`, `medicaid`, `poverty`, `schools`, `sex`, `medically uninsured`, `european continental ancestry group`, `asian continental ancestry group`, `oceanic ancestry group`, `continental population groups`, `prescription drugs`, `prescriptions`, `age`, `health us`, `sdoh-poverty-income`, `sdoh-access-to-health-care`, `sdoh-high-school`, `sdoh-higher-eduaction`
- Rows: 5,082. Data updated: 2022-04-28. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DAE
- Description: Data on delay or nonreceipt of needed medical care, nonreceipt of needed prescription drugs, or nonreceipt of needed dental care during the past 12 months due to cost by selected population characteristics. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder (https://www.cdc.gov/nchs/hus/contents2019.htm) for critical information about measures, definitions, and changes over time. SOURCE: NCHS, National Health Interview Survey, Family Core, Sample Child, and Sample Adult questionnaires. Data for level of difficulty are from the 2010 Quality of Life, 2011-2017 Fu…
- Sample row fields ($limit=1): `indicator`, `panel`, `panel_num`, `unit`, `unit_num`, `stub_name`, `stub_name_num`, `stub_label`, `stub_label_num`, `year`, `year_num`, `age`, `age_num`, `estimate`, `se`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | INDICATOR | text | Measure being estimated. |
| `panel` | PANEL | text | Submeasures of INDICATOR. Datasets may have multiple panels. |
| `panel_num` | PANEL_NUM | number | Numeric code for levels of PANEL that may be used for easier coding or formatting of the PANEL variable. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `year` | YEAR | text | Data year or range of data years pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `age` | AGE | text | Age group pertaining to the estimate. |
| `age_num` | AGE_NUM | number | Numeric code for levels of AGE that may be used for easier coding or formatting of the AGE variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `se` | SE | number | Calculated standard error of the estimate. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnotes in the source table (Excel) for more information. |

### jwta-jxbg

**Distribution of COVID-19 Deaths and Populations, by Jurisdiction, Age, and Race and Hispanic Origin** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/jwta-jxbg.json`
- Metadata: `GET https://data.cdc.gov/api/views/jwta-jxbg.json`; page: https://data.cdc.gov/d/jwta-jxbg
- Topics: Category: National Center for Health Statistics
- Tags: `death rate`, `covid-19`, `coronavirus`, `age group`, `race`, `hispanic origin`, `nchs`, `nvss`, `deaths`, `mortality`, `provisional`, `age`, `united states`, `state`
- Rows: 3,710. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. This visualization provides data that can be used to illustrate potential differences in the burden of deaths due to COVID-19 by race and ethnicity.
- Sample row fields ($limit=1): `data_as_of`, `start_week`, `end_week`, `state`, `race_hispanic_origin`, `count_of_covid_19_deaths`, `distribution_of_covid_19`, `unweighted_distribution_of`, `weighted_distribution_of`, `difference_between_covid_unweighted_pop`, `difference_between_covid_weighted_pop`, `agegroup`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Date of analysis |
| `start_week` | Start Date | calendar_date | First week-ending date of data period |
| `end_week` | End Date | calendar_date | Last week-ending date of data period |
| `state` | State | text | Jurisdiction of occurrence |
| `race_hispanic_origin` | Race/Hispanic origin | text | Race and Hispanic origin group |
| `count_of_covid_19_deaths` | Count of COVID-19 deaths | number | Number of COVID-19 deaths |
| `distribution_of_covid_19` | Distribution of COVID-19 deaths (%) | number | Percent of COVID-19 deaths by group |
| `unweighted_distribution_of` | Unweighted distribution of population (%) | number | Unweighted percent of the population in each group |
| `weighted_distribution_of` | Weighted distribution of population (%) | number | Weighted percent of the population in each group |
| `difference_between_covid_unweighted_pop` | Difference between COVID-19 and unweighted population % | number | Difference between percent of COVID-19 deaths and unweighted population percent |
| `difference_between_covid_weighted_pop` | Difference between COVID-19 and weighted population % | number | Difference between percent of COVID-19 deaths and weighted population percent |
| `agegroup` | AgeGroup | text | Age Group |
| `suppression` | Suppression | text | Suppression flag |

### daba-4vfq

**DQS Birth and fertility rates, by age group, race, and Hispanic origin of mother: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/daba-4vfq.json`
- Metadata: `GET https://data.cdc.gov/api/views/daba-4vfq.json`; page: https://data.cdc.gov/d/daba-4vfq
- Topics: Category: National Center for Health Statistics
- Tags: `birth rate`, `fertility rate`, `natality`, `live birth`, `pregnancy`, `infant`, `newborn`, `age-specific birth rate`, `teen birth rate`, `reproductive health`, `race and hispanic origin`, `race of mother`, `hispanic or latino`, `non-hispanic`, `single race`, `american indian and alaska native`, `asian`, `black or african american`, `native hawaiian or other pacific islander`, `white`, `national vital statistics system`, `nvss`, `birth file`, `health us`
- Rows: 1,296. Data updated: 2026-06-03. Probe status: 200.
- Update frequency: Annual R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on birth rates and fertility rates in the United States, by age group, race, and Hispanic origin of mother. Data are from Health, United States. SOURCE: National Vital Statistics System, Birth File. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or other analytical categories (e.g., Urbanicity, Age group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age group, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Number). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data were collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the uncertainty around the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., unreliable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### 6tn6-vc33

**DQS Cholesterol in adults age 20 and older, by selected characteristics: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/6tn6-vc33.json`
- Metadata: `GET https://data.cdc.gov/api/views/6tn6-vc33.json`; page: https://data.cdc.gov/d/6tn6-vc33
- Topics: Category: National Center for Health Statistics
- Tags: `mean serum total cholesterol`, `total cholesterol`, `cholesterol`, `high cholesterol`, `hypercholesterolemia`, `chronic conditions`, `poverty level`, `male`, `female`, `non-hispanic asian`, `non-hispanic black`, `non-hispanic white`, `hispanic`, `mexican`, `national health and nutrition examination survey`, `nhanes`, `health us`, `sdoh-use-of-health-care`, `sdoh-poverty-income`, `sdoh-access-to-health-care`, `health status and determinants`
- Rows: 1,440. Data updated: 2025-08-25. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on cholesterol in adults age 20 and older in the United States, by selected characteristics. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Health and Nutrition Examination Survey. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### 8miz-siyd

**DQS Community hospital beds, by state: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8miz-siyd.json`
- Metadata: `GET https://data.cdc.gov/api/views/8miz-siyd.json`; page: https://data.cdc.gov/d/8miz-siyd
- Topics: Category: National Center for Health Statistics
- Tags: `community hospital beds`, `hospital`, `hospital beds`, `hospital occupancy`, `state`, `american hospital association`, `health us`, `sdoh-access-to-health-care`, `health care resources`
- Rows: 2,340. Data updated: 2026-09-23. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on community hospital beds in the United States, by state. Data are from Health, United States. SOURCE: American Hospital Association (AHA) Annual Survey of Hospitals, Hospital Statistics. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`, `state_fips`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | Measure being estimated. |
| `subtopic` | SUBTOPIC | text | Subtopics of Topic. |
| `subtopic_id` | SUBTOPIC_ID | text | Numeric code for levels of SUBTOPIC that may be used for easier coding or formatting of the SUBTOPIC variable. |
| `taxonomy` | TAXONOMY | text | CDC taxonomic category. |
| `taxonomy_id` | TAXONOMY_ID | number | Ordering of taxonomic categories. |
| `classification` | CLASSIFICATION | text | Description of the category pertaining to the GROUP. |
| `classification_id` | CLASSIFICATION_ID | number | Numeric code for levels of CLASSIFICATION. |
| `group` | GROUP | text | Description of the population category pertaining to the estimate. |
| `group_id` | GROUP_ID | number | Numeric code for levels of GROUP. |
| `group_order` | GROUP_ORDER | number | Numeric code for the order of the levels of GROUP. |
| `subgroup` | SUBGROUP | text | Specific population subgroup. |
| `subgroup_id` | SUBGROUP_ID | number | Numeric code for levels of SUBGROUP. |
| `subgroup_order` | SUBGROUP_ORDER | number | Numeric code for the order of the levels of SUBGROUP. |
| `nesting_label` | NESTING_LABEL | text | Indication of groupings of subgroups. |
| `nesting_label_id` | NESTING_LABEL_ID | text | Nesting label order. |
| `estimate_type` | ESTIMATE_TYPE | text | Unit of measurement of the estimate. |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | Numeric code for levels of ESTIMATE_TYPE. |
| `time_period` | TIME_PERIOD | text | Data year or range of data years pertaining to the estimate. |
| `time_period_id` | TIME_PERIOD_ID | number | Numeric code for levels of TIME_PERIOD. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure, to agreed upon publication standard decimal places and with suppression rules applied. |
| `standard_error` | STANDARD_ERROR | text | Calculated standard error of the estimate, to agreed upon publication standard decimal places and with publication and suppression rules applied. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | List of footnote IDs. |
| `state_fips` | STATE_FIPS | number | Integer for state identifiers. |

### 7aq9-prdf

**DQS Death rates for heart disease, by sex, race, Hispanic origin, and age: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/7aq9-prdf.json`
- Metadata: `GET https://data.cdc.gov/api/views/7aq9-prdf.json`; page: https://data.cdc.gov/d/7aq9-prdf
- Topics: Category: National Center for Health Statistics
- Tags: `mortality`, `death rates`, `heart diseases`, `cardiovascular diseases`, `circulatory system`, `male`, `female`, `hispanic or latino`, `non-hispanic`, `single race`, `american indian and alaska native`, `asian`, `black or african american`, `native hawaiian or other pacific islander`, `white`, `national vital statistics system`, `nvss`, `mortality files`, `health us`, `health status and determinants`
- Rows: 1,435. Data updated: 2026-05-18. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on death rates for diseases of heart in the United States, by age, sex, race, and Hispanic origin. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality File. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | text | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### h3hw-hzvg

**DQS Death rates for malignant neoplasms, by sex, race, Hispanic origin, and age: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/h3hw-hzvg.json`
- Metadata: `GET https://data.cdc.gov/api/views/h3hw-hzvg.json`; page: https://data.cdc.gov/d/h3hw-hzvg
- Topics: Category: National Center for Health Statistics
- Tags: `mortality`, `death rates`, `malignant neoplasm`, `neoplasm`, `cancer`, `cancer deaths`, `male`, `female`, `hispanic or latino`, `non-hispanic`, `single race`, `american indian and alaska native`, `asian`, `black or african american`, `native hawaiian or other pacific islander`, `white`, `national vital statistics system`, `nvss`, `mortality files`, `health us`, `health status and determinants`
- Rows: 1,743. Data updated: 2026-05-28. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on death rates for neoplasms in the United States, by age, sex, race, and Hispanic origin. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality File. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | text | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### w26f-tf3h

**DQS Death rates for suicide, by sex, race, Hispanic origin, and age: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/w26f-tf3h.json`
- Metadata: `GET https://data.cdc.gov/api/views/w26f-tf3h.json`; page: https://data.cdc.gov/d/w26f-tf3h
- Topics: Category: National Center for Health Statistics
- Tags: `mortality`, `death rates`, `suicide`, `suicide rates`, `intentional injury`, `intentional injury deaths`, `intentional injury death rates`, `male`, `female`, `hispanic or latino`, `non-hispanic`, `single race`, `american indian and alaska native`, `asian`, `black or african american`, `native hawaiian or other pacific islander`, `white`, `national vital statistics system`, `nvss`, `mortality files`, `health us`, `health status and determinants`
- Rows: 1,386. Data updated: 2026-06-16. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on death rates for suicide in the United States, by age, sex, race, and Hispanic origin. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality File. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### p4r5-qsgs

**DQS Delay or nonreceipt of needed medical care, prescription drugs, or dental care during the past 12 months due to cost: United States(Archived)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/p4r5-qsgs.json`
- Metadata: `GET https://data.cdc.gov/api/views/p4r5-qsgs.json`; page: https://data.cdc.gov/d/p4r5-qsgs
- Topics: Category: National Center for Health Statistics
- Tags: `heath care access`, `dental care`, `prescription drugs`, `adults`, `american indian or alaska native`, `asian`, `black or african american`, `children and adolescents`, `education`, `female`, `functional limitation status`, `health insurance`, `hispanic or latino`, `mexican`, `male`, `metropolitan and nonmetropolitan`, `rural population`, `urban population`, `multiple race`, `native hawaiian or other pacific islander`, `older adults`, `poverty`, `region`, `white`
- Rows: 4,278. Data updated: 2024-11-05. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: This topic is no longer available in the NCHS Data Query System (DQS). Data on delay or nonreceipt of needed medical care, nonreceipt of needed prescription drugs, or nonreceipt of needed dental care during the past 12 months due to cost, in the United States, by selected population characteristics. Data from Health, United States. SOURCE: National Center for Health Statistics, National Health Interview Survey. Search, visualize, and download these and other estimates from over 120 health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.ht…
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | Measure being estimated. |
| `subtopic` | SUBTOPIC | text | Submeasures of TOPIC. Datasets may have multiple subtopics. |
| `subtopic_id` | SUBTOPIC_ID | number | Numeric code for levels of SUBTOPIC that may be used for easier coding or formatting of the SUBTOPIC variable. |
| `classification` | CLASSIFICATION | text | Description of the category pertaining to the group. |
| `classification_id` | CLASSIFICATION_ID | number | Numeric code for levels of CLASSIFICATION that may be used for easier coding or formatting of the CLASSIFICATION variable. |
| `group` | GROUP | text | Description of the population category pertaining to the estimate. |
| `group_id` | GROUP_ID | number | Numeric code for levels of GROUP that may be used for easier coding or formatting of the GROUP variable. |
| `group_order` | GROUP_ORDER | number | Integer provided for GROUP that indicates the order in which groups will display in the drop down menu. |
| `subgroup` | SUBGROUP | text | Specific population subgroup pertaining to the estimate. |
| `subgroup_id` | SUBGROUP_ID | number | Numeric code for levels of SUBGROUP that may be used for easier coding or formatting of the SUBGROUP variable. |
| `subgroup_order` | SUBGROUP_ORDER | number | Integer provided for SUBGROUP that indicates the order in which subgroups will display in the drop down menu. |
| `estimate_type` | ESTIMATE_TYPE | text | Unit of measurement of the estimate. |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | Numeric code for levels of ESTIMATE_TYPE that may be used for easier coding or formatting of the ESTIMATE_TYPE variable. |
| `time_period` | TIME_PERIOD | text | Data year or range of data years pertaining to the estimate. |
| `time_period_id` | TIME_PERIOD_ID | number | Numeric code for levels of TIME_PERIOD that may be used for easier coding or formatting of the TIME_PERIOD variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `standard_error` | STANDARD_ERROR | number | Calculated standard error of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | Lower limit of 95% confidence interval. |
| `estimate_uci` | ESTIMATE_UCI | text | Upper limit of 95% confidence interval. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the Footnotes section of this page for more information. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | Footnotes associated with each estimate. |

### yib5-h3pw

**DQS Dentists, by state: United States.** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/yib5-h3pw.json`
- Metadata: `GET https://data.cdc.gov/api/views/yib5-h3pw.json`; page: https://data.cdc.gov/d/yib5-h3pw
- Topics: Category: National Center for Health Statistics
- Tags: `dentists`, `united states`, `american dental association`, `health us`, `sdoh-access-to-health-care`, `healthcare resources`
- Rows: 2,496. Data updated: 2026-01-13. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on supply of active dentists in the United States by state. Data are from Health, United States. SOURCE: American Dental Association, Health Policy Institute. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`, `state_fips`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | Measure being estimated. |
| `subtopic` | SUBTOPIC | text | Subtopics of Topic. |
| `subtopic_id` | SUBTOPIC_ID | text | Numeric code for levels of SUBTOPIC that may be used for easier coding or formatting of the SUBTOPIC variable. |
| `taxonomy` | TAXONOMY | text | CDC taxonomic category. |
| `taxonomy_id` | TAXONOMY_ID | number | Ordering of taxonomic categories. |
| `classification` | CLASSIFICATION | text | Description of the category pertaining to the GROUP. |
| `classification_id` | CLASSIFICATION_ID | number | Numeric code for levels of CLASSIFICATION. |
| `group` | GROUP | text | Description of the population category pertaining to the estimate. |
| `group_id` | GROUP_ID | number | Numeric code for levels of GROUP. |
| `group_order` | GROUP_ORDER | number | Numeric code for the order of the levels of GROUP. |
| `subgroup` | SUBGROUP | text | Specific population subgroup. |
| `subgroup_id` | SUBGROUP_ID | number | Numeric code for levels of SUBGROUP. |
| `subgroup_order` | SUBGROUP_ORDER | number | Numeric code for the order of the levels of SUBGROUP. |
| `nesting_label` | NESTING_LABEL | text | Indication of groupings of subgroups. |
| `nesting_label_id` | NESTING_LABEL_ID | text | Nesting label order. |
| `estimate_type` | ESTIMATE_TYPE | text | Unit of measurement of the estimate. |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | Numeric code for levels of ESTIMATE_TYPE. |
| `time_period` | TIME_PERIOD | text | Data year or range of data years pertaining to the estimate. |
| `time_period_id` | TIME_PERIOD_ID | number | Numeric code for levels of TIME_PERIOD. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure, to agreed upon publication standard decimal places and with suppression rules applied. |
| `standard_error` | STANDARD_ERROR | text | Calculated standard error of the estimate, to agreed upon publication standard decimal places and with publication and suppression rules applied. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | List of footnote IDs. |
| `state_fips` | STATE_FIPS | number | Integer for state identifiers. |

### rdjz-vn2n

**DQS Drug overdose death rates, by drug type, sex, age, race, and Hispanic origin: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/rdjz-vn2n.json`
- Metadata: `GET https://data.cdc.gov/api/views/rdjz-vn2n.json`; page: https://data.cdc.gov/d/rdjz-vn2n
- Topics: Category: National Center for Health Statistics
- Tags: `drug overdose death rates`, `overdose`, `deaths`, `mortality`, `opioid deaths`, `methadone deaths`, `heroin deaths`, `injury deaths`, `drug misuse`, `male`, `female`, `hispanic or latino`, `non-hispanic`, `single race`, `american indian and alaska native`, `asian`, `black or african american`, `native hawaiian or other pacific islander`, `white`, `national vital statistics system`, `nvss`, `mortality files`, `health us`, `health status and determinants`
- Rows: 3,738. Data updated: 2026-08-03. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on drug overdose death rates in the United States, by age, sex, race, Hispanic origin, and drug type. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Vital Statistics System, Mortality File. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### 6vwk-ensg

**DQS Estimate of Emergency Department Visits in the United States Footnotes** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/6vwk-ensg.json`
- Metadata: `GET https://data.cdc.gov/api/views/6vwk-ensg.json`; page: https://data.cdc.gov/d/6vwk-ensg
- Topics: Category: National Center for Health Statistics
- Tags: `emergency department`, `patient characteristics`, `visit characteristics`, `reason for visit`, `diagnosis`
- Rows: 13. Data updated: 2026-01-26. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DHCS
- Description: List of footnotes, notes, and source information for The National Hospital Ambulatory Medical Care Survey (NHAMCS). Each row of this dataset contains the accompanying text for a footnote found in NHAMCS dataset. The footnote lookup can be merged onto any NHAMCS dataset using, DATASET_SHORT_NAME, FN_ID, FN_TYPE, and FN_TEXT. SOURCE: National Center for Health Statistics CDC, The National Hospital Ambulatory Medical Care Survey (NHAMCS)
- Sample row fields ($limit=1): `dataset_shortname`, `footnote_id_list`, `fn_type`, `fn_text`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `dataset_shortname` | dataset_shortname | text | A short identifier or abbreviation representing the dataset to which the footnote applies. Used to link the footnote to the appropriate dataset. |
| `footnote_id_list` | footnote_id_list | text | A unique identifier for the footnote. This ID is referenced in the main dataset to associate specific data values with corresponding explanatory notes. |
| `fn_type` | fn_type | text | The classification of the footnote, indicating its purpose or context. |
| `fn_code` | fn_code | text | The symbol or character used in the dataset to indicate the presence of a footnote, typically corresponding to a specific fn_type. |
| `flag` | flag | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `fn_text` | fn_text | text | The full explanatory text of the footnote, providing context, clarification, or relevant details related to specific data values or methodology.. |

### e4ec-z5aa

**DQS Estimate of Emergency Department Visits in the United States, 2016-2022** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/e4ec-z5aa.json`
- Metadata: `GET https://data.cdc.gov/api/views/e4ec-z5aa.json`; page: https://data.cdc.gov/d/e4ec-z5aa
- Topics: Category: National Center for Health Statistics
- Tags: `emergency department`, `patient characteristics`, `visit characteristics`, `reason for visit`, `diagnosis`, `healthcare access and utilization`
- Rows: 6,776. Data updated: 2025-06-09. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DHCS
- Description: These data include counts and rates of emergency department visits from 2016-2022 for selected primary diagnoses and reasons for visit, stratified by selected patient and hospital characteristics. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### wd75-kcmv

**DQS Fetal, late fetal, and perinatal mortality rates, by detailed race and Hispanic origin of mother United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/wd75-kcmv.json`
- Metadata: `GET https://data.cdc.gov/api/views/wd75-kcmv.json`; page: https://data.cdc.gov/d/wd75-kcmv
- Topics: Category: National Center for Health Statistics
- Tags: `fetal deaths`, `late fetal deaths`, `perinatal deaths`, `fetal mortality`, `late fetal mortality`, `perinatal mortality`, `race and hispanic origin of mother`, `bridged race`, `single race`, `american indian or alaska native`, `non-hispanic`, `asian or pacific islander`, `asian`, `black`, `native hawaiian or other pacific islander`, `white`, `national vital statistics system`, `nvss`, `fetal death data set`, `health us`, `health status and determinants`
- Rows: 528. Data updated: 2025-06-09. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on fetal, late fetal, and perinatal mortality rates in the United States, by detailed race and Hispanic origin of mother. Data are from Health, United States. Source: National Center for Health Statistics, National Vital Statistics System, Fetal Death Data Set. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | text | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | text | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### 7siw-u4fz

**DQS Health care employment and wages, by selected occupations: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/7siw-u4fz.json`
- Metadata: `GET https://data.cdc.gov/api/views/7siw-u4fz.json`; page: https://data.cdc.gov/d/7siw-u4fz
- Topics: Category: National Center for Health Statistics
- Tags: `healthcare employment`, `healthcare wages`, `mean hourly wages`, `hourly wages`, `healthcare practitioners`, `healthcare practitioners and technical occupations`, `healthcare support occupations`, `us department of labor`, `bureau of labor statistics`, `occupational employment and wage statistics`, `health us`, `sdoh-source-of-healthcare`, `sdoh-access-to-healthcare`, `sdoh-employment`
- Rows: 2,444. Data updated: 2026-09-08. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on health care employment and wages in the United States, by selected occupations. Data are from Health, United States. Source: U.S. Department of Labor, Bureau of Labor Statistics, Occupational Employment and Wage Statistics. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### 4q35-rqzk

**DQS Hospital admission, average length of stay, outpatient visits, and outpatient surgery by type of ownership and size of hospital: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/4q35-rqzk.json`
- Metadata: `GET https://data.cdc.gov/api/views/4q35-rqzk.json`; page: https://data.cdc.gov/d/4q35-rqzk
- Topics: Category: National Center for Health Statistics
- Tags: `health care use`, `hospital`, `hospital admissions`, `length of hospital stay`, `outpatient visits`, `outpatient surgery`, `hospital ownership`, `community hospitals`, `federal hospitals`, `hospital size`, `american hospital association`, `health us`, `sdoh-access-to-health-care`, `sdoh-use-of-health-care`, `healthcare resources`
- Rows: 2,254. Data updated: 2026-07-10. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on hospital admission, average length of stay, outpatient visits, and outpatient surgery in the United States, by type of ownership and size of hospital. Data are from Health, United States. SOURCE: American Hospital Association (AHA) Annual Survey of Hospitals, Hospital Statistics. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | text | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | text | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### va5e-efw9

**DQS Hypertension in adults age 20 and older, by selected characteristics: United States.** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/va5e-efw9.json`
- Metadata: `GET https://data.cdc.gov/api/views/va5e-efw9.json`; page: https://data.cdc.gov/d/va5e-efw9
- Topics: Category: National Center for Health Statistics
- Tags: `hypertension`, `high blood pressure`, `chronic conditions`, `poverty level`, `male`, `female`, `non-hispanic asian`, `non-hispanic black`, `non-hispanic white`, `hispanic`, `mexican`, `national health and nutrition examination survey`, `nhanes`, `health us`, `sdoh-use-of-health-care`, `sdoh-poverty-income`, `sdoh-access-to-health-care`, `health status and determinants`
- Rows: 480. Data updated: 2025-08-25. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on hypertension in adults age 20 and older in the United States, by selected characteristics. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Health and Nutrition Examination Survey. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### pjb2-jvdr

**DQS Infant mortality rates, by race and Hispanic origin of mother, state, and territory: United States and U.S. dependent areas (Archived)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/pjb2-jvdr.json`
- Metadata: `GET https://data.cdc.gov/api/views/pjb2-jvdr.json`; page: https://data.cdc.gov/d/pjb2-jvdr
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `infant mortality`, `american indian or alaska native`, `asian or pacific islander`, `black or african american`, `child and adolescent`, `hispanic or latino`, `state`, `white`, `health us`
- Rows: 1,710. Data updated: 2024-03-06. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: This topic is no longer available in the NCHS Data Query System (DQS). Search, visualize, and download other estimates from over 120 health topics with DQS, available from: https://www.cdc.gov/nchs/dataquery/index.htm. Data on on average annual infant mortality rates in the United States and U.S. dependent areas, by race and Hispanic origin of mother, state, and territory. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Vital Statistics System, Linked Birth/Infant Death Data Set.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`, `state_fips`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | Measure being estimated. |
| `subtopic` | SUBTOPIC | text | Submeasures of TOPIC. Datasets may have multiple subtopics. |
| `subtopic_id` | SUBTOPIC_ID | number | Numeric code for levels of SUBTOPIC that may be used for easier coding or formatting of the SUBTOPIC variable. |
| `classification` | CLASSIFICATION | text | Description of the category pertaining to the group. |
| `classification_id` | CLASSIFICATION_ID | number | Numeric code for levels of CLASSIFICATION that may be used for easier coding or formatting of the CLASSIFICATION variable. |
| `group` | GROUP | text | Description of the population category pertaining to the estimate. |
| `group_id` | GROUP_ID | number | Numeric code for levels of GROUP that may be used for easier coding or formatting of the GROUP variable. |
| `group_order` | GROUP_ORDER | number | Integer provided for GROUP that indicates the order in which groups will display in the drop down menu. |
| `subgroup` | SUBGROUP | text | Specific population subgroup pertaining to the estimate. |
| `subgroup_id` | SUBGROUP_ID | number | Numeric code for levels of SUBGROUP that may be used for easier coding or formatting of the SUBGROUP variable. |
| `subgroup_order` | SUBGROUP_ORDER | number | Integer provided for SUBGROUP that indicates the order in which subgroups will display in the drop down menu. |
| `estimate_type` | ESTIMATE_TYPE | text | Unit of measurement of the estimate. |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | Numeric code for levels of ESTIMATE_TYPE that may be used for easier coding or formatting of the ESTIMATE_TYPE variable. |
| `time_period` | TIME_PERIOD | text | Data year or range of data years pertaining to the estimate. |
| `time_period_id` | TIME_PERIOD_ID | number | Numeric code for levels of TIME_PERIOD that may be used for easier coding or formatting of the TIME_PERIOD variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `standard_error` | STANDARD_ERROR | text | Calculated standard error of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | Lower limit of 95% confidence interval. |
| `estimate_uci` | ESTIMATE_UCI | text | Upper limit of 95% confidence interval. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the Footnotes section of this page for more information. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | Footnotes associated with each estimate. |
| `state_fips` | STATE_FIPS | number | Integer provided for state identifiers. |

### j7ym-uwqy

**DQS Infant, neonatal, and postneonatal mortality rates, by detailed race and Hispanic origin of mother: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/j7ym-uwqy.json`
- Metadata: `GET https://data.cdc.gov/api/views/j7ym-uwqy.json`; page: https://data.cdc.gov/d/j7ym-uwqy
- Topics: Category: National Center for Health Statistics
- Tags: `infant`, `newborn`, `neonatal`, `postneonatal`, `infant deaths`, `neonatal deaths`, `postneonatal deaths`, `infant mortality`, `neonatal mortality`, `postneonatal mortality`, `death rates`, `mortality`, `mortality rates`, `race and hispanic origin of mother`, `hispanic or latino`, `central and south american`, `cuban`, `mexican`, `puerto rican`, `non-hispanic`, `single race`, `asian`, `american indian and alaska native`, `black or african american`, `native hawaiian or other pacific islander`, `white`, `national vital statistics system`, `nvss`, `health us`, `health status and determinants`
- Rows: 360. Data updated: 2026-06-04. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on infant, neonatal, and postneonatal mortality rates in the United States, by detailed race and Hispanic origin of mother. Data are from Health, United States. Source: National Center for Health Statistics, National Vital Statistics System, Linked Birth/Infant Death Data Set. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | text | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | text | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### a92y-5zud

**DQS Initial injury-related visits to hospital emergency departments, by sex, age, and intent and mechanism of injury: United States (Archived)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/a92y-5zud.json`
- Metadata: `GET https://data.cdc.gov/api/views/a92y-5zud.json`; page: https://data.cdc.gov/d/a92y-5zud
- Topics: Category: National Center for Health Statistics
- Tags: `health care use`, `emergency department visits`, `injury`, `wounds and injuries`, `accidents`, `traffic`, `accidental falls`, `children and adolescents`, `men`, `older persons`, `women`, `health us`, `healthcare access and utilization`
- Rows: 1,480. Data updated: 2025-05-15. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: This topic is no longer available in the NCHS Data Query System (DQS). Data on initial injury-related visits to hospital emergency departments in the United States, by sex, age, and intent and mechanism of injury. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Hospital Ambulatory Medical Care Survey. Search, visualize, and download these and other estimates from over 150 health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text |  |
| `subtopic` | SUBTOPIC | text |  |
| `subtopic_id` | SUBTOPIC_ID | text |  |
| `taxonomy` | TAXONOMY | text |  |
| `taxonomy_id` | TAXONOMY_ID | number |  |
| `classification` | CLASSIFICATION | text |  |
| `classification_id` | CLASSIFICATION_ID | number |  |
| `group` | GROUP | text |  |
| `group_id` | GROUP_ID | number |  |
| `group_order` | GROUP_ORDER | number |  |
| `subgroup` | SUBGROUP | text |  |
| `subgroup_id` | SUBGROUP_ID | number |  |
| `subgroup_order` | SUBGROUP_ORDER | number |  |
| `nesting_label` | NESTING_LABEL | text |  |
| `nesting_label_id` | NESTING_LABEL_ID | number |  |
| `estimate_type` | ESTIMATE_TYPE | text |  |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number |  |
| `time_period` | TIME_PERIOD | text |  |
| `time_period_id` | TIME_PERIOD_ID | number |  |
| `estimate` | ESTIMATE | number |  |
| `standard_error` | STANDARD_ERROR | number |  |
| `estimate_lci` | ESTIMATE_LCI | text |  |
| `estimate_uci` | ESTIMATE_UCI | text |  |
| `flag` | FLAG | text |  |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text |  |

### hdja-ybdg

**DQS Medicaid coverage among persons under age 65, by selected characteristics: United States (Archived)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/hdja-ybdg.json`
- Metadata: `GET https://data.cdc.gov/api/views/hdja-ybdg.json`; page: https://data.cdc.gov/d/hdja-ybdg
- Topics: Category: National Center for Health Statistics
- Tags: `health insurance`, `medicaid`, `adults`, `american indian or alaska native`, `asian`, `black or african american`, `children and adolescents`, `education`, `female`, `functional limitation status`, `hispanic or latino`, `mexican`, `male`, `metropolitan and nonmetropolitan`, `rural population`, `urban population`, `multiple race`, `native hawaiian or other pacific islander`, `poverty`, `region`, `white`
- Rows: 1,944. Data updated: 2025-03-17. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: This topic is no longer available in the NCHS Data Query System (DQS). Data on Medicaid coverage among people under age 65, in the United States, by selected population characteristics. Data from Health, United States. SOURCE: National Center for Health Statistics, National Health Interview Survey. Search, visualize, and download these and other estimates from over 120 health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | Measure being estimated. |
| `subtopic` | SUBTOPIC | text | Submeasures of TOPIC. Datasets may have multiple subtopics. |
| `subtopic_id` | SUBTOPIC_ID | text | Numeric code for levels of SUBTOPIC that may be used for easier coding or formatting of the SUBTOPIC variable. |
| `classification` | CLASSIFICATION | text | Description of the category pertaining to the group. |
| `classification_id` | CLASSIFICATION_ID | number | Numeric code for levels of CLASSIFICATION that may be used for easier coding or formatting of the CLASSIFICATION variable. |
| `group` | GROUP | text | Description of the population category pertaining to the estimate. |
| `group_id` | GROUP_ID | number | Numeric code for levels of GROUP that may be used for easier coding or formatting of the GROUP variable. |
| `group_order` | GROUP_ORDER | number | Integer provided for GROUP that indicates the order in which groups will display in the drop down menu. |
| `subgroup` | SUBGROUP | text | Specific population subgroup pertaining to the estimate. |
| `subgroup_id` | SUBGROUP_ID | number | Numeric code for levels of SUBGROUP that may be used for easier coding or formatting of the SUBGROUP variable. |
| `subgroup_order` | SUBGROUP_ORDER | number | Integer provided for SUBGROUP that indicates the order in which subgroups will display in the drop down menu. |
| `estimate_type` | ESTIMATE_TYPE | text | Unit of measurement of the estimate. |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | Numeric code for levels of ESTIMATE_TYPE that may be used for easier coding or formatting of the ESTIMATE_TYPE variable. |
| `time_period` | TIME_PERIOD | text | Data year or range of data years pertaining to the estimate. |
| `time_period_id` | TIME_PERIOD_ID | number | Numeric code for levels of TIME_PERIOD that may be used for easier coding or formatting of the TIME_PERIOD variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `standard_error` | STANDARD_ERROR | number | Calculated standard error of the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | Upper limit of 95% confidence interval. |
| `estimate_lci` | ESTIMATE_LCI | text | Lower limit of 95% confidence interval. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the Footnotes section of this page for more information. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | Footnotes associated with each estimate. |

### s57w-7gbe

**DQS National health spending: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/s57w-7gbe.json`
- Metadata: `GET https://data.cdc.gov/api/views/s57w-7gbe.json`; page: https://data.cdc.gov/d/s57w-7gbe
- Topics: Category: National Center for Health Statistics
- Tags: `national health care spending`, `national health care expenditures`, `personal health care expenditures`, `personal health care spending`, `health consumption spending`, `health care`, `hospital care`, `physician and clinical services`, `dental services`, `home health care`, `nursing care facilities and continuing care retirement communities`, `prescription drugs`, `durable medical equipment`, `government administration of health insurance`, `net cost of health insurance`, `non-medical insurance`, `government public health activities`, `investment`, `research`, `structures and equipment`, `gross domestic product`, `gdp`, `national health expenditures accounts`, `nhea`, `bea`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-workplace`, `health us`
- Rows: 1,755. Data updated: 2026-06-08. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on national health spending in the United States, by type of spending and gross domestic product. Data are from Health, United States. SOURCE: Centers for Medicare & Medicaid Services, Office of the Actuary, National Health Statistics Group, National Health Expenditure Accounts. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | text | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### sz5x-j2c3

**DQS National Post-acute and Long-term Care Providers** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/sz5x-j2c3.json`
- Metadata: `GET https://data.cdc.gov/api/views/sz5x-j2c3.json`; page: https://data.cdc.gov/d/sz5x-j2c3
- Topics: Category: National Center for Health Statistics
- Tags: `united states`, `sdoh-use-of-health-care`, `sdoh-access-to-health-care`, `long-term care`, `residential care communities`, `adult day services centers`, `medicaid`, `healthcare`, `activities of daily living`, `diagnosis`, `nurse staffing`, `post-acute care`
- Rows: 608. Data updated: 2026-08-19. Probe status: 200.
- Update frequency: R/P2Y.
- Source: NCHS/Division of Health Care Statistics
- Description: Health estimates of providers of post-acute and long-term care in the United States. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or other analytical categories (e.g., Urbanicity, Age group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age group, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | text | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Number). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data were collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the uncertainty around the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., unreliable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### 6pdm-py4x

**DQS National Post-acute and Long-term Care Users** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/6pdm-py4x.json`
- Metadata: `GET https://data.cdc.gov/api/views/6pdm-py4x.json`; page: https://data.cdc.gov/d/6pdm-py4x
- Topics: Category: National Center for Health Statistics
- Tags: `united states`, `sdoh-use-of-health-care`, `sdoh-access-to-health-care`, `long-term care`, `residential care communities`, `adult day services centers`, `medicaid`, `healthcare`, `activities of daily living`, `diagnoses`, `nurse staffing`, `post-acute care`
- Rows: 397. Data updated: 2026-04-16. Probe status: 200.
- Update frequency: R/P2Y.
- Source: NCHS/Division of Health Care Statistics
- Description: Health estimates of users of post-acute and long-term care in the United States. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### iqm3-hbev

**DQS NHANES Footnotes** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/iqm3-hbev.json`
- Metadata: `GET https://data.cdc.gov/api/views/iqm3-hbev.json`; page: https://data.cdc.gov/d/iqm3-hbev
- Topics: Category: National Center for Health Statistics
- Tags: `nhanes`, `national-health-and-nutrition-examination-survey`, `footnotes`
- Rows: 30. Data updated: 2026-05-28. Probe status: 200.
- Update frequency: R/P2Y.
- Source: https://www.cdc.gov/nchs/nhanes/visualization/
- Description: List of footnotes, notes, and source information for NHANES Summary Statistics. Each row of this dataset contains the accompanying text for a footnote found in the NHANES Datasets.
- Sample row fields ($limit=1): `dataset_shortname`, `footnote_id_list`, `fn_type`, `fn_text`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `dataset_shortname` | dataset_shortname | text | A short identifier or abbreviation representing the dataset to which the footnote applies. Used to link the footnote to the appropriate dataset. |
| `footnote_id_list` | footnote_id_list | text | A unique identifier for the footnote. This ID is referenced in the main dataset to associate specific data values with corresponding explanatory notes. |
| `fn_type` | fn_type | text | The classification of the footnote, indicating its purpose or context. |
| `fn_code` | fn_code | text | The symbol or character used in the dataset to indicate the presence of a footnote, typically corresponding to a specific fn_type. |
| `fn_text` | fn_text | text | The full explanatory text of the footnote, providing context, clarification, or relevant details related to specific data values or methodology. |

### 6rvp-rahv

**DQS NHANES Select Chronic Conditions Prevalence Estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/6rvp-rahv.json`
- Metadata: `GET https://data.cdc.gov/api/views/6rvp-rahv.json`; page: https://data.cdc.gov/d/6rvp-rahv
- Topics: Category: National Center for Health Statistics
- Tags: `chronic conditions`, `nhanes`, `dqs`, `health status and determinants`
- Rows: 1,140. Data updated: 2026-05-28. Probe status: 200.
- Update frequency: R/P2Y.
- Source: NCHS/DHANES
- Description: These data represent prevalence estimates of select chronic conditions from the National Health and Nutrition Examination Survey (NHANES). This version of the dataset is specific for use by the NCHS DQS. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.)." |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### v7tk-n6v3

**DQS NHANES Select Infectious Diseases Prevalence Estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/v7tk-n6v3.json`
- Metadata: `GET https://data.cdc.gov/api/views/v7tk-n6v3.json`; page: https://data.cdc.gov/d/v7tk-n6v3
- Topics: Category: National Center for Health Statistics
- Tags: `nhanes`, `dqs`, `health status and determinants`
- Rows: 340. Data updated: 2026-05-28. Probe status: 200.
- Update frequency: R/P2Y.
- Source: NCHS/DHANES
- Description: These data represent prevalence estimates of select infectious diseases from the National Health and Nutrition Examination Survey (NHANES). This version of the NHANES dataset is specific to visualization within the NCHS DQS. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### 8ekv-ep3s

**DQS NHANES Select Mean Dietary Intake Estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8ekv-ep3s.json`
- Metadata: `GET https://data.cdc.gov/api/views/8ekv-ep3s.json`; page: https://data.cdc.gov/d/8ekv-ep3s
- Topics: Category: National Center for Health Statistics
- Tags: `nhanes`, `dqs`, `health status and determinants`
- Rows: 4,284. Data updated: 2026-05-28. Probe status: 200.
- Update frequency: R/P2Y.
- Source: NCHS/DHANES
- Description: These data represent mean intake, on a given day, estimates of nutrients from foods and beverages from the National Health and Nutrition Examination Survey (NHANES). Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### 36ue-xht5

**DQS NHANES Select Oral Health Prevalence Estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/36ue-xht5.json`
- Metadata: `GET https://data.cdc.gov/api/views/36ue-xht5.json`; page: https://data.cdc.gov/d/36ue-xht5
- Topics: Category: National Center for Health Statistics
- Tags: `diet`, `nhanes`, `dqs`, `health status and determinants`, `healthcare access and utilization`
- Rows: 1,160. Data updated: 2026-05-28. Probe status: 200.
- Update frequency: R/P2Y.
- Source: NCHS/DHANES
- Description: These data represent prevalence estimates of select oral health topics from the National Health and Nutrition Examination Survey (NHANES). Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | text | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### gj3i-hsbz

**DQS NHIS Adult Summary Health Statistics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/gj3i-hsbz.json`
- Metadata: `GET https://data.cdc.gov/api/views/gj3i-hsbz.json`; page: https://data.cdc.gov/d/gj3i-hsbz
- Topics: Category: National Center for Health Statistics
- Tags: `summary health statistics`, `nhis`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-food-access`, `sdoh-workplace`
- Rows: 30,576. Data updated: 2026-08-27. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DHIS
- Description: Interactive Summary Health Statistics for Adults provide annual estimates of selected health topics for adults aged 18 years and over based on final data from the National Health Interview Survey. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected." |
| `time_period_id` | TIME_PERIOD_ID | text | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | text | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### gpsd-ru5i

**DQS NHIS Adult Summary Statistics Footnotes** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/gpsd-ru5i.json`
- Metadata: `GET https://data.cdc.gov/api/views/gpsd-ru5i.json`; page: https://data.cdc.gov/d/gpsd-ru5i
- Topics: Category: National Center for Health Statistics
- Tags: `summary health statistics`, `nhis`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-food-access`, `sdoh-workplace`
- Rows: 80. Data updated: 2026-08-31. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DHIS
- Description: List of footnotes, notes, and source information for NHIS Adult Summary Statistics. Each row of this dataset contains the accompanying text for a footnote found in the NHIS Adults Summary Statistics Dataset.
- Sample row fields ($limit=1): `dataset_shortname`, `fn_id`, `fn_type`, `fn_code`, `fn_text`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `dataset_shortname` | dataset_shortname | text | A short identifier or abbreviation representing the dataset to which the footnote applies. Used to link the footnote to the appropriate dataset. |
| `fn_id` | fn_id | text | A unique identifier for the footnote. This ID is referenced in the main dataset to associate specific data values with corresponding explanatory notes. |
| `fn_type` | fn_type | text | The classification of the footnote, indicating its purpose or context. |
| `fn_code` | fn_code | text | The symbol or character used in the dataset to indicate the presence of a footnote, typically corresponding to a specific fn_type. |
| `fn_text` | fn_text | text | The full explanatory text of the footnote, providing context, clarification, or relevant details related to specific data values or methodology. |

### 7ctq-myvs

**DQS NHIS Child Summary Health Statistics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/7ctq-myvs.json`
- Metadata: `GET https://data.cdc.gov/api/views/7ctq-myvs.json`; page: https://data.cdc.gov/d/7ctq-myvs
- Topics: Category: National Center for Health Statistics
- Tags: `summary health statistics`, `nhis`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-food-access`, `sdoh-workplace`
- Rows: 8,918. Data updated: 2026-09-09. Probe status: 200.
- Update frequency: Annual R/P1Y.
- Source: NCHS/DHIS
- Description: Interactive Summary Health Statistics for Children provide annual estimates of selected health topics for children under age 18 years based on final data from the National Health Interview Survey. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | text | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | text | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### mk5r-qxdg

**DQS NHIS Child Summary Statistics Footnotes** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/mk5r-qxdg.json`
- Metadata: `GET https://data.cdc.gov/api/views/mk5r-qxdg.json`; page: https://data.cdc.gov/d/mk5r-qxdg
- Topics: Category: National Center for Health Statistics
- Tags: `summary health statistics`, `nhis`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-food-access`, `sdoh-workplace`
- Rows: 42. Data updated: 2026-08-31. Probe status: 200.
- Source: NCHS/DHIS
- Description: List of footnotes, notes, and source information for NHIS Child Summary Statistics. Each row of this dataset contains the accompanying text for a footnote found in the NHIS Child Summary Statistics Dataset.
- Sample row fields ($limit=1): `dataset_shortname`, `footnote_id_list`, `fn_type`, `fn_text`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `dataset_shortname` | dataset_shortname | text | A short identifier or abbreviation representing the dataset to which the footnote applies. Used to link the footnote to the appropriate dataset. |
| `footnote_id_list` | footnote_id_list | text | A unique identifier for the footnote. This ID is referenced in the main dataset to associate specific data values with corresponding explanatory notes. |
| `fn_type` | fn_type | text | The classification of the footnote, indicating its purpose or context. |
| `fn_code` | fn_code | text | The symbol or character used in the dataset to indicate the presence of a footnote, typically corresponding to a specific fn_type. |
| `fn_text` | fn_text | text | The full explanatory text of the footnote, providing context, clarification, or relevant details related to specific data values or methodology. |

### v728-xui5

**DQS NHIS Functioning difficulties Footnotes** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/v728-xui5.json`
- Metadata: `GET https://data.cdc.gov/api/views/v728-xui5.json`; page: https://data.cdc.gov/d/v728-xui5
- Topics: Category: National Center for Health Statistics
- Tags: `functioning`, `functioning difficulties`, `nhis`, `sdoh-poverty-income`, `sdoh-employment-status`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `health status and determinants`
- Rows: 19. Data updated: 2026-10-13. Probe status: 200.
- Update frequency: Annual (R/P1Y).
- Source: NCHS/DAE/MREB
- Description: List of footnotes, notes, and source information for NHIS Functioning Difficulties Statistics. Each row of this dataset contains the accompanying text for a footnote found in the NHIS Functioning Difficulties Dataset.
- Sample row fields ($limit=1): `dataset_shortname`, `fn_id`, `fn_type`, `fn_code`, `fn_text`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `dataset_shortname` | dataset_shortname | text | A short identifier or abbreviation representing the dataset to which the footnote applies. Used to link the footnote to the appropriate dataset. |
| `fn_id` | fn_id | text | A unique identifier for the footnote. This ID is referenced in the main dataset to associate specific data values with corresponding explanatory notes. |
| `fn_type` | fn_type | text | The classification of the footnote, indicating its purpose or context. |
| `fn_code` | fn_code | text | The symbol or character used in the dataset to indicate the presence of a footnote, typically corresponding to a specific fn_type. |
| `fn_text` | fn_text | text | The full explanatory text of the footnote, providing context, clarification, or relevant details related to specific data values or methodology. |

### btv3-srcc

**DQS NHIS Functioning difficulties in adults age 18 and older by selected characteristics United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/btv3-srcc.json`
- Metadata: `GET https://data.cdc.gov/api/views/btv3-srcc.json`; page: https://data.cdc.gov/d/btv3-srcc
- Topics: Category: National Center for Health Statistics
- Tags: `functioning`, `functioning difficulties`, `nhis`, `sdoh-poverty-income`, `sdoh-employment-status`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `health status and determinants`
- Rows: 2,268. Data updated: 2026-10-13. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DAE/MREB
- Description: Annual estimates of level of functioning difficulties for adults aged 18 years and over based on final data from the National Health Interview Survey. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | number | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | number | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### be57-s94j

**DQS Normal weight, overweight, and obesity among adults aged 20 and over, by selected characteristics: United States (Archived)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/be57-s94j.json`
- Metadata: `GET https://data.cdc.gov/api/views/be57-s94j.json`; page: https://data.cdc.gov/d/be57-s94j
- Topics: Category: National Center for Health Statistics
- Tags: `obesity`, `overweight`, `body mass index`, `body weight`, `chronic conditions`, `health risk factors`, `adults`, `black or african american`, `hispanic or latino`, `mexican`, `men`, `older persons`, `poverty`, `white`, `women`, `health us`, `health status and determinants`
- Rows: 2,352. Data updated: 2025-06-23. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: This topic is no longer available in the NCHS Data Query System (DQS). Data on overweight and obesity among adults aged 20 and over in the United States, by selected characteristics, including sex, age, race, Hispanic origin, and poverty level. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Health and Nutrition Examination Survey. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### 83mw-v57c

**DQS NPALS Footnotes** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/83mw-v57c.json`
- Metadata: `GET https://data.cdc.gov/api/views/83mw-v57c.json`; page: https://data.cdc.gov/d/83mw-v57c
- Topics: Category: National Center for Health Statistics
- Tags: `npals`, `national-post-acute-and-long-term-care-study`, `footnotes`
- Rows: 27. Data updated: 2026-03-25. Probe status: 200.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: List of footnotes, notes, and source information for NPALS Summary Statistics. Each row of this dataset contains the accompanying text for a footnote found in the NPALS Datasets.
- Sample row fields ($limit=1): `dataset_shortname`, `footnote_id_list`, `fn_type`, `fn_text`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `dataset_shortname` | dataset_shortname | text | A short identifier or abbreviation representing the dataset to which the footnote applies. Used to link the footnote to the appropriate dataset. |
| `footnote_id_list` | footnote_id_list | text | A unique identifier for the footnote. This ID is referenced in the main dataset to associate specific data values with corresponding explanatory notes. |
| `fn_type` | fn_type | text | The classification of the footnote, indicating its purpose or context. |
| `fn_code` | fn_code | text | The symbol or character used in the dataset to indicate the presence of a footnote, typically corresponding to a specific fn_type. |
| `fn_text` | fn_text | text | The full explanatory text of the footnote, providing context, clarification, or relevant details related to specific data values or methodology. |

### mzhq-xsdd

**DQS NVSS Footnotes** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/mzhq-xsdd.json`
- Metadata: `GET https://data.cdc.gov/api/views/mzhq-xsdd.json`; page: https://data.cdc.gov/d/mzhq-xsdd
- Topics: Category: National Center for Health Statistics
- Tags: `nvss`
- Rows: 8. Data updated: 2026-03-18. Probe status: 200.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: List of footnotes, notes, and source information for NVSS Summary Statistics. Each row of this dataset contains the accompanying text for a footnote found in the NVSS Datasets.
- Sample row fields ($limit=1): `dataset_shortname`, `fn_id`, `fn_type`, `fn_code`, `fn_text`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `dataset_shortname` | dataset_shortname | text | A short identifier or abbreviation representing the dataset to which the footnote applies. Used to link the footnote to the appropriate dataset. |
| `fn_id` | fn_id | text | A unique identifier for the footnote. This ID is referenced in the main dataset to associate specific data values with corresponding explanatory notes. |
| `fn_type` | fn_type | text | The classification of the footnote, indicating its purpose or context. |
| `fn_code` | fn_code | text | The symbol or character used in the dataset to indicate the presence of a footnote, typically corresponding to a specific fn_type. |
| `fn_text` | fn_text | text | The full explanatory text of the footnote, providing context, clarification, or relevant details related to specific data values or methodology. |

### ga7k-kycn

**DQS NVSS Low birthweight live births, by state: United States.** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ga7k-kycn.json`
- Metadata: `GET https://data.cdc.gov/api/views/ga7k-kycn.json`; page: https://data.cdc.gov/d/ga7k-kycn
- Topics: Category: National Center for Health Statistics
- Tags: `births`, `nvss`
- Rows: 520. Data updated: 2026-01-28. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on Low birthweight live births by state in the United States. SOURCE: National Center for Health Statistics, National Vital Statistics System, Birth File. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`, `state_fips`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | text | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | text | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |
| `state_fips` | STATE_FIPS | number | A Federal Information Processing Standards (FIPS) code representing the U.S. state or territory associated with the data. |

### uzn2-cq9f

**DQS Obesity in children and adolescents aged 2–19 years, by selected characteristics: United States (Archived)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/uzn2-cq9f.json`
- Metadata: `GET https://data.cdc.gov/api/views/uzn2-cq9f.json`; page: https://data.cdc.gov/d/uzn2-cq9f
- Topics: Category: National Center for Health Statistics
- Tags: `obesity`, `overweight`, `body mass index`, `body weight`, `chronic conditions`, `health risk factors`, `black or african american`, `children and adolescents`, `hispanic or latino`, `mexican`, `poverty`, `white`, `health us`, `health status and determinants`
- Rows: 693. Data updated: 2025-08-29. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: This topic is no longer available in the NCHS Data Query System (DQS). Data on obesity in children and adolescents aged 2-19 years in the United States, by selected characteristics, including sex, age, race, Hispanic origin, and poverty level. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Health and Nutrition Examination Survey. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | text | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### gu48-2cs8

**DQS Personal healthcare spending: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/gu48-2cs8.json`
- Metadata: `GET https://data.cdc.gov/api/views/gu48-2cs8.json`; page: https://data.cdc.gov/d/gu48-2cs8
- Topics: Category: National Center for Health Statistics
- Tags: `personal health care expenditures`, `personal health care spending`, `health care`, `hospital care`, `physician and clinical services`, `dental services`, `home health care`, `nursing care facilities and continuing care retirement communities`, `prescription drugs`, `health insurance`, `national health expenditure accounts`, `nhea`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-workplace`, `health us`
- Rows: 1,365. Data updated: 2026-06-08. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on personal healthcare spending in the United States, by source of funds. Data are from Health, United States. SOURCE: Centers for Medicare & Medicaid Services, Office of the Actuary, National Health Statistics Group, National Health Expenditure Accounts. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | text | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### kusj-ex57

**DQS prescription medication use in the past 30 days, by sex, race and Hispanic origin, and age group: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/kusj-ex57.json`
- Metadata: `GET https://data.cdc.gov/api/views/kusj-ex57.json`; page: https://data.cdc.gov/d/kusj-ex57
- Topics: Category: National Center for Health Statistics
- Tags: `prescription drugs`, `drugs`, `prescriptions`, `medications`, `health care use`, `male`, `female`, `non-hispanic asian`, `non-hispanic white`, `hispanic`, `mexican`, `national health and nutrition examination survey`, `health us`, `sdoh-use-of-health-care`, `healthcare access and utilization`
- Rows: 1,296. Data updated: 2026-08-03. Probe status: 200.
- Update frequency: R/P2Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on prescription medication use in the past 30 days in the United States, by sex, race and Hispanic origin, and age group. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Health and Nutrition Examination Survey. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `standard_error`, `estimate_lci`, `estimate_uci`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes. |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.). |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | number | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected. |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | number | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### mtgp-t7vw

**DQS Use of selected substances in the past 30 days among 12th graders, 10th graders, and 8th graders, by sex and race: United States.** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/mtgp-t7vw.json`
- Metadata: `GET https://data.cdc.gov/api/views/mtgp-t7vw.json`; page: https://data.cdc.gov/d/mtgp-t7vw
- Topics: Category: National Center for Health Statistics
- Tags: `substance use`, `drug use`, `substance use among students`, `drug use among students`, `alcohol`, `binge drinking`, `cigarettes`, `tobacco use`, `cocaine`, `inhalants`, `marijuana`, `marijuana vaping`, `mdma`, `ecstasy`, `molly`, `nicotine vaping`, `vaping`, `e-cigarette use`, `smoking`, `students`, `male`, `female`, `boys`, `girls`, `race and hispanic origin`, `black`, `white`, `hispanic or latino`, `non-hispanic`, `12th grade`, `10th grade`, `8th grade`, `monitoring the future`, `national institute of drug abuse`, `health us`, `sdoh-high-school`
- Rows: 6,951. Data updated: 2026-08-19. Probe status: 200.
- Update frequency: Annual R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: Data on use of selected substances in the past 30 days among 12th graders, 10th graders, and 8th graders in the United States, by sex and race. Data are from Health, United States. Source: Monitoring the Future, Institute for Social Research, University of Michigan, supported by National Institutes of Health, National Institute on Drug Abuse. Search, visualize, and download these and other estimates from a wide range of health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `flag`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text | The broad subject area or theme under which data is categorized. |
| `subtopic` | SUBTOPIC | text | A more specific category within a topic that provides further detail or granularity. |
| `subtopic_id` | SUBTOPIC_ID | number | A unique identifier assigned to each subtopic, typically used for database referencing or joins. |
| `taxonomy` | TAXONOMY | text | A classification scheme or structure that organizes topics and subtopics into a hierarchy or logical order. |
| `taxonomy_id` | TAXONOMY_ID | number | A unique identifier for each taxonomy used to ensure consistency and version control across data assets. |
| `classification` | CLASSIFICATION | text | A categorical grouping used to segment the data based on a shared attribute. |
| `classification_id` | CLASSIFICATION_ID | number | A unique identifier for each classification type. |
| `group` | GROUP | text | A variable used to group or segment data, often reflecting demographics, geography, or analytical categories (e.g., Urbanicity, Age Group). |
| `group_id` | GROUP_ID | number | A unique identifier associated with each group. |
| `group_order` | GROUP_ORDER | number | An integer value indicating the preferred display order of groups for visualization or tabulation purposes." |
| `subgroup` | SUBGROUP | text | A further breakdown within a group (e.g., if GROUP is Age, SUBGROUP could be 18–24, 25–34, etc.)." |
| `subgroup_id` | SUBGROUP_ID | number | A unique identifier for each subgroup. |
| `subgroup_order` | SUBGROUP_ORDER | number | An integer value indicating the display or sort order of subgroups. |
| `nesting_label` | NESTING_LABEL | text | A label used to nest or group subgroups within a hierarchy (e.g., combining specific age bands into broader age categories). |
| `nesting_label_id` | NESTING_LABEL_ID | text | A unique identifier for each nesting label. |
| `estimate_type` | ESTIMATE_TYPE | text | The type of statistical estimate reported (e.g., Percentage, Rate, Mean). |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number | A unique identifier for the estimate type. |
| `time_period` | TIME_PERIOD | text | The specific time frame during which the data was collected." |
| `time_period_id` | TIME_PERIOD_ID | number | A unique identifier for the time period. |
| `estimate` | ESTIMATE | number | The numeric value representing the key metric. |
| `standard_error` | STANDARD_ERROR | text | The standard error of the estimate, representing the variability or precision of the estimate. |
| `estimate_lci` | ESTIMATE_LCI | text | The lower bound of the 95% confidence interval for the estimate. |
| `estimate_uci` | ESTIMATE_UCI | text | The upper bound of the 95% confidence interval for the estimate. |
| `flag` | FLAG | text | A quality or interpretation flag (e.g., suppressed value, unstable estimate) that provides metadata or warnings about the estimate. |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text | A list of one or more footnote identifiers associated with the data value. Each ID corresponds to an explanatory note providing additional context, clarification, or data caveats. |

### gebw-t5b7

**DQS Visits to physician offices, hospital outpatient departments, and hospital emergency departments, by age, sex, and race: United States (Archived)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/gebw-t5b7.json`
- Metadata: `GET https://data.cdc.gov/api/views/gebw-t5b7.json`; page: https://data.cdc.gov/d/gebw-t5b7
- Topics: Category: National Center for Health Statistics
- Tags: `ambulatory care`, `office visits`, `health care use`, `physician office visits`, `physicians`, `hospital use`, `emergency department visits`, `emergency service`, `black or african american`, `children and adolescents`, `men`, `older persons`, `white`, `women`, `health us`, `healthcare access and utilization`
- Rows: 1,938. Data updated: 2025-05-14. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/Division of Analysis and Epidemiology
- Description: This topic is no longer available in the NCHS Data Query System (DQS). Data on visits to physician offices and hospital emergency departments in the United States, by age, sex, and race. Data are from Health, United States. SOURCE: National Center for Health Statistics, National Ambulatory Medical Care Survey and National Hospital Ambulatory Medical Care Survey. Search, visualize, and download these and other estimates from over 150 health topics with the NCHS Data Query System (DQS), available from: https://www.cdc.gov/nchs/dataquery/index.htm.
- Sample row fields ($limit=1): `topic`, `subtopic`, `subtopic_id`, `taxonomy`, `taxonomy_id`, `classification`, `classification_id`, `group`, `group_id`, `group_order`, `subgroup`, `subgroup_id`, `subgroup_order`, `estimate_type`, `estimate_type_id`, `time_period`, `time_period_id`, `estimate`, `footnote_id_list`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `topic` | TOPIC | text |  |
| `subtopic` | SUBTOPIC | text |  |
| `subtopic_id` | SUBTOPIC_ID | number |  |
| `taxonomy` | TAXONOMY | text |  |
| `taxonomy_id` | TAXONOMY_ID | number |  |
| `classification` | CLASSIFICATION | text |  |
| `classification_id` | CLASSIFICATION_ID | number |  |
| `group` | GROUP | text |  |
| `group_id` | GROUP_ID | number |  |
| `group_order` | GROUP_ORDER | number |  |
| `subgroup` | SUBGROUP | text |  |
| `subgroup_id` | SUBGROUP_ID | number |  |
| `subgroup_order` | SUBGROUP_ORDER | number |  |
| `nesting_label` | NESTING_LABEL | text |  |
| `nesting_label_id` | NESTING_LABEL_ID | number |  |
| `estimate_type` | ESTIMATE_TYPE | text |  |
| `estimate_type_id` | ESTIMATE_TYPE_ID | number |  |
| `time_period` | TIME_PERIOD | text |  |
| `time_period_id` | TIME_PERIOD_ID | number |  |
| `estimate` | ESTIMATE | number |  |
| `standard_error` | STANDARD_ERROR | number |  |
| `estimate_lci` | ESTIMATE_LCI | text |  |
| `estimate_uci` | ESTIMATE_UCI | text |  |
| `flag` | FLAG | text |  |
| `footnote_id_list` | FOOTNOTE_ID_LIST | text |  |

### 95ax-ymtc

**Drug overdose death rates, by drug type, sex, age, race, and Hispanic origin: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/95ax-ymtc.json`
- Metadata: `GET https://data.cdc.gov/api/views/95ax-ymtc.json`; page: https://data.cdc.gov/d/95ax-ymtc
- Topics: Category: National Center for Health Statistics
- Tags: `drug overdose`, `injury`, `alaskan natives`, `american natives`, `analgesics`, `opioid`, `african americans`, `death`, `heroin`, `hispanic americans`, `methadone`, `mortality`, `sex`, `european continental ancestry group`, `asian continental ancestry group`, `continental population groups`, `age`, `health us`
- Rows: 6,228. Data updated: 2022-04-28. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DAE
- Description: Data on drug overdose death rates, by drug type and selected population characteristics. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder (https://www.cdc.gov/nchs/hus/contents2019.htm) for critical information about measures, definitions, and changes over time. SOURCE: NCHS, National Vital Statistics System, numerator data from annual public-use Mortality Files; denominator data from U.S. Census Bureau national population estimates; and Murphy SL, Xu JQ, Kochanek KD, Arias E, Tejada-Vera B. Deaths: Final data for 2018. National Vital Statistics Reports; vol…
- Sample row fields ($limit=1): `indicator`, `panel`, `panel_num`, `unit`, `unit_num`, `stub_name`, `stub_name_num`, `stub_label`, `stub_label_num`, `year`, `year_num`, `age`, `age_num`, `estimate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | INDICATOR | text | Measure being estimated. |
| `panel` | PANEL | text | Submeasures of INDICATOR. Datasets may have multiple panels. |
| `panel_num` | PANEL_NUM | number | Numeric code for levels of PANEL that may be used for easier coding or formatting of the PANEL variable. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `year` | YEAR | text | Data year or range of data years pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `age` | AGE | text | Age group pertaining to the estimate. |
| `age_num` | AGE_NUM | number | Numeric code for levels of AGE that may be used for easier coding or formatting of the AGE variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnotes in the source table (Excel) for more information. |

### gypc-kpgn

**Drug Use Data from Selected Hospitals** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/gypc-kpgn.json`
- Metadata: `GET https://data.cdc.gov/api/views/gypc-kpgn.json`; page: https://data.cdc.gov/d/gypc-kpgn
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `opioids`, `benzodiazepines`, `cocaine`, `health care delivery`, `heroin`, `emergency departments`, `fentanyl`, `patient care`, `hospitalization`, `hospitals`, `inpatient`, `mental health`, `methadone`, `substance use`, `icd-10-cm`, `drug overdose`, `opioid overdose`, `amphetamine`, `cdc`, `classification`, `emergency`, `bed size`, `federal hospitals`, `methylphenidate`, `opium`, `tramadol`, `electronic health records`
- Rows: 8,481. Data updated: 2026-08-10. Probe status: 200.
- Update frequency: R/P2M.
- Source: NCHS/DHCS
- Description: The National Hospital Care Survey (NHCS) collects data on patient care in hospital-based settings to describe patterns of health care delivery and utilization in the United States. Settings currently include inpatient and emergency departments (ED). From this collection, the NHCS contributes data that may inform emerging national health threats such as the current opioid public health emergency. The 2024 - 2025 NHCS are not yet fully operational, so it is important to note that the data presented here are preliminary and not nationally representative. The data are from 81 hospitals submitting…
- Sample row fields ($limit=1): `figure`, `setting`, `time`, `start_time`, `end_time`, `value`, `measure`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `figure` | FIGURE | text |  |
| `setting` | SETTING | text |  |
| `indicator` | INDICATOR | text |  |
| `group` | GROUP | text |  |
| `subgroup` | SUBGROUP | text |  |
| `time` | TIME | number |  |
| `start_time` | START_TIME | calendar_date |  |
| `end_time` | END_TIME | calendar_date |  |
| `value` | VALUE | number |  |
| `measure` | MEASURE | text |  |

### v2g4-wqg2

**Early Model-based Provisional Estimates of Drug Overdose, Suicide, and Transportation-related Deaths** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/v2g4-wqg2.json`
- Metadata: `GET https://data.cdc.gov/api/views/v2g4-wqg2.json`; page: https://data.cdc.gov/d/v2g4-wqg2
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `vsrr`, `mortality`, `deaths`, `provisional`, `united states`, `state`, `weekly`, `transport accidents`, `drug overdose`, `suicide`, `nowcasting`
- Rows: 46,665. Data updated: 2022-02-04. Probe status: 200.
- Update frequency: irregular.
- Source: National Center for Health Statistics
- Description: This dataset provides model-based provisional estimates of the weekly numbers of drug overdose, suicide, and transportation-related deaths using “nowcasting” methods to account for the normal lag between the occurrence and reporting of these deaths. Estimates less than 10 are suppressed. These early model-based provisional estimates were generated using a multi-stage hierarchical Bayesian modeling process to generate smoothed estimates of the weekly numbers of death, accounting for reporting lags. These estimates are based on several assumptions about how the reporting lags have changed in re…
- Sample row fields ($limit=1): `weekending`, `state`, `stateabb`, `outcome`, `mmwryear`, `mmwrweek`, `analysisdate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `weekending` | Week Ending Date | calendar_date | Week of Death |
| `state` | State | text |  |
| `stateabb` | State Abbreviation | text |  |
| `mediannumber` | Median Number | number | Posterior Predicted Median Number |
| `lowerbound` | Lower Bound | number | 95% Credible Interval Lower Bound |
| `upperbound` | Upper Bound | number | 95% Credible Interval Upper Bound |
| `outcome` | Outcome | text | Drug overdose, suicide, or transportation-related death |
| `mmwryear` | MMWR Year | text |  |
| `mmwrweek` | MMWR Week | text |  |
| `rolling4weekmean` | Rolling 4-Week Mean | number | Posterior Predicted Median Number (Rolling 4-week average) |
| `rolling4weeklower` | Rolling 4-Week Lower | number | 95% Credible Interval Lower Bound (Rolling 4-week average) |
| `rolling4weekupper` | Rolling 4-Week Upper | number | 95% Credible Interval Upper Bound (Rolling 4-week average) |
| `analysisdate` | AnalysisDate | text | Date of Analysis |

### ycxr-emue

**Estimates of Emergency Department Visits in the United States from 2016-2022** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ycxr-emue.json`
- Metadata: `GET https://data.cdc.gov/api/views/ycxr-emue.json`; page: https://data.cdc.gov/d/ycxr-emue
- Topics: Category: National Center for Health Statistics
- Tags: `emergency department`, `national hospital ambulatory medical care survey`, `reason for visit`, `primary diagnosis`
- Rows: 6,776. Data updated: 2024-07-25. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DHCS
- Description: The National Hospital Ambulatory Medical Care Survey (NHAMCS), conducted by the National Center for Health Statistics (NCHS), collects annual data on visits to emergency departments to describe patterns of utilization and provision of ambulatory care delivery in the United States. Data are collected from nonfederal, general, and short-stay hospitals from all 50 U.S. states and the District of Columbia, and are used to develop nationally representative estimates. The data include counts and rates of emergency department visits from 2016-2022 for the 10 leading primary diagnoses and reasons for…
- Sample row fields ($limit=1): `year`, `measure_type`, `leading_10_ranking`, `measure`, `group`, `subgroup`, `estimate_type`, `estimate`, `standard_error`, `lower_95_ci`, `upper_95_ci`, `reliable`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | text | Survey year from which the estimate was derived |
| `measure_type` | Measure Type | text | Type of measure: primary diagnosis or reason for visit |
| `leading_10_ranking` | Leading 10 Ranking | text | The 2022 ranking of the selected measure, if applicable |
| `measure` | Measure | text | Name of the primary diagnosis or reason for visit of interest |
| `group` | Group | text | Indicator of the grouping variable: sex, age, race/ethnicity, region, metropolitan statistical area, or expected payment source |
| `subgroup` | Subgroup | text | Subcategories for each group |
| `estimate_type` | Estimate Type | text | Type of estimate: visit count or visit rate (per 1,000 people) |
| `estimate` | Estimate | number | Estimate of the selected measure |
| `standard_error` | Standard Error | number | Standard error of the estimate |
| `lower_95_ci` | Lower 95% CI | number | Lower 95% confidence interval of the estimate |
| `upper_95_ci` | Upper 95% CI | number | Upper 95% confidence interval of the estimate |
| `reliable` | Reliable | text | Indicator of estimate’s reliability according to NCHS standards |

### xkkf-xrst

**Excess Deaths Associated with COVID-19** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/xkkf-xrst.json`
- Metadata: `GET https://data.cdc.gov/api/views/xkkf-xrst.json`; page: https://data.cdc.gov/d/xkkf-xrst
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `excess deaths`, `united states`, `state`, `puerto rico`, `weekly`, `all causes`, `covid-19`, `coronavirus`
- Rows: 56,700. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. Estimates of excess deaths can provide information about the burden of mortality potentially related to COVID-19, beyond the number of deaths that are directly attributed to COVID-19. Excess deaths are typically defined as the difference between observed numbers of deaths and expected numbers. This visualization provides weekly data on excess deaths by jurisdiction of occurrence. Counts of deaths in more recent weeks are compared with historical trends to determine whether th…
- Sample row fields ($limit=1): `week_ending_date`, `state`, `observed_number`, `upper_bound_threshold`, `exceeds_threshold`, `average_expected_count`, `excess_estimate`, `total_excess_estimate`, `percent_excess_estimate`, `year`, `type`, `outcome`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending_date` | Week Ending Date | text |  |
| `state` | State | text |  |
| `observed_number` | Observed Number | number |  |
| `upper_bound_threshold` | Upper Bound Threshold | number |  |
| `exceeds_threshold` | Exceeds Threshold | checkbox |  |
| `average_expected_count` | Average Expected Count | number |  |
| `excess_estimate` | Excess Estimate | number | Excess estimate |
| `total_excess_estimate` | Total Excess Estimate | number | Total excess estimate |
| `percent_excess_estimate` | Percent Excess Estimate | number | Percent excess estimate |
| `year` | Year | text |  |
| `type` | Type | text |  |
| `outcome` | Outcome | text |  |
| `suppress` | Suppress | text |  |
| `note` | Note | text |  |

### 2m93-xvra

**Health conditions among children under age 18, by selected characteristics: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/2m93-xvra.json`
- Metadata: `GET https://data.cdc.gov/api/views/2m93-xvra.json`; page: https://data.cdc.gov/d/2m93-xvra
- Topics: Category: National Center for Health Statistics
- Tags: `asthma`, `allergy`, `attention deficit/hyperactivity disorder`, `ear infection`, `emotional or behavioral difficulties`, `mental health`, `alaskan natives`, `american natives`, `african americans`, `child`, `food`, `hispanic americans`, `hypersensitivity`, `insurance`, `health`, `medicaid`, `poverty`, `sex`, `skin`, `medically uninsured`, `european continental ancestry group`, `asian continental ancestry group`, `oceanic ancestry group`, `continental population groups`, `age`, `respiratory tract diseases`, `ear diseases`, `health us`, `sdoh-poverty-income`, `sdoh-access-to-health-care`
- Rows: 2,744. Data updated: 2021-10-20. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DAE
- Description: NOTE: On October 19, 2021, estimates for 2016–2018 by health insurance status were revised to correct errors. Changes are highlighted and tagged at https://www.cdc.gov/nchs/data/hus/2019/012-508.pdf Data on health conditions among children under age 18, by selected population characteristics. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder (https://www.cdc.gov/nchs/hus/contents2019.htm) for critical information about measures, definitions, and changes over time. SOURCE: NCHS, National Health Interview Survey, Family Core and Sample Child questionnaires. For…
- Sample row fields ($limit=1): `indicator`, `panel`, `panel_num`, `unit`, `unit_num`, `stub_name`, `stub_name_num`, `stub_label`, `stub_label_num`, `year`, `year_num`, `age`, `age_num`, `flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | INDICATOR | text | Measure being estimated. |
| `panel` | PANEL | text | Submeasures of INDICATOR. Datasets may have multiple panels. |
| `panel_num` | PANEL_NUM | number | Numeric code for levels of PANEL that may be used for easier coding or formatting of the PANEL variable. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `year` | YEAR | text | Data year or range of data years pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `age` | AGE | text | Age group pertaining to the estimate. |
| `age_num` | AGE_NUM | number | Numeric code for levels of AGE that may be used for easier coding or formatting of the AGE variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `se` | SE | number | Calculated standard error of the estimate. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnotes in the source table (Excel) for more information. |

### 3q3z-9ucr

**Healthy People 2020 Final Progress by Population Group Chart and Table** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3q3z-9ucr.json`
- Metadata: `GET https://data.cdc.gov/api/views/3q3z-9ucr.json`; page: https://data.cdc.gov/d/3q3z-9ucr
- Topics: Category: National Center for Health Statistics
- Tags: `healthy people 2020`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-literacy`, `sdoh-early-childhood`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-health-literacy`, `sdoh-food-access`, `sdoh-housing-quality`, `sdoh-crime-violence`, `sdoh-environmental`, `sdoh-workplace`, `sdoh-transportation`, `sdoh-social-emotional`, `sdoh-civic-participation`, `sdoh-discrimination`, `sdoh-racism`, `sdoh-incarceration`, `sdoh-language`
- Rows: 7,482. Data updated: 2022-05-04. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DAE
- Description: [1] The Progress by Population Group analysis is a component of the Healthy People 2020 (HP2020) Final Review. The analysis included subsets of the 1,111 measurable HP2020 objectives that have data available for any of six broad population characteristics: sex, race and ethnicity, educational attainment, family income, disability status, and geographic location. Progress toward meeting HP2020 targets is presented for up to 24 population groups within these characteristics, based on objective data aggregated across HP2020 topic areas. The Progress by Population Group data are also available at…
- Sample row fields ($limit=1): `hp2020_objective`, `topic_area`, `population_characteristic`, `population_group`, `baseline_year_s`, `baseline_estimate`, `baseline_estimate_standard`, `final_year_s`, `final_year_estimate`, `final_year_estimate_standard`, `target_value`, `final_progress_status_category`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `hp2020_objective` | HP2020 Objective | text | [1] The analysis included subsets of the 1,111 measurable HP2020 objectives that had data available for any of six broad population characteristics: sex, race and ethnicity, educational attainment, family income, disability status, and geo… |
| `topic_area` | Topic Area | text | A subset of the HP2020 topic areas that had measurable objectives with data available for any of the six population characteristics. |
| `population_characteristic` | Population Characteristic | text | Characteristics available in the “Group By” menu of the Progress by Population Group chart include sex, race and ethnicity, educational attainment, family income, disability status, and geographic location. |
| `population_group` | Population Group | text | Population groups defined by sex, race and ethnicity, educational attainment, family income, disability status, and geographic location. See “Population Group Definitions and Categorizations for Healthy People 2020 Final Review” for furthe… |
| `baseline_year_s` | Baseline Year(s) | text | The first year(s) of HP2020 data for the population group. |
| `baseline_estimate` | Baseline Estimate | number | Estimate for the population group for the baseline year(s). This estimate can be a count, percentage, or rate depending on the objective. For more information on how estimates for specific objectives were calculated, see https://www.health… |
| `baseline_estimate_standard` | Baseline Estimate Standard Error | number | Standard error of the baseline estimate, if available. |
| `final_year_s` | Final Year(s) | text | [2] The final year(s) of reliable data that were included for the population group in HP2020. The final value was generally based on data available on the HP2020 website as of January 2020. For objectives that are continuing into HP2030, m… |
| `final_year_estimate` | Final Year Estimate | number | Estimate for the population group during the final year(s). This estimate can be a count, percentage, or rate depending on the objective. For more information on how estimates for specific objectives were calculated, see https://www.health… |
| `final_year_estimate_standard` | Final Year Estimate Standard Error | number | Standard error of the final year(s) estimate, if available. |
| `target_value` | Target Value | number | [3] Targets were generally set using one of several available target-setting methods, based on objectives’ baseline values for the total population covered by the objective. For information on the target-setting methods used in HP2020, see… |
| `final_progress_status_category` | Final Progress Status Category | text | [4] Status was determined using the baseline, final, and target value. The status categories used in HP2020 were: a. Target met or exceeded; b. Improved; c. Little or no detectable change; and d. Got worse. |

### x749-vh2i

**Healthy People 2020 Final Progress Table** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/x749-vh2i.json`
- Metadata: `GET https://data.cdc.gov/api/views/x749-vh2i.json`; page: https://data.cdc.gov/d/x749-vh2i
- Topics: Category: National Center for Health Statistics
- Tags: `healthy people 2020`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-literacy`, `sdoh-early-childhood`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-health-literacy`, `sdoh-food-access`, `sdoh-housing-quality`, `sdoh-crime-violence`, `sdoh-environmental`, `sdoh-workplace`, `sdoh-transportation`, `sdoh-social-emotional`, `sdoh-civic-participation`, `sdoh-discrimination`, `sdoh-racism`, `sdoh-incarceration`, `sdoh-language`
- Rows: 1,111. Data updated: 2021-03-24. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DAE
- Description: [1] Status is determined using the baseline, final, and target value. The statuses used in Healthy People 2020 were: 1 - Target met or exceeded—One of the following applies: (i) At baseline, the target was not met or exceeded, and the most recent value was equal to or exceeded the target. (The percentage of targeted change achieved was equal to or greater than 100%.); (ii) The baseline and most recent values were equal to or exceeded the target. (The percentage of targeted change achieved was not assessed.) 2 - Improved—One of the following applies: (i) Movement was toward the target, standar…
- Sample row fields ($limit=1): `status`, `topic`, `objective_description`, `baseline_value`, `baseline_year`, `final_value`, `final_year`, `target`, `movement_toward_target_3`, `movement_away_from_baseline`, `movement_statistically`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `status` | Status [1] | number | [1] Status is determined using the baseline, final, and target value. The statuses used in Healthy People 2020 were: 1 - Target met or exceeded; 2 - Improved; 3 - Little or no detectable change; 4 - Got worse; 5 - Baseline only; 6 - Inform… |
| `topic` | Topic | text |  |
| `objective_description` | Objective Description | text |  |
| `baseline_value` | Baseline Value | text |  |
| `baseline_year` | Baseline Year | text |  |
| `final_value` | Final Value [2] | text | [2] The final value is generally based on data available on the Healthy People 2020 website as of January 2020. For objectives that are continuing into Healthy People 2030, more recent data are available on the Healthy People 2030 website:… |
| `final_year` | Final Year | text |  |
| `target` | Target | text |  |
| `movement_toward_target_3` | Movement Toward Target [3] | text | [3] For objectives that moved toward their targets, movement toward the target was measured as the percentage of targeted change achieved (unless the target was already met or exceeded at baseline): Percentage of targeted change achieved =… |
| `movement_away_from_baseline` | Movement Away From Baseline [4] (if movement not toward target) | text | [4] For objectives that were not improving, did not meet or exceed their targets, and did not move toward their targets, movement away from the baseline was measured as the magnitude of the percent change from baseline: Magnitude of percen… |
| `movement_statistically` | Movement Statistically Significant [5][6] | text | [5] Statistical significance was tested when the objective had a target, at least two data points (of unequal value), and available standard errors of the data. A normal distribution was assumed. All available digits were used to test stat… |

### f3a8-hmpp

**Healthy People 2020 Foundation Health Measures** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/f3a8-hmpp.json`
- Metadata: `GET https://data.cdc.gov/api/views/f3a8-hmpp.json`; page: https://data.cdc.gov/d/f3a8-hmpp
- Topics: Category: National Center for Health Statistics
- Tags: `healthy people 2020`, `sdoh-access-to-health-care`
- Rows: 378. Data updated: 2022-01-26. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DAE
- Description: The Foundation Health Measures component of the Healthy People 2020 (HP2020) Final Review includes data on 14 global summary measures used to monitor improvement in population health. See Technical Notes of the Foundation Health Measures in the HP2020 Final Review for additional information on the definition and construction of these measures included.
- Sample row fields ($limit=1): `measure_id`, `measure_statement_full`, `measures_statement_short`, `category`, `population`, `year`, `estimate`, `unit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `measure_id` | Measure_ID | text | ID for the 14 global summary measures used to monitor improvement in population health. |
| `measure_statement_full` | Measure_statement_full | text | Full FHM statement. |
| `measures_statement_short` | Measures_statement_short | text | Shorten FHM statement. |
| `category` | Category | text | Overarching categories for grouping the FHMs. |
| `population` | Population | text | Populations included are total, male and female. |
| `year` | Year | text | Data year pertaining to the estimate. |
| `estimate` | Estimate | number | Calculated estimate of the measure. |
| `se` | SE | number | Calculated standard error of the estimate. A blank cell indicates that the standard error was not available for this calculation. |
| `unit` | Unit | text | Unit of measurement for the estimate. |
| `flag` | Flag | text | Additional information pertaining to the estimate. See the footnotes in the source table for more information. |

### fdpm-fddm

**Healthy People 2020 Overview of Health Disparities** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/fdpm-fddm.json`
- Metadata: `GET https://data.cdc.gov/api/views/fdpm-fddm.json`; page: https://data.cdc.gov/d/fdpm-fddm
- Topics: Category: National Center for Health Statistics
- Tags: `healthy people 2020`, `health disparities`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-higher-education`, `sdoh-literacy`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-housing-quality`, `sdoh-crime-violence`, `sdoh-environmental`, `sdoh-workplace`, `sdoh-civic-participation`, `sdoh-discrimination`, `sdoh-racism`, `sdoh-incarceration`, `sdoh-transportation`, `sdoh-social-emotional`, `sdoh-health-literacy`, `sdoh-food-access`, `sdoh-language`, `sdoh-access-to-health-care`, `sdoh-poverty-income`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-early-childhood`
- Rows: 2,030. Data updated: 2022-03-08. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DAE
- Description: The Overview of Health Disparities analysis is a component of the Healthy People 2020 (HP2020) Final Review. The analysis included 611 objectives in HP2020. This file contains summary level information used for the evaluation of changes in disparities during HP2020, including calculations for the disparities measures and the disparities change categories for all objectives and population characteristics in the analysis. See Technical Notes for the Healthy People 2020 Overview of Health Disparities (https://www.cdc.gov/nchs/healthy_people/hp2020/health-disparities-technical-notes.htm) for addi…
- Sample row fields ($limit=1): `hp2020_objective`, `objective_description`, `topic_area`, `population_characteristic`, `number_of_population_groups`, `best_rate_baseline_year_s`, `standard_error_of_best_rate`, `population_group_with_the`, `average_of_other_rates`, `standard_error_of_average`, `rate_ratio_baseline_year`, `standard_error_of_rate_ratio`, `best_rate_final_year_s`, `standard_error_of_best_rate_1`, `population_group_with_the_1`, `average_of_other_rates_final`, `standard_error_of_average_1`, `rate_ratio_final_year_s`, `standard_error_of_rate_ratio_1`, `difference_in_the_rate_ratio`, `z_score_of_the_difference`, `disparities_change_over_time`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `hp2020_objective` | HP2020 objective | text | The analysis included 611 HP2020 objectives that met the criteria for the population characteristics in the disparities analysis (see Technical Notes). |
| `objective_description` | Objective description | text |  |
| `topic_area` | Topic area | text | The HP2020 topic area corresponding to the objective included in the disparities analysis. |
| `population_characteristic` | Population characteristic | text | Population characteristics included in the disparities analysis are sex, race and ethnicity, educational attainment, family income, disability status, and geographic location. |
| `number_of_population_groups` | Number of population groups | number | Number of population groups included in the disparities analysis for the corresponding population characteristic at the baseline and final data points. |
| `best_rate_baseline_year_s` | Best rate, baseline year(s) | number | Value of the best population-group rate (most favorable, least adverse) for the corresponding population characteristic at the baseline data point in the disparities analysis. |
| `standard_error_of_best_rate` | Standard error of best rate, baseline year(s) | number | Standard error of the best population-group rate (most favorable, least adverse) for the corresponding population characteristic for the baseline data point in the disparities analysis. A blank cell indicates that the standard error was no… |
| `population_group_with_the` | Population group with the best rate, baseline year(s) | text | Population group with the best rate for the corresponding population characteristic at the baseline data point in the disparities analysis. |
| `average_of_other_rates` | Average of other rates, baseline year(s) | number | Average rate of all other groups (if the number of population groups is three or more) besides the group with the best rate for the corresponding population characteristic at the baseline data point in the disparities analysis. If only two… |
| `standard_error_of_average` | Standard error of average of other rates, baseline year(s) | number | Standard error of the average rate of all other groups (if the number of population groups is three or more) besides the group with the best rate for the corresponding population characteristic at the baseline data point in the disparities… |
| `rate_ratio_baseline_year` | Rate ratio, baseline year(s) | number | Ratio of the best group rate to the average of the other group rates (if the number of population groups is three or more) for the baseline data point in the disparities analysis. If only two population groups are included for the characte… |
| `standard_error_of_rate_ratio` | Standard error of rate ratio, baseline year(s) | number | Standard error of the ratio comparing the best group rate with the average of the other group rates (if the number of population groups is three or more) for the baseline data point in the disparities analysis. If only two population group… |
| `best_rate_final_year_s` | Best rate, final year(s) | number | Value of the best population-group rate (most favorable, least adverse) for the corresponding population characteristic at the final data point in the disparities analysis. |
| `standard_error_of_best_rate_1` | Standard error of best rate, final year(s) | number | Standard error of the best population-group rate (most favorable, least adverse) for the corresponding population characteristic at the final data point in the disparities analysis. A blank cell indicates that the standard error was not av… |
| `population_group_with_the_1` | Population group with the best rate, final year(s) | text | Population group category name with the best rate for the corresponding population characteristic at the final data point in the disparities analysis. |
| `average_of_other_rates_final` | Average of other rates, final year(s) | number | Average rate of all other groups (if the number of population groups is three or more) besides the group with the best rate for the corresponding population characteristic at the final data point in the disparities analysis. If only two po… |
| `standard_error_of_average_1` | Standard error of average of other rates, final year(s) | number | Standard error of the average rate of all other groups (if the number of population groups is three or more) besides the group with the best rate for the corresponding population characteristic at the final data point in the disparities an… |
| `rate_ratio_final_year_s` | Rate ratio, final year(s) | number | Ratio of the best group rate to the average of the other group rates (if the number of population groups is three or more) for the final data point in the disparities analysis. If only two population groups are included for the characteris… |
| `standard_error_of_rate_ratio_1` | Standard error of rate ratio, final year(s) | number | Standard error of the ratio comparing the best group rate with the average of the other group rates (if the number of population groups is three or more) for the final data point in the disparities analysis. If only two population groups a… |
| `difference_in_the_rate_ratio` | Difference in the rate ratio over time | number | Absolute difference in the rate ratio between the final and baseline data point in the disparities analysis. A blank cell indicates that the difference in the rate ratio could not be calculated. |
| `z_score_of_the_difference` | z score of the difference | number | z score corresponding to the difference in the rate ratio between the final and baseline data point in the disparities analysis. A blank cell indicates that the z score was not calculated. |
| `disparities_change_over_time` | Disparities change over time status | text | Status category indicating whether the disparity had a decrease, showed little or no detectable change, or had an increase between the baseline and final data point in the disparities analysis. |

### gjsp-ircr

**HUS_Footnote_Look_Up_ASTHCH** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/gjsp-ircr.json`
- Metadata: `GET https://data.cdc.gov/api/views/gjsp-ircr.json`; page: https://data.cdc.gov/d/gjsp-ircr
- Topics: Category: National Center for Health Statistics
- Tags: `asthma`, `asthma attack`, `immune system diseases`, `respiratory tract diseases`, `lung diseases`, `bronchial diseases`, `respiratory hypersensitivity`, `children`, `adolescents`, `age group`, `race`, `race and hispanic origin`, `sex`, `health insurance status`, `poverty level`, `american indian and alaska native`, `asian`, `black`, `native hawaiian or other pacific islander`, `white`, `hispanic`, `non-hispanic`, `female`, `male`, `private health insurance`, `medicaid`, `uninsured`, `national health interview survey`, `nhis`, `health us`, `sdoh-poverty-income`, `sdoh-access-to-health-care`
- Rows: 10. Data updated: 2024-09-27. Probe status: 200.
- Description: Footnotes for Health, US - Asthma in children younger than age 18, by selected characteristics: United States. Data on asthma in children younger than age 18 in the United States, by selected characteristics. Data are from Health, United States. Source: National Center for Health Statistics, National Health Interview Survey.
- Sample row fields ($limit=1): `fn_id`, `fn_text`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `fn_id` | FN_ID | text | Footnote ID |
| `fn_text` | FN_TEXT | text | Footnote Text Description |

### 8pt5-q6wp

**Indicators of Anxiety or Depression Based on Reported Frequency of Symptoms During Last 7 Days** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8pt5-q6wp.json`
- Metadata: `GET https://data.cdc.gov/api/views/8pt5-q6wp.json`; page: https://data.cdc.gov/d/8pt5-q6wp
- Topics: Category: National Center for Health Statistics
- Tags: `depression`, `anxiety`, `covid-19`
- Rows: 16,794. Data updated: 2024-10-04. Probe status: 200.
- Update frequency: R/P2W.
- Source: NCHS/DHIS
- Description: The U.S. Census Bureau, in collaboration with five federal agencies, launched the Household Pulse Survey to produce data on the social and economic impacts of Covid-19 on American households. The Household Pulse Survey was designed to gauge the impact of the pandemic on employment status, consumer spending, food security, housing, education disruptions, and dimensions of physical and mental wellness. The survey was designed to meet the goal of accurate and timely weekly estimates. It was conducted by an internet questionnaire, with invitations to participate sent by email and text message. Th…
- Sample row fields ($limit=1): `indicator`, `group`, `state`, `subgroup`, `phase`, `time_period`, `time_period_label`, `time_period_start_date`, `time_period_end_date`, `value`, `lowci`, `highci`, `confidence_interval`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | Indicator | text |  |
| `group` | Group | text |  |
| `state` | State | text |  |
| `subgroup` | Subgroup | text |  |
| `phase` | Phase | text |  |
| `time_period` | Time Period | text |  |
| `time_period_label` | Time Period Label | text |  |
| `time_period_start_date` | Time Period Start Date | calendar_date |  |
| `time_period_end_date` | Time Period End Date | calendar_date |  |
| `value` | Value | number |  |
| `lowci` | Low CI | number |  |
| `highci` | High CI | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `quartile_range` | Quartile Range | text |  |

### jb9g-gnvr

**Indicators of Health Insurance Coverage at the Time of Interview** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/jb9g-gnvr.json`
- Metadata: `GET https://data.cdc.gov/api/views/jb9g-gnvr.json`; page: https://data.cdc.gov/d/jb9g-gnvr
- Topics: Category: National Center for Health Statistics
- Tags: `uninsured`, `public coverage`, `private coverage`, `covid-19`, `sdoh-access-to-health-care`
- Rows: 16,056. Data updated: 2024-10-04. Probe status: 200.
- Update frequency: R/P2W.
- Source: NCHS/DHIS
- Description: The U.S. Census Bureau, in collaboration with five federal agencies, launched the Household Pulse Survey to produce data on the social and economic impacts of Covid-19 on American households. The Household Pulse Survey was designed to gauge the impact of the pandemic on employment status, consumer spending, food security, housing, education disruptions, and dimensions of physical and mental wellness. The survey was designed to meet the goal of accurate and timely weekly estimates. It was conducted by an internet questionnaire, with invitations to participate sent by email and text message. Th…
- Sample row fields ($limit=1): `indicator`, `group`, `state`, `subgroup`, `phase`, `time_period`, `time_period_label`, `time_period_start_date`, `time_period_end_date`, `value`, `lowci`, `highci`, `confidence_interval`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | Indicator | text |  |
| `group` | Group | text |  |
| `state` | State | text |  |
| `subgroup` | Subgroup | text |  |
| `phase` | Phase | text |  |
| `time_period` | Time Period | text |  |
| `time_period_label` | Time Period Label | text |  |
| `time_period_start_date` | Time Period Start Date | calendar_date |  |
| `time_period_end_date` | Time Period End Date | calendar_date |  |
| `value` | Value | number |  |
| `lowci` | Low CI | number |  |
| `highci` | High CI | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `quartile_range` | Quartile Range | text |  |
| `quartile_number` | Quartile Number | text |  |
| `suppression_flag` | Suppression Flag | text |  |

### xb3p-q62w

**Indicators of Reduced Access to Care Due to the Coronavirus Pandemic During Last 4 Weeks** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/xb3p-q62w.json`
- Metadata: `GET https://data.cdc.gov/api/views/xb3p-q62w.json`; page: https://data.cdc.gov/d/xb3p-q62w
- Topics: Category: National Center for Health Statistics
- Tags: `delayed care`, `unmet need`, `covid-19`, `sdoh-access-to-health-care`
- Rows: 7,118. Data updated: 2021-07-14. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DHIS
- Description: The U.S. Census Bureau, in collaboration with five federal agencies, launched the Household Pulse Survey to produce data on the social and economic impacts of Covid-19 on American households. The Household Pulse Survey was designed to gauge the impact of the pandemic on employment status, consumer spending, food security, housing, education disruptions, and dimensions of physical and mental wellness. The survey was designed to meet the goal of accurate and timely weekly estimates. It was conducted by an internet questionnaire, with invitations to participate sent by email and text message. Th…
- Sample row fields ($limit=1): `indicator`, `group`, `state`, `subgroup`, `phase`, `time_period`, `time_period_label`, `time_period_start_date`, `time_period_end_date`, `value`, `lowci`, `highci`, `confidence_interval`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | Indicator | text |  |
| `group` | Group | text |  |
| `state` | State | text |  |
| `subgroup` | Subgroup | text |  |
| `phase` | Phase | text |  |
| `time_period` | Time Period | text |  |
| `time_period_label` | Time Period Label | text |  |
| `time_period_start_date` | Time Period Start Date | calendar_date |  |
| `time_period_end_date` | Time Period End Date | calendar_date |  |
| `value` | Value | number |  |
| `lowci` | Low CI | number |  |
| `highci` | High CI | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `quartile_range` | Quartile Range | text |  |

### nfuu-hu6j

**Infant, neonatal, postneonatal, fetal, and perinatal mortality rates, by detailed race and Hispanic origin of mother: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/nfuu-hu6j.json`
- Metadata: `GET https://data.cdc.gov/api/views/nfuu-hu6j.json`; page: https://data.cdc.gov/d/nfuu-hu6j
- Topics: Category: National Center for Health Statistics
- Tags: `alaskan natives`, `american natives`, `african americans`, `fetal death`, `hispanic americans`, `infant`, `mortality`, `mothers`, `european continental ancestry group`, `asian continental ancestry group`, `oceanic ancestry group`, `continental population groups`, `live birth`, `infant death`, `pregnancy`, `pregnancy complications`, `death`, `health us`
- Rows: 2,688. Data updated: 2022-04-27. Probe status: 200.
- Source: NCHS/DAE
- Description: Data on infant, neonatal, postneonatal, fetal, and perinatal mortality rates by selected characteristics of the mother. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder (https://www.cdc.gov/nchs/hus/contents2019.htm) for critical information about measures, definitions, and changes over time. SOURCE: NCHS, National Vital Statistics System, public-use Linked Birth/Infant Death Data Set, public-use Fetal Death File, and public-use Birth File. For more information on the National Vital Statistics System, see the corresponding Appendix entry at https://www.cdc.go…
- Sample row fields ($limit=1): `indicator`, `indicator_num`, `unit`, `unit_num`, `stub_name`, `stub_name_num`, `stub_label`, `stub_label_num`, `year`, `year_num`, `estimate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | INDICATOR | text | Measure being estimated. |
| `indicator_num` | INDICATOR_NUM | text | Numeric code for levels of INDICATOR that may be used for easier coding or formatting of the INDICATOR variable. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `year` | YEAR | text | Data year or range of data years pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnotes in the source table (Excel) for more information. |

### w4cs-jspc

**Initial injury-related visits to hospital emergency departments, by sex, age, and intent and mechanism of injury: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/w4cs-jspc.json`
- Metadata: `GET https://data.cdc.gov/api/views/w4cs-jspc.json`; page: https://data.cdc.gov/d/w4cs-jspc
- Topics: Category: National Center for Health Statistics
- Tags: `accidental falls`, `emergency service`, `hospital`, `hospitals`, `sex`, `wounds and injuries`, `age`, `disasters`, `health us`, `sdoh-use-of-health-care`
- Rows: 1,880. Data updated: 2022-04-28. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DAE
- Description: <strong>On December 20 2021, all estimates and standard errors for 2017–2018 were revised in this table to correct programming errors.</strong> Data on initial injury-related visits to hospital emergency departments, by sex, age, and intent and mechanism of injury. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder (https://www.cdc.gov/nchs/hus/contents2019.htm) for critical information about measures, definitions, and changes over time. Due to a change in national medical data coding standards in 2015, from the International Classification of Diseases, 9th Rev…
- Sample row fields ($limit=1): `indicator`, `unit`, `unit_num`, `stub_name`, `stub_name_num`, `stub_label`, `stub_label_num`, `year`, `year_num`, `age`, `age_num`, `flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | INDICATOR | text | Measure being estimated. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `year` | YEAR | text | Data year or range of data years pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `age` | AGE | text | Age group pertaining to the estimate. |
| `age_num` | AGE_NUM | number | Numeric code for levels of AGE that may be used for easier coding or formatting of the AGE variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnotes in the source table (Excel) for more information. |

### mnaa-qctp

**Lack of Social Connection** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/mnaa-qctp.json`
- Metadata: `GET https://data.cdc.gov/api/views/mnaa-qctp.json`; page: https://data.cdc.gov/d/mnaa-qctp
- Topics: Category: National Center for Health Statistics
- Tags: `hps`, `social isolation and loneliness`, `social determinants of health (sdoh)`, `social-emotional`
- Rows: 5,460. Data updated: 2024-10-04. Probe status: 200.
- Update frequency: R/P1M.
- Source: NCHS/DHIS
- Description: In 2020, the National Center for Health Statistics (NCHS) partnered with the Census Bureau on an experimental data system called the Household Pulse Survey. This survey was designed to complement the ability of the federal statistical system to rapidly respond and provide relevant information about how emergent issues are impacting American households. Beginning in Phase 4.0 (on January 9, 2024), questions on social support, loneliness, and social isolation were added to the survey. These questions have been included on other nationally representative surveys. Briefly, the question on social…
- Sample row fields ($limit=1): `indicator`, `group`, `state`, `subgroup`, `phase`, `time_period`, `time_period_label`, `time_period_start_date`, `time_period_end_date`, `value`, `low_ci`, `high_ci`, `confidence_interval`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | Indicator | text |  |
| `group` | Group | text |  |
| `state` | State | text |  |
| `subgroup` | Subgroup | text |  |
| `phase` | Phase | text |  |
| `time_period` | Time Period | text |  |
| `time_period_label` | Time Period Label | text |  |
| `time_period_start_date` | Time Period Start Date | calendar_date |  |
| `time_period_end_date` | Time Period End Date | calendar_date |  |
| `value` | Value | number |  |
| `low_ci` | Low CI | number |  |
| `high_ci` | High CI | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `quartile_range` | Quartile Range | text |  |
| `suppression_flag` | Suppression Flag | number |  |
| `quartile_number` | Quartile Number | number |  |

### 3j26-kg6d

**Long-term Care and COVID-19** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3j26-kg6d.json`
- Metadata: `GET https://data.cdc.gov/api/views/3j26-kg6d.json`; page: https://data.cdc.gov/d/3j26-kg6d
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `long-term care`, `residential care communities`, `adult day services centers`
- Rows: 830. Data updated: 2022-09-12. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DHCS
- Description: The NCHS National Post-acute and Long-term Care Study (NPALS) collects data on long-term care every two years for all 50 states and the District of Columbia to monitor the diverse post-acute and long-term care fields. The 2020 survey provided an opportunity to collect COVID-19-related data for residential care communities and adult day services centers, important long-term care settings. These data are not available from other data systems. These data are related to experiences of COVID-19 from January 2020 through mid-July 2021, including the number of COVID-19 cases, hospitalizations, and d…
- Sample row fields ($limit=1): `figure_number`, `setting`, `select_measure`, `select_measure_2`, `response_category`, `population`, `value_type`, `reporting_period`, `select_group`, `value`, `low_95_ci`, `high_95_ci`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `figure_number` | Figure Number | number | Corresponds to Figures reported on https://www.cdc.gov/nchs/covid19/npals.htm |
| `setting` | Setting | text | Indicates the long-term care setting: Residential Care Community or Adult Day Services Center |
| `select_measure` | Select Measure | text | Name of the measure of interest |
| `select_measure_2` | Select Measure 2 | text | Name of the second cross-tabulated measure of interest, if applicable |
| `response_category` | Response category | text | The response options of the measure, if applicable |
| `population` | Population | text | The population measured: Resident/Participant or Staff |
| `value_type` | Value type | text | Whether the estimate is a number or percentage |
| `reporting_period` | Reporting Period | text | Reporting Period |
| `select_group` | Select Group | text | Indicates the grouping variable: Census Region or Metropolitan Statistical Area |
| `value` | Value | number | The estimate of the measure |
| `low_95_ci` | Low 95% CI | number | Lower limit of 95% confidence interval |
| `high_95_ci` | High 95% CI | number | Upper limit of 95% confidence interval |
| `reliability` | Reliability | text | * Estimate does not meet NCHS data presentation standards for reliable proportions and should be interpreted cautiously. |

### qgkx-mswu

**Loss of Work Due to Illness from COVID-19** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/qgkx-mswu.json`
- Metadata: `GET https://data.cdc.gov/api/views/qgkx-mswu.json`; page: https://data.cdc.gov/d/qgkx-mswu
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `rands`, `sdoh-employment`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-workplace`
- Rows: 57. Data updated: 2021-08-06. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DRM
- Description: The Research and Development Survey (RANDS) is a platform designed for conducting survey question evaluation and statistical research. RANDS is an ongoing series of surveys from probability-sampled commercial survey panels used for methodological research at the National Center for Health Statistics (NCHS). RANDS estimates are generated using an experimental approach that differs from the survey design approaches generally used by NCHS, including possible biases from different response patterns and sampling frames as well as increased variability from lower sample sizes. Use of the RANDS plat…
- Sample row fields ($limit=1): `round`, `indicator`, `group`, `subgroup`, `sample_size`, `percent`, `standard_error`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `round` | Round | number | Data collection period; Round 1 occurred June 9, 2020–July 6, 2020, Round 2 occurred August 3, 2020–August 20, 2020, and Round 3 occurred May 17, 2021–June 30, 2021 |
| `indicator` | Indicator | text | Unable to work due to self or family member having COVID-19 |
| `group` | Group | text | Estimates were reported at the national level (total) and by age group, race and Hispanic origin, sex, education level, urbanization, and selected chronic conditions. |
| `subgroup` | Subgroup | text | Subcategories for each group |
| `sample_size` | Sample Size | number | Sample size |
| `percent` | Percent | number | Percent estimate |
| `standard_error` | Standard Error | number | Standard error estimate |
| `suppression` | Suppression | text | Identifies percent and standard error estimates that did not meet NCHS Data Presentation Standards for Proportions |
| `significant_1` | Significant 1 | number | Indicator for significance testing of difference from Round 1 where a value of 0 indicates the estimates are not statistically significantly different at the 5% significance level and a value of 1 indicates that the estimates are statistic… |
| `significant_2` | Significant 2 | number | Indicator for significance testing of difference from Round 2 where a value of 0 indicates the estimates are not statistically significantly different at the 5% significance level and a value of 1 indicates that the estimates are statistic… |

### km5s-4339

**Medicaid coverage among persons under age 65, by selected characteristics: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/km5s-4339.json`
- Metadata: `GET https://data.cdc.gov/api/views/km5s-4339.json`; page: https://data.cdc.gov/d/km5s-4339
- Topics: Category: National Center for Health Statistics
- Tags: `alaskan natives`, `american natives`, `african americans`, `divorce`, `hispanic americans`, `medicaid`, `poverty`, `sex`, `marital status`, `european continental ancestry group`, `asian continental ancestry group`, `oceanic ancestry group`, `continental population groups`, `age`, `health insurance`, `health us`, `sdoh-poverty-income`, `sdoh-access-to-health-care`
- Rows: 1,917. Data updated: 2022-04-28. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DAE
- Description: Data on Medicaid coverage among persons under age 65 by selected population characteristics. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder (https://www.cdc.gov/nchs/hus/contents2019.htm) for critical information about measures, definitions, and changes over time. SOURCE: NCHS, National Health Interview Survey, health insurance supplements (1984, 1989, 1994-1996). Starting with 1997, data are from the family core and the sample adult questionnaires. Data for level of difficulty are from the 2010 Quality of Life, 2011-2017 Functioning and Disability, and 201…
- Sample row fields ($limit=1): `indicator`, `unit`, `unit_num`, `stub_name`, `stub_name_num`, `stub_label`, `stub_label_num`, `year`, `year_num`, `age`, `age_num`, `estimate`, `flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | INDICATOR | text | Measure being estimated. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `year` | YEAR | text | Data year or range of data years pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `age` | AGE | text | Age group pertaining to the estimate. |
| `age_num` | AGE_NUM | number | Numeric code for levels of AGE that may be used for easier coding or formatting of the AGE variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `se` | SE | number | Calculated standard error of the estimate. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnotes in the source table (Excel) for more information. |

### yni7-er2q

**Mental Health Care in the Last 4 Weeks** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/yni7-er2q.json`
- Metadata: `GET https://data.cdc.gov/api/views/yni7-er2q.json`; page: https://data.cdc.gov/d/yni7-er2q
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `mental health`, `sdoh-use-of-health-care`
- Rows: 10,404. Data updated: 2022-11-28. Probe status: 200.
- Update frequency: R/P2W.
- Source: NCHS/DHIS
- Description: The U.S. Census Bureau, in collaboration with five federal agencies, launched the Household Pulse Survey to produce data on the social and economic impacts of Covid-19 on American households. The Household Pulse Survey was designed to gauge the impact of the pandemic on employment status, consumer spending, food security, housing, education disruptions, and dimensions of physical and mental wellness. The survey was designed to meet the goal of accurate and timely weekly estimates. It was conducted by an internet questionnaire, with invitations to participate sent by email and text message. Th…
- Sample row fields ($limit=1): `indicator`, `group`, `state`, `subgroup`, `phase`, `time_period`, `time_period_label`, `time_period_start_date`, `time_period_end_date`, `value`, `lowci`, `highci`, `confidence_interval`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | Indicator | text |  |
| `group` | Group | text |  |
| `state` | State | text |  |
| `subgroup` | Subgroup | text |  |
| `phase` | Phase | text |  |
| `time_period` | Time Period | number |  |
| `time_period_label` | Time Period Label | text |  |
| `time_period_start_date` | Time Period Start Date | calendar_date |  |
| `time_period_end_date` | Time Period End Date | calendar_date |  |
| `value` | Value | number |  |
| `lowci` | LowCI | number |  |
| `highci` | HighCI | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `quartile_range` | Quartile Range | text |  |
| `suppression_flag` | Suppression Flag | text |  |

### bxq8-mugm

**Monthly Counts of Deaths by Select Causes, 2014-2019** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/bxq8-mugm.json`
- Metadata: `GET https://data.cdc.gov/api/views/bxq8-mugm.json`; page: https://data.cdc.gov/d/bxq8-mugm
- Topics: Category: National Center for Health Statistics
- Tags: `monthly`, `deaths`, `mortality`, `united states`, `all causes`, `nchs`, `nvss`, `causes of death`, `natural cause`, `cancer`, `diabetes`, `alzheimer disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `respiratory disease`, `kidney disease`, `diseases of heart`, `cerebrovascular disease`, `motor vehicle accidents`, `unintentional injuries`, `suicide`, `homicide`, `drug overdose`, `septicemia`
- Rows: 72. Data updated: 2021-02-03. Probe status: 200.
- Update frequency: R/P1M.
- Source: NCHS/DVS
- Description: Final counts of deaths by the month the deaths occurred and by select causes of death for 2014-2019.
- Sample row fields ($limit=1): `jurisdiction_of_occurrence`, `year`, `month`, `all_cause`, `natural_cause`, `septicemia`, `malignant_neoplasms`, `diabetes_mellitus`, `alzheimer_disease`, `influenza_and_pneumonia`, `chronic_lower_respiratory`, `other_diseases_of_respiratory`, `nephritis_nephrotic_syndrom`, `symptoms_signs_and_abnormal`, `diseases_of_heart`, `cerebrovascular_diseases`, `accidents_unintentional`, `motor_vehicle_accidents`, `intentional_self_harm_suicide`, `assault_homicide`, `drug_overdose`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text | Jurisdiction of Occurrence |
| `year` | Year | number | Year |
| `month` | Month | number | Month |
| `all_cause` | All Cause | number | AllCause |
| `natural_cause` | Natural Cause | number | NaturalCause (A00-R99) |
| `septicemia` | Septicemia | number | Septicemia (A40-A41) |
| `malignant_neoplasms` | Malignant Neoplasms | number | Malignant neoplasms (C00-C97) |
| `diabetes_mellitus` | Diabetes Mellitus | number | Diabetes mellitus (E10-E14) |
| `alzheimer_disease` | Alzheimer Disease | number | Alzheimer disease (G30) |
| `influenza_and_pneumonia` | Influenza and Pneumonia | number | Influenza and pneumonia (J10-J18) |
| `chronic_lower_respiratory` | Chronic Lower Respiratory Diseases | number | Chronic lower respiratory diseases (J40-J47) |
| `other_diseases_of_respiratory` | Other Diseases of Respiratory System | number | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) |
| `nephritis_nephrotic_syndrom` | Nephritis, Nephrotic Syndrome, and Nephrosis | number | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) |
| `symptoms_signs_and_abnormal` | Symptoms, Signs, and Abnormal Clinical and Laboratory Findings, Not Elsewhere Classified | number | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) |
| `diseases_of_heart` | Diseases of Heart | number | Diseases of heart (I00-I09,I11,I13,I20-I51) |
| `cerebrovascular_diseases` | Cerebrovascular Diseases | number | Cerebrovascular diseases (I60-I69) |
| `accidents_unintentional` | Accidents (Unintentional Injuries) | number | Accidents (Unintentional Injuries) (V01-X59,Y85-Y86) |
| `motor_vehicle_accidents` | Motor Vehicle Accidents | number | Motor Vehicle Accidents (V01-V99,Y85) |
| `intentional_self_harm_suicide` | Intentional Self-Harm (Suicide) | number | Intentional Self-Harm (Suicide) (U03,X60-X84,Y87.0) |
| `assault_homicide` | Assault (Homicide) | number | Assault (Homicide) (U01-U02,X85-Y09,Y87.1) |
| `drug_overdose` | Drug Overdose | number | Drug Overdose |

### 9dzk-mvmi

**Monthly Provisional Counts of Deaths by Select Causes, 2020-2023** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/9dzk-mvmi.json`
- Metadata: `GET https://data.cdc.gov/api/views/9dzk-mvmi.json`; page: https://data.cdc.gov/d/9dzk-mvmi
- Topics: Category: National Center for Health Statistics
- Tags: `monthly`, `mortality`, `nvss`, `deaths`, `provisional`, `nchs`, `united states`, `covid-19`, `coronavirus`, `all causes`, `causes of death`, `natural cause`, `septicemia`, `cancer`, `diabetes`, `alzheimer disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `respiratory disease`, `kidney disease`, `diseases of heart`, `cerebrovascular disease`, `unintentional injuries`, `homicide`, `suicide`, `motor vehicle accidents`, `drug overdose`
- Rows: 45. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: R/P1W.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. Provisional counts of deaths by the month the death occurred and by select causes of death for 2020-2023.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `jurisdiction_of_occurrence`, `year`, `month`, `all_cause`, `natural_cause`, `septicemia`, `malignant_neoplasms`, `diabetes_mellitus`, `alzheimer_disease`, `influenza_and_pneumonia`, `chronic_lower_respiratory`, `other_diseases_of_respiratory`, `nephritis_nephrotic_syndrome`, `symptoms_signs_and_abnormal`, `diseases_of_heart`, `cerebrovascular_diseases`, `accidents_unintentional`, `motor_vehicle_accidents`, `intentional_self_harm_suicide`, `assault_homicide`, `drug_overdose`, `covid_19_multiple_cause_of`, `covid_19_underlying_cause`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text | Jurisdiction of Occurrence |
| `year` | Year | number | Year |
| `month` | Month | number | Month |
| `all_cause` | All Cause | number | AllCause |
| `natural_cause` | Natural Cause | number | NaturalCause (A00-R99,U07) |
| `septicemia` | Septicemia | number | Septicemia (A40-A41) |
| `malignant_neoplasms` | Malignant Neoplasms | number | Malignant neoplasms (C00-C97) |
| `diabetes_mellitus` | Diabetes Mellitus | number | Diabetes mellitus (E10-E14) |
| `alzheimer_disease` | Alzheimer Disease | number | Alzheimer disease (G30) |
| `influenza_and_pneumonia` | Influenza and Pneumonia | number | Influenza and pneumonia (J10-J18) |
| `chronic_lower_respiratory` | Chronic Lower Respiratory Diseases | number | Chronic lower respiratory diseases (J40-J47) |
| `other_diseases_of_respiratory` | Other Diseases of Respiratory System | number | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) |
| `nephritis_nephrotic_syndrome` | Nephritis, Nephrotic Syndrome and Nephrosis | number | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) |
| `symptoms_signs_and_abnormal` | Symptoms, Signs and Abnormal Clinical and Laboratory Findings, Not Elsewhere Classified | number | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) |
| `diseases_of_heart` | Diseases of Heart | number | Diseases of heart (I00-I09,I11,I13,I20-I51) |
| `cerebrovascular_diseases` | Cerebrovascular Diseases | number | Cerebrovascular diseases (I60-I69) |
| `accidents_unintentional` | Accidents (Unintentional Injuries) | number | Accidents (Unintentional Injuries) (V01-X59,Y85-Y86) |
| `motor_vehicle_accidents` | Motor Vehicle Accidents | number | Motor Vehicle Accidents (V02–V04,V09.0, V09.2,V12–V14,V19.0–V19.2,V19.4–V19.6, V20–V79,V80.3–V80.5, V81.0–V81.1,V82.0–V82.1,V83–V86, V87.0–V87.8,V88.0–V88.8, V89.0,V89.2) |
| `intentional_self_harm_suicide` | Intentional Self-Harm (Suicide) | number | Intentional Self-Harm (Suicide) (U03,X60-X84,Y87.0) |
| `assault_homicide` | Assault (Homicide) | number | Assault (Homicide) (U01-U02,X85-Y09,Y87.1) |
| `drug_overdose` | Drug Overdose | number | Drug Overdose |
| `covid_19_multiple_cause_of` | COVID-19 (Multiple Cause of Death) | number | COVID-19 (U071, Multiple Cause of Death) |
| `covid_19_underlying_cause` | COVID-19 (Underlying Cause of Death) | number | COVID-19 (U071, Underlying Cause of Death) |
| `flag_accid` | flag_accid | text | Data not shown (6 month lag) |
| `flag_mva` | flag_mva | text | Data not shown (6 month lag) |
| `flag_suic` | flag_suic | text | Data not shown (6 month lag) |
| `flag_homic` | flag_homic | text | Data not shown (6 month lag) |
| `flag_drugod` | flag_drugod | text | Data not shown (6 month lag) |

### 6rkc-nb2q

**NCHS - Age-adjusted Death Rates for Selected Major Causes of Death** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/6rkc-nb2q.json`
- Metadata: `GET https://data.cdc.gov/api/views/6rkc-nb2q.json`; page: https://data.cdc.gov/d/6rkc-nb2q
- Topics: Category: National Center for Health Statistics
- Tags: `age-adjusted death rate`, `cause of death`, `mortality united states`, `nchs`
- Rows: 595. Data updated: 2020-09-08. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: This dataset of U.S. mortality trends since 1900 highlights trends in age-adjusted death rates for five selected major causes of death. Age-adjusted death rates (deaths per 100,000) after 1998 are calculated based on the 2000 U.S. standard population. Populations used for computing death rates for 2011–2017 are postcensal estimates based on the 2010 census, estimated as of July 1, 2010. Rates for census years are based on populations enumerated in the corresponding censuses. Rates for noncensus years between 2000 and 2010 are revised using updated intercensal population estimates and may diff…
- Sample row fields ($limit=1): `year`, `leading_causes`, `age_adjusted_death_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `leading_causes` | Cause | text | Selected Major Cause of Death |
| `age_adjusted_death_rate` | Age Adjusted Death Rate | number |  |

### yt7u-eiyg

**NCHS - Birth Rates for Females by Age Group: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/yt7u-eiyg.json`
- Metadata: `GET https://data.cdc.gov/api/views/yt7u-eiyg.json`; page: https://data.cdc.gov/d/yt7u-eiyg
- Topics: Category: National Center for Health Statistics
- Tags: `birth rates`, `age of mother`, `united states`, `nchs`
- Rows: 632. Data updated: 2020-01-27. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset includes birth rates for females by age group in the United States since 1940. The number of states in the reporting area differ historically. In 1915 (when the birth registration area was established), 10 states and the District of Columbia reported births; by 1933, 48 states and the District of Columbia were reporting births, with the last two states, Alaska and Hawaii, added to the registration area in 1959 and 1960, when these regions gained statehood. Reporting area information is detailed in references 1 and 2 below. Trend lines for 1909–1958 are based on live births adjust…
- Sample row fields ($limit=1): `year`, `age_group`, `birth_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | text |  |
| `age_group` | Age Group | text |  |
| `birth_rate` | Birth Rate | number |  |

### 6tkz-y37d

**NCHS - Birth Rates for Unmarried Women by Age, Race, and Hispanic Origin: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/6tkz-y37d.json`
- Metadata: `GET https://data.cdc.gov/api/views/6tkz-y37d.json`; page: https://data.cdc.gov/d/6tkz-y37d
- Topics: Category: National Center for Health Statistics
- Tags: `birth rates`, `race`, `ethnicity`, `hispanic origin`, `nonmarital`, `united states`, `nchs`
- Rows: 1,068. Data updated: 2017-08-23. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset includes birth rates for unmarried women by age group, race, and Hispanic origin in the United States since 1970. Methods for collecting information on marital status changed over the reporting period and have been documented in: • Ventura SJ, Bachrach CA. Nonmarital childbearing in the United States, 1940–99. National vital statistics reports; vol 48 no 16. Hyattsville, Maryland: National Center for Health Statistics. 2000. Available from: http://www.cdc.gov/nchs/data/nvsr/nvsr48/nvs48_16.pdf. • National Center for Health Statistics. User guide to the 2013 natality public use fi…
- Sample row fields ($limit=1): `year`, `age`, `race`, `birth_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `age` | Age Group | text |  |
| `race` | Race or Hispanic Origin | text |  |
| `birth_rate` | Birth Rate | number |  |

### rg8a-czmp

**NCHS - Birth Rates for Women Aged 15-17, 17-18, and 15-19: United States, 1960-2015** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/rg8a-czmp.json`
- Metadata: `GET https://data.cdc.gov/api/views/rg8a-czmp.json`; page: https://data.cdc.gov/d/rg8a-czmp
- Topics: Category: National Center for Health Statistics
- Tags: `birth rate`, `women`, `united states`, `nchs`, `u.s. teen birth rate`, `teen births`
- Rows: 168. Data updated: 2017-08-15. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset assembles all final birth data for females aged 15–19, 15–17, and 18–19 for the United States.
- Sample row fields ($limit=1): `year`, `age_group`, `birth_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `age_group` | Age Group | text |  |
| `birth_rate` | Birth Rate | number |  |

### e6fc-ccez

**NCHS - Births and General Fertility Rates: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/e6fc-ccez.json`
- Metadata: `GET https://data.cdc.gov/api/views/e6fc-ccez.json`; page: https://data.cdc.gov/d/e6fc-ccez
- Topics: Category: National Center for Health Statistics
- Tags: `birth rate`, `fertility rate`, `united states`, `nchs`
- Rows: 110. Data updated: 2020-01-27. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset includes crude birth rates and general fertility rates in the United States since 1909. The number of states in the reporting area differ historically. In 1915 (when the birth registration area was established), 10 states and the District of Columbia reported births; by 1933, 48 states and the District of Columbia were reporting births, with the last two states, Alaska and Hawaii, added to the registration area in 1959 and 1960, when these regions gained statehood. Reporting area information is detailed in references 1 and 2 below. Trend lines for 1909–1958 are based on live birt…
- Sample row fields ($limit=1): `year`, `birth_number`, `general_fertility_rate`, `crude_birth_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | text |  |
| `birth_number` | Birth Number | number |  |
| `general_fertility_rate` | General Fertility Rate | number |  |
| `crude_birth_rate` | Crude Birth Rate | number |  |

### g6qk-ngsf

**NCHS - Births to Unmarried Women by Age Group: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/g6qk-ngsf.json`
- Metadata: `GET https://data.cdc.gov/api/views/g6qk-ngsf.json`; page: https://data.cdc.gov/d/g6qk-ngsf
- Topics: Category: National Center for Health Statistics
- Tags: `births`, `nonmarital`, `united states`, `nchs`
- Rows: 469. Data updated: 2017-08-23. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset includes number of births to unmarried women by age group in the United States since 1940. Methods for collecting information on marital status changed over the reporting period and have been documented in: • Ventura SJ, Bachrach CA. Nonmarital childbearing in the United States, 1940–99. National vital statistics reports; vol 48 no 16. Hyattsville, Maryland: National Center for Health Statistics. 2000. Available from: http://www.cdc.gov/nchs/data/nvsr/nvsr48/nvs48_16.pdf. • National Center for Health Statistics. User guide to the 2013 natality public use file. Hyattsville, Maryla…
- Sample row fields ($limit=1): `year`, `age_group`, `birth_number`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `age_group` | Age Group | text |  |
| `birth_number` | Number of Births | number |  |

### v6ab-adf5

**NCHS - Childhood Mortality Rates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/v6ab-adf5.json`
- Metadata: `GET https://data.cdc.gov/api/views/v6ab-adf5.json`; page: https://data.cdc.gov/d/v6ab-adf5
- Topics: Category: National Center for Health Statistics
- Tags: `children`, `death rates`, `mortality`, `united states`, `nchs`
- Rows: 476. Data updated: 2020-09-08. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: This dataset of U.S. mortality trends since 1900 highlights childhood mortality rates by age group for age at death. Age-adjusted death rates (deaths per 100,000) after 1998 are calculated based on the 2000 U.S. standard population. Populations used for computing death rates for 2011–2017 are postcensal estimates based on the 2010 census, estimated as of July 1, 2010. Rates for census years are based on populations enumerated in the corresponding censuses. Rates for noncensus years between 2000 and 2010 are revised using updated intercensal population estimates and may differ from rates previ…
- Sample row fields ($limit=1): `year`, `age_at_death`, `mortality_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `age_at_death` | Age Group | text | Age group based on age at death |
| `mortality_rate` | Death Rate | number |  |

### w9j2-ggv5

**NCHS - Death rates and life expectancy at birth** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/w9j2-ggv5.json`
- Metadata: `GET https://data.cdc.gov/api/views/w9j2-ggv5.json`; page: https://data.cdc.gov/d/w9j2-ggv5
- Topics: Category: National Center for Health Statistics
- Tags: `death rates`, `life expectancy`, `mortality`, `united states`, `nchs`
- Rows: 1,071. Data updated: 2020-09-08. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: This dataset of U.S. mortality trends since 1900 highlights the differences in age-adjusted death rates and life expectancy at birth by race and sex. Age-adjusted death rates (deaths per 100,000) after 1998 are calculated based on the 2000 U.S. standard population. Populations used for computing death rates for 2011–2017 are postcensal estimates based on the 2010 census, estimated as of July 1, 2010. Rates for census years are based on populations enumerated in the corresponding censuses. Rates for noncensus years between 2000 and 2010 are revised using updated intercensal population estimate…
- Sample row fields ($limit=1): `year`, `race`, `sex`, `average_life_expectancy`, `mortality`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `race` | Race | text |  |
| `sex` | Sex | text |  |
| `average_life_expectancy` | Average Life Expectancy (Years) | number |  |
| `mortality` | Age-adjusted Death Rate | number |  |

### pbkm-d27e

**NCHS - Drug Poisoning Mortality by County: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/pbkm-d27e.json`
- Metadata: `GET https://data.cdc.gov/api/views/pbkm-d27e.json`; page: https://data.cdc.gov/d/pbkm-d27e
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `drug poisoning`, `mortality`, `county`, `united states`, `nchs`
- Rows: 53,387. Data updated: 2017-04-11. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset describes drug poisoning deaths at the county level by selected demographic characteristics and includes age-adjusted death rates for drug poisoning from 1999 to 2015. Deaths are classified using the International Classification of Diseases, Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 (undetermined intent). Estimates are based on the National Vital Statistics System multiple cause-of-death mortality files (1). Age-adjusted death rates (deaths per…
- Sample row fields ($limit=1): `fips`, `year`, `state`, `st`, `fips_state`, `county`, `population`, `estimated_age_adjusted_death_rate_11_categories_in_ranges`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `fips` | FIPS | text |  |
| `year` | Year | number |  |
| `state` | State | text |  |
| `st` | ST | text |  |
| `fips_state` | FIPS State | text |  |
| `county` | County | text |  |
| `population` | Population | number |  |
| `estimated_age_adjusted_death_rate_11_categories_in_ranges` | Estimated Age-adjusted Death Rate, 16 Categories (in ranges) | text |  |

### rpvx-m2md

**NCHS - Drug Poisoning Mortality by County: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/rpvx-m2md.json`
- Metadata: `GET https://data.cdc.gov/api/views/rpvx-m2md.json`; page: https://data.cdc.gov/d/rpvx-m2md
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `drug poisoning`, `mortality`, `state`, `national`, `united states`, `nchs`
- Rows: 59,584. Data updated: 2023-04-20. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset describes drug poisoning deaths at the U.S. and state level by selected demographic characteristics, and includes age-adjusted death rates for drug poisoning. Deaths are classified using the International Classification of Diseases, Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 (undetermined intent). Estimates are based on the National Vital Statistics System multiple cause-of-death mortality files (1). Age-adjusted death rates (deaths per 100,000 U…
- Sample row fields ($limit=1): `fips`, `year`, `state`, `fipsstate`, `county`, `population`, `model_based_death_rate`, `standard_deviation`, `lower95ci`, `upper95ci`, `urbanrural`, `censusdivision`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `fips` | FIPS | number |  |
| `year` | Year | number |  |
| `state` | State | text |  |
| `fipsstate` | FIPS State | number |  |
| `county` | County | text |  |
| `population` | Population | number |  |
| `model_based_death_rate` | Model-based Death Rate | number |  |
| `standard_deviation` | Standard Deviation | number |  |
| `lower95ci` | Lower Confidence Limit | number |  |
| `upper95ci` | Upper Confidence Limit | number |  |
| `urbanrural` | Urban/Rural Category | text |  |
| `censusdivision` | Census Division | number |  |

### p56q-jrxg

**NCHS - Drug Poisoning Mortality by County: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/p56q-jrxg.json`
- Metadata: `GET https://data.cdc.gov/api/views/p56q-jrxg.json`; page: https://data.cdc.gov/d/p56q-jrxg
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `drug poisoning`, `mortality`, `county`, `united states`, `nchs`
- Rows: 56,448. Data updated: 2018-01-22. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset contains model-based county estimates for drug-poisoning mortality. Deaths are classified using the International Classification of Diseases, Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 (undetermined intent). Estimates are based on the National Vital Statistics System multiple cause-of-death mortality files (1). Age-adjusted death rates (deaths per 100,000 U.S. standard population for 2000) are calculated using the direct method. Populations used…
- Sample row fields ($limit=1): `fips`, `year`, `state`, `fips_state`, `county`, `population`, `estimated_age_adjusted_death_rate_16_categories_in_ranges`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `fips` | FIPS | number |  |
| `year` | Year | number |  |
| `state` | State | text |  |
| `fips_state` | FIPS State | number |  |
| `county` | County | text |  |
| `population` | Population | number |  |
| `estimated_age_adjusted_death_rate_16_categories_in_ranges` | Estimated Age-adjusted Death Rate, 16 Categories (in ranges) | text |  |

### xbxb-epbu

**NCHS - Drug Poisoning Mortality by State: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/xbxb-epbu.json`
- Metadata: `GET https://data.cdc.gov/api/views/xbxb-epbu.json`; page: https://data.cdc.gov/d/xbxb-epbu
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `drug poisoning`, `mortality`, `state`, `national`, `united states`, `nchs`
- Rows: 2,862. Data updated: 2018-06-04. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset describes drug poisoning deaths at the U.S. and state level by selected demographic characteristics, and includes age-adjusted death rates for drug poisoning. Deaths are classified using the International Classification of Diseases, Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 (undetermined intent). Estimates are based on the National Vital Statistics System multiple cause-of-death mortality files (1). Age-adjusted death rates (deaths per 100,000 U…
- Sample row fields ($limit=1): `state`, `year`, `sex`, `age_group`, `race_and_hispanic_origin`, `deaths`, `population`, `crude_death_rate`, `standard_error_for_crude_rate`, `lower_confidence_limit_for_crude_rate`, `upper_confidence_limit_for_crude_rate`, `age_adjusted_rate`, `standard_error_for_age_adjusted_rate`, `lower_confidence_limit_for_age_adjusted_rate`, `upper_confidence_limit_for_age_adjusted_rate`, `state_crude_rate_in_range`, `us_crude_rate`, `us_age_adjusted_rate`, `unit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `state` | State | text |  |
| `year` | Year | number |  |
| `sex` | Sex | text |  |
| `age_group` | Age Group | text |  |
| `race_and_hispanic_origin` | Race and Hispanic Origin | text |  |
| `deaths` | Deaths | number |  |
| `population` | Population | number |  |
| `crude_death_rate` | Crude Death Rate | number |  |
| `standard_error_for_crude_rate` | Standard Error for Crude Rate | number |  |
| `lower_confidence_limit_for_crude_rate` | Lower Confidence Limit for Crude Rate | number |  |
| `upper_confidence_limit_for_crude_rate` | Upper Confidence Limit for Crude Rate | number |  |
| `age_adjusted_rate` | Age-adjusted Rate | number |  |
| `standard_error_for_age_adjusted_rate` | Standard Error for Age-adjusted Rate | number |  |
| `lower_confidence_limit_for_age_adjusted_rate` | Lower Confidence Limit for Age-adjusted Rate | number |  |
| `upper_confidence_limit_for_age_adjusted_rate` | Upper Confidence Limit for Age-adjusted Rate | number |  |
| `state_crude_rate_in_range` | State Crude Rate in Range | text |  |
| `us_crude_rate` | US Crude Rate | number |  |
| `us_age_adjusted_rate` | US Age-adjusted Rate | number |  |
| `unit` | Unit | text |  |

### jx6g-fdh6

**NCHS - Drug Poisoning Mortality by State: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/jx6g-fdh6.json`
- Metadata: `GET https://data.cdc.gov/api/views/jx6g-fdh6.json`; page: https://data.cdc.gov/d/jx6g-fdh6
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `drug poisoning`, `mortality`, `state`, `national`, `united states`, `nchs`
- Rows: 2,703. Data updated: 2017-08-25. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset describes drug poisoning deaths at the U.S. and state level by selected demographic characteristics, and includes age-adjusted death rates for drug poisoning from 1999 to 2015. Deaths are classified using the International Classification of Diseases, Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 (undetermined intent). Estimates are based on the National Vital Statistics System multiple cause-of-death mortality files (1). Age-adjusted death rates (de…
- Sample row fields ($limit=1): `year`, `sex`, `age`, `race_hispanic_origin`, `state`, `deaths`, `population`, `crude_death_rate`, `standard_error_for_crude_rate`, `low_confidence_limit_for_crude_rate`, `upper_confidence_limit_for_crude_rate`, `age_adjusted_rate`, `standard_error_age_adjusted_rate`, `lower_confidence_limit_for_age_adjusted_rate`, `upper_confidence_limit_for_age_adjusted_rate`, `state_crude_rate_in_range`, `us_crude_rate`, `us_age_adjusted_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `sex` | Sex | text |  |
| `age` | Age | text |  |
| `race_hispanic_origin` | Race and Hispanic Origin | text |  |
| `state` | State | text |  |
| `deaths` | Deaths | number |  |
| `population` | Population | number |  |
| `crude_death_rate` | Crude Death Rate | number |  |
| `standard_error_for_crude_rate` | Standard Error for Crude Rate | number |  |
| `low_confidence_limit_for_crude_rate` | Low Confidence Limit for Crude Rate | number |  |
| `upper_confidence_limit_for_crude_rate` | Upper Confidence Limit for Crude Rate | number |  |
| `age_adjusted_rate` | Age-adjusted Rate | number |  |
| `standard_error_age_adjusted_rate` | Standard Error Age-adjusted Rate | number |  |
| `lower_confidence_limit_for_age_adjusted_rate` | Lower Confidence Limit for Age-adjusted rate | number |  |
| `upper_confidence_limit_for_age_adjusted_rate` | Upper Confidence Limit for Age-adjusted Rate | number |  |
| `state_crude_rate_in_range` | State Crude Rate in Range | text |  |
| `us_crude_rate` | US Crude Rate | number |  |
| `us_age_adjusted_rate` | US Age-adjusted Rate | number |  |

### 44rk-q6r2

**NCHS - Drug Poisoning Mortality by State: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/44rk-q6r2.json`
- Metadata: `GET https://data.cdc.gov/api/views/44rk-q6r2.json`; page: https://data.cdc.gov/d/44rk-q6r2
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `drug poisoning`, `mortality`, `state`, `national`, `united states`, `nchs`
- Rows: 3,180. Data updated: 2020-09-08. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset describes drug poisoning deaths at the U.S. and state level by selected demographic characteristics, and includes age-adjusted death rates for drug poisoning. Deaths are classified using the International Classification of Diseases, Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 (undetermined intent). Estimates are based on the National Vital Statistics System multiple cause-of-death mortality files (1). Age-adjusted death rates (deaths per 100,000 U…
- Sample row fields ($limit=1): `state`, `year`, `sex`, `age`, `race`, `deaths`, `popul`, `rate`, `se`, `slcl`, `sucl`, `usrate`, `usageadjrate`, `unit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `state` | State | text |  |
| `year` | Year | number |  |
| `sex` | Sex | text |  |
| `age` | Age Group | text |  |
| `race` | Race and Hispanic Origin | text |  |
| `deaths` | Deaths | number |  |
| `popul` | Population | number |  |
| `rate` | Crude Death Rate | number |  |
| `se` | Standard Error for Crude Rate | number |  |
| `slcl` | Low Confidence Limit for Crude Rate | number |  |
| `sucl` | Upper Confidence Limit for Crude Rate | number |  |
| `ageadjrate` | Age-adjusted Rate | number |  |
| `sea` | Standard Error Age-adjusted Rate | number |  |
| `alcl` | Lower Confidence Limit for Age-adjusted Rate | number |  |
| `aucl` | Upper Confidence for Age-adjusted Rate | number |  |
| `strankn` | State Crude Rate in Range | text |  |
| `usrate` | US Crude Rate | number |  |
| `usageadjrate` | US Age-adjusted Rate | number |  |
| `unit` | Unit | text |  |

### epev-k6ss

**NCHS - Infant and neonatal mortality rates: United States, 1915-2013** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/epev-k6ss.json`
- Metadata: `GET https://data.cdc.gov/api/views/epev-k6ss.json`; page: https://data.cdc.gov/d/epev-k6ss
- Topics: Category: National Center for Health Statistics
- Tags: `infant`, `neonatal`, `mortality`, `united states`, `nchs`
- Rows: 198. Data updated: 2016-06-22. Probe status: 200.
- Source: NCHS/DVS
- Description: Rates are infants (under 1 year) and neonatal (under 28 days) deaths per 1,000 live births. https://www.cdc.gov/nchs/data-visualization/mortality-trends/
- Sample row fields ($limit=1): `type`, `year`, `mortality_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `type` | Type | text |  |
| `year` | Year | number |  |
| `mortality_rate` | Mortality Rate | number |  |

### ddsk-zebd

**NCHS - Infant Mortality Rates, by Race: United States, 1915-2013** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ddsk-zebd.json`
- Metadata: `GET https://data.cdc.gov/api/views/ddsk-zebd.json`; page: https://data.cdc.gov/d/ddsk-zebd
- Topics: Category: National Center for Health Statistics
- Tags: `infant mortality rates`, `race`, `united states`, `nchs`
- Rows: 198. Data updated: 2016-06-22. Probe status: 200.
- Source: NCHS/DVS
- Description: All birth data by race before 1980 are based on race of the child; starting in 1980, birth data by race are based on race of the mother. Birth data are used to calculate infant mortality rate. https://www.cdc.gov/nchs/data-visualization/mortality-trends/
- Sample row fields ($limit=1): `race`, `year`, `infant_mortality_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `race` | Race | text |  |
| `year` | Year | number |  |
| `infant_mortality_rate` | Infant Mortality Rate | number |  |

### nt65-c7a7

**NCHS - Injury Mortality: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/nt65-c7a7.json`
- Metadata: `GET https://data.cdc.gov/api/views/nt65-c7a7.json`; page: https://data.cdc.gov/d/nt65-c7a7
- Topics: Category: National Center for Health Statistics
- Tags: `injury`, `mortality`, `united states`, `nchs`
- Rows: 98,280. Data updated: 2018-06-12. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset describes injury mortality in the United States beginning in 1999. Two concepts are included in the circumstances of an injury death: intent of injury and mechanism of injury. Intent of injury describes whether the injury was inflicted purposefully (intentional injury) and, if purposeful, whether the injury was self-inflicted (suicide or self-harm) or inflicted by another person (homicide). Injuries that were not purposefully inflicted are considered unintentional (accidental) injuries. Mechanism of injury describes the source of the energy transfer that resulted in physical or p…
- Sample row fields ($limit=1): `year`, `sex`, `age_years`, `race`, `injury_mechanism`, `injury_intent`, `deaths`, `population`, `age_specific_rate`, `age_specific_rate_standard_error`, `age_specific_rate_lower_confidence_limit`, `age_specific_rate_upper_confidence_limit`, `unit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | text |  |
| `sex` | Sex | text |  |
| `age_years` | Age group (years) | text |  |
| `race` | Race | text |  |
| `injury_mechanism` | Injury mechanism | text |  |
| `injury_intent` | Injury intent | text |  |
| `deaths` | Deaths | number |  |
| `population` | Population | number |  |
| `age_specific_rate` | Age Specific Rate | number |  |
| `age_specific_rate_standard_error` | Age Specific Rate Standard Error | number |  |
| `age_specific_rate_lower_confidence_limit` | Age Specific Rate Lower Confidence Limit | number |  |
| `age_specific_rate_upper_confidence_limit` | Age Specific Rate Upper Confidence Limit | number |  |
| `age_adjusted_rate` | Age Adjusted Rate | number |  |
| `age_adjusted_rate_standard_error` | Age Adjusted Rate Standard Error | number |  |
| `age_adjusted_rate_lower_confidence_limit` | Age Adjusted Rate Lower Confidence Limit | number |  |
| `age_adjusted_rate_upper_confidence_limit` | Age Adjusted Rate Upper Confidence Limit | number |  |
| `unit` | Unit | text |  |

### vc9m-u7tv

**NCHS - Injury Mortality: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/vc9m-u7tv.json`
- Metadata: `GET https://data.cdc.gov/api/views/vc9m-u7tv.json`; page: https://data.cdc.gov/d/vc9m-u7tv
- Topics: Category: National Center for Health Statistics
- Tags: `injury`, `mortality`, `united states`, `nchs`
- Rows: 98,280. Data updated: 2018-03-07. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset describes injury mortality in the United States beginning in 1999. Two concepts are included in the circumstances of an injury death: intent of injury and mechanism of injury. Intent of injury describes whether the injury was inflicted purposefully (intentional injury) and, if purposeful, whether the injury was self-inflicted (suicide or self-harm) or inflicted by another person (homicide). Injuries that were not purposefully inflicted are considered unintentional (accidental) injuries. Mechanism of injury describes the source of the energy transfer that resulted in physical or p…
- Sample row fields ($limit=1): `year`, `sex`, `age_group_years`, `race`, `injury_mechanism`, `injury_intent`, `deaths`, `population`, `age_specific_rate`, `age_specific_rate_standard_error`, `age_specific_rate_lower_confidence_limit`, `age_specific_rate_upper_confidence_limit`, `age_adjusted_rate`, `age_adjusted_rate_standard_error`, `age_adjusted_rate_lower_confidence_limit`, `age_adjusted_rate_upper_confidence_limit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `sex` | Sex | text |  |
| `age_group_years` | Age Group (Years) | text |  |
| `race` | Race | text |  |
| `injury_mechanism` | Injury Mechanism | text |  |
| `injury_intent` | Injury Intent | text |  |
| `deaths` | Deaths | number |  |
| `population` | Population | number |  |
| `age_specific_rate` | Age Specific Rate | number |  |
| `age_specific_rate_standard_error` | Age Specific Rate Standard Error | number |  |
| `age_specific_rate_lower_confidence_limit` | Age Specific Rate Lower Confidence Limit | number |  |
| `age_specific_rate_upper_confidence_limit` | Age Specific Rate Upper Confidence Limit | number |  |
| `age_adjusted_rate` | Age Adjusted Rate | text |  |
| `age_adjusted_rate_standard_error` | Age Adjusted Rate Standard Error | text |  |
| `age_adjusted_rate_lower_confidence_limit` | Age Adjusted Rate Lower Confidence Limit | text |  |
| `age_adjusted_rate_upper_confidence_limit` | Age Adjusted Rate Upper Confidence Limit | text |  |

### bi63-dtpu

**NCHS - Leading Causes of Death: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/bi63-dtpu.json`
- Metadata: `GET https://data.cdc.gov/api/views/bi63-dtpu.json`; page: https://data.cdc.gov/d/bi63-dtpu
- Topics: Category: National Center for Health Statistics
- Tags: `leading causes of death`, `mortality`, `state`, `united states`, `nchs`
- Rows: 10,868. Data updated: 2019-10-24. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset presents the age-adjusted death rates for the 10 leading causes of death in the United States beginning in 1999. Data are based on information from all resident death certificates filed in the 50 states and the District of Columbia using demographic and medical characteristics. Age-adjusted death rates (per 100,000 population) are based on the 2000 U.S. standard population. Populations used for computing death rates after 2010 are postcensal estimates based on the 2010 census, estimated as of July 1, 2010. Rates for census years are based on populations enumerated in the correspo…
- Sample row fields ($limit=1): `year`, `_113_cause_name`, `cause_name`, `state`, `deaths`, `aadr`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `_113_cause_name` | 113 Cause Name | text |  |
| `cause_name` | Cause Name | text |  |
| `state` | State | text |  |
| `deaths` | Deaths | number |  |
| `aadr` | Age-adjusted Death Rate | number |  |

### s54h-bixi

**NCHS - Natality Measures for Females by Hispanic Origin Subgroup: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/s54h-bixi.json`
- Metadata: `GET https://data.cdc.gov/api/views/s54h-bixi.json`; page: https://data.cdc.gov/d/s54h-bixi
- Topics: Category: National Center for Health Statistics
- Tags: `birth`, `birth rate`, `ethnicity`, `fertility rate`, `hispanic origin`, `united states`, `nchs`
- Rows: 151. Data updated: 2020-01-27. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset includes live births, birth rates, and fertility rates by Hispanic origin of mother in the United States since 1989. National data on births by Hispanic origin exclude data for Louisiana, New Hampshire, and Oklahoma in 1989; New Hampshire and Oklahoma in 1990; and New Hampshire in 1991 and 1992. Birth and fertility rates for the Central and South American population includes other and unknown Hispanic. Information on reporting Hispanic origin is detailed in the Technical Appendix for the 1999 public-use natality data file (see ftp://ftp.cdc.gov/pub/Health_Statistics/NCHS/Dataset_…
- Sample row fields ($limit=1): `year`, `hispanic_origin`, `live_births`, `birth_rates`, `fertility_rates`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | text |  |
| `hispanic_origin` | Hispanic Origin | text |  |
| `live_births` | Live Births | number |  |
| `birth_rates` | Birth Rates | number |  |
| `fertility_rates` | Fertility Rates | number |  |

### 89yk-m38d

**NCHS - Natality Measures for Females by Race and Hispanic Origin: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/89yk-m38d.json`
- Metadata: `GET https://data.cdc.gov/api/views/89yk-m38d.json`; page: https://data.cdc.gov/d/89yk-m38d
- Topics: Category: National Center for Health Statistics
- Tags: `births`, `birth rates`, `ethnicity`, `fertility rates`, `hispanic origin`, `race`, `united states`, `nchs`
- Rows: 470. Data updated: 2020-01-27. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset includes live births, birth rates, and fertility rates by race of mother in the United States since 1960. Data availability varies by race and ethnicity groups. All birth data by race before 1980 are based on race of the child. Since 1980, birth data by race are based on race of the mother. For race, data are available for Black and White births since 1960, and for American Indians/Alaska Native and Asian/Pacific Islander births since 1980. Data on Hispanic origin are available since 1989. Teen birth rates for specific racial and ethnic categories are also available since 1989. F…
- Sample row fields ($limit=1): `year`, `race`, `live_births`, `birth_rate`, `fertility_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | text |  |
| `race` | Race | text |  |
| `live_births` | Live Births | number |  |
| `birth_rate` | Birth Rate | number |  |
| `fertility_rate` | Fertility Rate | number |  |

### jvf6-ix4w

**NCHS - Nonmarital Birth Rates, by Age Group for All Women Age 15-44: United States, 1970-2013** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/jvf6-ix4w.json`
- Metadata: `GET https://data.cdc.gov/api/views/jvf6-ix4w.json`; page: https://data.cdc.gov/d/jvf6-ix4w
- Topics: Category: National Center for Health Statistics
- Tags: `birth rates`, `age group`, `women`, `united states`, `nchs`
- Rows: 1,494. Data updated: 2015-12-02. Probe status: 200.
- Source: NCHS/DVS
- Description: https://www.cdc.gov/nchs/data-visualization/births-to-unmarried-women/index.htm
- Sample row fields ($limit=1): `year`, `age`, `race`, `birth_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `age` | Age | text |  |
| `race` | Race | text |  |
| `birth_rate` | Birth Rate | number |  |

### isx2-c2ii

**NCHS - Percent Distribution of Births for Females by Age Group: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/isx2-c2ii.json`
- Metadata: `GET https://data.cdc.gov/api/views/isx2-c2ii.json`; page: https://data.cdc.gov/d/isx2-c2ii
- Topics: Category: National Center for Health Statistics
- Tags: `maternal age`, `births`, `united states`, `nchs`
- Rows: 688. Data updated: 2020-01-27. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset includes percent distribution of births for females by age group in the United States since 1933. The number of states in the reporting area differ historically. In 1915 (when the birth registration area was established), 10 states and the District of Columbia reported births; by 1933, 48 states and the District of Columbia were reporting births, with the last two states, Alaska and Hawaii, added to the registration area in 1959 and 1960, when these regions gained statehood. Reporting area information is detailed in references 1 and 2 below. Trend lines for 1909–1958 are based on…
- Sample row fields ($limit=1): `year`, `age_group`, `percentage_of_birth`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | text |  |
| `age_group` | Age Group | text |  |
| `percentage_of_birth` | Percentage of Births | number |  |

### hzd8-r9mj

**NCHS - Percent Distribution of Births to Unmarried Women by Age Group: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/hzd8-r9mj.json`
- Metadata: `GET https://data.cdc.gov/api/views/hzd8-r9mj.json`; page: https://data.cdc.gov/d/hzd8-r9mj
- Topics: Category: National Center for Health Statistics
- Tags: `births`, `percent distribution`, `nonmarital`, `age`, `nchs`
- Rows: 230. Data updated: 2017-08-23. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset includes percent distribution of births to unmarried women by age group in the United States since 1970. Methods for collecting information on marital status changed over the reporting period and have been documented in: • Ventura SJ, Bachrach CA. Nonmarital childbearing in the United States, 1940–99. National vital statistics reports; vol 48 no 16. Hyattsville, Maryland: National Center for Health Statistics. 2000. Available from: http://www.cdc.gov/nchs/data/nvsr/nvsr48/nvs48_16.pdf. • National Center for Health Statistics. User guide to the 2013 natality public use file. Hyatt…
- Sample row fields ($limit=1): `year`, `age_group`, `percent`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `age_group` | Age Group | text |  |
| `percent` | Percent of Nonmarital Births | number |  |

### vdpk-qzpr

**NCHS - Potentially Excess Deaths from the Five Leading Causes of Death** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/vdpk-qzpr.json`
- Metadata: `GET https://data.cdc.gov/api/views/vdpk-qzpr.json`; page: https://data.cdc.gov/d/vdpk-qzpr
- Topics: Category: National Center for Health Statistics
- Tags: `heart disease`, `cancer`, `unintentional injury`, `chronic lower respiratory disease`, `stroke`
- Rows: 205,920. Data updated: 2017-08-15. Probe status: 200.
- Source: NCHS/DVS
- Description: MMWR Surveillance Summary 66 (No. SS-1):1-8 found that nonmetropolitan areas have significant numbers of potentially excess deaths from the five leading causes of death. These figures accompany this report by presenting information on potentially excess deaths in nonmetropolitan and metropolitan areas at the state level. They also add additional years of data and options for selecting different age ranges and benchmarks. Potentially excess deaths are defined in MMWR Surveillance Summary 66(No. SS-1):1-8 as deaths that exceed the numbers that would be expected if the death rates of states with…
- Sample row fields ($limit=1): `year`, `cause_of_death`, `state`, `state_fips_code`, `hhs_region`, `age_range`, `benchmark`, `locality`, `observed_deaths`, `population`, `expected_deaths`, `potentially_excess_deaths`, `percent_potentially_excess_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | text |  |
| `cause_of_death` | Cause of Death | text |  |
| `state` | State | text |  |
| `state_fips_code` | State FIPS Code | text |  |
| `hhs_region` | HHS Region | number |  |
| `age_range` | Age Range | text |  |
| `benchmark` | Benchmark | text |  |
| `locality` | Locality | text |  |
| `observed_deaths` | Observed Deaths | number |  |
| `population` | Population | number |  |
| `expected_deaths` | Expected Deaths | number |  |
| `potentially_excess_deaths` | Potentially Excess Deaths | number |  |
| `percent_potentially_excess_deaths` | Percent Potentially Excess Deaths | number |  |

### 7pcd-2tnr

**NCHS - Pregnancy and Live Birth Rates, by Marital Status and Race and Hispanic Origin: United States, 1990-2010** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/7pcd-2tnr.json`
- Metadata: `GET https://data.cdc.gov/api/views/7pcd-2tnr.json`; page: https://data.cdc.gov/d/7pcd-2tnr
- Topics: Category: National Center for Health Statistics
- Tags: `live birth rate`, `marital status`, `race`, `hispanic origin`, `united states`, `nchs`
- Rows: 190. Data updated: 2015-12-02. Probe status: 200.
- Source: NCHS/DVS
- Description: https://www.cdc.gov/nchs/data-visualization/births-to-unmarried-women/index.htm
- Sample row fields ($limit=1): `year`, `marrital_status`, `race_ethnicity`, `all_pregnancies`, `live_births`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `marrital_status` | Marrital Status | text |  |
| `race_ethnicity` | Race Ethnicity | text |  |
| `all_pregnancies` | All Pregnancies | number |  |
| `live_births` | Live Births | number |  |

### hdy7-e2a3

**NCHS - Pregnancy Rates, by Age for Hispanic Women: United States, 1990-2010** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/hdy7-e2a3.json`
- Metadata: `GET https://data.cdc.gov/api/views/hdy7-e2a3.json`; page: https://data.cdc.gov/d/hdy7-e2a3
- Topics: Category: National Center for Health Statistics
- Tags: `pregnancy rate`, `hispanic women`, `united states`, `nchs`
- Rows: 190. Data updated: 2015-12-02. Probe status: 200.
- Source: NCHS/DVS
- Description: https://www.cdc.gov/nchs/data-visualization/natality-trends/index.htm
- Sample row fields ($limit=1): `year`, `race_ethnicity`, `marrital_status`, `all_pregnancies`, `live_birth`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `race_ethnicity` | Race Ethnicity | text |  |
| `marrital_status` | Marrital Status | text |  |
| `all_pregnancies` | All pregnancies | number |  |
| `live_birth` | Live birth | number |  |

### 3h58-x6cd

**NCHS - Teen Birth Rates for Age Group 15-19 in the United States by County** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3h58-x6cd.json`
- Metadata: `GET https://data.cdc.gov/api/views/3h58-x6cd.json`; page: https://data.cdc.gov/d/3h58-x6cd
- Topics: Category: National Center for Health Statistics
- Tags: `county teen birth trends`, `teen births`, `county trends on teen births`, `u.s. teen birth rate`, `united states`, `nchs`
- Rows: 56,466. Data updated: 2022-04-08. Probe status: 200.
- Source: NCHS/DVS
- Description: This data set contains estimated teen birth rates for age group 15–19 (expressed per 1,000 females aged 15–19) by county and year. DEFINITIONS Estimated teen birth rate: Model-based estimates of teen birth rates for age group 15–19 (expressed per 1,000 females aged 15–19) for a specific county and year. Estimated county teen birth rates were obtained using the methods described elsewhere (1,2,3,4). These annual county-level teen birth estimates “borrow strength” across counties and years to generate accurate estimates where data are sparse due to small population size (1,2,3,4). The inferenti…
- Sample row fields ($limit=1): `year`, `state`, `county`, `state_fips_code`, `county_fips_code`, `combined_fips_code`, `birth_rate`, `lower_confidence_limit`, `upper_confidence_limit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | text |  |
| `state` | State | text |  |
| `county` | County | text |  |
| `state_fips_code` | State FIPS Code | text |  |
| `county_fips_code` | County FIPS Code | text |  |
| `combined_fips_code` | Combined FIPS Code | text |  |
| `birth_rate` | Birth Rate | number |  |
| `lower_confidence_limit` | Lower Confidence Limit | number |  |
| `upper_confidence_limit` | Upper Confidence Limit | number |  |

### e8kx-wbww

**NCHS - Teen Birth Rates for Females by Age Group, Race, and Hispanic Origin: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/e8kx-wbww.json`
- Metadata: `GET https://data.cdc.gov/api/views/e8kx-wbww.json`; page: https://data.cdc.gov/d/e8kx-wbww
- Topics: Category: National Center for Health Statistics
- Tags: `birth rate`, `age`, `ethnicity`, `hispanic origin`, `race`, `united states`, `nchs`
- Rows: 896. Data updated: 2020-01-27. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset includes teen birth rates for females by age group, race, and Hispanic origin in the United States since 1960. Data availability varies by race and ethnicity groups. All birth data by race before 1980 are based on race of the child. Since 1980, birth data by race are based on race of the mother. For race, data are available for Black and White births since 1960, and for American Indians/Alaska Native and Asian/Pacific Islander births since 1980. Data on Hispanic origin are available since 1989. Teen birth rates for specific racial and ethnic categories are also available since 19…
- Sample row fields ($limit=1): `year`, `race`, `age`, `birth_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | text |  |
| `race` | Race or Hispanic Origin | text |  |
| `age` | Age Group | text |  |
| `birth_rate` | Birth Rate | number |  |

### mc4y-cbbv

**NCHS - Top Five Leading Causes of Death: United States, 1990, 1950, 2000** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/mc4y-cbbv.json`
- Metadata: `GET https://data.cdc.gov/api/views/mc4y-cbbv.json`; page: https://data.cdc.gov/d/mc4y-cbbv
- Topics: Category: National Center for Health Statistics
- Tags: `cause of death`, `mortality`, `united states`, `nchs`
- Rows: 15. Data updated: 2020-09-08. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: This dataset contains information on the number of deaths and age-adjusted death rates for the five leading causes of death in 1900, 1950, and 2000. Age-adjusted death rates (deaths per 100,000) after 1998 are calculated based on the 2000 U.S. standard population. Populations used for computing death rates for 2011–2017 are postcensal estimates based on the 2010 census, estimated as of July 1, 2010. Rates for census years are based on populations enumerated in the corresponding censuses. Rates for noncensus years between 2000 and 2010 are revised using updated intercensal population estimates…
- Sample row fields ($limit=1): `year`, `leading_causes`, `number_of_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `leading_causes` | Cause | text |  |
| `number_of_deaths` | Number of Deaths | number |  |

### y268-sna3

**NCHS - U.S. and State Trends on Teen Births** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/y268-sna3.json`
- Metadata: `GET https://data.cdc.gov/api/views/y268-sna3.json`; page: https://data.cdc.gov/d/y268-sna3
- Topics: Category: National Center for Health Statistics
- Tags: `state teen birth trends`, `teen births`, `u.s. and state trends on teen births`, `u.s. teen birth rate`, `united states`, `nchs`
- Rows: 4,680. Data updated: 2022-05-09. Probe status: 200.
- Source: NCHS/DVS
- Description: This dataset assembles all final birth data for females aged 15–19, 15–17, and 18–19 for the United States and each of the 50 states. Data are based on 100% of birth certificates filed in all 50 states. All the teen birth rates in this dashboard reflect the latest revisions to Census populations (i.e., the intercensal populations) and thus provide a consistent series of accurate rates for the past 25 years. The denominators of the teen birth rates for 1991–1999 have been revised to incorporate the results of the 2000 Census. The denominators of the teen birth rates for 2001–2009 have revised…
- Sample row fields ($limit=1): `year`, `state`, `age_years`, `state_rate`, `state_births`, `u_s_births`, `u_s_birth_rate`, `unit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year` | Year | number |  |
| `state` | State | text |  |
| `age_years` | Age Group (Years) | text |  |
| `state_rate` | State Rate | number |  |
| `state_births` | State Births | number |  |
| `u_s_births` | U.S. Births | number |  |
| `u_s_birth_rate` | U.S. Birth Rate | number |  |
| `unit` | Unit | text |  |

### jqwm-z2g9

**NCHS - VSRR Quarterly provisional estimates for infant mortality** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/jqwm-z2g9.json`
- Metadata: `GET https://data.cdc.gov/api/views/jqwm-z2g9.json`; page: https://data.cdc.gov/d/jqwm-z2g9
- Topics: Category: National Center for Health Statistics
- Tags: `vsrr`, `nvss`, `infant mortality`, `causes of death`, `nchs`, `provisional`, `mortality`, `deaths`, `united states`, `quarterly`
- Rows: 168. Data updated: 2026-10-29. Probe status: 200.
- Update frequency: R/P3M.
- Source: NCHS/DVS
- Description: Provisional estimates of infant mortality (deaths of infants under 1 year per 1,000 live births), neonatal mortality (deaths of infants aged 0-27 days per 1,000 live births), postneonatal mortality (deaths of infants aged 28 days through 11 months per 1,000 live births), and death rates for the five leading causes of infant death.
- Sample row fields ($limit=1): `year_and_quarter`, `topic`, `indicator`, `time_period`, `rate`, `unit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year_and_quarter` | Year and Quarter | text |  |
| `topic` | Topic | text |  |
| `indicator` | Indicator | text |  |
| `time_period` | Time Period | text |  |
| `rate` | Rate | number |  |
| `unit` | Unit | text |  |
| `significant` | Significant | text |  |
| `standard_error` | Standard Error | number |  |
| `footnote_symbol` | Footnote Symbol | text |  |
| `footnote` | Footnote | text |  |

### 76vv-a7x8

**NCHS - VSRR Quarterly provisional estimates for selected birth indicators** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/76vv-a7x8.json`
- Metadata: `GET https://data.cdc.gov/api/views/76vv-a7x8.json`; page: https://data.cdc.gov/d/76vv-a7x8
- Topics: Category: National Center for Health Statistics
- Tags: `vital statistics rapid release`, `vsrr`, `birth rate`, `fertility rate`, `preterm birth`, `cesarean delivery`, `nchs`
- Rows: 1,000. Data updated: 2026-09-17. Probe status: 200.
- Update frequency: R/P3M.
- Source: NCHS/DVS
- Description: Provisional estimates of selected reproductive indicators. Estimates are presented for: general fertility rates, age-specific birth rates, total and low risk cesarean delivery rates, preterm birth rates and other gestational age categories.
- Sample row fields ($limit=1): `year_and_quarter`, `topic`, `topic_subgroup`, `indicator`, `race_ethnicity`, `rate`, `unit`, `significant`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year_and_quarter` | Year and Quarter | text |  |
| `topic` | Topic | text |  |
| `topic_subgroup` | Topic Subgroup | text |  |
| `indicator` | Indicator | text |  |
| `race_ethnicity` | Race Ethnicity Category | text |  |
| `rate` | Rate | number |  |
| `unit` | Unit | text |  |
| `significant` | Significant | text | An asterisk (*) indicates that estimates for the most recent quarter are significantly different from the same quarter of the previous year |

### 489q-934x

**NCHS - VSRR Quarterly provisional estimates for selected indicators of mortality** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/489q-934x.json`
- Metadata: `GET https://data.cdc.gov/api/views/489q-934x.json`; page: https://data.cdc.gov/d/489q-934x
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `vsrr`, `provisional`, `deaths`, `mortality`, `quarterly`, `all causes`, `causes of death`, `covid-19`, `coronavirus`, `state`, `united states`, `age`, `age group`, `sex`, `death rate`, `alzheimer disease`, `cancer`, `chronic lower respiratory disease`, `chronic liver disease`, `cirrhosis`, `diabetes`, `drug overdose`, `falls`, `firearm injury`, `diseases of heart`, `hiv disease`, `homicide`, `influenza`, `pneumonia`, `kidney disease`, `parkinson disease`, `septicemia`, `cerebrovascular disease`, `suicide`, `unintentional injuries`, `pneumonitis due to solids and liquids`, `hypertensive disease`
- Rows: 924. Data updated: 2026-06-23. Probe status: 200.
- Update frequency: R/P3M.
- Source: National Center for Health Statistics
- Description: Provisional estimates of death rates. Estimates are presented for each of the 15 leading causes of death plus estimates for deaths attributed to drug overdose, falls (for persons aged 65 and over), human immunodeficiency virus (HIV) disease, homicide, and firearms-related deaths.
- Sample row fields ($limit=1): `year_and_quarter`, `time_period`, `cause_of_death`, `rate_type`, `unit`, `rate_overall`, `rate_sex_female`, `rate_sex_male`, `rate_alaska`, `rate_alabama`, `rate_arkansas`, `rate_arizona`, `rate_california`, `rate_colorado`, `rate_connecticut`, `rate_district_of_columbia`, `rate_delaware`, `rate_florida`, `rate_georgia`, `rate_hawaii`, `rate_iowa`, `rate_idaho`, `rate_illinois`, `rate_indiana`, `rate_kansas`, `rate_kentucky`, `rate_louisiana`, `rate_massachusetts`, `rate_maryland`, `rate_maine`, `rate_michigan`, `rate_minnesota`, `rate_missouri`, `rate_mississippi`, `rate_montana`, `rate_north_carolina`, `rate_north_dakota`, `rate_nebraska`, `rate_new_hampshire`, `rate_new_jersey`, `rate_new_mexico`, `rate_nevada`, `rate_new_york`, `rate_ohio`, `rate_oklahoma`, `rate_oregon`, `rate_pennsylvania`, `rate_rhode_island`, `rate_south_carolina`, `rate_south_dakota`, `rate_tennessee`, `rate_texas`, `rate_utah`, `rate_virginia`, `rate_vermont`, `rate_washington`, `rate_wisconsin`, `rate_west_virginia`, `rate_wyoming`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `year_and_quarter` | Year and Quarter | text |  |
| `time_period` | Time Period | text |  |
| `cause_of_death` | Cause of Death | text |  |
| `rate_type` | Rate Type | text |  |
| `unit` | Unit | text |  |
| `rate_overall` | Overall Rate | number |  |
| `rate_sex_female` | Rate Sex Female | number |  |
| `rate_sex_male` | Rate Sex Male | number |  |
| `rate_age_1_4` | Rate Age 1-4 | number |  |
| `rate_age_5_14` | Rate Age 5-14 | number |  |
| `rate_age_15_24` | Rate Age 15-24 | number |  |
| `rate_age_25_34` | Rate Age 25-34 | number |  |
| `rate_age_35_44` | Rate Age 35-44 | number |  |
| `rate_age_45_54` | Rate Age 45-54 | number |  |
| `rate_age_55_64` | Rate Age 55-64 | number |  |
| `rate_65_74` | Rate 65-74 | number |  |
| `rate_age_75_84` | Rate Age 75-84 | number |  |
| `rate_age_85_plus` | Rate Age 85 plus | number |  |
| `rate_alaska` | Rate Alaska | number |  |
| `rate_alabama` | Rate Alabama | number |  |
| `rate_arkansas` | Rate Arkansas | number |  |
| `rate_arizona` | Rate Arizona | number |  |
| `rate_california` | Rate California | number |  |
| `rate_colorado` | Rate Colorado | number |  |
| `rate_connecticut` | Rate Connecticut | number |  |
| `rate_district_of_columbia` | Rate District of Columbia | number |  |
| `rate_delaware` | Rate Delaware | number |  |
| `rate_florida` | Rate Florida | number |  |
| `rate_georgia` | Rate Georgia | number |  |
| `rate_hawaii` | Rate Hawaii | number |  |
| `rate_iowa` | Rate Iowa | number |  |
| `rate_idaho` | Rate Idaho | number |  |
| `rate_illinois` | Rate Illinois | number |  |
| `rate_indiana` | Rate Indiana | number |  |
| `rate_kansas` | Rate Kansas | number |  |
| `rate_kentucky` | Rate Kentucky | number |  |
| `rate_louisiana` | Rate Louisiana | number |  |
| `rate_massachusetts` | Rate Massachusetts | number |  |
| `rate_maryland` | Rate Maryland | number |  |
| `rate_maine` | Rate Maine | number |  |
| `rate_michigan` | Rate Michigan | number |  |
| `rate_minnesota` | Rate Minnesota | number |  |
| `rate_missouri` | Rate Missouri | number |  |
| `rate_mississippi` | Rate Mississippi | number |  |
| `rate_montana` | Rate Montana | number |  |
| `rate_north_carolina` | Rate North Carolina | number |  |
| `rate_north_dakota` | Rate North Dakota | number |  |
| `rate_nebraska` | Rate Nebraska | number |  |
| `rate_new_hampshire` | Rate New Hampshire | number |  |
| `rate_new_jersey` | Rate New Jersey | number |  |
| `rate_new_mexico` | Rate New Mexico | number |  |
| `rate_nevada` | Rate Nevada | number |  |
| `rate_new_york` | Rate New York | number |  |
| `rate_ohio` | Rate Ohio | number |  |
| `rate_oklahoma` | Rate Oklahoma | number |  |
| `rate_oregon` | Rate Oregon | number |  |
| `rate_pennsylvania` | Rate Pennsylvania | number |  |
| `rate_rhode_island` | Rate Rhode Island | number |  |
| `rate_south_carolina` | Rate South Carolina | number |  |
| `rate_south_dakota` | Rate South Dakota | number |  |
| `rate_tennessee` | Rate Tennessee | number |  |
| `rate_texas` | Rate Texas | number |  |
| `rate_utah` | Rate Utah | number |  |
| `rate_virginia` | Rate Virginia | number |  |
| `rate_vermont` | Rate Vermont | number |  |
| `rate_washington` | Rate Washington | number |  |
| `rate_wisconsin` | Rate Wisconsin | number |  |
| `rate_west_virginia` | Rate West Virginia | number |  |
| `rate_wyoming` | Rate Wyoming | number |  |

### p89x-xx88

**NCHS Rapid Surveys System** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/p89x-xx88.json`
- Metadata: `GET https://data.cdc.gov/api/views/p89x-xx88.json`; page: https://data.cdc.gov/d/p89x-xx88
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `dhis`
- Rows: 6,279. Data updated: 2026-02-26. Probe status: 200.
- Update frequency: R/P3M.
- Source: NCHS/DHIS
- Description: The NCHS Rapid Surveys System includes questions sponsored by CDC programs and other partners to address time-sensitive data needs, public health attitudes or behaviors, and developmental work to improve concept measurement and inform future question design. It also includes standard variables used for sample weighting and calibration, as well as selected portions of existing content from NCHS surveys (such as the National Health Interview Survey) to compare panel estimates to these benchmarks, assess the fitness-for-use of the panel survey data, and for other methodological purposes.
- Sample row fields ($limit=1): `round`, `topic`, `indicator`, `full_indicator`, `demographic_variable`, `demographic_variable_label`, `estimate`, `confidence_interval`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `round` | Round | number | Data collection period |
| `topic` | Topic | text | Topic |
| `indicator` | Indicator | text | Indicator |
| `full_indicator` | Title | text | Title |
| `demographic_variable` | Demographic Variable | text | Estimates were reported at the national level (total) and by age group, race and Hispanic origin, sex, education level, region, urbanization, and poverty. |
| `demographic_variable_label` | Demographic Variable Label | text | Demographic Variable Label |
| `estimate` | Percent Estimate | text | Percent Estimate |
| `confidence_interval` | Confidence Interval | text | Confidence interval |

### i667-sjhg

**NHANES Select Chronic Conditions Prevalence Estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/i667-sjhg.json`
- Metadata: `GET https://data.cdc.gov/api/views/i667-sjhg.json`; page: https://data.cdc.gov/d/i667-sjhg
- Topics: Category: National Center for Health Statistics
- Tags: `chronic conditions`, `nchs`, `nhanes`, `health statistics`, `surveillance`, `survey`
- Rows: 950. Data updated: 2023-02-27. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DHNES
- Description: These data represent prevalence estimates of select chronic conditions from the National Health and Nutrition Examination Survey (NHANES).
- Sample row fields ($limit=1): `survey_years`, `sex`, `age_group`, `race_and_hispanic_origin`, `measure`, `percent`, `standard_error`, `lower_95_ci_limit`, `upper_95_ci_limit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `survey_years` | Survey Years | text | data release cycle |
| `sex` | Sex | text | participant’s sex |
| `age_group` | Age Group | text | age in years of the participant at the time of screening. |
| `race_and_hispanic_origin` | Race and Hispanic Origin | text | participant’s race/ethnicity |
| `measure` | Measure | text | select chronic condition |
| `percent` | Percent | number | prevalence estimate |
| `standard_error` | Standard Error | number | standard error of estimate |
| `lower_95_ci_limit` | Lower 95% CI Limit | number | lower 95% confidence interval limit |
| `upper_95_ci_limit` | Upper 95% CI Limit | number | upper 95% confidence interval limit |
| `presentation_standard` | Presentation Standard | text | indication if estimate meets NCHS presentation standards |
| `note1` | Note1 | text | note explaining non-Hispanic Asian and Hispanic data availability |
| `notea` | Notea | text | corresponding symbol to Note1 |

### pqn7-e45s

**NHANES Select Infectious Diseases Prevalence Estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/pqn7-e45s.json`
- Metadata: `GET https://data.cdc.gov/api/views/pqn7-e45s.json`; page: https://data.cdc.gov/d/pqn7-e45s
- Topics: Category: National Center for Health Statistics
- Tags: `infectious disease`, `nchs`, `nhanes`, `health statistics`, `surveillance`, `survey`
- Rows: 340. Data updated: 2023-02-27. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DHNES
- Description: These data represent prevalence estimates of select infectious diseases from the National Health and Nutrition Examination Survey (NHANES).
- Sample row fields ($limit=1): `survey_years`, `sex`, `age_group`, `race_and_hispanic_origin`, `infectious_disease`, `percent`, `standard_error`, `lower_95_ci_limit`, `upper_95_ci_limit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `survey_years` | Survey Years | text | data release cycle |
| `sex` | Sex | text | participant’s sex |
| `age_group` | Age Group | text | age in years of the participant at the time of screening |
| `race_and_hispanic_origin` | Race and Hispanic Origin | text | participant’s race/ethnicity |
| `infectious_disease` | Infectious Disease | text | select infectious disease |
| `percent` | Percent | number | prevalence estimate |
| `standard_error` | Standard Error | number | standard error of estimate |
| `lower_95_ci_limit` | Lower 95% CI Limit | number | lower 95% confidence interval limit |
| `upper_95_ci_limit` | Upper 95% CI Limit | number | upper 95% confidence interval limit |
| `presentation_standard` | Presentation Standard | text | indication if estimate meets NCHS presentation standards |
| `note1` | Note1 | text | note explaining non-Hispanic Asian and Hispanic data availability |
| `notea` | Notea | text | corresponding symbol to Note1 |

### 8wmh-yzz9

**NHANES Select Mean Dietary Intake Estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8wmh-yzz9.json`
- Metadata: `GET https://data.cdc.gov/api/views/8wmh-yzz9.json`; page: https://data.cdc.gov/d/8wmh-yzz9
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nhanes`, `health statistics`, `surveillance`, `survey`, `nutrition`
- Rows: 3,570. Data updated: 2023-02-27. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DHNES
- Description: These data represent mean intake, on a given day, estimates of nutrients from foods and beverages from the National Health and Nutrition Examination Survey (NHANES).
- Sample row fields ($limit=1): `survey_years`, `sex`, `age_group`, `race_and_hispanic_origin`, `nutrient`, `mean`, `standard_error`, `lower_95_ci_limit`, `upper_95_ci_limit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `survey_years` | Survey Years | text | data release cycle |
| `sex` | Sex | text | participant’s sex |
| `age_group` | Age Group | text | age in years of the participant at the time of screening. |
| `race_and_hispanic_origin` | Race and Hispanic Origin | text | participant’s race/ethnicity |
| `nutrient` | Nutrient | text | select nutrient |
| `mean` | Mean | number | mean intake estimate |
| `standard_error` | Standard Error | number | standard error of estimate |
| `lower_95_ci_limit` | Lower 95% CI Limit | number | lower 95% confidence interval limit |
| `upper_95_ci_limit` | Upper 95% CI Limit | number | upper 95% confidence interval limit |
| `note1` | Note1 | text | note explaining non-Hispanic Asian and Hispanic data availability |
| `note2` | Note2 | text | note explaining vitamin D data availability |
| `notea` | Notea | text | corresponding symbol to Note1 |
| `noteb` | Noteb | text | corresponding symbol to Note2 |

### ggsw-596z

**NHANES Select Oral Health Prevalence Estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ggsw-596z.json`
- Metadata: `GET https://data.cdc.gov/api/views/ggsw-596z.json`; page: https://data.cdc.gov/d/ggsw-596z
- Topics: Category: National Center for Health Statistics
- Tags: `oral health`, `nchs`, `nhanes`, `health statistics`, `surveillance`, `survey`
- Rows: 1,160. Data updated: 2023-02-27. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DHNES
- Description: These data represent prevalence estimates of select oral health topics from the National Health and Nutrition Examination Survey (NHANES).
- Sample row fields ($limit=1): `survey_years`, `sex`, `age_group`, `race_and_hispanic_origin`, `measure`, `percent`, `standard_error`, `lower_95_ci_limit`, `upper_95_ci_limit`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `survey_years` | Survey Years | text | data release cycle |
| `sex` | Sex | text | participant’s sex |
| `age_group` | Age Group | text | age in years of the participant at the time of screening |
| `race_and_hispanic_origin` | Race and Hispanic Origin | text | participant’s race/ethnicity |
| `measure` | Measure | text | select oral health topic |
| `percent` | Percent | number | prevalence estimate |
| `standard_error` | Standard Error | number | standard error of estimate |
| `lower_95_ci_limit` | Lower 95% CI Limit | number | lower 95% confidence interval limit |
| `upper_95_ci_limit` | Upper 95% CI Limit | number | upper 95% confidence interval limit |
| `presentation_standard` | Presentation Standard | text | indication if estimate meets NCHS presentation standards |
| `note1` | Note1 | text | note explaining non-Hispanic Asian and Hispanic data availability |
| `note2` | Note2 | text | note explaining dental caries data availability |
| `notea` | Notea | text | corresponding symbol to Note1 |
| `noteb` | Noteb | text | Noteb: corresponding symbol to Note2 |

### krhz-spsc

**NHIS Adult 3-Year Summary Health Statistics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/krhz-spsc.json`
- Metadata: `GET https://data.cdc.gov/api/views/krhz-spsc.json`; page: https://data.cdc.gov/d/krhz-spsc
- Topics: Category: National Center for Health Statistics
- Tags: `summary health statistics`, `nhis`, `race`, `ethnicity`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-food-access`, `sdoh-workplace`
- Rows: 7,599. Data updated: 2025-09-18. Probe status: 200.
- Update frequency:  R/P1Y.
- Source: NCHS/DHIS
- Description: Interactive Summary Health Statistics for Adults, by Detailed Race and Ethnicity provide estimates as three-year averages of selected health topics for adults aged 18 years and over based on final data from the National Health Interview Survey.
- Sample row fields ($limit=1): `outcome_or_indicator`, `group`, `percentage`, `confidence_interval`, `title`, `description`, `year`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `outcome_or_indicator` | Outcome (or Indicator) | text |  |
| `group` | Group | text |  |
| `percentage` | Percentage | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `title` | Title | text |  |
| `description` | Description | text |  |
| `year` | Year | text |  |

### 25m4-6qqq

**NHIS Adult Summary Health Statistics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/25m4-6qqq.json`
- Metadata: `GET https://data.cdc.gov/api/views/25m4-6qqq.json`; page: https://data.cdc.gov/d/25m4-6qqq
- Topics: Category: National Center for Health Statistics
- Tags: `summary health statistics`, `nhis`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-food-access`, `sdoh-workplace`
- Rows: 30,499. Data updated: 2026-08-27. Probe status: 200.
- Source: NCHS/DHIS
- Description: Interactive Summary Health Statistics for Adults provide annual estimates of selected health topics for adults aged 18 years and over based on final data from the National Health Interview Survey.
- Sample row fields ($limit=1): `outcome_or_indicator`, `grouping_category`, `group`, `percentage`, `confidence_interval`, `title`, `description`, `year`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `outcome_or_indicator` | Outcome (or Indicator) | text |  |
| `grouping_category` | Grouping category | text | Group by category |
| `group` | Group | text |  |
| `percentage` | Percentage | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `title` | Title | text |  |
| `description` | Description | text |  |
| `year` | Year | number |  |

### wxz7-ekz9

**NHIS Child Summary Health Statistics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/wxz7-ekz9.json`
- Metadata: `GET https://data.cdc.gov/api/views/wxz7-ekz9.json`; page: https://data.cdc.gov/d/wxz7-ekz9
- Topics: Category: National Center for Health Statistics
- Tags: `summary health statistics`, `nhis`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-food-access`, `sdoh-workplace`
- Rows: 8,918. Data updated: 2026-08-27. Probe status: 200.
- Source: NCHS/DHIS
- Description: Interactive Summary Health Statistics for Children provide annual estimates of selected health topics for children under age 18 years based on final data from the National Health Interview Survey.
- Sample row fields ($limit=1): `outcome_or_indicator`, `group`, `percentage`, `confidence_interval`, `title`, `description`, `year`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `outcome_or_indicator` | Outcome (or Indicator) | text |  |
| `group` | Group | text |  |
| `percentage` | Percentage | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `title` | Title | text |  |
| `description` | Description | text |  |
| `year` | Year | number |  |

### trpk-sp8z

**NHIS Interactive Biannual Early Release Estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/trpk-sp8z.json`
- Metadata: `GET https://data.cdc.gov/api/views/trpk-sp8z.json`; page: https://data.cdc.gov/d/trpk-sp8z
- Topics: Category: National Center for Health Statistics
- Tags: `key health indicators`, `early release`, `nhis`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-food-access`, `sdoh-workplace`
- Rows: 5,634. Data updated: 2026-05-28. Probe status: 200.
- Update frequency: R/P6M.
- Source: NCHS/DHIS
- Description: Interactive Biannual Early Release Estimates provide health statistics based on data from the 2019-2021 National Health Interview Survey (NHIS) for selected health topics for adults aged 18 years and over. All estimates are unadjusted percentages based on preliminary data files and are released prior to final data editing and final weighting to provide access to the most recent information from the NHIS. Estimates can be grouped by demographic characteristics (such as age, race and Hispanic origin, or sex). Estimates based on 2019-2020 NHIS quarterly data are available in Interactive Quarterl…
- Sample row fields ($limit=1): `outcome_or_indicator`, `group_by_variable`, `percentage`, `confidence_interval`, `title`, `description`, `year`, `first_or_second_half`, `year_and_months`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `outcome_or_indicator` | Outcome (or Indicator) | text |  |
| `group_by_variable` | Group | text |  |
| `percentage` | Percentage | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `title` | Title | text |  |
| `description` | Description | text |  |
| `year` | Year | number |  |
| `first_or_second_half` | First or Second Half | number |  |
| `year_and_months` | Year and Months | text |  |

### wpti-gvdi

**NHIS Interactive Quarterly Early Release Estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/wpti-gvdi.json`
- Metadata: `GET https://data.cdc.gov/api/views/wpti-gvdi.json`; page: https://data.cdc.gov/d/wpti-gvdi
- Topics: Category: National Center for Health Statistics
- Tags: `nhis`, `key health indicators`, `early release`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`
- Rows: 528. Data updated: 2025-06-24. Probe status: 200.
- Update frequency: R/P3M.
- Source: NCHS/DHIS
- Description: Interactive Quarterly Early Release Estimates provide health statistics since 2019 based on data from the National Health Interview Survey (NHIS) for selected health topics for adults aged 18 years and over. All estimates are unadjusted percentages based on preliminary data files and are released prior to final data editing and final weighting to provide access to the most recent information from the NHIS. Estimates presented here are based on quarterly data. Estimates based on half-year data, with groupings by demographic characteristics, are available in the Interactive Biannual Early Relea…
- Sample row fields ($limit=1): `outcome_or_indicator`, `percentage`, `confidence_interval`, `title`, `description`, `year`, `quarter`, `year_and_quarter`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `outcome_or_indicator` | Outcome (or Indicator) | text |  |
| `percentage` | Percentage | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `title` | Title | text |  |
| `description` | Description | text |  |
| `year` | Year | number |  |
| `quarter` | Quarter | number |  |
| `year_and_quarter` | Year and Quarter | text |  |

### 5pqj-rvh4

**NHIS Teen** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/5pqj-rvh4.json`
- Metadata: `GET https://data.cdc.gov/api/views/5pqj-rvh4.json`; page: https://data.cdc.gov/d/5pqj-rvh4
- Topics: Category: National Center for Health Statistics
- Tags: `summary health statistics`, `nhis`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-food-access`, `sdoh-workplace`
- Rows: 3,400. Data updated: 2024-09-03. Probe status: 200.
- Source: NCHS/DHIS
- Description: Interactive Summary Health Statistics for Teens provide estimates of selected health topics for youth aged 12-17 years based on final data from the National Health Interview Survey— Teen.
- Sample row fields ($limit=1): `stat_group`, `stat_var`, `outcome_or_indicator`, `row_group`, `row_var`, `row_label`, `rowlevels`, `col_group`, `col_var`, `col_label`, `group`, `percentage`, `confidence_interval`, `title`, `new_caption2`, `figure`, `cr_p_reliable`, `cr_q_reliable`, `zero`, `date_range`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `stat_group` | stat_group | text |  |
| `stat_var` | stat_var | text |  |
| `outcome_or_indicator` | Outcome (or Indicator) | text |  |
| `row_group` | row_group | text |  |
| `row_var` | row_var | text |  |
| `row_label` | row_label | text |  |
| `rowlevels` | rowLevels | text |  |
| `col_group` | col_group | text |  |
| `col_var` | col_var | text |  |
| `col_label` | col_label | text |  |
| `group` | Group | text |  |
| `percentage` | Percentage | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `title` | Title | text |  |
| `description` | Description | text |  |
| `new_caption2` | new_caption2 | text |  |
| `figure` | FIGURE | number |  |
| `cr_p_reliable` | CR_P_RELIABLE | number |  |
| `cr_q_reliable` | CR_Q_RELIABLE | number |  |
| `zero` | ZERO | number |  |
| `kg_flag` | KG_FLAG | text |  |
| `date_range` | Date Range | text |  |

### 3nzu-udr9

**Normal weight, overweight, and obesity among adults aged 20 and over, by selected characteristics: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3nzu-udr9.json`
- Metadata: `GET https://data.cdc.gov/api/views/3nzu-udr9.json`; page: https://data.cdc.gov/d/3nzu-udr9
- Topics: Category: National Center for Health Statistics
- Tags: `obesity`, `overweight`, `chronic conditions`, `health risk factors`, `adult`, `african americans`, `hispanic americans`, `poverty`, `sex`, `european continental ancestry group`, `asian continental ancestry group`, `continental population groups`, `age`, `health us`, `sdoh-poverty-income`
- Rows: 3,360. Data updated: 2022-04-28. Probe status: 200.
- Update frequency: R/P1Y.
- Source: NCHS/DAE
- Description: Data on normal weight, overweight, and obesity among adults aged 20 and over by selected population characteristics. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder (https://www.cdc.gov/nchs/hus/contents2019.htm) for critical information about measures, definitions, and changes over time. SOURCE: NCHS, National Health and Nutrition Examination Survey. For more information on the National Health and Nutrition Examination Survey, see the corresponding Appendix entry at https://www.cdc.gov/nchs/data/hus/hus19-appendix-508.pdf.
- Sample row fields ($limit=1): `indicator`, `panel`, `panel_num`, `unit`, `unit_num`, `stub_name`, `stub_name_num`, `stub_label`, `stub_label_num`, `year`, `year_num`, `age`, `age_num`, `estimate`, `se`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | INDICATOR | text | Measure being estimated. |
| `panel` | PANEL | text | Submeasures of INDICATOR. Datasets may have multiple panels. |
| `panel_num` | PANEL_NUM | number | Numeric code for levels of PANEL that may be used for easier coding or formatting of the PANEL variable. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `year` | YEAR | text | Data year or range of data years pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `age` | AGE | text | Age group pertaining to the estimate. |
| `age_num` | AGE_NUM | number | Numeric code for levels of AGE that may be used for easier coding or formatting of the AGE variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `se` | SE | number | Calculated standard error of the estimate. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnotes in the source table (Excel) for more information. |

### 9gay-j69q

**Obesity among children and adolescents aged 2–19 years, by selected characteristics: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/9gay-j69q.json`
- Metadata: `GET https://data.cdc.gov/api/views/9gay-j69q.json`; page: https://data.cdc.gov/d/9gay-j69q
- Topics: Category: National Center for Health Statistics
- Tags: `adolescent`, `african americans`, `child`, `hispanic americans`, `obesity`, `poverty`, `sex`, `european continental ancestry group`, `asian continental ancestry group`, `continental population groups`, `age`, `adult`, `overweight`, `chronic conditions`, `health risk factors`, `health us`, `sdoh-poverty-income`
- Rows: 840. Data updated: 2022-04-28. Probe status: 200.
- Update frequency: R/P1W.
- Source: NCHS/DAE
- Description: Data on obesity among children and adolescents aged 2-19 years by selected population characteristics. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder (https://www.cdc.gov/nchs/hus/contents2019.htm) for critical information about measures, definitions, and changes over time. SOURCE: NCHS, National Health and Nutrition Examination Survey. For more information on the National Health and Nutrition Examination Survey, see the corresponding Appendix entry at https://www.cdc.gov/nchs/data/hus/hus19-appendix-508.pdf.
- Sample row fields ($limit=1): `indicator`, `panel`, `panel_num`, `unit`, `unit_num`, `stub_name`, `stub_name_num`, `stub_label_num`, `stub_label`, `year`, `year_num`, `age`, `age_num`, `estimate`, `se`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | INDICATOR | text | Measure being estimated. |
| `panel` | PANEL | text | Submeasures of INDICATOR. Datasets may have multiple panels. |
| `panel_num` | PANEL_NUM | number | Numeric code for levels of PANEL that may be used for easier coding or formatting of the PANEL variable. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `year` | YEAR | text | Data year or range of data years pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `age` | AGE | text | Age group pertaining to the estimate. |
| `age_num` | AGE_NUM | number | Numeric code for levels of AGE that may be used for easier coding or formatting of the AGE variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `se` | SE | number | Calculated standard error of the estimate. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnotes in the source table (Excel) for more information. |

### kk8c-wtm4

**Physician Experiences Related to COVID-19 from the National Ambulatory Medical Care Survey** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/kk8c-wtm4.json`
- Metadata: `GET https://data.cdc.gov/api/views/kk8c-wtm4.json`; page: https://data.cdc.gov/d/kk8c-wtm4
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `physicians`
- Rows: 160. Data updated: 2023-01-12. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DHCS
- Description: The National Ambulatory Medical Care Survey (NAMCS), conducted by the National Center for Health Statistics (NCHS), collects data on visits to physician offices to describe patterns of ambulatory care delivery in the United States. As part of NAMCS, the Physician Induction Interview collects information about practice characteristics at physician offices. Partway through the 2020 NAMCS, NCHS added questions to the Physician Induction Interview to assess physician experiences related to COVID-19 in office-based settings. The data include nationally representative estimates of experiences relat…
- Sample row fields ($limit=1): `figure`, `interview_period`, `interview_dates`, `measure`, `group`, `subgroup`, `percent`, `lower_95_ci`, `upper_95_ci`, `estimate_reliable`, `estimate_s_complement_reliable`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `figure` | Figure | number | Corresponds to the Figures reported on https://www.cdc.gov/nchs/covid19/namcs.htm |
| `interview_period` | Interview Period | text | The NAMCS interview period from which the estimate is derived |
| `interview_dates` | Interview Dates | text | The date range in which interviews were conducted |
| `measure` | Measure | text | Measures of physician experiences related to COVID-19 |
| `group` | Group | text | Estimates were reported for all physicians (total) and by office type, owner type, specialty type, and urbanicity of office location. |
| `subgroup` | Subgroup | text | Subcategories for each group |
| `percent` | Percent | number | Percent estimate |
| `lower_95_ci` | Lower 95% CI | number | Lower 95% confidence interval, using the Korn-Graubard method |
| `upper_95_ci` | Upper 95% CI | number | Upper 95% confidence interval, using the Korn-Graubard method |
| `estimate_reliable` | Estimate Reliable? | text | Indicator of percent’s (or proportion’s) reliability according to NCHS standards https://www.cdc.gov/nchs/data/series/sr_02/sr02_175.pdf |
| `estimate_s_complement_reliable` | Estimate's Complement Reliable? | text | Indicator of the compliment of the percent’s (or proportion’s) reliability according to NCHS standards https://www.cdc.gov/nchs/data/series/sr_02/sr02_175.pdf |

### jfbs-8cpp

**Population Group Estimates used in the Healthy People 2020 Overview of Health Disparities** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/jfbs-8cpp.json`
- Metadata: `GET https://data.cdc.gov/api/views/jfbs-8cpp.json`; page: https://data.cdc.gov/d/jfbs-8cpp
- Topics: Category: National Center for Health Statistics
- Tags: `healthy people 2020`, `health disparities`, `sdoh-poverty-income`, `sdoh-employment`, `sdoh-food-insecurity`, `sdoh-housing-stability`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-literacy`, `sdoh-early-childhood`, `sdoh-access-to-health-care`, `sdoh-source-of-health-care`, `sdoh-use-of-health-care`, `sdoh-health-literacy`, `sdoh-food-access`, `sdoh-housing-quality`, `sdoh-crime-violence`, `sdoh-environmental`, `sdoh-workplace`, `sdoh-transportation`, `sdoh-social-emotional`, `sdoh-civic-participation`, `sdoh-discrimination`, `sdoh-racism`, `sdoh-incarceration`, `sdoh-language`
- Rows: 6,978. Data updated: 2022-03-08. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DAE
- Description: The Overview of Health Disparities analysis is a component of the Healthy People 2020 (HP2020) Final Review. The analysis included 611 objectives in HP2020. See Technical Notes for the Healthy People 2020 Overview of Health Disparities (https://www.cdc.gov/nchs/healthy_people/hp2020/health-disparities.htm) for additional information and criteria for objectives, data years, and population characteristics included in the analysis and statistical formulas and definitions for the disparities measures. This file contains estimates and standard errors for the baseline and final years for individual…
- Sample row fields ($limit=1): `hp2020_objective`, `objective_description`, `topic_area`, `population_group`, `baseline_year_s`, `final_year_s`, `baseline_value`, `standard_error_of_baseline`, `final_value`, `standard_error_of_final_value`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `hp2020_objective` | HP2020 objective | text | The analysis included 611 HP2020 objectives that met the criteria for the population characteristics in the disparities analysis (see Technical Notes). |
| `objective_description` | Objective description | text |  |
| `topic_area` | Topic area | text | The HP2020 topic area corresponding to the objective included in the disparities analysis. |
| `population_group` | Population group | text | Category name for the population groups included in the disparities analysis for the corresponding baseline and final data points. |
| `baseline_year_s` | Baseline year(s) | text | Baseline year(s) for the corresponding objective in the disparities analysis. |
| `final_year_s` | Final year(s) | text | Final year(s) for the corresponding objective in the disparities analysis. |
| `baseline_value` | Baseline value | number | Value for the corresponding population group at the baseline year(s) of the disparities analysis for the objective. |
| `standard_error_of_baseline` | Standard error of baseline value | number | Standard error of the value for the corresponding population group at the baseline year(s) of the disparities analysis for the objective. A blank cell indicates that the standard error was not available. |
| `final_value` | Final value | number | Value for the corresponding population group at the final year(s) of the disparities analysis for the objective. |
| `standard_error_of_final_value` | Standard error of final value | number | Standard error of the value for the corresponding population group at the final year(s) of the disparities analysis for the objective. A blank cell indicates that the standard error was not available. |

### gsea-w83j

**Post-COVID Conditions** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/gsea-w83j.json`
- Metadata: `GET https://data.cdc.gov/api/views/gsea-w83j.json`; page: https://data.cdc.gov/d/gsea-w83j
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `post-covid`
- Rows: 18,639. Data updated: 2024-10-04. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DHIS
- Description: As part of an ongoing partnership with the Census Bureau, the National Center for Health Statistics (NCHS) recently added questions to assess the prevalence of post-COVID-19 conditions (long COVID), on the experimental Household Pulse Survey. This 20-minute online survey was designed to complement the ability of the federal statistical system to rapidly respond and provide relevant information about the impact of the coronavirus pandemic in the U.S. Data collection began on April 23, 2020. Beginning in Phase 3.5 (on June 1, 2022), NCHS included questions about the presence of symptoms of COVI…
- Sample row fields ($limit=1): `indicator`, `group`, `state`, `subgroup`, `phase`, `time_period`, `time_period_label`, `time_period_start_date`, `time_period_end_date`, `value`, `lowci`, `highci`, `confidence_interval`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | Indicator | text | Outcome of interest |
| `group` | Group | text | Covariates or subgroups |
| `state` | State | text | National or state-specific |
| `subgroup` | Subgroup | text | Subgroup levels |
| `phase` | Phase | number | Survey phase label |
| `time_period` | Time Period | text | Week label |
| `time_period_label` | Time Period Label | text | Weeks of data collection |
| `time_period_start_date` | Time Period Start Date | calendar_date |  |
| `time_period_end_date` | Time Period End Date | calendar_date |  |
| `value` | Value | number |  |
| `lowci` | LowCI | number |  |
| `highci` | HighCI | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `quartile_range` | Quartile range | text |  |
| `quartile_number` | Quartile number | number |  |
| `suppression_flag` | Suppression Flag | text |  |

### 367e-pucc

**Preliminary Estimates of Visits to Health Centers in the United States, January 2022-December 2025** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/367e-pucc.json`
- Metadata: `GET https://data.cdc.gov/api/views/367e-pucc.json`; page: https://data.cdc.gov/d/367e-pucc
- Topics: Category: National Center for Health Statistics
- Tags: none
- Rows: 6,208. Data updated: 2026-06-30. Probe status: 200.
- Update frequency: Monthly.
- Source: NCHS/DHCS
- Description: The National Ambulatory Medical Care Survey (NAMCS) Health Center Component, conducted by the National Center for Health Statistics (NCHS), collects annual data on visits to health centers to describe patterns of utilization and provision of ambulatory care delivery in the United States. Data are collected from federally qualified health centers (FQHCs) and FQHC look-alikes from all 50 U.S. states and the District of Columbia and are used to develop nationally representative estimates. The data include preliminary, biannual counts and rates of health center visits from January 2022-December 2…
- Sample row fields ($limit=1): `time_period`, `measure_type`, `measure`, `group`, `subgroup`, `estimate_type`, `estimate`, `standard_error`, `lower_95_ci`, `upper_95_ci`, `reliable`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `time_period` | Time Period | text | Six month period from which the estimate was derived |
| `measure_type` | Measure Type | text | Type of measure: Diagnosis Chapter, maternal health, mental health, or respiratory health indicator |
| `measure` | Measure | text | Name of the diagnosis chapter, maternal health, mental health, or respiratory health indicator |
| `group` | Group | text | Indicator of the grouping variable: age, race/ethnicity, or sex |
| `subgroup` | Subgroup | text | Subcategories for each group |
| `estimate_type` | Estimate Type | text | Type of estimate: visit count or visit rate (per 1,000 people) |
| `estimate` | Estimate | number | Preliminary estimate of selected measure |
| `standard_error` | Standard Error | number | Standard error of the estimate |
| `lower_95_ci` | Lower 95% CI | number | Lower 95% confidence interval of the estimate |
| `upper_95_ci` | Upper 95% CI | number | Upper 95% confidence interval of the estimate |
| `reliable` | Reliable | text | Indicator of estimate’s reliability according to NCHS standards |

### 28df-2bwy

**Prevalence of Selected Measures Among Adults Aged 20 and Over: United States, 1999-2000 through 2017-2018** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/28df-2bwy.json`
- Metadata: `GET https://data.cdc.gov/api/views/28df-2bwy.json`; page: https://data.cdc.gov/d/28df-2bwy
- Topics: Category: National Center for Health Statistics
- Tags: `hypertension`, `high cholesterol`, `obesity`, `nhanes`
- Rows: 360. Data updated: 2020-12-16. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DHNES
- Description: This data represents the age-adjusted prevalence of high total cholesterol, hypertension, and obesity among US adults aged 20 and over between 1999-2000 to 2017-2018. Notes: * All estimates are age adjusted by the direct method to the U.S. Census 2000 population using age groups 20–39, 40–59, and 60 and over. Definitions Hypertension: Systolic blood pressure greater than or equal to 130 mmHg or diastolic blood pressure greater than or equal to 80 mmHg, or currently taking medication to lower high blood pressure High total cholesterol: Serum total cholesterol greater than or equal to 240 mg/dL…
- Sample row fields ($limit=1): `survey_years`, `sex`, `age_group`, `measure`, `percent`, `standard_error`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `survey_years` | Survey Years | text |  |
| `sex` | Sex | text |  |
| `age_group` | Age Group | text |  |
| `measure` | Measure | text |  |
| `percent` | Percent | number |  |
| `standard_error` | Standard Error | number |  |

### yrur-wghw

**Provisional COVID-19 death counts and rates by month, jurisdiction of residence, and demographic characteristics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/yrur-wghw.json`
- Metadata: `GET https://data.cdc.gov/api/views/yrur-wghw.json`; page: https://data.cdc.gov/d/yrur-wghw
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `mortality`, `deaths`, `death rate`, `united states`, `hhs region`, `coronavirus`, `covid-19`, `monthly`, `race`, `hispanic origin`, `sex`, `age`, `age group`
- Rows: 71,280. Data updated: 2026-09-17. Probe status: 200.
- Update frequency: R/P1W.
- Source: NCHS/DVS
- Description: This file contains COVID-19 death counts and rates by month and year of death, jurisdiction of residence (U.S., HHS Region) and demographic characteristics (sex, age, race and Hispanic origin, and age/race and Hispanic origin). United States death counts and rates include the 50 states, plus the District of Columbia. Deaths with confirmed or presumed COVID-19, coded to ICD–10 code U07.1. Number of deaths reported in this file are the total number of COVID-19 deaths received and coded as of the date of analysis and may not represent all deaths that occurred in that period. Counts of deaths occ…
- Sample row fields ($limit=1): `data_as_of`, `jurisdiction_residence`, `year`, `month`, `group`, `subgroup1`, `covid_deaths`, `footnote`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | data_as_of | calendar_date | Date of analysis |
| `jurisdiction_residence` | jurisdiction_residence | text | Jurisdiction of residence |
| `year` | year | number | Year of death |
| `month` | month | number | Month of death |
| `group` | group | text | Demographic characteristic |
| `subgroup1` | subgroup1 | text | Demographic subgroup 1 |
| `subgroup2` | subgroup2 | text | Demographic subgroup 2 |
| `covid_deaths` | COVID_deaths | number | Deaths involving COVID-19 (ICD-10 code U07.1) |
| `crude_covid_rate` | crude_COVID_rate | number | Crude COVID-19 death rate |
| `aa_covid_rate` | aa_COVID_rate | number | Age-adjusted COVID-19 death rate |
| `crude_covid_rate_ann` | crude_COVID_rate_ann | number | Crude COVID-19 death rate - annualized |
| `aa_covid_rate_ann` | aa_COVID_rate_ann | number | Age-adjusted COVID-19 death rate - annualized |
| `footnote` | footnote | text | Footnote |

### dmnu-8erf

**Provisional COVID-19 death counts and rates, by jurisdiction of residence and demographic characteristics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/dmnu-8erf.json`
- Metadata: `GET https://data.cdc.gov/api/views/dmnu-8erf.json`; page: https://data.cdc.gov/d/dmnu-8erf
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `mortality`, `deaths`, `death rate`, `united states`, `hhs region`, `coronavirus`, `covid-19`, `weekly`
- Rows: 177,309. Data updated: 2023-10-26. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: This file contains COVID-19 death counts and rates by jurisdiction of residence (U.S., HHS Region) and demographic characteristics (sex, age, race and Hispanic origin, and age/race and Hispanic origin). United States death counts and rates include the 50 states, plus the District of Columbia. Deaths with confirmed or presumed COVID-19, coded to ICD–10 code U07.1. Number of deaths reported in this file are the total number of COVID-19 deaths received and coded as of the date of analysis and may not represent all deaths that occurred in that period. Counts of deaths occurring before or after th…
- Sample row fields ($limit=1): `data_as_of`, `jurisdiction_residence`, `data_period_start`, `data_period_end`, `group`, `subgroup1`, `covid_deaths`, `crude_covid_rate`, `aa_covid_rate`, `crude_covid_rate_ann`, `aa_covid_rate_ann`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | data_as_of | calendar_date | Date of analysis |
| `jurisdiction_residence` | jurisdiction_residence | text | Jurisdiction of residence |
| `data_period_start` | data_period_start | calendar_date | First date of data period |
| `data_period_end` | data_period_end | calendar_date | Last date of data period |
| `group` | group | text | Demographic characteristic |
| `subgroup1` | subgroup1 | text | Demographic subgroup 1 |
| `subgroup2` | subgroup2 | text | Demographic subgroup 2 |
| `covid_deaths` | COVID_deaths | number | Deaths involving COVID-19 (ICD-10 code U07.1) |
| `crude_covid_rate` | crude_COVID_rate | number | Crude COVID-19 death rate |
| `aa_covid_rate` | aa_COVID_rate | number | Age-adjusted COVID-19 death rate |
| `crude_covid_rate_ann` | crude_COVID_rate_ann | number | Crude COVID-19 death rate - annualized |
| `aa_covid_rate_ann` | aa_COVID_rate_ann | number | Age-adjusted COVID-19 death rate - annualized |
| `footnote` | footnote | text | Footnote |

### 3apk-4u4f

**Provisional COVID-19 Death Counts by Age in Years, 2020-2023** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3apk-4u4f.json`
- Metadata: `GET https://data.cdc.gov/api/views/3apk-4u4f.json`; page: https://data.cdc.gov/d/3apk-4u4f
- Topics: Category: National Center for Health Statistics
- Tags: `coronavirus`, `deaths`, `mortality`, `covid-19`, `nchs`, `nvss`, `provisional`, `united states`, `age`, `sex`, `all causes`, `children`
- Rows: 174. Data updated: 2023-06-28. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective June 28, 2023, this dataset will no longer be updated. Similar data are accessible from CDC WONDER (https://wonder.cdc.gov/mcd-icd10-provisional.html). Cumulative deaths involving COVID-19 reported to NCHS by sex and age in years, in the United States.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `sex`, `age_years`, `total_deaths`, `covid19_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Data of analysis |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `sex` | Sex | text | Sex |
| `age_years` | Age Years | text | Age in years |
| `total_deaths` | Total deaths | number | Deaths from all causes |
| `covid19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |

### r8kw-7aab

**Provisional COVID-19 Death Counts by Week Ending Date and State** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/r8kw-7aab.json`
- Metadata: `GET https://data.cdc.gov/api/views/r8kw-7aab.json`; page: https://data.cdc.gov/d/r8kw-7aab
- Topics: Category: National Center for Health Statistics
- Tags: `coronavirus`, `state`, `united states`, `nchs`, `covid-19`, `mortality`, `pneumonia`, `influenza`, `nvss`, `provisional`, `weekly`, `monthly`, `yearly`, `all causes`, `puerto rico`, `deaths`
- Rows: 24,138. Data updated: 2026-11-05. Probe status: 200.
- Update frequency: R/P1W.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will be updated weekly on Thursdays. Deaths involving COVID-19, pneumonia, and influenza reported to NCHS by week ending date and by state
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `group`, `year`, `mmwr_week`, `week_ending_date`, `state`, `covid_19_deaths`, `total_deaths`, `percent_of_expected_deaths`, `pneumonia_deaths`, `pneumonia_and_covid_19_deaths`, `influenza_deaths`, `pneumonia_influenza_or_covid_19_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `group` | Group | text | Time period of reporting |
| `year` | Year | text | Year of reporting |
| `month` | Month | number | Month of reporting |
| `mmwr_week` | MMWR Week | number | MMWR week of reporting |
| `week_ending_date` | Week Ending Date | calendar_date | Week-ending date for the week of reporting |
| `state` | State | text | Jurisdiction of occurrence |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-10 code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `percent_of_expected_deaths` | Percent of Expected Deaths | number | Percent of expected deaths |
| `pneumonia_deaths` | Pneumonia Deaths | number | Pneumonia Deaths (ICD-10 codes J12.0-J18.9) |
| `pneumonia_and_covid_19_deaths` | Pneumonia and COVID-19 Deaths | number | Deaths with Pneumonia and COVID-19 (ICD-10 codes J12.0-J18.9 and U07.1) |
| `influenza_deaths` | Influenza Deaths | number | Influenza Deaths (ICD-10 codes J09-J11) |
| `pneumonia_influenza_or_covid_19_deaths` | Pneumonia, Influenza, or COVID-19 Deaths | number | Pneumonia, Influenza, or COVID-19 Deaths (ICD-10 codes J12.0-J18.9, J09-J11, U07.1) |
| `footnote` | Footnote | text | Suppressed counts (1-9) |

### kn79-hsxy

**Provisional COVID-19 Death Counts in the United States by County** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/kn79-hsxy.json`
- Metadata: `GET https://data.cdc.gov/api/views/kn79-hsxy.json`; page: https://data.cdc.gov/d/kn79-hsxy
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `mortality`, `united states`, `county`, `covid-19`, `coronavirus`, `nchs`, `all causes`, `provisional`, `nvss`, `sdoh-environmental`
- Rows: 3,089. Data updated: 2023-06-28. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective June 28, 2023, this dataset will no longer be updated. Similar data are accessible from CDC WONDER (https://wonder.cdc.gov/mcd-icd10-provisional.html) Provisional count of deaths involving COVID-19 by county of occurrence, in the United States, 2020-2023.
- Sample row fields ($limit=1): `data_as_of`, `start_week`, `end_week`, `state_name`, `county_name`, `county_fips_code`, `urban_rural_code`, `total_death`, `footnote`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Date as of | calendar_date | Date of analysis |
| `start_week` | Start Date | calendar_date | First date of data period |
| `end_week` | End Date | calendar_date | Last date of data period |
| `state_name` | State | text | State of occurrence |
| `county_name` | County name | text | County of occurrence |
| `county_fips_code` | FIPS County Code | number | FIPS County Code |
| `urban_rural_code` | Urban Rural Code | text | Urban-rural classification is based on the 2013 National Center for Health Statistics Urban-Rural Classification Scheme for Counties |
| `covid_death` | Deaths involving COVID-19 | number | Deaths involving COVID-19, coded to ICD-code U07.1 |
| `total_death` | Deaths from All Causes | number | Deaths from all causes of death |
| `footnote` | Footnote | text | Footnote |

### mpx5-t7tu

**Provisional COVID-19 death counts, rates, and percent of total deaths, by jurisdiction of residence** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/mpx5-t7tu.json`
- Metadata: `GET https://data.cdc.gov/api/views/mpx5-t7tu.json`; page: https://data.cdc.gov/d/mpx5-t7tu
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `mortality`, `deaths`, `coronavirus`, `covid-19`, `united states`, `hhs region`, `state`, `death rate`, `puerto rico`
- Rows: 45,565. Data updated: 2026-09-17. Probe status: 200.
- Update frequency: R/P1W.
- Source: NCHS/DVS
- Description: This file contains COVID-19 death counts, death rates, and percent of total deaths by jurisdiction of residence. The data is grouped by different time periods including 3-month period, weekly, and total (cumulative since January 1, 2020). United States death counts and rates include the 50 states, plus the District of Columbia and New York City. New York state estimates exclude New York City. Puerto Rico is included in HHS Region 2 estimates. Deaths with confirmed or presumed COVID-19, coded to ICD–10 code U07.1. Number of deaths reported in this file are the total number of COVID-19 deaths r…
- Sample row fields ($limit=1): `data_as_of`, `jurisdiction_residence`, `group`, `data_period_start`, `data_period_end`, `covid_deaths`, `covid_pct_of_total`, `crude_covid_rate`, `aa_covid_rate`, `crude_covid_rate_ann`, `aa_covid_rate_ann`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | data_as_of | calendar_date | Date of analysis |
| `jurisdiction_residence` | Jurisdiction_Residence | text | Jurisdiction of Residence |
| `group` | Group | text | Time period of reporting |
| `data_period_start` | data_period_start | calendar_date | First date of data period |
| `data_period_end` | data_period_end | calendar_date | Last date of data period |
| `covid_deaths` | COVID_deaths | number | Deaths involving COVID-19 (ICD-10 code U07.1) |
| `covid_pct_of_total` | COVID_pct_of_total | number | Percent of deaths due to COVID-19 |
| `pct_change_wk` | pct_change_wk | number | Relative percent change by week, % of deaths due to COVID-19 |
| `pct_diff_wk` | pct_diff_wk | number | Absolute percent change by week, % of deaths due to COVID-19 |
| `crude_covid_rate` | crude_COVID_rate | number | Crude COVID-19 death rate |
| `aa_covid_rate` | aa_COVID_rate | number | Age-adjusted COVID-19 death rate |
| `crude_covid_rate_ann` | crude_COVID_rate_ann | number | Crude COVID-19 death rate - annualized |
| `aa_covid_rate_ann` | aa_COVID_rate_ann | number | Age-adjusted COVID-19 death rate - annualized |
| `footnote` | footnote | text | Footnote |

### k8wy-p9cg

**Provisional COVID-19 Deaths by County, and Race and Hispanic Origin** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/k8wy-p9cg.json`
- Metadata: `GET https://data.cdc.gov/api/views/k8wy-p9cg.json`; page: https://data.cdc.gov/d/k8wy-p9cg
- Topics: Category: National Center for Health Statistics
- Tags: `county`, `race`, `coronavirus`, `covid-19`, `mortality`, `united states`, `provisional`, `nvss`, `hispanic origin`, `deaths`, `all causes`, `nchs`, `sdoh-environmental`
- Rows: 3,687. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. County data on race and Hispanic origin is available for counties with more than 100 COVID-19 deaths. Deaths are cumulative from the week ending January 4, 2020 to the most recent reporting week, and based on county of occurrence. Data is provisional. Urban-rural classification is based on the 2013 National Center for Health Statistics Urban-Rural Classification Scheme for Counties (https://www.cdc.gov/nchs/data_access/urban_rural.htm).
- Sample row fields ($limit=1): `data_as_of`, `start_week`, `end_week`, `state`, `county_name`, `urbanruralcode`, `fipsstate`, `fipscounty`, `fipscode`, `indicator`, `all_deaths_total`, `covid_19_deaths_total`, `non_hispanic_white`, `non_hispanic_black`, `non_hispanic_american_indian`, `non_hispanic_asian`, `non_hispanic_nhopi`, `hispanic`, `other`, `urbanruraldesc`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Date of analysis |
| `start_week` | Start Date | calendar_date |  |
| `end_week` | End Date | calendar_date |  |
| `state` | State | text | Jurisdiction of occurrence |
| `county_name` | County Name | text | County of occurrence |
| `urbanruralcode` | Urban Rural Code | number | Urban Rural Code |
| `fipsstate` | FIPS State | number | FIPS State Code |
| `fipscounty` | FIPS County | number | FIPS County Code |
| `fipscode` | FIPS Code | number | FIPS Code |
| `indicator` | Indicator | text | Distribution of all-cause deaths (%), Distribution of COVID-19 deaths (%), Distribution of population (%) |
| `all_deaths_total` | Total deaths | number | Deaths from all causes of death |
| `covid_19_deaths_total` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |
| `non_hispanic_white` | Non-Hispanic White | number | Non-Hispanic White |
| `non_hispanic_black` | Non-Hispanic Black | number | Non-Hispanic Black or African American |
| `non_hispanic_american_indian` | Non-Hispanic American Indian or Alaska Native | number | Non-Hispanic American Indian or Alaska Native |
| `non_hispanic_asian` | Non-Hispanic Asian | number | Non-Hispanic Asian |
| `non_hispanic_nhopi` | Non-Hispanic Native Hawaiian or Other Pacific Islander | number | Non-Hispanic Native Hawaiian or Other Pacific Islander |
| `hispanic` | Hispanic | number | Hispanic or Latino |
| `other` | Other | number | More than one race and unknown |
| `urbanruraldesc` | Urban Rural Description | text | Urban Rural Description |
| `footnote` | Footnote | text | Data based on counts less than 10 suppressed |

### tpcp-uiv5

**Provisional COVID-19 Deaths by HHS Region, Race, and Age** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/tpcp-uiv5.json`
- Metadata: `GET https://data.cdc.gov/api/views/tpcp-uiv5.json`; page: https://data.cdc.gov/d/tpcp-uiv5
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `race`, `hispanic origin`, `age`, `deaths`, `nchs`, `nvss`, `provisional`, `coronavirus`, `age group`, `weekly`, `all causes`, `mortality`, `united states`, `puerto rico`, `hhs region`, `children`
- Rows: 194,040. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. Deaths involving COVID-19 reported to NCHS by time-period, HHS region, race and Hispanic origin, and age group. United States death counts include the 50 states, plus the District of Columbia and New York City. The ten (10) United States Department of Health and Human Services (HHS) regions include the following jurisdictions. Region 1: Connecticut, Maine, Massachusetts, New Hampshire, Rhode Island, Vermont; Region 2: New Jersey, New York, New York City, Puerto Rico; Region 3…
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `group`, `mmwr_year`, `mmwr_week`, `week_ending_date`, `hhs_region`, `race_and_hispanic_origin`, `age_group`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date | Start Date |
| `end_date` | End Date | calendar_date | End Date |
| `group` | Group | text |  |
| `mmwr_year` | Year | text | Year |
| `month` | Month | text | Month |
| `mmwr_week` | MMWR Week | number | MMWR Week |
| `week_ending_date` | Week-Ending Date | calendar_date | Week-Ending Date |
| `hhs_region` | HHS Region | text | HHS Region |
| `race_and_hispanic_origin` | Race and Hispanic Origin Group | text | Race and Hispanic Origin Group |
| `age_group` | Age Group | text | Age Group |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `footnote` | Footnote | text |  |

### 4va6-ph5s

**Provisional COVID-19 Deaths by Place of Death and Age** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/4va6-ph5s.json`
- Metadata: `GET https://data.cdc.gov/api/views/4va6-ph5s.json`; page: https://data.cdc.gov/d/4va6-ph5s
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `mortality`, `nchs`, `covid-19`, `coronavirus`, `age`, `age group`, `influenza`, `pneumonia`, `united states`, `state`, `puerto rico`, `place of death`, `all causes`, `nvss`, `provisional`, `yearly`, `monthly`
- Rows: 218,700. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. Deaths involving COVID-19, influenza, and pneumonia reported to NCHS by jurisdiction of occurrence, place of death, and age group.
- Sample row fields ($limit=1): `data_as_of`, `start_week`, `end_week`, `group`, `hhs_region`, `state`, `place_of_death`, `age_group`, `covid_19_deaths`, `total_deaths`, `pneumonia`, `pneumonia_and_covid`, `influenza_deaths`, `pneumonia_influenza_or_covid`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Date of analysis |
| `start_week` | Start Date | calendar_date | First date of data period |
| `end_week` | End Date | calendar_date | Last date of data period |
| `group` | Group | text | Details whether data is by Month, by Year, or Total. |
| `year` | Year | number | Year in which death occurred |
| `month` | Month | number | Month in which death occurred |
| `hhs_region` | HHS Region | number | HHS Region |
| `state` | State | text | Jurisdiction of Occurrence |
| `place_of_death` | Place of Death | text | Place of death |
| `age_group` | Age group | text | Age group |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `pneumonia` | Pneumonia Deaths | number | Pneumonia Deaths (ICD-10 codes J12.0-J18.9) |
| `pneumonia_and_covid` | Pneumonia and COVID-19 Deaths | number | Deaths with Pneumonia and COVID-19 (ICD-10 codes J12.0-J18.9 and U07.1) |
| `influenza_deaths` | Influenza Deaths | number | Influenza Deaths (ICD-10 codes J09-J11) |
| `pneumonia_influenza_or_covid` | Pneumonia, Influenza, or COVID-19 Deaths | number | Deaths with Pneumonia, Influenza, or COVID-19 (ICD-10 codes U07.1 or J09-J18.9) |
| `footnote` | Footnote | text | Suppressed counts (1-9) |

### uggs-hy5q

**Provisional COVID-19 Deaths by Place of Death and State** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/uggs-hy5q.json`
- Metadata: `GET https://data.cdc.gov/api/views/uggs-hy5q.json`; page: https://data.cdc.gov/d/uggs-hy5q
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `coronavirus`, `covid-19`, `state`, `united states`, `mortality`, `monthly`, `yearly`, `nvss`, `place of death`, `provisional`, `puerto rico`, `deaths`, `influenza`, `pneumonia`
- Rows: 22,842. Data updated: 2023-06-28. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective June 28, 2023, this dataset will no longer be updated. Data deaths by place of death are available in this dataset https://data.cdc.gov/NCHS/d/4va6-ph5s. Deaths involving COVID-19, pneumonia and influenza reported to NCHS by place of death and state, United States.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `group`, `state`, `place_of_death`, `covid_19_deaths`, `total_deaths`, `pneumonia_deaths`, `pneumonia_and_covid_19_deaths`, `influenza_deaths`, `pneumonia_influenza_or_covid`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `group` | Group | text | Indicates whether measure is by Month, by Year, or Total. |
| `year` | Year | number | Year in which death occurred |
| `month` | Month | number | Month in which death occurred |
| `state` | State | text | Jurisdiction of occurrence |
| `place_of_death` | Place of Death | text | Place of Death |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `pneumonia_deaths` | Pneumonia Deaths | number | Pneumonia Deaths (ICD-10 codes J12.0-J18.9) |
| `pneumonia_and_covid_19_deaths` | Pneumonia and COVID-19 Deaths | number | Deaths with Pneumonia and COVID-19 (ICD-10 codes J12.0-J18.9 and U07.1) |
| `influenza_deaths` | Influenza Deaths | number | Influenza Deaths (ICD-10 codes J09-J11) |
| `pneumonia_influenza_or_covid` | Pneumonia, Influenza, or COVID-19 Deaths | number | Deaths with Pneumonia, Influenza, or COVID-19 (ICD-10 codes U07.1 or J09-J18.9) |
| `footnote` | Footnote | text | Suppressed counts (1-9) |

### ks3g-spdg

**Provisional COVID-19 Deaths by Race and Hispanic Origin, and Age** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ks3g-spdg.json`
- Metadata: `GET https://data.cdc.gov/api/views/ks3g-spdg.json`; page: https://data.cdc.gov/d/ks3g-spdg
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `coronavirus`, `covid-19`, `pneumonia`, `influenza`, `hispanic origin`, `race`, `state`, `age group`, `nvss`, `united states`, `puerto rico`, `all causes`, `provisional`, `mortality`, `deaths`, `age`
- Rows: 6,489. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. Deaths involving COVID-19, pneumonia, and influenza reported to NCHS by race, age, and jurisdiction of occurrence.
- Sample row fields ($limit=1): `data_as_of`, `start_week`, `end_week`, `state`, `age_group_new`, `race_and_hispanic_origin`, `covid_19_deaths`, `total_deaths`, `pneumonia_deaths`, `pneumonia_and_covid_19_deaths`, `influenza_deaths`, `pneumonia_influenza_or_covid_19`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Date of analysis |
| `start_week` | Start Date | calendar_date | First date of data period |
| `end_week` | End Date | calendar_date | Last date of data period |
| `state` | State | text | Jurisdiction of occurrence |
| `age_group_new` | Age group | text | Age group |
| `race_and_hispanic_origin` | Race and Hispanic Origin Group | text | Race or Hispanic Origin Group |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `pneumonia_deaths` | Pneumonia Deaths | number | Pneumonia Deaths (ICD-10 codes J12.0-J18.9) |
| `pneumonia_and_covid_19_deaths` | Pneumonia and COVID-19 Deaths | number | Deaths with Pneumonia and COVID-19 (ICD-10 codes J12.0-J18.9 and U07.1) |
| `influenza_deaths` | Influenza Deaths | number | Influenza Deaths (ICD-10 codes J09-J11) |
| `pneumonia_influenza_or_covid_19` | Pneumonia, Influenza, or COVID-19 Deaths | number | Deaths with Pneumonia, Influenza, or COVID-19 (ICD-10 codes U07.1 or J09-J18.9) |
| `footnote` | Footnote | text | Suppressed counts (1-9) |

### 9bhg-hcku

**Provisional COVID-19 Deaths by Sex and Age** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/9bhg-hcku.json`
- Metadata: `GET https://data.cdc.gov/api/views/9bhg-hcku.json`; page: https://data.cdc.gov/d/9bhg-hcku
- Topics: Category: National Center for Health Statistics
- Tags: `age`, `sex`, `state`, `mortality`, `coronavirus`, `covid-19`, `nchs`, `united states`, `influenza`, `pneumonia`, `provisional`, `puerto rico`, `monthly`, `yearly`, `nvss`, `age group`, `deaths`
- Rows: 137,700. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. Deaths involving COVID-19, pneumonia, and influenza reported to NCHS by sex, age group, and jurisdiction of occurrence.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `group`, `state`, `sex`, `age_group`, `covid_19_deaths`, `total_deaths`, `pneumonia_deaths`, `pneumonia_and_covid_19_deaths`, `influenza_deaths`, `pneumonia_influenza_or_covid`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `group` | Group | text | Indicator of whether data measured by Month, by Year, or Total |
| `year` | Year | number | Year in which death occurred |
| `month` | Month | number | Month in which death occurred |
| `state` | State | text | Jurisdiction of occurrence |
| `sex` | Sex | text | Sex |
| `age_group` | Age Group | text | Age group |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `pneumonia_deaths` | Pneumonia Deaths | number | Pneumonia Deaths (ICD-10 codes J12.0-J18.9) |
| `pneumonia_and_covid_19_deaths` | Pneumonia and COVID-19 Deaths | number | Deaths with Pneumonia and COVID-19 (ICD-10 codes J12.0-J18.9 and U07.1) |
| `influenza_deaths` | Influenza Deaths | number | Influenza Deaths (ICD-10 codes J09-J11) |
| `pneumonia_influenza_or_covid` | Pneumonia, Influenza, or COVID-19 Deaths | number | Deaths with Pneumonia, Influenza, or COVID-19 (ICD-10 codes U07.1 or J09-J18.9) |
| `footnote` | Footnote | text | Suppressed counts (1-9) |

### 9hdi-ekmb

**Provisional COVID-19 Deaths by Week and County Social Vulnerability Index** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/9hdi-ekmb.json`
- Metadata: `GET https://data.cdc.gov/api/views/9hdi-ekmb.json`; page: https://data.cdc.gov/d/9hdi-ekmb
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `deaths`, `mortality`, `united states`, `weekly`, `covid-19`, `coronavirus`, `all causes`, `social vulnerability index`, `sdoh-environmental`
- Rows: 780. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. Deaths involving COVID-19 reported to NCHS by week and county Social Vulnerability Index (SVI) in the United States. SVI scores are from CDC/ASTDR's Geospatial Research, Analysis & Service Program 2018 database. These scores range from 0 to 1, and categorized as low (0-0.333), moderate (0.334-0.666) or high (0.667-1). More information on SVI can be found here: https://www.atsdr.cdc.gov/placeandhealth/svi/index.html
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `mmwr_year`, `mmwr_week`, `week_ending_date`, `social_vulnerability_index`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `start_date` | Start Date | calendar_date | First date of data period |
| `end_date` | End Date | calendar_date | Last date of data period |
| `mmwr_year` | MMWR Year | text | MMWR year of reporting |
| `mmwr_week` | MMWR Week | number | MMWR week of reporting |
| `week_ending_date` | Week-Ending Date | calendar_date | Week-ending date for the week of reporting |
| `social_vulnerability_index` | Social Vulnerability Index | text | County Social Vulnerability Index score |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-10 code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `footnote` | Footnote | text | Suppressed counts (1-9) |

### hkhc-f7hg

**Provisional COVID-19 Deaths by Week and Urbanicity** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/hkhc-f7hg.json`
- Metadata: `GET https://data.cdc.gov/api/views/hkhc-f7hg.json`; page: https://data.cdc.gov/d/hkhc-f7hg
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `mortality`, `deaths`, `provisional`, `united states`, `weekly`, `urbanicity`, `covid-19`, `all causes`, `coronavirus`
- Rows: 585. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. Provisional COVID-19 deaths by urbanicity and week. Deaths are based on the county of occurrence in the United States. Urbanicity is defined as metropolitan and non-metropolitan, based on the 2013 National Center for Health Statistics (NCHS) Urban-Rural Classification Scheme for Counties. Counties are classified as “metropolitan” if they are large central metro, large fringe metro, medium metro or small metro; and “non-metropolitan” if micropolitan or non-core.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `mmwr_year`, `mmwr_week`, `week_ending_date`, `jurisdiction_of_occurrence`, `urbanization_classification`, `covid_19_deaths`, `total_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date |  |
| `start_date` | Start Date | calendar_date |  |
| `end_date` | End Date | calendar_date |  |
| `mmwr_year` | MMWR Year | number |  |
| `mmwr_week` | MMWR Week | number |  |
| `week_ending_date` | Week-Ending Date | calendar_date |  |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text |  |
| `urbanization_classification` | Urbanization Classification | text |  |
| `covid_19_deaths` | COVID-19 Deaths | number |  |
| `total_deaths` | Total Deaths | number |  |
| `footnote` | Footnote | text |  |

### vsak-wrfu

**Provisional COVID-19 Deaths by Week, Sex, and Age** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/vsak-wrfu.json`
- Metadata: `GET https://data.cdc.gov/api/views/vsak-wrfu.json`; page: https://data.cdc.gov/d/vsak-wrfu
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `coronavirus`, `covid-19`, `sex`, `age group`, `united states`, `nvss`, `mortality`, `provisional`, `weekly`, `all causes`, `deaths`, `age`
- Rows: 6,552. Data updated: 2023-06-28. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective June 28, 2023, this dataset will no longer be updated. Similar data are accessible from CDC WONDER (https://wonder.cdc.gov/mcd-icd10-provisional.html). Deaths involving COVID-19 reported to NCHS by sex and age group and week ending date.
- Sample row fields ($limit=1): `data_as_of`, `state`, `mmwr_week`, `week_ending_date`, `sex`, `age_group`, `total_deaths`, `covid_19_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Date of analysis |
| `state` | State | text | Jurisdiction of occurrence |
| `mmwr_week` | MMWR Week | number | MMWR week number |
| `week_ending_date` | End Week | calendar_date | Last week-ending date of data period |
| `sex` | Sex | text | Sex |
| `age_group` | Age Group | text | Age group |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |

### pj7m-y5uh

**Provisional COVID-19 Deaths: Distribution of Deaths by Race and Hispanic Origin** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/pj7m-y5uh.json`
- Metadata: `GET https://data.cdc.gov/api/views/pj7m-y5uh.json`; page: https://data.cdc.gov/d/pj7m-y5uh
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `race`, `mortality`, `united states`, `state`, `covid-19`, `coronavirus`, `nchs`, `hispanic origin`, `provisional`, `nvss`
- Rows: 10,600. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. This data file contains the following indicators that can be used to illustrate potential differences in the burden of deaths due to COVID-19 according to race and ethnicity: count of COVID-19 deaths, distribution of COVID-19 deaths, unweighted distribution of population, and weighted distribution of population.
- Sample row fields ($limit=1): `data_as_of`, `start_week`, `end_week`, `year`, `group`, `state`, `indicator`, `non_hispanic_white`, `non_hispanic_black_african_american`, `non_hispanic_american_indian_alaska_native`, `non_hispanic_asian_pacific_islander`, `nh_nhopi`, `non_hispanic_more_than_one_race`, `hispanic_latino_total`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date |  |
| `start_week` | Start Date | calendar_date |  |
| `end_week` | End Date | calendar_date |  |
| `year` | Year | text | Year in which death occurred. |
| `month` | Month | number | Month in which death occurred. |
| `group` | Group | text | Group |
| `state` | State | text |  |
| `indicator` | Indicator | text |  |
| `non_hispanic_white` | Non-Hispanic White | number |  |
| `non_hispanic_black_african_american` | Non-Hispanic Black or African American | number |  |
| `non_hispanic_american_indian_alaska_native` | Non-Hispanic American Indian or Alaska Native | number |  |
| `non_hispanic_asian_pacific_islander` | Non-Hispanic Asian | number |  |
| `nh_nhopi` | Non-Hispanic Native Hawaiian or Other Pacific Islander | number |  |
| `non_hispanic_more_than_one_race` | Non Hispanic more than one race | number | Non-Hispanic more than one race |
| `hispanic_latino_total` | Hispanic or Latino | number |  |
| `footnote` | Footnote | text |  |

### nr4s-juj3

**Provisional COVID-19 Deaths: Focus on Ages 0-18 Years** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/nr4s-juj3.json`
- Metadata: `GET https://data.cdc.gov/api/views/nr4s-juj3.json`; page: https://data.cdc.gov/d/nr4s-juj3
- Topics: Category: National Center for Health Statistics
- Tags: `mortality`, `children`, `nchs`, `nvss`, `provisional`, `covid-19`, `coronavirus`, `race`, `age group`, `sex`, `united states`, `hispanic origin`, `deaths`, `age`
- Rows: 29. Data updated: 2023-06-28. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective June 28, 2023, this dataset will no longer be updated. Similar data are accessible from CDC WONDER (https://wonder.cdc.gov/mcd-icd10-provisional.html). Deaths involving coronavirus disease 2019 (COVID-19) with a focus on ages 0-18 years in the United States.
- Sample row fields ($limit=1): `data_as_of`, `age_group`, `covid_19_deaths`, `indicator`, `sex`, `race_group`, `start_week`, `end_week`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | text |  |
| `age_group` | Age group | text |  |
| `covid_19_deaths` | COVID-19 Deaths | number |  |
| `indicator` | Indicator | text |  |
| `sex` | Sex | text |  |
| `race_group` | Race or Hispanic Origin Group | text |  |
| `start_week` | Start Week | text |  |
| `end_week` | End Week | text |  |

### hc4f-j6nb

**Provisional Death Counts for Coronavirus Disease (COVID-19)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/hc4f-j6nb.json`
- Metadata: `GET https://data.cdc.gov/api/views/hc4f-j6nb.json`; page: https://data.cdc.gov/d/hc4f-j6nb
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `mortality`, `united states`, `state`, `covid-19`, `coronavirus`, `nchs`, `age`, `pneumonia`, `provisional`, `puerto rico`, `weekly`, `age group`, `all causes`, `influenza`
- Rows: 93. Data updated: 2020-04-30. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: This dataset is no longer updated. Please see the following datasets for recent data: Provisional COVID-19 Deaths by Week (https://data.cdc.gov/dataset/Provisional-COVID-19-Death-Counts-by-Week-Ending-D/r8kw-7aab/) Provisional COVID-19 Deaths by Sex, Age, and State (https://data.cdc.gov/NCHS/Provisional-COVID-19-Death-Counts-by-Sex-Age-and-S/9bhg-hcku)
- Sample row fields ($limit=1): `data_as_of`, `group`, `state`, `indicator`, `start_week`, `end_week`, `covid_deaths`, `total_deaths`, `percent_expected_deaths`, `pneumonia_deaths`, `pneumonia_and_covid_deaths`, `all_influenza_deaths_j09_j11`, `pneumonia_influenza_and_covid_19_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date |  |
| `group` | Group | text |  |
| `state` | State | text |  |
| `indicator` | Indicator | text |  |
| `start_week` | Start week | calendar_date |  |
| `end_week` | End week | calendar_date |  |
| `covid_deaths` | All COVID-19 Deaths (U07.1) | number |  |
| `total_deaths` | Deaths from All Causes | number |  |
| `percent_expected_deaths` | Percent of Expected Deaths | number |  |
| `pneumonia_deaths` | All Pneumonia Deaths (J12.0-J18.9) | number |  |
| `pneumonia_and_covid_deaths` | Deaths with Pneumonia and COVID-19 (J12.0-J18.9 and U07.1) | number |  |
| `all_influenza_deaths_j09_j11` | All Influenza Deaths (J09-J11) | number |  |
| `pneumonia_influenza_and_covid_19_deaths` | Pneumonia, Influenza, and COVID-19 Deaths | number |  |
| `footnote` | Footnote | text |  |

### ynw2-4viq

**Provisional Death Counts for Influenza, Pneumonia, and COVID-19** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ynw2-4viq.json`
- Metadata: `GET https://data.cdc.gov/api/views/ynw2-4viq.json`; page: https://data.cdc.gov/d/ynw2-4viq
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `state`, `weekly`, `age group`, `age`, `covid-19`, `coronavirus`, `pneumonia`, `influenza`, `all causes`, `hhs region`
- Rows: 50,400. Data updated: 2023-11-02. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Deaths counts for influenza, pneumonia, and COVID-19 reported to NCHS by week ending date, by state and HHS region, and age group.
- Sample row fields ($limit=1): `data_as_of`, `start_week`, `end_week`, `mmwryear`, `mmwrweek`, `week_ending_date`, `group`, `indicator`, `jurisdiction`, `age_group`, `covid_19_deaths`, `total_deaths`, `pneumonia_deaths`, `influenza_deaths`, `pneumonia_or_influenza`, `pneumonia_influenza_or_covid`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | text | Date of analysis |
| `start_week` | Start Week | text | First date of data period |
| `end_week` | End Week | text | Last date of data period |
| `mmwryear` | MMWRyear | text | MMWR year |
| `mmwrweek` | MMWRweek | number | MMWR week number |
| `week_ending_date` | Week Ending Date | calendar_date | Week-ending date for the week of reporting |
| `group` | Group | text | Group |
| `indicator` | Indicator | text | Indicator |
| `jurisdiction` | Jurisdiction | text | Jurisdiction of Residence |
| `age_group` | Age Group | text | Age group |
| `covid_19_deaths` | COVID-19 Deaths | number | Deaths involving COVID-19 (ICD-code U07.1) |
| `total_deaths` | Total Deaths | number | Deaths from all causes |
| `pneumonia_deaths` | Pneumonia Deaths | number | Pneumonia Deaths (ICD-10 codes J12.0-J18.9) |
| `influenza_deaths` | Influenza Deaths | number | Influenza Deaths (ICD-10 codes J09-J11) |
| `pneumonia_or_influenza` | Pneumonia or Influenza | number | Deaths with Pneumonia or Influenza |
| `pneumonia_influenza_or_covid` | Pneumonia, Influenza, or COVID-19 Deaths | number | Pneumonia, Influenza, or COVID-19 Deaths (ICD-10 codes J12.0-J18.9, J09-J11, U07.1) |
| `footnote` | Footnote | text | Suppressed counts (1-9) |

### 8hzs-zshh

**Provisional drug overdose death counts for specific drugs** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8hzs-zshh.json`
- Metadata: `GET https://data.cdc.gov/api/views/8hzs-zshh.json`; page: https://data.cdc.gov/d/8hzs-zshh
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `vsrr`, `provisional`, `deaths`, `mortality`, `drug overdose`, `united states`, `hhs region`
- Rows: 11,088. Data updated: 2026-07-15. Probe status: 200.
- Update frequency: R/P6M.
- Source: National Center for Health Statistics
- Description: This data presents counts of provisional drug overdose deaths by selected drugs and U.S. Department of Health and Human Services (HHS) public health regions, based on provisional mortality data from the National Vital Statistics System. This data is limited to drug overdose deaths with an underlying cause of death assigned to International Statistical Classification of Diseases, 10th Revision (ICD-10) code numbers X40-X44 (unintentional), X60-X64 (suicide), X85 (homicide), or Y10-Y14 (undetermined intent). Specific drugs were identified using methods for searching literal text from death cert…
- Sample row fields ($limit=1): `data_as_of`, `death_year`, `death_month`, `jurisdiction_occurrence`, `drug_involved`, `time_period`, `month_ending_date`, `drug_overdose_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | data_as_of | calendar_date | Date of analysis |
| `death_year` | death_year | text | 12 month-ending year |
| `death_month` | death_month | text | 12 month-ending month |
| `jurisdiction_occurrence` | jurisdiction_occurrence | text | Jurisdiction of occurrence |
| `drug_involved` | drug_involved | text | Name of drug |
| `time_period` | time_period | text | Time period of reporting |
| `month_ending_date` | month_ending_date | calendar_date | 12 month-ending date |
| `drug_overdose_deaths` | drug_overdose_deaths | number | Number of deaths during 12 month-ending period |
| `footnote` | footnote | text | Suppressed counts (1-9) |

### dtm2-meqi

**Provisional Drug Overdose Deaths by Urban/Rural Classification Scheme for 12 month-ending December 2018-December 2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/dtm2-meqi.json`
- Metadata: `GET https://data.cdc.gov/api/views/dtm2-meqi.json`; page: https://data.cdc.gov/d/dtm2-meqi
- Topics: Category: National Center for Health Statistics
- Tags: `provisional`, `mortality`, `deaths`, `nchs`, `nvss`, `united states`, `monthly`, `drug overdose`, `all causes`, `urbanicity`, `sdoh-environmental`
- Rows: 150. Data updated: 2021-08-10. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: National provisional drug overdose deaths by month and 2013 NCHS Urban–Rural Classification Scheme for Counties. Drug overdose deaths are identified using underlying cause-of-death codes from the Tenth Revision of ICD (ICD–10): X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), and Y10–Y14 (undetermined). Deaths are based on the county of residence in the United States. Death counts provided are for “12-month ending periods,” defined as the number of deaths occurring in the 12-month period ending in the month indicated. Estimates for 2020 are based on provisional data. Estimates for…
- Sample row fields ($limit=1): `data_as_of`, `jurisdiction_of_occurrence`, `urban_rural_classification`, `year`, `month`, `time_period`, `total_deaths`, `drug_overdose_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text |  |
| `urban_rural_classification` | Urban-Rural Classification | text | 2013 NCHS Urban–Rural Classification Scheme for Counties |
| `year` | Year | text | Year of reporting |
| `month` | Month | number | Month of reporting |
| `time_period` | Time Period | text | Time period of reporting |
| `total_deaths` | Total Deaths | number | Deaths from all causes of death |
| `drug_overdose_deaths` | Drug Overdose Deaths | number | Drug overdose deaths (ICD-10 codes X40–X44, X60–X64, X85, and Y10–Y14) |

### 4bc2-bbpq

**Provisional Percent of Deaths for COVID-19, Influenza, and RSV** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/4bc2-bbpq.json`
- Metadata: `GET https://data.cdc.gov/api/views/4bc2-bbpq.json`; page: https://data.cdc.gov/d/4bc2-bbpq
- Topics: Category: National Center for Health Statistics
- Tags: `respiratory-virus-response`, `mortality`, `nchs`, `nvss`, `deaths`, `united states`, `coronavirus`, `covid19`, `weekly`, `influenza`, `rsv`
- Rows: 144. Data updated: 2026-11-06. Probe status: 200.
- Update frequency: R/P1W .
- Description: This file contains the provisional percent of total deaths by week for COVID-19, Influenza, and Respiratory Syncytial Virus for deaths occurring among residents in the United States. Provisional data are based on non-final counts of deaths based on the flow of mortality data in National Vital Statistics System.
- Sample row fields ($limit=1): `week_end`, `pathogen`, `percent_deaths`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_end` | week_end | calendar_date | Weekending Date |
| `pathogen` | pathogen | text | Pathogen |
| `percent_deaths` | percent_deaths | number | Percent of total deaths for pathogen for current week |

### 53g5-jf7x

**Provisional Percent of Deaths for COVID-19, Influenza, and RSV by Select Characteristics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/53g5-jf7x.json`
- Metadata: `GET https://data.cdc.gov/api/views/53g5-jf7x.json`; page: https://data.cdc.gov/d/53g5-jf7x
- Topics: Category: National Center for Health Statistics
- Tags: `respiratory-virus-response`, `mortality`, `nchs`, `deaths`, `united-states`, `coronavirus`, `covid-19`, `weekly`, `influenza`, `rsv`
- Rows: 22,080. Data updated: 2026-11-06. Probe status: 200.
- Update frequency: R/P1W.
- Description: This file contains the provisional percent of total deaths by week for COVID-19, Influenza, and Respiratory Syncytial Virus for deaths occurring among residents in the United States, by sex, age group, and race and Hispanic origin. Provisional data are based on non-final counts of deaths based on the flow of mortality data in National Vital Statistics System.
- Sample row fields ($limit=1): `data_as_of`, `start_date`, `end_date`, `group`, `year`, `month`, `mmwr_week`, `weekending_date`, `state`, `demographic_type`, `demographic_values`, `pathogen`, `total_deaths`, `suppressed`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | data_as_of | calendar_date | Data as of |
| `start_date` | start_date | calendar_date | First date of data period |
| `end_date` | end_date | calendar_date | Last date of data period |
| `group` | group | text | Time period of reporting |
| `year` | year | number | Year of reporting |
| `month` | month | number | Month of reporting |
| `mmwr_week` | mmwr_week | number | MMWR week of reporting |
| `weekending_date` | weekending_date | calendar_date | Week-ending date for the week of reporting |
| `state` | state | text | Jurisdiction of residence. |
| `demographic_type` | demographic_type | text | Demographic characteristic [Age, Race/Ethnicity, Sex] |
| `demographic_values` | demographic_values | text | Demographic subgroup |
| `pathogen` | pathogen | text | Cause of death (pathogen) [COVID-19, Flu, RSV, Combined] |
| `deaths` | deaths | number | Number of deaths involving pathogen, null if value is suppressed for privacy protection. |
| `total_deaths` | total_deaths | number | Deaths from all causes of death |
| `percent_deaths` | percent_deaths | number | Percent of deaths due to pathogen, null if value is suppressed for privacy protection. |
| `provisional` | provisional | text | Is this data provisional |
| `suppressed` | suppressed | text | Values based death counts between 1-9 are suppressed. If this field is not null, then the “deaths” and “percent_deaths” fields are suppressed for privacy protection. |

### th9n-ghnr

**Reduced Access to Care During COVID-19** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/th9n-ghnr.json`
- Metadata: `GET https://data.cdc.gov/api/views/th9n-ghnr.json`; page: https://data.cdc.gov/d/th9n-ghnr
- Topics: Category: National Center for Health Statistics
- Tags: `covid-19`, `rands`, `sdoh-high-school`, `sdoh-higher-education`, `sdoh-access-to-health-care`, `sdoh-use-of-health-care`
- Rows: 1,710. Data updated: 2021-08-06. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DRM
- Description: The Research and Development Survey (RANDS) is a platform designed for conducting survey question evaluation and statistical research. RANDS is an ongoing series of surveys from probability-sampled commercial survey panels used for methodological research at the National Center for Health Statistics (NCHS). RANDS estimates are generated using an experimental approach that differs from the survey design approaches generally used by NCHS, including possible biases from different response patterns and sampling frames as well as increased variability from lower sample sizes. Use of the RANDS plat…
- Sample row fields ($limit=1): `round`, `indicator`, `group`, `subgroup`, `sample_size`, `response`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `round` | Round | number | Data collection period; Round 1 occurred June 9, 2020–July 6, 2020, Round 2 occurred August 3, 2020–August 20, 2020, and Round 3 occurred May 17, 2021–June 30, 2021 |
| `indicator` | Indicator | text | Indicators include reduced access to 1) one or more types of care, 2) urgent care, 3) surgical procedure, 4) diagnostic or medical screening test, 5) treatment for ongoing condition, 6) regular checkup, 7) prescription drugs or medications… |
| `group` | Group | text | Estimates were reported at the national level (total) and by age group, race and Hispanic origin, sex, education level, urbanization, and selected chronic conditions. |
| `subgroup` | Subgroup | text | Subcategories for each group |
| `sample_size` | Sample Size | number | Sample size |
| `response` | Response | text | Survey question response for each indicator |
| `percent` | Percent | number | Percent estimate |
| `standard_error` | Standard Error | number | Standard error estimate |
| `suppression` | Suppression | text | Identifies percent and standard error estimates that did not meet NCHS Data Presentation Standards for Proportions. |
| `significant_1` | Significant 1 | number | Indicator for significance testing of difference from Round 1 where a value of 0 indicates the estimates are not statistically significantly different at the 5% significance level and a value of 1 indicates that the estimates are statistic… |
| `significant_2` | Significant 2 | number | Indicator for significance testing of difference from Round 2 where a value of 0 indicates the estimates are not statistically significantly different at the 5% significance level and a value of 1 indicates that the estimates are statistic… |

### h7xa-837u

**Telemedicine Use in the Last 4 Weeks** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/h7xa-837u.json`
- Metadata: `GET https://data.cdc.gov/api/views/h7xa-837u.json`; page: https://data.cdc.gov/d/h7xa-837u
- Topics: Category: National Center for Health Statistics
- Tags: `telemedicine`, `covid-19`, `sdoh-use-of-health-care`
- Rows: 3,344. Data updated: 2022-11-28. Probe status: 200.
- Update frequency: R/P2W.
- Source: NCHS/DHIS
- Description: To rapidly monitor recent changes in the use of telemedicine, the National Center for Health Statistics (NCHS) and the Health Resources and Services Administration’s Maternal and Child Health Bureau (HRSA MCHB) partnered with the Census Bureau on an experimental data system called the Household Pulse Survey. This 20-minute online survey was designed to complement the ability of the federal statistical system to rapidly respond and provide relevant information about the impact of the coronavirus pandemic in the U.S. The U.S. Census Bureau, in collaboration with five federal agencies, launched…
- Sample row fields ($limit=1): `indicator`, `group`, `state`, `subgroup`, `phase`, `time_period`, `time_period_label`, `time_period_start_date`, `time_period_end_date`, `value`, `low_ci`, `high_ci`, `confidence_interval`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | Indicator | text |  |
| `group` | Group | text |  |
| `state` | State | text |  |
| `subgroup` | Subgroup | text |  |
| `phase` | Phase | number |  |
| `time_period` | Time Period | number |  |
| `time_period_label` | Time Period Label | text |  |
| `time_period_start_date` | Time Period Start Date | calendar_date |  |
| `time_period_end_date` | Time Period End Date | calendar_date |  |
| `value` | Value | number |  |
| `low_ci` | Low CI | number |  |
| `high_ci` | High CI | number |  |
| `confidence_interval` | Confidence Interval | text |  |
| `quartile_range` | Quartile Range | text |  |
| `suppression_flag` | Suppression Flag | text |  |

### 5h56-n989

**U.S. Life Expectancy at Birth by State and Census Tract - 2010-2015** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/5h56-n989.json`
- Metadata: `GET https://data.cdc.gov/api/views/5h56-n989.json`; page: https://data.cdc.gov/d/5h56-n989
- Topics: Category: National Center for Health Statistics
- Tags: `life expectancy`, `birth`, `census tract`, `united states`, `nchs`, `nvss`, `state`, `county`
- Rows: 73,121. Data updated: 2020-03-09. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: This dataset includes estimates of U.S. life expectancy at birth by state and census tract for the period 2010-2015 (1). Estimates were produced for 65,662 census tracts, covering the District of Columbia (D.C.) and all states, excluding Maine and Wisconsin, representing 88.7% of all U.S. census tracts (see notes). These estimates are the result of the collaborative project, “U.S. Small-area Life Expectancy Estimates Project (USALEEP),” between the National Center for Health Statistics (NCHS), the National Association for Public Health Statistics and Information Systems (NAPHSIS), and the Rob…
- Sample row fields ($limit=1): `state_name`, `county_name`, `le`, `le_range`, `se_le`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `state_name` | State | text |  |
| `county_name` | County | text |  |
| `full_ct_num` | Census Tract Number | text |  |
| `le` | Life Expectancy | number |  |
| `le_range` | Life Expectancy Range | text |  |
| `se_le` | Life Expectancy Standard Error | number |  |

### a5a8-jsrq

**U.S. State Life Expectancy by Sex, 2018** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/a5a8-jsrq.json`
- Metadata: `GET https://data.cdc.gov/api/views/a5a8-jsrq.json`; page: https://data.cdc.gov/d/a5a8-jsrq
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `united states`, `state`, `life expectancy`, `nvss`, `mortality`, `deaths`, `sex`
- Rows: 156. Data updated: 2022-02-03. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: The dataset presents life expectancy at birth estimates based on annual complete period life tables for each of the 50 states and the District of Columbia (D.C.) in 2018 for the total, male and female populations.
- Sample row fields ($limit=1): `state`, `sex`, `leb`, `quartile`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `state` | State | text | Jurisdiction of residence |
| `sex` | Sex | text | Sex |
| `leb` | LEB | number | Life expectancy at birth |
| `se` | SE | number | Life expectancy Standard Error |
| `quartile` | Quartile | text | Life Expectancy Range |

### ncvk-7amm

**U.S. State Life Expectancy by Sex, 2019** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ncvk-7amm.json`
- Metadata: `GET https://data.cdc.gov/api/views/ncvk-7amm.json`; page: https://data.cdc.gov/d/ncvk-7amm
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `united states`, `state`, `life expectancy`, `nvss`, `mortality`, `deaths`, `sex`
- Rows: 156. Data updated: 2022-02-03. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: The dataset presents life expectancy at birth estimates based on annual complete period life tables for each of the 50 states and the District of Columbia (D.C.) in 2019 for the total, male and female populations.
- Sample row fields ($limit=1): `state`, `sex`, `leb`, `se`, `quartile`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `state` | State | text | Jurisdiction of residence |
| `sex` | Sex | text | Sex |
| `leb` | LEB | number | Life expectancy at birth |
| `se` | SE | number | Life expectancy Standard Error |
| `quartile` | Quartile | text | Life Expectancy Range |

### ss2j-8ajj

**U.S. State Life Expectancy by Sex, 2020** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ss2j-8ajj.json`
- Metadata: `GET https://data.cdc.gov/api/views/ss2j-8ajj.json`; page: https://data.cdc.gov/d/ss2j-8ajj
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `united states`, `state`, `life expectancy`, `nvss`, `mortality`, `deaths`, `sex`
- Rows: 156. Data updated: 2022-09-01. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: The dataset presents life expectancy at birth estimates based on annual complete period life tables for each of the 50 states and the District of Columbia (D.C.) in 2020 for the total, male and female populations.
- Sample row fields ($limit=1): `state`, `sex`, `le`, `se`, `quartile`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `state` | State | text |  |
| `sex` | Sex | text |  |
| `le` | LE | number |  |
| `se` | SE | number |  |
| `quartile` | Quartile | text |  |

### it4f-frdc

**U.S. State Life Expectancy by Sex, 2021** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/it4f-frdc.json`
- Metadata: `GET https://data.cdc.gov/api/views/it4f-frdc.json`; page: https://data.cdc.gov/d/it4f-frdc
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `united states`, `state`, `life expectancy`, `nvss`, `mortality`, `deaths`, `sex`
- Rows: 153. Data updated: 2024-09-11. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: The dataset presents life expectancy at birth estimates based on annual complete period life tables for each of the 50 states and the District of Columbia (D.C.) in 2021 for the total, male and female populations.
- Sample row fields ($limit=1): `area`, `sex`, `leb`, `se`, `quartile`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `area` | State | text |  |
| `sex` | Sex | text |  |
| `leb` | LE | number |  |
| `se` | SE | number |  |
| `quartile` | Quartile | text |  |

### xt86-xqxz

**Visits to physician offices, hospital outpatient departments, and hospital emergency departments, by age, sex, and race: United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/xt86-xqxz.json`
- Metadata: `GET https://data.cdc.gov/api/views/xt86-xqxz.json`; page: https://data.cdc.gov/d/xt86-xqxz
- Topics: Category: National Center for Health Statistics
- Tags: `african americans`, `emergency service`, `hospital`, `hospitals`, `outpatients`, `physicians`, `physicians' offices`, `sex`, `european continental ancestry group`, `continental population groups`, `age`, `disasters`, `health us`, `sdoh-use-of-health-care`
- Rows: 3,570. Data updated: 2021-06-03. Probe status: 200.
- Source: NCHS/DAE
- Description: Data on visits to physician offices, hospital outpatient departments and hospital emergency departments by selected population characteristics. Please refer to the PDF or Excel version of this table in the HUS 2019 Data Finder (https://www.cdc.gov/nchs/hus/contents2019.htm) for critical information about measures, definitions, and changes over time. Note that the data file available here has more recent years of data than what is shown in the PDF or Excel version. Data for 2017 physician office visits are not available. SOURCE: NCHS, National Ambulatory Medical Care Survey and National Hospit…
- Sample row fields ($limit=1): `indicator`, `panel`, `panel_num`, `unit`, `unit_num`, `stub_name`, `stub_name_num`, `stub_label`, `stub_label_num`, `year`, `year_num`, `age`, `age_num`, `estimate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `indicator` | INDICATOR | text | Measure being estimated. |
| `panel` | PANEL | text | Submeasures of INDICATOR. Datasets may have multiple panels. |
| `panel_num` | PANEL_NUM | number | Numeric code for levels of PANEL that may be used for easier coding or formatting of the PANEL variable. |
| `unit` | UNIT | text | Unit of measurement of the estimate. |
| `unit_num` | UNIT_NUM | number | Numeric code for levels of UNIT that may be used for easier coding or formatting of the UNIT variable. |
| `stub_name` | STUB_NAME | text | Description of the population category pertaining to the estimate. |
| `stub_name_num` | STUB_NAME_NUM | number | Numeric code for levels of STUB_NAME that may be used for easier coding or formatting of the STUB_NAME variable. |
| `stub_label` | STUB_LABEL | text | Specific population subgroup pertaining to the estimate. |
| `stub_label_num` | STUB_LABEL_NUM | number | Numeric code for levels of STUB_LABEL that may be used for easier coding or formatting of the STUB_LABEL variable. |
| `year` | YEAR | text | Data year or range of data years pertaining to the estimate. |
| `year_num` | YEAR_NUM | number | Numeric code for levels of YEAR that may be used for easier coding or formatting of the YEAR variable. |
| `age` | AGE | text | Age group pertaining to the estimate. |
| `age_num` | AGE_NUM | number | Numeric code for levels of AGE that may be used for easier coding or formatting of the AGE variable. |
| `estimate` | ESTIMATE | number | Calculated estimate of the measure. |
| `se` | SE | number | Calculated standard error of the estimate. |
| `flag` | FLAG | text | Additional information pertaining to the estimate. See the footnotes in the source table (Excel) for more information. |

### hmz2-vwda

**VSRR - State and National Provisional Counts for Live Births, Deaths, and Infant Deaths** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/hmz2-vwda.json`
- Metadata: `GET https://data.cdc.gov/api/views/hmz2-vwda.json`; page: https://data.cdc.gov/d/hmz2-vwda
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `united states`, `puerto rico`, `vsrr`, `nvss`, `nchs`, `provisional`, `mortality`, `state`, `monthly`, `birth`
- Rows: 1,980. Data updated: 2024-12-11. Probe status: 200.
- Update frequency: R/P3M.
- Source: NCHS/DVS
- Description: NOTES: Figures include all revisions received from the states and, therefore, may differ from those previously published. Data are provisional and are subject to monthly reporting variation. National data are calculated by summing the number of events reported by state of residence; counts are rounded to the nearest thousand (births and deaths) or hundred (infant deaths). Provisional counts may differ by approximately 2% from final counts, due to rounding and reporting variation. Additionally, the accuracy of the provisional counts may change over time. Data are estimates by state of residenc…
- Sample row fields ($limit=1): `state`, `year`, `month`, `period`, `indicator`, `data_value`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `state` | State | text |  |
| `year` | Year | text |  |
| `month` | Month | text |  |
| `period` | Period | text |  |
| `indicator` | Indicator | text |  |
| `data_value` | Data Value | number |  |

### gb4e-yj24

**VSRR Provisional County-Level Drug Overdose Death Counts** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/gb4e-yj24.json`
- Metadata: `GET https://data.cdc.gov/api/views/gb4e-yj24.json`; page: https://data.cdc.gov/d/gb4e-yj24
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `vsrr`, `deaths`, `mortality`, `provisional`, `united states`, `county`, `drug overdose`, `monthly`, `drug`, `sdoh-environmental`
- Rows: 235,800. Data updated: 2026-10-14. Probe status: 200.
- Source: NCHS/DVS
- Description: This data visualization presents county-level provisional counts for drug overdose deaths based on a current flow of mortality data in the National Vital Statistics System. County-level provisional counts include deaths occurring within the 50 states and the District of Columbia, as of the date specified and may not include all deaths that occurred during a given time period. Provisional counts are often incomplete and causes of death may be pending investigation resulting in an underestimate relative to final counts (see Technical Notes). The provisional data presented on the dashboard below…
- Sample row fields ($limit=1): `data_as_of`, `year`, `month`, `st_abbrev`, `state_name`, `countyname`, `fips`, `statefips`, `countyfips`, `code2013`, `footnote`, `percentage_of_records_pending`, `monthendingdate`, `start_date`, `end_date`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data as of | calendar_date | Analysis Date |
| `year` | Year | text | Year of death |
| `month` | Month | number | Month of death |
| `st_abbrev` | ST_ABBREV | text | State of residence abbreviation |
| `state_name` | STATE_NAME | text | State of residence |
| `countyname` | COUNTYNAME | text | County of residence |
| `fips` | FIPS | text | FIPS state and county code |
| `statefips` | STATEFIPS | text | FIPS state code |
| `countyfips` | COUNTYFIPS | text | FIPS county code |
| `code2013` | CODE2013 | number | Urban-rural classification is based on the 2013 National Center for Health Statistics Urban-Rural Classification Scheme for Counties |
| `provisional_drug_overdose` | Provisional Drug Overdose Deaths | number | Count of provisional drug overdose deaths |
| `footnote` | Footnote | text | Suppressed counts (1-9) |
| `percentage_of_records_pending` | Percentage Of Records Pending Investigation | number | Percentage Of Records Pending Investigation |
| `historicaldatacompletenessnote` | HistoricalDataCompletenessNote | text | Note on 2019 county completeness |
| `monthendingdate` | MonthEndingDate | calendar_date | 12 month-ending date |
| `start_date` | Start Date | calendar_date | First month-ending date of reporting period |
| `end_date` | End Date | calendar_date | Last month-ending date of reporting period |

### xkb8-kh2a

**VSRR Provisional Drug Overdose Death Counts** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/xkb8-kh2a.json`
- Metadata: `GET https://data.cdc.gov/api/views/xkb8-kh2a.json`; page: https://data.cdc.gov/d/xkb8-kh2a
- Topics: Category: National Center for Health Statistics
- Tags: `deaths`, `drug`, `drug overdose`, `mortality`, `united states`, `nchs`, `state`, `heroin`, `cocaine`, `methadone`, `opiate`, `opioid`, `psychostimulants`, `nvss`, `vsrr`, `monthly`, `provisional`
- Rows: 87,543. Data updated: 2026-10-14. Probe status: 200.
- Update frequency: R/P1M.
- Source: National Center for Health Statistics
- Description: This data presents provisional counts for drug overdose deaths based on a current flow of mortality data in the National Vital Statistics System. Counts for the most recent final annual data are provided for comparison. National provisional counts include deaths occurring within the 50 states and the District of Columbia as of the date specified and may not include all deaths that occurred during a given time period. Provisional counts are often incomplete and causes of death may be pending investigation resulting in an underestimate relative to final counts. To address this, methods were dev…
- Sample row fields ($limit=1): `state`, `year`, `month`, `period`, `indicator`, `percent_complete`, `percent_pending_investigation`, `state_name`, `footnote`, `footnote_symbol`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `state` | State | text |  |
| `year` | Year | number |  |
| `month` | Month | text |  |
| `period` | Period | text |  |
| `indicator` | Indicator | text |  |
| `data_value` | Data Value | number |  |
| `percent_complete` | Percent Complete | text |  |
| `percent_pending_investigation` | Percent Pending Investigation | number |  |
| `state_name` | State Name | text |  |
| `footnote` | Footnote | text |  |
| `footnote_symbol` | Footnote Symbol | text |  |
| `predicted_value` | Predicted Value | number |  |

### e2d5-ggg7

**VSRR Provisional Maternal Death Counts and Rates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/e2d5-ggg7.json`
- Metadata: `GET https://data.cdc.gov/api/views/e2d5-ggg7.json`; page: https://data.cdc.gov/d/e2d5-ggg7
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `deaths`, `mortality`, `united states`, `age`, `age group`, `race`, `hispanic origin`, `maternal causes`, `death rates`
- Rows: 870. Data updated: 2026-07-16. Probe status: 200.
- Update frequency: R/P3M.
- Source: National Center for Health Statistics
- Description: This data presents national-level provisional maternal mortality rates based on a current flow of mortality and natality data in the National Vital Statistics System. Provisional rates which are an early estimate of the number of maternal deaths per 100,000 live births, are shown as of the date specified and may not include all deaths and births that occurred during a given time period (see Technical Notes). A maternal death is the death of a woman while pregnant or within 42 days of termination of pregnancy irrespective of the duration and the site of the pregnancy, from any cause related to…
- Sample row fields ($limit=1): `data_as_of`, `jurisdiction`, `group`, `subgroup`, `year_of_death`, `month_of_death`, `time_period`, `month_ending_date`, `maternal_deaths`, `live_births`, `maternal_mortality_rate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `jurisdiction` | Jurisdiction | text | Jurisdiction of occurrence |
| `group` | Group | text | Demographic group 1 |
| `subgroup` | Subgroup | text | Demographic group 2 |
| `year_of_death` | Year of Death | text | 12-month ending year |
| `month_of_death` | Month of Death | number | 12-month ending month |
| `time_period` | Time Period | text | Time period of reporting |
| `month_ending_date` | Month Ending Date | calendar_date | 12-month ending date |
| `maternal_deaths` | Maternal Deaths | number | Deaths from maternal causes (ICD-10 codes A34, O00–O95, and O98–O99) |
| `live_births` | Live Births | number | Number of live births during 12 month-ending period |
| `maternal_mortality_rate` | Maternal Mortality Rate | number | Maternal mortality rate during 12 month-ending period |
| `footnote` | Footnote | text | Suppressed counts (1-9) |

### u6jv-9ijr

**Weekly Counts of Death by Jurisdiction and Select Causes of Death** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/u6jv-9ijr.json`
- Metadata: `GET https://data.cdc.gov/api/views/u6jv-9ijr.json`; page: https://data.cdc.gov/d/u6jv-9ijr
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `mortality`, `deaths`, `united states`, `state`, `puerto rico`, `weekly`, `causes of death`, `alzheimer disease`, `dementia`, `cancer`, `cerebrovascular disease`, `diabetes`, `chronic lower respiratory disease`, `influenza`, `pneumonia`, `respiratory disease`, `renal failure`, `heart failure`, `hypertensive disease`, `ischemic heart disease`, `circulatory disease`, `septicemia`
- Rows: 481,140. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: National Center for Health Statistics
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. This visualization provides weekly data on the number of deaths by jurisdiction of occurrence and cause of death. Counts of deaths in more recent weeks can be compared with counts from earlier years to determine if the number is higher than expected. Selected causes of death are shown, based on analyses of the most prevalent comorbid conditions reported on death certificates where COVID-19 was listed as a cause of death (see https://www.cdc.gov/nchs/nvss/vsrr/covid_weekly/ind…
- Sample row fields ($limit=1): `jurisdiction`, `week_ending_date`, `state_abbreviation`, `mmwryear`, `mmwrweek`, `cause_group`, `number_of_deaths`, `cause_subgroup`, `time_period`, `average_number_of_deaths`, `type`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `jurisdiction` | Jurisdiction | text | Jurisdiction of occurrence |
| `week_ending_date` | Week Ending Date | calendar_date | Week ending date |
| `state_abbreviation` | State Abbreviation | text | State abbreviation |
| `mmwryear` | Year | number | Year |
| `mmwrweek` | Week | number | Week number |
| `cause_group` | Cause Group | text | Cause group |
| `number_of_deaths` | Number of Deaths | number | Number of deaths |
| `cause_subgroup` | Cause Subgroup | text | Cause Subgroup |
| `time_period` | Time Period | text | Time period |
| `suppress` | Suppress | text | Flag for data suppression |
| `note` | Note | text | Note about data |
| `average_number_of_deaths` | Average Number of Deaths in Time Period | number | Average number of deaths in a given time period and week number |
| `difference_from_2015_2019_to_2020` | Difference from 2015-2019 to 2020 | number | Difference in the number of deaths in 2020 relative to 2015-2019 |
| `percent_difference_from_15_19_to_20` | Percent Difference from 2015-2019 to 2020 | number | Percent difference in the number of deaths in 2020 relative to 2015-2019 |
| `type` | Type | text | Estimate type (predicted or observed) |

### y5bj-9g5w

**Weekly Counts of Deaths by Jurisdiction and Age** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/y5bj-9g5w.json`
- Metadata: `GET https://data.cdc.gov/api/views/y5bj-9g5w.json`; page: https://data.cdc.gov/d/y5bj-9g5w
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `deaths`, `mortality`, `united states`, `state`, `puerto rico`, `weekly`, `age group`, `age`, `all causes`
- Rows: 269,016. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. This visualization provides weekly data on the number of deaths from all causes by jurisdiction of occurrence and age group. Counts of deaths in more recent weeks can be compared with counts from earlier years to determine if the number is higher than expected.
- Sample row fields ($limit=1): `jurisdiction`, `week_ending_date`, `state_abbreviation`, `year`, `week`, `age_group`, `number_of_deaths`, `time_period`, `type`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `jurisdiction` | Jurisdiction | text | Jurisdiction of occurrence |
| `week_ending_date` | Week Ending Date | calendar_date | Week ending date |
| `state_abbreviation` | State Abbreviation | text | State abbreviation |
| `year` | Year | number | Year |
| `week` | Week | number | Week number |
| `age_group` | Age Group | text | Age group |
| `number_of_deaths` | Number of Deaths | number | Number of deaths |
| `time_period` | Time Period | text | Time period |
| `type` | Type | text | Estimate type (predicted or observed) |
| `suppress` | Suppress | text | Flag for data suppression |
| `note` | Note | text | Note about data |

### qfhf-uhaa

**Weekly Counts of Deaths by Jurisdiction, and Race and Hispanic Origin** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/qfhf-uhaa.json`
- Metadata: `GET https://data.cdc.gov/api/views/qfhf-uhaa.json`; page: https://data.cdc.gov/d/qfhf-uhaa
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `provisional`, `deaths`, `mortality`, `united states`, `state`, `puerto rico`, `weekly`, `race`, `hispanic origin`, `all causes`, `covid-19`, `coronavirus`
- Rows: 985,608. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. This visualization provides weekly data on the number of deaths from all causes by jurisdiction of occurrence and race and Hispanic origin. Numbers of deaths are also shown for all causes excluding COVID-19, and for COVID-19. Counts of deaths in more recent weeks can be compared with counts from earlier years to determine if the number is higher than expected.
- Sample row fields ($limit=1): `jurisdiction`, `week_ending_date`, `state_abbreviation`, `mmwryear`, `mmwrweek`, `race_ethnicity`, `time_period`, `suppress`, `outcome`, `type`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `jurisdiction` | Jurisdiction | text |  |
| `week_ending_date` | Week Ending Date | calendar_date |  |
| `state_abbreviation` | State Abbreviation | text |  |
| `mmwryear` | MMWRYear | number |  |
| `mmwrweek` | MMWRWeek | number |  |
| `race_ethnicity` | Race/Ethnicity | text |  |
| `time_period` | Time Period | text |  |
| `suppress` | Suppress | text |  |
| `note` | Note | text |  |
| `outcome` | Outcome | text |  |
| `number_of_deaths` | Number of Deaths | number |  |
| `average_number_of_deaths` | Average Number of Deaths in Time Period | number |  |
| `difference_from_2015_2019` | Difference from 2015-2019 to 2020 | number |  |
| `percent_difference_from_2015` | Percent Difference from 2015-2019 to 2020 | number |  |
| `type` | Type | text |  |

### 3yf8-kanr

**Weekly Counts of Deaths by State and Select Causes, 2014-2019** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3yf8-kanr.json`
- Metadata: `GET https://data.cdc.gov/api/views/3yf8-kanr.json`; page: https://data.cdc.gov/d/3yf8-kanr
- Topics: Category: National Center for Health Statistics
- Tags: `mortality`, `deaths`, `nchs`, `nvss`, `united states`, `state`, `puerto rico`, `weekly`, `all causes`, `causes of death`, `natural cause`, `septicemia`, `cancer`, `diabetes`, `alzheimer disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `respiratory disease`, `kidney disease`, `diseases of heart`, `cerebrovascular disease`
- Rows: 16,902. Data updated: 2021-01-21. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Final counts of deaths by the week the deaths occurred, by state of occurrence, and by select causes of death for 2014-2019. Death counts in this dataset were derived from the National Vital Statistics System database that provides the most timely access to the data. Therefore, counts may differ slightly from final data due to differences in processing, recoding, and imputation.
- Sample row fields ($limit=1): `jurisdiction_of_occurrence`, `mmwryear`, `mmwrweek`, `weekendingdate`, `allcause`, `naturalcause`, `septicemia_a40_a41`, `malignant_neoplasms_c00_c97`, `diabetes_mellitus_e10_e14`, `alzheimer_disease_g30`, `influenza_and_pneumonia_j10`, `chronic_lower_respiratory`, `other_diseases_of_respiratory`, `nephritis_nephrotic_syndrome`, `symptoms_signs_and_abnormal`, `diseases_of_heart_i00_i09`, `cerebrovascular_diseases`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text | Jurisdiction of Occurrence |
| `mmwryear` | MMWR Year | text | MMWR Year |
| `mmwrweek` | MMWR Week | text | MMWR Week |
| `weekendingdate` | Week Ending Date | calendar_date | Week Ending Date |
| `allcause` | All Cause | number | All Cause |
| `naturalcause` | Natural Cause | number | Natural Cause (A00-R99) |
| `septicemia_a40_a41` | Septicemia (A40-A41) | number | Septicemia (A40-A41) |
| `malignant_neoplasms_c00_c97` | Malignant neoplasms (C00-C97) | number | Malignant neoplasms (C00-C97) |
| `diabetes_mellitus_e10_e14` | Diabetes mellitus (E10-E14) | number | Diabetes mellitus (E10-E14) |
| `alzheimer_disease_g30` | Alzheimer disease (G30) | number | Alzheimer disease (G30) |
| `influenza_and_pneumonia_j10` | Influenza and pneumonia (J10-J18) | number | Influenza and pneumonia (J10-J18) |
| `chronic_lower_respiratory` | Chronic lower respiratory diseases (J40-J47) | number | Chronic lower respiratory diseases (J40-J47) |
| `other_diseases_of_respiratory` | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) | number | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) |
| `nephritis_nephrotic_syndrome` | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) | number | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) |
| `symptoms_signs_and_abnormal` | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) | number | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) |
| `diseases_of_heart_i00_i09` | Diseases of heart (I00-I09,I11,I13,I20-I51) | number | Diseases of heart (I00-I09,I11,I13,I20-I51) |
| `cerebrovascular_diseases` | Cerebrovascular diseases (I60-I69) | number | Cerebrovascular diseases (I60-I69) |
| `flag_allcause` | flag_allcause | text | Suppressed (counts 1-9) for All causes of death |
| `flag_natcause` | flag_natcause | text | Suppressed (counts 1-9) for Natural causes of death |
| `flag_sept` | flag_sept | text | Suppressed (counts 1-9) for Septicemia |
| `flag_neopl` | flag_neopl | text | Suppressed (counts 1-9) for Malignant eoplasms |
| `flag_diab` | flag_diab | text | Suppressed (counts 1-9) for Diabetes mellitis |
| `flag_alz` | flag_alz | text | Suppressed (counts 1-9) for Alzheimer disease |
| `flag_inflpn` | flag_inflpn | text | Suppressed (counts 1-9) for Influenza and pneumonia |
| `flag_clrd` | flag_clrd | text | Suppressed (counts 1-9) for Chronic lower respiratory diseases |
| `flag_otherresp` | flag_otherresp | text | Suppressed (counts 1-9) for Other diseases of respiratory system |
| `flag_nephr` | flag_nephr | text | Suppressed (counts 1-9) for Nephritis, nephrotic syndrome and nephrosis |
| `flag_otherunk` | flag_otherunk | text | Suppressed (counts 1-9) for Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified |
| `flag_hd` | flag_hd | text | Suppressed (counts 1-9) for Diseases of heart |
| `flag_stroke` | flag_stroke | text | Suppressed (counts 1-9) for Cerebrovascular diseases |

### 9cpv-whbv

**Weekly counts of deaths from all causes by jurisdiction, 2015-2019** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/9cpv-whbv.json`
- Metadata: `GET https://data.cdc.gov/api/views/9cpv-whbv.json`; page: https://data.cdc.gov/d/9cpv-whbv
- Topics: Category: National Center for Health Statistics
- Tags: `united states`, `puerto rico`, `state`, `nchs`, `nvss`, `mortality`, `deaths`, `weekly`, `all causes`
- Rows: 65,382. Data updated: 2024-09-23. Probe status: 200.
- Update frequency: R/P4Y.
- Source: NCHS/DVS
- Description: This dataset includes the number of deaths from all causes by week in which the death occurred and by jurisdiction, from 2015 to 2019, United States and Puerto Rico.
- Sample row fields ($limit=1): `jurisdiction`, `age_group`, `mmwryear`, `mmwrweek`, `covid_19_deaths`, `week_ending_date`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `jurisdiction` | Jurisdiction | text |  |
| `age_group` | Age.Group | text |  |
| `mmwryear` | MMWRyear | number |  |
| `mmwrweek` | MMWRweek | number |  |
| `total_deaths` | Total.Deaths | number |  |
| `covid_19_deaths` | COVID.19.Deaths | number |  |
| `data_as_of` | Data.As.Of | text |  |
| `week_ending_date` | Week.Ending.Date | calendar_date |  |

### muzy-jte6

**Weekly Provisional Counts of Deaths by State and Select Causes, 2020-2023** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/muzy-jte6.json`
- Metadata: `GET https://data.cdc.gov/api/views/muzy-jte6.json`; page: https://data.cdc.gov/d/muzy-jte6
- Topics: Category: National Center for Health Statistics
- Tags: `nchs`, `nvss`, `mortality`, `deaths`, `all causes`, `covid-19`, `coronavirus`, `weekly`, `united states`, `state`, `puerto rico`, `provisional`, `causes of death`, `natural cause`, `septicemia`, `cancer`, `diabetes`, `alzheimer disease`, `influenza`, `pneumonia`, `chronic lower respiratory disease`, `respiratory disease`, `kidney disease`, `diseases of heart`, `cerebrovascular disease`
- Rows: 10,476. Data updated: 2023-09-27. Probe status: 200.
- Update frequency: irregular.
- Source: NCHS/DVS
- Description: Effective September 27, 2023, this dataset will no longer be updated. Similar data are accessible from wonder.cdc.gov. Provisional counts of deaths by the week the deaths occurred, by state of occurrence, and by select underlying causes of death for 2020-2023. The dataset also includes weekly provisional counts of death for COVID-19, coded to ICD-10 code U07.1 as an underlying or multiple cause of death. NOTE: death counts are presented with a one week lag.
- Sample row fields ($limit=1): `data_as_of`, `jurisdiction_of_occurrence`, `mmwryear`, `mmwrweek`, `week_ending_date`, `all_cause`, `natural_cause`, `septicemia_a40_a41`, `malignant_neoplasms_c00_c97`, `diabetes_mellitus_e10_e14`, `alzheimer_disease_g30`, `influenza_and_pneumonia_j09_j18`, `chronic_lower_respiratory`, `other_diseases_of_respiratory`, `nephritis_nephrotic_syndrome`, `symptoms_signs_and_abnormal`, `diseases_of_heart_i00_i09`, `cerebrovascular_diseases`, `covid_19_u071_multiple_cause_of_death`, `covid_19_u071_underlying_cause_of_death`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_as_of` | Data As Of | calendar_date | Date of analysis |
| `jurisdiction_of_occurrence` | Jurisdiction of Occurrence | text | Jurisdiction of Occurrence |
| `mmwryear` | MMWR Year | text | MMWR Year |
| `mmwrweek` | MMWR Week | text | MMWR Week |
| `week_ending_date` | Week Ending Date | text | Week Ending Date |
| `all_cause` | All Cause | number | All Cause |
| `natural_cause` | Natural Cause | number | Natural Cause (A00-R99, U07) |
| `septicemia_a40_a41` | Septicemia (A40-A41) | number | Septicemia (A40-A41) |
| `malignant_neoplasms_c00_c97` | Malignant neoplasms (C00-C97) | number | Malignant neoplasms (C00-C97) |
| `diabetes_mellitus_e10_e14` | Diabetes mellitus (E10-E14) | number | Diabetes mellitus (E10-E14) |
| `alzheimer_disease_g30` | Alzheimer disease (G30) | number | Alzheimer disease (G30) |
| `influenza_and_pneumonia_j09_j18` | Influenza and pneumonia (J09-J18) | number | Influenza and pneumonia (J09-J18) |
| `chronic_lower_respiratory` | Chronic lower respiratory diseases (J40-J47) | number | Chronic lower respiratory diseases (J40-J47) |
| `other_diseases_of_respiratory` | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) | number | Other diseases of respiratory system (J00-J06,J30-J39,J67,J70-J98) |
| `nephritis_nephrotic_syndrome` | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) | number | Nephritis, nephrotic syndrome and nephrosis (N00-N07,N17-N19,N25-N27) |
| `symptoms_signs_and_abnormal` | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) | number | Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified (R00-R99) |
| `diseases_of_heart_i00_i09` | Diseases of heart (I00-I09,I11,I13,I20-I51) | number | Diseases of heart (I00-I09,I11,I13,I20-I51) |
| `cerebrovascular_diseases` | Cerebrovascular diseases (I60-I69) | number | Cerebrovascular diseases (I60-I69) |
| `covid_19_u071_multiple_cause_of_death` | COVID-19 (U071, Multiple Cause of Death) | number | COVID-19 (U071, Multiple Cause of Death) |
| `covid_19_u071_underlying_cause_of_death` | COVID-19 (U071, Underlying Cause of Death) | number | COVID-19 (U071, Underlying Cause of Death) |
| `flag_allcause` | flag_allcause | text | Suppressed (counts 1-9) for All causes of death |
| `flag_natcause` | flag_natcause | text | Suppressed (counts 1-9) for Natural causes of death |
| `flag_sept` | flag_sept | text | Suppressed (counts 1-9) for Septicemia |
| `flag_neopl` | flag_neopl | text | Suppressed (counts 1-9) for Malignant eoplasms |
| `flag_diab` | flag_diab | text | Suppressed (counts 1-9) for Diabetes mellitis |
| `flag_alz` | flag_alz | text | Suppressed (counts 1-9) for Alzheimer disease |
| `flag_inflpn` | flag_inflpn | text | Suppressed (counts 1-9) for Influenza and pneumonia |
| `flag_clrd` | flag_clrd | text | Suppressed (counts 1-9) for Chronic lower respiratory diseases |
| `flag_otherresp` | flag_otherresp | text | Suppressed (counts 1-9) for Other diseases of respiratory system |
| `flag_nephr` | flag_nephr | text | Suppressed (counts 1-9) for Nephritis, nephrotic syndrome and nephrosis |
| `flag_otherunk` | flag_otherunk | text | Suppressed (counts 1-9) for Symptoms, signs and abnormal clinical and laboratory findings, not elsewhere classified |
| `flag_hd` | flag_hd | text | Suppressed (counts 1-9) for Diseases of heart |
| `flag_stroke` | flag_stroke | text | Suppressed (counts 1-9) for Cerebrovascular diseases |
| `flag_cov19mcod` | flag_cov19mcod | text | Suppressed (counts 1-9) for COVID-19 (U071, Multiple Cause of Death) |
| `flag_cov19ucod` | flag_cov19ucod | text | Suppressed (counts 1-9) for COVID-19 (U071, Underlying Cause of Death) |

## Usage tips

- Pick the dataset by question:
  - Deaths by cause: leading causes by state 1999-2017 `bi63-dtpu`; weekly counts by jurisdiction and cause `u6jv-9ijr` (to 2023) and 2014-2019 `3yf8-kanr`; age-adjusted death rates `6rkc-nb2q`; Health, United States death rate tables `7aq9-prdf` (heart disease), `h3hw-hzvg` (cancer), `w26f-tf3h` (suicide).
  - COVID-19 deaths: by week and state, current `r8kw-7aab`; by county `kn79-hsxy`; by sex and age `9bhg-hcku`; excess deaths `xkkf-xrst`. Share of deaths from COVID-19, influenza and RSV each week: `4bc2-bbpq`.
  - Drug overdose deaths: provisional 12-month-ending counts by state `xkb8-kh2a`, by county `gb4e-yj24`, by drug `8hzs-zshh`; rates by drug type and demographics `rdjz-vn2n`.
  - Births: VSRR quarterly birth indicators `76vv-a7x8`, teen birth rates by county `3h58-x6cd`, birth and fertility rates `daba-4vfq`. Life expectancy: by state and census tract 2010-2015 `5h56-n989`, by state and sex 2018-2021 (`a5a8-jsrq`, `ncvk-7amm`, `ss2j-8ajj`, `it4f-frdc`).
  - Survey estimates: NHIS adult and child summary statistics `gj3i-hsbz` / `7ctq-myvs`, NHIS early release `trpk-sp8z`, NHANES `6rvp-rahv` and related `DQS NHANES` tables, Household Pulse indicators (anxiety or depression `8pt5-q6wp`, insurance `jb9g-gnvr`), Rapid Surveys `p89x-xx88`.
- **Provisional counts are suppressed when small.** Counts of 1-9 are left empty and flagged in a `footnote` column, and null fields are omitted from the row, so a missing count is not a zero. Sums over suppressed rows understate the total; use the dataset's own total rows (e.g. `state='United States'`) when they exist.
- Rows often mix levels of aggregation. `r8kw-7aab` has `group` `By Week`, `By Month`, `By Year` and `By Total`, and `state` includes `United States` and `New York City` next to `New York`. `group` is a SoQL keyword, so quote it with backticks: ``$where=`group`='By Week'``. In `xkb8-kh2a`, `state` is a 2-letter code (`US` for the nation), `month` is a month name (text), and `indicator` picks the measure (`Number of Drug Overdose Deaths`, `Opioids (T40.0-T40.4,T40.6)`, ...).
- `DQS` datasets and their non-`DQS` namesakes (e.g. `rdjz-vn2n` vs `95ax-ymtc`) cover the same Health, United States table; the `DQS` copy is the one still updated, and its columns can differ. `... Footnotes` datasets only decode footnote codes.
- Examples:

  ```
  # COVID-19 deaths per week nationally, newest first
  GET https://data.cdc.gov/resource/r8kw-7aab.json?$select=week_ending_date,covid_19_deaths,total_deaths&$where=`group`='By Week' AND state='United States'&$order=week_ending_date DESC&$limit=10
  # Overdose deaths in the 12 months ending May 2026, by state (check the latest month first)
  GET https://data.cdc.gov/resource/xkb8-kh2a.json?$select=state_name,year,month,data_value&$where=indicator='Number of Drug Overdose Deaths' AND year=2026 AND month='May'&$order=data_value DESC
  # Leading causes of death in Maryland, 2017
  GET https://data.cdc.gov/resource/bi63-dtpu.json?$where=state='Maryland' AND year=2017&$order=deaths DESC
  ```
