"""Generate one SKILL.md per openFDA drug and food endpoint (api.fda.gov).

Run from the project root:
``uv run python -m servers.fda.build_skills [folder ...]``, e.g.
``uv run python -m servers.fda.build_skills food_adverse_events``. With no arguments every
endpoint in ``_ENDPOINTS`` is rebuilt. Needs network access to api.fda.gov and open.fda.gov.

1. ``https://api.fda.gov/download.json`` (fetched once) gives each endpoint's bulk export date
   and record total.
2. The endpoint's field definitions (``https://open.fda.gov/fields/<name>.yaml``) are walked
   into a dotted-path field table: type, ``.exact`` flag, description and possible values.
3. The endpoint is probed with ``limit=1``. Its ``meta.results.total`` and
   ``meta.last_updated`` are recorded, plus the dotted field names of the sample record. The
   values are discarded. Names the field definitions don't list are recorded as extras.
4. Each hand-written example query is run and must return HTTP 200 with at least one result;
   only its status and total (or number of count terms) are recorded.
5. ``skills/<folder>/SKILL.md`` is written. If any fetch fails after retries, or an example
   returns no results, the run aborts before writing that endpoint's skill.

HTTP follows the rules in :mod:`servers.fda.api` (bounded exponential backoff on 429/5xx and
transport errors; 404 "No matches found!" means empty). The optional ``OPENFDA_API_KEY`` from
``.env`` is sent as the Basic-auth username to api.fda.gov only, and is never logged or written.

The hand-written parts of each skill (front-matter description, overview bullets, usage tips
and example queries) live in ``_ENDPOINTS`` below; edit them there, not in the generated file.
"""

from __future__ import annotations

import logging
import re
import ssl
import sys
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any

import httpx
import truststore
import yaml

from config import get_openfda_settings
from servers.fda import api

logger = logging.getLogger(__name__)

_PACKAGE_DIR = Path(__file__).resolve().parent
_SKILLS_DIR = _PACKAGE_DIR / "skills"
_API = "https://api.fda.gov"
_FIELDS_URL = "https://open.fda.gov/fields/{name}.yaml"
_MANIFEST_URL = f"{_API}/download.json"
_DOCS_URL = "https://open.fda.gov/apis/{id}/"
_REQUEST_INTERVAL = 0.25  # openFDA allows 240 requests per minute
_TIMEOUT_SECONDS = 60.0
_DESCRIPTION_LIMIT = 240
_SCALAR_TYPES = {
    "string": "string",
    "number": "number",
    "integer": "number",
    "float": "number",
    "boolean": "boolean",
}


@dataclass(frozen=True, slots=True)
class Example:
    """One example query run against the live API while generating the skill."""

    comment: str
    search: str | None = None
    count: str | None = None
    limit: int | None = None
    sort: str | None = None

    def params(self) -> dict[str, str | int]:
        """Return the query parameters, with ``limit=1`` for record queries without a limit."""
        params: dict[str, str | int] = {}
        if self.search:
            params["search"] = self.search
        if self.count:
            params["count"] = self.count
        if self.sort:
            params["sort"] = self.sort
        if self.limit is not None:
            params["limit"] = self.limit
        elif not self.count:
            params["limit"] = 1
        return params


@dataclass(frozen=True, slots=True)
class Endpoint:
    """Hand-written parts of one endpoint skill."""

    id: str  # e.g. "drug/event"
    yaml_name: str  # e.g. "drugevent"
    title: str
    skill_name: str
    category: str  # "drug" or "food"
    description: str
    overview: str
    tips: str
    examples: tuple[Example, ...]


@dataclass(frozen=True, slots=True)
class FieldDef:
    """One field from the endpoint's field definitions YAML."""

    path: str
    type: str
    exact: bool
    description: str
    possible_values: str


@dataclass(frozen=True, slots=True)
class ExampleResult:
    """The status and size of one example query's result (no values)."""

    example: Example
    status: int
    size: int  # total records, or number of count terms


@dataclass(frozen=True, slots=True)
class Collected:
    """Everything fetched for one endpoint."""

    fields: list[FieldDef]
    total: int
    last_updated: str
    export_date: str
    status: int
    sample_fields: list[str]
    extra_fields: list[str]
    examples: list[ExampleResult]


