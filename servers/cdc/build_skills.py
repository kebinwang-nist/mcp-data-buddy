"""Generate SKILL.md files for CDC open data (data.cdc.gov) topics.

Run from the project root:
``uv run python -m servers.cdc.build_skills [skill_dir ...]``, e.g.
``uv run python -m servers.cdc.build_skills smoking_tobacco``. With no arguments every topic in
``_CATEGORIES`` is rebuilt.

1. The Socrata catalog API lists every asset in the topic's CDC category.
2. Only public assets with an API endpoint are kept: type ``dataset``, ``filter``, ``map`` or
   ``chart``; catalog ``Common-Core_Public-Access-Level`` not ``restricted public`` or
   ``non-public``; and ``GET /api/views/{id}.json`` succeeds with a ``public`` grant. The others
   are counted in the Overview's "Excluded" line. A 401/403/404 on that call counts as not
   public; a 5xx or transport error is retried, and if it persists, or on any other 4xx, the
   run aborts before writing the skill.
3. ``GET /api/views/{id}.json`` gives each asset's columns, parent dataset, filter condition and
   the Topics (``category``) and Tags (``tags``) shown on its intro page ``/d/{id}``.
4. Each dataset and filtered view is called with ``$limit=1`` and ``$select=count(*)`` to check
   the endpoint and record its row count. Only the field names of the sample row are kept,
   never the values.
5. ``skills/<skill_dir>/SKILL.md`` is written with an endpoint index and one ``### <id>`` section
   of columns per queryable asset.

The front-matter description, extra overview bullets and usage tips of each topic are kept in
``_CATEGORIES`` below; edit them there, not in the generated file.
"""

from __future__ import annotations

import re
import ssl
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import quote, quote_plus

import httpx
import truststore

_PACKAGE_DIR = Path(__file__).resolve().parent
_SKILLS_DIR = _PACKAGE_DIR / "skills"
_HOST = "data.cdc.gov"
_DOMAIN = f"https://{_HOST}"
_CATALOG_URL = "https://api.us.socrata.com/api/catalog/v1"
_REQUEST_INTERVAL = 0.2
_TIMEOUT_SECONDS = 60.0
_MAX_RETRIES = 3
_QUERYABLE = ("dataset", "filter")
_TYPE_ORDER = {"dataset": 0, "filter": 1, "map": 2, "chart": 3}
_NOT_PUBLIC_LEVELS = ("restricted public", "non-public")
_ACCESS_LEVEL_KEYS = ("Common-Core_Public-Access-Level", "Common-Core-3_Public-Access-Level")
_COMMON_TAGS = 20
_METADATA_ATTEMPTS = 4  # waits of 1 s, 2 s and 4 s between attempts
_NOT_PUBLIC_STATUSES = (401, 403, 404)


@dataclass(frozen=True, slots=True)
class Category:
    """Hand-written parts of one category's skill."""

    title: str  # Socrata category name, e.g. "Vaccinations"
    skill_name: str
    description: str
    overview: str  # extra markdown bullets appended to ## Overview
    tips: str  # markdown body of ## Usage tips


