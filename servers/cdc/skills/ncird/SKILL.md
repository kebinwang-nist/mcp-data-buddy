---
name: cdc-ncird
description: Query CDC open data (data.cdc.gov, Socrata SODA API) for the National Center for Immunization and Respiratory Diseases (NCIRD) category. Use it for weekly emergency department visit shares for respiratory conditions (pneumonia, bronchiolitis, croup, sinus infection and others) by age group, and for influenza A virus ferret studies (viral titers in tissues, weight loss, fever, lethality and transmission).
---

# CDC open data: National Center for Immunization and Respiratory Diseases

## Overview

- Portal: `https://data.cdc.gov` (Socrata). Category browse page: `https://data.cdc.gov/browse?category=National+Center+for+Immunization+and+Respiratory+Diseases`.
- Catalog snapshot taken 2026-11-09: 3 public assets in the category: 3 datasets, 0 filtered views, 0 maps, 0 charts.
- Excluded (not public or no API endpoint): none.
- Common tags (number of assets): `ncird` (3), `virus` (3), `animal model` (2), `ferret` (2), `flu` (2), `in vivo` (2), `influenza` (2), `ncird-id` (2), `pathogenesis` (2), `risk assessment` (2), `ari other` (1), `bacteria` (1), `ed data` (1), `necropsy` (1), `ophdst` (1), `respiratory-virus-response` (1), `rvr` (1), `tissue` (1).
- Surface: read-only `GET`. Each dataset and filtered view has its own data endpoint keyed by a 4x4 id (e.g. `d9u6-mdu6`). Maps and charts have no data endpoint of their own; query their parent dataset instead.
- Auth: none for reads. An optional Socrata app token in header `X-App-Token` raises the throttling limit; without one, heavy use from one IP may get HTTP 429. No key for this API exists in this project.
- Types: Socrata column types are `text`, `number`, `calendar_date` (floating timestamp, returned as `2024-10-04T00:00:00.000`), `point` (GeoJSON `{"type":"Point","coordinates":[lon,lat]}`), `url` (`{"url": ...}`), `checkbox` (boolean). In JSON output, numbers come back as strings. Null fields are omitted from a row object rather than returned as `null`.
- Topics and tags: each section's `Topics` and `Tags` lines come from the dataset's intro page (`/d/{id}`, "About this Dataset"), read from `/api/views/{id}.json`. `Sample row fields` lists the field names one `$limit=1` row returned; values were not stored.
- Freshness: `v58w-vynu` (respiratory conditions in the emergency department) is updated weekly and starts in October 2023. The two ferret datasets are fixed research releases.

## Endpoints per asset

Replace `{id}` with the asset id from the index.

