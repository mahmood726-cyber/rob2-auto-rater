# RoB 2 Registry Evidence Triage — prototype

**Publication readiness: NOT READY.** This project currently provides a
deterministic *evidence triage* helper, **not an automated risk-of-bias rater**.
No domain judgement or traffic-light score is generated.

## Why the original approach is not a valid RoB 2 rating

The original proposed rules equated registry attributes with Cochrane RoB 2
domain decisions: “Randomized” with low risk in Domain 1, “Quadruple masking”
with Domain 2, registry enrolment versus denominator counts with Domain 3,
outcome wording with Domain 4, and current registry fields with Domain 5.
These are not adequate proxies.

RoB 2 evaluates a **specific result (outcome, contrast and timepoint)**, not
an entire study in the abstract. It requires result-specific signalling
questions about randomization, deviations, missing data, measurement, and
selection of the reported result, with supporting evidence and justification.
For example, a registry “Randomized” label does not establish allocation
concealment. A quadruple-blind label cannot rule out deviations; comparing
overall enrolment with one outcome denominator may be misleading. A single
current registry record cannot establish pre-specification without dated
history and a protocol/statistical analysis plan.

See Cochrane Handbook Chapter 8:
https://training.cochrane.org/handbook/current/chapter-08

## What this version does

`rob2_triage.py` accepts a user-created JSON evidence record for **one
specific result**. It reports registration-timing flags, allocation and masking
context, and a reminder about data and reporting checks. It returns
`rob2_judgement: null` and `domain_judgements: null`, even if every
registry field looks reassuring. Late registration is a **review flag**,
**not** evidence by itself that a trial has high risk of bias.

It neither fetches registry data nor runs an LLM in this version. Registry
fields supplied by a user have not been independently authenticated.
Source provenance should be independently checked against versioned registry
records, trial reports, protocols and SAPs.

## Quick start

```bash
python rob2_triage.py --input examples/registry_evidence.json --output outputs/triage.json
python -m unittest discover -s tests -v
```

The example is illustrative, not a real RCT.

## Gates before a methods paper or use in reviews

1. Implement the actual official RoB 2 signalling-question workflow and
   outcome-specific evidence/quotation audit trails, with copyright and
   licensing checks on official materials.
2. Develop versioned registry ingestion, historical protocol and SAP retrieval,
   article/full-text linkage, extraction provenance, explicit “not available”
   states and discrepancy adjudication. Do not equate NCT registry metadata
   with true patient-level missingness.
3. Define a preregistered **evaluation**, based on independently double-rated
   reference assessments and adjudicated disagreement, across designs,
   outcomes, interventions and publication eras.
4. Report domain-specific sensitivity, specificity, calibration, error types,
   inter-rater agreement and human review burden with uncertainty intervals.
5. Evaluate ambiguous and adversarial cases, including registration amendments,
   masked trials with allocation failures and timepoint-dependent missingness.
6. Obtain independent methodological review and require a human-in-the-loop
   sign-off before using any proposed judgement in a systematic review.

**No manuscript-level RoB 2 validity or clinical reliability is claimed.**