_CATEGORIES = {
    "vaccinations": Category(
        title="Vaccinations",
        skill_name="cdc-vaccinations",
        description=(
            "Query CDC open data (data.cdc.gov, Socrata SODA API) for the Vaccinations "
            "category. Use it for vaccination coverage of children, adolescents, adults, "
            "pregnant women, health care personnel and nursing home residents (National "
            "Immunization Survey, IQVIA, Medicare and Household Pulse based estimates), flu "
            "vaccination coverage and doses distributed, COVID-19 vaccinations, vaccine "
            "allocations, COVID-19 vaccine hesitancy estimates by county, kindergarten "
            "vaccination coverage and exemptions, and RSV vaccination and nirsevimab."
        ),
        overview="""\
- Freshness: the daily COVID-19 vaccination series (`8xkx-amqh` county, `unsk-b7fc` jurisdiction, `rh2h-3yt2` trends, `km4m-vcsb` demographics, `5i5k-6cmh` age and sex, booster datasets) stopped on 2023-05-12, and the vaccine allocation datasets stopped in 2021. Still updated in 2026: the RespVaxView survey data (`ee83-ukst`, `5c6r-xi2t`, `94wp-9pid`, `ksfb-ug5d`, `eanj-9nie`, `8yup-c35n`), monthly COVID-19 and RSV dose counts (`3bmy-cyyd`, `q84f-e68r`, `2yum-eg9f`, `vhcj-3k53`), Medicare beneficiary coverage (`jjpx-mxt8`), adult coverage `aetd-68ew` and kindergarten coverage `ijqb-a7ye`.
- Several datasets share a name (e.g. `vugp-mqip` / `wtw5-4wi3`, `n2zz-25mk` / `2yum-eg9f`, `eudc-n39h` / `vfj2-bfuw`). Compare "Data updated" and the columns before choosing. `3myw-4j4q` has 0 rows; its archived copy `8dyx-9z99` has the data.""",
        tips="""\
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
  ```""",
    ),
    "smoking_tobacco": Category(
        title="Smoking & Tobacco Use",
        skill_name="cdc-smoking-tobacco",
        description=(
            "Query CDC open data (data.cdc.gov, Socrata SODA API) for the Smoking & Tobacco Use "
            "category. Use it for adult smoking prevalence by state and year from the "
            "Behavioral Risk Factor Surveillance System (BRFSS), 1995-2011 (current smokers, "
            "every-day and some-day smokers, former smokers and never smokers)."
        ),
        overview="""\
- Freshness: all three datasets are BRFSS snapshots last updated in 2013 and stop at 2011. For later years, use the BRFSS portal or the NCHS / Vaccinations categories, not this one.""",
        tips="""\
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
  ```""",
    ),
    "nchs": Category(
        title="National Center for Health Statistics",
        skill_name="cdc-nchs",
        description=(
            "Query CDC open data (data.cdc.gov, Socrata SODA API) for the National Center for "
            "Health Statistics (NCHS) category. Use it for deaths and mortality (provisional "
            "and final counts by cause, age, sex, race and place, drug overdose, excess and "
            "COVID-19 deaths, life expectancy), births and fertility, health survey estimates "
            "(NHIS, NHANES, Household Pulse, Rapid Surveys), health care use and insurance, "
            "and the Health, United States (DQS) tables."
        ),
        overview="""\
- Freshness: still updated in 2026: provisional COVID-19 deaths by week and state `r8kw-7aab`, percent of deaths for COVID-19, influenza and RSV `4bc2-bbpq` / `53g5-jf7x`, VSRR drug overdose deaths `xkb8-kh2a` (state) and `gb4e-yj24` (county), maternal deaths `e2d5-ggg7`, quarterly VSRR birth and mortality indicators, NHIS summary statistics and the `DQS` (Health, United States) tables. Most `AH` ("ad hoc") datasets and many COVID-19 datasets stopped between 2020 and 2023. Check "Data updated" in the index.
- Not in the index: 80 `href` assets (links to external files, 66 of them restricted-use research data) have no API endpoint and were left out.""",
        tips="""\
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
  ```""",
    ),
    "ncird": Category(
        title="National Center for Immunization and Respiratory Diseases",
        skill_name="cdc-ncird",
        description=(
            "Query CDC open data (data.cdc.gov, Socrata SODA API) for the National Center for "
            "Immunization and Respiratory Diseases (NCIRD) category. Use it for weekly "
            "emergency department visit shares for respiratory conditions (pneumonia, "
            "bronchiolitis, croup, sinus infection and others) by age group, and for influenza "
            "A virus ferret studies (viral titers in tissues, weight loss, fever, lethality and "
            "transmission)."
        ),
        overview="""\
- Freshness: `v58w-vynu` (respiratory conditions in the emergency department) is updated weekly and starts in October 2023. The two ferret datasets are fixed research releases.""",
        tips="""\
- Pick the dataset by question:
  - Share of emergency department visits for a respiratory condition, nationally by week: `v58w-vynu`. `condition` has 11 values (`Pneumonia`, `Bronchiolitis`, `Croup`, `Sinus infection`, ...); `age_group` is `Overall`, `Infants 0-1`, `Kids 2-4`, `Kids 5-17`, `Adults 18-49`, `Adults 50-64`, `Seniors 65+`. `percent_visits` is a percentage of all ED visits.
  - Influenza A virus in ferrets: day-3 tissue titers `d9u6-mdu6` (one row per ferret); serial nasal wash titers, weight loss, temperature, lethality and transmission `cr56-k9wj`. Some titer columns are `text` because missing samples are coded `NA`.
- Examples:

  ```
  # Pneumonia share of ED visits for seniors, newest weeks first
  GET https://data.cdc.gov/resource/v58w-vynu.json?$where=condition='Pneumonia' AND age_group='Seniors 65+'&$order=week_end DESC&$limit=10
  # Ferrets per HA subtype and lethality
  GET https://data.cdc.gov/resource/cr56-k9wj.json?$select=ha,lethal,count(*) as n&$group=ha,lethal&$order=ha
  ```""",
    ),
    "public_health_infrastructure": Category(
        title=(
            "National Center for State, Tribal, Local, and Territorial Public Health "
            "Infrastructure and Workforce"
        ),
        skill_name="cdc-public-health-infrastructure",
        description=(
            "Query CDC open data (data.cdc.gov, Socrata SODA API) for the National Center for "
            "State, Tribal, Local, and Territorial Public Health Infrastructure and Workforce "
            "category. Use it for the CDC Text Corpora for Learners, the article metadata "
            "(title, series, date, DOI, keywords, authors) and HTML mirror file lists of the "
            "MMWR, Emerging Infectious Diseases (EID) and Preventing Chronic Disease (PCD) "
            "journals."
        ),
        overview="""\
- Freshness: both datasets are one release built in March 2024 from content retrieved in January 2024 (update frequency irregular). The article text itself is in ZIP attachments on the dataset pages, not in the API rows.""",
        tips="""\
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
  ```""",
    ),
    "respiratory_viruses": Category(
        title="Coronavirus and Other Respiratory Viruses",
        skill_name="cdc-respiratory-viruses",
        description=(
            "Query CDC open data (data.cdc.gov, Socrata SODA API) for the Coronavirus and Other "
            "Respiratory Viruses category. Use it for daily emergency department visit shares "
            "for COVID-19, influenza, RSV and acute respiratory illness by state (NSSP), "
            "imputed weekly RSV hospitalization counts by state for 2018-2024, and a SARS-CoV-2 "
            "serology test comparison panel."
        ),
        overview="""\
- Freshness: `vjzj-u7u8` (NSSP emergency department visits) is updated daily from September 2022. `whhs-7a5d` (imputed RSV hospitalizations) covers 2018-2024 and is no longer updated, and `hhvg-83jq` is a one-off 2023 study.""",
        tips="""\
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
  ```""",
    ),
}


