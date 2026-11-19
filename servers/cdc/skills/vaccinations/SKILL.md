---
name: cdc-vaccinations
description: Query CDC open data (data.cdc.gov, Socrata SODA API) for the Vaccinations category. Use it for vaccination coverage of children, adolescents, adults, pregnant women, health care personnel and nursing home residents (National Immunization Survey, IQVIA, Medicare and Household Pulse based estimates), flu vaccination coverage and doses distributed, COVID-19 vaccinations, vaccine allocations, COVID-19 vaccine hesitancy estimates by county, kindergarten vaccination coverage and exemptions, and RSV vaccination and nirsevimab.
---

# CDC open data: Vaccinations

## Overview

- Portal: `https://data.cdc.gov` (Socrata). Category browse page: `https://data.cdc.gov/browse?category=Vaccinations`.
- Catalog snapshot taken 2026-11-09: 87 public assets in the category: 78 datasets, 0 filtered views, 4 maps, 5 charts.
- Excluded (not public or no API endpoint): 2 assets: 1 `story` (no API endpoint), 1 restricted public.
- Common tags (number of assets): `vaccination` (32), `nis-acm` (25), `iqvia` (24), `covid-19 vaccination` (22), `iis` (21), `covid-19` (20), `vsd` (20), `rsv vaccination` (19), `coronavirus` (18), `immunization` (18), `influenza` (16), `administration` (12), `flu` (12), `flu vaccination` (12), `izdl` (12), `adults` (11), `vaccine coverage` (11), `age` (8), `vaccination coverage` (8), `ethnicity` (7).
- Surface: read-only `GET`. Each dataset and filtered view has its own data endpoint keyed by a 4x4 id (e.g. `egm8-9wq7`). Maps and charts have no data endpoint of their own; query their parent dataset instead.
- Auth: none for reads. An optional Socrata app token in header `X-App-Token` raises the throttling limit; without one, heavy use from one IP may get HTTP 429. No key for this API exists in this project.
- Types: Socrata column types are `text`, `number`, `calendar_date` (floating timestamp, returned as `2024-10-04T00:00:00.000`), `point` (GeoJSON `{"type":"Point","coordinates":[lon,lat]}`), `url` (`{"url": ...}`), `checkbox` (boolean). In JSON output, numbers come back as strings. Null fields are omitted from a row object rather than returned as `null`.
- Topics and tags: each section's `Topics` and `Tags` lines come from the dataset's intro page (`/d/{id}`, "About this Dataset"), read from `/api/views/{id}.json`. `Sample row fields` lists the field names one `$limit=1` row returned; values were not stored.
- Freshness: the daily COVID-19 vaccination series (`8xkx-amqh` county, `unsk-b7fc` jurisdiction, `rh2h-3yt2` trends, `km4m-vcsb` demographics, `5i5k-6cmh` age and sex, booster datasets) stopped on 2023-05-12, and the vaccine allocation datasets stopped in 2021. Still updated in 2026: the RespVaxView survey data (`ee83-ukst`, `5c6r-xi2t`, `94wp-9pid`, `ksfb-ug5d`, `eanj-9nie`, `8yup-c35n`), monthly COVID-19 and RSV dose counts (`3bmy-cyyd`, `q84f-e68r`, `2yum-eg9f`, `vhcj-3k53`), Medicare beneficiary coverage (`jjpx-mxt8`), adult coverage `aetd-68ew` and kindergarten coverage `ijqb-a7ye`.
- Several datasets share a name (e.g. `vugp-mqip` / `wtw5-4wi3`, `n2zz-25mk` / `2yum-eg9f`, `eudc-n39h` / `vfj2-bfuw`). Compare "Data updated" and the columns before choosing. `3myw-4j4q` has 0 rows; its archived copy `8dyx-9z99` has the data.

## Endpoints per asset

Replace `{id}` with the asset id from the index.