_ENDPOINTS: dict[str, Endpoint] = {
    "drug_adverse_events": Endpoint(
        id="drug/event",
        yaml_name="drugevent",
        title="Drug adverse events (FAERS)",
        skill_name="fda-drug-adverse-events",
        category="drug",
        description=(
            "Query openFDA drug adverse event reports (FAERS, api.fda.gov/drug/event). Use it "
            "for side effects and reactions reported for a drug, serious outcomes such as "
            "death or hospitalization, reports by patient age or sex, and counts of reports by "
            "drug, reaction, country or date since 2004."
        ),
        overview="""\
- Coverage: reports received from 2004 on (`receivedate`), plus 387 older ones back to 1986. With over 21 million reports, aggregate with `count` instead of paging (`skip` stops at 25,000).""",
        tips="""\
- Pick the field by question:
  - Drug in the report: `patient.drug.medicinalproduct` (as reported), or the harmonized `patient.drug.openfda.brand_name` / `generic_name` / `substance_name`. The `openfda` fields are missing on about 2.2 million reports, so search `medicinalproduct` too when completeness matters.
  - Reactions: `patient.reaction.reactionmeddrapt` (MedDRA preferred terms). Its `.exact` values are uppercase (`DRUG INEFFECTIVE`, `NAUSEA`).
  - Seriousness: `serious` is `1` (serious) or `2` (not). The `seriousness*` flags (`seriousnessdeath`, `seriousnesshospitalization`, ...) are documented as `1` or absent, but the data also holds `2`, so search `seriousnessdeath:1`, not `_exists_:seriousnessdeath`.
  - Patient: `patient.patientsex` is `0` unknown, `1` male, `2` female; `patient.patientonsetage` with `patient.patientonsetageunit`.
  - Drug role: `patient.drug.drugcharacterization` is `1` suspect, `2` concomitant, `3` interacting.
  - Country where the event occurred: `occurcountry.exact` (2-letter codes, `US` first).
- Brand names in `patient.drug.openfda.brand_name.exact` are uppercase: `.exact:"LIPITOR"` works and `.exact:"Lipitor"` returns no matches, while plain `patient.drug.openfda.brand_name:"lipitor"` matches 248,656 reports.
- `count=receivedate` returns daily `time` buckets (`YYYYMMDD`); narrow it with a `receivedate:[A TO B]` search.
- A report says a reaction happened while a drug was taken. It does not show the drug caused it, and counts reflect reporting, not incidence.""",
        examples=(
            Example(
                "Top reactions reported for Lipitor",
                search='patient.drug.openfda.brand_name.exact:"LIPITOR"',
                count="patient.reaction.reactionmeddrapt.exact",
                limit=5,
            ),
            Example(
                "Serious reports with a death outcome received in 2025",
                search="serious:1 AND seriousnessdeath:1 AND receivedate:[20250101 TO 20251231]",
            ),
            Example(
                "Reports for Ozempic by patient sex",
                search='patient.drug.medicinalproduct:"OZEMPIC"',
                count="patient.patientsex",
            ),
        ),
    ),
    "drug_labeling": Endpoint(
        id="drug/label",
        yaml_name="druglabel",
        title="Drug labeling (SPL)",
        skill_name="fda-drug-labeling",
        category="drug",
        description=(
            "Query openFDA drug labeling (structured product labels, api.fda.gov/drug/label). "
            "Use it for the text of prescription and OTC drug labels, such as indications, "
            "dosage, boxed warnings, contraindications, adverse reactions, drug interactions "
            "and active ingredients, looked up by brand or generic name."
        ),
        overview="""\
- Records are large: in a sample of 20 labels, one record was 1.6 KB to 352 KB of JSON. Always pass `fields` (and a small `limit`) to fda_get_dataset.""",
        tips="""\
- Pick the field by question:
  - Find the label: `openfda.brand_name`, `openfda.generic_name`, `openfda.substance_name`, `openfda.manufacturer_name`, `openfda.product_ndc`.
  - Label sections (arrays of text): `indications_and_usage`, `dosage_and_administration`, `boxed_warning`, `warnings` / `warnings_and_cautions`, `contraindications`, `adverse_reactions`, `drug_interactions`, `pregnancy`, `active_ingredient`, `inactive_ingredient`, `purpose` (OTC). Most sections also have a `<section>_table` field for the tables in that section.
  - Version: `effective_time` (`YYYYMMDD`), `set_id`, `version`; sort with `sort=effective_time:desc` for the newest labels.
- 197 fields, nearly all of them label sections. Test whether a section exists with `_exists_:<section>`, e.g. `_exists_:boxed_warning` (33,440 labels).
- One product has many labels (one per labeler and repackager): `openfda.brand_name:"tylenol"` matches 112. Its `.exact` values keep the label's casing (`Lipitor`, `TYLENOL Extra Strength`, `Tylenol Extra Strength`), so search the plain field and count `openfda.brand_name.exact` to see the variants.
- Label sections are text, so search words in them (`boxed_warning:"liver"`) but don't `count` them.""",
        examples=(
            Example("Labels for ibuprofen", search='openfda.generic_name:"ibuprofen"'),
            Example("Labels for Tylenol", search='openfda.brand_name:"tylenol"'),
            Example(
                "Routes of administration of labels with a boxed warning",
                search="_exists_:boxed_warning",
                count="openfda.route.exact",
                limit=5,
            ),
        ),
    ),
    "drug_ndc": Endpoint(
        id="drug/ndc",
        yaml_name="drugndc",
        title="National Drug Code directory (NDC)",
        skill_name="fda-drug-ndc",
        category="drug",
        description=(
            "Query the openFDA National Drug Code directory (api.fda.gov/drug/ndc). Use it to "
            "look up drug products and packages by NDC, brand or generic name, labeler, dosage "
            "form, route, active ingredients and strengths, and marketing category and dates."
        ),
        overview="",
        tips="""\
- Pick the field by question:
  - Look up a product: `product_ndc` (labeler-product, e.g. `0573-0133` for an Advil product), `brand_name`, `generic_name`, `labeler_name` (returned by the API but not in the field definitions; `labeler_name.exact` counts work).
  - Packages: `packaging.package_ndc`, `packaging.description`.
  - Ingredients and form: `active_ingredients.name`, `active_ingredients.strength`, `dosage_form`, `route`.
  - Regulatory: `marketing_category` (`ANDA`, `OTC MONOGRAPH DRUG`, `NDA`, `BLA`, `UNAPPROVED HOMEOPATHIC`, ...), `product_type` (`HUMAN PRESCRIPTION DRUG`, `HUMAN OTC DRUG`, ...), `dea_schedule`, `marketing_start_date`.
- Count `marketing_category` without `.exact` (`.exact` returns "Nothing to count"); `product_type.exact` and `dosage_form.exact` work.
- `marketing_start_date` sorted ascending starts at `19000101`, so ignore implausibly old dates.""",
        examples=(
            Example("Products named Advil", search='brand_name:"Advil"'),
            Example(
                "Dosage forms of metformin products",
                search='generic_name:"metformin"',
                count="dosage_form.exact",
                limit=5,
            ),
            Example(
                "Manufacturers with the most products first marketed in 2025",
                search="marketing_start_date:[20250101 TO 20251231]",
                count="openfda.manufacturer_name.exact",
                limit=5,
            ),
        ),
    ),
    "drug_recalls": Endpoint(
        id="drug/enforcement",
        yaml_name="drugenforcement",
        title="Drug recalls (enforcement reports)",
        skill_name="fda-drug-recalls",
        category="drug",
        description=(
            "Query openFDA drug recall enforcement reports (api.fda.gov/drug/enforcement). Use "
            "it for drug recalls since 2012 by recalling firm, product, reason, classification "
            "(Class I, II or III), status, distribution and report date."
        ),
        overview="""\
- Coverage: `report_date` starts on 2012-06-20. Records name the recalling firm with its address, and some carry contact phone numbers or emails in text fields.""",
        tips="""\
- Pick the field by question:
  - Severity: `classification` is `Class I` (most serious), `Class II` or `Class III`. Search it plainly (`classification:"Class I"`) or exactly (`classification.exact:"Class I"`); `.exact:"class i"` returns no matches.
  - Why: `reason_for_recall` (free text; search words such as `"nitrosamine"`, `"sterility"`).
  - Who and what: `recalling_firm`, `product_description`, `openfda.brand_name` / `generic_name` (present only for some recalls), `distribution_pattern`.
  - Progress: `status` is `Terminated`, `Ongoing` or `Completed` (count `status.exact`); dates `recall_initiation_date`, `report_date`, `termination_date`.
- `reason_for_recall` and `product_description` are text fields: counting them returns HTTP 500 "Text fields are not optimised". Count `recalling_firm.exact` or `classification.exact` instead.
- `count=report_date` returns every report date in the result (744 dates for all records) regardless of `limit`; narrow it with a `report_date:[A TO B]` search.""",
        examples=(
            Example(
                "Class I drug recalls reported in 2025",
                search='classification:"Class I" AND report_date:[20250101 TO 20251231]',
            ),
            Example(
                "Firms with the most nitrosamine recalls",
                search='reason_for_recall:"nitrosamine"',
                count="recalling_firm.exact",
                limit=5,
            ),
            Example("Recall reports per report date", count="report_date", limit=5),
        ),
    ),
    "drugs_fda": Endpoint(
        id="drug/drugsfda",
        yaml_name="drugsfda",
        title="Drugs@FDA approvals",
        skill_name="fda-drugs-fda",
        category="drug",
        description=(
            "Query openFDA Drugs@FDA (api.fda.gov/drug/drugsfda). Use it for FDA-approved drug "
            "applications (NDA, ANDA, BLA) with their sponsor, products, marketing status, "
            "and submission history such as original approvals, supplements and approval dates."
        ),
        overview="",
        tips="""\
- Pick the field by question:
  - Application: `application_number` (prefix `NDA`, `ANDA` or `BLA`), `sponsor_name`.
  - Products: `products.brand_name`, `products.active_ingredients.name`, `products.dosage_form`, `products.route`, `products.marketing_status` (`Prescription`, `Over-the-counter`, `Discontinued`, `None (Tentative Approval)`), `products.te_code`.
  - History: `submissions.submission_type` (`ORIG` original, `SUPPL` supplement), `submissions.submission_status` (`AP` approved, `TA` tentative approval), `submissions.submission_status_date`, `submissions.application_docs.url` (letters, labels, reviews).
- Count `sponsor_name` and `submissions.submission_type` without `.exact`: although the field definitions mark `sponsor_name` as exact, `.exact` returns "Nothing to count".
- `submissions` is a list, so `submissions.submission_type:"ORIG" AND submissions.submission_status_date:[...]` can match the two terms in different submissions of one application. Check the returned submissions when the pairing matters.""",
        examples=(
            Example("Applications for Lipitor", search='openfda.brand_name:"lipitor"'),
            Example(
                "Sponsors with the most original submissions dated 2025",
                search=(
                    'submissions.submission_type:"ORIG" AND '
                    "submissions.submission_status_date:[20250101 TO 20251231]"
                ),
                count="sponsor_name",
                limit=5,
            ),
            Example("Products by marketing status", count="products.marketing_status"),
        ),
    ),
    "drug_shortages": Endpoint(
        id="drug/shortages",
        yaml_name="drugshortages",
        title="Drug shortages",
        skill_name="fda-drug-shortages",
        category="drug",
        description=(
            "Query openFDA drug shortages (api.fda.gov/drug/shortages). Use it for current, "
            "resolved and to-be-discontinued drug shortages by generic name, company, "
            "therapeutic category, dosage form, shortage reason and availability."
        ),
        overview="""\
- One record per product presentation (package) in a shortage, not per drug: `generic_name:"lidocaine"` returns many records. Records include the company's `contact_info`, usually a phone number.""",
        tips="""\
- Pick the field by question:
  - Drug: `generic_name`, `proprietary_name`, `openfda.brand_name`, `presentation`, `package_ndc`, `company_name`.
  - State: `status` is `Current`, `To Be Discontinued` or `Resolved`; `availability`, `shortage_reason`, `resolved_note`.
  - Grouping: `therapeutic_category` (`Anesthesia`, `Pediatric`, `Psychiatry`, ...).
- **Dates are `MM/DD/YYYY` strings** (`update_date`, `initial_posting_date`, `change_date`, `discontinued_date`). Search one day as `update_date:"10/06/2026"`, and ranges as `update_date:[10/01/2026 TO 10/31/2026]` or `update_date:[2026-10-01 TO 2026-10-31]`. The `YYYYMMDD` form used by the other endpoints returns no matches here. `count=update_date` still returns `YYYYMMDD` time buckets.
- Count `therapeutic_category` and `status` without `.exact` (`therapeutic_category.exact` returns "Nothing to count").""",
        examples=(
            Example("Shortages by status", count="status"),
            Example(
                "Therapeutic categories of current shortages",
                search='status:"Current"',
                count="therapeutic_category",
                limit=5,
            ),
            Example("Shortage records for lidocaine", search='generic_name:"lidocaine"'),
        ),
    ),
    "drug_orange_book": Endpoint(
        id="drug/orangebook",
        yaml_name="drugorangebook",
        title="Orange Book (approved drug products with therapeutic equivalence evaluations)",
        skill_name="fda-drug-orange-book",
        category="drug",
        description=(
            "Query the openFDA Orange Book (api.fda.gov/drug/orangebook). Use it for approved "
            "drug products with therapeutic equivalence (TE) codes, reference listed drugs, "
            "and the patents and exclusivities that protect an application, with expiration "
            "dates."
        ),
        overview="",
        tips="""\
- Pick the field by question:
  - Product: `products.brand_name` (uppercase, e.g. `LIPITOR`), `products.active_ingredients.name`, `products.dosage_form`, `products.route`, `products.application_number`, `products.application_type` (`A` ANDA, `N` NDA).
  - Equivalence: `products.therapeutic_equivalence_codes` (TE codes such as `AB`), `products.reference_listed_drug`, `products.reference_standard`.
  - Protection: `patents.patent_number`, `patents.expiration_date`, `patents.patent_use_code`, `exclusivity.exclusivity_code`, `exclusivity.exclusivity_expiration_date`.
- `products.marketing_status` is returned by the API but is not in the field definitions.
- `patents` and `exclusivity` are lists: a date range on `patents.expiration_date` matches applications with at least one patent in the range.""",
        examples=(
            Example("Orange Book entries for Lipitor", search='products.brand_name:"LIPITOR"'),
            Example("Products by application type", count="products.application_type"),
            Example(
                "Applications with a patent expiring in 2027",
                search="patents.expiration_date:[20270101 TO 20271231]",
            ),
        ),
    ),
    "food_recalls": Endpoint(
        id="food/enforcement",
        yaml_name="foodenforcement",
        title="Food recalls (enforcement reports)",
        skill_name="fda-food-recalls",
        category="food",
        description=(
            "Query openFDA food recall enforcement reports (api.fda.gov/food/enforcement). Use "
            "it for food and dietary supplement recalls since 2012 by firm, product, reason "
            "(such as Listeria, Salmonella or undeclared allergens), classification, state and "
            "report date."
        ),
        overview="""\
- Coverage: `report_date` starts on 2012-06-20. Records name the recalling firm with its address.""",
        tips="""\
- Pick the field by question:
  - Severity: `classification` (`Class I`, `Class II`, `Class III`, `Not Yet Classified`; count `classification.exact`).
  - Why: `reason_for_recall` (free text; search words such as `"listeria"`, `"salmonella"`, `"undeclared"`).
  - Who and what: `recalling_firm`, `product_description`, `state` and `city` of the firm, `distribution_pattern`.
  - Progress: `status` (`Terminated`, `Ongoing`, `Completed`), `recall_initiation_date`, `report_date`, `termination_date`.
- `state` needs `.exact` to count: `count=state` returns HTTP 500 "Text fields are not optimised", `count=state.exact` returns 2-letter codes (`CA`, `TX`, `IL`, ...). It is the firm's state, not where the product was sold; see `distribution_pattern` for that.
- The `openfda` fields are defined but empty for food recalls.""",
        examples=(
            Example(
                "Listeria recalls reported in 2025",
                search='reason_for_recall:"listeria" AND report_date:[20250101 TO 20251231]',
            ),
            Example(
                "States of the recalling firms in 2025",
                search="report_date:[20250101 TO 20251231]",
                count="state.exact",
                limit=5,
            ),
            Example("Recalls by classification", count="classification.exact"),
        ),
    ),
    "food_adverse_events": Endpoint(
        id="food/event",
        yaml_name="foodevent",
        title="Food, dietary supplement and cosmetic adverse events (CAERS)",
        skill_name="fda-food-adverse-events",
        category="food",
        description=(
            "Query openFDA food adverse event reports (CAERS, api.fda.gov/food/event). Use it "
            "for reactions and outcomes reported for foods, dietary supplements and cosmetics, "
            "by product, industry, consumer age and gender, and report date."
        ),
        overview="""\
- Freshness: `meta.last_updated` is older than the drug endpoints (see the snapshot line). Reports go back to 1999 (`date_created`).""",
        tips="""\
- Pick the field by question:
  - Product: `products.name_brand`, `products.industry_name` (e.g. `Cosmetics`, `Vit/Min/Prot/Unconv Diet(Human/Animal)` for dietary supplements), `products.role` (`SUSPECT` or `CONCOMITANT`).
  - Effect: `reactions` (MedDRA terms), `outcomes` (`Hospitalization`, `Death`, `Visited Emergency Room`, ...).
  - Consumer: `consumer.age` with `consumer.age_unit`, `consumer.gender`.
- Cosmetics are included: they are the second-largest industry (52,219 reports), after dietary supplements (54,906).
- `reactions.exact` has case variants of the same term (`Ovarian cancer` / `OVARIAN CANCER`, `Diarrhoea` / `DIARRHOEA`); add up the variants when ranking reactions.
- `products.name_brand` is often `EXEMPTION 4` (39,396 reports): the brand was withheld under FOIA exemption 4 (confidential business information).""",
        examples=(
            Example("Reports by product industry", count="products.industry_name.exact", limit=5),
            Example(
                "Top reactions reported for cosmetics",
                search='products.industry_name:"Cosmetics"',
                count="reactions.exact",
                limit=5,
            ),
            Example("Reports by outcome", count="outcomes.exact"),
            Example("Reports created in 2025", search="date_created:[20250101 TO 20251231]"),
        ),
    ),
}