@dataclass(slots=True)
class Asset:
    """One catalog asset with what the generator learned about it."""

    id: str
    name: str
    type: str
    description: str
    data_updated: str
    meta_updated: str
    update_frequency: str
    parents: list[str]
    columns: list[dict[str, Any]]
    view_filter: str
    attribution: str
    status: int | None = None
    rows: int | None = None
    extra_fields: list[str] = field(default_factory=list)


class _Api:
    """Throttled GET client for the Socrata APIs."""

    def __init__(self) -> None:
        self._client = httpx.Client(
            timeout=_TIMEOUT_SECONDS,
            verify=truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT),
            headers={"Accept": "application/json"},
        )
        self._last = 0.0

    def get(self, url: str, params: dict[str, str | int] | None = None) -> httpx.Response:
        """GET ``url``, waiting between calls and backing off on HTTP 429."""
        for attempt in range(_MAX_RETRIES + 1):
            wait = self._last + _REQUEST_INTERVAL - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
            response = self._client.get(url, params=params)
            if response.status_code != 429 or attempt == _MAX_RETRIES:
                return response
            time.sleep(10 * (attempt + 1))
        raise AssertionError("unreachable")

    def json(self, url: str, params: dict[str, str | int] | None = None) -> Any:
        response = self.get(url, params)
        response.raise_for_status()
        return response.json()


def _one_line(text: object) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _cell(text: object, limit: int = 0) -> str:
    """Make ``text`` safe for one markdown table cell, optionally truncated."""
    value = _one_line(text).replace("|", "\\|")
    if limit and len(value) > limit:
        value = value[: limit - 1].rstrip() + "…"
    return value


def _date(value: object) -> str:
    if isinstance(value, int | float):
        return datetime.fromtimestamp(value, UTC).strftime("%Y-%m-%d")
    return str(value or "")[:10]


def _view_filter(query_string: str) -> str:
    """Return the WHERE/ORDER BY/GROUP BY tail of a filtered view's SoQL ``queryString``."""
    match = re.search(
        r"\b(WHERE|ORDER BY|GROUP BY|LIMIT)\b.*", _one_line(query_string), re.IGNORECASE
    )
    return match.group(0) if match else ""


