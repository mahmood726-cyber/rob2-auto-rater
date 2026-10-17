"""Registry evidence *triage* for result-specific human RoB 2 assessment.

A registry alone cannot establish the five RoB 2 domain judgements. No score
or traffic-light judgement is produced, even when metadata appear reassuring.
"""

from __future__ import annotations

import argparse
from datetime import date
import json
from pathlib import Path


def _date(value, field):
    if value is None or value == "":
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field} must be an ISO date string or null")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be an ISO date YYYY-MM-DD") from exc


def triage(record: dict) -> dict:
    if not isinstance(record, dict):
        raise ValueError("Input must be a JSON object")

    # RoB 2 is assessed per result, not once per trial.
    required = ("trial_id", "registry_url", "outcome", "contrast", "timepoint")
    for field in required:
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"{field} is required for attributable result-specific triage")
    reg = _date(record.get("registration_date"), "registration_date")
    start = _date(record.get("first_enrollment_date"), "first_enrollment_date")

    checks = []
    if reg is None or start is None:
        checks.append({
            "name": "registration_timing",
            "status": "unknown",
            "finding": "Registration and enrolment dates insufficient for timing comparison.",
        })
    elif reg > start:
        checks.append({
            "name": "registration_timing",
            "status": "review_flag",
            "finding": "Registry registration date is after first enrolment date; verify historic versions and protocol.",
        })
    else:
        checks.append({
            "name": "registration_timing",
            "status": "context_only",
            "finding": "Registration is not later than recorded first enrolment; this does not establish prespecification.",
        })

    allocation = record.get("allocation")
    if not isinstance(allocation, str) or not allocation.strip():
        checks.append({
            "name": "allocation",
            "status": "unknown",
            "finding": "Registry allocation field unavailable; sequence generation and concealment cannot be assessed.",
        })
    else:
        checks.append({
            "name": "allocation",
            "status": "review_flag" if allocation.strip().lower() != "randomized" else "context_only",
            "finding": (
                f"Registry allocation label: {allocation}; verify actual sequence generation, allocation concealment, "
                "and baseline balance in full reports."
            ),
        })

    masking = record.get("masking")
    checks.append({
        "name": "masking",
        "status": "context_only" if masking else "unknown",
        "finding": (
            f"Registry masking description: {masking}. This does not determine deviations from intended "
            "interventions or outcome-measurement bias."
            if masking else "Masking information unavailable; examine outcome-specific assessor knowledge."
        ),
    })

    checks.extend([
        {
            "name": "missing_outcome_data",
            "status": "human_review_required",
            "finding": "Overall enrolment and registry denominators are not substitutes for outcome-specific missingness, "
                       "reasons and plausible impact of missing data.",
        },
        {
            "name": "selective_reporting",
            "status": "human_review_required",
            "finding": "Compare dated protocol, SAP, registry history and reported analysis for this specific result. "
                       "Current registry text alone cannot establish selective reporting.",
        },
    ])

    return {
        "tool_status": "EVIDENCE_TRIAGE_ONLY",
        "rob2_judgement": None,
        "domain_judgements": None,
        "trial_id": record["trial_id"],
        "result": {
            "outcome": record["outcome"],
            "contrast": record["contrast"],
            "timepoint": record["timepoint"],
        },
        "provenance": {
            "registry_url": record["registry_url"],
            "registry_snapshot_date": record.get("registry_snapshot_date"),
        },
        "checks": checks,
        "next_step": "Two independent trained assessors complete result-specific RoB 2 signalling questions "
                     "using protocol/SAP, full report and supporting documents; adjudicate differences.",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="JSON registry evidence record")
    parser.add_argument("--output", required=True, help="JSON triage report")
    args = parser.parse_args()
    record = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = triage(record)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
