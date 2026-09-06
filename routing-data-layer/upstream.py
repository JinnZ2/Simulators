# SPDX-License-Identifier: CC0-1.0
"""
F6, the load-bearing failure class -- two independently maintained systems
return different routings for the same movement, both wrong. The marker's
inference: that pattern indicates the fault is UPSTREAM of either vendor's
maintenance, so a single-vendor fix cannot close it (RDL-2).

The argument is the `effective-redundancy-audit` / shared-node shape: two
channels marketed as independent, both failing on one input, points to a
shared upstream node (the incomplete source record) rather than two
independent maintenance defects. "Errors in different directions" strengthens
it -- it rules out a common systematic bias and points to a gap each vendor
filled differently.

`upstream_verdict` classifies the pattern; `single_vendor_fix_closes` reports
whether a single vendor can close it. Both are checked in every direction on
CONSTRUCTED cases. Nothing here is a result: no real routing output is read.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

BOTH_CORRECT = "BOTH_CORRECT"
VENDOR_DEFECT = "VENDOR_DEFECT"            # one right, one wrong -> that vendor
UPSTREAM_INCOMPLETE = "UPSTREAM_INCOMPLETE"  # both wrong, different directions
SHARED_BIAS = "SHARED_BIAS"                # both wrong, same direction


def upstream_verdict(truth: float, a: float, b: float,
                     tol: float = 1e-9) -> str:
    """Classify two systems' answers against ground truth.

    - both within tol of truth            -> BOTH_CORRECT
    - exactly one wrong                    -> VENDOR_DEFECT (closable by that
                                              vendor's maintenance)
    - both wrong, opposite sign of error   -> UPSTREAM_INCOMPLETE (the F6
                                              signature: a source gap each
                                              vendor filled differently)
    - both wrong, same sign of error       -> SHARED_BIAS (a common upstream
                                              systematic, also not a single-
                                              vendor fix)
    """
    ea, eb = a - truth, b - truth
    a_wrong, b_wrong = abs(ea) > tol, abs(eb) > tol
    if not a_wrong and not b_wrong:
        return BOTH_CORRECT
    if a_wrong != b_wrong:
        return VENDOR_DEFECT
    # both wrong
    if (ea > 0) != (eb > 0):
        return UPSTREAM_INCOMPLETE
    return SHARED_BIAS


def single_vendor_fix_closes(verdict: str) -> bool:
    """RDL-2: only a lone vendor defect is closable by a single-vendor fix.
    Both-wrong patterns need a source (field-survey) correction upstream."""
    return verdict == VENDOR_DEFECT


if __name__ == "__main__":
    import sys
    sys.stderr.write("upstream.py is a library; its checks live in "
                     "routing-data-layer/selftest_rdl.py.\n")
    sys.exit(2)