class _Api:
    """Throttled, retrying GET client for api.fda.gov and open.fda.gov."""

    def __init__(self) -> None:
        key = get_openfda_settings().openfda_api_key
        self._auth = api.basic_auth(key.get_secret_value() if key else None)
        self._client = httpx.Client(
            timeout=_TIMEOUT_SECONDS,
            verify=truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT),
        )
        self._last = 0.0

    def get(
        self, url: str, params: dict[str, str | int] | None = None
    ) -> tuple[api.Outcome, httpx.Response]:
        """GET ``url`` with retries; return the final outcome and response.

        Raises:
            RuntimeError: If the request still fails or is retryable after
                :data:`servers.fda.api.MAX_ATTEMPTS` attempts, or returns an ``error``.
        """
        auth = self._auth if url.startswith(_API) else None
        problem = ""
        error: httpx.TransportError | None = None
        for attempt in range(1, api.MAX_ATTEMPTS + 1):
            wait = self._last + _REQUEST_INTERVAL - time.monotonic()
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
            retry_after: str | None = None
            try:
                response = self._client.get(url, params=params, auth=auth)
            except httpx.TransportError as exc:
                problem, error = f"{type(exc).__name__}: {exc}", exc
            else:
                outcome = api.classify(response.status_code, _json_or_none(response))
                if outcome.kind in ("ok", "empty"):
                    return outcome, response
                problem, error = outcome.message, None
                if outcome.kind == "error":
                    break
                retry_after = response.headers.get("Retry-After")
            if attempt < api.MAX_ATTEMPTS:
                delay = api.retry_delay(attempt, retry_after)
                logger.warning(
                    "GET %s: %s, retry %d/%d in %.0f s",
                    url,
                    problem,
                    attempt,
                    api.MAX_ATTEMPTS - 1,
                    delay,
                )
                time.sleep(delay)
        raise RuntimeError(
            f"GET {url} {params or {}} failed: {problem}; aborting so no partial skill is written"
        ) from error


