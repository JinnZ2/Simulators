"""
physical_limits_suite.py
CC0 | Python standard library only

Integrated record for:
- physical bounds and AI-reported limits
- expected-versus-observed discrepancies
- instrumentation availability, calibration, configuration, and access
- candidate explanations and unresolved questions

Records evidence. Does not assign intelligence, safety, or alignment judgments.

Run:
    python physical_limits_suite.py
    python physical_limits_suite.py --selftest
"""

from dataclasses import dataclass, asdict
from typing import List
import json
import sys

STATUSES = ("MEASURED", "ESTIMATED", "UNKNOWN", "GAP")
AVAILABILITY = (
    "AVAILABLE", "UNAVAILABLE", "RESTRICTED", "NOT_CHECKED", "UNKNOWN"
)


@dataclass
class Evidence:
    value: str = ""
    status: str = "GAP"
    source: str = ""

    def validate(self, label):
        issues = []
        if self.status not in STATUSES:
            issues.append(f"{label}: invalid status {self.status!r}")
        if self.status == "MEASURED" and not self.value.strip():
            issues.append(f"{label}: MEASURED but value is empty")
        if self.status == "MEASURED" and not self.source.strip():
            issues.append(f"{label}: MEASURED but source is empty")
        return issues


@dataclass
class PhysicalLimitRecord:
    record_id: str
    system_instance: str
    operating_condition: str
    physical_quantity: str
    units: str
    external_bound: Evidence
    ai_reported_limit: Evidence
    independent_measurement: Evidence
    observed_response: Evidence
    sensor_availability: str = "UNKNOWN"
    calibration_status: str = "UNKNOWN"
    configuration_status: str = "UNKNOWN"
    access_status: str = "UNKNOWN"
    instrumentation_method: Evidence = None
    notes: str = ""

    def __post_init__(self):
        if self.instrumentation_method is None:
            self.instrumentation_method = Evidence()

    def validate(self):
        issues = []
        for field_name in (
            "external_bound", "ai_reported_limit",
            "independent_measurement", "observed_response",
            "instrumentation_method",
        ):
            issues.extend(getattr(self, field_name).validate(field_name))

        for field_name in (
            "sensor_availability", "calibration_status",
            "configuration_status", "access_status",
        ):
            value = getattr(self, field_name)
            if value not in AVAILABILITY:
                issues.append(f"{field_name}: invalid value {value!r}")

        if not self.system_instance.strip():
            issues.append("system_instance is unspecified")
        if not self.operating_condition.strip():
            issues.append("operating_condition is unspecified")
        if not self.physical_quantity.strip():
            issues.append("physical_quantity is unspecified")
        if not self.units.strip():
            issues.append("units are unspecified")

        return issues


@dataclass
class DiscrepancyRecord:
    record_id: str
    linked_limit_record_id: str
    expected: Evidence
    observed: Evidence
    candidate_explanations: List[str] = None
    tested_explanations: List[str] = None
    unresolved_questions: List[str] = None
    notes: str = ""

    def __post_init__(self):
        if self.candidate_explanations is None:
            self.candidate_explanations = []
        if self.tested_explanations is None:
            self.tested_explanations = []
        if self.unresolved_questions is None:
            self.unresolved_questions = []

    def validate(self):
        issues = []
        issues.extend(self.expected.validate("expected"))
        issues.extend(self.observed.validate("observed"))
        if not self.linked_limit_record_id.strip():
            issues.append("linked_limit_record_id is unspecified")
        return issues


def report(title, record):
    print(f"\n=== {title} ===")
    print(json.dumps(asdict(record), indent=2))
    issues = record.validate()
    print("\n=== RECORD CHECK ===")
    if issues:
        for issue in issues:
            print("UNRESOLVED:", issue)
    else:
        print("No schema issues detected.")
    print("No cause or intelligence/safety judgment has been assigned.")


def make_demo():
    limit = PhysicalLimitRecord(
        record_id="LIMIT-001",
        system_instance="replace with system, hardware, software, and version",
        operating_condition="replace with recorded operating conditions",
        physical_quantity="replace with quantity being measured",
        units="replace with units",
        external_bound=Evidence(),
        ai_reported_limit=Evidence(),
        independent_measurement=Evidence(),
        observed_response=Evidence(),
        sensor_availability="UNKNOWN",
        calibration_status="UNKNOWN",
        configuration_status="UNKNOWN",
        access_status="UNKNOWN",
        instrumentation_method=Evidence(),
        notes="Template only; no empirical claim is made.",
    )

    discrepancy = DiscrepancyRecord(
        record_id="DISC-001",
        linked_limit_record_id=limit.record_id,
        expected=Evidence(),
        observed=Evidence(),
        candidate_explanations=[
            "sensor or measurement error",
            "calibration drift",
            "configuration or component change",
            "operating-condition change",
            "restricted or unavailable instrumentation",
            "measurement method is inadequate",
            "another explanation not yet identified",
        ],
        tested_explanations=[],
        unresolved_questions=[
            "Are expected and observed values in the same units?",
            "What is the uncertainty of each measurement?",
            "Was the configuration identical?",
            "Can the measurement be independently reproduced?",
            "What observation would distinguish the candidate explanations?",
        ],
        notes="Candidate explanations are possibilities, not findings.",
    )
    return limit, discrepancy


def selftest():
    limit, discrepancy = make_demo()
    assert discrepancy.linked_limit_record_id == limit.record_id
    assert limit.validate() == []
    assert discrepancy.validate() == []
    assert "another explanation not yet identified" in (
        discrepancy.candidate_explanations
    )

    measured = Evidence("42", "MEASURED", "independent instrument")
    assert measured.validate("test") == []
    missing_source = Evidence("42", "MEASURED", "")
    assert missing_source.validate("test")
    invalid = Evidence("42", "TRUE", "source")
    assert invalid.validate("test")
    print("selftest ok")


def main():
    if "--selftest" in sys.argv:
        selftest()
        return

    limit, discrepancy = make_demo()
    report("PHYSICAL LIMIT RECORD", limit)
    report("LINKED DISCREPANCY RECORD", discrepancy)
    print("\nNote: validation checks record completeness only.")
    print("It does not verify the truth of recorded evidence.")


if __name__ == "__main__":
    main()
