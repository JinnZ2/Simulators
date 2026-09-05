# SPDX-License-Identifier: CC0-1.0
"""
Test case format -- REQUIRED for every test case in this spec (v2).

Every case carries three fields, not one:

    tests           what a pass establishes
    does_not_test   what a pass does NOT establish
    why_not         the structural reason it cannot reach that

The `does_not_test` field is information of the same class as the positive
result, not a caveat. A positive result gets cited for whatever the citer
needs; an undeclared boundary is filled in by a reader who was not present
when the case was designed, and the case becomes evidence for something it
never established within one citation. So this is Rule 5 -- declared boundary
-- applied to test cases: `validate_case` REFUSES a case missing any of the
three fields, and the refusal message says a case with no `does_not_test`
must not be cited. `why_not` is what makes the boundary auditable rather than
asserted -- it names the property that blocks the wider claim, so a later
reader can check whether a different case WOULD reach it.

Stdlib only. Parses under Python 3.9. CC0.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional


class IncompleteCase(Exception):
    """Raised when a test case is missing tests / does_not_test / why_not.
    Such a case is incomplete and must not be cited."""


@dataclass
class TestCase:
    name: str
    tests: str
    does_not_test: str
    why_not: str
    # an optional runnable check: returns (passed, detail). The three fields
    # above are required whether or not a runnable check is attached -- the
    # boundary declaration is the point, not the automation.
    run: Optional[Callable[[], object]] = None

    def citable(self) -> bool:
        return bool(self.tests and self.does_not_test and self.why_not)


def validate_case(case: TestCase) -> None:
    """Refuse a case that is not citable. A case that establishes X and is
    silent about what it does NOT establish becomes evidence for Y within one
    citation, and the error is then downstream of the record."""
    missing = [f for f in ("tests", "does_not_test", "why_not")
               if not getattr(case, f)]
    if missing:
        raise IncompleteCase(
            "case %r is missing %s; a case with no 'does_not_test' field is "
            "incomplete and must not be cited (this is Rule 5 applied to "
            "test cases)" % (case.name, ", ".join(missing)))


if __name__ == "__main__":
    import sys as _s
    _s.stderr.write("test_case.py is a library; its checks live in "
                    "machine-record-format/selftest_mrf.py.\n")
    _s.exit(2)