def _one_line(text: object) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _cell(text: object, limit: int = 0) -> str:
    """Make ``text`` safe for one markdown table cell, optionally truncated."""
    value = _one_line(text).replace("|", "\\|")
    if limit and len(value) > limit:
        value = value[: limit - 1].rstrip() + "…"
    return value


def _json_or_none(response: httpx.Response) -> Any:
    """Return the parsed JSON body, or ``None`` if it is not JSON."""
    if "json" not in response.headers.get("content-type", ""):
        return None
    try:
        return response.json()
    except ValueError:
        logger.warning("Response from %s is not valid JSON", response.url)
        return None


def _type_name(node: dict[str, Any]) -> str:
    """Return ``string``, ``number``, ``boolean`` or ``date`` for a scalar field node."""
    if node.get("format") == "date":
        return "date"
    raw = node.get("type")
    return _SCALAR_TYPES.get(raw, "string") if isinstance(raw, str) else "string"


def _possible_values(value: object) -> str:
    """Render a YAML ``possible_values`` entry for a table cell ("" if none)."""
    if not isinstance(value, dict):
        return ""
    kind, content = value.get("type"), value.get("value")
    if kind == "one_of" and isinstance(content, dict):
        text = "; ".join(f"`{k}`: {_one_line(v)}" for k, v in content.items())
        return _cell(text, _DESCRIPTION_LIMIT)
    if kind == "reference" and isinstance(content, dict):
        name, link = _one_line(content.get("name")), _one_line(content.get("link"))
        return _cell(f"see {name} ({link})" if link else f"see {name}")
    return ""


