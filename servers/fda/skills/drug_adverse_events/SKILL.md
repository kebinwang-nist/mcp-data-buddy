---
name: fda-drug-adverse-events
description: Query openFDA drug adverse event reports (FAERS, api.fda.gov/drug/event). Use it for side effects and reactions reported for a drug, serious outcomes such as death or hospitalization, reports by patient age or sex, and counts of reports by drug, reaction, country or date since 2004.
---

# openFDA: Drug adverse events (FAERS)

## Overview

- API: `https://api.fda.gov` (openFDA, Elasticsearch-based REST API). Docs: https://open.fda.gov/apis/drug/event/. Field definitions: https://open.fda.gov/fields/drugevent.yaml.
- Snapshot taken 2026-11-19: 21,054,159 records; data last updated 2026-10-28 (`meta.last_updated`); bulk export date 2026-11-18 (download.json).
- Surface: read-only `GET`, JSON only. One endpoint; no per-record ids to look up.
- Auth: optional API key (env `OPENFDA_API_KEY`, sent as the Basic-auth username). Without a key: 240 requests/minute and 1,000/day per IP; with a key: 120,000/day. `count` with `limit=1000` needs a key.
- Disclaimer: openFDA asks users not to base medical care decisions on it and to treat all results as unvalidated; FDA may limit API access under its terms. Terms: https://open.fda.gov/terms/. License: https://open.fda.gov/license/.
- Sample record: one `limit=1` record was fetched to list the fields it returns; values were not stored.
- Coverage: reports received from 2004 on (`receivedate`), plus 387 older ones back to 1986. With over 21 million reports, aggregate with `count` instead of paging (`skip` stops at 25,000).

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
| `drug/event` | Drug adverse events (FAERS) | drug | 21,054,159 | 87 | 2026-10-28 |

## Endpoint

### drug/event

**Drug adverse events (FAERS)**

- Endpoint: `GET https://api.fda.gov/drug/event.json`
- Records: 21,054,159. Last updated: 2026-10-28. Probe status: 200.
- Sample record fields (limit=1): `safetyreportid`, `transmissiondateformat`, `transmissiondate`, `serious`, `seriousnessdeath`, `receivedateformat`, `receivedate`, `receiptdateformat`, `receiptdate`, `fulfillexpeditecriteria`, `companynumb`, `primarysource.reportercountry`, `primarysource.qualification`, `sender.senderorganization`, `receiver`, `patient.patientonsetage`, `patient.patientonsetageunit`, `patient.patientsex`, `patient.patientdeath.patientdeathdateformat`, `patient.patientdeath.patientdeathdate`, `patient.reaction.reactionmeddrapt`, `patient.drug.drugcharacterization`, `patient.drug.medicinalproduct`, `patient.drug.drugauthorizationnumb`, `patient.drug.drugadministrationroute`, `patient.drug.drugindication`
- Example queries (run on 2026-11-19):

  ```
  # Top reactions reported for Lipitor (200, 5 terms)
  GET https://api.fda.gov/drug/event.json?search=patient.drug.openfda.brand_name.exact:"LIPITOR"&count=patient.reaction.reactionmeddrapt.exact&limit=5
  # Serious reports with a death outcome received in 2025 (200, 97,722 records)
  GET https://api.fda.gov/drug/event.json?search=serious:1+AND+seriousnessdeath:1+AND+receivedate:[20250101+TO+20251231]&limit=1
  # Reports for Ozempic by patient sex (200, 3 terms)
  GET https://api.fda.gov/drug/event.json?search=patient.drug.medicinalproduct:"OZEMPIC"&count=patient.patientsex
  ```

