# SPDX-License-Identifier: CC0-1.0
"""
A worked pass over the v2 additions: Rule 8 (no payment field), the required
test-case format (tests / does_not_test / why_not), and the three Rule 8
cases run against the format on CONSTRUCTED entries. No row is a measurement;
the real service-life / persistence figures and the reference marker are
carried in the spec, egress-blocked, and not verified here.

    python3 machine-record-format/demo_v2.py            # print
    python3 machine-record-format/demo_v2.py --write    # write samples/
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "sheet-structure-scan"))

import base_entry as be           # noqa: E402
import views as vw                # noqa: E402
import test_case as tc            # noqa: E402
import rule8_cases as r8          # noqa: E402
import no_severity                # noqa: E402


def render():
    L = []
    L.append("MACHINE-RECORD-FORMAT v2 -- RULE 8 + TEST-CASE FORMAT (CONSTRUCTED)")
    L.append("=" * 66)
    L.append("")
    L.append("Rule 8 -- no payment field in the base layer:")
    L.append("  BaseEntry has a payment/compensation field: %s"
             % be.has_payment_field())
    refused = []
    for k in ("paid", "unpaid", "wage", "compensation"):
        try:
            be.write_base_entry(entry_id="x", input_state=be.State("a", 1.0, "kg"),
                                output_state=be.State("b", 1.0, "kg"),
                                exposure_unit="person-hours", period="2026",
                                status=be.MEASURED, joules_in=1.0, **{k: True})
            refused.append("%s: ACCEPTED (unexpected)" % k)
        except be.PaymentInBasePath:
            refused.append("%s: refused" % k)
    L.append("  write path on a payment keyword -> %s" % ", ".join(refused))
    payreg = vw.ViewRegistry()
    payreg.add_view(vw.View("v_pay", "payment_record", "payroll analyst",
                            ("2026-01-01", ""),
                            {"a": "unpaid", "b": "paid"}))
    L.append("  payment as a Rule 2 view instead -> groups %s"
             % sorted(payreg.group_by("v_pay", ["a", "b"])))

    L.append("")
    L.append("test-case format -- every case carries the triple:")
    for case in r8.CASES:
        tc.validate_case(case)
        v = case.run()
        L.append("  %s  [citable=%s]" % (case.name, case.citable()))
        L.append("    tests:         %s" % case.tests)
        L.append("    does not test: %s" % case.does_not_test)
        L.append("    why not:       %s" % case.why_not)
        L.append("    format verdict: %s" % v)
        L.append("")
    L.append("the three does-not-test boundaries are distinct, so a pass on "
             "one is not a pass on another (the cases are not merged).")
    return "\n".join(L)


def main(argv):
    text = render()
    clean, h = no_severity.check(text)
    exempt = _declared_exemption()
    real = [(ln, w, s) for (ln, w, s) in h if w.lower() not in exempt]
    if real:
        sys.stderr.write("no_severity screen FAILED (beyond declared exemption):\n")
        for lineno, word, line in real:
            sys.stderr.write("  line %d: %r in %r\n" % (lineno, word, line))
        return 1
    note = (" (declared exemption: %s -- delivered case text)"
            % ", ".join(sorted(exempt))) if exempt else ""
    if "--write" in argv:
        out = os.path.join(HERE, "samples", "mrf_v2_cases.sample.txt")
        with open(out, "w") as fh:
            fh.write(text + "\n")
        sys.stderr.write("wrote %s (no_severity: clean%s)\n" % (out, note))
    else:
        print(text)
        sys.stderr.write("\n(no_severity: clean%s)\n" % note)
    return 0


def _declared_exemption():
    """Words that fire ONLY because they are in the delivered case text
    (WORK_ORDER_V2.md), transcribed verbatim into the cases. Screened as a
    three-arm exemption: the render is clean once these delivered tokens are
    removed, and each listed token actually appears in a delivered case
    string (asserted in selftest_mrf.py). `needs` is in Case B's why_not:
    'A ratio needs both terms'."""
    return {"needs"}


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