def _update_frequency(view: dict[str, Any]) -> str:
    custom = (view.get("metadata") or {}).get("custom_fields") or {}
    for group in custom.values():
        if isinstance(group, dict) and group.get("Update Frequency"):
            return str(group["Update Frequency"])
    return ""


@dataclass(slots=True)
class CdcAsset(Asset):
    """A catalog asset plus its intro-page Topics/Tags and sample-row field names."""

    topics: str = ""
    tags: list[str] = field(default_factory=list)
    sample_fields: list[str] = field(default_factory=list)
    access_level: str = ""


def _access_level(result: dict[str, Any]) -> str:
    """Return the catalog ``Public-Access-Level`` of a catalog result, lowercased ("" if blank)."""
    metadata = {
        entry.get("key"): entry.get("value")
        for entry in (result.get("classification") or {}).get("domain_metadata") or []
    }
    for key in _ACCESS_LEVEL_KEYS:
        if metadata.get(key):
            return _one_line(metadata[key]).lower()
    return ""


def _has_public_grant(view: dict[str, Any]) -> bool:
    """Return whether the view metadata grants the ``public`` flag."""
    return any("public" in (grant.get("flags") or []) for grant in view.get("grants") or [])


def _view_metadata(api: _Api, asset_id: str) -> httpx.Response:
    """GET ``/api/views/{asset_id}.json``, retrying 5xx responses and transport errors.

    Returns:
        A successful response, or a 401/403/404 response (the view is not publicly readable).

    Raises:
        RuntimeError: On any other 4xx, or when a 5xx or transport error persists after
            ``_METADATA_ATTEMPTS`` attempts. This aborts the run so a public dataset is never
            dropped from a skill because of a transient error.
    """
    url = f"{_DOMAIN}/api/views/{asset_id}.json"
    problem, attempt = "", 0
    error: httpx.TransportError | None = None
    for attempt in range(1, _METADATA_ATTEMPTS + 1):
        try:
            response = api.get(url)
        except httpx.TransportError as exc:
            problem, error = f"{type(exc).__name__}: {exc}", exc
        else:
            if response.is_success or response.status_code in _NOT_PUBLIC_STATUSES:
                return response
            problem, error = f"HTTP {response.status_code}", None
            if response.status_code < 500:
                break
        if attempt < _METADATA_ATTEMPTS:
            print(
                f"{asset_id}: metadata {problem}, retry {attempt}/{_METADATA_ATTEMPTS - 1}",
                file=sys.stderr,
                flush=True,
            )
            time.sleep(2 ** (attempt - 1))
    raise RuntimeError(
        f"GET {url} failed for {asset_id}: {problem} after {attempt} attempt(s); "
        "aborting so no partial skill is written"
    ) from error


def _collect(api: _Api, category: Category) -> tuple[list[CdcAsset], dict[str, str], Counter[str]]:
    """List the topic's public assets and probe each one.

    Returns:
        The kept assets, id -> name for assets and their parents, and the count of excluded
        assets per reason.
    """
    catalog = api.json(
        _CATALOG_URL,
        {
            "domains": _HOST,
            "search_context": _HOST,
            "categories": category.title,
            "limit": 1000,
        },
    )
    assets: list[CdcAsset] = []
    excluded: Counter[str] = Counter()
    for result in catalog["results"]:
        resource = result["resource"]
        asset_id, asset_type = resource["id"], resource["type"]
        if asset_type not in _TYPE_ORDER:
            excluded[f"`{asset_type}` (no API endpoint)"] += 1
            continue
        level = _access_level(result)
        if level in _NOT_PUBLIC_LEVELS:
            excluded[level] += 1
            continue
        response = _view_metadata(api, asset_id)
        if not response.is_success:
            excluded[f"metadata HTTP {response.status_code}"] += 1
            continue
        view = response.json()
        if not _has_public_grant(view):
            excluded["no public grant"] += 1
            continue
        parents = [*(resource.get("parent_fxf") or []), view.get("modifyingViewUid")]
        assets.append(
            CdcAsset(
                id=asset_id,
                name=_one_line(resource["name"]),
                type=asset_type,
                description=_one_line(resource.get("description")),
                data_updated=_date(
                    view.get("rowsUpdatedAt")
                    or resource.get("data_updated_at")
                    or resource.get("updatedAt")
                ),
                meta_updated=_date(
                    resource.get("metadata_updated_at") or resource.get("updatedAt")
                ),
                update_frequency=_update_frequency(view),
                parents=[p for p in dict.fromkeys(parents) if p],
                columns=[
                    c
                    for c in view.get("columns") or []
                    if not c.get("fieldName", ":").startswith(":")
                ],
                view_filter=_view_filter(view.get("queryString") or ""),
                attribution=_one_line(view.get("attribution")),
                topics=_one_line(view.get("category")),
                tags=[_one_line(t) for t in view.get("tags") or [] if _one_line(t)],
                access_level=level,
            )
        )

    names = {a.id: a.name for a in assets}
    for parent in {p for a in assets for p in a.parents} - names.keys():
        response = api.get(f"{_DOMAIN}/api/views/{parent}.json")
        if response.is_success:
            other = response.json()
            names[parent] = (
                f"{_one_line(other.get('name'))} ({other.get('category') or 'no category'})"
            )
        else:
            names[parent] = f"HTTP {response.status_code}"

    for asset in assets:
        if asset.type in _QUERYABLE:
            _probe(api, asset)
        print(f"{asset.id} {asset.type}: status={asset.status} rows={asset.rows}", flush=True)
    assets.sort(key=lambda a: (_TYPE_ORDER.get(a.type, 9), a.name.lower()))
    return assets, names, excluded


