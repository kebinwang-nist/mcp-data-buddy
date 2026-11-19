---
name: cdc-public-health-infrastructure
description: Query CDC open data (data.cdc.gov, Socrata SODA API) for the National Center for State, Tribal, Local, and Territorial Public Health Infrastructure and Workforce category. Use it for the CDC Text Corpora for Learners, the article metadata (title, series, date, DOI, keywords, authors) and HTML mirror file lists of the MMWR, Emerging Infectious Diseases (EID) and Preventing Chronic Disease (PCD) journals.
---

# CDC open data: National Center for State, Tribal, Local, and Territorial Public Health Infrastructure and Workforce

## Overview

- Portal: `https://data.cdc.gov` (Socrata). Category browse page: `https://data.cdc.gov/browse?category=National+Center+for+State%2C+Tribal%2C+Local%2C+and+Territorial+Public+Health+Infrastructure+and+Workforce`.
- Catalog snapshot taken 2026-11-09: 2 public assets in the category: 2 datasets, 0 filtered views, 0 maps, 0 charts.
- Excluded (not public or no API endpoint): none.
- Common tags (number of assets): `corpora` (2), `corpus` (2), `data science` (2), `eid` (2), `harvest-cdc-journals` (2), `informatics` (2), `language` (2), `machine learning` (2), `ml` (2), `mmwr` (2), `morphology` (2), `ncstltphiw` (2), `pcd` (2), `phic` (2), `text analysis` (2), `ai` (1), `linguistic` (1), `linguistics` (1), `llm` (1), `nlp` (1).
- Surface: read-only `GET`. Each dataset and filtered view has its own data endpoint keyed by a 4x4 id (e.g. `ut5n-bmc3`). Maps and charts have no data endpoint of their own; query their parent dataset instead.
- Auth: none for reads. An optional Socrata app token in header `X-App-Token` raises the throttling limit; without one, heavy use from one IP may get HTTP 429. No key for this API exists in this project.
- Types: Socrata column types are `text`, `number`, `calendar_date` (floating timestamp, returned as `2024-10-04T00:00:00.000`), `point` (GeoJSON `{"type":"Point","coordinates":[lon,lat]}`), `url` (`{"url": ...}`), `checkbox` (boolean). In JSON output, numbers come back as strings. Null fields are omitted from a row object rather than returned as `null`.
- Topics and tags: each section's `Topics` and `Tags` lines come from the dataset's intro page (`/d/{id}`, "About this Dataset"), read from `/api/views/{id}.json`. `Sample row fields` lists the field names one `$limit=1` row returned; values were not stored.
- Freshness: both datasets are one release built in March 2024 from content retrieved in January 2024 (update frequency irregular). The article text itself is in ZIP attachments on the dataset pages, not in the API rows.

## Endpoints per asset

Replace `{id}` with the asset id from the index.

