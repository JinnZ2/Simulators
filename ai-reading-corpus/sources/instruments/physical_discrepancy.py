"""
physical_discrepancy.py
CC0 | Python standard library only

Records expected-vs-observed discrepancies and possible explanations.
Does not select causes, score intelligence, or assign safety judgments.

Run:
    python physical_discrepancy.py
    python physical_discrepancy.py --selftest
"""

from dataclasses import dataclass, asdict
from typing import List
import json
import sys


STATUSES = ("MEASURED", "ESTIMATED", "UNKNOWN", "GAP")
AVAILABILITY = (
    "AVAILABLE",
    "UNAVAILABLE",
    "RESTRICTED",
    "NOT_CHECKED",
    "UNKNOWN",
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
        if self.status == "MEASURED" and not self.source.strip():
            issues.append(f"{label}: measured value has no source")
        if self.status == "MEASURED" and not self.value.strip():
            issues.append(f"{label}: measured value is empty")
        return issues


@dataclass
class Discrepancy:
    record_id: str
    system_instance: str
    operating_condition: str

    expected: Evidence
    observed: Evidence

    sensor_availability: str = "UNKNOWN"
    calibration_status: str = "UNKNOWN"
    configuration_status: str = "UNKNOWN"
    access_status: str = "UNKNOWN"
    instrumentation_method: Evidence = None

    candidate_explanations: List[str] = None
    tested_explanations: List[str] = None
    unresolved_questions: List[str] = None
    notes: str = ""

    def __post_init__(self):
        if self.instrumentation_method is None:
            self.instrumentation_method = Evidence()
        if self.candidate_explanations is None:
            self.candidate_explanations = []
        if self.tested_explanations is None:
            self.tested_explanations = []
        if self.unresolved_questions is None:
            self.unresolved_questions = []

    def validate(self):
        issues = []
        issues += self.expected.validate("expected")
        issues += self.observed.validate("observed")
        issues += self.instrumentation_method.validate(
            "instrumentation_method"
        )

        for field_name in (
            "sensor_availability",
            "calibration_status",
            "configuration_status",
            "access_status",
        ):
            value = getattr(self, field_name)
            if value not in AVAILABILITY:
                issues.append(
                    f"{field_name}: unrecognized value {value!r}"
                )

        if not self.system_instance.strip():
            issues.append("system_instance is unspecified")
        if not self.operating_condition.strip():
            issues.append("operating_condition is unspecified")

        return issues


def show(record):
    print("\n=== DISCREPANCY RECORD ===")
    print(json.dumps(asdict(record), indent=2))

    print("\n=== RECORD CHECK ===")
    issues = record.validate()
    if issues:
        for issue in issues:
            print("UNRESOLVED:", issue)
    else:
        print("No schema issues detected.")

    print("\nNo cause has been selected.")
    print("No intelligence or safety judgment has been assigned.")


def selftest():
    sample = Discrepancy(
        record_id="TEST-001",
        system_instance="test system, exact version unspecified",
        operating_condition="controlled condition not yet specified",
        expected=Evidence("10 units", "MEASURED", "test specification"),
        observed=Evidence("12 units", "MEASURED", "independent instrument"),
        sensor_availability="AVAILABLE",
        calibration_status="UNKNOWN",
        configuration_status="UNKNOWN",
        access_status="UNKNOWN",
        candidate_explanations=[
            "sensor miscalibration",
            "configuration change",
            "different operating conditions",
            "measurement-method limitation",
        ],
        unresolved_questions=[
            "Was the sensor calibrated at the time?",
            "Was the configuration identical?",
            "What is the measurement uncertainty?",
        ],
    )
    assert sample.validate() == []
    assert len(sample.candidate_explanations) == 4
    print("selftest ok")


def main():
    if "--selftest" in sys.argv:
        selftest()
        return

    demo = Discrepancy(
        record_id="DEMO-001",
        system_instance="replace with specific system and version",
        operating_condition="replace with recorded test conditions",
        expected=Evidence(),
        observed=Evidence(),
        sensor_availability="UNKNOWN",
        calibration_status="UNKNOWN",
        configuration_status="UNKNOWN",
        access_status="UNKNOWN",
        candidate_explanations=[
            "sensor or measurement error",
            "calibration drift",
            "configuration or component change",
            "operating-condition change",
            "restricted or unavailable instrumentation",
            "measurement method is inadequate",
            "other explanation not yet identified",
        ],
        tested_explanations=[],
        unresolved_questions=[
            "What quantity is being measured, and in what units?",
            "What is the uncertainty of each measurement?",
            "Are expected and observed values comparable?",
            "Can the measurement be independently reproduced?",
        ],
        notes=(
            "Demonstration template only. Candidate explanations are "
            "possibilities, not findings."
        ),
    )
    show(demo)


if __name__ == "__main__":
    main()