| Purpose | Endpoint |
|---|---|
| Rows as JSON (SODA 2.1, SoQL params) | `GET https://data.cdc.gov/resource/{id}.json` |
| Rows as CSV / GeoJSON | `GET https://data.cdc.gov/resource/{id}.csv`, `.geojson` |
| Column + view metadata | `GET https://data.cdc.gov/api/views/{id}.json` |
| Full export (no row limit) | `GET https://data.cdc.gov/api/views/{id}/rows.csv?accessType=DOWNLOAD` |
| Human page | `https://data.cdc.gov/d/{id}` |
| Catalog search (this category) | `GET https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&categories=National%20Center%20for%20Immunization%20and%20Respiratory%20Diseases&limit=100` |

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
| 1 | [`d9u6-mdu6`](#d9u6-mdu6) | An aggregated dataset of day 3 post-inoculation viral titer measurements from influenza A virus-infected ferret tissues | dataset |  | 351 | 15 | 2026-03-09 |  | 200 |
| 2 | [`cr56-k9wj`](#cr56-k9wj) | An aggregated dataset of serially collected influenza A virus morbidity and titer measurements from virus-infected ferrets. | dataset |  | 851 | 29 | 2026-03-09 |  | 200 |
| 3 | [`v58w-vynu`](#v58w-vynu) | Respiratory Conditions Treated in the Emergency Department | dataset |  | 12,397 | 4 | 2026-11-06 |  | 200 |

## Datasets and filtered views

### d9u6-mdu6

**An aggregated dataset of day 3 post-inoculation viral titer measurements from influenza A virus-infected ferret tissues** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/d9u6-mdu6.json`
- Metadata: `GET https://data.cdc.gov/api/views/d9u6-mdu6.json`; page: https://data.cdc.gov/d/d9u6-mdu6
- Topics: Category: National Center for Immunization and Respiratory Diseases
- Tags: `influenza`, `pathogenesis`, `ferret`, `animal model`, `risk assessment`, `in vivo`, `flu`, `virus`, `tissue`, `necropsy`, `ncird`, `ncird-id`
- Rows: 351. Data updated: 2026-03-09. Probe status: 200.
- Source: Influenza Division/Immunology and Pathogenesis Branch/Pathogenesis Laboratory Team
- Description: Data from influenza A virus (IAV) infected ferrets (Mustela putorius furo) provides invaluable information towards the study of novel and emerging viruses that pose a threat to human health. This gold standard animal model can recapitulate many clinical signs of infection present in IAV-infected humans, supports virus replication of human and zoonotic strains without prior adaptation, and permits evaluation of virus transmissibility by multiple modes. While ferrets have been employed in risk assessment settings for >20 years, results from this work are typically reported in discrete stand-alo…
- Sample row fields ($limit=1): `ferret`, `virus`, `ha`, `na`, `hpai`, `hpai_mbaa`, `origin`, `units`, `inoc_dose`, `nt`, `tr`, `lg`, `bnob`, `bn`, `int`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `ferret` | Ferret | text | Unique observational ID for each individual animal in the dataset. |
| `virus` | Virus | text | Unique identifier for each virus used to inoculate ferrets in the dataset. |
| `ha` | HA | text | Categorical column indicating hemagglutinin subtype of the inoculating virus. |
| `na` | NA | text | Categorical column indicating neuraminidase subtype of the inoculating virus. |
| `hpai` | HPAI | checkbox | Binary column that indicates if the inoculating virus has been classified as a highly pathogenic avian influenza (HPAI) virus based on criteria of the intravenous pathogenicity index (TRUE) or is a low pathogenic avian influenza (LPAI) or… |
| `hpai_mbaa` | HPAI_MBAA | checkbox | Binary column that indicates if the inoculating virus has been classified as a highly pathogenic avian influenza (HPAI) virus based on criteria of the intravenous pathogenicity index (TRUE) or is a low pathogenic avian influenza (LPAI) or… |
| `origin` | Origin | text | Categorical column indicating the host origin of the inoculating virus. Avian, isolated from avian host or originated from an avian species during a zoonotic spillover to humans; human, human origin; swine, swine origin; canine, canine ori… |
| `units` | units | text | Binary column that indicates if log10 titers reported in NW columns are reported as EID50 (titration in eggs, EID, LOD = 1.5) or PFU (titration in cells, PFU, LOD = 1). EID and PFU units are not interchangeable; See PMID 38760422 for limit… |
| `inoc_dose` | inoc_dose | number | Numeric column that indicates the log10 infectious units used to intranasally inoculate the ferret (in a 1ml total volume, with virus diluted in PBS). |
| `nt` | NT | number | Numerical columns reporting Nasal Turbinate (NT) tissue log10 titer/ml, in the units specified in ‘units’, collected from each ferret day 3 post-inoculation. Nasal Turbinate tissue was typically dislodged and removed using forceps via the… |
| `tr` | Tr | text | Numerical columns reporting Trachea (Tr) tissue log10 titer/gram, in the units specified in ‘units’, collected from each ferret day 3 post-inoculation. NA, represents no tissue sample was collected. LOD, represents a tissue sample was coll… |
| `lg` | Lg | text | Numerical columns reporting Lung (Lg) tissue log10 titer/gram, in the units specified in ‘units’, collected from each ferret day 3 post-inoculation. NA, represents no tissue sample was collected. LOD, represents a tissue sample was collect… |
| `bnob` | BnOB | text | Numerical columns reporting Brain Olfactory Bulb (BnOB) tissue log10 titer/gram, in the units specified in ‘units’, collected from each ferret day 3 post-inoculation. NA, represents no tissue sample was collected. LOD, represents a tissue… |
| `bn` | Bn | text | Numerical columns reporting Brain (Bn) tissue log10 titer/gram, in the units specified in ‘units’, collected from each ferret day 3 post-inoculation. NA, represents no tissue sample was collected. LOD, represents a tissue sample was collec… |
| `int` | Int | text | Numerical columns reporting Intestine (Int) tissue log10 titer/gram, in the units specified in ‘units’, collected from each ferret day 3 post-inoculation. NA, represents no tissue sample was collected. LOD, represents a tissue sample was c… |

### cr56-k9wj

**An aggregated dataset of serially collected influenza A virus morbidity and titer measurements from virus-infected ferrets.** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/cr56-k9wj.json`
- Metadata: `GET https://data.cdc.gov/api/views/cr56-k9wj.json`; page: https://data.cdc.gov/d/cr56-k9wj
- Topics: Category: National Center for Immunization and Respiratory Diseases
- Tags: `influenza`, `pathogenesis`, `ferret`, `animal model`, `risk assessment`, `in vivo`, `flu`, `virus`, `ncird`, `ncird-id`
- Rows: 851. Data updated: 2026-03-09. Probe status: 200.
- Source: Influenza Division/Immunology and Pathogenesis Branch/Pathogenesis Laboratory Team
- Description: Data from influenza A virus (IAV) infected ferrets (Mustela putorius furo) provides invaluable information towards the study of novel and emerging viruses that pose a threat to human health. This gold standard animal model can recapitulate many clinical signs of infection present in IAV-infected humans, support virus replication of human and zoonotic strains without prior adaptation, and permit evaluation of virus transmissibility by multiple modes. While ferrets have been employed in risk assessment settings for >20 years, results from this work are typically reported in discrete stand-alone…
- Sample row fields ($limit=1): `ferret`, `virus`, `inoc_dose`, `units`, `expt`, `lethal`, `lethal_day`, `nw_typical`, `rd_trans`, `hpai`, `hpai_mbaa`, `ha`, `na`, `origin`, `wt_loss`, `wt_loss_day`, `temp`, `temp_day`, `temp_5`, `temp_5_day`, `d1_inoc`, `d3_inoc`, `d5_inoc`, `d7_inoc`, `d9_inoc`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `ferret` | Ferret | text | Unique observational ID for each individual animal in the dataset. |
| `virus` | Virus | text | Unique identifier for each virus used to inoculate ferrets in the dataset. |
| `inoc_dose` | inoc_dose | number | Numeric column that indicates the log10 infectious units used to intranasally inoculate the ferret (in a 1ml total volume, with virus diluted in PBS). |
| `units` | units | text | Binary column that indicates if log10 titers reported in NW columns are reported as EID50 (titration in eggs, EID) or PFU (titration in cells, PFU). EID and PFU units are not interchangeable; see usage notes for limitations in drawing comp… |
| `expt` | expt | text | Binary column that indicates if experimental results within the row are limited to virus-inoculated animals only (path) or if respiratory droplet transmissibility to a contact animal was concurrently assessed and reported within the row (R… |
| `lethal` | lethal | checkbox | Binary column that indicates if the ferret survived the 14 day p.i. inoculation period (FALSE) or was humanely euthanized between days 1-14 p.i. due to reaching experimental endpoints (TRUE). |
| `lethal_day` | lethal_day | number | Numerical column that indicates the day p.i. an animal was euthanized if humane endpoint criteria were reached (animals surviving the infection are reflected as 0). |
| `nw_typical` | NW_typical | checkbox | Binary column that indicates if every-other-day NW sample collection started on day 1 p.i. (TRUE) or day 2 p.i. (FALSE). |
| `rd_trans` | RD_trans | text | Binary column that indicates (when a respiratory droplet transmission assessment was conducted) if virus transmission was observed based on the criteria described in the Methods (TRUE) or not (FALSE). |
| `hpai` | HPAI | checkbox | Binary column that indicates if the inoculating virus has been classified as a highly pathogenic avian influenza (HPAI) virus based on criteria of the intravenous pathogenicity index15 (TRUE) or is a low pathogenic avian influenza (LPAI) o… |
| `hpai_mbaa` | HPAI_MBAA | checkbox | Binary column that indicates if the inoculating virus is a HPAI virus that includes a multibasic amino acid HA cleavage site (TRUE) or is a HPAI virus that does not include this molecular feature or is not identified as a HPAI virus (FALSE… |
| `ha` | HA | text | Categorical column indicating hemagglutinin subtype of the inoculating virus. |
| `na` | NA | text | Categorical column indicating neuraminidase subtype of the inoculating virus. |
| `origin` | Origin | text | Categorical column indicating the host origin of the inoculating virus. Avian, isolated from avian host or originated from an avian species during a zoonotic spillover to humans; human, human origin; swine, swine origin; canine, canine ori… |
| `wt_loss` | wt_loss | number | Numerical column that specifies the maximum percentage weight loss (normalized from preinoculation baseline weight) recorded in the inoculated animal between days 1-14 p.i. (animals with no recorded drop in weight are reflected as 0). |
| `wt_loss_day` | wt_loss_day | number | Numerical column that indicates the day p.i. the maximum percentage weight loss reported in wt_loss was detected (animals with no recorded drop in weight are reflected as 0). |
| `temp` | temp | number | Numerical column that specifies the maximum increase in degrees Celsius (normalized from preinoculation baseline temperature) recorded in the inoculated animal between days 1-14 p.i. (animals with no recorded rise in temperature are reflec… |
| `temp_day` | temp_day | number | Numerical column that indicates the day p.i. the maximum percentage weight loss reported in temp was detected (animals with no recorded drop in weight are reflected as 0). |
| `temp_5` | temp_5 | number | Numerical column that specifies the maximum increase in degrees Celsius (normalized from preinoculation baseline temperature) recorded in the inoculated animal between days 1-5 p.i. (animals with no recorded rise in temperature are reflect… |
| `temp_5_day` | temp_5_day | number | Numerical column that indicates the day p.i. the maximum percentage weight loss reported in temp_5 was detected (animals with no recorded drop in weight are reflected as 0). |
| `d1_inoc` | d1_inoc | number | Numerical columns reporting NW log10 titer/ml collected from the inoculated ferret, in the units specified in units. NA, no NW was collected that day (due to every-other-day sampling schedule, or because the ferret was euthanized due to re… |
| `d2_inoc` | d2_inoc | number | Numerical columns reporting NW log10 titer/ml collected from the inoculated ferret, in the units specified in units. NA, no NW was collected that day (due to every-other-day sampling schedule, or because the ferret was euthanized due to re… |
| `d3_inoc` | d3_inoc | number | Numerical columns reporting NW log10 titer/ml collected from the inoculated ferret, in the units specified in units. NA, no NW was collected that day (due to every-other-day sampling schedule, or because the ferret was euthanized due to re… |
| `d4_inoc` | d4_inoc | number | Numerical columns reporting NW log10 titer/ml collected from the inoculated ferret, in the units specified in units. NA, no NW was collected that day (due to every-other-day sampling schedule, or because the ferret was euthanized due to re… |
| `d5_inoc` | d5_inoc | number | Numerical columns reporting NW log10 titer/ml collected from the inoculated ferret, in the units specified in units. NA, no NW was collected that day (due to every-other-day sampling schedule, or because the ferret was euthanized due to re… |
| `d6_inoc` | d6_inoc | number | Numerical columns reporting NW log10 titer/ml collected from the inoculated ferret, in the units specified in units. NA, no NW was collected that day (due to every-other-day sampling schedule, or because the ferret was euthanized due to re… |
| `d7_inoc` | d7_inoc | number | Numerical columns reporting NW log10 titer/ml collected from the inoculated ferret, in the units specified in units. NA, no NW was collected that day (due to every-other-day sampling schedule, or because the ferret was euthanized due to re… |
| `d8_inoc` | d8_inoc | number | Numerical columns reporting NW log10 titer/ml collected from the inoculated ferret, in the units specified in units. NA, no NW was collected that day (due to every-other-day sampling schedule, or because the ferret was euthanized due to re… |
| `d9_inoc` | d9_inoc | number | Numerical columns reporting NW log10 titer/ml collected from the inoculated ferret, in the units specified in units. NA, no NW was collected that day (due to every-other-day sampling schedule, or because the ferret was euthanized due to re… |

### v58w-vynu

**Respiratory Conditions Treated in the Emergency Department** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/v58w-vynu.json`
- Metadata: `GET https://data.cdc.gov/api/views/v58w-vynu.json`; page: https://data.cdc.gov/d/v58w-vynu
- Topics: Category: National Center for Immunization and Respiratory Diseases
- Tags: `respiratory-virus-response`, `virus`, `rvr`, `ophdst`, `ncird`, `bacteria`, `ed data`, `ari other`
- Rows: 12,397. Data updated: 2026-11-06. Probe status: 200.
- Description: Methods for Creating Respiratory Conditions: The International Classification of Diseases, Tenth Revision, Clinical Modification (ICD-10-CM) discharge diagnostic codes listed in the Acute Respiratory Index (ARI) were used as a starting point to define respiratory conditions. For a list of diagnostic codes included in the ARI metric, visit the <a href="https://cdn.ymaws.com/www.cste.org/resource/resmgr/pdfs/CDC_Broad_Acute_Respiratory_.pdf">Acute Respiratory Illness Technical Brief</a>. These codes were further refined to exclude pathogen-specific codes and, when appropriate, were grouped usin…
- Sample row fields ($limit=1): `week_end`, `condition`, `percent_visits`, `age_group`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `week_end` | week_end | calendar_date |  |
| `condition` | condition | text |  |
| `percent_visits` | percent_visits | number |  |
| `age_group` | age_group | text |  |

## Usage tips

- Pick the dataset by question:
  - Share of emergency department visits for a respiratory condition, nationally by week: `v58w-vynu`. `condition` has 11 values (`Pneumonia`, `Bronchiolitis`, `Croup`, `Sinus infection`, ...); `age_group` is `Overall`, `Infants 0-1`, `Kids 2-4`, `Kids 5-17`, `Adults 18-49`, `Adults 50-64`, `Seniors 65+`. `percent_visits` is a percentage of all ED visits.
  - Influenza A virus in ferrets: day-3 tissue titers `d9u6-mdu6` (one row per ferret); serial nasal wash titers, weight loss, temperature, lethality and transmission `cr56-k9wj`. Some titer columns are `text` because missing samples are coded `NA`.
- Examples:

  ```
  # Pneumonia share of ED visits for seniors, newest weeks first
  GET https://data.cdc.gov/resource/v58w-vynu.json?$where=condition='Pneumonia' AND age_group='Seniors 65+'&$order=week_end DESC&$limit=10
  # Ferrets per HA subtype and lethality
  GET https://data.cdc.gov/resource/cr56-k9wj.json?$select=ha,lethal,count(*) as n&$group=ha,lethal&$order=ha
  ```
