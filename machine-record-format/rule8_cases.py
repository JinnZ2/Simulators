# SPDX-License-Identifier: CC0-1.0
"""
Rule 8 test cases A / B / C (v2), each testing a DIFFERENT thing. They are
NOT merged into one validation -- a pass on one is not a pass on the others.

Each case is a `TestCase` carrying the required tests / does_not_test /
why_not triple (transcribed from WORK_ORDER_V2.md), plus a runnable check
that exercises the format machinery. The runnable checks operate on the
FORMAT only: whether the record can hold the case, not whether the
real-world figures are true. The illustrative values in the entries are
CONSTRUCTED and marked so; the real service-life / persistence figures and
the reference marker are carried in the spec, egress-blocked, and not
verified here.

    Case A  Amish barn raising     -> Rule 8 end to end (has a paid control)
    Case B  terra preta            -> the durability column + Rule 7 per column
    Case C  Machu Picchu / mit'a   -> Rule 6, no conversion

Stdlib only. Parses under Python 3.9. CC0.
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import base_entry as be           # noqa: E402
import views as vw                # noqa: E402
import aggregate as ag            # noqa: E402
from test_case import TestCase    # noqa: E402

S = be.State


# ---- Case A: Amish barn raising -- Rule 8 end to end ----------------------

def _run_case_a():
    """Record a community-raised frame and a contract-built structure on
    IDENTICAL footing: same exposure unit, same declared boundary, both with
    measured output, NEITHER carrying a payment field. Then they must sum."""
    boundary = be.Boundary(("frame-raising",), ("site-prep",),
                           "the raising event, not the whole project")
    community = be.write_base_entry(
        entry_id="barn_community", input_state=S("materials", 100.0, "board-ft"),
        output_state=S("service_life", 75.0, "years"), exposure=1200.0,
        exposure_unit="person-hours", joules_in=8.0e8, period="2026",
        observation_method="crew-size x days documented; frame inspectable",
        provenance="constructed", status=be.MEASURED, boundary=boundary,
        release_date="2026-01-01")
    contract = be.write_base_entry(
        entry_id="barn_contract", input_state=S("materials", 100.0, "board-ft"),
        output_state=S("service_life", 60.0, "years"), exposure=900.0,
        exposure_unit="person-hours", joules_in=7.0e8, period="2026",
        observation_method="contractor timesheet; structure inspectable",
        provenance="constructed", status=be.MEASURED, boundary=boundary,
        release_date="2026-01-01")
    reg = vw.ViewRegistry()
    reg.add_view(vw.View("v", "use_class", "auditor", ("", ""),
                         {"barn_community": "ag_structure",
                          "barn_contract": "ag_structure"}))
    res = ag.compute(ag.AggregateSpec("s", "v", ag.SUM), [community, contract],
                     reg, 1)
    summed = res.by_label()["ag_structure"].value
    # a paid/unpaid field cannot be added to either entry
    payment_refused = False
    try:
        be.write_base_entry(entry_id="x", paid=True,
                            input_state=S("a", 1.0, "kg"),
                            output_state=S("b", 1.0, "kg"),
                            exposure_unit="person-hours", period="2026",
                            status=be.MEASURED, joules_in=1.0,
                            boundary=boundary, release_date="2026-01-01")
    except be.PaymentInBasePath:
        payment_refused = True
    return {"both_present": True, "summable_joules": summed,
            "no_payment_field": not be.has_payment_field(),
            "payment_field_refused": payment_refused}


CASE_A = TestCase(
    name="Case A -- Amish barn raising",
    tests="both entries present on identical footing, summable, neither "
          "carrying a payment field (Rule 8 end to end)",
    does_not_test="whether the willingness structure is transferable outside "
                  "a community that already has it; also does not test "
                  "large-scale or non-structural output classes",
    why_not="the community supplying the labor is self-selected and has "
            "standing agreements predating any given raising. The comparison "
            "holds output class constant, not social substrate. It answers "
            "'does the record handle both,' not 'would this work elsewhere.'",
    run=_run_case_a)


# ---- Case B: terra preta -- durability column + Rule 7 per column ----------

def _run_case_b():
    """A strong output figure (persistence) with an ABSENT exposure column.
    The entry must be ACCEPTED (not dropped for want of exposure, and the
    exposure not fabricated), and any efficiency ratio must be
    NOT_COMPUTABLE -- a ratio needs both terms."""
    boundary = be.Boundary(("soil-formation",), ("original-labor",),
                           "the artifact as it persists, not its making")
    terra = be.write_base_entry(
        entry_id="terra_preta",
        input_state=S("substrate", 1.0, "hectare"),
        output_state=S("carbon_persistence", 750.0, "years"),
        exposure=None,                     # absent, not estimated
        exposure_unit="person-hours",
        joules_in=None,
        period="pre-columbian",
        observation_method="present soil carbon / depth / extent measured",
        provenance="constructed", status=be.MEASURED, boundary=boundary,
        release_date="2026-01-01",
        # Rule 7 PER COLUMN: output measured, exposure and joules absent
        column_status={"exposure": be.UNMEASURED_NO_INSTRUMENT,
                       "joules_in": be.UNMEASURED_NO_INSTRUMENT})
    accepted = terra.entry_id == "terra_preta"
    reg = vw.ViewRegistry()
    reg.add_view(vw.View("v", "artifact", "soil scientist", ("", ""),
                         {"terra_preta": "amended_soil"}))
    # an efficiency ratio (joules per exposure) must be NOT_COMPUTABLE
    rate = ag.compute(ag.AggregateSpec("r", "v", ag.RATE, denominator="exposure"),
                      [terra], reg, 1).by_label()["amended_soil"]
    # the output column is readable regardless
    durability = terra.output_state.value
    return {"accepted_with_absent_exposure": accepted,
            "exposure_value_is_none": terra.exposure_value() is None,
            "ratio_flag": rate.flag,
            "durability_readable": durability}


CASE_B = TestCase(
    name="Case B -- terra preta",
    tests="whether the record can carry a strong output figure against an "
          "absent exposure figure without either discarding the entry or "
          "fabricating the exposure",
    does_not_test="output per unit of labor, or any efficiency claim at all",
    why_not="the exposure column is absent. A ratio needs both terms, and "
            "inferring the missing one from the present one makes the ratio "
            "circular. Durability is available; efficiency is not.",
    run=_run_case_b)


# ---- Case C: Machu Picchu / Inca mit'a -- Rule 6, no conversion -----------

def _run_case_c():
    """Labor-unit records ingested and compared WITHOUT conversion to a
    monetary or hour-equivalent common unit. Comparison on the native labor
    unit works; any conversion raises."""
    boundary = be.Boundary(("state-labor-tax",), ("subsistence-labor",),
                           "the mit'a levy as administered")
    a = be.write_base_entry(
        entry_id="terrace_a", input_state=S("slope", 1.0, "hectare"),
        output_state=S("terrace", 1.0, "hectare"), exposure=5000.0,
        exposure_unit="person-hours", joules_in=None, period="inca",
        observation_method="state khipu labor accounting",
        provenance="constructed", status=be.MEASURED, boundary=boundary,
        release_date="2026-01-01",
        column_status={"joules_in": be.UNMEASURED_NO_INSTRUMENT})
    b = be.write_base_entry(
        entry_id="terrace_b", input_state=S("slope", 1.0, "hectare"),
        output_state=S("terrace", 1.0, "hectare"), exposure=4200.0,
        exposure_unit="person-hours", joules_in=None, period="inca",
        observation_method="state khipu labor accounting",
        provenance="constructed", status=be.MEASURED, boundary=boundary,
        release_date="2026-01-01",
        column_status={"joules_in": be.UNMEASURED_NO_INSTRUMENT})
    # compared on the native labor unit -- no conversion needed, same class
    native_total = a.exposure + b.exposure
    convert_raised = False
    try:
        be.convert_exposure(a.exposure, "person-hours", "monetary")
    except be.ExposureConversion:
        convert_raised = True
    return {"compared_on_native_unit": native_total,
            "same_exposure_class": a.exposure_unit == b.exposure_unit,
            "convert_raises": convert_raised}


CASE_C = TestCase(
    name="Case C -- Machu Picchu / Inca mit'a",
    tests="whether labor-unit records can be ingested and compared WITHOUT "
          "conversion to a monetary or hour-equivalent common unit",
    does_not_test="the willingness structure, community capital, or unpaid "
                  "coordination of any kind",
    why_not="mit'a was a labor TAX. Coordination was state-directed and "
            "compulsory. Absence of money is not presence of willingness -- "
            "those are separate axes, and this case is non-monetary and "
            "non-voluntary simultaneously, which is exactly why it isolates "
            "the units question.",
    run=_run_case_c)


CASES = (CASE_A, CASE_B, CASE_C)


if __name__ == "__main__":
    import sys as _s
    _s.stderr.write("rule8_cases.py holds the three cases; their checks run "
                    "in machine-record-format/selftest_mrf.py.\n")
    _s.exit(2)