def _probe(api: _Api, asset: CdcAsset) -> None:
    """Record the field names of one sample row and the row count of a dataset or view.

    The sample row's values are discarded; only its keys are stored.
    """
    url = f"{_DOMAIN}/resource/{asset.id}.json"
    try:
        response = api.get(url, {"$limit": 1})
        asset.status = response.status_code
        if response.is_success and (rows := response.json()):
            asset.sample_fields = [k for k in rows[0] if not k.startswith(":")]
            listed = {c["fieldName"] for c in asset.columns}
            asset.extra_fields = sorted(k for k in asset.sample_fields if k not in listed)
        response = api.get(url, {"$select": "count(*) as n"})
        if response.is_success and (rows := response.json()):
            asset.rows = int(rows[0].get("n", 0))
    except httpx.HTTPError as exc:
        print(f"{asset.id}: {type(exc).__name__}: {exc}", file=sys.stderr)


def _tags(tags: list[str]) -> str:
    return ", ".join(f"`{_cell(t)}`" for t in tags) or "none"


def _sample_line(asset: CdcAsset) -> str:
    if asset.sample_fields:
        return f"- Sample row fields ($limit=1): {_tags(asset.sample_fields)}"
    if asset.status == 200:
        return "- Sample row: none (0 rows)"
    return f"- Sample row fields ($limit=1): unavailable (probe status {asset.status})"


def _excluded_line(excluded: Counter[str]) -> str:
    total = sum(excluded.values())
    if not total:
        return "- Excluded (not public or no API endpoint): none."
    reasons = ", ".join(f"{n} {reason}" for reason, n in excluded.most_common())
    return f"- Excluded (not public or no API endpoint): {total} assets: {reasons}."


def _common_tags_line(assets: list[CdcAsset]) -> str:
    counts = Counter(t for a in assets for t in dict.fromkeys(a.tags))
    top = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:_COMMON_TAGS]
    if not top:
        return "- Common tags: none."
    tags = ", ".join(f"`{_cell(tag)}` ({n})" for tag, n in top)
    return f"- Common tags (number of assets): {tags}."