def _description(node: dict[str, Any]) -> str:
    """Return the one-line description of a node ("" for missing or ``None``)."""
    text = _one_line(node.get("description"))
    return "" if text == "None" else text


def _is_schema(node: dict[str, Any]) -> bool:
    """Return whether ``node`` is a field schema (has a string ``type`` or ``properties``)."""
    return isinstance(node.get("type"), str) or isinstance(node.get("properties"), dict)


def _scalar(path: str, node: dict[str, Any], array: bool, parent: dict[str, Any]) -> FieldDef:
    """Build the field for a scalar (or array-of-scalars) node."""
    return FieldDef(
        path=path,
        type=_type_name(node) + ("[]" if array else ""),
        exact=bool(node.get("is_exact") or parent.get("is_exact")),
        description=_description(node) or _description(parent),
        possible_values=_possible_values(node.get("possible_values"))
        or _possible_values(parent.get("possible_values")),
    )


def _walk(properties: dict[str, Any], prefix: str, out: list[FieldDef]) -> None:
    """Append a :class:`FieldDef` for every leaf under ``properties`` to ``out``.

    Skips the top-level ``meta`` subtree and non-dict nodes (e.g. a stray ``type: object``),
    and handles array ``items`` with or without a ``properties`` wrapper.
    """
    for key, node in properties.items():
        if not isinstance(node, dict) or (not prefix and key == "meta"):
            continue
        path = f"{prefix}{key}"
        if isinstance(node.get("properties"), dict):
            _walk(node["properties"], f"{path}.", out)
        elif node.get("type") == "array" and isinstance(node.get("items"), dict):
            items: dict[str, Any] = node["items"]
            if isinstance(items.get("properties"), dict):
                _walk(items["properties"], f"{path}.", out)
            elif _is_schema(items):
                out.append(_scalar(path, items, array=True, parent=node))
            else:  # the items mapping is itself the property map
                _walk(items, f"{path}.", out)
        else:
            out.append(_scalar(path, node, array=False, parent={}))


