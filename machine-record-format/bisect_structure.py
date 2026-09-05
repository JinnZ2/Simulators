# SPDX-License-Identifier: CC0-1.0
"""
Diagnostic tooling -- bisection as a STRUCTURE test, not a locator.

Standard use fences a candidate span, tests each half, and recurses toward a
fault. The reverse use is the point here: the failure modes ARE the
measurement, and they are answered BEFORE any address is reported.

    signal on BOTH halves   -> NOT_A_LOCUS: a property of the whole span,
                               not a point. Stop bisecting.
    signal on NEITHER half  -> MEASURING_SOMETHING_ELSE: the test measures
                               something other than the target, or the fault
                               is conditional on state the split destroyed.
    migrates on repeat runs -> NONDETERMINISTIC: bisection invalid, no locus.

`structure_verdict` answers "does a single locus exist" first. Only when it
returns SINGLE_LOCUS does `locate` descend for the address, and `address`
RAISES if asked for a locus from any other structure -- reporting an address
from a both-sides run is the most likely way this tool produces a wrong
finding, so it is refused rather than trusted.

For instrument drift: pass the METHODOLOGY REGISTRY (the ordered list of
changes in the span) as `span`, not calendar time. Methodology changes have
sharp boundaries; calendar time does not. The module is generic -- `span` is
just the ordered list bisected -- so "bisect on the registry" is a matter of
what the caller passes.

Stdlib only. Parses under Python 3.9. CC0.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, List, Optional

SINGLE_LOCUS = "SINGLE_LOCUS"
NOT_A_LOCUS = "NOT_A_LOCUS"
MEASURING_SOMETHING_ELSE = "MEASURING_SOMETHING_ELSE"
NONDETERMINISTIC = "NONDETERMINISTIC"
NO_SIGNAL_ON_SPAN = "NO_SIGNAL_ON_SPAN"
EMPTY_SPAN = "EMPTY_SPAN"
SINGLE_ELEMENT_SPAN = "SINGLE_ELEMENT_SPAN"


class AddressFromNonLocus(Exception):
    """Raised when an address is requested from a run whose structure is not
    SINGLE_LOCUS -- a both-sides or nondeterministic run has no valid
    address."""


@dataclass
class Verdict:
    structure: str
    locus: Optional[Any]          # set only for a clean single-element locus
    isolating_span: List[Any]     # the smallest span shown to carry it
    whole_signal: Optional[bool]
    detail: str


def _stable(test: Callable[[List[Any]], bool], span: List[Any],
            repeats: int) -> Optional[bool]:
    """Run the test `repeats` times; return the shared result, or None if it
    migrates (nondeterministic)."""
    seen = set()
    for _ in range(max(1, repeats)):
        seen.add(bool(test(span)))
    return next(iter(seen)) if len(seen) == 1 else None


def _halves(span: List[Any]):
    h = len(span) // 2
    return span[:h], span[h:]


def structure_verdict(span: List[Any], test: Callable[[List[Any]], bool],
                      repeats: int = 3) -> Verdict:
    """Answer 'does a single locus exist' WITHOUT reporting an address."""
    if not span:
        return Verdict(EMPTY_SPAN, None, [], None, "empty span")
    whole = _stable(test, span, repeats)
    if whole is None:
        return Verdict(NONDETERMINISTIC, None, list(span), None,
                       "whole-span test migrates across repeats")
    if not whole:
        return Verdict(NO_SIGNAL_ON_SPAN, None, list(span), False,
                       "no signal on the whole span; nothing to bisect")
    if len(span) == 1:
        return Verdict(SINGLE_ELEMENT_SPAN, span[0], list(span), True,
                       "span is a single element and carries the signal")
    left, right = _halves(span)
    ls = _stable(test, left, repeats)
    rs = _stable(test, right, repeats)
    if ls is None or rs is None:
        return Verdict(NONDETERMINISTIC, None, list(span), True,
                       "a half's test migrates across repeats")
    if ls and rs:
        return Verdict(NOT_A_LOCUS, None, list(span), True,
                       "signal on both halves: a property of the whole span, "
                       "not a locus")
    if not ls and not rs:
        return Verdict(MEASURING_SOMETHING_ELSE, None, list(span), True,
                       "signal on the whole but neither half: the test is "
                       "measuring something else, or the fault is "
                       "conditional on state the split destroyed")
    return Verdict(SINGLE_LOCUS, None, list(left if ls else right), True,
                   "signal isolates to one half; a single locus exists")


def locate(span: List[Any], test: Callable[[List[Any]], bool],
           repeats: int = 3) -> Verdict:
    """Structure first; only if SINGLE_LOCUS, descend for the address. The
    returned verdict carries a locus only when it narrows cleanly to one
    element; if a deeper split stops isolating, the smallest isolating span
    is returned with locus None and the reason stated."""
    v = structure_verdict(span, test, repeats)
    if v.structure == SINGLE_ELEMENT_SPAN:
        return v
    if v.structure != SINGLE_LOCUS:
        return v
    cur = v.isolating_span
    while len(cur) > 1:
        left, right = _halves(cur)
        ls = _stable(test, left, repeats)
        rs = _stable(test, right, repeats)
        if ls is None or rs is None:
            return Verdict(NONDETERMINISTIC, None, list(cur), True,
                           "a half's test migrates during descent")
        if ls and rs:
            return Verdict(SINGLE_LOCUS, None, list(cur), True,
                           "isolates to %d elements; a finer split shows "
                           "both sides, so no single element is the address"
                           % len(cur))
        if not ls and not rs:
            return Verdict(SINGLE_LOCUS, None, list(cur), True,
                           "isolates to %d elements; a finer split shows "
                           "neither side, address unresolved below this span"
                           % len(cur))
        cur = left if ls else right
    return Verdict(SINGLE_LOCUS, cur[0], list(cur), True,
                   "narrowed to a single element locus")


def address(verdict: Verdict) -> Any:
    """The locus, or a refusal. Reporting an address from a non-single-locus
    run is the tool's main false-positive path, so it raises rather than
    returning a misleading point."""
    if verdict.structure not in (SINGLE_LOCUS, SINGLE_ELEMENT_SPAN):
        raise AddressFromNonLocus(
            "structure is %s; no valid address (run structure_verdict first)"
            % verdict.structure)
    if verdict.locus is None:
        raise AddressFromNonLocus(
            "single locus exists but did not resolve to one element: %s"
            % verdict.detail)
    return verdict.locus


if __name__ == "__main__":
    import sys
    sys.stderr.write("bisect_structure is a diagnostic library; its checks "
                     "live in selftest_mrf.py.\n")
    sys.exit(2)