def _render(
    category: Category,
    assets: list[CdcAsset],
    names: dict[str, str],
    excluded: Counter[str],
) -> str:
    today = date.today().isoformat()
    queryable = [a for a in assets if a.type in _QUERYABLE]
    visuals = [a for a in assets if a.type not in _QUERYABLE]
    counts = {t: sum(a.type == t for a in assets) for t in _TYPE_ORDER}
    browse = quote_plus(category.title)
    encoded = quote(category.title, safe="")

    def parent_names(asset: Asset) -> str:
        return ", ".join(f"`{p}` ({_cell(names.get(p, '?'))})" for p in asset.parents)

    lines = [
        "---",
        f"name: {category.skill_name}",
        f"description: {category.description}",
        "---",
        "",
        f"# CDC open data: {category.title}",
        "",
        "## Overview",
        "",
        f"- Portal: `{_DOMAIN}` (Socrata). Category browse page: `{_DOMAIN}/browse?category={browse}`.",
        (
            f"- Catalog snapshot taken {today}: {len(assets)} public assets in the category: "
            f"{counts['dataset']} datasets, {counts['filter']} filtered views, {counts['map']} maps, "
            f"{counts['chart']} charts."
        ),
        _excluded_line(excluded),
        _common_tags_line(assets),
        "- Surface: read-only `GET`. Each dataset and filtered view has its own data endpoint keyed "
        "by a 4x4 id (e.g. `" + (queryable[0].id if queryable else "abcd-1234") + "`). Maps and "
        "charts have no data endpoint of their own; query their parent dataset instead.",
        (
            "- Auth: none for reads. An optional Socrata app token in header `X-App-Token` raises the "
            "throttling limit; without one, heavy use from one IP may get HTTP 429. No key for this "
            "API exists in this project."
        ),
        (
            "- Types: Socrata column types are `text`, `number`, `calendar_date` (floating timestamp, "
            "returned as `2024-10-04T00:00:00.000`), `point` (GeoJSON "
            '`{"type":"Point","coordinates":[lon,lat]}`), `url` (`{"url": ...}`), `checkbox` '
            "(boolean). In JSON output, numbers come back as strings. Null fields are omitted from a "
            "row object rather than returned as `null`."
        ),
        (
            "- Topics and tags: each section's `Topics` and `Tags` lines come from the dataset's "
            'intro page (`/d/{id}`, "About this Dataset"), read from `/api/views/{id}.json`. '
            "`Sample row fields` lists the field names one `$limit=1` row returned; values were "
            "not stored."
        ),
    ]
    if category.overview:
        lines.append(category.overview)
    lines += [
        "",
        "## Endpoints per asset",
        "",
        "Replace `{id}` with the asset id from the index.",
        "",
        "| Purpose | Endpoint |",
        "|---|---|",
        f"| Rows as JSON (SODA 2.1, SoQL params) | `GET {_DOMAIN}/resource/{{id}}.json` |",
        f"| Rows as CSV / GeoJSON | `GET {_DOMAIN}/resource/{{id}}.csv`, `.geojson` |",
        f"| Column + view metadata | `GET {_DOMAIN}/api/views/{{id}}.json` |",
        f"| Full export (no row limit) | `GET {_DOMAIN}/api/views/{{id}}/rows.csv?accessType=DOWNLOAD` |",
        f"| Human page | `{_DOMAIN}/d/{{id}}` |",
        (
            f"| Catalog search (this category) | `GET {_CATALOG_URL}?domains={_HOST}"
            f"&categories={encoded}&limit=100` |"
        ),
        "",
        "## Query parameters (SoQL)",
        "",
        "All optional, passed on `/resource/{id}.json`. URL-encode values (spaces as `%20`, `'` as `%27`).",
        "",
        "| Param | Meaning | Example |",
        "|---|---|---|",
        "| `$select` | Columns or expressions | `$select=col_a,col_b` / `$select=count(*) as n` |",
        "| `$where` | Filter (SoQL condition) | `$where=upper(col_a)='X' AND date_col >= '2026-10-01'` |",
        "| `$order` | Sort, `ASC`/`DESC` allowed | `$order=date_col DESC` |",
        "| `$group` | Group by (with aggregates in `$select`) | `$select=col_a,count(*)&$group=col_a` |",
        "| `$having` | Filter on aggregates | `$having=count(*) > 10` |",
        "| `$limit` | Max rows; **default 1000** | `$limit=50000` |",
        "| `$offset` | Rows to skip, for paging (use with a stable `$order`) | `$offset=1000` |",
        "| `$q` | Full-text search across text columns | `$q=influenza` |",
        "| `<field>=<value>` | Simple equality filter | `col_a=X` |",
        "",
        "SoQL notes:",
        "",
        (
            "- String literals use single quotes, and comparison is case-sensitive. Casing is often "
            "inconsistent within a column, so match text with `upper(col) = 'X'` or "
            "`upper(col) like '%X%'`, and group by `upper(col)`."
        ),
        (
            "- Dates: compare `calendar_date` columns with ISO literals, e.g. "
            "`date_col between '2026-10-01' and '2026-10-31T23:59:59'`. Compute relative dates "
            '("last 7 days") yourself and pass literals.'
        ),
        (
            "- Count rows with `$select=count(*)`. Aggregates: `count`, `sum`, `avg`, `min`, `max`; "
            "`date_trunc_ym(col)` for month buckets."
        ),
        (
            '- Errors: HTTP 400 with `{"errorCode": "query.soql.no-such-column", ...}` for a bad '
            "field name; use the field names (not display names) from the column tables below."
        ),
        "- Geo: `within_circle(location, lat, lon, meters)` works on `point` columns.",
        "",
        "## Endpoint index",
        "",
        (
            "Queryable assets (datasets and filtered views). Rows were counted and each endpoint was "
            f"called with `$limit=1` on {today}."
        ),
        "",
        "| # | Id | Name | Type | Parent | Rows | Cols | Data updated | Update frequency | Status |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for number, a in enumerate(queryable, 1):
        rows = f"{a.rows:,}" if a.rows is not None else "?"
        parents = ", ".join(f"`{p}`" for p in a.parents)
        lines.append(
            f"| {number} | [`{a.id}`](#{a.id}) | {_cell(a.name)} | {a.type} | {parents} | {rows} | "
            f"{len(a.columns)} | {a.data_updated} | {_cell(a.update_frequency)} | {a.status} |"
        )
    if visuals:
        lines += [
            "",
            "Maps and charts (no data endpoint; query the parent):",
            "",
            "| Id | Name | Type | Built on | Updated |",
            "|---|---|---|---|---|",
        ]
        for a in visuals:
            lines.append(
                f"| `{a.id}` | {_cell(a.name)} | {a.type} | {parent_names(a) or 'unknown'} | "
                f"{a.meta_updated} |"
            )
        lines += ["", "Map/chart topics and tags:", ""]
        for a in visuals:
            lines.append(
                f"- `{a.id}`: Category: {_cell(a.topics) or 'none'}; Tags: {_tags(a.tags)}"
            )
    lines += ["", "## Datasets and filtered views", ""]
    for a in queryable:
        rows = f"{a.rows:,}" if a.rows is not None else "unknown"
        lines += [
            f"### {a.id}",
            "",
            f"**{a.name}** ({a.type})",
            "",
            f"- Endpoint: `GET {_DOMAIN}/resource/{a.id}.json`",
            f"- Metadata: `GET {_DOMAIN}/api/views/{a.id}.json`; page: {_DOMAIN}/d/{a.id}",
            f"- Topics: Category: {_cell(a.topics) or 'none'}",
            f"- Tags: {_tags(a.tags)}",
            f"- Rows: {rows}. Data updated: {a.data_updated}. Probe status: {a.status}.",
        ]
        if a.update_frequency:
            lines.append(f"- Update frequency: {a.update_frequency}.")
        if a.parents:
            lines.append(f"- Built on: {parent_names(a)}.")
        if a.view_filter:
            lines.append(f"- View condition (SoQL, applied server-side): `{a.view_filter}`")
        if a.attribution:
            lines.append(f"- Source: {a.attribution}")
        if a.description:
            lines.append(f"- Description: {_cell(a.description, 600)}")
        if a.extra_fields:
            extra = ", ".join(f"`{f}`" for f in a.extra_fields)
            lines.append(f"- Also returned by the API (not in the column list): {extra}")
        lines += [
            _sample_line(a),
            "",
            "| Field name | Display name | Type | Description |",
            "|---|---|---|---|",
        ]
        for c in a.columns:
            lines.append(
                f"| `{c.get('fieldName')}` | {_cell(c.get('name'))} | {c.get('dataTypeName', '')} | "
                f"{_cell(c.get('description'), 240)} |"
            )
        lines.append("")
    if category.tips:
        lines += ["## Usage tips", "", category.tips, ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    """Rebuild the skills named in ``argv`` (all topics if empty); return the exit code."""
    unknown = [name for name in argv if name not in _CATEGORIES]
    if unknown:
        print(f"unknown skill dir(s) {unknown}; known: {sorted(_CATEGORIES)}", file=sys.stderr)
        return 2
    api = _Api()
    for skill_dir in argv or list(_CATEGORIES):
        category = _CATEGORIES[skill_dir]
        print(f"== {category.title}", flush=True)
        assets, names, excluded = _collect(api, category)
        target = _SKILLS_DIR / skill_dir / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_render(category, assets, names, excluded), encoding="utf-8")
        failed = [a.id for a in assets if a.type in _QUERYABLE and a.status != 200]
        print(
            f"wrote {target.relative_to(_PACKAGE_DIR)}; excluded: {dict(excluded)}; "
            f"failed probes: {failed}",
            flush=True,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