def _flatten_keys(value: Any, prefix: str = "") -> list[str]:
    """Return the dotted leaf key paths of a record (values are not kept)."""
    if isinstance(value, list):
        return list(dict.fromkeys(k for item in value for k in _flatten_keys(item, prefix)))
    if isinstance(value, dict) and value:
        keys: list[str] = []
        for key, child in value.items():
            keys.extend(_flatten_keys(child, f"{prefix}{key}."))
        return list(dict.fromkeys(keys))
    return [prefix.rstrip(".")] if prefix else []


def _extras(sample: list[str], fields: list[FieldDef]) -> list[str]:
    """Return sample keys no field equals or is a child of (``key + "."`` prefix)."""
    paths = [f.path for f in fields]
    known = set(paths)
    return [
        key
        for key in sample
        if key not in known and not any(p.startswith(f"{key}.") for p in paths)
    ]


def _meta(payload: Any) -> tuple[int, str]:
    """Return ``meta.results.total`` and ``meta.last_updated`` of a records response."""
    meta = (payload.get("meta") or {}) if isinstance(payload, dict) else {}
    results = meta.get("results") or {}
    return int(results.get("total") or 0), str(meta.get("last_updated") or "")


def _collect(client: _Api, folder: str, endpoint: Endpoint, manifest: Any) -> Collected:
    """Fetch the field definitions, probe the endpoint and run its examples.

    Raises:
        RuntimeError: If a fetch fails or an example returns no results.
    """
    category, name = endpoint.id.split("/")
    entry = manifest.get("results", {}).get(category, {}).get(name, {})

    yaml_url = _FIELDS_URL.format(name=endpoint.yaml_name)
    _, response = client.get(yaml_url)
    definitions = yaml.safe_load(response.text)
    if not isinstance(definitions, dict) or not isinstance(definitions.get("properties"), dict):
        raise TypeError(f"{yaml_url} has no top-level properties mapping; aborting {folder}")
    fields: list[FieldDef] = []
    _walk(definitions["properties"], "", fields)
    fields.sort(key=lambda f: f.path)

    url = f"{_API}/{endpoint.id}.json"
    outcome, response = client.get(url, {"limit": 1})
    if outcome.kind != "ok":
        raise RuntimeError(f"GET {url}?limit=1 returned no records ({outcome.message})")
    payload = response.json()
    total, last_updated = _meta(payload)
    records = payload.get("results") or []
    sample = _flatten_keys(records[0]) if records else []

    results: list[ExampleResult] = []
    for example in endpoint.examples:
        outcome, response = client.get(url, example.params())
        body = response.json() if outcome.kind == "ok" else {}
        rows = body.get("results") or []
        if outcome.kind != "ok" or not rows:
            raise RuntimeError(
                f"{folder} example '{example.comment}' returned no results "
                f"({outcome.message or 'empty'}); fix it in _ENDPOINTS"
            )
        size = len(rows) if example.count else _meta(body)[0]
        results.append(ExampleResult(example, response.status_code, size))

    return Collected(
        fields=fields,
        total=total,
        last_updated=last_updated,
        export_date=str(entry.get("export_date") or "unknown"),
        status=200,
        sample_fields=sample,
        extra_fields=_extras(sample, fields),
        examples=results,
    )