| Purpose | Endpoint |
|---|---|
| Rows as JSON (SODA 2.1, SoQL params) | `GET https://data.cdc.gov/resource/{id}.json` |
| Rows as CSV / GeoJSON | `GET https://data.cdc.gov/resource/{id}.csv`, `.geojson` |
| Column + view metadata | `GET https://data.cdc.gov/api/views/{id}.json` |
| Full export (no row limit) | `GET https://data.cdc.gov/api/views/{id}/rows.csv?accessType=DOWNLOAD` |
| Human page | `https://data.cdc.gov/d/{id}` |
| Catalog search (this category) | `GET https://api.us.socrata.com/api/catalog/v1?domains=data.cdc.gov&categories=National%20Center%20for%20State%2C%20Tribal%2C%20Local%2C%20and%20Territorial%20Public%20Health%20Infrastructure%20and%20Workforce&limit=100` |

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
| 1 | [`ut5n-bmc3`](#ut5n-bmc3) | CDC Text Corpora for Learners: HTML Mirrors of MMWR, EID, and PCD | dataset |  | 33,576 | 8 | 2024-03-20 | Irregular | 200 |
| 2 | [`7rih-tqi5`](#7rih-tqi5) | CDC Text Corpora for Learners: MMWR, EID, and PCD Article Metadata | dataset |  | 33,567 | 23 | 2024-03-21 | Irregular | 200 |

## Datasets and filtered views

### ut5n-bmc3

**CDC Text Corpora for Learners: HTML Mirrors of MMWR, EID, and PCD** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/ut5n-bmc3.json`
- Metadata: `GET https://data.cdc.gov/api/views/ut5n-bmc3.json`; page: https://data.cdc.gov/d/ut5n-bmc3
- Topics: Category: National Center for State, Tribal, Local, and Territorial Public Health Infrastructure and Workforce
- Tags: `harvest-cdc-journals`, `text analysis`, `corpus`, `corpora`, `ncstltphiw`, `phic`, `informatics`, `data science`, `nlp`, `mmwr`, `pcd`, `eid`, `ai`, `ml`, `machine learning`, `llm`, `language`, `semantic`, `linguistic`, `morphology`
- Rows: 33,576. Data updated: 2024-03-20. Probe status: 200.
- Update frequency: Irregular.
- Source: NCSTLTPHIW(PHIC)
- Description: The attached ZIP archives are part of the <a href="https://github.com/cmheilig/harvest-cdc-journals">CDC Text Corpora for Learners</a> program. This version, comprised of 33,567 articles, was constructed on 2024-03-01 using source content retrieved on 2024-01-09. The attached three ZIP archives contain the 33,567 articles in 33,576 compiled HTML mirrors of the MMWR <a href="https://www.cdc.gov/mmwr/">Morbidity and Mortality Weekly Report</a> including its series: <i>Weekly Reports</i>, <i>Recommendations and Reports</i>, <i>Surveillance Summaries</i>, <i>Supplements</i>, and <i>Notifiable Dis…
- Sample row fields ($limit=1): `series`, `length`, `method`, `size`, `cmpr`, `date_time`, `crc_32`, `name`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `series` | Series | text | journal series |
| `length` | Length | number | uncompressed file size |
| `method` | Method | text | method of compression |
| `size` | Size | number | compressed file size |
| `cmpr` | Cmpr | number | compression percentage |
| `date_time` | Date Time | calendar_date | creation date time |
| `crc_32` | CRC-32 | text | CRC-32 rom zip archive |
| `name` | Name | text | filename (including partial path information) |

### 7rih-tqi5

**CDC Text Corpora for Learners: MMWR, EID, and PCD Article Metadata** (dataset)

- Endpoint: `GET https://data.cdc.gov/resource/7rih-tqi5.json`
- Metadata: `GET https://data.cdc.gov/api/views/7rih-tqi5.json`; page: https://data.cdc.gov/d/7rih-tqi5
- Topics: Category: National Center for State, Tribal, Local, and Territorial Public Health Infrastructure and Workforce
- Tags: `harvest-cdc-journals`, `corpora`, `corpus`, `ncstltphiw`, `phic`, `informatics`, `data science`, `text analysis`, `mmwr`, `eid`, `pcd`, `smokefree indoor air`, `ml`, `machine learning`, `language`, `linguistics`, `semantics`, `morphology`
- Rows: 33,567. Data updated: 2024-03-21. Probe status: 200.
- Update frequency: Irregular.
- Source: NCSTLTPHIW(PHIC)
- Description: This landing page is part of the <a href="https://github.com/cmheilig/harvest-cdc-journals">CDC Text Corpora for Learners</a> program; this includes the compiled 33,576 CDC Text for Learners <a href="https://data.cdc.gov/National-Center-for-State-Tribal-Local-and-Territo/CDC-Text-Corpora-for-Learners-HTML-Mirrors-of-MMWR/ut5n-bmc3/about_data">HTML mirrors</a> of the MMWR <a href="https://www.cdc.gov/mmwr/">Morbidity and Mortality Weekly Report</a> including its series: <i>Weekly Reports</i>, <i>Recommendations and Reports</i>, <i>Surveillance Summaries</i>, <i>Supplements</i>, and <i>Notifiab…
- Sample row fields ($limit=1): `url`, `stratum`, `collection`, `series`, `level`, `lang`, `dl_year_mo`, `dl_vol_iss`, `dl_date`, `dateline`, `base`, `string`, `mirror_path`, `title`

| Field name | Display name | Type | Description |
|---|---|---|---|
| `url` | url | url | URL of retrieved document (primary key) |
| `stratum` | stratum | text | journal (mmwr, eid, or pcd) and scope (toc or art) |
| `collection` | collection | text | series, scope, and language code |
| `series` | series | text | CDC series (mmwr, mmrr, mmss, mmsu, mmnd, eid, pcd) |
| `level` | level | text | level in hierarchy (home, series, volume, issue, article) |
| `lang` | lang | text | language (en, es, fr, zhs, zht) |
| `dl_year_mo` | dl_year_mo | text | year and month of volume (YYYY or YYYY-MM) |
| `dl_vol_iss` | dl_vol_iss | text | volume and issue (VV, VV(II), or VV(IIII)) |
| `dl_date` | dl_date | text | date of publication (YYYY-MM-DD) |
| `dl_page` | dl_page | text | first arabic page number of article (MMWR, EID) (DDDD) |
| `dl_art_num` | dl_art_num | text | article number (PCD) (ADDD or EDDD) |
| `dateline` | dateline | text | dateline string from document or auxiliary |
| `base` | base | url | base URL from which document reference was harvested |
| `string` | string | text | text of <a> element referring to document |
| `link_canon` | link_canon | text | canonical link from <link> |
| `mirror_path` | mirror_path | text | folder path and filename in mirror |
| `md_citation_doi` | md_citation_doi | text | citation DOI from <meta> |
| `title` | title | text | title from <title> |
| `md_citation_categories` | md_citation_categories | text | citation categories from <meta> |
| `dl_cat` | dl_cat | text | category from dateline |
| `md_kwds` | md_kwds | text | keywords from <meta>, pipe-delimited if > 1 |
| `md_desc` | md_desc | text | description from <meta> |
| `md_citation_author` | md_citation_author | text | citation author(s) from <meta>, pipe-delimited if > 1 |

## Usage tips

- Pick the dataset by question:
  - Articles and pages (one row per document, `url` is the key): `7rih-tqi5`. `series` is `mmwr`, `mmrr`, `mmss`, `mmsu`, `mmnd`, `eid`, `eid0`, `eid1`, `eid2` or `pcd`; `level` is `volume`, `issue` or `article`; `lang` is `en`, `es`, `fr`, `zhs` or `zht`.
  - Files in the HTML mirror ZIP archives (name, size, CRC): `ut5n-bmc3`.
- `dl_date` and `dl_year_mo` are `text` (`YYYY-MM-DD`, `YYYY-MM`), so they compare and sort as strings. `md_kwds` and `md_citation_author` are pipe-delimited lists; search them with `like '%word%'`. `url` and `base` are `url` columns (objects with a `url` key).
- Examples:

  ```
  # Documents per series
  GET https://data.cdc.gov/resource/7rih-tqi5.json?$select=series,count(*) as n&$group=series&$order=n DESC
  # Spanish-language MMWR articles
  GET https://data.cdc.gov/resource/7rih-tqi5.json?$select=title,dl_date&$where=series='mmwr' AND lang='es' AND level='article'&$order=dl_date DESC&$limit=20
  ```
