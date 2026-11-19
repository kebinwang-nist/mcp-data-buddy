---
name: fda-drug-labeling
description: Query openFDA drug labeling (structured product labels, api.fda.gov/drug/label). Use it for the text of prescription and OTC drug labels, such as indications, dosage, boxed warnings, contraindications, adverse reactions, drug interactions and active ingredients, looked up by brand or generic name.
---

# openFDA: Drug labeling (SPL)

## Overview

- API: `https://api.fda.gov` (openFDA, Elasticsearch-based REST API). Docs: https://open.fda.gov/apis/drug/label/. Field definitions: https://open.fda.gov/fields/druglabel.yaml.
- Snapshot taken 2026-11-19: 264,929 records; data last updated 2026-11-19 (`meta.last_updated`); bulk export date 2026-11-19 (download.json).
- Surface: read-only `GET`, JSON only. One endpoint; no per-record ids to look up.
- Auth: optional API key (env `OPENFDA_API_KEY`, sent as the Basic-auth username). Without a key: 240 requests/minute and 1,000/day per IP; with a key: 120,000/day. `count` with `limit=1000` needs a key.
- Disclaimer: openFDA asks users not to base medical care decisions on it and to treat all results as unvalidated; FDA may limit API access under its terms. Terms: https://open.fda.gov/terms/. License: https://open.fda.gov/license/.
- Sample record: one `limit=1` record was fetched to list the fields it returns; values were not stored.
- Records are large: in a sample of 20 labels, one record was 1.6 KB to 352 KB of JSON. Always pass `fields` (and a small `limit`) to fda_get_dataset.

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
| `drug/label` | Drug labeling (SPL) | drug | 264,929 | 197 | 2026-11-19 |

## Endpoint

### drug/label

**Drug labeling (SPL)**

- Endpoint: `GET https://api.fda.gov/drug/label.json`
- Records: 264,929. Last updated: 2026-11-19. Probe status: 200.
- Sample record fields (limit=1): `effective_time`, `inactive_ingredient`, `purpose`, `keep_out_of_reach_of_children`, `warnings`, `questions`, `spl_product_data_elements`, `openfda.brand_name`, `openfda.generic_name`, `openfda.manufacturer_name`, `openfda.product_ndc`, `openfda.product_type`, `openfda.route`, `openfda.substance_name`, `openfda.spl_id`, `openfda.spl_set_id`, `openfda.package_ndc`, `openfda.is_original_packager`, `openfda.upc`, `openfda.unii`, `version`, `dosage_and_administration`, `pregnancy_or_breast_feeding`, `stop_use`, `storage_and_handling`, `do_not_use`, `package_label_principal_display_panel`, `indications_and_usage`, `set_id`, `id`, `active_ingredient`
- Example queries (run on 2026-11-19):

  ```
  # Labels for ibuprofen (200, 1,189 records)
  GET https://api.fda.gov/drug/label.json?search=openfda.generic_name:"ibuprofen"&limit=1
  # Labels for Tylenol (200, 112 records)
  GET https://api.fda.gov/drug/label.json?search=openfda.brand_name:"tylenol"&limit=1
  # Routes of administration of labels with a boxed warning (200, 5 terms)
  GET https://api.fda.gov/drug/label.json?search=_exists_:boxed_warning&count=openfda.route.exact&limit=5
  ```