| Purpose | Endpoint |
|---|---|
| Rows as JSON (SODA 2.1, SoQL params) | `GET https://data.cdc.gov/resource/{id}.json` |
| Rows as CSV / GeoJSON | `GET https://data.cdc.gov/resource/{id}.csv`, `.geojson` |
| Column + view metadata | `GET https://data.cdc.gov/api/views/{id}.json` |
| Full export (no row limit) | `GET https://data.cdc.gov/api/views/{id}/rows.csv?accessType=DOWNLOAD` |
| Human page | `https://data.cdc.gov/d/{id}` |
| Catalog search (this category) | `GET https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&categories=Vaccinations&limit=100` |

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
| 1 | [`egm8-9wq7`](#egm8-9wq7) | Archive: COVID-19 LTC Program Vaccinations and Trends in the United States, Jurisdiction | dataset |  | 19,466 | 38 | 2021-10-06 | Archived | 200 |
| 2 | [`gxj9-t96f`](#gxj9-t96f) | Archive: COVID-19 Vaccination and Case Trends by Age Group, United States | dataset |  | 5,331 | 5 | 2022-10-14 | Archived | 200 |
| 3 | [`2vpi-n544`](#2vpi-n544) | Archive: COVID-19 Vaccination Demographic Trends by Report Date, National | dataset |  | 9,448 | 6 | 2021-11-17 | Archived | 200 |
| 4 | [`jk8p-fqhn`](#jk8p-fqhn) | COVID-19 Booster Dose Eligibility in the United States | dataset |  | 808 | 28 | 2023-05-12 | R/P1D | 200 |
| 5 | [`3pbe-qh9z`](#3pbe-qh9z) | COVID-19 Primary Series Completion, Booster Dose Eligibility, and Booster Dose Receipt by Age, United States | dataset |  | 329 | 13 | 2023-05-12 | R/P1D | 200 |
| 6 | [`hwk8-wu83`](#hwk8-wu83) | COVID-19 Updated Vaccines Distributed | dataset |  | 260 | 6 | 2023-10-14 | R/P1D | 200 |
| 7 | [`5i5k-6cmh`](#5i5k-6cmh) | COVID-19 Vaccination Age and Sex Trends in the United States, National and Jurisdictional | dataset |  | 2,267,820 | 12 | 2023-05-12 | R/P1D | 200 |
| 8 | [`ksfb-ug5d`](#ksfb-ug5d) | COVID-19 Vaccination Coverage, Overall and by Selected Demographics and Jurisdiction, Among Adults 18 Years and Older, by Season | dataset |  | 54,950 | 15 | 2026-03-04 |  | 200 |
| 9 | [`km4m-vcsb`](#km4m-vcsb) | COVID-19 Vaccination Demographics in the United States,National | dataset |  | 29,886 | 25 | 2023-05-12 | R/P1D | 200 |
| 10 | [`rh2h-3yt2`](#rh2h-3yt2) | COVID-19 Vaccination Trends in the United States,National and Jurisdictional | dataset |  | 88,560 | 29 | 2023-05-12 | R/P1D | 200 |
| 11 | [`8xkx-amqh`](#8xkx-amqh) | COVID-19 Vaccinations in the United States,County | dataset |  | 1,962,781 | 80 | 2023-05-12 | R/P1D | 200 |
| 12 | [`unsk-b7fc`](#unsk-b7fc) | COVID-19 Vaccinations in the United States,Jurisdiction | dataset |  | 38,488 | 109 | 2023-05-12 | R/P1D | 200 |
| 13 | [`w9zu-fywh`](#w9zu-fywh) | COVID-19 Vaccine Distribution Allocations by Jurisdiction - Janssen | dataset |  | 504 | 3 | 2021-05-05 | Weekly (Tuesday) | 200 |
| 14 | [`b7pe-5nws`](#b7pe-5nws) | COVID-19 Vaccine Distribution Allocations by Jurisdiction - Moderna | dataset |  | 1,701 | 4 | 2021-06-17 | Weekly (Tuesday) | 200 |
| 15 | [`saz5-9hgg`](#saz5-9hgg) | COVID-19 Vaccine Distribution Allocations by Jurisdiction - Pfizer | dataset |  | 1,764 | 4 | 2021-06-17 | Weekly (Tuesday) | 200 |
| 16 | [`9b5z-wnve`](#9b5z-wnve) | COVID-19 Vaccines Up to Date Status | dataset |  | 12,685 | 6 | 2023-10-13 | R/P1D | 200 |
| 17 | [`b6uq-hdgz`](#b6uq-hdgz) | Cumulative Influenza Vaccination Coverage and Comparison, Adults 18 Years and Older, US, National Immunization Survey-Adult COVID Module | dataset |  | 45,312 | 36 | 2023-04-28 |  | 200 |
| 18 | [`6p3a-6xr9`](#6p3a-6xr9) | Cumulative Influenza Vaccination Coverage and Intent for Vaccination Among Adults 18 Years and Older by Age, Race/Ethnicity, and COVID-19 Vaccination and Intent, United States; IPSOS Knowledge Panel and NORC AmeriSpeak Omnibus Surveys. | dataset |  | 52 | 22 | 2023-03-31 | Weekly | 200 |
| 19 | [`ty79-wym3`](#ty79-wym3) | Cumulative Influenza Vaccination Coverage by Age Group, Race/Ethnicity, Urbanicity and Jurisdiction, NIS-ACM, Adults 18 Years and Older - NIS ACM | dataset |  | 105,728 | 25 | 2023-04-28 |  | 200 |
| 20 | [`3myw-4j4q`](#3myw-4j4q) | Cumulative Influenza Vaccination Coverage by Race/Ethnicity and Age Group, NIS-ACM | dataset |  | 0 | 22 | 2023-03-28 |  | 200 |
| 21 | [`8dyx-9z99`](#8dyx-9z99) | Cumulative Influenza Vaccination Coverage by Race/Ethnicity and Age Group, NIS-ACM (Archived) | dataset |  | 7,152 | 22 | 2022-09-28 |  | 200 |
| 22 | [`2den-c3u2`](#2den-c3u2) | Cumulative Influenza Vaccination Coverage Differences by Race/Ethnicity, Children 6 months through 17 years, United States | dataset |  | 2,208 | 13 | 2024-05-24 | Weekly | 200 |
| 23 | [`kmap-fsfn`](#kmap-fsfn) | Cumulative Influenza Vaccination Coverage, Adults 18 years and older, by Age Group and Race/Ethnicity, United States | dataset |  | 140 | 18 | 2022-04-01 | Weekly | 200 |
| 24 | [`nkr7-scx6`](#nkr7-scx6) | Cumulative Influenza Vaccination Coverage, by Flu Season and Race/Ethnicity, Pregnant Women 18-49 years | dataset |  | 280 | 4 | 2025-01-31 |  | 200 |
| 25 | [`v22g-tzpk`](#v22g-tzpk) | Differences in Cumulative Influenza Vaccination Coverage by Selected Demographics, Adults 18 Year and Older, NIS Adult COVID Module | dataset |  | 4,323 | 13 | 2024-05-24 |  | 200 |
| 26 | [`muep-c3qd`](#muep-c3qd) | Household Pulse Survey (HPS): COVID-19 Vaccination among People with Disabilities | dataset |  | 1,347 | 10 | 2022-12-20 |  | 200 |
| 27 | [`scrf-8d7w`](#scrf-8d7w) | Monthly Cumulative Number and Percent of Adults 60 Years and Older Who Received at least one RSV Vaccination Doses by Jurisdiction, United States | dataset |  | 549 | 7 | 2024-08-05 |  | 200 |
| 28 | [`n2zz-25mk`](#n2zz-25mk) | Monthly Cumulative Number and Percent of Adults 75 Years and Older Who Received 1+ RSV Vaccination Doses by Jurisdiction, United States | dataset |  | 504 | 8 | 2025-05-16 |  | 200 |
| 29 | [`2yum-eg9f`](#2yum-eg9f) | Monthly Cumulative Number and Percent of Adults 75 Years and Older Who Received 1+ RSV Vaccination Doses by Jurisdiction, United States | dataset |  | 567 | 8 | 2026-05-20 | Monthly | 200 |
| 30 | [`ku7p-zn4c`](#ku7p-zn4c) | Monthly Cumulative Number and Percent of Children <20 Months Who Received Nirsevimab by Age Group and Jurisdiction, United States | dataset |  | 1,647 | 6 | 2024-08-05 |  | 200 |
| 31 | [`vhcj-3k53`](#vhcj-3k53) | Monthly Cumulative Number and Percent of Children <8 Months Who Received 1+ Monoclonal Antibody Doses by Jurisdiction, United States | dataset |  | 504 | 7 | 2026-05-20 | Monthly | 200 |
| 32 | [`4bdk-kyzv`](#4bdk-kyzv) | Monthly Cumulative Number and Percent of Children <8 Months Who Received Nirsevimab by Jurisdiction, United States | dataset |  | 441 | 7 | 2025-05-16 |  | 200 |
| 33 | [`q84f-e68r`](#q84f-e68r) | Monthly Cumulative Number and Percent of Persons Who Received 1+ COVID-19 Vaccination Doses and Comparison between 2025─26 and Previous Seasons, by Age Group and Jurisdiction, United States | dataset |  | 12,600 | 13 | 2026-05-20 |  | 200 |
| 34 | [`3bmy-cyyd`](#3bmy-cyyd) | Monthly Cumulative Number and Percent of Persons Who Received 1+ COVID-19 Vaccination Doses, by Season, Age Group, and Jurisdiction, United States | dataset |  | 21,420 | 9 | 2026-05-20 |  | 200 |
| 35 | [`wtw5-4wi3`](#wtw5-4wi3) | Monthly Cumulative Number and Percent of Persons Who Received 1+ updated 2023-24 COVID-19 Vaccination Doses by Age Group and Jurisdiction, United States | dataset |  | 6,237 | 7 | 2024-08-05 |  | 200 |
| 36 | [`vugp-mqip`](#vugp-mqip) | Monthly Cumulative Number and Percent of Persons Who Received 1+ updated 2023-24 COVID-19 Vaccination Doses by Age Group and Jurisdiction, United States | dataset |  | 6,237 | 8 | 2024-08-05 |  | 200 |
| 37 | [`si7g-c2bs`](#si7g-c2bs) | National Immunization Survey Adult COVID Module (NIS-ACM): RespVaxView\| Data \| Centers for Disease Control and Prevention (cdc.gov) 2024-2025 Archive Season | dataset |  | 1,440,643 | 14 | 2025-05-16 |  | 200 |
| 38 | [`qz99-wyhv`](#qz99-wyhv) | National Immunization Survey Adult COVID Module (NIS-ACM): Trends in Behavioral Indicators Among Unvaccinated People | dataset |  | 42,767 | 13 | 2023-08-03 |  | 200 |
| 39 | [`akkj-j5ru`](#akkj-j5ru) | National Immunization Survey Adult COVID Module (NIS-ACM): Trends in Vaccination Status and Intent | dataset |  | 9,436 | 13 | 2023-08-03 |  | 200 |
| 40 | [`iwxc-qftf`](#iwxc-qftf) | National Immunization Survey Adult COVID Module (NIS-ACM): Vaccination Status and Intent by Demographics | dataset |  | 165,474 | 13 | 2023-08-03 |  | 200 |
| 41 | [`uny6-e3dx`](#uny6-e3dx) | National Immunization Survey Child COVID Module (NIS-CCM): COVIDVaxViews\| Data \| Centers for Disease Control and Prevention (cdc.gov)-Archived | dataset |  | 45,635 | 14 | 2024-01-18 |  | 200 |
| 42 | [`gr26-95h2`](#gr26-95h2) | National Immunization Survey Child COVID Module (NIS-CCM): Vaccination Status and Intent by Demographics \| Data \| Centers for Disease Control and Prevention (cdc.gov) | dataset |  | 8,609 | 14 | 2023-08-03 |  | 200 |
| 43 | [`ee83-ukst`](#ee83-ukst) | National Immunization Survey Fall Respiratory Virus Module (NIS-FRVM): RespVaxView\| Data \| Centers for Disease Control and Prevention (cdc.gov) | dataset |  | 544,489 | 14 | 2026-03-04 |  | 200 |
| 44 | [`94wp-9pid`](#94wp-9pid) | Vaccination Concerns, Issues, and Motivators \| RespVaxView \| Data \| Centers for Disease Control and Prevention (cdc.gov) | dataset |  | 14,942 | 16 | 2026-10-16 |  | 200 |
| 45 | [`aetd-68ew`](#aetd-68ew) | Vaccination Coverage among Adults (18+ Years) | dataset |  | 67,596 | 11 | 2026-03-11 |  | 200 |
| 46 | [`xerk-pcm8`](#xerk-pcm8) | Vaccination Coverage among Health Care Personnel | dataset |  | 1,456 | 8 | 2024-09-12 |  | 200 |
| 47 | [`8w4j-reb4`](#8w4j-reb4) | Vaccination Coverage among Nursing Home Residents | dataset |  | 44,518 | 8 | 2024-09-12 |  | 200 |
| 48 | [`ijqb-a7ye`](#ijqb-a7ye) | Vaccination Coverage and Exemptions among Kindergartners | dataset |  | 8,753 | 11 | 2026-08-28 |  | 200 |
| 49 | [`q9mh-h2tw`](#q9mh-h2tw) | Vaccine Hesitancy for COVID-19: County and local estimates | dataset |  | 3,142 | 21 | 2021-06-17 | Monthly | 200 |
| 50 | [`djj9-kh3p`](#djj9-kh3p) | Vaccine Hesitancy for COVID-19: Public Use Microdata Areas (PUMAs) | dataset |  | 2,351 | 12 | 2021-06-17 | Monthly | 200 |
| 51 | [`5jp2-pgaw`](#5jp2-pgaw) | Vaccines.gov: COVID-19 vaccinating provider locations | dataset |  | 253,144 | 34 | 2024-08-01 |  | 200 |
| 52 | [`eanj-9nie`](#eanj-9nie) | Weekly Cumulative COVID-19 Vaccination Coverage Map and Comparison Between 2025–26 and Previous Seasons, Overall, by Jurisdiction Among Adults 18 Years | dataset |  | 2,894 | 23 | 2026-03-04 |  | 200 |
| 53 | [`jjpx-mxt8`](#jjpx-mxt8) | Weekly Cumulative COVID-19 Vaccination Coverage, by Season and Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥65 years | dataset |  | 792 | 9 | 2026-05-20 |  | 200 |
| 54 | [`k87d-gv3u`](#k87d-gv3u) | Weekly Cumulative Doses (in Millions) of Influenza Vaccine Distributed by Flu Season in the United States | dataset |  | 160 | 9 | 2026-08-03 | Weekly | 200 |
| 55 | [`ewpg-rz7g`](#ewpg-rz7g) | Weekly Cumulative Estimated Number of COVID-19 Vaccinations Administered in Retail Pharmacies and Physician Medical Offices, Adults 18 years and older, by Season and Age Group, United States | dataset |  | 2,730 | 13 | 2026-05-20 |  | 200 |
| 56 | [`83ng-twza`](#83ng-twza) | Weekly Cumulative Estimated Number of Influenza Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 18 years and older, United States | dataset |  | 627 | 12 | 2024-05-24 | Weekly | 200 |
| 57 | [`uxgd-cqqc`](#uxgd-cqqc) | Weekly Cumulative Estimated Number of Influenza Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 18 years and older, United States (ARCHIVED) | dataset |  | 363 | 12 | 2022-09-28 |  | 200 |
| 58 | [`a3gi-4phs`](#a3gi-4phs) | Weekly Cumulative Estimated Number of RSV Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 60 years and older, United States | dataset |  | 138 | 10 | 2024-09-11 |  | 200 |
| 59 | [`52ds-xw49`](#52ds-xw49) | Weekly Cumulative Estimated Number of RSV Vaccinations Administered in Retail Pharmacies and Physicians' Medical Offices, Adults 50 to 74 Years and 75 years and older, United States | dataset |  | 342 | 10 | 2026-05-20 | Weekly | 200 |
| 60 | [`hea5-6w9c`](#hea5-6w9c) | Weekly Cumulative Estimated Number of RSV Vaccinations Administered in Retail Pharmacies and Physicians’ Medical Offices, Adults 60 to 74 Years and 75 years and older, United States | dataset |  | 222 | 11 | 2025-05-16 |  | 200 |
| 61 | [`w76m-r924`](#w76m-r924) | Weekly Cumulative Estimated Number of Updated 2023-24 COVID-19 Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 18 years and older, United States, Data Source(s): IQVIA Pharmacy and Physician Medical Office Claims | dataset |  | 99 | 10 | 2024-08-28 |  | 200 |
| 62 | [`g57i-yx3r`](#g57i-yx3r) | Weekly Cumulative Influenza Vaccination Coverage, by Flu Season and Race/Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥65 years, United States | dataset |  | 1,446 | 9 | 2025-04-22 | Weekly | 200 |
| 63 | [`eudc-n39h`](#eudc-n39h) | Weekly Cumulative Influenza Vaccination Coverage, Children 6 months through 17 years, United States | dataset |  | 4,262 | 24 | 2024-05-24 | Weekly | 200 |
| 64 | [`vfj2-bfuw`](#vfj2-bfuw) | Weekly Cumulative Influenza Vaccination Coverage, Children 6 months through 17 years, United States | dataset |  | 6,694 | 23 | 2022-09-28 |  | 200 |
| 65 | [`e5zk-7tx5`](#e5zk-7tx5) | Weekly Cumulative Influenza Vaccine Doses Distributed in the United States | dataset |  | 176 | 9 | 2022-09-28 |  | 200 |
| 66 | [`sjpm-fk4b`](#sjpm-fk4b) | Weekly Cumulative Percentage of Adults 18 Years and Older Vaccinated with the Updated 2023-24 COVID-19 Vaccine by Jurisdiction | dataset |  | 18,250 | 10 | 2024-08-28 |  | 200 |
| 67 | [`qve4-fp9c`](#qve4-fp9c) | Weekly Cumulative Percentage of Adults 60 Years and Older Vaccinated with Respiratory Syncytial Virus (RSV) Vaccine by Jurisdiction | dataset |  | 17,425 | 10 | 2024-08-28 |  | 200 |
| 68 | [`qeq7-f3ir`](#qeq7-f3ir) | Weekly Cumulative RSV Vaccination Coverage and Intent, Overall, by Selected Demographics and Jurisdiction, Among Adults 75 and Older and 50-74 Years with High-Risk Conditions Ever Vaccinated, United States | dataset |  | 7,400 | 14 | 2026-03-04 |  | 200 |
| 69 | [`k4cb-dxd7`](#k4cb-dxd7) | Weekly Cumulative RSV Vaccination Coverage and Intent, Overall, by Selected Demographics and Jurisdiction, Among Adults 75 and Older and 60-74 Years with High-Risk Conditions Ever Vaccinated, United States | dataset |  | 12,420 | 15 | 2025-05-20 |  | 200 |
| 70 | [`55uq-699y`](#55uq-699y) | Weekly Cumulative RSV Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥65 years, United States, Data Source: Centers for Medicare & Medicaid Services Chronic Conditions Warehouse | dataset |  | 288 | 7 | 2026-07-30 |  | 200 |
| 71 | [`nqu5-vn7d`](#nqu5-vn7d) | Weekly Cumulative RSV Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥75 years and enrolled in a Part D plan, United States, Data Source: Centers for Medicare & Medicaid Services Chronic Conditions Warehouse | dataset |  | 156 | 7 | 2025-05-16 |  | 200 |
| 72 | [`msnx-y6hi`](#msnx-y6hi) | Weekly Cumulative RSV Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥75 years and Enrolled in a Part D plan, United States, Data Source: Centers for Medicare & Medicaid Services Chronic Conditions Warehouse | dataset |  | 186 | 7 | 2026-05-20 |  | 200 |
| 73 | [`brsb-akdp`](#brsb-akdp) | Weekly Cumulative Updated 2023-24 COVID-19 Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥65 years, United States, Data Source: Centers for Medicare & Medicaid Services Chronic Conditions Warehouse | dataset |  | 186 | 8 | 2026-08-03 |  | 200 |
| 74 | [`8yup-c35n`](#8yup-c35n) | Weekly Differences in Cumulative COVID-19 Vaccination Coverage by Selected Demographics and by Season, Among Adults 18 Years, Overall | dataset |  | 2,460 | 13 | 2026-03-04 |  | 200 |
| 75 | [`4tme-u33f`](#4tme-u33f) | Weekly Differences in Cumulative Respiratory Syncytial Virus (RSV) Vaccination Coverage and Comparison, Overall, by Jurisdiction, Among Adults 75 Years and Older and Adults 50-74 Years with High-Risk Conditions | dataset |  | 1,760 | 13 | 2026-03-04 |  | 200 |
| 76 | [`mcvh-596h`](#mcvh-596h) | Weekly Differences in Cumulative RSV Vaccination Coverage Among Adults 75 and Older and 60-74 Years with High-Risk Conditions Ever Vaccinated with RSV Vaccine, Overall, by Selected Demographics | dataset |  | 3,074 | 13 | 2025-12-10 | Weekly | 200 |
| 77 | [`ndai-i7s4`](#ndai-i7s4) | Weekly Differences in Cumulative RSV Vaccination Coverage Among Adults 75 and Older and 60–74 Years with High-Risk Conditions Ever Vaccinated with RSV Vaccine, Overall, by Selected Demographics | dataset |  | 3,074 | 13 | 2025-05-16 |  | 200 |
| 78 | [`5c6r-xi2t`](#5c6r-xi2t) | Weekly Respiratory Virus Vaccination Data, Children 6 Months-17 Years and Adults 18 Years and Older, National Immunization Survey | dataset |  | 1,040 | 17 | 2026-09-14 | R/P1W | 200 |

Maps and charts (no data endpoint; query the parent):

| Id | Name | Type | Built on | Updated |
|---|---|---|---|---|
| `s5hu-2eck` | Ability to handle a COVID-19 outbreak (CVAC) | map | `q9mh-h2tw` (Vaccine Hesitancy for COVID-19: County and local estimates) | 2026-09-09 |
| `c4bi-8ytd` | COVID-19 County Hesitancy | map | `q9mh-h2tw` (Vaccine Hesitancy for COVID-19: County and local estimates) | 2026-09-10 |
| `jm79-dz78` | Fully Vaccinated Adults | map | `q9mh-h2tw` (Vaccine Hesitancy for COVID-19: County and local estimates) | 2026-09-10 |
| `ypqf-r5qs` | Social Vulnerability Index | map | `q9mh-h2tw` (Vaccine Hesitancy for COVID-19: County and local estimates) | 2026-09-09 |
| `2r93-e5cs` | National Weekly Janssen Allocations | chart | `w9zu-fywh` (COVID-19 Vaccine Distribution Allocations by Jurisdiction - Janssen) | 2026-09-10 |
| `ke78-phpe` | National Weekly Moderna Allocations | chart | `b7pe-5nws` (COVID-19 Vaccine Distribution Allocations by Jurisdiction - Moderna) | 2026-09-10 |
| `sxbq-3sid` | National Weekly Pfizer Allocations | chart | `saz5-9hgg` (COVID-19 Vaccine Distribution Allocations by Jurisdiction - Pfizer) | 2026-09-09 |
| `spzz-he63` | State Moderna Allocation Totals | chart | `b7pe-5nws` (COVID-19 Vaccine Distribution Allocations by Jurisdiction - Moderna) | 2026-09-09 |
| `y77q-5ru3` | State Pfizer Allocation Totals | chart | `saz5-9hgg` (COVID-19 Vaccine Distribution Allocations by Jurisdiction - Pfizer) | 2026-09-09 |

Map/chart topics and tags:

- `s5hu-2eck`: Category: Vaccinations; Tags: none
- `c4bi-8ytd`: Category: Vaccinations; Tags: none
- `jm79-dz78`: Category: Vaccinations; Tags: none
- `ypqf-r5qs`: Category: Vaccinations; Tags: none
- `2r93-e5cs`: Category: Vaccinations; Tags: none
- `ke78-phpe`: Category: Vaccinations; Tags: none
- `sxbq-3sid`: Category: Vaccinations; Tags: none
- `spzz-he63`: Category: Vaccinations; Tags: none
- `y77q-5ru3`: Category: Vaccinations; Tags: none

## Datasets and filtered views

### egm8-9wq7

**Archive: COVID-19 LTC Program Vaccinations and Trends in the United States, Jurisdiction** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/egm8-9wq7.json`
- Metadata: `GET https://data.cdc.gov/api/views/egm8-9wq7.json`; page: https://data.cdc.gov/d/egm8-9wq7
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `report date`
- Rows: 19,466. Data updated: 2021-10-06. Probe status: 200.
- Update frequency: Archived.
- Description: The Federal Pharmacy Partnership for Long-Term Care (LTC) Program was a partnership between CDC and CVS, Walgreens, and Managed Health Care Associates, Inc. The program offered on-site COVID-19 vaccination services for residents of nursing homes and assisted living facilities. The Federal Pharmacy Partnership for LTC Program was in effect after vaccines became available to April 23, 2021. This is the historical archived data related to the LTC Program and represents data that was shown on COVID Data Tracker through September 30, 2021. Twelve variables that provided data on residents and staff…
- Sample row fields ($limit=1): `date`, `date_type`, `mmwr_week`, `location`, `distributed`, `distributed_moderna`, `distributed_pfizer`, `distributed_janssen`, `distributed_unk_manuf`, `administered`, `recip_administered`, `administered_moderna`, `administered_pfizer`, `administered_janssen`, `administered_unk_manuf`, `administered_daily`, `administered_cumulative`, `administered_7_day_rolling`, `admin_dose_1_daily`, `admin_dose_1_cumulative`, `admin_dose_1_day_rolling`, `administered_daily_change`, `administered_daily_change_1`, `series_complete_daily`, `series_complete_cumulative`, `series_complete_day_rolling`, `administered_fed_ltc`, `administered_fed_ltc_residents`, `administered_fed_ltc_staff`, `administered_fed_ltc_unk`, `administered_fed_ltc_dose1`, `administered_fed_ltc_dose1_1`, `administered_fed_ltc_dose1_2`, `administered_fed_ltc_dose1_3`, `series_complete_fedltc`, `series_complete_fedltc_1`, `series_complete_fedltc_staff`, `series_complete_fedltc_unknown`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date |
| `date_type` | Date_Type | text | The week of the epidemiologic year as defined by the Morbidity and Mortality Weekly Report (https://ndc.services.cdc.gov/wp-content/uploads/MMWR_week_overview.pdf). |
| `mmwr_week` | MMWR_week | number | Jurisdiction abbreviation (see tab 2 for full name) |
| `location` | Location | text | Total number of distributed doses |
| `distributed` | Distributed | number | Total number of Moderna doses delivered |
| `distributed_moderna` | Distributed_Moderna | number | Total number of Pfizer-BioNTech doses delivered |
| `distributed_pfizer` | Distributed_Pfizer | number | Total number of J&J/Janssen doses delivered |
| `distributed_janssen` | Distributed_Janssen | number | Total number of doses from unknown manufacturer delivered |
| `distributed_unk_manuf` | Distributed_Unk_Manuf | number | Total number of administered doses based on the jurisdiction (state/territory) where administered |
| `administered` | Administered | number | Total number of doses administered based on the jurisdiction where recipient lives |
| `recip_administered` | Recip_Administered | number | Total number of Moderna doses administered |
| `administered_moderna` | Administered_Moderna | number | Total number of Pfizer-BioNTech doses administered |
| `administered_pfizer` | Administered_Pfizer | number | Total number of J&J/Janssen doses administered |
| `administered_janssen` | Administered_Janssen | number | Total number of doses from unknown manufacturer administered |
| `administered_unk_manuf` | Administered_Unk_Manuf | number | Type of date on COVID Tracker: "Admin" = Date of Administration "Report" = Date of Report |
| `administered_daily` | Administered_Daily | number | Total number of administered doses by date of administration. |
| `administered_cumulative` | Administered_Cumulative | number | Cumulative number of reported doses administered by date of administration |
| `administered_7_day_rolling` | Administered_7_Day_Rolling_Average | number | 7-day average of the daily doses administered by date of administration |
| `admin_dose_1_daily` | Admin_Dose_1_Daily | number | Total number of Dose 1 administations by date of administration |
| `admin_dose_1_cumulative` | Admin_Dose_1_Cumulative | number | Cumulative number of people with at least one dose of any vaccine by date of administration. |
| `admin_dose_1_day_rolling` | Admin_Dose_1_Day_Rolling_Average | number | 7-day average count of people with at least one dose of any vaccine by date of administration |
| `administered_daily_change` | Administered_daily_change_report | number | Change between the cumulative number of doses administered on a given day and the previous day by date of report |
| `administered_daily_change_1` | Administered_daily_change_report_7dayroll | number | 7-day average of the daily change based by date of report |
| `series_complete_daily` | Series_Complete_Daily | number | Daily total count of people fully vaccinated by date of administration |
| `series_complete_cumulative` | Series_Complete_Cumulative | number | Cumulative total of people who are fully vaccinated by date of administration |
| `series_complete_day_rolling` | Series_Complete_Day_Rolling_Average | number | 7-day average count of people who are fully vaccinated by date of administration |
| `administered_fed_ltc` | Administered_Fed_LTC | number | Total number of doses administed in long-term care facilities |
| `administered_fed_ltc_residents` | Administered_Fed_LTC_Residents | number | Total number of doses administed to long-term care facility residents |
| `administered_fed_ltc_staff` | Administered_Fed_LTC_Staff | number | Total number of doses administed to long-term care facility staff |
| `administered_fed_ltc_unk` | Administered_Fed_LTC_Unk | number | Total number of doses administed to other people in long-term care facility |
| `administered_fed_ltc_dose1` | Administered_Fed_LTC_Dose1 | number | Total number of people with at least one dose of any vaccine in long-term care facilities |
| `administered_fed_ltc_dose1_1` | Administered_Fed_LTC_Dose1_Residents | number | Total number of residents with at least one dose of any vaccine in long-term care facilities |
| `administered_fed_ltc_dose1_2` | Administered_Fed_LTC_Dose1_Staff | number | Total number of staff with at least one dose of any vaccine in long-term care facilities |
| `administered_fed_ltc_dose1_3` | Administered_Fed_LTC_Dose1_Unk | number | Total number of other people with at least one dose of any vaccine in long-term care facilities |
| `series_complete_fedltc` | Series_Complete_FedLTC | number | Total number of people who are fully vaccinated (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) in long-term care facilities |
| `series_complete_fedltc_1` | Series_Complete_FedLTC_Residents | number | Total number of residents who are fully vaccinated (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) in long-term care facilities |
| `series_complete_fedltc_staff` | Series_Complete_FedLTC_Staff | number | Total number of staff who are fully vaccinated (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) in long-term care facilities |
| `series_complete_fedltc_unknown` | Series_Complete_FedLTC_Unknown | number | Total number of other people who are fully vaccinated (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) in long-term care facilities |

### gxj9-t96f

**Archive: COVID-19 Vaccination and Case Trends by Age Group, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/gxj9-t96f.json`
- Metadata: `GET https://data.cdc.gov/api/views/gxj9-t96f.json`; page: https://data.cdc.gov/d/gxj9-t96f
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `report date`, `cases`
- Rows: 5,331. Data updated: 2022-10-14. Probe status: 200.
- Update frequency: Archived.
- Source: IISInfo
- Description: </p><p style="margin:0in;vertical-align:baseline;"><strong><em><span style='font-size:15px;font-family:"Calibri",sans-serif;color:black;'>After October 13, 2022, this dataset will no longer be updated as the related CDC COVID Data Tracker site was retired on October 13, 2022.</span></em></strong><span style='font-size:15px;font-family:"Calibri",sans-serif;color:black;'>&nbsp;</span></p>This dataset contains historical trends in vaccinations and cases by age group, at the US national level. Data is stratified by at least one dose and fully vaccinated. Data also represents all vaccine partners…
- Sample row fields ($limit=1): `cdc_case_earliest_dt`, `agegroupvacc`, `_7_day_avg_group_cases_per`, `administered_dose1_pct`, `series_complete_pop_pct`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `cdc_case_earliest_dt` | Date Administered | calendar_date | Best available date related to illness/specimen collection and when a case is reported. |
| `agegroupvacc` | AgeGroupVacc | text | Age group specifics for vaccination data |
| `_7_day_avg_group_cases_per` | 7-day_avg_group_cases_per_100k | number | 7 day average of the daily cases reported |
| `administered_dose1_pct` | Administered_Dose1_pct_agegroup | number | Percent of population with at lease one dose in that specific age group |
| `series_complete_pop_pct` | Series_Complete_Pop_pct_agegroup | number | Percent of people who completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) in an age group |

### 2vpi-n544

**Archive: COVID-19 Vaccination Demographic Trends by Report Date, National** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/2vpi-n544.json`
- Metadata: `GET https://data.cdc.gov/api/views/2vpi-n544.json`; page: https://data.cdc.gov/d/2vpi-n544
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `report date`
- Rows: 9,448. Data updated: 2021-11-17. Probe status: 200.
- Update frequency: Archived.
- Description: This data dictionary provides information about archived demographic trend data for people receiving COVID-19 vaccinations in the United States at the national level. Data represents all vaccine partners including jurisdictional partner clinics, retail pharmacies, long-term care facilities, dialysis centers, Federal Emergency Management Agency and Health Resources and Services Administration partner sites, and federal entity facilities. These data have been archived to provide historical demographic trend data for COVID-19 vaccine recipients prior to CDC converting the Vaccination Demographic…
- Sample row fields ($limit=1): `date`, `demographic_category`, `administered_dose1`, `series_complete_yes`, `administered_dose1_pct`, `series_complete_pop_pct`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date data were reported on CDC COVID Data Tracker |
| `demographic_category` | Demographic_category | text | Age, sex, or race/ethnicity group of vaccine recipient |
| `administered_dose1` | Administered_Dose1 | number | Total count of people with at least one dose, based on date of report to CDC |
| `series_complete_yes` | Series_Complete_Yes | number | Total count of people who are fully vaccinated, based on date of report to CDC |
| `administered_dose1_pct` | Administered_Dose1_pct_agegroup | number | Percent of people in a demographic category with at least one dose, based on date of report to CDC |
| `series_complete_pop_pct` | Series_Complete_Pop_pct_agegroup | number | Percent of people in a demographic category who are fully vaccinated, based on date of report to CDC |

### jk8p-fqhn

**COVID-19 Booster Dose Eligibility in the United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/jk8p-fqhn.json`
- Metadata: `GET https://data.cdc.gov/api/views/jk8p-fqhn.json`; page: https://data.cdc.gov/d/jk8p-fqhn
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `demographics`, `sex`, `age`, `race`, `ethnicity`
- Rows: 808. Data updated: 2023-05-12. Probe status: 200.
- Update frequency: R/P1D.
- Source: IISInfo
- Description: <p style="margin:0in;vertical-align:baseline;"><span style='font-size:15px;font-family:"Calibri",sans-serif;color:black;'>This site provides historical data related to COVID-19 booster dose eligibility presented on two CDC COVID Data Tracker sites:&nbsp;</span><a href="https://covid.cdc.gov/covid-data-tracker/#vaccinations"><span style='font-size:15px;font-family:"Calibri",sans-serif;color:black;'>Vaccinations in the US</span></a><span style='font-size:15px;font-family:"Calibri",sans-serif;color:black;'>&nbsp;and&nbsp;</span><a href="https://covid.cdc.gov/covid-data-tracker/#vaccination-equit…
- Sample row fields ($limit=1): `date`, `category`, `location`, `booster_eligible`, `booster_eligible_notboosted`, `booster_eligible_boosted_pct`, `booster_eligible_notboosted_pct`, `booster_eligible_us_pct`, `booster_eligible_18plus`, `booster_eligible_notboosted_18plus`, `booster_eligible_boosted_18plus_pct`, `booster_eligible_notboosted_18plus_pct`, `booster_eligible_us_18plus_pct`, `booster_eligible_50plus`, `booster_eligible_notboosted_50plus`, `booster_eligible_boosted_50plus_pct`, `booster_eligible_notboosted_50plus_pct`, `booster_eligible_us_50plus_pct`, `booster_eligible_65plus`, `booster_eligible_notboosted_65plus`, `booster_eligible_boosted_65plus_pct`, `booster_eligible_notboosted_65plus_pct`, `booster_eligible_us_65plus_pct`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date data are reported on CDC COVID Data Tracker |
| `category` | Category | text | Demographic category |
| `location` | Location | text | Location |
| `booster_eligible` | Booster_Eligible | number | People Eligible for a Booster Dose, Total |
| `booster_eligible_notboosted` | Booster_Eligible_NotBoosted | number | People Eligible for a Booster with no Booster Dose, Total |
| `booster_eligible_boosted_pct` | Booster_Eligible_Boosted_Pct | number | Percent of Booster Eligible People with a Booster Dose |
| `booster_eligible_notboosted_pct` | Booster_Eligible_NotBoosted_Pct | number | Percent of Booster Eligible People with no Booster Dose |
| `booster_eligible_us_pct` | Booster_Eligible_US_Pct | number | Percent of US Population Eligible for a Booster Dose |
| `booster_eligible_12plus` | Booster_Eligible_12Plus | number | People Eligible for a Booster Dose, ≥12 Years of Age |
| `booster_eligible_notboosted_12plus` | Booster_Eligible_NotBoosted_12Plus | number | Count of people eligible for a booster dose who have not received a booster dose (for ages ≥12 years) |
| `booster_eligible_boosted_12plus_pct` | Booster_Eligible_Boosted_12Plus_Pct | number | Percent of Booster Eligible People with a Booster Dose, ≥12 Years of Age |
| `booster_eligible_notboosted_12plus_pct` | Booster_Eligible_NotBoosted_12Plus_Pct | number | Percent of people eligible for a booster dose who have not received a booster dose (for ages ≥12 years) |
| `booster_eligible_us_12plus_pct` | Booster_Eligible_US_12Plus_Pct | number | Percent of US Population Eligible for a Booster, ≥12 Years of Age |
| `booster_eligible_18plus` | Booster_Eligible_18Plus | number | People Eligible for a Booster Dose, ≥18 Years of Age |
| `booster_eligible_notboosted_18plus` | Booster_Eligible_NotBoosted_18Plus | number | People Eligible for a Booster with no Booster Dose, ≥18 Years of Age |
| `booster_eligible_boosted_18plus_pct` | Booster_Eligible_Boosted_18Plus_Pct | number | Percent of Booster Eligible People with a Booster Dose, ≥18 Years of Age |
| `booster_eligible_notboosted_18plus_pct` | Booster_Eligible_NotBoosted_18Plus_Pct | number | Percent of Booster Eligible People with no Booster Dose, ≥18 Years of Age |
| `booster_eligible_us_18plus_pct` | Booster_Eligible_US_18Plus_Pct | number | Percent of US Population Eligible for a Booster, ≥18 Years of Age |
| `booster_eligible_50plus` | Booster_Eligible_50Plus | number | People Eligible for a Booster Dose, ≥50 Years of Age |
| `booster_eligible_notboosted_50plus` | Booster_Eligible_NotBoosted_50Plus | number | People Eligible for a Booster Dose with no Booster Dose, ≥50 Years of Age |
| `booster_eligible_boosted_50plus_pct` | Booster_Eligible_Boosted_50Plus_Pct | number | Percent of Booster Eligible People with a Booster Dose, ≥50 Years of Age |
| `booster_eligible_notboosted_50plus_pct` | Booster_Eligible_NotBoosted_50Plus_Pct | number | Percent of Booster Eligible People with no Booster Dose, ≥50 Years of Age |
| `booster_eligible_us_50plus_pct` | Booster_Eligible_US_50Plus_Pct | number | Percent of US Population Eligible for a Booster, ≥50 Years of Age |
| `booster_eligible_65plus` | Booster_Eligible_65Plus | number | People Eligible for a Booster Dose, ≥65 Years of Age |
| `booster_eligible_notboosted_65plus` | Booster_Eligible_NotBoosted_65Plus | number | People Eligible for a Booster Dose with no Booster Dose, ≥65 Years of Age |
| `booster_eligible_boosted_65plus_pct` | Booster_Eligible_Boosted_65Plus_Pct | number | Percent of Booster Eligible People with a Booster Dose, ≥65 Years of Age |
| `booster_eligible_notboosted_65plus_pct` | Booster_Eligible_NotBoosted_65Plus_Pct | number | Percent of Booster Eligible People with no Booster Dose, ≥65 Years of Age |
| `booster_eligible_us_65plus_pct` | Booster_Eligible_US_65Plus_Pct | number | Percent of US Population Eligible for a Booster, ≥65 Years of Age |

### 3pbe-qh9z

**COVID-19 Primary Series Completion, Booster Dose Eligibility, and Booster Dose Receipt by Age, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3pbe-qh9z.json`
- Metadata: `GET https://data.cdc.gov/api/views/3pbe-qh9z.json`; page: https://data.cdc.gov/d/3pbe-qh9z
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `demographics`, `sex`, `age`, `race`, `ethnicity`
- Rows: 329. Data updated: 2023-05-12. Probe status: 200.
- Update frequency: R/P1D.
- Source: IISInfo
- Description: This site provides historical data beginning June 22, 2022, for the visualization presented on <a href="https://covid.cdc.gov/covid-data-tracker/#vaccinations" target="_blank">COVID-19 Data Tracker’s “Vaccinations in the United States”</a> site titled “Primary Series Completion, Booster Dose Eligibility, and Booster Dose Receipt by Age, United States”. <b >Fully Vaccinated / Completed Primary Series:</b> <ul><li> For surveillance purposes, COVID Data Tracker counts people as being "fully vaccinated" or as having "completed a primary series" if they received two doses on different days (regard…
- Sample row fields ($limit=1): `date`, `demographic_category`, `census`, `series_complete`, `series_complete_pop_pct`, `first_booster_eligible`, `first_booster_eligible_pop`, `first_booster`, `first_booster_pop_pct`, `second_booster_eligible`, `second_booster_eligible_pop`, `second_booster`, `second_booster_pop_pct`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date |
| `demographic_category` | Demographic_category | text | Age group of vaccine recipient |
| `census` | Census | number | Census estimate for each age group |
| `series_complete` | Series_Complete | number | Total number of people who completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) |
| `series_complete_pop_pct` | Series_Complete_Pop_Pct | number | Percentage of each age group who completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) |
| `first_booster_eligible` | First_Booster_Eligible | number | Count of people eligible for a first booster dose, regardless of whether a booster was received or not (for all booster eligible ages) |
| `first_booster_eligible_pop` | First_Booster_Eligible_Pop_Pct | number | Percentage of each age group that is eligible for a first booster dose, regardless of whether a first booster was received or not (for all booster eligible ages) |
| `first_booster` | First_Booster | number | Total number of people who have completed a primary series and have received a booster (or additional) dose |
| `first_booster_pop_pct` | First_Booster_Pop_Pct | number | Percentage of each age group that has received a first booster (or additional) dose |
| `second_booster_eligible` | Second_Booster_Eligible | number | Count of people eligible for a second booster dose, regardless of whether a second booster was received or not (for all booster eligible ages) |
| `second_booster_eligible_pop` | Second_Booster_Eligible_Pop_Pct | number | Percentage of each age group that is eligible for a second booster dose, regardless of whether a second booster was received or not (for all booster eligible ages) |
| `second_booster` | Second_Booster | number | Total number of people who have received a second booster dose |
| `second_booster_pop_pct` | Second_Booster_Pop_Pct | number | Percentage of each age group that has received a second booster dose |

### hwk8-wu83

**COVID-19 Updated Vaccines Distributed** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/hwk8-wu83.json`
- Metadata: `GET https://data.cdc.gov/api/views/hwk8-wu83.json`; page: https://data.cdc.gov/d/hwk8-wu83
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `report date`
- Rows: 260. Data updated: 2023-10-14. Probe status: 200.
- Update frequency: R/P1D.
- Description: This site provides historical data beginning June 14, 2023, for the visualization presented on <a href="https://covid.cdc.gov/covid-data-tracker/#vaccinations">COVID-19 Data Tracker’s “Vaccinations in the United States" </a> site titled “US COVID-19 Vaccine Doses Delivered by Vaccine Type” <b>Definition for Distributed: </b> Cumulative number of COVID-19 updated vaccine doses distributed in the United States. CDC is no longer reporting metrics for Johnson & Johnson, and the original Pfizer and Moderna vaccines. Data represents all vaccine partners including jurisdictional partner clinics, ret…
- Sample row fields ($limit=1): `date`, `location`, `distributed_bivalent`, `dist_bivalent_mod`, `dist_bivalent_pfr`, `distributed_novavax`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date data are reported on CDC COVID Data Tracker (https://covid.cdc.gov/covid-data-tracker/#vaccination-states-jurisdictions) |
| `location` | Location | text | Jurisdiction (State/Territory/Federal Entity) |
| `distributed_bivalent` | Distributed_Bivalent | number | Cumulative count of updated (bivalent) Pfizer and Moderna vaccines distributed |
| `dist_bivalent_mod` | Dist_Bivalent_MOD | number | Cumulative count of updated (bivalent) Moderna doses delivered |
| `dist_bivalent_pfr` | Dist_Bivalent_PFR | number | Cumulative count of updated (bivalent) Pfizer-BioNTech doses delivered |
| `distributed_novavax` | Distributed_Novavax | number | Cumulative count of Novavax doses delivered |

### 5i5k-6cmh

**COVID-19 Vaccination Age and Sex Trends in the United States, National and Jurisdictional** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/5i5k-6cmh.json`
- Metadata: `GET https://data.cdc.gov/api/views/5i5k-6cmh.json`; page: https://data.cdc.gov/d/5i5k-6cmh
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `demographics`, `sex`, `age`, `race`, `ethnicity`
- Rows: 2,267,820. Data updated: 2023-05-12. Probe status: 200.
- Update frequency: R/P1D.
- Description: This site provides data for select demographic characteristics (age, sex, and age by sex) of people receiving COVID-19 vaccinations in the United States at the national and jurisdictional levels. For national race/ethnicity data, please visit <a href="https://data.cdc.gov/Vaccinations/COVID-19-Vaccination-Demographics-in-the-United-St/km4m-vcsb">COVID-19 Vaccination Demographics in the United States,National</a>. For jurisdictional race/ethnicity data, please visit the relevant health department website if available. Data represents all vaccine partners including jurisdictional partner clinic…
- Sample row fields ($limit=1): `date`, `location`, `demographic_category`, `census`, `administered_dose1`, `series_complete_yes`, `booster_doses`, `administered_dose1_pct_agegroup`, `series_complete_pop_pct_agegroup`, `booster_doses_vax_pct_agegroup`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date of vaccine administration |
| `location` | Location | text | Jurisdiction abbreviation (see "Jurisdiction Abbreviations" tab) |
| `demographic_category` | Demographic_Category | text | Age, sex, or age by sex group of vaccine recipient |
| `census` | census | number | 2019 Census Population |
| `administered_dose1` | Administered_Dose1 | number | Total count of people with at least one dose |
| `series_complete_yes` | Series_Complete_Yes | number | Total count of people who completed a primary series |
| `booster_doses` | Booster_Doses | number | Total count of people aged 5 years and older who completed a primary series and received a first booster dose |
| `second_booster` | Second_Booster | number | Total count of people aged 50 years and older who have received two booster doses |
| `administered_dose1_pct_agegroup` | Administered_Dose1_pct_agegroup | number | Percent of people in a demographic category with at least one dose who have information for the selected demographic category |
| `series_complete_pop_pct_agegroup` | Series_Complete_Pop_pct_agegroup | number | Percent of people in a demographic category who completed a primary series and have information for the selected demographic category |
| `booster_doses_vax_pct_agegroup` | Booster_Doses_Vax_pct_agegroup | number | Percent of people aged 5 years and older with a completed primary series in a demographic category who have received a first booster dose and have information for the selected demographic category |
| `second_booster_vax_pct_agegroup` | Second_Booster_Vax_pct_agegroup | number | Percent of people aged 50 years and older with a first booster dose who received a second booster dose and have information for the selected demographic category |

### ksfb-ug5d

**COVID-19 Vaccination Coverage, Overall and by Selected Demographics and Jurisdiction, Among Adults 18 Years and Older, by Season** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ksfb-ug5d.json`
- Metadata: `GET https://data.cdc.gov/api/views/ksfb-ug5d.json`; page: https://data.cdc.gov/d/ksfb-ug5d
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `vsd`, `iqvia`, `nis-flu`, `covid-19 vaccination`, `cms`, `iis-child`, `nis-child`, `iis-adult`
- Rows: 54,950. Data updated: 2026-03-04. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • Weekly COVID-19 Vaccination Coverage and intent among adults 18 Years and Older by Demographic Characteristics and Jurisdiction, by Season • Weekly estimates of COVID-19 vaccination coverage and intent for vaccination among adults are calculated using data from the National Immunization Surveys (NIS)-Fall Respiratory Virus Module (NIS-FRVM) (https://www.cdc.gov/nis/about/index.html). The NIS–FRVM is an ongoing random-digit-dial cellular telephone survey of households with adults 18 years and older. All estimates are based upon self-reported receipt of vaccination and month of that vaccinati…
- Sample row fields ($limit=1): `vaccine`, `geographic_level`, `geographic_name`, `demographic_level`, `demographic_name`, `indicator_label`, `indicator_category_label`, `month_week`, `week_ending`, `estimate`, `ci_half_width_95pct`, `unweighted_sample_size`, `current_season_week_ending`, `covid_season`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | Vaccine | text | COVID-19 Vaccine |
| `geographic_level` | Geographic Level | text | Geography Level (National, Region, State) |
| `geographic_name` | Geographic Name | text | Geography Name |
| `demographic_level` | Demographic Level | text | Demographic Category Level (Age, chronic conditions, disability status, health insurance, overall, poverty status, race and ethnicity, sex, sexual orientation, and urbanicity) |
| `demographic_name` | Demographic Name | text | Name of Specific Demographic (Age: 18yrs-29yrs. 18yrs-49yrs, 30yrs-39yrs, 40yrs-49yrs, 50yrs-64yrs, 60+yrs, 65+yrs, 65yrs-74yrs, 75+yrs; Chronic Conditions: Yes, No; Disability Status: Yes, No; Health Insurance: Insured, Uninsured; Overall… |
| `indicator_label` | indicator_label | text | Intention Level |
| `indicator_category_label` | indicator_category_label | text | Specific Intention Category |
| `month_week` | Month_Week | text | Month and Week |
| `week_ending` | Week_ending | calendar_date | Week Ending Date |
| `estimate` | Estimate | text | Estimate (%) |
| `ci_half_width_95pct` | CI_Half_width_95pct | text | 95% Confidence Interval Half Width |
| `unweighted_sample_size` | Unweighted Sample Size | number | Unweighted Sample Size |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | calendar_date | Current Season Week Ending Date |
| `covid_season` | COVID_season | text | COVID Season |
| `suppression_flag` | suppression_flag | number |  |

### km4m-vcsb

**COVID-19 Vaccination Demographics in the United States,National** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/km4m-vcsb.json`
- Metadata: `GET https://data.cdc.gov/api/views/km4m-vcsb.json`; page: https://data.cdc.gov/d/km4m-vcsb
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `demographics`, `sex`, `age`, `race`, `ethnicity`
- Rows: 29,886. Data updated: 2023-05-12. Probe status: 200.
- Update frequency: R/P1D.
- Source: IISInfo
- Description: Overall Demographic Characteristics of People Receiving COVID-19 Vaccinations in the United States at national level. Data represents all vaccine partners including jurisdictional partner clinics, retail pharmacies, long-term care facilities, dialysis centers, Federal Emergency Management Agency and Health Resources and Services Administration partner sites, and federal entity facilities.
- Sample row fields ($limit=1): `date`, `demographic_category`, `administered_dose1`, `administered_dose1_pct_known`, `administered_dose1_pct_us`, `series_complete_yes`, `administered_dose1_pct`, `series_complete_pop_pct`, `series_complete_pop_pct_known`, `series_complete_pop_pct_us`, `booster_doses_vax_pct_agegroup`, `booster_doses_pop_pct_known`, `booster_doses_vax_pct_us`, `booster_doses_pop_pct_known_last14days`, `booster_doses_yes`, `booster_doses_yes_last14days`, `second_booster_vax_pct_agegroup`, `second_booster_pop_pct_known`, `second_booster_pop_pct_us`, `second_booster_pop_pct_known_last14days`, `second_booster`, `second_booster_last14days`, `bivalent_booster`, `bivalent_booster_pop_pct_agegroup`, `bivalent_booster_pop_pct_known`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date data are reported on CDC COVID Data Tracker |
| `demographic_category` | Demographic_category | text | Age, sex or race/ethnicity of person receiving vaccination |
| `administered_dose1` | Administered_Dose1 | number | Total count of people with at least one dose in demographic category |
| `administered_dose1_pct_known` | Administered_Dose1_pct_known | number | Percent among persons with at least one dose who are Hispanic/Latino |
| `administered_dose1_pct_us` | Administered_Dose1_pct_US | number | Percent among persons with at least one dose, who have demographic information available on age, race/ethnicity or sex |
| `series_complete_yes` | Series_Complete_Yes | number | Total count of people who completed a primary series |
| `administered_dose1_pct` | Administered_Dose1_pct_agegroup | number | Percent among persons with at least one dose in demographic category |
| `series_complete_pop_pct` | Series_Complete_Pop_pct_agegroup | number | Percent of people in a demographic category who have completed a primary series and have information for the selected demographic category |
| `series_complete_pop_pct_known` | Series_Complete_Pop_Pct_known | number | Percent of people with a completed primary series who have known demographic information for the selected demographic category |
| `series_complete_pop_pct_us` | Series_Complete_Pop_Pct_US | number | Percent of people with a completed primary series who have known demographic information for the selected demographic category |
| `booster_doses_vax_pct_agegroup` | Booster_Doses_Vax_pct_agegroup | number | Percent of people aged 5 years and older with a completed primary series in a demographic category who have received a booster dose and have information for the selected demographic category |
| `booster_doses_pop_pct_known` | Booster_Doses_Pop_Pct_known | number | Percent of people aged 5 years and older with a completed primary series who received a booster dose and have known demographic information for the selected demographic category |
| `booster_doses_vax_pct_us` | Booster_Doses_Vax_Pct_US | number | Percent of the fully vaccinated population aged 5 years and older with a completed primary series and a booster dose who have known demographic information for the selected demographic category |
| `booster_doses_pop_pct_known_last14days` | Booster_Doses_Pop_Pct_known_Last14Days | number | Percent of population aged 5 years and older with a completed primary series and a booster dose (within the last 14 days) who have known demographic information for the selected demographic category |
| `booster_doses_yes` | Booster_Doses_Yes | number | People 12+ with a booster dose |
| `booster_doses_yes_last14days` | Booster_Doses_Yes_Last14Days | number | People 12+ with a booster dose in the last 14 days |
| `second_booster_vax_pct_agegroup` | Second_Booster_Vax_pct_agegroup | number | Percent of people aged 50 years and older in a demographic category with a first booster dose who have received a second booster dose and have information for the selected demographic category |
| `second_booster_pop_pct_known` | Second_Booster_Pop_Pct_known | number | Percent of people aged 50 years and older with a first booster who have received a second booster dose and have known demographic information for the selected demographic category |
| `second_booster_pop_pct_us` | Second_Booster_Pop_Pct_US | number | Percent of population aged 50 years and older with a completed primary series and a first booster dose who have known demographic information for the selected demographic category |
| `second_booster_pop_pct_known_last14days` | Second_Booster_Pop_Pct_known_Last14Days | number | Percent of people aged 50 years and older with a first booster who have received a second booster dose (within the last 14 days) and have known demographic information for the selected demographic category |
| `second_booster` | Second_Booster | number | Total count of people aged 50 years and older with a second booster dose |
| `second_booster_last14days` | Second_Booster_Last14Days | number | Total count of people aged 50 years and older with a second booster dose in the last 14 days |
| `bivalent_booster` | Bivalent_Booster | number | Total count of people aged 5 years and older with a bivalent booster dose |
| `bivalent_booster_pop_pct_agegroup` | Bivalent_Booster_Pop_Pct_agegroup | number | Percent of people in a demographic category who have a bivalent booster dose who have information for the selected demographic category |
| `bivalent_booster_pop_pct_known` | Bivalent_Booster_Pop_Pct_known | number | Percent of people with a bivalent booster dose who have known demographic information for the selected demographic category |

### rh2h-3yt2

**COVID-19 Vaccination Trends in the United States,National and Jurisdictional** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/rh2h-3yt2.json`
- Metadata: `GET https://data.cdc.gov/api/views/rh2h-3yt2.json`; page: https://data.cdc.gov/d/rh2h-3yt2
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `report date`
- Rows: 88,560. Data updated: 2023-05-12. Probe status: 200.
- Update frequency: R/P1D.
- Source: IISInfo
- Description: Overall Trends in Number of COVID-19 Vaccinations in the US at national and jurisdictional levels. Data represents all vaccine partners including jurisdictional partner clinics, retail pharmacies, long-term care facilities, dialysis centers, Federal Emergency Management Agency and Health Resources and Services Administration partner sites, and federal entity facilities.
- Sample row fields ($limit=1): `date`, `date_type`, `mmwr_week`, `location`, `administered_daily`, `administered_cumulative`, `admin_dose_1_daily`, `admin_dose_1_cumulative`, `administered_dose1_pop_pct`, `series_complete_daily`, `series_complete_cumulative`, `series_complete_pop_pct`, `booster_daily`, `booster_cumulative`, `additional_doses_vax_pct`, `second_booster_50plus_daily`, `second_booster_50plus_cumulative`, `second_booster_50plus_vax_pct`, `bivalent_booster_daily`, `bivalent_booster_cumulative`, `bivalent_booster_pop_pct`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date data are reported on CDC COVID Data Tracker |
| `date_type` | date_type | text | Date of administration or date reported by CDC on COVID Tracker |
| `mmwr_week` | MMWR_week | number | The week of the epidemiologic year as defined by the Morbidity and Mortality Weekly Report (https://ndc.services.cdc.gov/wp-content/uploads/MMWR_week_overview.pdf). |
| `location` | Location | text | State/Territory/Federal Entity |
| `administered_daily` | Administered_Daily | number | Total number of administered doses by date of administration. |
| `administered_cumulative` | Administered_Cumulative | number | Cumulative number of reported doses administered by date of administration |
| `administered_7_day_rolling` | Administered_7_Day_Rolling_Average | number | 7-day moving average of the daily doses administered by date of administration |
| `admin_dose_1_daily` | Admin_Dose_1_Daily | number | Total number of dose 1 administations by date of administration |
| `admin_dose_1_cumulative` | Admin_Dose_1_Cumulative | number | Cumulative number of people with at least one dose of any vaccine by date of administration. |
| `admin_dose_1_day_rolling` | Admin_Dose_1_Day_Rolling_Average | number | 7-day moving average count of people with at least one dose of any vaccine by date of administration |
| `administered_dose1_pop_pct` | Administered_Dose1_Pop_Pct | number | Percent of population with at least one dose based on the jurisdiction where recipient lives |
| `administered_daily_change` | Administered_daily_change_report | number | Change between the cumulative number of doses administered on a given day and the previous day by date of report |
| `administered_daily_change_1` | Administered_daily_change_report_7dayroll | number | 7-day moving average of the daily change based by date of report |
| `series_complete_daily` | Series_Complete_Daily | number | Daily total count of people with a completed primary series by date of administration |
| `series_complete_cumulative` | Series_Complete_Cumulative | number | Cumulative total of people with a completed primary series by date of administration |
| `series_complete_day_rolling` | Series_Complete_Day_Rolling_Average | number | 7-day moving average count of people with a completed primary series by date of administration |
| `series_complete_pop_pct` | Series_Complete_Pop_Pct | number | Percent of people with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `booster_daily` | Booster_Daily | number | Daily total count of people who have completed a primary series and have received a booster (or additional) dose by date of administration |
| `booster_cumulative` | Booster_Cumulative | number | Cumulative total of people who have completed a primary series and have received a booster (or additional) dose by date of administration |
| `booster_7_day_rolling_average` | Booster_7_Day_Rolling_Average | number | 7-day moving average count of people who have completed a primary series and have received a booster (or additional) dose by date of administration |
| `additional_doses_vax_pct` | Additional_Doses_Vax_Pct | number | Percent of people who have completed a primary series and have received a booster (or additional) dose. |
| `second_booster_50plus_daily` | Second_Booster_50Plus_Daily | number | Daily count of people ages 50+ receiving a second booster dose |
| `second_booster_50plus_cumulative` | Second_Booster_50Plus_Cumulative | number | Cumulative total of people ages 50+ who have received a second booster dose |
| `second_booster_50plus_7_day_rolling_average` | Second_Booster_50Plus_7_Day_Rolling_Average | number | 7-day moving average count of people ages 50+ who have received a second booster dose |
| `second_booster_50plus_vax_pct` | Second_Booster_50Plus_Vax_Pct | number | Percent of people ages 50+ with a first booster dose who received a second booster dose |
| `bivalent_booster_daily` | Bivalent_Booster_Daily | text | Total number of administered bivalent booster doses by date of administration |
| `bivalent_booster_cumulative` | Bivalent_Booster_Cumulative | text | Cumulative number of reported bivalent booster doses administered by date of administration |
| `bivalent_booster_7_day_rolling_average` | Bivalent_Booster_7_Day_Rolling_Average | text | 7-day moving average of the daily bivalent booster doses administered by date of administration |
| `bivalent_booster_pop_pct` | Bivalent_Booster_Pop_Pct | text | Percent of population with a bivalent booster dose based on the jurisdiction where recipient lives |

### 8xkx-amqh

**COVID-19 Vaccinations in the United States,County** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8xkx-amqh.json`
- Metadata: `GET https://data.cdc.gov/api/views/8xkx-amqh.json`; page: https://data.cdc.gov/d/8xkx-amqh
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `age`
- Rows: 1,962,781. Data updated: 2023-05-12. Probe status: 200.
- Update frequency: R/P1D.
- Source: IISInfo
- Description: Overall US COVID-19 Vaccine administration and vaccine equity data at county level. Data represents all vaccine partners including jurisdictional partner clinics, retail pharmacies, long-term care facilities, dialysis centers, Federal Emergency Management Agency and Health Resources and Services Administration partner sites, and federal entity facilities.
- Sample row fields ($limit=1): `date`, `fips`, `mmwr_week`, `recip_county`, `recip_state`, `completeness_pct`, `administered_dose1_recip`, `administered_dose1_pop_pct`, `administered_dose1_recip_5plus`, `administered_dose1_recip_5pluspop_pct`, `administered_dose1_recip_12plus`, `administered_dose1_recip_12pluspop_pct`, `administered_dose1_recip_18plus`, `administered_dose1_recip_18pluspop_pct`, `administered_dose1_recip_65plus`, `administered_dose1_recip_65pluspop_pct`, `series_complete_yes`, `series_complete_pop_pct`, `series_complete_5plus`, `series_complete_5pluspop_pct`, `series_complete_5to17`, `series_complete_5to17pop_pct`, `series_complete_12plus`, `series_complete_12pluspop_pct`, `series_complete_18plus`, `series_complete_18pluspop_pct`, `series_complete_65plus`, `series_complete_65pluspop_pct`, `booster_doses`, `booster_doses_vax_pct`, `booster_doses_5plus`, `booster_doses_5plus_vax_pct`, `booster_doses_12plus`, `booster_doses_12plus_vax_pct`, `booster_doses_18plus`, `booster_doses_18plus_vax_pct`, `booster_doses_50plus`, `booster_doses_50plus_vax_pct`, `booster_doses_65plus`, `booster_doses_65plus_vax_pct`, `second_booster_50plus`, `second_booster_50plus_vax_pct`, `second_booster_65plus`, `second_booster_65plus_vax_pct`, `svi_ctgy`, `series_complete_pop_pct_svi`, `series_complete_5pluspop_pct_svi`, `series_complete_5to17pop_pct_svi`, `series_complete_12pluspop_pct_svi`, `series_complete_18pluspop_pct_svi`, `series_complete_65pluspop_pct_svi`, `metro_status`, `series_complete_pop_pct_ur_equity`, `series_complete_5pluspop_pct_ur_equity`, `series_complete_5to17pop_pct_ur_equity`, `series_complete_12pluspop_pct_ur_equity`, `series_complete_18pluspop_pct_ur_equity`, `series_complete_65pluspop_pct_ur_equity`, `booster_doses_vax_pct_svi`, `booster_doses_12plusvax_pct_svi`, `booster_doses_18plusvax_pct_svi`, `booster_doses_65plusvax_pct_svi`, `booster_doses_vax_pct_ur_equity`, `booster_doses_12plusvax_pct_ur_equity`, `booster_doses_18plusvax_pct_ur_equity`, `booster_doses_65plusvax_pct_ur_equity`, `census2019`, `census2019_5pluspop`, `census2019_5to17pop`, `census2019_12pluspop`, `census2019_18pluspop`, `census2019_65pluspop`, `bivalent_booster_5plus`, `bivalent_booster_5plus_pop_pct`, `bivalent_booster_12plus`, `bivalent_booster_12plus_pop_pct`, `bivalent_booster_18plus`, `bivalent_booster_18plus_pop_pct`, `bivalent_booster_65plus`, `bivalent_booster_65plus_pop_pct`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date data are reported on CDC COVID Data Tracker |
| `fips` | FIPS | text | Federal Information Processing Standard State Code |
| `mmwr_week` | MMWR_week | number | MMWR Week |
| `recip_county` | Recip_County | text | County of residence |
| `recip_state` | Recip_State | text | Recipient State |
| `completeness_pct` | Completeness_pct | number | Represents the proportion of people with a completed primary series whose Federal Information Processing Standards (FIPS) code is reported and matches a valid county FIPS code in the jurisdiction. |
| `administered_dose1_recip` | Administered_Dose1_Recip | number | People with at least one Dose by State of Residence |
| `administered_dose1_pop_pct` | Administered_Dose1_Pop_Pct | number | Percent of Total Pop with at least one Dose by State of Residence |
| `administered_dose1_recip_5plus` | Administered_Dose1_Recip_5Plus | number | Total number of people 5+ with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_recip_5pluspop_pct` | Administered_Dose1_Recip_5PlusPop_Pct | number | Percent of 5+ population with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_recip_12plus` | Administered_Dose1_Recip_12Plus | number | People 12+ with at least one Dose by State of Residence |
| `administered_dose1_recip_12pluspop_pct` | Administered_Dose1_Recip_12PlusPop_Pct | number | Percent of 12+ Pop with at least one Dose by State of Residence |
| `administered_dose1_recip_18plus` | Administered_Dose1_Recip_18Plus | number | People 18+ with at least one Dose by State of Residence |
| `administered_dose1_recip_18pluspop_pct` | Administered_Dose1_Recip_18PlusPop_Pct | number | Percent of 18+ Pop with at least one Dose by State of Residence |
| `administered_dose1_recip_65plus` | Administered_Dose1_Recip_65Plus | number | People 65+ with at least one Dose by State of Residence |
| `administered_dose1_recip_65pluspop_pct` | Administered_Dose1_Recip_65PlusPop_Pct | number | Percent of 65+ Pop with at least one Dose by State of Residence |
| `series_complete_yes` | Series_Complete_Yes | number | Total number of people who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction and county where vaccine recipient lives |
| `series_complete_pop_pct` | Series_Complete_Pop_Pct | number | Percent of people who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction and county where vaccine recipient lives |
| `series_complete_5plus` | Series_Complete_5Plus | number | Total number of people ages 5+ who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_5pluspop_pct` | Series_Complete_5PlusPop_Pct | number | Percent of people ages 5+ who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_5to17` | Series_Complete_5to17 | number | Total number of people ages 5-17 years who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_5to17pop_pct` | Series_Complete_5to17Pop_Pct | number | Percent of people ages 5-17 years who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_12plus` | Series_Complete_12Plus | number | Total number of people ages 12+ who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction and county where vaccine recipient lives |
| `series_complete_12pluspop_pct` | Series_Complete_12PlusPop_Pct | number | Percent of people ages 12+ who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction and county where vaccine recipient lives |
| `series_complete_18plus` | Series_Complete_18Plus | number | Total number of people ages 18+ who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction and county where vaccine recipient lives |
| `series_complete_18pluspop_pct` | Series_Complete_18PlusPop_Pct | number | Percent of people ages 18+ who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction and county where vaccine recipient lives |
| `series_complete_65plus` | Series_Complete_65Plus | number | Total number of people ages 65+ who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where vaccine recipient lives |
| `series_complete_65pluspop_pct` | Series_Complete_65PlusPop_Pct | number | Percent of people ages 65+ who have completed a primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where vaccine recipient lives |
| `booster_doses` | Booster_Doses | number | Total number of people who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_vax_pct` | Booster_Doses_Vax_Pct | number | Percent of people who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_5plus` | Booster_Doses_5Plus | number | Total number of people ages 5+ who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_5plus_vax_pct` | Booster_Doses_5Plus_Vax_Pct | number | Percent of people ages 5+ who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_12plus` | Booster_Doses_12Plus | number | Total number of people ages 12+ who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_12plus_vax_pct` | Booster_Doses_12Plus_Vax_Pct | number | Percent of people ages 12+ who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_18plus` | Booster_Doses_18Plus | number | Total number of people ages 18+ who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_18plus_vax_pct` | Booster_Doses_18Plus_Vax_Pct | number | Percent of people ages 18+ who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_50plus` | Booster_Doses_50Plus | number | Total number of people ages 50+ who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_50plus_vax_pct` | Booster_Doses_50Plus_Vax_Pct | number | Percent of people ages 50+ who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_65plus` | Booster_Doses_65Plus | number | Total number of people ages 65+ who completed a primary series and have received a booster (or additional) dose. |
| `booster_doses_65plus_vax_pct` | Booster_Doses_65Plus_Vax_Pct | number | Percent of people ages 65+ who completed a primary series and have received a booster (or additional) dose. |
| `second_booster_50plus` | Second_Booster_50Plus | text | Total number of people ages 50+ who have received a second booster dose. |
| `second_booster_50plus_vax_pct` | Second_Booster_50Plus_Vax_Pct | text | Percentage of people ages 50+ with a first booster dose who received a second booster dose. |
| `second_booster_65plus` | Second_Booster_65Plus | text | Total number of people ages 65+ who have received a second booster dose. |
| `second_booster_65plus_vax_pct` | Second_Booster_65Plus_Vax_Pct | text | Percentage of people ages 65+ with a first booster dose who received a second booster dose. |
| `svi_ctgy` | SVI_CTGY | text | SVI |
| `series_complete_pop_pct_svi` | Series_Complete_Pop_Pct_SVI | number | Percent of Population Fully Vaccinated/SVI |
| `series_complete_5pluspop_pct_svi` | Series_Complete_5PlusPop_Pct_SVI | number | Percent of 5+ Pop Fully Vaccinated/SVI |
| `series_complete_5to17pop_pct_svi` | Series_Complete_5to17Pop_Pct_SVI | number | Percent of 5-17 Pop Fully Vaccinated/SVI |
| `series_complete_12pluspop_pct_svi` | Series_Complete_12PlusPop_Pct_SVI | number | Percent of 12+ Pop Fully Vaccinated/SVI |
| `series_complete_18pluspop_pct_svi` | Series_Complete_18PlusPop_Pct_SVI | number | Percent of 18+ Pop Fully Vaccinated/SVI |
| `series_complete_65pluspop_pct_svi` | Series_Complete_65PlusPop_Pct_SVI | number | Percent of 65+ Pop Fully Vaccinated/SVI |
| `metro_status` | Metro_status | text | Metro/Non-metro |
| `series_complete_pop_pct_ur_equity` | Series_Complete_Pop_Pct_UR_Equity | number | Percent of Population Fully Vaccinated/MetroNon-Metro |
| `series_complete_5pluspop_pct_ur_equity` | Series_Complete_5PlusPop_Pct_UR_Equity | number | Percent of 5+ Pop Fully Vaccinated/MetroNon-Metro |
| `series_complete_5to17pop_pct_ur_equity` | Series_Complete_5to17Pop_Pct_UR_Equity | number | Percent of 5-17 Pop Fully Vaccinated/MetroNon-Metro |
| `series_complete_12pluspop_pct_ur_equity` | Series_Complete_12PlusPop_Pct_UR_Equity | number | Percent of 12+ Pop Fully Vaccinated/MetroNon-Metro |
| `series_complete_18pluspop_pct_ur_equity` | Series_Complete_18PlusPop_Pct_UR_Equity | number | Percent of 18+ Pop Fully Vaccinated/MetroNon-Metro |
| `series_complete_65pluspop_pct_ur_equity` | Series_Complete_65PlusPop_Pct_UR_Equity | number | Percent of 65+ Pop Fully Vaccinated/MetroNon-Metro |
| `booster_doses_vax_pct_svi` | Booster_Doses_Vax_Pct_SVI | number | Percent of Pop Fully Vaccinated with Booster Dose/SVI |
| `booster_doses_12plusvax_pct_svi` | Booster_Doses_12PlusVax_Pct_SVI | number | Percent of 12+ Pop Fully Vaccinated with Booster Dose/SVI |
| `booster_doses_18plusvax_pct_svi` | Booster_Doses_18PlusVax_Pct_SVI | number | Percent of 18+ Pop Fully Vaccinated with Booster Dose/SVI |
| `booster_doses_65plusvax_pct_svi` | Booster_Doses_65PlusVax_Pct_SVI | number | Percent of 65+ Pop Fully Vaccinated with Booster Dose/SVI |
| `booster_doses_vax_pct_ur_equity` | Booster_Doses_Vax_Pct_UR_Equity | number | Percent of Population Fully Vaccinated with Booster Dose/MetroNon-Metro |
| `booster_doses_12plusvax_pct_ur_equity` | Booster_Doses_12PlusVax_Pct_UR_Equity | number | Percent of 12+ Pop Fully Vaccinated with Booster Dose/MetroNon-Metro |
| `booster_doses_18plusvax_pct_ur_equity` | Booster_Doses_18PlusVax_Pct_UR_Equity | number | Percent of 18+ Pop Fully Vaccinated with Booster Dose/MetroNon-Metro |
| `booster_doses_65plusvax_pct_ur_equity` | Booster_Doses_65PlusVax_Pct_UR_Equity | number | Percent of 65+ Pop Fully Vaccinated with Booster Dose/MetroNon-Metro |
| `census2019` | Census2019 | number | 2019 Census Population |
| `census2019_5pluspop` | Census2019_5PlusPop | number | 2019 Census Population for ≥5 years of age |
| `census2019_5to17pop` | Census2019_5to17Pop | number | 2019 Census Population for 5-17 years of age |
| `census2019_12pluspop` | Census2019_12PlusPop | number | 2019 Census Population for ≥12 years of age |
| `census2019_18pluspop` | Census2019_18PlusPop | number | 2019 Census Population for ≥18 years of age |
| `census2019_65pluspop` | Census2019_65PlusPop | number | 2019 Census Population for ≥65 years of age |
| `bivalent_booster_5plus` | Bivalent_Booster_5Plus | number | Total number of people ages 5+ with an updated (bivalent) booster dose |
| `bivalent_booster_5plus_pop_pct` | Bivalent_Booster_5Plus_Pop_Pct | number | Percent of people ages 5+ with an updated (bivalent) booster dose |
| `bivalent_booster_12plus` | Bivalent_Booster_12Plus | number | Total number of people ages 12+ with an updated (bivalent) booster dose |
| `bivalent_booster_12plus_pop_pct` | Bivalent_Booster_12Plus_Pop_Pct | number | Percent of people ages 12+ with an updated (bivalent) booster dose |
| `bivalent_booster_18plus` | Bivalent_Booster_18Plus | number | Total number of people ages 18+ with an updated (bivalent) booster dose |
| `bivalent_booster_18plus_pop_pct` | Bivalent_Booster_18Plus_Pop_Pct | number | Percent of people ages 18+ with an updated (bivalent) booster dose |
| `bivalent_booster_65plus` | Bivalent_Booster_65Plus | number | Total number of people ages 65+ with an updated (bivalent) booster dose |
| `bivalent_booster_65plus_pop_pct` | Bivalent_Booster_65Plus_Pop_Pct | number | Percent of people ages 65+ with an updated (bivalent) booster dose |

### unsk-b7fc

**COVID-19 Vaccinations in the United States,Jurisdiction** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/unsk-b7fc.json`
- Metadata: `GET https://data.cdc.gov/api/views/unsk-b7fc.json`; page: https://data.cdc.gov/d/unsk-b7fc
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `age`
- Rows: 38,488. Data updated: 2023-05-12. Probe status: 200.
- Update frequency: R/P1D.
- Source: IISInfo
- Description: Overall US COVID-19 Vaccine deliveries and administration data at national and jurisdiction level. Data represents all vaccine partners including jurisdictional partner clinics, retail pharmacies, long-term care facilities, dialysis centers, Federal Emergency Management Agency and Health Resources and Services Administration partner sites, and federal entity facilities.
- Sample row fields ($limit=1): `date`, `mmwr_week`, `location`, `distributed`, `distributed_janssen`, `distributed_moderna`, `distributed_pfizer`, `distributed_unk_manuf`, `dist_per_100k`, `distributed_per_100k_12plus`, `distributed_per_100k_18plus`, `distributed_per_100k_65plus`, `administered`, `administered_12plus`, `administered_18plus`, `administered_65plus`, `administered_janssen`, `administered_moderna`, `administered_pfizer`, `administered_unk_manuf`, `admin_per_100k`, `admin_per_100k_12plus`, `admin_per_100k_18plus`, `admin_per_100k_65plus`, `recip_administered`, `administered_dose1_recip`, `administered_dose1_pop_pct`, `administered_dose1_recip_12plus`, `administered_dose1_recip_12pluspop_pct`, `administered_dose1_recip_18plus`, `administered_dose1_recip_18pluspop_pct`, `administered_dose1_recip_65plus`, `administered_dose1_recip_65pluspop_pct`, `series_complete_yes`, `series_complete_pop_pct`, `series_complete_12plus`, `series_complete_12pluspop`, `series_complete_18plus`, `series_complete_18pluspop`, `series_complete_65plus`, `series_complete_65pluspop`, `series_complete_janssen`, `series_complete_moderna`, `series_complete_pfizer`, `series_complete_unk_manuf`, `series_complete_janssen_12plus`, `series_complete_moderna_12plus`, `series_complete_pfizer_12plus`, `series_complete_unk_manuf_1`, `series_complete_janssen_18plus`, `series_complete_moderna_18plus`, `series_complete_pfizer_18plus`, `series_complete_unk_manuf_2`, `series_complete_janssen_65plus`, `series_complete_moderna_65plus`, `series_complete_pfizer_65plus`, `series_complete_unk_manuf_3`, `additional_doses`, `additional_doses_vax_pct`, `additional_doses_18plus`, `additional_doses_18plus_vax_pct`, `additional_doses_50plus`, `additional_doses_50plus_vax_pct`, `additional_doses_65plus`, `additional_doses_65plus_vax_pct`, `additional_doses_moderna`, `additional_doses_pfizer`, `additional_doses_janssen`, `additional_doses_unk_manuf`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date data are reported on CDC COVID Data Tracker (https://covid.cdc.gov/covid-data-tracker/#vaccinations) |
| `mmwr_week` | MMWR_week | number | The week of the epidemiologic year as defined by the Morbidity and Mortality Weekly Report (https://ndc.services.cdc.gov/wp-content/uploads/MMWR_week_overview.pdf). |
| `location` | Location | text | Jurisdiction (State/Territory/Federal Entity) |
| `distributed` | Distributed | number | Total number of delivered doses |
| `distributed_janssen` | Distributed_Janssen | number | Total number of J&J/Janssen doses delivered |
| `distributed_moderna` | Distributed_Moderna | number | Total number of Moderna doses delivered |
| `distributed_pfizer` | Distributed_Pfizer | number | Total number of Pfizer-BioNTech doses delivered |
| `distributed_novavax` | Distributed_Novavax | number | Total number of Novavax doses delivered |
| `distributed_unk_manuf` | Distributed_Unk_Manuf | number | Total number of doses delivered from other manufacturers |
| `dist_per_100k` | Dist_Per_100K | number | Delivered doses per 100,000 census population |
| `distributed_per_100k_5plus` | Distributed_Per_100k_5Plus | number | Total number of doses delivered per 100,000 people ages 5+ |
| `distributed_per_100k_12plus` | Distributed_Per_100k_12Plus | number | Total number of doses delivered per 100,000 people ages 12+ |
| `distributed_per_100k_18plus` | Distributed_Per_100k_18Plus | number | Total number of doses delivered per 100,000 people ages 18+ |
| `distributed_per_100k_65plus` | Distributed_Per_100k_65Plus | number | Total number of doses delivered per 100,000 people ages 65+ |
| `administered` | Administered | number | Total number of administered doses based on the jurisdiction (state/territory) where administered |
| `administered_5plus` | Administered_5Plus | number | Total number of doses administered to people ages 5+ based on the jurisdiction where administered |
| `administered_12plus` | Administered_12Plus | number | Total number of doses administered to people ages 12+ based on the jurisdiction where administered |
| `administered_18plus` | Administered_18Plus | number | Total number of doses administered to people ages 18+ based on the jurisdiction where administered |
| `administered_65plus` | Administered_65Plus | number | Total number of doses administered to people ages 65+ based on the jurisdiction where administered |
| `administered_janssen` | Administered_Janssen | number | Total number of J&J/Janssen doses administered |
| `administered_moderna` | Administered_Moderna | number | Total number of Moderna doses administered |
| `administered_pfizer` | Administered_Pfizer | number | Total number of Pfizer-BioNTech doses administered |
| `administered_novavax` | Administered_Novavax | number | Total number of Novavax doses administered |
| `administered_unk_manuf` | Administered_Unk_Manuf | number | Total number of administered doses from other manufacturers |
| `admin_per_100k` | Admin_Per_100K | number | Total number of doses administered per 100,000 census population based on the jurisdiction where recipient lives |
| `admin_per_100k_5plus` | Admin_Per_100k_5Plus | number | Total number of doses administered per 100,000 people ages 5+ |
| `admin_per_100k_12plus` | Admin_Per_100k_12Plus | number | Total number of doses administered per 100,000 people ages 12+ |
| `admin_per_100k_18plus` | Admin_Per_100k_18Plus | number | Total number of doses administered per 100,000 people ages 18+ |
| `admin_per_100k_65plus` | Admin_Per_100k_65Plus | number | Total number of doses administered per 100,000 people ages 65+ |
| `recip_administered` | Recip_Administered | number | Total number of doses administered based on the jurisdiction where recipient lives |
| `administered_dose1_recip` | Administered_Dose1_Recip | number | Total number of people with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_pop_pct` | Administered_Dose1_Pop_Pct | number | Percent of population with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_recip_5plus` | Administered_Dose1_Recip_5Plus | number | Total number of people ages 5+ with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_recip_5pluspop_pct` | Administered_Dose1_Recip_5PlusPop_Pct | number | Percent of population ages 5+ with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_recip_12plus` | Administered_Dose1_Recip_12Plus | number | Total number of people ages 12+ with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_recip_12pluspop_pct` | Administered_Dose1_Recip_12PlusPop_Pct | number | Percent of population ages 12+ with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_recip_18plus` | Administered_Dose1_Recip_18Plus | number | Total number of people ages 18+ with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_recip_18pluspop_pct` | Administered_Dose1_Recip_18PlusPop_Pct | number | Percent of population ages 18+ with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_recip_65plus` | Administered_Dose1_Recip_65Plus | number | Total number of people ages 65+ with at least one dose based on the jurisdiction where recipient lives |
| `administered_dose1_recip_65pluspop_pct` | Administered_Dose1_Recip_65PlusPop_Pct | number | Percent of population ages 65+ with at least one dose based on the jurisdiction where recipient lives |
| `series_complete_yes` | Series_Complete_Yes | number | Total number of people with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_pop_pct` | Series_Complete_Pop_Pct | number | Percent of people with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_5plus` | Series_Complete_5Plus | number | Total number of people 5+ with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_5pluspop_pct` | Series_Complete_5PlusPop_Pct | number | Percent of people 5+ with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_12plus` | Series_Complete_12Plus | number | Total number of people 12+ with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_12pluspop` | Series_Complete_12PlusPop_Pct | number | Percent of people 12+ with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_18plus` | Series_Complete_18Plus | number | Total number of people 18+ with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_18pluspop` | Series_Complete_18PlusPop_Pct | number | Percent of people 18+ with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_65plus` | Series_Complete_65Plus | number | Total number of people 65+ with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_65pluspop` | Series_Complete_65PlusPop_Pct | number | Percent of people 65+ with a completed primary series (have second dose of a two-dose vaccine or one dose of a single-dose vaccine) based on the jurisdiction where recipient lives |
| `series_complete_janssen` | Series_Complete_Janssen | number | Total number of people with the J&J/Janssen vaccine |
| `series_complete_moderna` | Series_Complete_Moderna | number | Total number of people who completed a Moderna primary series |
| `series_complete_pfizer` | Series_Complete_Pfizer | number | Total number of people who completed a Pfizer primary series |
| `series_complete_novavax` | Series_Complete_Novavax | number | Total number of people who completed a Novavax primary series |
| `series_complete_unk_manuf` | Series_Complete_Unk_Manuf | number | Total number of people who received two primary series doses from an unknown or other two-dose vaccine manufacturer |
| `series_complete_janssen_5plus` | Series_Complete_Janssen_5Plus | number | Total number of people 5+ with the J&J/Janssen vaccine |
| `series_complete_moderna_5plus` | Series_Complete_Moderna_5Plus | number | Total number of people 5+ who completed a Moderna primary series |
| `series_complete_pfizer_5plus` | Series_Complete_Pfizer_5Plus | number | Total number of people 5+ who completed a Pfizer primary series |
| `series_complete_unk_manuf_5plus` | Series_Complete_Unk_Manuf_5Plus | number | Total number of people 5+ who received two primary series doses from an unknown or other two-dose vaccine manufacturer |
| `series_complete_janssen_12plus` | Series_Complete_Janssen_12Plus | number | Total number of people 12+ with the J&J/Janssen vaccine |
| `series_complete_moderna_12plus` | Series_Complete_Moderna_12Plus | number | Total number of people 12+ who completed a Moderna primary series |
| `series_complete_pfizer_12plus` | Series_Complete_Pfizer_12Plus | number | Total number of people 12+ who completed a Pfizer primary series |
| `series_complete_unk_manuf_1` | Series_Complete_Unk_Manuf_12Plus | number | Total number of people 12+ who received two primary series doses from an unknown or other two-dose vaccine manufacturer |
| `series_complete_janssen_18plus` | Series_Complete_Janssen_18Plus | number | Total number of people 18+ with the J&J/Janssen vaccine. |
| `series_complete_moderna_18plus` | Series_Complete_Moderna_18Plus | number | Total number of people 18+ who completed a Moderna primary series |
| `series_complete_pfizer_18plus` | Series_Complete_Pfizer_18Plus | number | Total number of people 18+ who completed a Pfizer primary series |
| `series_complete_unk_manuf_2` | Series_Complete_Unk_Manuf_18Plus | number | Total number of people 18+ who received two doses from an unknown or other two-dose vaccine manufacturer |
| `series_complete_janssen_65plus` | Series_Complete_Janssen_65Plus | number | Total number of people 65+ with the J&J/Janssen vaccine. |
| `series_complete_moderna_65plus` | Series_Complete_Moderna_65Plus | number | Total number of people 65+ who completed a Moderna primary series |
| `series_complete_pfizer_65plus` | Series_Complete_Pfizer_65Plus | number | Total number of people 65+ who completed a Pfizer primary series |
| `series_complete_unk_manuf_3` | Series_Complete_Unk_Manuf_65Plus | number | Total number of people 65+ who received two doses from an unknown or other two-dose vaccine manufacturer. |
| `additional_doses` | Additional_Doses | number | Total number of people who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_vax_pct` | Additional_Doses_Vax_Pct | number | Percent of people who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_5plus` | Additional_Doses_5Plus | number | Total number of people 5+ who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_5plus_vax_pct` | Additional_Doses_5Plus_Vax_Pct | number | Percent of people 5+ who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_12plus` | Additional_Doses_12Plus | number | Total number of people 12+ who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_12plus_vax_pct` | Additional_Doses_12Plus_Vax_Pct | number | Percent of people 12+ who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_18plus` | Additional_Doses_18Plus | number | Total number of people 18+ who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_18plus_vax_pct` | Additional_Doses_18Plus_Vax_Pct | number | Percent of people 18+ who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_50plus` | Additional_Doses_50Plus | number | Total number of people 50+ who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_50plus_vax_pct` | Additional_Doses_50Plus_Vax_Pct | number | Percent of people 50+ who completed a primary series and have received a booster (or additiuonal) dose. |
| `additional_doses_65plus` | Additional_Doses_65Plus | number | Total number of people 65+ who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_65plus_vax_pct` | Additional_Doses_65Plus_Vax_Pct | number | Percent of people 65+ who completed a primary series and have received a booster (or additional) dose. |
| `additional_doses_moderna` | Additional_Doses_Moderna | number | Total number of people with a completed primary series who have received a Moderna booster (or additional) dose. |
| `additional_doses_pfizer` | Additional_Doses_Pfizer | number | Total number of people with a completed primary series who have received a Pfizer booster (or additional) dose. |
| `additional_doses_janssen` | Additional_Doses_Janssen | number | Total number of people with a completed primary series who have received a Janssen booster (or additional) dose. |
| `additional_doses_unk_manuf` | Additional_Doses_Unk_Manuf | number | Total number of people with a completed primary series who have received an unknown or other booster (or additional) dose. |
| `second_booster` | Second_Booster | number | Total number of people who have received a second booster dose in the US |
| `second_booster_50plus` | Second_Booster_50Plus | number | Total number of people ages 50+ who have received a second booster dose based on the jurisdiction where recipient lives |
| `second_booster_50plus_vax_pct` | Second_Booster_50Plus_Vax_Pct | number | Percentage of people ages 50+ with a first booster dose who received a second booster dose based on the jurisdiction where recipient lives |
| `second_booster_65plus` | Second_Booster_65Plus | number | Total number of people ages 65+ who have received a second booster dose based on the jurisdiction where recipient lives |
| `second_booster_65plus_vax_pct` | Second_Booster_65Plus_Vax_Pct | number | Percentage of people ages 65+ with a first booster dose who received a second booster dose based on the jurisdiction where recipient lives |
| `second_booster_janssen` | Second_Booster_Janssen | number | Total number of people who have received a second booster dose manufactured by J&J/Janssen |
| `second_booster_moderna` | Second_Booster_Moderna | number | Total number of people who have received a second booster dose manufactured by Moderna |
| `second_booster_pfizer` | Second_Booster_Pfizer | number | Total number of people who have received a second booster dose manufactured by Pfizer-BioNTech |
| `second_booster_unk_manuf` | Second_Booster_Unk_Manuf | number | Total number of people who have received a second booster dose from another manufacturer |
| `administered_bivalent` | Administered_Bivalent | number | Total number of people who have received an updated (bivalent) booster dose since September 1, 2022 |
| `admin_bivalent_pfr` | Admin_Bivalent_PFR | number | Total number of updated (bivalent) Pfizer booster doses administered |
| `admin_bivalent_mod` | Admin_Bivalent_MOD | number | Total number of updated (bivalent) Moderna booster doses administered |
| `dist_bivalent_pfr` | Dist_Bivalent_PFR | number | Total number of updated (bivalent) Pfizer booster doses distributed |
| `dist_bivalent_mod` | Dist_Bivalent_MOD | number | Total number of updated (bivalent) Moderna booster doses distributed |
| `bivalent_booster_5plus` | Bivalent_Booster_5Plus | number | Total number of people ages 5+ with an updated (bivalent) booster dose |
| `bivalent_booster_5plus_pop_pct` | Bivalent_Booster_5Plus_Pop_Pct | number | Percent of people ages 5+ with an updated (bivalent) booster dose |
| `bivalent_booster_12plus` | Bivalent_Booster_12Plus | number | Total number of people ages 12+ with an updated (bivalent) booster dose |
| `bivalent_booster_12plus_pop_pct` | Bivalent_Booster_12Plus_Pop_Pct | number | Percent of people ages 12+ with an updated (bivalent) booster dose |
| `bivalent_booster_18plus` | Bivalent_Booster_18Plus | number | Total number of people ages 18+ with an updated (bivalent) booster dose |
| `bivalent_booster_18plus_pop_pct` | Bivalent_Booster_18Plus_Pop_Pct | number | Percent of people ages 18+ with an updated (bivalent) booster dose |
| `bivalent_booster_65plus` | Bivalent_Booster_65Plus | number | Total number of people ages 65+ with an updated (bivalent) booster dose |
| `bivalent_booster_65plus_pop_pct` | Bivalent_Booster_65Plus_Pop_Pct | number | Percent of people ages 65+ with an updated (bivalent) booster dose |

### w9zu-fywh

**COVID-19 Vaccine Distribution Allocations by Jurisdiction - Janssen** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/w9zu-fywh.json`
- Metadata: `GET https://data.cdc.gov/api/views/w9zu-fywh.json`; page: https://data.cdc.gov/d/w9zu-fywh
- Topics: Category: Vaccinations
- Tags: `covid-19`, `vaccination`, `coronavirus`
- Rows: 504. Data updated: 2021-05-05. Probe status: 200.
- Update frequency: Weekly (Tuesday).
- Source: HHS ASPA
- Description: New weekly allocations of doses are posted every Tuesday. Beginning the following Thursday, states can begin ordering doses from that week’s new allocation of 1st doses. Beginning two weeks (Pfizer) or three weeks (Moderna) from the following Sunday, states can begin ordering doses from that week’s new allocation of 2nd doses. After doses are ordered by states, shipments begin the following Monday. The entire order may not arrive in one shipment or on one day, but over the course of the week. Second doses are opened up for orders on Sundays, at the appropriate interval two or three weeks late…
- Sample row fields ($limit=1): `jurisdiction`, `week_of_allocations`, `_1st_dose_allocations`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `jurisdiction` | Jurisdiction | text | City, State, Territory |
| `week_of_allocations` | Week of Allocations | calendar_date | Week that vaccines are allocated to a jurisdiction |
| `_1st_dose_allocations` | 1st Dose Allocations | number | Number of 1st dose allocations that a jurisdiction can order from |

### b7pe-5nws

**COVID-19 Vaccine Distribution Allocations by Jurisdiction - Moderna** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/b7pe-5nws.json`
- Metadata: `GET https://data.cdc.gov/api/views/b7pe-5nws.json`; page: https://data.cdc.gov/d/b7pe-5nws
- Topics: Category: Vaccinations
- Tags: `covid-19`, `vaccination`, `coronavirus`
- Rows: 1,701. Data updated: 2021-06-17. Probe status: 200.
- Update frequency: Weekly (Tuesday).
- Source: HHS ASPA
- Description: New weekly allocations of doses are posted every Tuesday. Beginning the following Thursday, states can begin ordering doses from that week’s new allocation of 1st doses. Beginning two weeks (Pfizer) or three weeks (Moderna) from the following Sunday, states can begin ordering doses from that week’s new allocation of 2nd doses. After doses are ordered by states, shipments begin the following Monday. The entire order may not arrive in one shipment or on one day, but over the course of the week. Second doses are opened up for orders on Sundays, at the appropriate interval two or three weeks late…
- Sample row fields ($limit=1): `jurisdiction`, `week_of_allocations`, `_1st_dose_allocations`, `_2nd_dose_allocations`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `jurisdiction` | Jurisdiction | text | City, State, Territory |
| `week_of_allocations` | Week of Allocations | calendar_date |  |
| `_1st_dose_allocations` | 1st Dose Allocations | number | Number of 1st dose allocations that a jurisdiction can order from |
| `_2nd_dose_allocations` | 2nd Dose Allocations | number | Number of 2nd dose allocations that a jurisdiction can order from |

### saz5-9hgg

**COVID-19 Vaccine Distribution Allocations by Jurisdiction - Pfizer** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/saz5-9hgg.json`
- Metadata: `GET https://data.cdc.gov/api/views/saz5-9hgg.json`; page: https://data.cdc.gov/d/saz5-9hgg
- Topics: Category: Vaccinations
- Tags: `covid-19`, `vaccination`, `coronavirus`
- Rows: 1,764. Data updated: 2021-06-17. Probe status: 200.
- Update frequency: Weekly (Tuesday).
- Source: HHS ASPA
- Description: New weekly allocations of doses are posted every Tuesday. Beginning the following Thursday, states can begin ordering doses from that week’s new allocation of 1st doses. Beginning two weeks (Pfizer) or three weeks (Moderna) from the following Sunday, states can begin ordering doses from that week’s new allocation of 2nd doses. After doses are ordered by states, shipments begin the following Monday. The entire order may not arrive in one shipment or on one day, but over the course of the week. Second doses are opened up for orders on Sundays, at the appropriate interval two or three weeks late…
- Sample row fields ($limit=1): `jurisdiction`, `week_of_allocations`, `_1st_dose_allocations`, `_2nd_dose_allocations`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `jurisdiction` | Jurisdiction | text | City, State, Territory |
| `week_of_allocations` | Week of Allocations | calendar_date | Week that vaccines are allocated to a jurisdiction |
| `_1st_dose_allocations` | 1st Dose Allocations | number | Number of 1st dose allocations that a jurisdiction can order from |
| `_2nd_dose_allocations` | 2nd Dose Allocations | number | Number of 2nd dose allocations that a jurisdiction can order from |

### 9b5z-wnve

**COVID-19 Vaccines Up to Date Status** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/9b5z-wnve.json`
- Metadata: `GET https://data.cdc.gov/api/views/9b5z-wnve.json`; page: https://data.cdc.gov/d/9b5z-wnve
- Topics: Category: Vaccinations
- Tags: `covid-19`, `coronavirus`, `izdl`, `immunization`, `administration`, `vaccination`, `age`
- Rows: 12,685. Data updated: 2023-10-13. Probe status: 200.
- Update frequency: R/P1D.
- Description: This site provides historical data beginning June 14, 2023, for the visualization presented on <a href="https://covid.cdc.gov/covid-data-tracker/#vaccinations">COVID-19 Data Tracker’s “Vaccinations in the United States</a>” site titled “Percent of Total Population Who Are Up to Date with COVID-19 Vaccines” <b>Definition for Up to Date: For surveillance purposes people are ‘Upto Date’ with COVID-19 vaccines based on the following criteria:</b> People ages 6 years and older: Are up to date if they received 1 updated Pfizer-BioNTech or Moderna COVID-19 vaccine. Children ages 6 months to 5 years…
- Sample row fields ($limit=1): `date`, `location`, `demographic_category`, `census`, `up_to_date`, `up_to_date_pct_agegroup`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `date` | Date | calendar_date | Date data are reported on CDC COVID Data Tracker (https://covid.cdc.gov/covid-data-tracker/#vaccination-states-jurisdictions) |
| `location` | Location | text | Jurisdiction (State/Territory/Federal Entity) |
| `demographic_category` | Demographic_Category | text | Age, sex, or age by sex group of vaccine recipient |
| `census` | census | number | Census population |
| `up_to_date` | Up_to_date | number | Count of people that are up to date with COVID-19 vaccines, as defined in https://www.cdc.gov/coronavirus/2019-ncov/vaccines/stay-up-to-date.html |
| `up_to_date_pct_agegroup` | Up_to_date_pct_agegroup | number | Percent of people that are up to date with COVID-19 vaccines |

### b6uq-hdgz

**Cumulative Influenza Vaccination Coverage and Comparison, Adults 18 Years and Older, US, National Immunization Survey-Adult COVID Module** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/b6uq-hdgz.json`
- Metadata: `GET https://data.cdc.gov/api/views/b6uq-hdgz.json`; page: https://data.cdc.gov/d/b6uq-hdgz
- Topics: Category: Vaccinations
- Tags: `influenza`, `adults`, `flu vaccination`, `vaccination`, `coverage`, `vaccine coverage`
- Rows: 45,312. Data updated: 2023-04-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Cumulative Influenza Vaccination Coverage and Comparison, Adults 18 Years and Older, United States, Data Source: National Immunization Survey-Adult COVID Module. • The National Immunization Survey-Adult COVID Module (NIS-ACM) was launched in April 2021 among adults 18 years and older. The survey was used to monitor COVID-19 vaccination uptake and confidence in vaccination among adults and included questions about influenza vaccination.
- Sample row fields ($limit=1): `geography_name`, `geographic_level`, `parent_geography_name`, `age_group`, `age_group_sort_order`, `race_ethnicity`, `race_ethnicity_sort_order`, `urbanicity`, `urbanicity_sort_order`, `month`, `calender_month_number`, `month_season_text`, `month_sort_order`, `current_season_week_ending`, `current_through`, `current_season`, `past_season`, `current_season_dc_period`, `previous_season_dc_period`, `season_filter_text`, `current_season_estimate`, `past_season_estimate`, `current_week_ending_date`, `previous_week_ending_date`, `current_season_95ci_halfwidth`, `past_season_95ci_halfwidth`, `difference_estimate`, `current_season_95_ci`, `past_season_95_ci`, `difference_95_ci`, `difference_indicator`, `difference_legend_sort`, `binrangetext`, `binrangeorder`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `geography_name` | Geography_Name | text |  |
| `geographic_level` | Geographic_Level | text |  |
| `parent_geography_name` | Parent_Geography_Name | text |  |
| `age_group` | Age_Group | text |  |
| `age_group_sort_order` | Age_Group_Sort_Order | number |  |
| `race_ethnicity` | Race_Ethnicity | text |  |
| `race_ethnicity_sort_order` | Race_Ethnicity_Sort_Order | number |  |
| `urbanicity` | Urbanicity | text |  |
| `urbanicity_sort_order` | Urbanicity_Sort_Order | number |  |
| `month` | Month | text |  |
| `calender_month_number` | Calender_Month_Number | number |  |
| `month_season_text` | Month_Season_Text | text |  |
| `month_sort_order` | Month_Sort_Order | number |  |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | calendar_date |  |
| `current_through` | Current_Through | calendar_date |  |
| `current_season` | Current_Season | text |  |
| `past_season` | Past_Season | text |  |
| `current_season_dc_period` | Current_Season_DC_Period | text |  |
| `previous_season_dc_period` | Previous_Season_DC_Period | text |  |
| `season_filter_text` | Season_Filter_Text | text |  |
| `current_season_estimate` | Current_Season_Estimate | number |  |
| `past_season_estimate` | Past_Season_Estimate | number |  |
| `current_week_ending_date` | Current_Week_Ending_Date | calendar_date |  |
| `previous_week_ending_date` | Previous_Week_Ending_Date | calendar_date |  |
| `current_season_95ci_halfwidth` | Current_Season_95CI_HalfWidth | number |  |
| `past_season_95ci_halfwidth` | Past_Season_95CI_HalfWidth | number |  |
| `difference_estimate` | Difference_Estimate | number |  |
| `current_season_95_ci` | Current_Season_95_CI | text |  |
| `past_season_95_ci` | Past_Season_95_CI | text |  |
| `difference_95_ci` | Difference_95_CI | text |  |
| `difference_indicator` | Difference_Indicator | text |  |
| `difference_legend_sort` | Difference_Legend_Sort | number |  |
| `binrangetext` | BinRangeText | text |  |
| `binrangeorder` | BinRangeOrder | number |  |
| `weighted_sample_size` | Weighted_Sample_Size | number |  |
| `unweighted_sample_size` | Unweighted_Sample_Size | number |  |

### 6p3a-6xr9

**Cumulative Influenza Vaccination Coverage and Intent for Vaccination Among Adults 18 Years and Older by Age, Race/Ethnicity, and COVID-19 Vaccination and Intent, United States; IPSOS Knowledge Panel and NORC AmeriSpeak Omnibus Surveys.** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/6p3a-6xr9.json`
- Metadata: `GET https://data.cdc.gov/api/views/6p3a-6xr9.json`; page: https://data.cdc.gov/d/6p3a-6xr9
- Topics: Category: Vaccinations
- Tags: `vaccination coverage`, `vaccination`, `adults`, `age group`, `age`, `race`, `ethnicity`, `covid-19`, `covid-19 vaccination`, `influenza`, `flu`
- Rows: 52. Data updated: 2023-03-31. Probe status: 200.
- Update frequency: Weekly.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: National Center for Immunization and Respiratory Diseases, US Centers for Disease Control and Prevention. Cumulative Influenza Vaccination Coverage and Intent for Vaccination Among Adults 18 Years and Older by Age, Race/Ethnicity, and COVID-19 Vaccination and Intent, United States; IPSOS Knowledge Panel and NORC AmeriSpeak Omnibus Surveys.
- Sample row fields ($limit=1): `figure`, `geography_type`, `geography`, `timeperiod`, `timeperiod_sort`, `characteristic_group`, `characteristic_group_sort`, `characteristic_type`, `characteristic_type_sort`, `characteristic_value`, `characteristic_value_sort`, `indicator_group`, `indicator_group_sort`, `indicator_type`, `indicator_type_sort`, `indicator_value`, `indicator_value_sort`, `estimate`, `sample_size`, `coninf`, `ipsos_survey_fielding_date_range`, `norc_survey_fielding_date_range`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `figure` | figure | text | Data Figure Number |
| `geography_type` | Geography Type | text |  |
| `geography` | Geography | text |  |
| `timeperiod` | Time Period | text |  |
| `timeperiod_sort` | Time Period Sort Order | number |  |
| `characteristic_group` | Characteristic Group | text |  |
| `characteristic_group_sort` | Characteristic Group Sort | number |  |
| `characteristic_type` | Characteristic Type | text |  |
| `characteristic_type_sort` | Characteristic Type Sort Order | number |  |
| `characteristic_value` | Characteristic Value | text |  |
| `characteristic_value_sort` | Characteristic Value Sort Order | number |  |
| `indicator_group` | Indicator Group | text |  |
| `indicator_group_sort` | Indicator Group Sort Order | number |  |
| `indicator_type` | Indicator Type | text |  |
| `indicator_type_sort` | Indicator Type Sort Order | number |  |
| `indicator_value` | Indicator Value | text |  |
| `indicator_value_sort` | Indicator Value Sort Order | number |  |
| `estimate` | Estimate | number |  |
| `sample_size` | Sample Size | number |  |
| `coninf` | 95% Confidence Interval | text |  |
| `ipsos_survey_fielding_date_range` | IPSOS Survey Fielding Date Range | text |  |
| `norc_survey_fielding_date_range` | NORC Survey Fielding Date Range | text |  |

### ty79-wym3

**Cumulative Influenza Vaccination Coverage by Age Group, Race/Ethnicity, Urbanicity and Jurisdiction, NIS-ACM, Adults 18 Years and Older - NIS ACM** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ty79-wym3.json`
- Metadata: `GET https://data.cdc.gov/api/views/ty79-wym3.json`; page: https://data.cdc.gov/d/ty79-wym3
- Topics: Category: Vaccinations
- Tags: `influenza`, `adults`, `flu vaccination`, `vaccination`, `coverage`, `vaccine coverage`
- Rows: 105,728. Data updated: 2023-04-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Cumulative Influenza Vaccination Coverage by Age Group, Race/Ethnicity, Urbanicity and Jurisdiction, NIS-ACM, Adults 18 Years and Older, United States, National Immunization Survey-Adult COVID Module. Archived data are available at the following locations: 1. https://data.cdc.gov/resource/8dyx-9z99 2. https://data.cdc.gov/resource/3myw-4j4q • The National Immunization Survey-Adult COVID Module (NIS-ACM) was launched in April 2021 among adults 18 years and older. The survey was used to monitor COVID-19 vaccination uptake and confidence in vaccination among adults and included questions about i…
- Sample row fields ($limit=1): `week_ending`, `current_season_week_ending`, `influenza_season`, `data_collection_period`, `geography`, `geographic_level`, `parent_geography`, `age_group`, `age_group_sort_order`, `race`, `race_ethnicity_sort_order`, `urbanicity`, `urbanicity_sort_order`, `ci_range`, `suppression_flag`, `data_collection_sort_order`, `current_through`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week_Ending | calendar_date |  |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | calendar_date |  |
| `influenza_season` | Influenza_Season | text |  |
| `data_collection_period` | Data_Collection_Period | text |  |
| `geography` | Geography | text |  |
| `geographic_level` | Geographic_Level | text |  |
| `parent_geography` | Parent_Geography | text |  |
| `age_group` | Age_Group | text |  |
| `age_group_sort_order` | Age_Group_Sort_Order | number |  |
| `race` | Race | text |  |
| `race_ethnicity_sort_order` | Race_Ethnicity_Sort_Order | number |  |
| `urbanicity` | Urbanicity | text |  |
| `urbanicity_sort_order` | Urbanicity_Sort_Order | number |  |
| `point_estimate` | Point_Estimate | number |  |
| `standard_error` | Standard_Error | number |  |
| `upper_ci` | Upper_CI | number |  |
| `lower_ci` | Lower_CI | number |  |
| `ci_range` | CI_Range | text |  |
| `weighted_sample_size` | Weighted_Sample_Size | number |  |
| `unweighted_sample_size` | Unweighted_Sample_Size | number |  |
| `suppression_flag` | Suppression_Flag | checkbox |  |
| `data_collection_sort_order` | data_collection_sort_order | number |  |
| `current_through` | Current_Through | calendar_date |  |
| `binrangetext` | BinRangeText | text |  |
| `binrangeorder` | BinRangeOrder | number |  |

### 3myw-4j4q

**Cumulative Influenza Vaccination Coverage by Race/Ethnicity and Age Group, NIS-ACM** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3myw-4j4q.json`
- Metadata: `GET https://data.cdc.gov/api/views/3myw-4j4q.json`; page: https://data.cdc.gov/d/3myw-4j4q
- Topics: Category: Vaccinations
- Tags: `influenza`, `adults`, `flu vaccination`, `vaccination`, `coverage`, `vaccine coverage`
- Rows: 0. Data updated: 2023-03-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Cumulative Influenza Vaccination Coverage Age Group, Race/Ethnicity, and Jurisdiction, Adults 18 Years and Older, United States, National Immunization Survey Adult COVID Module. Archived data are available including for Figures 4B and 4C: https://data.cdc.gov/resource/8dyx-9z99 • The National Immunization Survey-Adult COVID Module (NIS-ACM) was launched in April 2021 among adults 18 years and older. The survey was used to monitor COVID-19 vaccination uptake and confidence in vaccination among adults and included questions about influenza vaccination.
- Sample row: none (0 rows)

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week_Ending | calendar_date |  |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | text |  |
| `influenza_season` | Influenza_Season | text |  |
| `data_collection_period` | Data_Collection_Period | text |  |
| `geography` | Geography | text |  |
| `geographic_level` | Geographic_Level | text |  |
| `parent_geography` | Parent_Geography | text |  |
| `age_group` | Age_Group | text |  |
| `age_group_sort_order` | Age_Group_Sort_Order | number |  |
| `race` | Race | text |  |
| `race_ethnicity_sort_order` | Race_Ethnicity_Sort_Order | number |  |
| `point_estimate` | Point_Estimate | number |  |
| `standard_error` | Standard_Error | number |  |
| `upper_ci` | Upper_CI | number |  |
| `lower_ci` | Lower_CI | number |  |
| `ci_range` | CI_Range | text |  |
| `weighted_sample_size` | Weighted_Sample_Size | number |  |
| `unweighted_sample_size` | Unweighted_Sample_Size | number |  |
| `suppression_flag` | Suppression_Flag | checkbox |  |
| `current_through` | Current_Through | calendar_date |  |
| `binrangetext` | BinRangeText | text |  |
| `binrangeorder` | BinRangeOrder | number |  |

### 8dyx-9z99

**Cumulative Influenza Vaccination Coverage by Race/Ethnicity and Age Group, NIS-ACM (Archived)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8dyx-9z99.json`
- Metadata: `GET https://data.cdc.gov/api/views/8dyx-9z99.json`; page: https://data.cdc.gov/d/8dyx-9z99
- Topics: Category: Vaccinations
- Tags: `influenza`, `adults`, `flu vaccination`, `vaccination`, `coverage`, `vaccine coverage`
- Rows: 7,152. Data updated: 2022-09-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Cumulative Influenza Vaccination Coverage Age Group, Race/Ethnicity, and Jurisdiction, Adults 18 Years and Older, United States, National Immunization Survey Adult COVID Module. The National Immunization Survey-Adult COVID Module (NIS-ACM) was launched in April 2021 among adults 18 years and older. The survey was used to monitor COVID-19 vaccination uptake and confidence in vaccination among adults and included questions about influenza vaccination.
- Sample row fields ($limit=1): `week_ending`, `current_season_week_ending`, `influenza_season`, `data_collection_period`, `geography`, `geographic_level`, `parent_geography`, `age_group`, `age_group_sort_order`, `race`, `race_ethnicity_sort_order`, `point_estimate`, `standard_error`, `upper_ci`, `lower_ci`, `ci_range`, `weighted_sample_size`, `unweighted_sample_size`, `suppression_flag`, `current_through`, `binrangetext`, `binrangeorder`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week_Ending | calendar_date |  |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | calendar_date |  |
| `influenza_season` | Influenza_Season | text |  |
| `data_collection_period` | Data_Collection_Period | text |  |
| `geography` | Geography | text |  |
| `geographic_level` | Geographic_Level | text |  |
| `parent_geography` | Parent_Geography | text |  |
| `age_group` | Age_Group | text |  |
| `age_group_sort_order` | Age_Group_Sort_Order | number |  |
| `race` | Race | text |  |
| `race_ethnicity_sort_order` | Race_Ethnicity_Sort_Order | number |  |
| `point_estimate` | Point_Estimate | number |  |
| `standard_error` | Standard_Error | number |  |
| `upper_ci` | Upper_CI | number |  |
| `lower_ci` | Lower_CI | number |  |
| `ci_range` | CI_Range | text |  |
| `weighted_sample_size` | Weighted_Sample_Size | number |  |
| `unweighted_sample_size` | Unweighted_Sample_Size | number |  |
| `suppression_flag` | Suppression_Flag | checkbox |  |
| `current_through` | Current_Through | calendar_date |  |
| `binrangetext` | BinRangeText | text |  |
| `binrangeorder` | BinRangeOrder | number |  |

### 2den-c3u2

**Cumulative Influenza Vaccination Coverage Differences by Race/Ethnicity, Children 6 months through 17 years, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/2den-c3u2.json`
- Metadata: `GET https://data.cdc.gov/api/views/2den-c3u2.json`; page: https://data.cdc.gov/d/2den-c3u2
- Topics: Category: Vaccinations
- Tags: `influenza`, `flu`, `nis`, `children`, `vaccine coverage`, `flu shot`
- Rows: 2,208. Data updated: 2024-05-24. Probe status: 200.
- Update frequency: Weekly.
- Description: Cumulative Influenza Vaccination Coverage Differences by Race/Ethnicity, Children 6 months through 17 years, United States Vaccinations • Influenza vaccination coverage among children is assessed through the National Immunization Survey-Flu (NIS-Flu) annually, providing weekly influenza vaccination coverage estimates for children 6 months–17 years based upon parental report. (https://www.cdc.gov/vaccines/imz-managers/nis/about.html) o NIS-Flu is a national random-digit-dialed cellular telephone survey of households conducted during the flu season (October-June). • Final estimates for prior se…
- Sample row fields ($limit=1): `comparison_type`, `week_ending`, `current_season_week_ending`, `comparison_group1`, `comparison_group2`, `comparison_group1_point`, `comparison_group2_point`, `difference_estimate`, `difference_estimate_lower`, `difference_estimate_upper`, `significant_at_95_pct`, `comparison_group1_sort_order`, `comparison_group2_sort_order`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `comparison_type` | Comparison_Type | text | Comparison Type |
| `week_ending` | Week_Ending | calendar_date | Week Ending Date |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | calendar_date | Current Season Week Ending Label |
| `comparison_group1` | Comparison_Group1 | text | Comparison Group 1 |
| `comparison_group2` | Comparison_Group2 | text | Comparison Group 2 |
| `comparison_group1_point` | Comparison_Group1_Point_Estimate | number | Comparison Group 1 Point Estimate |
| `comparison_group2_point` | Comparison_Group2_Point_Estimate | number | Comparison Group 2 Point Estimate |
| `difference_estimate` | Difference_Estimate | number | Difference Estimate |
| `difference_estimate_lower` | Difference_Estimate_Lower_95_CI | number | Lower 95% Confidence Interval Bound of Difference Estimate |
| `difference_estimate_upper` | Difference_Estimate_Upper_95_CI | number | Upper 95% Confidence Interval Bound of Difference Estimate |
| `significant_at_95_pct` | Significant_at_95_Pct | text | Statistically Significant at 95% Confidence Indicator |
| `comparison_group1_sort_order` | Comparison_Group1_Sort_Order | number | Comparison Group 1 Sort Order |
| `comparison_group2_sort_order` | Comparison_Group2_Sort_Order | number | Comparison Group 2 Sort Order |

### kmap-fsfn

**Cumulative Influenza Vaccination Coverage, Adults 18 years and older, by Age Group and Race/Ethnicity, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/kmap-fsfn.json`
- Metadata: `GET https://data.cdc.gov/api/views/kmap-fsfn.json`; page: https://data.cdc.gov/d/kmap-fsfn
- Topics: Category: Vaccinations
- Tags: `flu`, `flu vaccination`, `vaccination`, `adults`, `age group`, `race`, `ethnicity`
- Rows: 140. Data updated: 2022-04-01. Probe status: 200.
- Update frequency: Weekly.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Cumulative Influenza Vaccination Coverage, Adults 18 years and older, by Age Group and Race/Ethnicity, United States, 2020-21, IPSOS Knowledge Panel Omnibus and NORC AmeriSpeak Omnibus Surveys
- Sample row fields ($limit=1): `data_collection_start_date`, `data_collection_end_date`, `data_collection_midpoint`, `data_collection_midpoint_1`, `data_collection_midpoint_2`, `data_collection_midpoint_3`, `data_collection_midpoint_4`, `month_abbrev`, `month_sort_order`, `data_source`, `suppressed`, `race_ethnicity`, `age_group`, `point_estimate`, `ci_halfwidth`, `ci_lower`, `ci_upper`, `sample_size`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `data_collection_start_date` | Data_Collection_Start_Date | calendar_date | Data Collection Start Date |
| `data_collection_end_date` | Data_Collection_End_Date | calendar_date | Data Collection End Date |
| `data_collection_midpoint` | Data_Collection_Midpoint_date | calendar_date | Data Collection Midpoint Date |
| `data_collection_midpoint_1` | Data_Collection_Midpoint_MMWR_Year | number | Data Collection Midpoint MMWR Year |
| `data_collection_midpoint_2` | Data_Collection_Midpoint_MMWR_Week | number | Data Collection Midpoint MMWR Week |
| `data_collection_midpoint_3` | Data_Collection_Midpoint_MMWR_Day | number | Data Collection Midpoint MMWR Day |
| `data_collection_midpoint_4` | Data_Collection_Midpoint_MMWRWeek_Display_Order | number | Data Collection Midpoint MMWR Week Display Order |
| `month_abbrev` | Month_Abbrev | text | Data Collection Month (Abbreviated) |
| `month_sort_order` | Month_Sort_Order | number | Data Collection Month Sort Order |
| `data_source` | Data_Source | text | Survey Data Source |
| `suppressed` | Suppressed | checkbox | Data Privacy Suppression Indicator (for samples <30) |
| `race_ethnicity` | Race_Ethnicity | text | Race and Ethnicity |
| `age_group` | Age_Group | text | Age Group |
| `point_estimate` | Point_Estimate | number | Point Estimate - Coverage (Percentage) |
| `ci_halfwidth` | CI_HalfWidth | number | Confidence Interval Half-Width (Percentage) |
| `ci_lower` | CI_Lower | number | 95% Confidence Interval - Lower Bound (Percentage) |
| `ci_upper` | CI_Upper | number | 95% Confidence Interval - Upper Bound (Percentage) |
| `sample_size` | Sample_Size | text | Sample Size |

### nkr7-scx6

**Cumulative Influenza Vaccination Coverage, by Flu Season and Race/Ethnicity, Pregnant Women 18-49 years** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/nkr7-scx6.json`
- Metadata: `GET https://data.cdc.gov/api/views/nkr7-scx6.json`; page: https://data.cdc.gov/d/nkr7-scx6
- Topics: Category: Vaccinations
- Tags: `influenza`, `flu`, `nis`, `nis-flu`, `children`, `vaccine coverage`
- Rows: 280. Data updated: 2025-01-31. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Cumulative Influenza Vaccination Coverage, by Flu Season and Race/Ethnicity, Pregnant Women 18-49 years • These monthly flu vaccination coverage estimates for pregnant women are based on electronic health record (EHR) data from the Vaccine Safety Datalink (VSD), a collaboration between CDC’s Immunization Safety Office and nine integrated health care organizations.§ This system has been used annually to estimate vaccination coverage among pregnant women. COVID-19 vaccination coverage for pregnant women is available here. • Figure 3A. Monthly Cumulative Influenza Vaccination Coverage*, by Flu S…
- Sample row fields ($limit=1): `month`, `flu_season`, `race_ethnicity`, `percentage_vaccinated`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `month` | Month | text | Calendar month |
| `flu_season` | Flu Season | text | Flu Season |
| `race_ethnicity` | Race_Ethnicity | text | Race and Ethnicity |
| `percentage_vaccinated` | Percentage Vaccinated | number | Percentage Vaccinated |

### v22g-tzpk

**Differences in Cumulative Influenza Vaccination Coverage by Selected Demographics, Adults 18 Year and Older, NIS Adult COVID Module** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/v22g-tzpk.json`
- Metadata: `GET https://data.cdc.gov/api/views/v22g-tzpk.json`; page: https://data.cdc.gov/d/v22g-tzpk
- Topics: Category: Vaccinations
- Tags: `vaccination`, `flu vaccination`, `flu`, `adults`, `race`, `ethnicity`, `vaccine coverage`
- Rows: 4,323. Data updated: 2024-05-24. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Differences in Cumulative Influenza Vaccination Coverage by Selected Demographics, Adults 18 Year and Older, NIS Adult COVID Module • The National Immunization Survey-Adult COVID Module (NIS-ACM) was launched in April 2021 among adults 18 years and older. The survey was used to monitor COVID-19 vaccination uptake and confidence in vaccination among adults and included questions about influenza vaccination.
- Sample row fields ($limit=1): `comparison_type`, `week_ending`, `current_season_week_ending`, `comparison_group1`, `comparison_group2`, `comparison_group1_point`, `comparison_group2_point`, `difference_estimate`, `difference_estimate_lower`, `difference_estimate_upper`, `significant_at_95_pct`, `comparison_group1_sort_order`, `comparison_group2_sort_order`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `comparison_type` | Comparison_Type | text | Comparison Type |
| `week_ending` | Week_Ending | calendar_date | Week Ending Date |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | calendar_date | Current Season Week Ending Label |
| `comparison_group1` | Comparison_Group1 | text | Comparison Group 1 |
| `comparison_group2` | Comparison_Group2 | text | Comparison Group 2 |
| `comparison_group1_point` | Comparison_Group1_Point_Estimate | number | Comparison Group 1 Point Estimate |
| `comparison_group2_point` | Comparison_Group2_Point_Estimate | number | Comparison Group 2 Point Estimate |
| `difference_estimate` | Difference_Estimate | number | Difference Estimate |
| `difference_estimate_lower` | Difference_Estimate_Lower_95_CI | number | Lower 95% Confidence Interval Bound of Difference Estimate |
| `difference_estimate_upper` | Difference_Estimate_Upper_95_CI | number | Upper 95% Confidence Interval Bound of Difference Estimate |
| `significant_at_95_pct` | Significant_at_95_Pct | text | Statistically Significant at 95% Confidence Indicator |
| `comparison_group1_sort_order` | Comparison_Group1_Sort_Order | number | Comparison Group 1 Sort Order |
| `comparison_group2_sort_order` | Comparison_Group2_Sort_Order | number | Comparison Group 2 Sort Order |

### muep-c3qd

**Household Pulse Survey (HPS): COVID-19 Vaccination among People with Disabilities** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/muep-c3qd.json`
- Metadata: `GET https://data.cdc.gov/api/views/muep-c3qd.json`; page: https://data.cdc.gov/d/muep-c3qd
- Topics: Category: Vaccinations
- Tags: `hps`, `covid tracker`, `disability`, `covid-19 vaccination`
- Rows: 1,347. Data updated: 2022-12-20. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Household Pulse Survey (HPS): HPS is a rapid-response survey of adults ages ≥18 years led by the U.S. Census Bureau, in partnership with seven other federal statistical agencies, to measure household experiences during the COVID-19 pandemic. Detailed information on probability sampling using the U.S. Census Bureau’s Master Address File, questionnaires, response rates, and bias assessment is available on the Census Bureau website (https://www.census.gov/data/experimental-data-products/household-pulse-survey.html). Data from adults age ≥18 years are collected by 20-minute online survey from ran…
- Sample row fields ($limit=1): `week`, `disability_type`, `status`, `category`, `demographic`, `estimate_type`, `estimate`, `coninf_95`, `sample_size`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week` | Data Collection Period | text | The date range during which data was collected to produce these estimates. More information about data collection periods can be found at https://www.census.gov/programs-surveys/household-pulse-survey/technical-documentation.html. |
| `disability_type` | Disability Type | text | One of the WG-SS four domains of functioning: seeing (even when wearing glasses), hearing (even when using a hearing aid), mobility (walking or climbing stairs), and cognition (remembering or concentrating); or "Any Disability" for respond… |
| `status` | Disability Status | text | The reported disability status for which estimates are calculated. The two statuses are “With Disability” and “Without Disability.” |
| `category` | Demographic Category | text | The classification of the sociodemographic category for which estimates are calculated. The two applicable categories are "Age" and "Race/Ethnicity." |
| `demographic` | Demographic | text | The sociodemographic group for which estimates are calculated. |
| `estimate_type` | Vaccination Status and Intent | text | Estimate categorization; one of “Vaccinated”, “Definitely Plan to Get Vaccinated”, “Probably Will Get Vaccinated or Are Unsure”, or “Probably or Definitely Will Not Get Vaccinated” |
| `estimate` | Estimate (%) | number | The numerical estimate of the weighted proportion giving the response. |
| `coninf_95` | 95% CI (%) | text | The 95% confidence interval of the estimate. |
| `sample_size` | Sample Size | number | The unweighted sample size used to create the estimate for each demographic and disability status grouping. |
| `suppression_flag` | Suppression Flag | number | Estimates that did not meet the National Center for Health Statistics (NCHS) standards of reliability are suppressed (left missing) and have a value of 1 for this field. If the estimate met the NCHS standards of reliability, the estimate w… |

### scrf-8d7w

**Monthly Cumulative Number and Percent of Adults 60 Years and Older Who Received at least one RSV Vaccination Doses by Jurisdiction, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/scrf-8d7w.json`
- Metadata: `GET https://data.cdc.gov/api/views/scrf-8d7w.json`; page: https://data.cdc.gov/d/scrf-8d7w
- Topics: Category: Vaccinations
- Tags: `rsv vaccination`, `iis`, `immunization information system`
- Rows: 549. Data updated: 2024-08-05. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Monthly Cumulative Number and Percent of Adults 60 Years and Older Who Received at least one RSV Vaccination Doses by Jurisdiction • Estimated Respiratory Syncytial Virus (RSV) vaccination coverage for adults is assessed through U.S. jurisdictions’ Immunization Information Systems (IIS) data, submitted from jurisdictions to CDC monthly in aggregate by age group. • Starting in July 2023, the CDC recommended the RSV vaccine to protect against serious illness from RSV. (https://www.cdc.gov/respiratory-viruses/whats-new/rsv-update-2023-09-22.html)
- Sample row fields ($limit=1): `month`, `numerator`, `population`, `jurisdiction`, `estimate`, `age_group_label`, `legend`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `month` | Month | text | The month of data |
| `numerator` | Numerator | text | Number of people receiving 1+ RSV dose |
| `population` | Population | text | U.S. Census Bureau population estimates |
| `jurisdiction` | Jurisdiction | text | The name of the jurisdiction |
| `estimate` | Estimate | text | Monthly percent coverage |
| `age_group_label` | Age_group_label | text | Age groups |
| `legend` | Legend | text | Combined language for the legend: jurisdiction and age group |

### n2zz-25mk

**Monthly Cumulative Number and Percent of Adults 75 Years and Older Who Received 1+ RSV Vaccination Doses by Jurisdiction, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/n2zz-25mk.json`
- Metadata: `GET https://data.cdc.gov/api/views/n2zz-25mk.json`; page: https://data.cdc.gov/d/n2zz-25mk
- Topics: Category: Vaccinations
- Tags: `iis`, `nis-acm`, `vsd`, `iqvia`, `rsv vaccination`
- Rows: 504. Data updated: 2025-05-16. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • Monthly Cumulative Percent of Adults 75 Years and Older Who Received 1+ RSV Vaccination Doses by Jurisdiction, United States. • Respiratory Syncytial Virus (RSV) vaccination coverage for adults is assessed through U.S. jurisdictions’ Immunization Information Systems Resources (IIS) data, submitted from jurisdictions to CDC monthly in aggregate by age group (https://www.cdc.gov/iis/about/).
- Sample row fields ($limit=1): `month`, `numerator`, `population`, `jurisdiction`, `estimate`, `age_group_label`, `season`, `legend`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `month` | Month | text | The month of data |
| `numerator` | Numerator | text | Number of people receiving 1+ RSV dose |
| `population` | Population | text | U.S. Census Bureau population estimates |
| `jurisdiction` | Jurisdiction | text | The name of the jurisdiction |
| `estimate` | Estimate | text | Monthly percent coverage |
| `age_group_label` | Age_group_label | text | Age groups |
| `season` | season | text | The current RSV season |
| `legend` | legend | text | Combined language for the legend: jurisdiction and age group |

### 2yum-eg9f

**Monthly Cumulative Number and Percent of Adults 75 Years and Older Who Received 1+ RSV Vaccination Doses by Jurisdiction, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/2yum-eg9f.json`
- Metadata: `GET https://data.cdc.gov/api/views/2yum-eg9f.json`; page: https://data.cdc.gov/d/2yum-eg9f
- Topics: Category: Vaccinations
- Tags: `iis`, `nis-acm`, `vsd`, `iqvia`, `rsv vaccination`
- Rows: 567. Data updated: 2026-05-20. Probe status: 200.
- Update frequency: Monthly.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Monthly Cumulative Percent of Adults 75 Years and Older Who Received 1+ RSV Vaccination Doses by Jurisdiction, United States. Respiratory Syncytial Virus (RSV) vaccination coverage for adults is assessed through U.S. jurisdictions’ Immunization Information Systems Resources (IIS) data, submitted from jurisdictions to CDC monthly in aggregate by age group. Monthly estimates shown are cumulative, reflecting all persons aged 75 years and older who received at least one dose of an RSV vaccine from June 21, 2023, through the end of the reporting month.*,† Cumulative estimates include any historica…
- Sample row fields ($limit=1): `month`, `numerator`, `jurisdiction`, `age_group_label`, `season`, `legend`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `month` | Month | text |  |
| `numerator` | Numerator | text |  |
| `population` | Population | number |  |
| `jurisdiction` | Jurisdiction | text |  |
| `estimate` | Estimate | number |  |
| `age_group_label` | Age_group_label | text |  |
| `season` | season | text |  |
| `legend` | legend | text |  |

### ku7p-zn4c

**Monthly Cumulative Number and Percent of Children <20 Months Who Received Nirsevimab by Age Group and Jurisdiction, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ku7p-zn4c.json`
- Metadata: `GET https://data.cdc.gov/api/views/ku7p-zn4c.json`; page: https://data.cdc.gov/d/ku7p-zn4c
- Topics: Category: Vaccinations
- Tags: `rsv vaccination`, `iis`, `immunization information system`
- Rows: 1,647. Data updated: 2024-08-05. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Monthly Cumulative Number and Percent of Children <20 Months Who Received Nirsevimab by Age Group and Jurisdiction • Estimated nirsevimab coverage for children 0-19 months is assessed through U.S. jurisdictions’ Immunization Information Systems (IIS) data, submitted from jurisdictions to CDC monthly in aggregate by age group. • Starting in July 2023, the CDC recommended the RSV vaccine to protect against serious illness from RSV. (https://www.cdc.gov/respiratory-viruses/whats-new/rsv-update-2023-09-22.html)
- Sample row fields ($limit=1): `month`, `numerator`, `population`, `jurisdiction`, `estimate`, `age_group_label`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `month` | Month | text | The month of data |
| `numerator` | Numerator | text | Number of people receiving 1+ Nirsevimab dose |
| `population` | Population | number | U.S. Census Bureau population estimates |
| `jurisdiction` | Jurisdiction | text | The name of the jurisdiction |
| `estimate` | Estimate | number | Monthly percent coverage |
| `age_group_label` | Age_group_label | text | Age groups |

### vhcj-3k53

**Monthly Cumulative Number and Percent of Children <8 Months Who Received 1+ Monoclonal Antibody Doses by Jurisdiction, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/vhcj-3k53.json`
- Metadata: `GET https://data.cdc.gov/api/views/vhcj-3k53.json`; page: https://data.cdc.gov/d/vhcj-3k53
- Topics: Category: Vaccinations
- Tags: `iis`, `nis-acm`, `vsd`, `iqvia`, `rsv vaccination`
- Rows: 504. Data updated: 2026-05-20. Probe status: 200.
- Update frequency: Monthly.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Monthly Cumulative Percent of Children <8 Months Who Received 1+ Monoclonal Antibody by Jurisdiction, United States. RSV monoclonal antibody coverage for children 0 to 7 months is assessed through U.S. jurisdictions’ Immunization Information Systems Resources (IIS) data, submitted from jurisdictions to CDC monthly in aggregate by age group. Monthly estimates shown are cumulative, reflecting all children who received an RSV monoclonal antibody from April 1 through the end of the reporting month.*,† Cumulative estimates include any historical data reported since the previous submission. Nationa…
- Sample row fields ($limit=1): `season`, `month`, `numerator`, `jurisdiction`, `age_group_label`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `season` | Season | text |  |
| `month` | Month | text | The month of data |
| `numerator` | Numerator | text | Number of people receiving 1+ RSV dose |
| `population` | Population | number | U.S. Census Bureau population estimates |
| `jurisdiction` | Jurisdiction | text | The name of the jurisdiction |
| `estimate` | Estimate | number | Monthly percent coverage |
| `age_group_label` | Age_group_label | text | Age groups |

### 4bdk-kyzv

**Monthly Cumulative Number and Percent of Children <8 Months Who Received Nirsevimab by Jurisdiction, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/4bdk-kyzv.json`
- Metadata: `GET https://data.cdc.gov/api/views/4bdk-kyzv.json`; page: https://data.cdc.gov/d/4bdk-kyzv
- Topics: Category: Vaccinations
- Tags: `iis`, `nis-acm`, `vsd`, `iqvia`, `rsv vaccination`
- Rows: 441. Data updated: 2025-05-16. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Monthly Cumulative Percent of Children <8 Months Who Received Nirsevimab by Jurisdiction, United States. Nirsevimab coverage for children 0 to 7 months is assessed through U.S. jurisdictions’ Immunization Information Systems Resources (IIS) data, submitted from jurisdictions to CDC monthly in aggregate by age group (https://www.cdc.gov/iis/about/).
- Sample row fields ($limit=1): `season`, `month`, `numerator`, `population`, `jurisdiction`, `estimate`, `age_group_label`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `season` | Season | text | The current RSV season |
| `month` | Month | text | The month of data |
| `numerator` | Numerator | text | Number of people receiving 1+ RSV dose |
| `population` | Population | text | U.S. Census Bureau population estimates |
| `jurisdiction` | Jurisdiction | text | The name of the jurisdiction |
| `estimate` | Estimate | text | Monthly percent coverage |
| `age_group_label` | Age_group_label | text | Age groups |

### q84f-e68r

**Monthly Cumulative Number and Percent of Persons Who Received 1+ COVID-19 Vaccination Doses and Comparison between 2025─26 and Previous Seasons, by Age Group and Jurisdiction, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/q84f-e68r.json`
- Metadata: `GET https://data.cdc.gov/api/views/q84f-e68r.json`; page: https://data.cdc.gov/d/q84f-e68r
- Topics: Category: Vaccinations
- Tags: `iis`, `nis-acm`, `vsd`, `iqvia`, `covid-19 vaccination`
- Rows: 12,600. Data updated: 2026-05-20. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Monthly Cumulative Number and Percent of Persons Who Received 1+COVID-19 Vaccination Doses and Comparison between 2025–26 and Previous Seasons, by Age Group and Jurisdiction COVID-19 vaccination coverage for children and adults is assessed through U.S. jurisdictions’ Immunization Information Systems Resources (IIS) data, submitted from jurisdictions to CDC monthly in aggregate by age group. Monthly estimates shown are cumulative, reflecting all persons vaccinated from July 1 through a given month of that season.*,†, ‡ Cumulative estimates include any historical data reported since the previou…
- Sample row fields ($limit=1): `current_season`, `month`, `previous_covid_season`, `jurisdiction`, `_2025_26_estimate`, `previous_estimate`, `difference_in_season_estimate`, `numerator`, `previous_season_numerator`, `population`, `age_group_label`, `difference_indicator`, `child_or_adult`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `current_season` | Current_season | text | The current COVID-19 season |
| `month` | Month | text | The month of data |
| `previous_covid_season` | Previous_covid_Season | text | Previous COVID-19 season |
| `jurisdiction` | Jurisdiction | text | The name of the jurisdiction |
| `_2025_26_estimate` | 2025_26_estimate | text | Monthly percent coverage for the 2025-26 season |
| `previous_estimate` | Previous_Estimate | text | Monthly percent coverage for the previous season |
| `difference_in_season_estimate` | Difference_in_season_estimate | text | Monthly percent coverage difference between the 2025-26 season and the previous season |
| `numerator` | Numerator | text | The number of people receiving 1+ COVID-19 dose |
| `previous_season_numerator` | Previous_season_numerator | text | The number of people receiving at least 1 Covid-19 dose in each previous season |
| `population` | Population | text | U.S. Census Bureau population estimates |
| `age_group_label` | Age_group_label | text | Age groups |
| `difference_indicator` | Difference_indicator | text | The difference levels shown on the comparison maps |
| `child_or_adult` | Child_or_adult | text | Child data or adult data based on the age range |

### 3bmy-cyyd

**Monthly Cumulative Number and Percent of Persons Who Received 1+ COVID-19 Vaccination Doses, by Season, Age Group, and Jurisdiction, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/3bmy-cyyd.json`
- Metadata: `GET https://data.cdc.gov/api/views/3bmy-cyyd.json`; page: https://data.cdc.gov/d/3bmy-cyyd
- Topics: Category: Vaccinations
- Tags: `iis`, `nis-acm`, `vsd`, `iqvia`, `covid-19 vaccination`
- Rows: 21,420. Data updated: 2026-05-20. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: COVID-19 vaccination coverage for children and adults is assessed through U.S. jurisdictions’ Immunization Information Systems Resources (IIS), submitted from jurisdictions to CDC monthly in aggregate by age group. Monthly estimates shown are cumulative, reflecting all persons vaccinated from July 1 through a given month of that season.*,†, ‡ Cumulative estimates include any historical data reported since the previous submission. National estimates are not presented since not all U.S. jurisdictions are currently reporting their IIS data to CDC. Jurisdictions reporting data to CDC include U.S.…
- Sample row fields ($limit=1): `current_season`, `month`, `numerator`, `population`, `jurisdiction`, `estimate`, `age_group_label`, `legend`, `child_or_adult`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `current_season` | current_season | text | The current COVID-19 Season |
| `month` | Month | text | The month of data |
| `numerator` | Numerator | text | Number of people receiving 1+ COVID-19 dose |
| `population` | Population | text | U.S. Census Bureau population estimates |
| `jurisdiction` | Jurisdiction | text | The name of the jurisdiction |
| `estimate` | Estimate | number | Monthly percent coverage |
| `age_group_label` | Age_group_label | text | Age groups |
| `legend` | Legend | text | Combined language for the legend: jurisdiction and age group |
| `child_or_adult` | Child or adult | text | Child data or adult data based on the age range |

### wtw5-4wi3

**Monthly Cumulative Number and Percent of Persons Who Received 1+ updated 2023-24 COVID-19 Vaccination Doses by Age Group and Jurisdiction, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/wtw5-4wi3.json`
- Metadata: `GET https://data.cdc.gov/api/views/wtw5-4wi3.json`; page: https://data.cdc.gov/d/wtw5-4wi3
- Topics: Category: Vaccinations
- Tags: `covid-19 vaccination`, `iis`, `immunization information system`
- Rows: 6,237. Data updated: 2024-08-05. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Monthly Cumulative Percent of Persons Who Received 1+ updated 2023-24 COVID-19 Vaccination Doses by Age Group and Jurisdiction • Estimated Number of COVID-19 vaccinations among children 6 months–17 years and adults is assessed through U.S. jurisdictions’ Immunization Information Systems (IIS) data, submitted from jurisdictions to CDC monthly in aggregate by age group. • Starting in September 2023, the CDC recommended the 2023-2024 updated COVID-19 vaccine to protect against serious illness from COVID-19. (https://www.cdc.gov/coronavirus/2019-ncov/vaccines/stay-up-to-date.html)
- Sample row fields ($limit=1): `month`, `numerator`, `population`, `jurisdiction`, `estimate`, `age_group_label`, `child_or_adult`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `month` | Month | text | The month of data |
| `numerator` | Numerator | text | Number of people receiving 1+ COVID-19 dose |
| `population` | Population | number | U.S. Census Bureau population estimates |
| `jurisdiction` | Jurisdiction | text | The name of the jurisdiction |
| `estimate` | Estimate | number | Monthly percent coverage |
| `age_group_label` | Age_group_label | text | Age groups |
| `child_or_adult` | Child or Adult | text | Child data or adult data based on the age range |

### vugp-mqip

**Monthly Cumulative Number and Percent of Persons Who Received 1+ updated 2023-24 COVID-19 Vaccination Doses by Age Group and Jurisdiction, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/vugp-mqip.json`
- Metadata: `GET https://data.cdc.gov/api/views/vugp-mqip.json`; page: https://data.cdc.gov/d/vugp-mqip
- Topics: Category: Vaccinations
- Tags: `covid-19 vaccination`, `iis`, `immunization information system`
- Rows: 6,237. Data updated: 2024-08-05. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Monthly Cumulative Percent of Persons Who Received 1+ updated 2023-24 COVID-19 Vaccination Doses by Age Group and Jurisdiction • Estimated Number of COVID-19 vaccinations among children 6 months–17 years and adults is assessed through U.S. jurisdictions’ Immunization Information Systems (IIS) data, submitted from jurisdictions to CDC monthly in aggregate by age group. • Starting in September 2023, the CDC recommended the 2023-2024 updated COVID-19 vaccine to protect against serious illness from COVID-19. (https://www.cdc.gov/coronavirus/2019-ncov/vaccines/stay-up-to-date.html)
- Sample row fields ($limit=1): `month`, `jurisdiction`, `age_group_label`, `legend`, `child_or_adult`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `month` | Month | text | The month of data |
| `numerator` | Numerator | text | Number of people receiving 1+ COVID-19 dose |
| `population` | Population | text | U.S. Census Bureau population estimates |
| `jurisdiction` | Jurisdiction | text | The name of the jurisdiction |
| `estimate` | Estimate | text | Monthly percent coverage |
| `age_group_label` | Age_group_label | text | Age groups |
| `legend` | Legend | text | Combined language for the legend: jurisdiction and age group |
| `child_or_adult` | Child_or_adult | text | Child data or adult data based on the age range |

### si7g-c2bs

**National Immunization Survey Adult COVID Module (NIS-ACM): RespVaxView| Data | Centers for Disease Control and Prevention (cdc.gov) 2024-2025 Archive Season** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/si7g-c2bs.json`
- Metadata: `GET https://data.cdc.gov/api/views/si7g-c2bs.json`; page: https://data.cdc.gov/d/si7g-c2bs
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `covid-19 vaccination`, `vaccine confidence`, `rsv vaccination`, `vaccination`, `vaccination coverage`
- Rows: 1,440,643. Data updated: 2025-05-16. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • National Immunization Survey Adult COVID Module (NIS-ACM): CDC is providing information on the updated 2024-25 COVID-19 vaccine, the 2024-25 seasonal flu vaccine, and the RSV vaccine uptake and confidence. These data represent trends in vaccination status and intent, and other behavioral indicators, by demographics and other characteristics. • The data start in September 2024. • The archived data can be found here: - 2023-24 season: https://data.cdc.gov/Vaccinations/National-Immunization-Survey-Adult-COVID-Module-NI/uc4z-hbsd/about_data - Before October 2023: https://data.cdc.gov/Vaccinatio…
- Sample row fields ($limit=1): `geography_type`, `geography`, `group_name`, `group_category`, `indicator_name`, `indicator_category`, `time_period`, `year`, `time_type`, `estimate`, `_95_ci`, `sample_size`, `new_vax_group`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `geography_type` | Geography Type | text | The classification (National, Regional, or Jurisdictional) of geographies. |
| `geography` | Geography | text | The name of the geography for which estimates are calculated. |
| `group_name` | Group Name | text | The name of the variable by which estimates are grouped. (All, Age, Sex, Race/Ethnicity, Health Insurance, Vaccination Status, Vaccination Intent, etc.) |
| `group_category` | Group Category | text | The level of each group variable (18–29 years, Insured/Not Insured, Urban etc.) |
| `indicator_name` | Indicator Name | text | The indicator variable assessed by the survey (Concern about COVID-19, Confidence in COVID-19 Vaccine Safety, Vaccination and Intent 4-level grouping etc.) |
| `indicator_category` | Indicator Category | text | The level of the indicator variable assessed by the survey (Many or Almost All Friends and Family Vaccinated, Very or Completely Confident in COVID-19 Vaccine Safety, Vaccinated, etc.) |
| `time_period` | Time Period | text | The dates the telephone interviews were conducted to collect the data on which the estimates were calculated (June 13 – June 19, May 30 – June 26, etc.) |
| `year` | Year | text | The year the telephone interviews were conducted. |
| `time_type` | Time Type | text | Indicates whether the estimate was based on a week of interview data or a month of interview data. |
| `estimate` | Estimate (%) | text | The numerical estimate of the weighted proportion giving the response. |
| `_95_ci` | 95% CI (%) | text | The 95% confidence interval of the estimate. |
| `sample_size` | Sample Size | text | The unweighted number of respondents in the denominator used to calculate the proportion estimates. |
| `new_vax_group` | Vaccine | text | The vaccines: COVID-19, Flu, RSV (All adults 60-74 years with high risk condition), and RSV (All adults 75+ years) |
| `suppression_flag` | Suppression Flag | text |  |

### qz99-wyhv

**National Immunization Survey Adult COVID Module (NIS-ACM): Trends in Behavioral Indicators Among Unvaccinated People** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/qz99-wyhv.json`
- Metadata: `GET https://data.cdc.gov/api/views/qz99-wyhv.json`; page: https://data.cdc.gov/d/qz99-wyhv
- Topics: Category: Vaccinations
- Tags: `covid tracker`, `covid-19 vaccination`, `nis-acm`
- Rows: 42,767. Data updated: 2023-08-03. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: National Immunization Survey-Adult COVID Module (NIS-ACM): CDC is providing information on COVID-19 vaccine confidence to supplement vaccine administration data. Trends in behavioral indicators represent the percent of unvaccinated people responding to each of the indicators by intent status and by week for the national-level view, and by month for the jurisdiction-level view.
- Sample row fields ($limit=1): `geography_type`, `geography`, `group_name`, `group_category`, `indicator_name`, `indicator_category`, `time_period`, `time_year`, `time_type`, `estimate`, `coninf_95`, `sample_size`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `geography_type` | Geography Type | text | The classification (National or Jurisdictional) of geographies. |
| `geography` | Geography | text | The name of the geography for which estimates are calculated. |
| `group_name` | Group Name | text | The name of the variable by which estimates are grouped. (All, Age, Sex, Race/Ethnicity, Health Insurance, Vaccination Status, Vaccination Intent etc.) |
| `group_category` | Group Category | text | The level of each group variable (18 – 29 years, Insured/Not Insured, Urban etc.) |
| `indicator_name` | Indicator Name | text | The indicator variable assessed by the survey (Concern about COVID-19, Confidence in COVID-19 Vaccine Safety, Vaccination and Intent 4 level grouping etc.) |
| `indicator_category` | Indicator Category | text | The level of the indicator variable assessed by the survey (Many or Almost All Friends and Family Vaccinated, Very or Completely Confident in COVID-19 Vaccine Safety, Vaccinated, etc.) |
| `time_period` | Time Period | text | The dates the telephone interviews were conducted to collect the data on which the estimates were calculated (June 13 – June 19, May 30 – June 26, etc.) |
| `time_year` | Year | text | The year the telephone interviews were conducted. |
| `time_type` | Time Type | text | Indicates whether the estimate was based on a week of interview data or a month of interview data. |
| `estimate` | Estimate (%) | text | The numerical estimate of the weighted proportion giving the response. |
| `coninf_95` | 95% CI (%) | text | The 95% confidence interval of the estimate. |
| `sample_size` | Sample Size | text | The unweighted number of respondents in the denominator used to calculate the proportion estimates. |
| `suppression_flag` | Suppression Flag | number | Estimates with sample sizes smaller than 30 people are suppressed (missing) and have a value of 1 for this field. If the estimate had a sample size greater than 30 people, the estimate was not suppressed, and this field has a value of 0. |

### akkj-j5ru

**National Immunization Survey Adult COVID Module (NIS-ACM): Trends in Vaccination Status and Intent** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/akkj-j5ru.json`
- Metadata: `GET https://data.cdc.gov/api/views/akkj-j5ru.json`; page: https://data.cdc.gov/d/akkj-j5ru
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `covid-19 vaccination`, `covid tracker`
- Rows: 9,436. Data updated: 2023-08-03. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: National Immunization Survey-Adult COVID Module (NIS-ACM): CDC is providing information on COVID-19 vaccine confidence to supplement vaccine administration data. These data represent trends in vaccination status and intent by week for the national-level view, and by month for the jurisdiction-level view.
- Sample row fields ($limit=1): `geography_type`, `geography`, `group_name`, `group_category`, `indicator_name`, `indicator_category`, `time_period`, `time_year`, `time_type`, `estimate`, `coninf_95`, `sample_size`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `geography_type` | Geography Type | text | The classification (National or Jurisdictional) of geographies. |
| `geography` | Geography | text | The name of the geography for which estimates are calculated. |
| `group_name` | Group Name | text | The name of the variable by which estimates are grouped. (All, Age, Sex, Race/Ethnicity, Health Insurance, Vaccination Status, Vaccination Intent etc.) |
| `group_category` | Group Category | text | The level of each group variable (18 – 29 years, Insured/Not Insured, Urban etc.) |
| `indicator_name` | Indicator Name | text | The indicator variable assessed by the survey (Concern about COVID-19, Confidence in COVID-19 Vaccine Safety, Vaccination and Intent 4 level grouping etc.) |
| `indicator_category` | Indicator Category | text | The level of the indicator variable assessed by the survey (Many or Almost All Friends and Family Vaccinated, Very or Completely Confident in COVID-19 Vaccine Safety, Vaccinated, etc.) |
| `time_period` | Time Period | text | The dates the telephone interviews were conducted to collect the data on which the estimates were calculated (June 13 – June 19, May 30 – June 26, etc.) |
| `time_year` | Year | text | The year the telephone interviews were conducted. |
| `time_type` | Time Type | text | Indicates whether the estimate was based on a week of interview data or a month of interview data. |
| `estimate` | Estimate (%) | number | The numerical estimate of the weighted proportion giving the response. |
| `coninf_95` | 95% CI (%) | text | The 95% confidence interval of the estimate. |
| `sample_size` | Sample Size | number | The unweighted number of respondents in the denominator used to calculate the proportion estimates. |
| `suppression_flag` | Suppression Flag | number | Estimates with sample sizes smaller than 30 people are suppressed (missing) and have a value of 1 for this field. If the estimate had a sample size greater than 30 people, the estimate was not suppressed, and this field has a value of 0. |

### iwxc-qftf

**National Immunization Survey Adult COVID Module (NIS-ACM): Vaccination Status and Intent by Demographics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/iwxc-qftf.json`
- Metadata: `GET https://data.cdc.gov/api/views/iwxc-qftf.json`; page: https://data.cdc.gov/d/iwxc-qftf
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `covid tracker`, `covid-19 vaccination`
- Rows: 165,474. Data updated: 2023-08-03. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: National Immunization Survey Adult COVID Module (NIS-ACM): CDC is providing information on COVID-19 vaccine confidence to supplement vaccine administration data. These data represent trends in vaccination status and intent by demographics. Following collection of August 2021 survey data, an error in data processing led to incorrect categorization of some survey respondents; some respondents who should have been categorized as MSA: Principal City instead were categorized as MSA: Non-Principal City. Data downloaded during the period September 12, 2021 through September 30, 2021 may have incorre…
- Sample row fields ($limit=1): `geography_type`, `geography`, `group_name`, `group_category`, `indicator_name`, `indicator_category`, `time_period`, `time_year`, `time_type`, `estimate`, `coninf_95`, `sample_size`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `geography_type` | Geography Type | text | The classification (National or Jurisdictional) of geographies. |
| `geography` | Geography | text | The name of the geography for which estimates are calculated |
| `group_name` | Group Name | text | The name of the variable by which estimates are grouped. (All, Age, Sex, Race/Ethnicity, Health Insurance, Vaccination Status, Vaccination Intent etc.) |
| `group_category` | Group Category | text | The level of each group variable (18 – 29 years, Insured/Not Insured, Urban etc.) |
| `indicator_name` | Indicator Name | text | The indicator variable assessed by the survey (Concern about COVID-19, Confidence in COVID-19 Vaccine Safety, Vaccination and Intent 4 level grouping etc.) |
| `indicator_category` | Indicator Category | text | The level of the indicator variable assessed by the survey (Many or Almost All Friends and Family Vaccinated, Very or Completely Confident in COVID-19 Vaccine Safety, Vaccinated, etc.) |
| `time_period` | Time Period | text | The dates the telephone interviews were conducted to collect the data on which the estimates were calculated (June 13 – June 19, May 30 – June 26, etc.) |
| `time_year` | Year | text | The year the telephone interviews were conducted. |
| `time_type` | Time Type | text | Indicates whether the estimate was based on a week of interview data or a month of interview data. |
| `estimate` | Estimate (%) | text | The numerical estimate of the weighted proportion giving the response |
| `coninf_95` | 95% CI (%) | text | The 95% confidence interval of the estimate |
| `sample_size` | Sample Size | text | The unweighted number of respondents in the denominator used to calculate the proportion estimates. |
| `suppression_flag` | Suppression Flag | number | Estimates with sample sizes smaller than 30 people are suppressed (missing) and have a value of 1 for this field. If the estimate had a sample size greater than 30 people, the estimate was not suppressed, and this field has a value of 0. |

### uny6-e3dx

**National Immunization Survey Child COVID Module (NIS-CCM): COVIDVaxViews| Data | Centers for Disease Control and Prevention (cdc.gov)-Archived** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/uny6-e3dx.json`
- Metadata: `GET https://data.cdc.gov/api/views/uny6-e3dx.json`; page: https://data.cdc.gov/d/uny6-e3dx
- Topics: Category: Vaccinations
- Tags: `nis-ccm`, `covid-19 vaccination`, `vaxviews`, `vaccination`, `immunization`, `vaccination coverage`, `covid-19`, `vaccine confidence`
- Rows: 45,635. Data updated: 2024-01-18. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: National Immunization Survey Child COVID Module (NIS-CCM): CDC is providing information on COVID-19 vaccine confidence to supplement vaccine administration data. These data represent trends in vaccination status and intent, and other behavioral indicators, by demographics and other characteristics.
- Sample row fields ($limit=1): `geography_type`, `geography`, `age_range`, `group_name`, `group_category`, `indicator_name`, `indicator_category`, `time_year`, `time_type`, `time_period`, `estimate`, `coninf_95`, `sample_size`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `geography_type` | Geography Type | text | The classification (National) of geographies. |
| `geography` | Geography | text | The name of the geography for which estimates are calculated. |
| `age_range` | Age Range | text | The age range of the child of the adult respondent. |
| `group_name` | Group Name | text | The name of the variable by which estimates are grouped. (All, Age, Sex, Race/Ethnicity, Health Insurance, Vaccination Status, Vaccination Intent, etc.) |
| `group_category` | Group Category | text | The level of each group variable (12-17 years, Uninsured, Urban etc.) |
| `indicator_name` | Indicator Name | text | The indicator variable assessed by the survey (Concern about COVID-19, Confidence in COVID-19 Vaccine Safety, Vaccination and Intent 4-level grouping etc.) |
| `indicator_category` | Indicator Category | text | The level of the indicator variable assessed by the survey (Very or Completely Confident in COVID-19 Vaccine Safety, Vaccinated, etc.) |
| `time_year` | Year | text | The year the telephone interviews were conducted. |
| `time_type` | Time Type | text | Indicates that the estimate was based on a month of interview data. |
| `time_period` | Time Period | text | The dates the telephone interviews were conducted to collect the data on which the estimates were calculated (May 30 – June 26, October 26 – November 30). |
| `estimate` | Estimate (%) | number | The numerical estimate of the weighted proportion giving the response. |
| `coninf_95` | 95% CI | text | The 95% confidence interval of the estimate. |
| `sample_size` | Sample Size | number | The unweighted number of respondents in the denominator used to calculate the proportion estimates. This column will be blank/missing where Suppression Flag has a value of 1. |
| `suppression_flag` | Suppression Flag | number | Estimates with sample sizes smaller than 30 people are suppressed (missing) and have a value of 1 for this field. If the estimate had a sample size greater than 30 people, the estimate was not suppressed, and this field has a value of 0. |

### gr26-95h2

**National Immunization Survey Child COVID Module (NIS-CCM): Vaccination Status and Intent by Demographics | Data | Centers for Disease Control and Prevention (cdc.gov)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/gr26-95h2.json`
- Metadata: `GET https://data.cdc.gov/api/views/gr26-95h2.json`; page: https://data.cdc.gov/d/gr26-95h2
- Topics: Category: Vaccinations
- Tags: `nis-ccm`, `covid tracker`, `covid-19 vaccination`
- Rows: 8,609. Data updated: 2023-08-03. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: National Immunization Survey Child COVID Module (NIS-CCM): CDC is providing information on COVID-19 vaccine confidence to supplement vaccine administration data. These data represent trends in vaccination status and intent, and other behavioral indicators, by demographics and other characteristics.
- Sample row fields ($limit=1): `geography_type`, `geography`, `age_range`, `group_name`, `group_category`, `indicator_name`, `indicator_category`, `time_period`, `time_year`, `time_type`, `estimate`, `coninf_95`, `sample_size`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `geography_type` | Geography Type | text | The classification (National) of geographies. |
| `geography` | Geography | text | The name of the geography for which estimates are calculated. |
| `age_range` | Age Range | text | The age range of the child of the adult respondent. |
| `group_name` | Group Name | text | The name of the variable by which estimates are grouped. (All, Age, Sex, Race/Ethnicity, Health Insurance, Vaccination Status, Vaccination Intent, etc.) |
| `group_category` | Group Category | text | The level of each group variable (12-17 years, Insured/Not Insured, Urban etc.) |
| `indicator_name` | Indicator Name | text | The indicator variable assessed by the survey (Concern about COVID-19, Confidence in COVID-19 Vaccine Safety, Vaccination and Intent 4-level grouping etc.) |
| `indicator_category` | Indicator Category | text | The level of the indicator variable assessed by the survey (Very or Completely Confident in COVID-19 Vaccine Safety, Vaccinated, etc.) |
| `time_period` | Time Period | text | The dates the telephone interviews were conducted to collect the data on which the estimates were calculated (May 30 – June 26, October 26 – November 30) |
| `time_year` | Year | text | The year the telephone interviews were conducted. |
| `time_type` | Time Type | text | Indicates that the estimate was based on a month of interview data. |
| `estimate` | Estimate (%) | number | The numerical estimate of the weighted proportion giving the response. |
| `coninf_95` | 95% CI (%) | text | The 95% confidence interval of the estimate. |
| `sample_size` | Sample Size | number | The unweighted number of respondents in the denominator used to calculate the proportion estimates. This column will be blank/missing where Suppression Flag has a value of 1. |
| `suppression_flag` | Suppression Flag | number | Estimates with sample sizes smaller than 30 people are suppressed (missing) and have a value of 1 for this field. If the estimate had a sample size greater than 30 people, the estimate was not suppressed, and this field has a value of 0. |

### ee83-ukst

**National Immunization Survey Fall Respiratory Virus Module (NIS-FRVM): RespVaxView| Data | Centers for Disease Control and Prevention (cdc.gov)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ee83-ukst.json`
- Metadata: `GET https://data.cdc.gov/api/views/ee83-ukst.json`; page: https://data.cdc.gov/d/ee83-ukst
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `covid-19 vaccination`, `vaccine confidence`, `rsv vaccination`, `vaccination`, `vaccination coverage`, `flu vaccination`
- Rows: 544,489. Data updated: 2026-03-04. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • National Immunization Survey Fall Respiratory Virus Module (NIS-FRVM): CDC is providing information on the updated 2025-26 COVID-19 vaccine, the 2025-26 seasonal flu vaccine, and the RSV vaccine uptake and confidence. These data represent trends in vaccination status and intent, and other behavioral indicators, by demographics and other characteristics. • The data start in October 2025. • The archived data can be found here: - 2024-25 season: https://data.cdc.gov/Vaccinations/National-Immunization-Survey-Adult-COVID-Module-NI/si7g-c2bs/about_data - 2023-24 season: https://data.cdc.gov/Vacci…
- Sample row fields ($limit=1): `geographic_level`, `geographic_label`, `dsss_group_variable_name`, `dsss_group_variable_category`, `dsss_indicator_label`, `dsss_indicator_category_label`, `dsss_timeperiodlabel`, `dsss_year`, `dsss_timetype`, `dsss_value`, `dsss_confidenceinterval`, `sample_size`, `new_vax_group`, `suppressionflag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `geographic_level` | Geography Type | text | The classification (National, Regional, or Jurisdictional) of geographies. |
| `geographic_label` | Geography | text | The name of the geography for which estimates are calculated. |
| `dsss_group_variable_name` | Group Name | text | The name of the variable by which estimates are grouped. (All, Age, Sex, Race/Ethnicity, Health Insurance, Vaccination Status, Vaccination Intent, etc.) |
| `dsss_group_variable_category` | Group Category | text | The level of each group variable (18–29 years, Insured/Not Insured, Urban etc.) |
| `dsss_indicator_label` | Indicator Name | text | The indicator variable assessed by the survey (Concern about COVID-19, Confidence in COVID-19 Vaccine Safety, Vaccination and Intent 4-level grouping etc.) |
| `dsss_indicator_category_label` | Indicator Category | text | The level of the indicator variable assessed by the survey (Many or Almost All Friends and Family Vaccinated, Very or Completely Confident in COVID-19 Vaccine Safety, Vaccinated, etc.) |
| `dsss_timeperiodlabel` | Time Period | text | The dates the telephone interviews were conducted to collect the data on which the estimates were calculated (June 13 – June 19, May 30 – June 26, etc.) |
| `dsss_year` | Year | text | The year the telephone interviews were conducted. |
| `dsss_timetype` | Time Type | text | Indicates whether the estimate was based on a week of interview data or a month of interview data. |
| `dsss_value` | Estimate (%) | number | The numerical estimate of the weighted proportion giving the response. |
| `dsss_confidenceinterval` | 95% CI (%) | text | The 95% confidence interval of the estimate. |
| `sample_size` | Sample Size | number | The unweighted number of respondents in the denominator used to calculate the proportion estimates. |
| `new_vax_group` | Vaccine | text | The vaccines: COVID-19, Flu, RSV (All adults 50-74 years with high risk condition), and RSV (All adults 75+ years) |
| `suppressionflag` | Suppression Flag | number |  |

### 94wp-9pid

**Vaccination Concerns, Issues, and Motivators | RespVaxView | Data | Centers for Disease Control and Prevention (cdc.gov)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/94wp-9pid.json`
- Metadata: `GET https://data.cdc.gov/api/views/94wp-9pid.json`; page: https://data.cdc.gov/d/94wp-9pid
- Topics: Category: Vaccinations
- Tags: `flu vaccination`, `covid-19 vaccination`, `rsv vaccination`
- Rows: 14,942. Data updated: 2026-10-16. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • CDC is providing information on COVID-19, flu, and RSV vaccination concerns, issues, and motivators to supplement weekly vaccination data. These monthly data represent trends in vaccination concerns, issues, and motivators, by demographics and other characteristics. • The data start in August 2024.
- Sample row fields ($limit=1): `vaccine`, `demo_group`, `demo_label`, `indicator_group`, `indicator_level`, `estimate`, `denominator`, `month_label`, `timeframe_survey`, `dashboard_type`, `suppression_flag`, `season`, `trend_month`, `trend_label`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | Vaccine | text | The vaccines: COVID-19, Flu, and RSV |
| `demo_group` | demo_group | text | Demographic category group (Overall, age, race and ethnicity, urbanicity, insurance status, vaccination coverage and intent) |
| `demo_label` | demo_category | text | Level of specific demographic group (Overall: overall; Age: 18-49 years, 50-64 years, 65+ years; Race and ethnicity: Hispanic, White, non-Hispanic, Black, non-Hispanic, Other or multiple races, non-Hispanic; Urbanicity: urban, suburban, ru… |
| `indicator_group` | Indicator_group | text | Concern/motivator category |
| `indicator_level` | Indicator_category | text | Specific concern/motivator |
| `estimate` | Estimate | text | Weighted estimate (%) |
| `lower_ci` | Lower_ci | text | Lower bound of the 95% CI |
| `upper_ci` | Upper_ci | text | Upper bound of the 95% CI |
| `denominator` | Unweighted Sample Size | text | Unweighted sample size |
| `month_label` | Month_label | text | Data Month |
| `timeframe_survey` | Timeframe_survey | text | The date range when the survey was conducted |
| `dashboard_type` | Dashboard_type | text | Indicator type: Issues/concerns or motivators |
| `suppression_flag` | Suppression_flag | text |  |
| `season` | season | text | Respiratory disease season |
| `trend_month` | trend_month | text | Month used in trend graph |
| `trend_label` | trend_label | text | The legend label for the trend graph |

### aetd-68ew

**Vaccination Coverage among Adults (18+ Years)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/aetd-68ew.json`
- Metadata: `GET https://data.cdc.gov/api/views/aetd-68ew.json`; page: https://data.cdc.gov/d/aetd-68ew
- Topics: Category: Vaccinations
- Tags: `vaxviews`, `vaccination`, `immunization`, `vaccination coverage`, `pneumococcal`, `td`, `tdap`, `zoster`, `shingles`
- Rows: 67,596. Data updated: 2026-03-11. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Vaccination Coverage among Adults (18+ Years) • Data on adult vaccination coverage from the Behavioral Risk Factor Surveillance System (BRFSS) for the general population at the national, regional, and state levels by age groups. • Additional information available at https://www.cdc.gov/vaccines/imz-managers/coverage/adultvaxview/index.html
- Sample row fields ($limit=1): `vaccine`, `dose`, `geography_type`, `geography`, `fips`, `year_season`, `dimension_type`, `dimension`, `coverage_estimate`, `_95_ci`, `population_sample_size`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | Vaccine | text | The name of the vaccine for which estimates are calculated |
| `dose` | Dose | text | The type of Tetanus shot (Tdap, Td or Tdap) |
| `geography_type` | Geography Type | text | The classification (HHS Region/National, State/Local Area, County) of geographies available. |
| `geography` | Geography | text | The name of the geography for which estimates are calculated. |
| `fips` | FIPS | text | The American National Standards Institute (ANSI)’s Federal Information Processing Series code. The codes are alphabetically assigned by geographic name. States have 2-digits codes, and counties have 5-digit codes comprising of the 2-digit… |
| `year_season` | Survey Year | text | The survey year for which estimates are calculated. |
| `dimension_type` | Dimension Type | text | The classification of the sociodemographic category for which estimates are calculated for each Vaccine Group. For adults, the two applicable types are "Age" and "Race/ethnicity." |
| `dimension` | Dimension | text | The sociodemographic group for which estimates are calculated. |
| `coverage_estimate` | Estimate (%) | text | The estimated vaccination coverage. Non-numeric data are present in this column, such as "*". These symbols indicate if data were not collected, |
| `_95_ci` | 95% CI (%) | text | The 95% confidence interval of the estimate of vaccination coverage. |
| `population_sample_size` | Sample Size | text | The size of the sample surveyed to create the estimate for each vaccine, geography, and dimension grouping. |

### xerk-pcm8

**Vaccination Coverage among Health Care Personnel** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/xerk-pcm8.json`
- Metadata: `GET https://data.cdc.gov/api/views/xerk-pcm8.json`; page: https://data.cdc.gov/d/xerk-pcm8
- Topics: Category: Vaccinations
- Tags: `vaxviews`, `vaccination`, `immunization`, `vaccination coverage`, `flu vaccination`, `influenza`
- Rows: 1,456. Data updated: 2024-09-12. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Vaccination Coverage among Health Care Personnel • Data on influenza vaccination performance measurement from the National Healthcare Safety Network (NHSN) for hospital-based health care personnel (HCP) at the national and state levels by personnel group. • Additional information available at https://www.cdc.gov/flu/fluvaxview/index.htm
- Sample row fields ($limit=1): `vaccine`, `geography_type`, `geography`, `year_season`, `dimension`, `coverage_estimate`, `population_sample_size`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | Vaccine | text | The name of the vaccine for which estimates are calculated. |
| `geography_type` | Geography Type | text | The classification (National, State) of geographies available. |
| `geography` | Geography | text | The name of the geography for which estimates are calculated. |
| `year_season` | Season | text | The influenza season for which estimates are calculated. |
| `dimension` | Personnel Type | text | The personnel classification for which estimates are calculated. |
| `coverage_estimate` | Estimate (%) | number | The estimated vaccination coverage. Non-numeric data are present in this column as "NR," which indicates the estimate was not reported. |
| `_95_ci` | 95% CI (%) | text | The 95% confidence interval of the estimate of vaccination coverage. |
| `population_sample_size` | Sample Size | number | The size of the sample surveyed to create the estimate for each vaccine, geography, dimension grouping. In the main VaxViews data set, this column is titled “Population/Sample Size.” |

### 8w4j-reb4

**Vaccination Coverage among Nursing Home Residents** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8w4j-reb4.json`
- Metadata: `GET https://data.cdc.gov/api/views/8w4j-reb4.json`; page: https://data.cdc.gov/d/8w4j-reb4
- Topics: Category: Vaccinations
- Tags: `vaxviews`, `vaccination`, `immunization`, `vaccination coverage`, `nursing home vaccination`, `influenza`, `pneumococcal`
- Rows: 44,518. Data updated: 2024-09-12. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Vaccination Coverage among Nursing Home Residents • Data on influenza and pneumococcal vaccination coverage from the Long-Term Care Minimum Data Set (MDS) from the Centers for Medicare & Medicaid Services (CMS) at the national, regional, and state levels by sociodemographic characteristics. • Additional information available at https://www.cdc.gov/vaccines/imz-managers/coverage/adultvaxview/index.html and https://www.cdc.gov/flu/fluvaxview/index.htm
- Sample row fields ($limit=1): `vaccine`, `geography_type`, `geography`, `year_season`, `dimension_type`, `dimension`, `coverage_estimate`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | Vaccine | text | The name of the vaccine for which estimates are calculated. |
| `geography_type` | Geography Type | text | The classification (HHS Region/National, State) of geographies available. |
| `geography` | Geography | text | The name of the geography for which estimates are calculated. |
| `year_season` | Survey Year/Influenza Season | text | The time period for which estimates are calculated. For pneumococcal data, information is aggregated by survey year. For influenza data, information is aggregated by influenza season. In the main VaxViews data set, this column is titled “Y… |
| `dimension_type` | Dimension Type | text | The classification of the sociodemographic category for which estimates are calculated. |
| `dimension` | Dimension | text | The sociodemographic group for which estimates are calculated. |
| `coverage_estimate` | Estimate (%) | text | The estimated vaccination coverage. Non-numeric data are present in this column, such as "NA" and "NR." These data indicate whether an estimate is not applicable or not reported. |
| `population_sample_size` | Population Size | text | The size of the population surveyed for each vaccine, geography, dimension grouping. A population size is provided as nursing home data come from a census. |

### ijqb-a7ye

**Vaccination Coverage and Exemptions among Kindergartners** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ijqb-a7ye.json`
- Metadata: `GET https://data.cdc.gov/api/views/ijqb-a7ye.json`; page: https://data.cdc.gov/d/ijqb-a7ye
- Topics: Category: Vaccinations
- Tags: `vaxviews`, `vaccination`, `immunization`, `school vaccination`, `school exemption`, `vaccination coverage`, `mmr`, `dtap`, `dt`, `dtp`, `varicella`, `hepatitis b`, `polio`, `any exemption`, `medical exemption`, `non-medical exemption`
- Rows: 8,753. Data updated: 2026-08-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Vaccination Coverage and Exemptions among Kindergartners • Data on school vaccination coverage and exemptions from the School Vaccination Assessment Program for kindergartners at the national and state levels. • Additional information available at https://www.cdc.gov/vaccines/imz-managers/coverage/schoolvaxview/index.html
- Sample row fields ($limit=1): `vaccine`, `dose`, `geography_type`, `geography`, `year_season`, `coverage_estimate`, `population_sample_size`, `percent_surveyed`, `foot_notes`, `survey_type`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | Vaccine/Exemption | text | The name of the vaccine or exemption type for which estimates are calculated. Exemptions only exist within Kindergartner data. |
| `dose` | Dose | text | This dose is only applicable for vaccination coverage. For vaccines, it shows dose of vaccine (≥1, ≥2, ≥3, ≥4) for which coverage is estimated. |
| `geography_type` | Geography Type | text | The classification (National, State) of geographies available. |
| `geography` | Geography | text | The name of the geography for which estimates are calculated. |
| `year_season` | School Year | text | The school year for which estimates are calculated. |
| `coverage_estimate` | Estimate (%) | text | The estimated vaccination coverage or prevalence of exemptions among all children enrolled in Kindergarten. Non-numeric data are present in this column, such as "NA" and "NReq." These data indicate whether an estimate is not applicable or… |
| `population_sample_size` | Population Size | text | The total number of children enrolled in kindergarten in by a state/local area for a given year. |
| `percent_surveyed` | Percent Surveyed | text | The percent of children enrolled in kindergarten surveyed by a state/local area for a given year. |
| `foot_notes` | Footnotes | text | Symbols used within this field indicate particular footnotes about the estimate reliability, sample size, confidence intervals, or survey methodology. For more information on the meaning of these symbols, refer to the Footnotes in the "Abo… |
| `number_of_exemptions` | Number of Exemptions | text | The number of vaccine exemptions among Kindergarteners. |
| `survey_type` | Survey Type | text | The description of the population used to create estimates by state/local area for a given year. Some states conduct a census and others a survey. More information is available at https://www.cdc.gov/vaccines/imz-managers/coverage/schoolva… |

### q9mh-h2tw

**Vaccine Hesitancy for COVID-19: County and local estimates** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/q9mh-h2tw.json`
- Metadata: `GET https://data.cdc.gov/api/views/q9mh-h2tw.json`; page: https://data.cdc.gov/d/q9mh-h2tw
- Topics: Category: Vaccinations
- Tags: `coronavirus`, `covid-19`, `vaccine hesitancy`
- Rows: 3,142. Data updated: 2021-06-17. Probe status: 200.
- Update frequency: Monthly.
- Source: HHS ASPE
- Description: Due to the change in the survey instrument regarding intention to vaccinate, our estimates for “hesitant or unsure” or “hesitant” derived from April 14-26, 2021, are not directly comparable with prior Household Pulse Survey data and should not be used to examine trends in hesitancy. To support state and local communication and outreach efforts, ASPE developed state, county, and sub-state level predictions of hesitancy rates (https://aspe.hhs.gov/pdf-report/vaccine-hesitancy) using the most recently available federal survey data. We estimate hesitancy rates at the state level using the U.S. Ce…
- Sample row fields ($limit=1): `fips_code`, `county_name`, `state`, `estimated_hesitant`, `estimated_hesitant_or_unsure`, `estimated_strongly_hesitant`, `social_vulnerability_index`, `svi_category`, `ability_to_handle_a_covid`, `cvac_category`, `percent_adults_fully`, `percent_hispanic`, `percent_non_hispanic_american`, `percent_non_hispanic_asian`, `percent_non_hispanic_black`, `percent_non_hispanic_native`, `percent_non_hispanic_white`, `geographical_point`, `state_code`, `county_boundary`, `state_boundary`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `fips_code` | FIPS Code | text | FIPS codes are numbers which uniquely identify geographic areas |
| `county_name` | County Name | text | Name of County |
| `state` | State | text | State |
| `estimated_hesitant` | Estimated hesitant | number | Estimate of percentage of adults who describe themselves as “probably not” or “definitely not” going to get a COVID-19 vaccine once one is available to them, based on national survey data. |
| `estimated_hesitant_or_unsure` | Estimated hesitant or unsure | number | Estimate of percentage of adults who describe themselves as “unsure”, “probably not”, or “definitely not” going to get a COVID-19 vaccine once one is available to them, based on national survey data. |
| `estimated_strongly_hesitant` | Estimated strongly hesitant | number | Estimate of percentage of adults who describe themselves as “definitely not” going to get a COVID-19 vaccine once one is available to them, based on national survey data. |
| `social_vulnerability_index` | Social Vulnerability Index (SVI) | number | SVI values range from 0 (least vulnerable) to 1 (most vulnerable). |
| `svi_category` | SVI Category | text | SVI categorized as follows: Very Low (0.0-0.19), Low (0.20-0.39); Moderate (0.40-0.59); High (0.60-0.79); Very High (0.80-1.0) |
| `ability_to_handle_a_covid` | CVAC level of concern for vaccination rollout | number | CVAC Index values range from 0 (lowest concern) to 1 (highest concern) |
| `cvac_category` | CVAC Level Of Concern | text | CVAC categorized as follows: Very Low (0.0-0.19), Low (0.20-0.39); Moderate (0.40-0.59); High (0.60-0.79); Very High (0.80-1.0) |
| `percent_adults_fully` | Percent adults fully vaccinated against COVID-19 (as of 6/10/21) | number | Percent of Adults fully vaccinated against COVID-19 |
| `percent_hispanic` | Percent Hispanic | number | Percent of county population that is Hispanic |
| `percent_non_hispanic_american` | Percent non-Hispanic American Indian/Alaska Native | number | Percent of county population that is non-Hispanic American Indian/Alaska Native |
| `percent_non_hispanic_asian` | Percent non-Hispanic Asian | number | Percent of county population that is non-Hispanic Asian |
| `percent_non_hispanic_black` | Percent non-Hispanic Black | number | Percent of county population that is non-Hispanic Black |
| `percent_non_hispanic_native` | Percent non-Hispanic Native Hawaiian/Pacific Islander | number | Percent of county population that is non-Hispanic Native Hawaiian/Pacific Islander |
| `percent_non_hispanic_white` | Percent non-Hispanic White | number | Percent of county population that is non-Hispanic White |
| `geographical_point` | Geographical Point | point |  |
| `state_code` | State Code | text |  |
| `county_boundary` | County Boundary | multipolygon |  |
| `state_boundary` | State Boundary | multipolygon |  |

### djj9-kh3p

**Vaccine Hesitancy for COVID-19: Public Use Microdata Areas (PUMAs)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/djj9-kh3p.json`
- Metadata: `GET https://data.cdc.gov/api/views/djj9-kh3p.json`; page: https://data.cdc.gov/d/djj9-kh3p
- Topics: Category: Vaccinations
- Tags: `coronavirus`, `covid-19`, `vaccine hesitancy`
- Rows: 2,351. Data updated: 2021-06-17. Probe status: 200.
- Update frequency: Monthly.
- Source: HHS ASPE
- Description: Due to the change in the survey instrument regarding intention to vaccinate, our estimates for “hesitant or unsure” or “hesitant” derived from April 14-26, 2021, are not directly comparable with prior Household Pulse Survey data and should not be used to examine trends in hesitancy. To support state and local communication and outreach efforts, ASPE developed state, county, and sub-state level predictions of hesitancy rates(https://aspe.hhs.gov/pdf-report/vaccine-hesitancy) using the most recently available federal survey data. We estimate hesitancy rates at the state level using the U.S. Cen…
- Sample row fields ($limit=1): `puma_code`, `puma_name`, `state`, `estimated_hesitant`, `estimated_unsure_or_hesitant`, `estimated_strongly_hesitant`, `percent_hispanic`, `percent_non_hispanic_american`, `percent_non_hispanic_asian`, `percent_non_hispanic_black`, `percent_non_hispanic_native`, `percent_non_hispanic_white`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `puma_code` | PUMA Code | number | Public Use Microdata Areas |
| `puma_name` | PUMA Name | text | Public Use Microdata Areas Name |
| `state` | State | text | State |
| `estimated_hesitant` | Estimated hesitant | number | Estimate of percentage of adults who describe themselves as “probably not” or “definitely not” going to get a COVID-19 vaccine once one is available to them, based on national survey data. |
| `estimated_unsure_or_hesitant` | Estimated unsure or hesitant | number | Estimate of percentage of adults who describe themselves as “unsure”, “probably not”, or “definitely not” going to get a COVID-19 vaccine once one is available to them, based on national survey data |
| `estimated_strongly_hesitant` | Estimated strongly hesitant | number | Estimate of percentage of adults who describe themselves as “definitely not” going to get a COVID-19 vaccine once one is available to them, based on national survey data. |
| `percent_hispanic` | Percent Hispanic | number | Percent of PUMA population that is Hispanic |
| `percent_non_hispanic_american` | Percent non-Hispanic American Indian/Alaska Native | number | Percent of PUMA population that is non-Hispanic American Indian/Alaska Native |
| `percent_non_hispanic_asian` | Percent non-Hispanic Asian | number | Percent of PUMA population that is non-Hispanic Asian |
| `percent_non_hispanic_black` | Percent non-Hispanic Black | number | Percent of PUMA population that is non-Hispanic Black |
| `percent_non_hispanic_native` | Percent non-Hispanic Native Hawaiian/Pacific Islander | number | Percent of PUMA population that is non-Hispanic Native Hawaiian/Pacific Islander |
| `percent_non_hispanic_white` | Percent non-Hispanic White | number | Percent of PUMA population that is non-Hispanic White |

### 5jp2-pgaw

**Vaccines.gov: COVID-19 vaccinating provider locations** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/5jp2-pgaw.json`
- Metadata: `GET https://data.cdc.gov/api/views/5jp2-pgaw.json`; page: https://data.cdc.gov/d/5jp2-pgaw
- Topics: Category: Vaccinations
- Tags: `vaccinefinder`, `covid-19`, `vaccines`, `vaccination sites`, `vaccination locations`, `providers`
- Rows: 253,144. Data updated: 2024-08-01. Probe status: 200.
- Description: Because inventory reporting is no longer required, Vaccines.gov information will not be updated on this site after July 2024.
- Sample row fields ($limit=1): `provider_location_guid`, `loc_store_no`, `loc_phone`, `loc_name`, `loc_admin_street1`, `loc_admin_city`, `loc_admin_state`, `loc_admin_zip`, `sunday_hours`, `monday_hours`, `tuesday_hours`, `wednesday_hours`, `thursday_hours`, `friday_hours`, `saturday_hours`, `web_address`, `pre_screen`, `insurance_accepted`, `walkins_accepted`, `provider_notes`, `ndc`, `med_name`, `in_stock`, `supply_level`, `quantity_last_updated`, `latitude`, `longitude`, `category`, `offers_free_masks`, `min_age_months`, `min_age_years`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `provider_location_guid` | provider_location_guid | text |  |
| `loc_store_no` | loc_store_no | text |  |
| `loc_phone` | loc_phone | text |  |
| `loc_name` | loc_name | text |  |
| `loc_admin_street1` | loc_admin_street1 | text |  |
| `loc_admin_street2` | loc_admin_street2 | text |  |
| `loc_admin_city` | loc_admin_city | text |  |
| `loc_admin_state` | loc_admin_state | text |  |
| `loc_admin_zip` | loc_admin_zip | text |  |
| `sunday_hours` | sunday_hours | text |  |
| `monday_hours` | monday_hours | text |  |
| `tuesday_hours` | tuesday_hours | text |  |
| `wednesday_hours` | wednesday_hours | text |  |
| `thursday_hours` | thursday_hours | text |  |
| `friday_hours` | friday_hours | text |  |
| `saturday_hours` | saturday_hours | text |  |
| `web_address` | web_address | text |  |
| `pre_screen` | pre_screen | text |  |
| `insurance_accepted` | insurance_accepted | checkbox |  |
| `walkins_accepted` | walkins_accepted | checkbox |  |
| `provider_notes` | provider_notes | text |  |
| `ndc` | ndc | text |  |
| `med_name` | med_name | text |  |
| `in_stock` | in_stock | checkbox |  |
| `supply_level` | supply_level | number |  |
| `quantity_last_updated` | quantity_last_updated | text |  |
| `latitude` | latitude | text |  |
| `longitude` | longitude | text |  |
| `category` | Category | text |  |
| `unnamed_column` | Unnamed Column | text |  |
| `offers_free_masks` | offers_free_masks | checkbox |  |
| `min_age_months` | min_age_months | text |  |
| `min_age_years` | min_age_years | text |  |
| `bridge_access_program` | bridge_access_program | text |  |

### eanj-9nie

**Weekly Cumulative COVID-19 Vaccination Coverage Map and Comparison Between 2025–26 and Previous Seasons, Overall, by Jurisdiction Among Adults 18 Years** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/eanj-9nie.json`
- Metadata: `GET https://data.cdc.gov/api/views/eanj-9nie.json`; page: https://data.cdc.gov/d/eanj-9nie
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `vsd`, `iqvia`, `covid-19 vaccination`, `iis-child`, `iis-adult`, `nis-child`, `cms`
- Rows: 2,894. Data updated: 2026-03-04. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • Weekly COVID-19 Vaccination Coverage of Adults 18 Years and Older by Jurisdiction • Weekly estimates of COVID-19 vaccination coverage and intent for vaccination among adults are calculated using data from the National Immunization Surveys (NIS)-Fall Respiratory Virus Module (NIS-FRVM) (https://www.cdc.gov/nis/about/index.html). • The NIS–FRVM is an ongoing random-digit-dial cellular telephone survey of households with adults 18 years and older. All estimates are based upon self-reported receipt of vaccination and month of that vaccination. • Weekly comparisons to previous season should take…
- Sample row fields ($limit=1): `geography_name`, `geography_level`, `demographic_level`, `demographic_name`, `curr_season`, `past_season`, `past_season_week_ending_date`, `season_filter_text`, `curr_est`, `current_season_week_ending_date`, `past_est`, `curr_ci_halfwidth`, `past_ci_halfwidth`, `difference_estimate`, `significance`, `curr_ci_95`, `past_ci_95`, `diff_cl_95`, `difference_indicator`, `difference_legend_sort`, `binrangetext`, `binrangeorder`, `geography_name_order`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `geography_name` | Geography_name | text | Geography Name |
| `geography_level` | Geography_level | text | Geography Level (National, Region, State) |
| `demographic_level` | Demographic_Level | text | Demographic level |
| `demographic_name` | Demographic_Name | text | Demographic name |
| `curr_season` | Curr_season | text | Current COVID Season |
| `past_season` | Past_season | text | Past COVID season |
| `past_season_week_ending_date` | past_week_ending | text | Past Season Week Ending Date |
| `season_filter_text` | Season_filter_text | text | Season Comparison Filter/Dropdown Text |
| `curr_est` | Curr_est | number | Current Season Estimate |
| `current_season_week_ending_date` | Current_season_Week_Ending | calendar_date | Current Season Week Ending Date |
| `past_est` | Past_est | text | Past Season Estimates |
| `curr_ci_halfwidth` | Curr_CI_HalfWidth | number | Current Season 95% Confidence Interval Half-Width |
| `past_ci_halfwidth` | Past_CI_HalfWidth | text | Past Season 95% Confidence Interval Half-Width |
| `difference_estimate` | Difference_estimate | text | Estimate difference |
| `significance` | Significance | text | Statistical significance |
| `curr_ci_95` | Curr_CI_95 | text | Current Season Coverage 95% Confidence Interval |
| `past_ci_95` | Past_CI_95 | text | Past Season Coverage 95% Confidence Interval |
| `diff_cl_95` | diff_CI_95 | text | Difference in Coverage 95% Confidence Interval |
| `difference_indicator` | Difference_indicator | text | Statistically Significant Difference Indicator Label |
| `difference_legend_sort` | Difference_legend_sort | number | Statistically Significant Difference Indicator Label Sort Order |
| `binrangetext` | BinRangeText | text | Map Color-Coding Bin Range |
| `binrangeorder` | BinRangeOrder | number | Map Color-Coding Bin Range Order |
| `geography_name_order` | Geography_name_order | number | Geography name sort order |

### jjpx-mxt8

**Weekly Cumulative COVID-19 Vaccination Coverage, by Season and Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥65 years** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/jjpx-mxt8.json`
- Metadata: `GET https://data.cdc.gov/api/views/jjpx-mxt8.json`; page: https://data.cdc.gov/d/jjpx-mxt8
- Topics: Category: Vaccinations
- Tags: `covid-19 vaccination`, `nis`, `vsd`, `iqvia`, `iis`
- Rows: 792. Data updated: 2026-05-20. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • COVID-19 vaccination coverage among Medicare fee-for-service beneficiaries aged 65 years and older is assessed using data files from the Medicare Fee-For-Service (FFS) administrative claims data managed by the Centers for Medicare & Medicaid Services (CMS). • Weekly COVID-19 vaccination coverage estimates were calculated using Kaplan-Meier survival analysis, based on beneficiaries enrolled as of August 1 of each year. For the 2025 ̶ 26 season, COVID-19 vaccines received since August 27, 2025, were included.*
- Sample row fields ($limit=1): `week_ending`, `covid_19_season`, `estimate`, `mmwr_year`, `mmwr_week`, `enrollment_date`, `race_and_ethnicity`, `current_season_week_ending`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week Ending | calendar_date | Week Ending |
| `covid_19_season` | COVID-19_Season | text | COVID-19 Vaccine |
| `estimate` | Estimate | number | Weekly percent coverage |
| `mmwr_year` | MMWR_Year | number | Week Ending MMWR Year |
| `mmwr_week` | MMWR_Week | number | Week Ending MMWR Week |
| `enrollment_date` | Enrollment Date | calendar_date | Enrollment end date |
| `as_of_date` | As of date | calendar_date | Date of data release by CMS |
| `race_and_ethnicity` | Race and ethnicity | text | Race and Ethnicity |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | text | Current Season Week Ending Label |

### k87d-gv3u

**Weekly Cumulative Doses (in Millions) of Influenza Vaccine Distributed by Flu Season in the United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/k87d-gv3u.json`
- Metadata: `GET https://data.cdc.gov/api/views/k87d-gv3u.json`; page: https://data.cdc.gov/d/k87d-gv3u
- Topics: Category: Vaccinations
- Tags: `influenza`, `flu`, `flu vaccination`
- Rows: 160. Data updated: 2026-08-03. Probe status: 200.
- Update frequency: Weekly.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Weekly Cumulative Doses (in Millions) of Influenza Vaccine Distributed by Flu Season in the United States • Archived data are available here: https://data.cdc.gov/resource/e5zk-7tx5 • Flu vaccine is produced by private manufacturers, so supply depends on manufacturers. Vaccine manufacturers have projected that they will supply the United States with as many as 173.5 million to 183.5 million doses of influenza vaccines for the 2022-2023 season. • Additional information is available: https://www.cdc.gov/flu/prevent/vaccine-supply-distribution.htm.
- Sample row fields ($limit=1): `influenza_season`, `start_date`, `end_date`, `reporting_timeframe`, `week`, `week_sort_order`, `current_season_week_ending_label`, `cumulative_flu_doses`, `current_through`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `influenza_season` | Influenza_Season | text |  |
| `start_date` | Start_Date | calendar_date |  |
| `end_date` | End_Date | calendar_date |  |
| `reporting_timeframe` | Reporting_Timeframe | text |  |
| `week` | Week | number |  |
| `week_sort_order` | Week_Sort_Order | number |  |
| `current_season_week_ending_label` | Current_Season_Week_Ending_Label | calendar_date |  |
| `cumulative_flu_doses` | Cumulative_Flu_Doses_Distributed | number |  |
| `current_through` | Current_Through | calendar_date |  |

### ewpg-rz7g

**Weekly Cumulative Estimated Number of COVID-19 Vaccinations Administered in Retail Pharmacies and Physician Medical Offices, Adults 18 years and older, by Season and Age Group, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ewpg-rz7g.json`
- Metadata: `GET https://data.cdc.gov/api/views/ewpg-rz7g.json`; page: https://data.cdc.gov/d/ewpg-rz7g
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `vsd`, `iis`, `iqvia`, `covid-19 vaccination`
- Rows: 2,730. Data updated: 2026-05-20. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: •Weekly Cumulative Estimated Number of COVID-19 Vaccinations Administered in Retail Pharmacies and Physician Medical Offices, Adults 18 Years and Older, United States •The projected pharmacy estimates are based on IQVIA†,‡ Longitudinal Prescription Claims (LRx) and vaccinations administered in retail pharmacies (including chain, mass merchandise, food stores, and independent pharmacies). § The projected physicians’ medical offices estimates are based on IQVIA’s Medical Claims (Dx). ± •Vaccinations administered in workplaces, community locations, long-term care settings, and other medical sett…
- Sample row fields ($limit=1): `influenza_season`, `week_id`, `current_season_week_ending_label`, `mmwr_week_order`, `mmwr_year`, `mmwr_week`, `mmwr_day`, `setting`, `doses`, `cumulative_doses`, `location_and_flu_season_order`, `current_through`, `age_group`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `influenza_season` | COVID-19_Season | text | COVID-19 Season |
| `week_id` | Week_ID | calendar_date | Week Ending Date of Data Collection Period |
| `current_season_week_ending_label` | Current_Season_Week_Ending_Label | calendar_date | Current Season Week Ending Label |
| `mmwr_week_order` | MMWR_Week_Order | number | MMWR Week Order |
| `mmwr_year` | MMWR_Year | number | MMWR Year |
| `mmwr_week` | MMWR_Week | number | MMWR Week |
| `mmwr_day` | MMWR_Day | number | MMWR Day |
| `setting` | Setting | text | Vaccine Administration Setting |
| `doses` | Doses | number | Number of Vaccine Doses |
| `cumulative_doses` | Cumulative_Doses | number | Cumulative Number of Vaccine Doses |
| `location_and_flu_season_order` | Location_and_Flu_Season_Order | text | Vaccine Administration Setting and COVID-19 Season Sort Order |
| `current_through` | Current_Through | calendar_date | Data Current Through Date |
| `age_group` | Age_Group | text | Age group |

### 83ng-twza

**Weekly Cumulative Estimated Number of Influenza Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 18 years and older, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/83ng-twza.json`
- Metadata: `GET https://data.cdc.gov/api/views/83ng-twza.json`; page: https://data.cdc.gov/d/83ng-twza
- Topics: Category: Vaccinations
- Tags: `influenza`, `flu`, `vaccine coverage`, `pharmacy vaccinations`, `physician medical office vaccinations`, `iqvia`
- Rows: 627. Data updated: 2024-05-24. Probe status: 200.
- Update frequency: Weekly.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Weekly Cumulative Estimated Number of Influenza Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 18 years and older, United States - Archived data are here: https://data.cdc.gov/resource/uxgd-cqqc - CDC is exploring use of data obtained from IQVIA§ (https://www.iqvia.com/) as a source of information on vaccinations administered in retail pharmacies (include chain, mass merchandise, food stores, and independent pharmacies) and physician medical offices. - These projected pharmacy estimates include flu vaccinations that were billed for (i.e. claims) or paid by cash.…
- Sample row fields ($limit=1): `influenza_season`, `week_id`, `current_season_week_ending_label`, `mmwr_week_order`, `mmwr_year`, `mmwr_week`, `mmwr_day`, `setting`, `doses`, `cumulative_doses`, `location_and_flu_season_order`, `current_through`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `influenza_season` | Influenza_Season | text | Influenza Season |
| `week_id` | Week_ID | calendar_date | Week Ending Date of Interviews Conducted/Data Collection Period |
| `current_season_week_ending_label` | Current_Season_Week_Ending_Label | calendar_date | Current Season Week Ending Labe (for x-axis alignment) |
| `mmwr_week_order` | MMWR_Week_Order | number | MMWR Week Order |
| `mmwr_year` | MMWR_Year | number | MMWR Year |
| `mmwr_week` | MMWR_Week | number | MMWR Week |
| `mmwr_day` | MMWR_Day | number | MMWR Day |
| `setting` | Setting | text | Vaccine Administration Setting |
| `doses` | Doses | number | Number of Vaccine Doses |
| `cumulative_doses` | Cumulative_Doses | number | Cumulative Number of Vaccine Doses |
| `location_and_flu_season_order` | Location_and_Flu_Season_Order | text | Vaccine Administration Setting and Flu Season Sort Order |
| `current_through` | Current_Through | calendar_date | Data Current Through Date |

### uxgd-cqqc

**Weekly Cumulative Estimated Number of Influenza Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 18 years and older, United States (ARCHIVED)** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/uxgd-cqqc.json`
- Metadata: `GET https://data.cdc.gov/api/views/uxgd-cqqc.json`; page: https://data.cdc.gov/d/uxgd-cqqc
- Topics: Category: Vaccinations
- Tags: `influenza`, `flu`, `vaccine coverage`, `pharmacy vaccinations`, `physician medical office vaccinations`, `iqvia`
- Rows: 363. Data updated: 2022-09-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Weekly Cumulative Estimated Number of Influenza Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 18 years and older, United States - Since 2019, CDC has been exploring use of data obtained from (https://www.iqvia.com/) as a source of information on vaccinations administered in retail pharmacies (include chain, mass merchandise, food stores, and independent pharmacies) and physician medical offices. These data are being presented publicly for the first time this season; further evaluations of these data are underway. - The pharmacy data include flu vaccinations tha…
- Sample row fields ($limit=1): `influenza_season`, `week_id`, `current_season_week_ending`, `mmwr_week_order`, `mmwr_year`, `mmwr_week`, `mmwr_day`, `setting`, `doses`, `cumulative_doses`, `location_and_flu_season_order`, `current_through`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `influenza_season` | Influenza_Season | text |  |
| `week_id` | Week_ID | calendar_date |  |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | calendar_date |  |
| `mmwr_week_order` | MMWR_Week_Order | number |  |
| `mmwr_year` | MMWR_Year | number |  |
| `mmwr_week` | MMWR_Week | number |  |
| `mmwr_day` | MMWR_Day | number |  |
| `setting` | Setting | text |  |
| `doses` | Doses | number |  |
| `cumulative_doses` | Cumulative_Doses | number |  |
| `location_and_flu_season_order` | Location_and_Flu_Season_Order | number |  |
| `current_through` | Current_Through | calendar_date |  |

### a3gi-4phs

**Weekly Cumulative Estimated Number of RSV Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 60 years and older, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/a3gi-4phs.json`
- Metadata: `GET https://data.cdc.gov/api/views/a3gi-4phs.json`; page: https://data.cdc.gov/d/a3gi-4phs
- Topics: Category: Vaccinations
- Tags: `rsv vaccination`, `iqvia`, `adults`
- Rows: 138. Data updated: 2024-09-11. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases
- Description: Weekly Cumulative Estimated Number of RSV Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 60 Years and Older, United States • Estimated Number of RSV vaccinations among adults 60 years and older is assessed through IQVIA (https://www.iqvia.com/) as a source of information on vaccinations administered in retail pharmacies (include chain, mass merchandise, food stores, and independent pharmacies) and physician medical offices. • Starting in September 2023, the CDC recommended the RSV vaccine for adults 60 years and older.
- Sample row fields ($limit=1): `week_id`, `mmwr_week_order`, `mmwr_year`, `mmwr_week`, `mmwr_day`, `setting`, `doses`, `cumulative_doses`, `location`, `current_through`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_id` | Week_ID | calendar_date | Week Ending Date of Data Collection Period |
| `mmwr_week_order` | MMWR_Week_Order | number | MMWR Week Order |
| `mmwr_year` | MMWR_Year | number | MMWR Year |
| `mmwr_week` | MMWR_Week | number | MMWR Week |
| `mmwr_day` | MMWR_Day | number | MMWR Day |
| `setting` | Setting | text | Vaccine Administration Setting |
| `doses` | Doses | number | Number of Vaccine Doses |
| `cumulative_doses` | Cumulative_Doses | number | Cumulative Number of Vaccine Doses |
| `location` | Location | text | Vaccine Administrative Setting |
| `current_through` | Current_Through | calendar_date | Data Current Through Date |

### 52ds-xw49

**Weekly Cumulative Estimated Number of RSV Vaccinations Administered in Retail Pharmacies and Physicians' Medical Offices, Adults 50 to 74 Years and 75 years and older, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/52ds-xw49.json`
- Metadata: `GET https://data.cdc.gov/api/views/52ds-xw49.json`; page: https://data.cdc.gov/d/52ds-xw49
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `iis`, `iqvia`, `vsd`, `rsv vaccination`
- Rows: 342. Data updated: 2026-05-20. Probe status: 200.
- Update frequency: Weekly.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • Weekly Cumulative Estimated Number of RSV Vaccinations Administered in Retail Pharmacies and Physicians’ Medical Offices, Adults 50–74 Years and 75 Years and Older, United States • In June 2023, the Advisory Committee on Immunization Practices (ACIP) voted to recommend that adults aged ≥60 years may receive a single dose of an RSV vaccine, using shared clinical decision-making. In June 2024, the ACIP voted to recommend a single dose of RSV vaccine for all adults 75 years and older and adults 60–74 years who are at increased risk for severe RSV disease.† On June 26, 2024, CDC adopted these r…
- Sample row fields ($limit=1): `week_id`, `mmwr_week_order`, `mmwr_year`, `mmwr_week`, `mmwr_day`, `setting`, `doses`, `cumulative_doses`, `current_through`, `age_group`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_id` | Week_ID | calendar_date | Week Ending Date of Data Collection Period |
| `mmwr_week_order` | MMWR_Week_Order | number | MMWR Week Order |
| `mmwr_year` | MMWR_Year | text | MMWR Year |
| `mmwr_week` | MMWR_Week | number | MMWR Week |
| `mmwr_day` | MMWR_Day | number | MMWR Day |
| `setting` | Setting | text | Vaccine Administration Setting |
| `doses` | Doses | number | Number of Vaccine Doses |
| `cumulative_doses` | Cumulative_Doses | number | Cumulative Number of Vaccine Doses |
| `current_through` | Current_Through | calendar_date | Data Current Through Date |
| `age_group` | Age_Group | text | Age Group (50-59 years, 60-74 years, 75+ years) |

### hea5-6w9c

**Weekly Cumulative Estimated Number of RSV Vaccinations Administered in Retail Pharmacies and Physicians’ Medical Offices, Adults 60 to 74 Years and 75 years and older, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/hea5-6w9c.json`
- Metadata: `GET https://data.cdc.gov/api/views/hea5-6w9c.json`; page: https://data.cdc.gov/d/hea5-6w9c
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `iis`, `iqvia`, `vsd`, `rsv vaccination`
- Rows: 222. Data updated: 2025-05-16. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: •Weekly Cumulative Estimated Number of RSV Vaccinations Administered in Retail Pharmacies and Physicians’ Medical Offices, Adults 60 to 74 Years and 75 Years and Older, United States • Estimated Number of RSV vaccinations among adults 60 years and older is assessed through IQVIA (https://www.iqvia.com/) as a source of information on vaccinations administered in retail pharmacies (include chain, mass merchandise, food stores, and independent pharmacies) and physician medical offices.
- Sample row fields ($limit=1): `week_id`, `mmwr_week_order`, `mmwr_year`, `mmwr_week`, `mmwr_day`, `setting`, `doses`, `cumulative_doses`, `location_and_flu_season_order`, `current_through`, `age_group`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_id` | Week_ID | calendar_date | Week Ending Date of Data Collection Period |
| `mmwr_week_order` | MMWR_Week_Order | number | MMWR Week Order |
| `mmwr_year` | MMWR_Year | text | MMWR Year |
| `mmwr_week` | MMWR_Week | number | MMWR Week |
| `mmwr_day` | MMWR_Day | number | MMWR Day |
| `setting` | Setting | text | Vaccine Administration Setting |
| `doses` | Doses | number | Number of Vaccine Doses |
| `cumulative_doses` | Cumulative_Doses | number | Cumulative Number of Vaccine Doses |
| `location_and_flu_season_order` | Location_and_Flu_Season_Order | number | Vaccine Administration Setting and RSV Season Sort Order |
| `current_through` | Current_Through | calendar_date | Data Current Through Date |
| `age_group` | Age_Group | text | Age group |

### w76m-r924

**Weekly Cumulative Estimated Number of Updated 2023-24 COVID-19 Vaccinations Administered in Pharmacies and Physician Medical Offices, Adults 18 years and older, United States, Data Source(s): IQVIA Pharmacy and Physician Medical Office Claims** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/w76m-r924.json`
- Metadata: `GET https://data.cdc.gov/api/views/w76m-r924.json`; page: https://data.cdc.gov/d/w76m-r924
- Topics: Category: Vaccinations
- Tags: `covid-19 vaccination`, `iqvia`, `adults`
- Rows: 99. Data updated: 2024-08-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases
- Description: Weekly Cumulative Estimated Number of Updated 2023-24 COVID-19 Vaccinations Administered in Pharmacies and Physical Medical Offices, Adults 18 Years and Older, United States • Estimated number of updated COVID-19 vaccinations among adults 18 years and older is assessed through IQVIA (https://www.iqvia.com/) as a source of information on vaccinations administered in retail pharmacies (include chain, mass merchandise, food stores, and independent pharmacies) and physician medical offices. • Starting in September 2023, the CDC recommended the updated 2023-2024 COVID-19 vaccine for adults ages 18…
- Sample row fields ($limit=1): `week_id`, `mmwr_week_order`, `mmwr_year`, `mmwr_week`, `mmwr_day`, `setting`, `doses`, `cumulative_doses`, `location`, `current_through`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_id` | Week_ID | calendar_date | Week Ending Date of Data Collection Period |
| `mmwr_week_order` | MMWR_Week_Order | number | MMWR Week Order |
| `mmwr_year` | MMWR_Year | number | MMWR Year |
| `mmwr_week` | MMWR_Week | number | MMWR Week |
| `mmwr_day` | MMWR_Day | number | MMWR Day |
| `setting` | Setting | text | Vaccine Administration Setting |
| `doses` | Doses | number | Number of Vaccine Doses |
| `cumulative_doses` | Cumulative_Doses | number | Cumulative Number of Vaccine Doses |
| `location` | Location | text | Vaccine Administration Setting |
| `current_through` | Current_Through | calendar_date | Data Current Through Date |

### g57i-yx3r

**Weekly Cumulative Influenza Vaccination Coverage, by Flu Season and Race/Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥65 years, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/g57i-yx3r.json`
- Metadata: `GET https://data.cdc.gov/api/views/g57i-yx3r.json`; page: https://data.cdc.gov/d/g57i-yx3r
- Topics: Category: Vaccinations
- Tags: `flu`, `influenza`, `flu vaccination`
- Rows: 1,446. Data updated: 2025-04-22. Probe status: 200.
- Update frequency: Weekly.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Weekly Cumulative Influenza Vaccination Coverage, by Flu Season and Race/Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥65 years, United States • Influenza vaccination coverage among Medicare fee-for-service beneficiaries aged ≥65 years is assessed using data files from the Medicare Fee-For-Service (FFS) administrative claims data managed by the Centers for Medicare & Medicaid Services (CMS). • Weekly influenza vaccination coverage estimates were calculated using Kaplan-Meier survival analysis, based on beneficiaries enrolled as of August 1, 2019 and followed through May 31, 2020 for…
- Sample row fields ($limit=1): `week_ending`, `influenza_season`, `mmwr_year`, `mmwr_week`, `mmwr_day`, `mmwrweek_display_order`, `race_ethnicity`, `point_estimate`, `current_season_week_ending_label`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week_Ending | calendar_date | Week Ending |
| `influenza_season` | Influenza_Season | text | Influenza Season |
| `mmwr_year` | MMWR_Year | number | Week Ending MMWR Year |
| `mmwr_week` | MMWR_Week | number | Week Ending MMWR Week |
| `mmwr_day` | MMWR_Day | number | Week Ending MMWR Day |
| `mmwrweek_display_order` | MMWRWeek_Display_Order | number | MMWR Week Display Order |
| `race_ethnicity` | Race_Ethnicity | text | Race and Ethncity |
| `point_estimate` | Point_Estimate | number | Point Estimate |
| `current_season_week_ending_label` | Current_Season_Week_Ending_Label | calendar_date | Current Season Week Ending Label (for x-axis) |

### eudc-n39h

**Weekly Cumulative Influenza Vaccination Coverage, Children 6 months through 17 years, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/eudc-n39h.json`
- Metadata: `GET https://data.cdc.gov/api/views/eudc-n39h.json`; page: https://data.cdc.gov/d/eudc-n39h
- Topics: Category: Vaccinations
- Tags: `influenza`, `flu`, `nis`, `nis-flu`, `children`, `vaccine coverage`, `flu shot`
- Rows: 4,262. Data updated: 2024-05-24. Probe status: 200.
- Update frequency: Weekly.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Weekly Cumulative Influenza Vaccination Coverage, Children 6 months through 17 years, United States • Archived data are available here: https://data.cdc.gov/resource/vfj2-bfuw • Influenza vaccination coverage among children is assessed through the National Immunization Survey-Flu (NIS-Flu) annually, providing weekly influenza vaccination coverage estimates for children 6 months–17 years based upon parental report. (https://www.cdc.gov/vaccines/imz-managers/nis/about.html) o NIS-Flu is a national random-digit-dialed cellular telephone survey of households conducted during the flu season (Octob…
- Sample row fields ($limit=1): `geographic_name`, `geographic_level`, `demographic_level`, `dsss_demographic_name`, `indicator_label`, `indicator_category_label`, `influenza_season`, `month_week`, `week_ending`, `current_season_week_ending_label`, `nd_weekly_estimate`, `ci_half_width_95pct`, `n_unweighted`, `n_weighted`, `suppression_flag`, `legend`, `ci_95`, `indicator_category_label_sort`, `demographic_level_sort_order`, `demographic_name_sort_order`, `geographic_name_sort_order`, `geographic_level_sort`, `season_sort`, `legend_sort`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `geographic_name` | Geography_Name | text | Geography Name |
| `geographic_level` | Geography_Level | text | Geography Level |
| `demographic_level` | Demographic_Level | text | Demographic |
| `dsss_demographic_name` | Demographic_Name | text | Demographic Name Category Group |
| `indicator_label` | Indicator_Label | text | Indicator Label |
| `indicator_category_label` | Indicator Category Label | text | Indicator Category Label |
| `influenza_season` | Influenza_Season | text | Influenza Season |
| `month_week` | Month_Week | text | Month and Week |
| `week_ending` | Week_Ending | calendar_date | Week Ending Date |
| `current_season_week_ending_label` | Current_Season_Week_Ending_Label | calendar_date | Current Season Week Ending Label |
| `nd_weekly_estimate` | Point_Estimate | number | Point Estimate (Coverage in Percent) |
| `ci_half_width_95pct` | CI_HalfWidth | number | 95% Confidence Interval Half Width |
| `n_unweighted` | n_unweighted | number | Unweighted Sample Size |
| `n_weighted` | n_weighted | number | Weighted Sample Size |
| `suppression_flag` | Suppression_Flag | number | Suppression Flag |
| `legend` | Legend_Label | text | Legend Label |
| `ci_95` | 95 CI (%) | text | 95% Confidence Interval |
| `indicator_category_label_sort` | Indicator_Category_Label_Sort | number | Indicator Category Label Sort |
| `demographic_level_sort_order` | Demographic_Level_Sort_Order | number | Demographic Level Sort Order |
| `demographic_name_sort_order` | Demographic_Name_Sort_Order | number | Demographic Name Category Group Sort Order |
| `geographic_name_sort_order` | geography_name_order | number | Geography Name Sort Order |
| `geographic_level_sort` | geography_level_sort_order | number | Geography Level Sort Order |
| `season_sort` | Season_Sort | number | Season Sort |
| `legend_sort` | Legend_Sort | number | Legend Sort |

### vfj2-bfuw

**Weekly Cumulative Influenza Vaccination Coverage, Children 6 months through 17 years, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/vfj2-bfuw.json`
- Metadata: `GET https://data.cdc.gov/api/views/vfj2-bfuw.json`; page: https://data.cdc.gov/d/vfj2-bfuw
- Topics: Category: Vaccinations
- Tags: `influenza`, `flu`, `nis`, `nis-flu`, `chlidren`, `vaccine coverage`, `flu shot`
- Rows: 6,694. Data updated: 2022-09-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Weekly Cumulative Influenza Vaccination Coverage, Children 6 months through 17 years, United States • Influenza vaccination coverage among children is assessed through the National Immunization Survey-Flu (NIS-Flu) annually, providing weekly influenza vaccination coverage estimates for children 6 months–17 years based upon parental report. (https://www.cdc.gov/vaccines/imz-managers/nis/about.html) o NIS-Flu is a national random-digit-dialed cellular telephone survey of households conducted during the flu season (October-June). • Additional information about NIS-Flu methods and estimates from…
- Sample row fields ($limit=1): `week_ending`, `current_season_week_ending`, `geography_name`, `geographic_level`, `geography_name_order`, `geography_label_sort_order`, `mmwr_year`, `mmwr_week`, `mmwr_day`, `month_week`, `month_display_order`, `mmwrweek_display_order`, `influenza_season`, `race_ethnicity`, `race_ethnicity_sort_order`, `point_estimate`, `ci_halfwidth`, `lower_ci`, `upper_ci`, `ci_range`, `season_race`, `season_race_sort_order`, `current_through`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week_Ending | calendar_date | Week Ending Date |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | calendar_date | Current Season Week Ending Label (for x-axis alignment) |
| `geography_name` | Geography_Name | text | Current Season Week Ending Label (for x-axis alignment) |
| `geographic_level` | Geographic_Level | text | Geographic Level |
| `geography_name_order` | Geography_Name_Order | number | Geography Name Sort Order |
| `geography_label_sort_order` | Geography_Label_Sort_Order | number | Geography Label Sort Order |
| `mmwr_year` | MMWR_Year | number | MMWR Year |
| `mmwr_week` | MMWR_Week | number | MMWR Week |
| `mmwr_day` | MMWR_Day | number | MMWR Day |
| `month_week` | Month_Week | text | Month Week Label |
| `month_display_order` | Month_Display_Order | number | Month Display Order |
| `mmwrweek_display_order` | MMWRWeek_Display_Order | number | Month Display Order |
| `influenza_season` | Influenza_Season | text | Influenza Season |
| `race_ethnicity` | Race_Ethnicity | text | Race and Ethnicity |
| `race_ethnicity_sort_order` | Race_Ethnicity_Sort_Order | number | Race and Ethnicity Sort Order |
| `point_estimate` | Point_Estimate | number | Point Estimate (Coverage) |
| `ci_halfwidth` | CI_HalfWidth | number | 95% Confidence Interval Half-width |
| `lower_ci` | Lower_CI | number | 95% Confidence Interval Half-width |
| `upper_ci` | Upper_CI | number | 95% Upper Confidence Interval |
| `ci_range` | CI_Range | text | Confidence Interval Range |
| `season_race` | Season_Race | text | Season and Race Label |
| `season_race_sort_order` | Season_Race_Sort_Order | text | Season and Race Label |
| `current_through` | Current_Through | calendar_date | Data Current Through Date |

### e5zk-7tx5

**Weekly Cumulative Influenza Vaccine Doses Distributed in the United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/e5zk-7tx5.json`
- Metadata: `GET https://data.cdc.gov/api/views/e5zk-7tx5.json`; page: https://data.cdc.gov/d/e5zk-7tx5
- Topics: Category: Vaccinations
- Tags: `influenza`, `flu`, `flu vaccination`
- Rows: 176. Data updated: 2022-09-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Weekly Cumulative Influenza Vaccine Doses Distributed in the United States, 2016-2021 • Flu vaccine is produced by private manufacturers. For the 2020-2021 season, manufacturers have projected they will provide as many as 194 to 198 million doses of influenza vaccine for the U.S. market. • Additional information is available: https://www.cdc.gov/flu/prevent/vaccine-supply-distribution.htm.
- Sample row fields ($limit=1): `season`, `month`, `month_number`, `week`, `month_week_label`, `month_week_sort_order`, `imputed_value`, `current_through`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `season` | Season | text |  |
| `month` | Month | text |  |
| `month_number` | Month_Number | number |  |
| `week` | Week | number |  |
| `month_week_label` | Month_Week_Label | text | Month Week Display Label |
| `month_week_sort_order` | Month_Week_Sort_Order | number | Month Week Sort Order |
| `cumulative_flu_doses` | Cumulative_Flu_Doses_Distributed | number |  |
| `imputed_value` | Imputed_Value | checkbox |  |
| `current_through` | Current_Through | calendar_date |  |

### sjpm-fk4b

**Weekly Cumulative Percentage of Adults 18 Years and Older Vaccinated with the Updated 2023-24 COVID-19 Vaccine by Jurisdiction** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/sjpm-fk4b.json`
- Metadata: `GET https://data.cdc.gov/api/views/sjpm-fk4b.json`; page: https://data.cdc.gov/d/sjpm-fk4b
- Topics: Category: Vaccinations
- Tags: `covid-19 vaccination`, `nis-acm`, `adults`
- Rows: 18,250. Data updated: 2024-08-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases
- Description: Weekly COVID-19 Vaccination Coverage of Adults 18 Years and Older by Jurisdiction • COVID-19 vaccination coverage among adults 18 years and older is assessed through the National Immunization Survey-Adult COVID Module, providing weekly COVID-19 vaccination coverage estimates. (https://www.cdc.gov/vaccines/imz-managers/nis/about.html) • Starting in September 2023, the CDC recommended the 2023-2024 updated COVID-19 vaccine for adults ages 18 years and older.
- Sample row fields ($limit=1): `vaccine`, `geographic_level`, `geographic_name`, `month_week`, `week_ending`, `estimate`, `ci_half_width_90pct`, `ci_half_width_95pct`, `unweighted_sample_size`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | Vaccine | text | COVID-19 Vaccine |
| `geographic_level` | Geographic Level | text | Geography Level (National, Region, State) |
| `geographic_name` | Geographic Name | text | Geography Name |
| `month_week` | Month_Week | text | Month and Week (October Week 1) |
| `week_ending` | Week_ending | calendar_date | Week Ending Date |
| `estimate` | Estimate | number | Estimate (%) |
| `ci_half_width_90pct` | CI_Half_width_90pct | number | 90% Confidence Interval Half Width |
| `ci_half_width_95pct` | CI_Half_width_95pct | number | 95% Confidence Interval Half Width |
| `unweighted_sample_size` | Unweighted Sample Size | number | Unweighted Sample Size |
| `suppression_flag` | suppression_flag | number |  |

### qve4-fp9c

**Weekly Cumulative Percentage of Adults 60 Years and Older Vaccinated with Respiratory Syncytial Virus (RSV) Vaccine by Jurisdiction** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/qve4-fp9c.json`
- Metadata: `GET https://data.cdc.gov/api/views/qve4-fp9c.json`; page: https://data.cdc.gov/d/qve4-fp9c
- Topics: Category: Vaccinations
- Tags: `vaccination`, `rsv`, `older adults`, `nis-acm`
- Rows: 17,425. Data updated: 2024-08-28. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Weekly RSV Vaccination Coverage of Adults 60 Years and Older by Jurisdiction • RSV vaccination coverage among adults 60 years and older is assessed through the National Immunization Survey-Adult COVID Module providing weekly RSV vaccination coverage estimates. (https://www.cdc.gov/vaccines/imz-managers/nis/about.html) • The CDC recommended the RSV vaccine for adults 60 years and older in July 2023. (https://www.cdc.gov/respiratory-viruses/whats-new/rsv-update-2023-09-22.html)
- Sample row fields ($limit=1): `vaccine`, `geographic_level`, `geographic_name`, `month_week`, `week_ending`, `estimate`, `ci_half_width_90pct`, `ci_half_width_95pct`, `unweighted_sample_size`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | Vaccine | text | RSV Vaccine |
| `geographic_level` | Geographic Level | text | Geography Level (National, Region, State) |
| `geographic_name` | Geographic Name | text | Geography Name |
| `month_week` | Month_Week | text | Month and Week (October Week 1) |
| `week_ending` | Week_ending | calendar_date | Week Ending Date |
| `estimate` | Estimate | number | Estimate (%) |
| `ci_half_width_90pct` | CI_Half_width_90pct | number | 90% Confidence Interval Half Width |
| `ci_half_width_95pct` | CI_Half_width_95pct | number | 95% Confidence Interval Half Width |
| `unweighted_sample_size` | Unweighted Sample Size | number | Unweighted Sample Size |
| `suppression_flag` | suppression_flag | number |  |

### qeq7-f3ir

**Weekly Cumulative RSV Vaccination Coverage and Intent, Overall, by Selected Demographics and Jurisdiction, Among Adults 75 and Older and 50-74 Years with High-Risk Conditions Ever Vaccinated, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/qeq7-f3ir.json`
- Metadata: `GET https://data.cdc.gov/api/views/qeq7-f3ir.json`; page: https://data.cdc.gov/d/qeq7-f3ir
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `vsd`, `iis`, `iqvia`, `rsv vaccination`, `cms`
- Rows: 7,400. Data updated: 2026-03-04. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • Weekly Cumulative RSV Vaccination Coverage and Intent Among Adults 75 Years and Older and 50-74 Years with High Risk Conditions Ever Vaccinated with RSV Vaccine by Demographic Characteristics and Jurisdiction • Weekly estimates of RSV vaccination coverage and intent among adults 75 years and older and 50-74 years with high risk conditions are calculated using data from National Immunization Surveys (NIS) – Fall Respiratory Virus Module (NIS–FRVM). The NIS-FRVM is an ongoing random-digit-dial cellular telephone survey of households with adults 18 years and older. • In June 2025, the Advisory…
- Sample row fields ($limit=1): `vaccine`, `age_group`, `geography_level`, `geography_name`, `demographic_level`, `demographic_name`, `indicator_label`, `indicator_category_label`, `month_week`, `week_ending`, `estimate`, `ci_half_width_95pct`, `unweighted_sample_size`, `suppression_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | Vaccine | text | RSV Vaccine |
| `age_group` | Age Group | text | Age Group (50-74 years (high-risk), 75+ years) |
| `geography_level` | Geography_level | text | Geography Level (National, Regional, State) |
| `geography_name` | Geography_name | text | Geography Name |
| `demographic_level` | Demographic Level | text | Demographic Category Level (Age, chronic conditions, disability status, health insurance, overall, poverty status, race and ethnicity, sex, sexual orientation, and urbanicity) |
| `demographic_name` | Demographic Name | text | Name of Specific Demographic (Age: 50-74yrs and 75+ yrs; Chronic Conditions: Yes, No; Disability Status: Yes, No; Health Insurance: Insured, Uninsured; Overall: Overall; Poverty Status: Above poverty, income >=75K, Above poverty, income <7… |
| `indicator_label` | Indicator_label | text | Intention Level |
| `indicator_category_label` | Indicator_category_label | text | Specific Intention Category |
| `month_week` | Month_Week | text | Month and Week |
| `week_ending` | Week_ending | calendar_date | Week Ending Date |
| `estimate` | Estimate | text | Estimate (%) |
| `ci_half_width_95pct` | CI_Half_width_95pct | text | 95% Confidence Interval Half Width |
| `unweighted_sample_size` | Unweighted Sample Size | number | Unweighted Sample Size |
| `suppression_flag` | Suppresion_flag | number |  |

### k4cb-dxd7

**Weekly Cumulative RSV Vaccination Coverage and Intent, Overall, by Selected Demographics and Jurisdiction, Among Adults 75 and Older and 60-74 Years with High-Risk Conditions Ever Vaccinated, United States** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/k4cb-dxd7.json`
- Metadata: `GET https://data.cdc.gov/api/views/k4cb-dxd7.json`; page: https://data.cdc.gov/d/k4cb-dxd7
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `vsd`, `iis`, `iqvia`, `nis-flu`, `rsv vaccination`
- Rows: 12,420. Data updated: 2025-05-20. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • Weekly Cumulative RSV Vaccination Coverage and Intent Among Adults 75 Years and Older and 60─74 Years with High Risk Conditions Ever Vaccinated with RSV Vaccine by Demographic Characteristics and Jurisdiction • Weekly estimates of RSV vaccination coverage and intent among adults 75 years and older and 60─74 years with high risk conditions are calculated using data from the National Immunization Survey–Adult COVID Module (NIS–ACM) (https://www.cdc.gov/nis/about/index.html). • In June 2023, the Advisory Committee on Immunization Practices (ACIP) voted to recommend that adults aged ≥60 years m…
- Sample row fields ($limit=1): `vaccine`, `age_group`, `geography_level`, `geography_name`, `demographic_level`, `demographic_name`, `indicator_label`, `indicator_category_label`, `month_week`, `week_ending`, `estimate`, `ci_half_width_90pct`, `ci_half_width_95pct`, `unweighted_sample_size`, `suppresion_flag`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | Vaccine | text | RSV Vaccine |
| `age_group` | Age Group | text | Age Group (60-74 years (high risk), 75+ years) |
| `geography_level` | Geography_level | text | Geography Level (National, Regional, State) |
| `geography_name` | Geography_name | text | Geography Name |
| `demographic_level` | Demographic Level | text | Demographic Category Level (Age, chronic conditions, disability status, health insurance, overall, poverty status, race and ethnicity, sex, sexual orientation, and urbanicity) |
| `demographic_name` | Demographic Name | text | Name of Specific Demographic (Age: 60yrs-74 and 75+ yrs; Chronic Conditions: Yes, No; Disability Status: Yes, No; Health Insurance: Insured, Uninsured; Overall: Overall; Poverty Status: Above poverty, income >=75K, Above poverty, income <7… |
| `indicator_label` | Indicator_label | text | Intention Level |
| `indicator_category_label` | Indicator_category_label | text | Specific Intention Category |
| `month_week` | Month_Week | text | Month and Week |
| `week_ending` | Week_ending | calendar_date | Week Ending Date |
| `estimate` | Estimate | text | Estimate (%) |
| `ci_half_width_90pct` | CI_Half_width_90pct | text | 90% Confidence Interval Half Width |
| `ci_half_width_95pct` | CI_Half_width_95pct | text | 95% Confidence Interval Half Width |
| `unweighted_sample_size` | Unweighted Sample Size | number | Unweighted Sample Size |
| `suppresion_flag` | Suppresion_flag | number |  |

### 55uq-699y

**Weekly Cumulative RSV Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥65 years, United States, Data Source: Centers for Medicare & Medicaid Services Chronic Conditions Warehouse** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/55uq-699y.json`
- Metadata: `GET https://data.cdc.gov/api/views/55uq-699y.json`; page: https://data.cdc.gov/d/55uq-699y
- Topics: Category: Vaccinations
- Tags: `vaccination`, `rsv`, `older adults`
- Rows: 288. Data updated: 2026-07-30. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Weekly Cumulative RSV Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged 65 years • Estimated COVID-19 vaccination coverage among Medicare fee-for-service beneficiaries >65 years is assessed using data files from the Medicare Fee-For-Service (FFS) administrative claims data managed by the Centers for Medicare & Medicaid Services (CMS). • Starting in July 2023, the CDC recommended the RSV vaccine to protect against serious illness from RSV. (https://www.cdc.gov/respiratory-viruses/whats-new/rsv-update-2023-09-22.html
- Sample row fields ($limit=1): `week_ending`, `point_estimate`, `mmwr_year`, `mmwr_week`, `enrollment_date`, `current_through_date`, `race_ethnicity`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week Ending | calendar_date | Week Ending |
| `point_estimate` | Estimate | text | Weekly percent coverage |
| `mmwr_year` | MMWR_Year | number | Week Ending MMWR Year |
| `mmwr_week` | MMWR_Week | number | Week Ending MMWR Week |
| `enrollment_date` | Enrollment Date | calendar_date | Enrollment end date |
| `current_through_date` | CMS Data As of date | calendar_date | Date of data release by CMS |
| `race_ethnicity` | Race and Ethnicity | text | Race and Ethnicity |

### nqu5-vn7d

**Weekly Cumulative RSV Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥75 years and enrolled in a Part D plan, United States, Data Source: Centers for Medicare & Medicaid Services Chronic Conditions Warehouse** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/nqu5-vn7d.json`
- Metadata: `GET https://data.cdc.gov/api/views/nqu5-vn7d.json`; page: https://data.cdc.gov/d/nqu5-vn7d
- Topics: Category: Vaccinations
- Tags: `rsv vaccination`, `nis`, `vsd`, `iqvia`, `iis`
- Rows: 156. Data updated: 2025-05-16. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • Weekly Cumulative RSV Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged 75 years • RSV vaccination coverage among Medicare-Fee-for-service beneficiaries aged 75 years and older and enrolled in a Part D plan in assessed using data files from the Medicare Fee-for-Service (FFS) administrative claims data managed by the Centers for Medicare & Medicaid Services (CMS).
- Sample row fields ($limit=1): `week_ending`, `estimate`, `mmwr_year`, `mmwr_week`, `enrollment_date`, `as_of_date`, `race_and_ethnicity`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week Ending | calendar_date | Week Ending |
| `estimate` | Estimate | number | Weekly percent coverage |
| `mmwr_year` | MMWR_Year | number | Week Ending MMWR Year |
| `mmwr_week` | MMWR_Week | number | Week Ending MMWR Week |
| `enrollment_date` | Enrollment Date | calendar_date | Enrollment end date |
| `as_of_date` | As of date | calendar_date | Date of data release by CMS |
| `race_and_ethnicity` | Race and ethnicity | text | Race and Ethnicity |

### msnx-y6hi

**Weekly Cumulative RSV Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥75 years and Enrolled in a Part D plan, United States, Data Source: Centers for Medicare & Medicaid Services Chronic Conditions Warehouse** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/msnx-y6hi.json`
- Metadata: `GET https://data.cdc.gov/api/views/msnx-y6hi.json`; page: https://data.cdc.gov/d/msnx-y6hi
- Topics: Category: Vaccinations
- Tags: `rsv vaccination`, `nis`, `vsd`, `iqvia`, `iis`
- Rows: 186. Data updated: 2026-05-20. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • RSV vaccination coverage among Medicare fee-for-service beneficiaries aged 75 years and older enrolled in a Part D plan is assessed using data files from the Medicare Fee-For-Service (FFS) administrative claims data managed by the Centers for Medicare & Medicaid Services (CMS). • Weekly RSV vaccination coverage estimates were calculated using Kaplan-Meier survival analysis, based on beneficiaries enrolled as of August 1, 2023. RSV vaccines received since August 1, 2023, among adults who were 75 years or older as of the end of the first year of the season (e.g., December 31, 2025, for the 20…
- Sample row fields ($limit=1): `week_ending`, `estimate`, `mmwr_year`, `mmwr_week`, `enrollment_date`, `as_of_date`, `race_and_ethnicity`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week Ending | calendar_date | Week Ending |
| `estimate` | Estimate | number | Weekly percent coverage |
| `mmwr_year` | MMWR_Year | text | Week Ending MMWR Year |
| `mmwr_week` | MMWR_Week | number | Week Ending MMWR Week |
| `enrollment_date` | Enrollment Date | calendar_date | Enrollment end date |
| `as_of_date` | As of date | calendar_date | Date of data release by CMS |
| `race_and_ethnicity` | Race and ethnicity | text | Race and ethnicity (Asian, Non-Hispanic, Black, Non-Hispanic, Hispanic, Other, Non-Hispanic, Overall) |

### brsb-akdp

**Weekly Cumulative Updated 2023-24 COVID-19 Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥65 years, United States, Data Source: Centers for Medicare & Medicaid Services Chronic Conditions Warehouse** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/brsb-akdp.json`
- Metadata: `GET https://data.cdc.gov/api/views/brsb-akdp.json`; page: https://data.cdc.gov/d/brsb-akdp
- Topics: Category: Vaccinations
- Tags: `covid-19 vaccination`, `adults`
- Rows: 186. Data updated: 2026-08-03. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: Weekly Cumulative Updated 2023-24 COVID-19 Vaccination Coverage, by Race and Ethnicity, Medicare Fee-For-Service Beneficiaries aged ≥65 years • Estimated COVID-19 vaccination coverage among Medicare fee-for-service beneficiaries >65 years is assessed using data files from the Medicare Fee-For-Service (FFS) administrative claims data managed by the Centers for Medicare & Medicaid Services (CMS). • Starting in September 2023, the CDC recommended the 2023-2024 updated COVID-19 vaccine to protect against serious illness from COVID-19. (https://www.cdc.gov/coronavirus/2019-ncov/vaccines/stay-up-to…
- Sample row fields ($limit=1): `week_ending`, `point_estimate`, `mmwr_year`, `mmwr_week`, `enrollment_date`, `current_through_date`, `race_ethnicity`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week Ending | calendar_date | Week Ending |
| `point_estimate` | Estimate | text | Weekly percent coverage |
| `mmwr_year` | MMWR Year | number | Week Ending MMWR Year |
| `mmwr_week` | MMWR Week | number | Week Ending MMWR Week |
| `enrollment_date` | Enrollment Date | calendar_date | Enrollment end date |
| `current_through_date` | CMS Data As of Date | calendar_date | Date of data release by CMS |
| `race_ethnicity` | Race and Ethnicity | text | Race and Ethnicity |
| `covid_season` | COVID_Season | calendar_date | The COVID-19 season |

### 8yup-c35n

**Weekly Differences in Cumulative COVID-19 Vaccination Coverage by Selected Demographics and by Season, Among Adults 18 Years, Overall** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/8yup-c35n.json`
- Metadata: `GET https://data.cdc.gov/api/views/8yup-c35n.json`; page: https://data.cdc.gov/d/8yup-c35n
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `vsd`, `iqvia`, `covid-19 vaccination`, `nis-child`, `iis-child`, `iis-adult`, `cms`
- Rows: 2,460. Data updated: 2026-03-04. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • Weekly COVID-19 Vaccination Coverage and Comparison among adults 18 Years and Older by Selected Demographics and by Season • Weekly estimates of COVID-19 vaccination coverage and intent for vaccination among adults are calculated using data from the National Immunization Surveys (NIS)-Fall Respiratory Virus Module (NIS-FRVM) (https://www.cdc.gov/nis/about/index.html). • The NIS–FRVM is an ongoing random-digit-dial cellular telephone survey of households with adults 18 years and older. All estimates are based upon self-reported receipt of vaccination and month of that vaccination. • Weekly c…
- Sample row fields ($limit=1): `comparison_type`, `week_ending`, `current_season_week_ending`, `comparison_group_1`, `comparison_group_2`, `comparison_group1_point`, `comparison_group2_point`, `estimate_difference`, `difference_estimate_lower`, `difference_estimate_upper`, `comparison_group_1_sort`, `comparison_group_2_sort_order`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `comparison_type` | Comparison_Type | text | Comparison Type |
| `week_ending` | Week_Ending | calendar_date | Week Ending Date |
| `current_season_week_ending` | Current_Season_Week_Ending_Label | calendar_date | Current Season Week Ending Label |
| `comparison_group_1` | Comparison_Group 1 | text | Comparison Group 1 |
| `comparison_group_2` | Comparison_Group 2 | text | Comparison Group 2 |
| `comparison_group1_point` | Comparison_Group1_Point_Estimate | number | Comparison Group 1 Point Estimate |
| `comparison_group2_point` | Comparison_Group2_Point_Estimate | text | Comparison Group 2 Point Estimate |
| `estimate_difference` | Estimate Difference | text | Estimate Difference |
| `difference_estimate_lower` | Difference_Estimate_Lower_95 CI | text | Lower 95% Confidence Interval Bound of Difference Estimate |
| `difference_estimate_upper` | Difference_Estimate_Upper_95 CI | text | Upper 95% Confidence Interval Bound of Difference Estimate |
| `significant_at_95_pct` | Significant_at_95_pct | text | Statistically Significant at 95% CI |
| `comparison_group_1_sort` | Comparison Group 1 Sort | number | Comparison Group 1 Sort Order |
| `comparison_group_2_sort_order` | Comparison Group 2 Sort Order | number | Comparison Group 2 Sort Order |

### 4tme-u33f

**Weekly Differences in Cumulative Respiratory Syncytial Virus (RSV) Vaccination Coverage and Comparison, Overall, by Jurisdiction, Among Adults 75 Years and Older and Adults 50-74 Years with High-Risk Conditions** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/4tme-u33f.json`
- Metadata: `GET https://data.cdc.gov/api/views/4tme-u33f.json`; page: https://data.cdc.gov/d/4tme-u33f
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `vsd`, `iis`, `iqvia`, `rsv vaccination`, `cms`
- Rows: 1,760. Data updated: 2026-03-04. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • Weekly Cumulative RSV Vaccination Coverage and Intent Among Adults 75 Years and Older and 50-74 Years with High Risk Conditions Ever Vaccinated with RSV Vaccine by Demographic Characteristics and Jurisdiction • Weekly estimates of RSV vaccination coverage and intent among adults 75 years and older and 50-74 years with high risk conditions are calculated using data from the National Immunization Survey - Fall Respiratory Virus Module (NIS–FRVM). The NIS-FRVM is an ongoing random-digit-dial cellular telephone survey of households with adults 18 years and older. • In June 2025, the Advisory Co…
- Sample row fields ($limit=1): `week_ending`, `demographic_level`, `comparison_group_1`, `comparison_group_2`, `comparison_group_1_estimate`, `comparison_group_2_estimate`, `estimate_difference`, `difference_estimate_lower_95_ci`, `difference_estimate_upper_95_ci`, `comparison_group_1_sort_order`, `comparison_group_2_sort_order`, `age_group`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week_Ending | calendar_date | Week Ending Date |
| `demographic_level` | Demographic Level | text | Demographic Category level (Age, chronic conditions, disability status, health insurance, overall, poverty status, race and ethnicity, sex, sexual orientation, and urbanicity) |
| `comparison_group_1` | Comparison Group 1 | text | Comparison group 1 |
| `comparison_group_2` | Comparison Group 2 | text | Comparison Group 2 |
| `comparison_group_1_estimate` | Comparison Group 1 Estimate | text | Comparison Group 1 Estimate |
| `comparison_group_2_estimate` | Comparison Group 2 Estimate | text | Comparison Group 2 Estimate |
| `estimate_difference` | Estimate Difference | text | Estimate difference |
| `difference_estimate_lower_95_ci` | Difference Estimate Lower 95 CI | text | Lower 95% Confidence Interval Bound of Difference Estimate |
| `difference_estimate_upper_95_ci` | Difference Estimate Upper 95 CI | text | Upper 95% Confidence Interval Bound of Difference Estimate |
| `significant_at_95_pct` | Significant at 95 pct | text | Statistically Significant at 95% Confidence Indicator |
| `comparison_group_1_sort_order` | Comparison Group 1 Sort Order | number | Comparison Group 1 Sort Order |
| `comparison_group_2_sort_order` | Comparison Group 2 Sort Order | number | Comparison Group 2 Sort Order |
| `age_group` | Age Group | text | Age groups (75+ years old, 50-74 years (high risk)) |

### mcvh-596h

**Weekly Differences in Cumulative RSV Vaccination Coverage Among Adults 75 and Older and 60-74 Years with High-Risk Conditions Ever Vaccinated with RSV Vaccine, Overall, by Selected Demographics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/mcvh-596h.json`
- Metadata: `GET https://data.cdc.gov/api/views/mcvh-596h.json`; page: https://data.cdc.gov/d/mcvh-596h
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `iis`, `iqvia`, `vsd`, `nis-flu`, `rsv vaccination`
- Rows: 3,074. Data updated: 2025-12-10. Probe status: 200.
- Update frequency: Weekly.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: . Weekly Cumulative RSV Vaccination Coverage and Intent Among Adults 75 Years and Older and 60?74 Years with High Risk Conditions Ever Vaccinated with RSV Vaccine by Demographic Characteristics and Jurisdiction . Weekly estimates of RSV vaccination coverage and intent among adults 75 years and older and 60?74 years with high risk conditions are calculated using data from the National Immunization Survey-Adult COVID Module (NIS-ACM) (https://www.cdc.gov/nis/about/) . In June 2023, the Advisory Committee on Immunization Practices (ACIP) voted to recommend that adults aged ?60 years may receive…
- Sample row fields ($limit=1): `week_ending`, `demographic_level`, `comparison_group_1`, `comparison_group_2`, `comparison_group_1_estimate`, `comparison_group_2_estimate`, `estimate_difference`, `difference_estimate_lower`, `difference_estimate_upper`, `significant_at_95_pct`, `comparison_group_1_sort_order`, `comparison_group_2_sort_order`, `age_group`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week Ending | text |  |
| `demographic_level` | Demographic Level | text |  |
| `comparison_group_1` | Comparison Group 1 | text |  |
| `comparison_group_2` | Comparison Group 2 | text |  |
| `comparison_group_1_estimate` | Comparison Group 1 Estimate | number |  |
| `comparison_group_2_estimate` | Comparison Group 2 Estimate | number |  |
| `estimate_difference` | Estimate Difference | number |  |
| `difference_estimate_lower` | Difference_Estimate_Lower_95_CI | number |  |
| `difference_estimate_upper` | Difference_Estimate_Upper_95_CI | number |  |
| `significant_at_95_pct` | Significant_at_95_pct | text |  |
| `comparison_group_1_sort_order` | Comparison Group 1 Sort Order | number |  |
| `comparison_group_2_sort_order` | Comparison Group 2 Sort Order | number |  |
| `age_group` | age_group | text |  |

### ndai-i7s4

**Weekly Differences in Cumulative RSV Vaccination Coverage Among Adults 75 and Older and 60–74 Years with High-Risk Conditions Ever Vaccinated with RSV Vaccine, Overall, by Selected Demographics** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ndai-i7s4.json`
- Metadata: `GET https://data.cdc.gov/api/views/ndai-i7s4.json`; page: https://data.cdc.gov/d/ndai-i7s4
- Topics: Category: Vaccinations
- Tags: `nis-acm`, `iis`, `iqvia`, `vsd`, `nis-flu`, `rsv vaccination`
- Rows: 3,074. Data updated: 2025-05-16. Probe status: 200.
- Source: National Center for Immunization and Respiratory Diseases (NCIRD)
- Description: • Weekly Cumulative RSV Vaccination Coverage and Intent Among Adults 75 Years and Older and 60─74 Years with High Risk Conditions Ever Vaccinated with RSV Vaccine by Demographic Characteristics and Jurisdiction • Weekly estimates of RSV vaccination coverage and intent among adults 75 years and older and 60─74 years with high risk conditions are calculated using data from the National Immunization Survey–Adult COVID Module (NIS–ACM) (https://www.cdc.gov/nis/about/) • In June 2023, the Advisory Committee on Immunization Practices (ACIP) voted to recommend that adults aged ≥60 years may receive…
- Sample row fields ($limit=1): `week_ending`, `demographic_level`, `comparison_group_1`, `comparison_group_2`, `comparison_group_1_estimate`, `comparison_group_2_estimate`, `estimate_difference`, `difference_estimate_lower_95_ci`, `difference_estimate_upper_95_ci`, `significant_at_95_pct`, `comparison_group_1_sort_order`, `comparison_group_2_sort_order`, `age_group`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_ending` | Week Ending | calendar_date | Week Ending Date |
| `demographic_level` | Demographic Level | text | Demographic Category level (Age, chronic conditions, disability status, health insurance, overall, poverty status, race and ethnicity, sex, sexual orientation, and urbanicity) |
| `comparison_group_1` | Comparison Group 1 | text | Comparison Group 1 |
| `comparison_group_2` | Comparison Group 2 | text | Comparison Group 2 |
| `comparison_group_1_estimate` | Comparison Group 1 Estimate | text | Comparison Group 1 Estimate |
| `comparison_group_2_estimate` | Comparison Group 2 Estimate | text | Comparison Group 2 Estimate |
| `estimate_difference` | Estimate Difference | text | Estimate Difference |
| `difference_estimate_lower_95_ci` | Difference_Estimate_Lower_95_CI | text | Lower 95% Confidence Interval Bound of Difference Estimate |
| `difference_estimate_upper_95_ci` | Difference_Estimate_Upper_95_CI | text | Upper 95% Confidence Interval Bound of Difference Estimate |
| `significant_at_95_pct` | Significant_at_95_pct | text | Statistically Significant at 95% Confidence Indicator |
| `comparison_group_1_sort_order` | Comparison Group 1 Sort Order | number | Comparison Group 1 Sort Order |
| `comparison_group_2_sort_order` | Comparison Group 2 Sort Order | number | Comparison Group 2 Sort Order |
| `age_group` | age_group | text | The age range of the survey participants |

### 5c6r-xi2t

**Weekly Respiratory Virus Vaccination Data, Children 6 Months-17 Years and Adults 18 Years and Older, National Immunization Survey** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/5c6r-xi2t.json`
- Metadata: `GET https://data.cdc.gov/api/views/5c6r-xi2t.json`; page: https://data.cdc.gov/d/5c6r-xi2t
- Topics: Category: Vaccinations
- Tags: `ncird`, `rsv`, `covid19`, `coronavirus`, `vaccination`, `immunization`, `nis-acm`, `nis-ccm`, `respiratory-virus-response`, `vaccination-coverage`
- Rows: 1,040. Data updated: 2026-09-14. Probe status: 200.
- Update frequency: R/P1W.
- Description: *Vaccination data updates for the 2024-2025 respiratory illness season ended on May 2, 2025. The weekly respiratory virus vaccination data come from the National Immunization Survey-Adult COVID Module (NIS-ACM), National Immunization Survey-Child COVID Module (NIS-CCM), and the National Immunization Survey-Flu (NIS-Flu). The NIS-ACM provides data on Influenza (flu), COVID-19, and RSV vaccination for adults aged ≥18 years in the United States. The NIS-CCM provides data on COVID-19 vaccination for children aged 6 months-17 years in the United States. The NIS-Flu provides data on Influenza vacci…
- Sample row fields ($limit=1): `vaccine`, `influenza_season`, `geographic_level`, `geographic_name`, `demographic_level`, `demographic_name`, `indicator_label`, `indicator_category_label`, `month_week`, `week_ending`, `nd_weekly_estimate`, `ci_half_width_90pct`, `ci_half_width_95pct`, `n_weighted`, `n_unweighted`, `suppression_flag`, `data_source`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `vaccine` | vaccine | text | The vaccine assessed by the survey (RSV, COVID-19, Influenza). |
| `influenza_season` | influenza_season | text | Applicable for influenza vaccine only; influenza season specified. |
| `geographic_level` | geographic_level | text | The classification (National, Region, or State) of geographies. |
| `geographic_name` | geographic_name | text | The name of the geography for which estimates are calculated. |
| `demographic_level` | demographic_level | text | The name of the variable by which estimates are grouped (Overall, Age, Sex, Race/Ethnicity, Poverty Status, Health Insurance, Urbanicity, Disability Status, Sexual Orientation). |
| `demographic_name` | demographic_name | text | The level of each demographic variable (18-29 years, Insured/Uninsured, Female/Male, etc.). |
| `indicator_label` | indicator_label | text | The indicator variable assessed by the survey (Up-to-date, 4-level vaccination and intent). |
| `indicator_category_label` | indicator_category_label | text | The level of the indicator variable assessed by the survey (Received a vaccination, Definitely will get a vaccine, etc.). |
| `month_week` | month_week | text | The month and week the telephone interviews were conducted. |
| `week_ending` | week_ending | text | The ending date of the week the telephone interviews were conducted. |
| `nd_weekly_estimate` | nd_weekly_estimate | text | The numerical estimate of the weighted proportion giving the response. |
| `ci_half_width_90pct` | ci_half_width_90pct | text | The half-width of the 90% confidence interval of the estimate. |
| `ci_half_width_95pct` | ci_half_width_95pct | text | The half-width of the 95% confidence interval of the estimate. |
| `n_weighted` | n_weighted | text | The weighted number of respondents in the denominator used to calculate the proportion estimates. |
| `n_unweighted` | n_unweighted | text | The unweighted number of respondents in the denominator used to calculate the proportion estimates. |
| `suppression_flag` | suppression_flag | text | Up-to-date estimates are suppressed (missing) and have a value of 1 for this field if the cumulative sample size across all weeks is less than 30 or if the most recent week sample size is less than 5. Four-level vaccination and intent esti… |
| `data_source` | data_source | text | Source of vaccine data. [NIS-ACM, NIS-CCM, NIS-Flu] |

## Usage tips

- Pick the dataset by question:
  - Kindergarten coverage (MMR, DTaP, polio, varicella, hepatitis B) and exemptions by state and school year since 2009-10: `ijqb-a7ye` (`vaccine='Exemption'` for exemptions).
  - Adult pneumococcal, tetanus (Td/Tdap) and shingles coverage by state, county and demographic group: `aetd-68ew`. Health care personnel `xerk-pcm8`, nursing home residents `8w4j-reb4`.
  - Weekly flu, COVID-19 and RSV vaccination and intent from the National Immunization Survey, current season: `5c6r-xi2t` (`vaccine` is `FLU`, `COVID` or `RSV`), `ee83-ukst`, and reasons and concerns `94wp-9pid`.
  - Flu vaccine doses distributed by season: `k87d-gv3u` (seasons up to 2022-2023 only).
  - COVID-19 vaccinations through May 2023: by county `8xkx-amqh`, by state or jurisdiction `unsk-b7fc`, national trends `rh2h-3yt2`. Vaccine hesitancy by county (2021): `q9mh-h2tw`.
- **Many estimate columns are `text`**, not `number`: `coverage_estimate`, `population_sample_size` and `number_of_exemptions` in `ijqb-a7ye` / `aetd-68ew`, and `nd_weekly_estimate` in `5c6r-xi2t`. They also hold codes such as `NA`, `NR` and `NReq`, so `sum`/`avg` and numeric `$order` don't work on them; fetch the rows and parse them. Check the column type before aggregating.
- `geography_type` separates national and state rows (`National`, `States` in `ijqb-a7ye`); filter on it so state rankings don't include the national value. The survey datasets use `geographic_level` / `geographic_name` and `demographic_level` / `demographic_name` (`Overall` for the total).
- Examples:

  ```
  # MMR kindergarten coverage by state, 2024-25
  GET https://data.cdc.gov/resource/ijqb-a7ye.json?$select=geography,coverage_estimate&$where=vaccine='MMR' AND year_season='2024-25' AND geography_type='States'&$order=geography
  # National kindergarten exemption estimates by school year
  GET https://data.cdc.gov/resource/ijqb-a7ye.json?$where=vaccine='Exemption' AND geography_type='National'&$order=year_season
  # Weekly national RSV vaccination estimates, overall
  GET https://data.cdc.gov/resource/5c6r-xi2t.json?$where=vaccine='RSV' AND geographic_level='National' AND demographic_level='Overall'&$order=week_ending
  ```
