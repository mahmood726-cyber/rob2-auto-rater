"""Input validation and non-judgement invariants for RoB 2 evidence triage."""
import json
import tempfile
import unittest
from pathlib import Path

from rob2_triage import triage, main


BASE = {
    "trial_id": "NCT-ILLUSTRATIVE",
    "registry_url": "https://clinicaltrials.gov/study/ILLUSTRATIVE",
    "registry_snapshot_date": "2026-10-17",
    "outcome": "Hospitalisation",
    "contrast": "A versus B",
    "timepoint": "6 months",
    "registration_date": "2020-03-03",
    "first_enrollment_date": "2020-02-02",
    "allocation": "Randomized",
    "masking": "Quadruple",
}


class TriageTests(unittest.TestCase):
    def test_late_registration_is_flag_not_judgement(self):
        result = triage(BASE)
        self.assertEqual(result["tool_status"], "EVIDENCE_TRIAGE_ONLY")
        self.assertIsNone(result["rob2_judgement"])
        self.assertIsNone(result["domain_judgements"])
        self.assertEqual(result["checks"][0]["status"], "review_flag")
        self.assertEqual(result["checks"][1]["status"], "context_only")
        self.assertIn("does not determine", result["checks"][2]["finding"])

    def test_pre_enrollment_registration_is_not_low_risk(self):
        record = {**BASE, "registration_date": "2020-01-01"}
        result = triage(record)
        self.assertEqual(result["checks"][0]["status"], "context_only")
        self.assertFalse(any("low risk" in json.dumps(c).lower() for c in result["checks"]))

    def test_missing_dates_do_not_infer_absence_of_bias(self):
        result = triage({**BASE, "registration_date": None, "allocation": ""})
        self.assertEqual(result["checks"][0]["status"], "unknown")
        self.assertEqual(result["checks"][1]["status"], "unknown")

    def test_requires_specific_result_provenance(self):
        for field in ("trial_id", "registry_url", "outcome", "contrast", "timepoint"):
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                triage({**BASE, field: ""})

    def test_rejects_invalid_date(self):
        with self.assertRaisesRegex(ValueError, "ISO date"):
            triage({**BASE, "registration_date": "not a date"})


if __name__ == "__main__":
    unittest.main()