def _example_lines(endpoint: Endpoint, results: list[ExampleResult]) -> list[str]:
    """Render the example queries block, with spaces shown as ``+`` (openFDA's convention)."""
    today = date.today().isoformat()
    lines = [f"- Example queries (run on {today}):", "", "  ```"]
    for result in results:
        query = "&".join(
            f"{key}={str(value).replace(' ', '+')}"
            for key, value in result.example.params().items()
        )
        unit = "terms" if result.example.count else "records"
        lines += [
            f"  # {result.example.comment} ({result.status}, {result.size:,} {unit})",
            f"  GET {_API}/{endpoint.id}.json?{query}",
        ]
    lines += ["  ```", ""]
    return lines


_QUERY_PARAMETERS = [
    "| Param | Meaning | Example |",
    "|---|---|---|",
    (
        "| `search` | Filter records: `field:term`, joined with `AND` / `OR` / `NOT`. Omit to "
        "match all records. | `search=serious:1+AND+receivedate:[20250101+TO+20251231]` |"
    ),
    (
        "| `count` | Count records per distinct value of one field instead of returning "
        'records. Returns `[{"term": ..., "count": n}]` (date fields: `{"time": ..., '
        '"count": n}`), most frequent first. | `count=patient.reaction.reactionmeddrapt.exact` |'
    ),
    (
        f"| `limit` | Records (or count terms) to return. Max {api.MAX_LIMIT}; default here "
        f"{api.DEFAULT_LIMIT} for records and {api.DEFAULT_COUNT_LIMIT} for count. `count` "
        "with `limit=1000` needs an API key. | `limit=100` |"
    ),
    (
        f"| `skip` | Records to skip, for paging. Max {api.MAX_SKIP}; not allowed with "
        "`count`. | `skip=100` |"
    ),
    "| `sort` | Sort records: `field:asc` or `field:desc`. | `sort=report_date:desc` |",
]

_SEARCH_NOTES = [
    "Search notes:",
    "",
    (
        '- `field:term` matches a word in the field; quote phrases: `field:"two words"`. '
        "Combine terms with `AND`, `OR` and `NOT`, and group them with parentheses."
    ),
    (
        "- Ranges: `field:[A TO B]` (inclusive). Dates are `YYYYMMDD` strings, e.g. "
        "`report_date:[20250101 TO 20251231]`."
    ),
    "- `_exists_:field` / `_missing_:field` match records where the field is present or absent.",
    (
        "- `field.exact` matches or counts the whole value, case-sensitively "
        '(`openfda.brand_name.exact:"TYLENOL"`). The plain field matches words '
        "case-insensitively. Count on `.exact` to get whole values instead of single words."
    ),
    (
        '- No hits returns HTTP 404 `NOT_FOUND` "No matches found!", which is an empty result, '
        "not an error. A misspelled field name returns the same 404, so check field names in "
        "the table."
    ),
    (
        "- HTTP 500 with `parse_exception` in the details is a search syntax error. "
        '"Text fields are not optimised" on a count means: count `<field>.exact` instead. '
        '"Nothing to count" on a `.exact` field can mean the field has no `.exact` variant; '
        "retry without `.exact`. The Exact column below is a guide, not a guarantee."
    ),
    (
        "- With `fda_get_dataset`, write spaces as spaces, not `+`; the tool encodes them. A "
        "literal `+` breaks the query."
    ),
]