| Field | Type | Exact | Description | Possible values |
|---|---|---|---|---|
| `abuse` | string[] |  | Information about the types of abuse that can occur with the drug and adverse reactions pertinent to those types of abuse, primarily based on human data. May include descriptions of particularly susceptible patient populations. |  |
| `abuse_table` | string[] |  | Information about the types of abuse that can occur with the drug and adverse reactions pertinent to those types of abuse, primarily based on human data. May include descriptions of particularly susceptible patient populations. |  |
| `accessories` | string[] |  | Documentation forthcoming. |  |
| `accessories_table` | string[] |  | Documentation forthcoming. |  |
| `active_ingredient` | string[] |  | A list of the active, medicinal ingredients in the drug product. |  |
| `active_ingredient_table` | string[] |  | A list of the active, medicinal ingredients in the drug product. |  |
| `adverse_reactions` | string[] |  | Information about undesirable effects, reasonably associated with use of the drug, that may occur as part of the pharmacological action of the drug or may be unpredictable in its occurrence. Adverse reactions include those that occur with… |  |
| `adverse_reactions_table` | string[] |  | Information about undesirable effects, reasonably associated with use of the drug, that may occur as part of the pharmacological action of the drug or may be unpredictable in its occurrence. Adverse reactions include those that occur with… |  |
| `alarms` | string[] |  | Documentation forthcoming. |  |
| `alarms_table` | string[] |  | Documentation forthcoming. |  |
| `animal_pharmacology_and_or_toxicology` | string[] |  | Information from studies of the drug in animals, if the data were not relevant to nor included in other parts of the labeling. Most labels do not contain this field. |  |
| `animal_pharmacology_and_or_toxicology_table` | string[] |  | Information from studies of the drug in animals, if the data were not relevant to nor included in other parts of the labeling. Most labels do not contain this field. |  |
| `ask_doctor` | string[] |  | Information about when a doctor should be consulted about existing conditions or sumptoms before using the drug product, including all warnings for persons with certain preexisting conditions (excluding pregnancy) and all warnings for pers… |  |
| `ask_doctor_or_pharmacist` | string[] |  | Information about when a doctor or pharmacist should be consulted about drug/drug or drug/food interactions before using a drug product. |  |
| `ask_doctor_or_pharmacist_table` | string[] |  | Information about when a doctor or pharmacist should be consulted about drug/drug or drug/food interactions before using a drug product. |  |
| `ask_doctor_table` | string[] |  | Information about when a doctor should be consulted about existing conditions or sumptoms before using the drug product, including all warnings for persons with certain preexisting conditions (excluding pregnancy) and all warnings for pers… |  |
| `assembly_or_installation_instructions` | string[] |  | Documentation forthcoming. |  |
| `assembly_or_installation_instructions_table` | string[] |  | Documentation forthcoming. |  |
| `boxed_warning` | string[] |  | Information about contraindications or serious warnings, particularly those that may lead to death or serious injury. |  |
| `boxed_warning_table` | string[] |  | Information about contraindications or serious warnings, particularly those that may lead to death or serious injury. |  |
| `calibration_instructions` | string[] |  | Documentation forthcoming. |  |
| `calibration_instructions_table` | string[] |  | Documentation forthcoming. |  |
| `carcinogenesis_and_mutagenesis_and_impairment_of_fertility` | string[] |  | Information about carcinogenic, mutagenic, or fertility impairment potential revealed by studies in animals. Information from human data about such potential is part of the `warnings` field. |  |
| `carcinogenesis_and_mutagenesis_and_impairment_of_fertility_table` | string[] |  | Information about carcinogenic, mutagenic, or fertility impairment potential revealed by studies in animals. Information from human data about such potential is part of the `warnings` field. |  |
| `cleaning` | string[] |  | Documentation forthcoming. |  |
| `cleaning_table` | string[] |  | Documentation forthcoming. |  |
| `clinical_pharmacology` | string[] |  | Information about the clinical pharmacology and actions of the drug in humans. |  |
| `clinical_pharmacology_table` | string[] |  | Information about the clinical pharmacology and actions of the drug in humans. |  |
| `clinical_studies` | string[] |  | This field may contain references to clinical studies in place of detailed discussion in other sections of the labeling. |  |
| `clinical_studies_table` | string[] |  | This field may contain references to clinical studies in place of detailed discussion in other sections of the labeling. |  |
| `compatible_accessories` | string[] |  | Documentation forthcoming. |  |
| `compatible_accessories_table` | string[] |  | Documentation forthcoming. |  |
| `components` | string[] |  | Documentation forthcoming. |  |
| `components_table` | string[] |  | Documentation forthcoming. |  |
| `contraindications` | string[] |  | Information about situations in which the drug product is contraindicated or should not be used because the risk of use clearly outweighs any possible benefit, including the type and nature of reactions that have been reported. |  |
| `contraindications_table` | string[] |  | Information about situations in which the drug product is contraindicated or should not be used because the risk of use clearly outweighs any possible benefit, including the type and nature of reactions that have been reported. |  |
| `controlled_substance` | string[] |  | Information about the schedule in which the drug is controlled by the Drug Enforcement Administration, if applicable. |  |
| `controlled_substance_table` | string[] |  | Information about the schedule in which the drug is controlled by the Drug Enforcement Administration, if applicable. |  |
| `dependence` | string[] |  | Information about characteristic effects resulting from both psychological and physical dependence that occur with the drug, the quantity of drug over a period of time that may lead to tolerance or dependence, details of adverse effects re… |  |
| `dependence_table` | string[] |  | Information about characteristic effects resulting from both psychological and physical dependence that occur with the drug, the quantity of drug over a period of time that may lead to tolerance or dependence, details of adverse effects re… |  |
| `description` | string[] |  | General information about the drug product, including the proprietary and established name of the drug, the type of dosage form and route of administration to which the label applies, qualitative and quantitative ingredient information, th… |  |
| `description_table` | string[] |  | General information about the drug product, including the proprietary and established name of the drug, the type of dosage form and route of administration to which the label applies, qualitative and quantitative ingredient information, th… |  |
| `diagram_of_device` | string[] |  | Documentation forthcoming. |  |
| `diagram_of_device_table` | string[] |  | Documentation forthcoming. |  |
| `disposal_and_waste_handling` | string[] |  |  |  |
| `disposal_and_waste_handling_table` | string[] |  |  |  |
| `do_not_use` | string[] |  | Information about all contraindications for use. These contraindications are absolute and are intended for situations in which consumers should not use the product unless a prior diagnosis has been established by a doctor or for situations… |  |
| `do_not_use_table` | string[] |  | Information about all contraindications for use. These contraindications are absolute and are intended for situations in which consumers should not use the product unless a prior diagnosis has been established by a doctor or for situations… |  |
| `dosage_and_administration` | string[] |  | Information about the drug product’s dosage and administration recommendations, including starting dose, dose range, titration regimens, and any other clinically sigificant information that affects dosing recommendations. |  |
| `dosage_and_administration_table` | string[] |  | Information about the drug product’s dosage and administration recommendations, including starting dose, dose range, titration regimens, and any other clinically sigificant information that affects dosing recommendations. |  |
| `dosage_forms_and_strengths` | string[] |  | Information about all available dosage forms and strengths for the drug product to which the labeling applies. This field may contain descriptions of product appearance. |  |
| `dosage_forms_and_strengths_table` | string[] |  | Information about all available dosage forms and strengths for the drug product to which the labeling applies. This field may contain descriptions of product appearance. |  |
| `drug_abuse_and_dependence` | string[] |  | Information about whether the drug is a controlled substance, the types of abuse that can occur with the drug, and adverse reactions pertinent to those types of abuse. |  |
| `drug_abuse_and_dependence_table` | string[] |  | Information about whether the drug is a controlled substance, the types of abuse that can occur with the drug, and adverse reactions pertinent to those types of abuse. |  |
| `drug_and_or_laboratory_test_interactions` | string[] |  | Information about any known interference by the drug with laboratory tests. |  |
| `drug_and_or_laboratory_test_interactions_table` | string[] |  | Information about any known interference by the drug with laboratory tests. |  |
| `drug_interactions` | string[] |  | Information about and practical guidance on preventing clinically significant drug/drug and drug/food interactions that may occur in people taking the drug. |  |
| `drug_interactions_table` | string[] |  | Information about and practical guidance on preventing clinically significant drug/drug and drug/food interactions that may occur in people taking the drug. |  |
| `effective_time` | date |  | Date reference to the particular version of the labeling document. |  |
| `environmental_warning` | string[] |  |  |  |
| `environmental_warning_table` | string[] |  |  |  |
| `food_safety_warning` | string[] |  |  |  |
| `food_safety_warning_table` | string[] |  |  |  |
| `general_precautions` | string[] |  | Information about any special care to be exercised for safe and effective use of the drug. |  |
| `general_precautions_table` | string[] |  | Information about any special care to be exercised for safe and effective use of the drug. |  |
| `geriatric_use` | string[] |  | Information about any limitations on any geriatric indications, needs for specific monitoring, hazards associated with use of the drug in the geriatric population. |  |
| `geriatric_use_table` | string[] |  | Information about any limitations on any geriatric indications, needs for specific monitoring, hazards associated with use of the drug in the geriatric population. |  |
| `guaranteed_analysis_of_feed` | string[] |  | Documentation forthcoming. |  |
| `guaranteed_analysis_of_feed_table` | string[] |  | Documentation forthcoming. |  |
| `health_care_provider_letter` | string[] |  | Documentation forthcoming. |  |
| `health_care_provider_letter_table` | string[] |  | Documentation forthcoming. |  |
| `health_claim` | string[] |  | Documentation forthcoming. |  |
| `health_claim_table` | string[] |  | Documentation forthcoming. |  |
| `how_supplied` | string[] |  | Information about the available dosage forms to which the labeling applies, and for which the manufacturer or distributor is responsible. This field ordinarily includes the strength of the dosage form (in metric units), the units in which… |  |
| `how_supplied_table` | string[] |  | Information about the available dosage forms to which the labeling applies, and for which the manufacturer or distributor is responsible. This field ordinarily includes the strength of the dosage form (in metric units), the units in which… |  |
| `id` | string |  | The document ID, A globally unique identifier (GUID) for the particular revision of a labeling document. |  |
| `inactive_ingredient` | string[] |  | A list of inactive, non-medicinal ingredients in a drug product. |  |
| `inactive_ingredient_table` | string[] |  | A list of inactive, non-medicinal ingredients in a drug product. |  |
| `indications_and_usage` | string[] |  | A statement of each of the drug product’s indications for use, such as for the treatment, prevention, mitigation, cure, or diagnosis of a disease or condition, or of a manifestation of a recognized disease or condition, or for the relief o… |  |
| `indications_and_usage_table` | string[] |  | A statement of each of the drug product’s indications for use, such as for the treatment, prevention, mitigation, cure, or diagnosis of a disease or condition, or of a manifestation of a recognized disease or condition, or for the relief o… |  |
| `information_for_owners_or_caregivers` | string[] |  | Documentation forthcoming. |  |
| `information_for_owners_or_caregivers_table` | string[] |  | Documentation forthcoming. |  |
| `information_for_patients` | string[] |  | Information necessary for patients to use the drug safely and effectively, such as precautions concerning driving or the concomitant use of other substances that may have harmful additive effects. |  |
| `information_for_patients_table` | string[] |  | Information necessary for patients to use the drug safely and effectively, such as precautions concerning driving or the concomitant use of other substances that may have harmful additive effects. |  |
| `instructions_for_use` | string[] |  | Information about safe handling and use of the drug product. |  |
| `instructions_for_use_table` | string[] |  | Information about safe handling and use of the drug product. |  |
| `intended_use_of_the_device` | string[] |  | Documentation forthcoming. |  |
| `intended_use_of_the_device_table` | string[] |  | Documentation forthcoming. |  |
| `keep_out_of_reach_of_children` | string[] |  | Information pertaining to whether the product should be kept out of the reach of children, and instructions about what to do in the case of accidental contact or ingestion, if appropriate. |  |
| `keep_out_of_reach_of_children_table` | string[] |  | Information pertaining to whether the product should be kept out of the reach of children, and instructions about what to do in the case of accidental contact or ingestion, if appropriate. |  |
| `labor_and_delivery` | string[] |  | Information about the drug’s use during labor or delivery, whether or not the use is stated in the indications section of the labeling, including the effect of the drug on the mother and fetus, on the duration of labor or delivery, on the… |  |
| `labor_and_delivery_table` | string[] |  | Information about the drug’s use during labor or delivery, whether or not the use is stated in the indications section of the labeling, including the effect of the drug on the mother and fetus, on the duration of labor or delivery, on the… |  |
| `laboratory_tests` | string[] |  | Information on laboratory tests helpful in following the patient’s response to the drug or in identifying possible adverse reactions. If appropriate, information may be provided on such factors as the range of normal and abnormal values ex… |  |
| `laboratory_tests_table` | string[] |  | Information on laboratory tests helpful in following the patient’s response to the drug or in identifying possible adverse reactions. If appropriate, information may be provided on such factors as the range of normal and abnormal values ex… |  |
| `mechanism_of_action` | string[] |  | Information about the established mechanism(s) of the drug’s action in humans at various levels (for example receptor, membrane, tissue, organ, whole body). If the mechanism of action is not known, this field contains a statement about the… |  |
| `mechanism_of_action_table` | string[] |  | Information about the established mechanism(s) of the drug’s action in humans at various levels (for example receptor, membrane, tissue, organ, whole body). If the mechanism of action is not known, this field contains a statement about the… |  |
| `microbiology` | string[] |  | Documentation forthcoming. |  |
| `microbiology_table` | string[] |  | Documentation forthcoming. |  |
| `nonclinical_toxicology` | string[] |  | Information about toxicology in non-human subjects. |  |
| `nonclinical_toxicology_table` | string[] |  | Information about toxicology in non-human subjects. |  |
| `nonteratogenic_effects` | string[] |  | Other information about the drug’s effects on reproduction and the drug’s use during pregnancy, if the information is relevant to the safe and effective use of the drug. |  |
| `nonteratogenic_effects_table` | string[] |  | Other information about the drug’s effects on reproduction and the drug’s use during pregnancy, if the information is relevant to the safe and effective use of the drug. |  |
| `nursing_mothers` | string[] |  | Information about excretion of the drug in human milk and effects on the nursing infant, including pertinent adverse effects observed in animal offspring. |  |
| `nursing_mothers_table` | string[] |  | Information about excretion of the drug in human milk and effects on the nursing infant, including pertinent adverse effects observed in animal offspring. |  |
| `openfda.application_number` | string[] | yes | This corresponds to the NDA, ANDA, or BLA number reported by the labeler for products which have the corresponding Marketing Category designated. If the designated Marketing Category is OTC Monograph Final or OTC Monograph Not Final, then… |  |
| `openfda.brand_name` | string[] | yes | Brand or trade name of the drug product. |  |
| `openfda.generic_name` | string[] | yes | Generic name(s) of the drug product. |  |
| `openfda.is_original_packager` | string | yes | Whether or not the drug has been repackaged for distribution. |  |
| `openfda.manufacturer_name` | string[] | yes | Name of manufacturer or company that makes this drug product, corresponding to the labeler code segment of the NDC. |  |
| `openfda.nui` | string[] | yes | Unique identifier applied to a drug concept within the National Drug File Reference Terminology (NDF-RT). | see NDF-RT (https://www.nlm.nih.gov/research/umls/sourcereleasedocs/current/NDFRT/) |
| `openfda.original_packager_product_ndc` | string[] | yes | This ndc identifies the original packager. |  |
| `openfda.package_ndc` | string[] | yes | This number, known as the NDC, identifies the labeler, product, and trade package size. The first segment, the labeler code, is assigned by the FDA. A labeler is any firm that manufactures (including repackers or relabelers), or distribute… |  |
| `openfda.pharm_class_cs` | string[] | yes | Chemical structure classification of the drug product’s pharmacologic class. Takes the form of the classification, followed by `[Chemical/Ingredient]` (such as `Thiazides [Chemical/Ingredient]` or `Antibodies, Monoclonal [Chemical/Ingredie… |  |
| `openfda.pharm_class_epc` | string[] | yes | Established pharmacologic class associated with an approved indication of an active moiety (generic drug) that the FDA has determined to be scientifically valid and clinically meaningful. Takes the form of the pharmacologic class, followed… |  |
| `openfda.pharm_class_moa` | string[] | yes | Mechanism of action of the drug—molecular, subcellular, or cellular functional activity—of the drug’s established pharmacologic class. Takes the form of the mechanism of action, followed by `[MoA]` (such as `Calcium Channel Antagonists [Mo… |  |
| `openfda.pharm_class_pe` | string[] | yes | Physiologic effect or pharmacodynamic effect—tissue, organ, or organ system level functional activity—of the drug’s established pharmacologic class. Takes the form of the effect, followed by `[PE]` (such as `Increased Diuresis [PE]` or `De… |  |
| `openfda.product_ndc` | string[] | yes | The labeler manufacturer code and product code segments of the NDC number, separated by a hyphen. |  |
| `openfda.product_type` | string[] | yes |  | see Type of drug product (http://www.fda.gov/ForIndustry/DataStandards/StructuredProductLabeling/ucm162063.htm) |
| `openfda.route` | string[] | yes | The route of administation of the drug product. | see Route of administration (http://www.fda.gov/ForIndustry/DataStandards/StructuredProductLabeling/ucm162034.htm) |
| `openfda.rxcui` | string[] | yes | The RxNorm Concept Unique Identifier. RxCUI is a unique number that describes a semantic concept about the drug product, including its ingredients, strength, and dose forms. | see RxNorm and RxCUI documentation (https://www.nlm.nih.gov/research/umls/rxnorm/docs/2012/rxnorm_doco_full_2012-3.html) |
| `openfda.spl_id` | string[] | yes | Unique identifier for a particular version of a Structured Product Label for a product. Also referred to as the document ID. |  |
| `openfda.spl_set_id` | string[] | yes | Unique identifier for the Structured Product Label for a product, which is stable across versions of the label. Also referred to as the set ID. |  |
| `openfda.substance_name` | string[] | yes | The list of active ingredients of a drug product. |  |
| `openfda.unii` | string[] | yes | Unique Ingredient Identifier, which is a non-proprietary, free, unique, unambiguous, non-semantic, alphanumeric identifier based on a substance’s molecular structure and/or descriptive information. | see Unique Ingredient Identifiers (http://fdasis.nlm.nih.gov/srs/srs.jsp) |
| `openfda.upc` | string[] | yes | Universal Product Code | see Universal Product Code (https://en.wikipedia.org/wiki/Universal_Product_Code) |
| `other_safety_information` | string[] |  | Information about safe use and handling of the product that may not have been specified in another field. |  |
| `other_safety_information_table` | string[] |  | Information about safe use and handling of the product that may not have been specified in another field. |  |
| `overdosage` | string[] |  | Information about signs, symptoms, and laboratory findings of acute ovedosage and the general principles of overdose treatment. |  |
| `overdosage_table` | string[] |  | Information about signs, symptoms, and laboratory findings of acute ovedosage and the general principles of overdose treatment. |  |
| `package_label_principal_display_panel` | string[] |  | The content of the principal display panel of the product package, usually including the product’s name, dosage forms, and other key information about the drug product. |  |
| `package_label_principal_display_panel_table` | string[] |  | The content of the principal display panel of the product package, usually including the product’s name, dosage forms, and other key information about the drug product. |  |
| `patient_medication_information` | string[] |  | Information or instructions to patients about safe use of the drug product, sometimes including a reference to a patient medication guide or counseling materials. |  |
| `patient_medication_information_table` | string[] |  | Information or instructions to patients about safe use of the drug product, sometimes including a reference to a patient medication guide or counseling materials. |  |
| `pediatric_use` | string[] |  | Information about any limitations on any pediatric indications, needs for specific monitoring, hazards associated with use of the drug in any subsets of the pediatric population (such as neonates, infants, children, or adolescents), differ… |  |
| `pediatric_use_table` | string[] |  | Information about any limitations on any pediatric indications, needs for specific monitoring, hazards associated with use of the drug in any subsets of the pediatric population (such as neonates, infants, children, or adolescents), differ… |  |
| `pharmacodynamics` | string[] |  | Information about any biochemical or physiologic pharmacologic effects of the drug or active metabolites related to the drug’s clinical effect in preventing, diagnosing, mitigating, curing, or treating disease, or those related to adverse… |  |
| `pharmacodynamics_table` | string[] |  | Information about any biochemical or physiologic pharmacologic effects of the drug or active metabolites related to the drug’s clinical effect in preventing, diagnosing, mitigating, curing, or treating disease, or those related to adverse… |  |
| `pharmacogenomics` | string[] |  | Documentation forthcoming. |  |
| `pharmacogenomics_table` | string[] |  | Documentation forthcoming. |  |
| `pharmacokinetics` | string[] |  | Information about the clinically significant pharmacokinetics of a drug or active metabolites, for instance pertinent absorption, distribution, metabolism, and excretion parameters. |  |
| `pharmacokinetics_table` | string[] |  | Information about the clinically significant pharmacokinetics of a drug or active metabolites, for instance pertinent absorption, distribution, metabolism, and excretion parameters. |  |
| `precautions` | string[] |  | Information about any special care to be exercised for safe and effective use of the drug. |  |
| `precautions_table` | string[] |  | Information about any special care to be exercised for safe and effective use of the drug. |  |
| `pregnancy` | string[] |  | Information about effects the drug may have on pregnant women or on a fetus. This field may be ommitted if the drug is not absorbed systemically and the drug is not known to have a potential for indirect harm to the fetus. It may contain i… |  |
| `pregnancy_or_breast_feeding` | string[] |  | Documentation forthcoming. |  |
| `pregnancy_or_breast_feeding_table` | string[] |  | Documentation forthcoming. |  |
| `pregnancy_table` | string[] |  | Information about effects the drug may have on pregnant women or on a fetus. This field may be ommitted if the drug is not absorbed systemically and the drug is not known to have a potential for indirect harm to the fetus. It may contain i… |  |
| `purpose` | string[] |  | Information about the drug product’s indications for use. |  |
| `purpose_table` | string[] |  | Information about the drug product’s indications for use. |  |
| `questions` | string[] |  | A telephone number of a source to answer questions about a drug product. Sometimes available days and times are also noted. |  |
| `questions_table` | string[] |  | A telephone number of a source to answer questions about a drug product. Sometimes available days and times are also noted. |  |
| `recent_major_changes` | string[] |  | A list of the section(s) that contain substantive changes that have been approved by FDA in the product labeling. The headings and subheadings, if appropriate, affected by the change are listed together with each section’s identifying numb… |  |
| `recent_major_changes_table` | string[] |  | A list of the section(s) that contain substantive changes that have been approved by FDA in the product labeling. The headings and subheadings, if appropriate, affected by the change are listed together with each section’s identifying numb… |  |
| `references` | string[] |  | This field may contain references when prescription drug labeling must summarize or otherwise relay on a recommendation by an authoritative scientific body, or on a standardized methodology, scale, or technique, because the information is… |  |
| `references_table` | string[] |  | This field may contain references when prescription drug labeling must summarize or otherwise relay on a recommendation by an authoritative scientific body, or on a standardized methodology, scale, or technique, because the information is… |  |
| `residue_warning` | string[] |  | Documentation forthcoming. |  |
| `residue_warning_table` | string[] |  | Documentation forthcoming. |  |
| `risks` | string[] |  | Documentation forthcoming. |  |
| `risks_table` | string[] |  | Documentation forthcoming. |  |
| `route` | string[] |  | Documentation forthcoming. |  |
| `route_table` | string[] |  | Documentation forthcoming. |  |
| `safe_handling_warning` | string[] |  | Documentation forthcoming. |  |
| `safe_handling_warning_table` | string[] |  | Documentation forthcoming. |  |
| `set_id` | string |  | The Set ID, A globally unique identifier (GUID) for the labeling, stable across all versions or revisions. |  |
| `spl_indexing_data_elements` | string[] |  | Documentation forthcoming. |  |
| `spl_indexing_data_elements_table` | string[] |  | Documentation forthcoming. |  |
| `spl_medguide` | string[] |  | Information about the patient medication guide that accompanies the drug product. Certain drugs must be dispensed with an accompanying medication guide. This field may contain information about when to consult the medication guide and the… |  |
| `spl_medguide_table` | string[] |  | Information about the patient medication guide that accompanies the drug product. Certain drugs must be dispensed with an accompanying medication guide. This field may contain information about when to consult the medication guide and the… |  |
| `spl_patient_package_insert` | string[] |  | Information necessary for patients to use the drug safely and effectively. |  |
| `spl_patient_package_insert_table` | string[] |  | Information necessary for patients to use the drug safely and effectively. |  |
| `spl_product_data_elements` | string[] |  | Usually a list of ingredients in a drug product. |  |
| `spl_product_data_elements_table` | string[] |  | Usually a list of ingredients in a drug product. |  |
| `spl_unclassified_section` | string[] |  | Information not classified as belonging to one of the other fields. Approximately 40% of labeling with `effective_time` between June 2009 and August 2014 have information in this field. |  |
| `spl_unclassified_section_table` | string[] |  | Information not classified as belonging to one of the other fields. Approximately 40% of labeling with `effective_time` between June 2009 and August 2014 have information in this field. |  |
| `statement_of_identity` | string[] |  | Documentation forthcoming. |  |
| `statement_of_identity_table` | string[] |  | Documentation forthcoming. |  |
| `stop_use` | string[] |  | Information about when use of the drug product should be discontinued immediately and a doctor consulted. Includes information about any signs of toxicity or other reactions that would necessitate immediately discontinuing use of the produ… |  |
| `stop_use_table` | string[] |  | Information about when use of the drug product should be discontinued immediately and a doctor consulted. Includes information about any signs of toxicity or other reactions that would necessitate immediately discontinuing use of the produ… |  |
| `storage_and_handling` | string[] |  | Information about safe storage and handling of the drug product. |  |
| `storage_and_handling_table` | string[] |  | Information about safe storage and handling of the drug product. |  |
| `summary_of_safety_and_effectiveness` | string[] |  | Documentation forthcoming. |  |
| `summary_of_safety_and_effectiveness_table` | string[] |  | Documentation forthcoming. |  |
| `teratogenic_effects` | string[] |  | _Pregnancy category A_: Adequate and well-controlled studies in pregnant women have failed to demonstrate a risk to the fetus in the first trimester of pregnancy, and there is no evidence of a risk in later trimesters. _Pregnancy category… |  |
| `teratogenic_effects_table` | string[] |  | _Pregnancy category A_: Adequate and well-controlled studies in pregnant women have failed to demonstrate a risk to the fetus in the first trimester of pregnancy, and there is no evidence of a risk in later trimesters. _Pregnancy category… |  |
| `troubleshooting` | string[] |  | Documentation forthcoming. |  |
| `troubleshooting_table` | string[] |  | Documentation forthcoming. |  |
| `use_in_specific_populations` | string[] |  | Information about use of the drug by patients in specific populations, including pregnant women and nursing mothers, pediatric patients, and geriatric patients. |  |
| `use_in_specific_populations_table` | string[] |  | Information about use of the drug by patients in specific populations, including pregnant women and nursing mothers, pediatric patients, and geriatric patients. |  |
| `user_safety_warnings` | string[] |  | When a drug can pose a hazard to human health by contact, inhalation, ingestion, injection, or by any exposure, this field contains information which can prevent or decrease the possibility of harm. |  |
| `user_safety_warnings_table` | string[] |  | When a drug can pose a hazard to human health by contact, inhalation, ingestion, injection, or by any exposure, this field contains information which can prevent or decrease the possibility of harm. |  |
| `version` | string |  | A sequentially increasing number identifying the particular version of a document, starting with `1`. |  |
| `warnings` | string[] |  | Information about serious adverse reactions and potential safety hazards, including limitations in use imposed by those hazards and steps that should be taken if they occur. |  |
| `warnings_and_cautions` | string[] |  | Documentation forthcoming. |  |
| `warnings_and_cautions_table` | string[] |  | Documentation forthcoming. |  |
| `warnings_table` | string[] |  | Information about serious adverse reactions and potential safety hazards, including limitations in use imposed by those hazards and steps that should be taken if they occur. |  |
| `when_using` | string[] |  | Information about side effects that people may experience, and the substances (e.g. alcohol) or activities (e.g. operating machinery, driving a car) to avoid while using the drug product. |  |
| `when_using_table` | string[] |  | Information about side effects that people may experience, and the substances (e.g. alcohol) or activities (e.g. operating machinery, driving a car) to avoid while using the drug product. |  |

## Usage tips

- Pick the field by question:
  - Find the label: `openfda.brand_name`, `openfda.generic_name`, `openfda.substance_name`, `openfda.manufacturer_name`, `openfda.product_ndc`.
  - Label sections (arrays of text): `indications_and_usage`, `dosage_and_administration`, `boxed_warning`, `warnings` / `warnings_and_cautions`, `contraindications`, `adverse_reactions`, `drug_interactions`, `pregnancy`, `active_ingredient`, `inactive_ingredient`, `purpose` (OTC). Most sections also have a `<section>_table` field for the tables in that section.
  - Version: `effective_time` (`YYYYMMDD`), `set_id`, `version`; sort with `sort=effective_time:desc` for the newest labels.
- 197 fields, nearly all of them label sections. Test whether a section exists with `_exists_:<section>`, e.g. `_exists_:boxed_warning` (33,440 labels).
- One product has many labels (one per labeler and repackager): `openfda.brand_name:"tylenol"` matches 112. Its `.exact` values keep the label's casing (`Lipitor`, `TYLENOL Extra Strength`, `Tylenol Extra Strength`), so search the plain field and count `openfda.brand_name.exact` to see the variants.
- Label sections are text, so search words in them (`boxed_warning:"liver"`) but don't `count` them.
- `.exact` is case-sensitive and matches the whole value. In drug/label, `openfda.brand_name.exact:"Tylenol"` returns no matches, while plain `openfda.brand_name:"tylenol"` returns 112 labels.
- A misspelled field name returns "No matches found!", the same as a search with no hits. fda_get_dataset adds a hint when a field is not in the table above.
- Counting a date field returns every date in the result, whatever the `limit`. Narrow the search to a date range first.
- Pass `fields` to fda_get_dataset to return only the paths you need, e.g. `fields=["openfda.brand_name", "boxed_warning"]`.