| Field | Type | Exact | Description | Possible values |
|---|---|---|---|---|
| `authoritynumb` | string | yes | Populated with the Regulatory Authority’s case report number, when available. |  |
| `companynumb` | string | yes | Identifier for the company providing the report. This is self-assigned. |  |
| `duplicate` | string |  | This value is `1` if earlier versions of this report were submitted to FDA. openFDA only shows the most recent version. |  |
| `fulfillexpeditecriteria` | string |  | Identifies expedited reports (those that were processed within 15 days). | `1`: True; `2`: |
| `occurcountry` | string | yes | The name of the country where the event occurred. | see Country codes (http://data.okfn.org/data/core/country-list) |
| `patient.drug.actiondrug` | string |  | Actions taken with the drug. | `1`: Drug withdrawn; `2`: Dose reduced; `3`: Dose increased; `4`: Dose not changed; `5`: Unknown; `6`: Not applicable |
| `patient.drug.activesubstance.activesubstancename` | string | yes | Product active ingredient, which may be different than other drug identifiers (when provided). |  |
| `patient.drug.drugadditional` | string |  | Dechallenge outcome information—whether the event abated after product use stopped or the dose was reduced. Only present when this was attempted and the data was provided. | `1`: Yes; `2`: No; `3`: Does not apply |
| `patient.drug.drugadministrationroute` | string | yes | The drug’s route of administration. | `001`: Auricular (otic); `002`: Buccal; `003`: Cutaneous; `004`: Dental; `005`: Endocervical; `006`: Endosinusial; `007`: Endotracheal; `008`: Epidural; `009`: Extra-amniotic; `010`: Hemodialysis; `011`: Intra corpus cavernosum; `012`: Int… |
| `patient.drug.drugauthorizationnumb` | string | yes | Drug authorization or application number (NDA or ANDA), if provided. |  |
| `patient.drug.drugbatchnumb` | string | yes | Drug product lot number, if provided. |  |
| `patient.drug.drugcharacterization` | string |  | Reported role of the drug in the adverse event report. These values are not validated by FDA. | `1`: Suspect (the drug was considered by the reporter to be the cause); `2`: Concomitant (the drug was reported as being taken along with the suspect drug); `3`: Interacting (the drug was considered by the reporter to have interacted with… |
| `patient.drug.drugcumulativedosagenumb` | string |  | The cumulative dose taken until the first reaction was experienced, if provided. |  |
| `patient.drug.drugcumulativedosageunit` | string |  | The unit for `drugcumulativedosagenumb`. | `001`: kg (kilograms); `002`: g (grams); `003`: mg (milligrams); `004`: µg (micrograms) |
| `patient.drug.drugdosageform` | string | yes | The drug’s dosage form. There is no standard, but values may include terms like `tablet` or `solution for injection`. |  |
| `patient.drug.drugdosagetext` | string | yes | Additional detail about the dosage taken. Frequently unknown, but occasionally including information like a brief textual description of the schedule of administration. |  |
| `patient.drug.drugenddate` | date |  | Date the patient stopped taking the drug. |  |
| `patient.drug.drugenddateformat` | string |  | Encoding format of the field `drugenddateformat`. Always set to `102` (YYYYMMDD). |  |
| `patient.drug.drugindication` | string | yes | Indication for the drug’s use. |  |
| `patient.drug.drugintervaldosagedefinition` | string |  | The unit for the interval in the field `drugintervaldosageunitnumb.` | `801`: Year; `802`: Month; `803`: Week; `804`: Day; `805`: Hour; `806`: Minute; `807`: Trimester; `810`: Cyclical; `811`: Trimester; `812`: As necessary; `813`: Total |
| `patient.drug.drugintervaldosageunitnumb` | string |  | Number of units in the field `drugintervaldosagedefinition`. |  |
| `patient.drug.drugrecurreadministration` | string |  | Whether the reaction occured after readministration of the drug. | `1`: Yes; `2`: No; `3`: Unknown |
| `patient.drug.drugrecurrence.drugrecuraction` | string | yes | Populated with the Reaction/Event information if/when `drugrecurreadministration` equals `1`. |  |
| `patient.drug.drugrecurrence.drugrecuractionmeddraversion` | string | yes | The version of MedDRA from which the term in `drugrecuraction` is drawn. |  |
| `patient.drug.drugseparatedosagenumb` | string |  | The number of separate doses that were administered. |  |
| `patient.drug.drugstartdate` | date |  | Date the patient began taking the drug. |  |
| `patient.drug.drugstartdateformat` | string |  | Encoding format of the field `drugstartdate`. Always set to `102` (YYYYMMDD). |  |
| `patient.drug.drugstructuredosagenumb` | string | yes | The number portion of a dosage; when combined with `drugstructuredosageunit` the complete dosage information is represented. For example, *300* in `300 mg`. |  |
| `patient.drug.drugstructuredosageunit` | string |  | The unit for the field `drugstructuredosagenumb`. For example, *mg* in `300 mg`. | `001`: kg (kilograms); `002`: g (grams); `003`: mg (milligrams); `004`: µg (micrograms) |
| `patient.drug.drugtreatmentduration` | string | yes | The interval of the field `drugtreatmentdurationunit` for which the patient was taking the drug. |  |
| `patient.drug.drugtreatmentdurationunit` | string |  |  | `801`: Year; `802`: Month; `803`: Week; `804`: Day; `805`: Hour; `806`: Minute |
| `patient.drug.medicinalproduct` | string | yes | Drug name. This may be the valid trade name of the product (such as `ADVIL` or `ALEVE`) or the generic name (such as `IBUPROFEN`). This field is not systematically normalized. It may contain misspellings or idiosyncratic descriptions of dr… |  |
| `patient.drug.openfda.application_number` | string[] | yes | This corresponds to the NDA, ANDA, or BLA number reported by the labeler for products which have the corresponding Marketing Category designated. If the designated Marketing Category is OTC Monograph Final or OTC Monograph Not Final, then… |  |
| `patient.drug.openfda.brand_name` | string[] | yes | Brand or trade name of the drug product. |  |
| `patient.drug.openfda.generic_name` | string[] | yes | Generic name(s) of the drug product. |  |
| `patient.drug.openfda.manufacturer_name` | string[] | yes | Name of manufacturer or company that makes this drug product, corresponding to the labeler code segment of the NDC. |  |
| `patient.drug.openfda.nui` | string[] | yes | Unique identifier applied to a drug concept within the National Drug File Reference Terminology (NDF-RT). | see NDF-RT (https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NDFRT/) |
| `patient.drug.openfda.package_ndc` | string[] | yes | This number, known as the NDC, identifies the labeler, product, and trade package size. The first segment, the labeler code, is assigned by the FDA. A labeler is any firm that manufactures (including repackers or relabelers), or distribute… |  |
| `patient.drug.openfda.pharm_class_cs` | string[] | yes | Chemical structure classification of the drug product’s pharmacologic class. Takes the form of the classification, followed by `[Chemical/Ingredient]` (such as `Thiazides [Chemical/Ingredient]` or `Antibodies, Monoclonal [Chemical/Ingredie… |  |
| `patient.drug.openfda.pharm_class_epc` | string[] | yes | Established pharmacologic class associated with an approved indication of an active moiety (generic drug) that the FDA has determined to be scientifically valid and clinically meaningful. Takes the form of the pharmacologic class, followed… |  |
| `patient.drug.openfda.pharm_class_moa` | string[] | yes | Mechanism of action of the drug—molecular, subcellular, or cellular functional activity—of the drug’s established pharmacologic class. Takes the form of the mechanism of action, followed by `[MoA]` (such as `Calcium Channel Antagonists [Mo… |  |
| `patient.drug.openfda.pharm_class_pe` | string[] | yes | Physiologic effect or pharmacodynamic effect—tissue, organ, or organ system level functional activity—of the drug’s established pharmacologic class. Takes the form of the effect, followed by `[PE]` (such as `Increased Diuresis [PE]` or `De… |  |
| `patient.drug.openfda.product_ndc` | string[] | yes | The labeler manufacturer code and product code segments of the NDC number, separated by a hyphen. |  |
| `patient.drug.openfda.product_type` | string[] | yes |  | see Type of drug product (http://www.fda.gov/ForIndustry/DataStandards/StructuredProductLabeling/ucm162063.htm) |
| `patient.drug.openfda.route` | string[] | yes | The route of administation of the drug product. | see Route of administration (http://www.fda.gov/ForIndustry/DataStandards/StructuredProductLabeling/ucm162034.htm) |
| `patient.drug.openfda.rxcui` | string[] | yes | The RxNorm Concept Unique Identifier. RxCUI is a unique number that describes a semantic concept about the drug product, including its ingredients, strength, and dose forms. | see RxNorm and RxCUI documentation (https://www.nlm.nih.gov/research/umls/rxnorm/docs/2012/rxnorm_doco_full_2012-3.html) |
| `patient.drug.openfda.spl_id` | string[] | yes | Unique identifier for a particular version of a Structured Product Label for a product. Also referred to as the document ID. |  |
| `patient.drug.openfda.spl_set_id` | string[] | yes | Unique identifier for the Structured Product Label for a product, which is stable across versions of the label. Also referred to as the set ID. |  |
| `patient.drug.openfda.substance_name` | string[] | yes | The list of active ingredients of a drug product. |  |
| `patient.drug.openfda.unii` | string[] | yes | Unique Ingredient Identifier, which is a non-proprietary, free, unique, unambiguous, non-semantic, alphanumeric identifier based on a substance’s molecular structure and/or descriptive information. | see Unique Ingredient Identifiers (http://fdasis.nlm.nih.gov/srs/srs.jsp) |
| `patient.patientagegroup` | string |  | Populated with Patient Age Group code. | `1`: Neonate; `2`: Infant; `3`: Child; `4`: Adolescent; `5`: Adult; `6`: Elderly |
| `patient.patientdeath.patientdeathdate` | date |  | If the patient died, the date that the patient died. |  |
| `patient.patientdeath.patientdeathdateformat` | string |  | Encoding format of the field `patientdeathdate`. Always set to `102` (YYYYMMDD). |  |
| `patient.patientonsetage` | string |  | Age of the patient when the event first occured. |  |
| `patient.patientonsetageunit` | string |  | The unit for the interval in the field `patientonsetage.` | `800`: Decade; `801`: Year; `802`: Month; `803`: Week; `804`: Day; `805`: Hour |
| `patient.patientsex` | string |  | The sex of the patient. | `0`: Unknown; `1`: Male; `2`: Female |
| `patient.patientweight` | string |  | The patient weight, in kg (kilograms). |  |
| `patient.reaction.reactionmeddrapt` | string | yes | Patient reaction, as a MedDRA term. Note that these terms are encoded in British English. For instance, diarrhea is spelled `diarrohea`. MedDRA is a standardized medical terminology. | see MedDRA (http://www.fda.gov/ForIndustry/DataStandards/StructuredProductLabeling/ucm162038.htm) |
| `patient.reaction.reactionmeddraversionpt` | string |  | The version of MedDRA from which the term in `reactionmeddrapt` is drawn. |  |
| `patient.reaction.reactionoutcome` | string |  | Outcome of the reaction in `reactionmeddrapt` at the time of last observation. | `1`: Recovered/resolved; `2`: Recovering/resolving; `3`: Not recovered/not resolved; `4`: Recovered/resolved with sequelae (consequent health issues); `5`: Fatal; `6`: Unknown |
| `patient.summary.narrativeincludeclinical` | string |  | Populated with Case Event Date, when available; does `NOT` include Case Narrative. |  |
| `primarysource.literaturereference` | string |  | Populated with the Literature Reference information, when available. |  |
| `primarysource.qualification` | string |  | Category of individual who submitted the report. | `1`: Physician; `2`: Pharmacist; `3`: Other health professional; `4`: Lawyer; `5`: Consumer or non-health professional |
| `primarysource.reportercountry` | string | yes | Country from which the report was submitted. |  |
| `primarysourcecountry` | string | yes | Country of the reporter of the event. | see Country codes (http://data.okfn.org/data/core/country-list) |
| `receiptdate` | date |  | Date that the _most recent_ information in the report was received by FDA. |  |
| `receiptdateformat` | string |  | Encoding format of the `receiptdate` field. Always set to 102 (YYYYMMDD). |  |
| `receivedate` | date |  | Date that the report was _first_ received by FDA. If this report has multiple versions, this will be the date the first version was received by FDA. |  |
| `receivedateformat` | string |  | Encoding format of the `receivedate` field. Always set to 102 (YYYYMMDD). |  |
| `receiver.receiverorganization` | string | yes | Name of the organization receiving the report. Because FDA received the report, the value is always `FDA`. |  |
| `receiver.receivertype` | string |  | The type of organization receiving the report. The value,`6`, is only specified if it is `other`, otherwise it is left blank. | `6`: Other |
| `reportduplicate.duplicatenumb` | string | yes | The case identifier for the duplicate. |  |
| `reportduplicate.duplicatesource` | string | yes | The name of the organization providing the duplicate. |  |
| `reporttype` | string |  | Code indicating the circumstances under which the report was generated. | `1`: Spontaneous; `2`: Report from study; `3`: Other; `4`: Not available to sender (unknown) |
| `safetyreportid` | string | yes | The 8-digit Safety Report ID number, also known as the case report number or case ID. The first 7 digits (before the hyphen) identify an individual report and the last digit (after the hyphen) is a checksum. This field can be used to ident… |  |
| `safetyreportversion` | string |  | The version number of the `safetyreportid`. Multiple versions of the same report may exist, it is generally best to only count the latest report and disregard others. openFDA will only return the latest version of a report. |  |
| `sender.senderorganization` | string | yes | Name of the organization sending the report. Because FDA is providing these reports to you, the value is always `FDA-Public Use.` |  |
| `sender.sendertype` | string |  | The name of the organization sending the report. Because FDA is providing these reports to you, the value is always `2`. | `2`: Regulatory authority |
| `serious` | string |  | Seriousness of the adverse event. | `1`: The adverse event resulted in death, a life threatening condition, hospitalization, disability, congenital anomaly, or other serious condition; `2`: The adverse event did not result in any of the above |
| `seriousnesscongenitalanomali` | string |  | This value is `1` if the adverse event resulted in a congenital anomaly, and absent otherwise. |  |
| `seriousnessdeath` | string |  | This value is `1` if the adverse event resulted in death, and absent otherwise. |  |
| `seriousnessdisabling` | string |  | This value is `1` if the adverse event resulted in disability, and absent otherwise. |  |
| `seriousnesshospitalization` | string |  | This value is `1` if the adverse event resulted in a hospitalization, and absent otherwise. |  |
| `seriousnesslifethreatening` | string |  | This value is `1` if the adverse event resulted in a life threatening condition, and absent otherwise. |  |
| `seriousnessother` | string |  | This value is `1` if the adverse event resulted in some other serious condition, and absent otherwise. |  |
| `transmissiondate` | date |  | Date that the record was created. This may be earlier than the date the record was received by the FDA. |  |
| `transmissiondateformat` | string |  | Encoding format of the `transmissiondate` field. Always set to 102 (YYYYMMDD). |  |

## Usage tips

- Pick the field by question:
  - Drug in the report: `patient.drug.medicinalproduct` (as reported), or the harmonized `patient.drug.openfda.brand_name` / `generic_name` / `substance_name`. The `openfda` fields are missing on about 2.2 million reports, so search `medicinalproduct` too when completeness matters.
  - Reactions: `patient.reaction.reactionmeddrapt` (MedDRA preferred terms). Its `.exact` values are uppercase (`DRUG INEFFECTIVE`, `NAUSEA`).
  - Seriousness: `serious` is `1` (serious) or `2` (not). The `seriousness*` flags (`seriousnessdeath`, `seriousnesshospitalization`, ...) are documented as `1` or absent, but the data also holds `2`, so search `seriousnessdeath:1`, not `_exists_:seriousnessdeath`.
  - Patient: `patient.patientsex` is `0` unknown, `1` male, `2` female; `patient.patientonsetage` with `patient.patientonsetageunit`.
  - Drug role: `patient.drug.drugcharacterization` is `1` suspect, `2` concomitant, `3` interacting.
  - Country where the event occurred: `occurcountry.exact` (2-letter codes, `US` first).
- Brand names in `patient.drug.openfda.brand_name.exact` are uppercase: `.exact:"LIPITOR"` works and `.exact:"Lipitor"` returns no matches, while plain `patient.drug.openfda.brand_name:"lipitor"` matches 248,656 reports.
- `count=receivedate` returns daily `time` buckets (`YYYYMMDD`); narrow it with a `receivedate:[A TO B]` search.
- A report says a reaction happened while a drug was taken. It does not show the drug caused it, and counts reflect reporting, not incidence.
- `.exact` is case-sensitive and matches the whole value. In drug/label, `openfda.brand_name.exact:"Tylenol"` returns no matches, while plain `openfda.brand_name:"tylenol"` returns 112 labels.
- A misspelled field name returns "No matches found!", the same as a search with no hits. fda_get_dataset adds a hint when a field is not in the table above.
- Counting a date field returns every date in the result, whatever the `limit`. Narrow the search to a date range first.
- Pass `fields` to fda_get_dataset to return only the paths you need, e.g. `fields=["openfda.brand_name", "boxed_warning"]`.