_COMMON_TIPS = [
    (
        "- `.exact` is case-sensitive and matches the whole value. In drug/label, "
        '`openfda.brand_name.exact:"Tylenol"` returns no matches, while plain '
        '`openfda.brand_name:"tylenol"` returns 112 labels.'
    ),
    (
        '- A misspelled field name returns "No matches found!", the same as a search with no '
        "hits. fda_get_dataset adds a hint when a field is not in the table above."
    ),
    (
        "- Counting a date field returns every date in the result, whatever the `limit`. "
        "Narrow the search to a date range first."
    ),
    (
        "- Pass `fields` to fda_get_dataset to return only the paths you need, e.g. "
        '`fields=["openfda.brand_name", "boxed_warning"]`.'
    ),
]


def _render(endpoint: Endpoint, data: Collected) -> str:
    """Render the SKILL.md text of one endpoint."""
    today = date.today().isoformat()
    docs = _DOCS_URL.format(id=endpoint.id)
    yaml_url = _FIELDS_URL.format(name=endpoint.yaml_name)
    lines = [
        "---",
        f"name: {endpoint.skill_name}",
        f"description: {endpoint.description}",
        "---",
        "",
        f"# openFDA: {endpoint.title}",
        "",
        "## Overview",
        "",
        (
            f"- API: `{_API}` (openFDA, Elasticsearch-based REST API). Docs: {docs}. "
            f"Field definitions: {yaml_url}."
        ),
        (
            f"- Snapshot taken {today}: {data.total:,} records; data last updated "
            f"{data.last_updated} (`meta.last_updated`); bulk export date {data.export_date} "
            "(download.json)."
        ),
        "- Surface: read-only `GET`, JSON only. One endpoint; no per-record ids to look up.",
        (
            "- Auth: optional API key (env `OPENFDA_API_KEY`, sent as the Basic-auth username). "
            "Without a key: 240 requests/minute and 1,000/day per IP; with a key: 120,000/day. "
            "`count` with `limit=1000` needs a key."
        ),
        (
            "- Disclaimer: openFDA asks users not to base medical care decisions on it and to "
            "treat all results as unvalidated; FDA may limit API access under its terms. "
            "Terms: https://open.fda.gov/terms/. License: https://open.fda.gov/license/."
        ),
        (
            "- Sample record: one `limit=1` record was fetched to list the fields it returns; "
            "values were not stored."
        ),
    ]
    if endpoint.overview:
        lines.append(endpoint.overview)
    lines += [
        "",
        "## Query parameters",
        "",
        *_QUERY_PARAMETERS,
        "",
        *_SEARCH_NOTES,
        "",
        "## Endpoint index",
        "",
        "| Id | Name | Category | Records | Fields | Last updated |",
        "|---|---|---|---|---|---|",
        (
            f"| `{endpoint.id}` | {_cell(endpoint.title)} | {endpoint.category} | "
            f"{data.total:,} | {len(data.fields)} | {data.last_updated} |"
        ),
        "",
        "## Endpoint",
        "",
        f"### {endpoint.id}",
        "",
        f"**{endpoint.title}**",
        "",
        f"- Endpoint: `GET {_API}/{endpoint.id}.json`",
        (
            f"- Records: {data.total:,}. Last updated: {data.last_updated}. "
            f"Probe status: {data.status}."
        ),
    ]
    if data.sample_fields:
        sample = ", ".join(f"`{name}`" for name in data.sample_fields)
        lines.append(f"- Sample record fields (limit=1): {sample}")
    else:
        lines.append("- Sample record fields (limit=1): none (no records)")
    if data.extra_fields:
        extra = ", ".join(f"`{name}`" for name in data.extra_fields)
        lines.append(f"- Also returned by the API (not in the field definitions): {extra}")
    lines += _example_lines(endpoint, data.examples)
    lines += [
        "| Field | Type | Exact | Description | Possible values |",
        "|---|---|---|---|---|",
    ]
    for f in data.fields:
        lines.append(
            f"| `{f.path}` | {f.type} | {'yes' if f.exact else ''} | "
            f"{_cell(f.description, _DESCRIPTION_LIMIT)} | {f.possible_values} |"
        )
    lines.append("")
    lines += ["## Usage tips", ""]
    if endpoint.tips:
        lines.append(endpoint.tips)
    lines += [*_COMMON_TIPS, ""]
    return "\n".join(lines)


def main(argv: list[str]) -> int:
    """Rebuild the skills named in ``argv`` (all endpoints if empty); return the exit code."""
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    unknown = [name for name in argv if name not in _ENDPOINTS]
    if unknown:
        logger.error("unknown skill folder(s) %s; known: %s", unknown, sorted(_ENDPOINTS))
        return 2
    client = _Api()
    _, response = client.get(_MANIFEST_URL)
    manifest = response.json()
    for folder in argv or list(_ENDPOINTS):
        endpoint = _ENDPOINTS[folder]
        logger.info("== %s (%s)", endpoint.title, endpoint.id)
        data = _collect(client, folder, endpoint, manifest)
        target = _SKILLS_DIR / folder / "SKILL.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(_render(endpoint, data), encoding="utf-8")
        logger.info(
            "wrote %s: %s records, %d fields, %d extra, examples ok %d/%d",
            target.relative_to(_PACKAGE_DIR).as_posix(),
            f"{data.total:,}",
            len(data.fields),
            len(data.extra_fields),
            len(data.examples),
            len(endpoint.examples),
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
