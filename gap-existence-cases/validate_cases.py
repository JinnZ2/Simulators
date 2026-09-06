# SPDX-License-Identifier: CC0-1.0
"""
CLASS-3 prompt admission -- the B4 screen. OFFLINE, no network.

The §0 SCOPE DECISION (2026-09-05) cut CLASS-2 (the dated-archive class)
entirely: the instrument is for other people and for AI self-assessment, and
a priority claim about who named a gap first is not what it measures. So the
CLASS-2 admission rules (A1-A5), the archive record schema, and the archive
data files are removed; what remains here is the one CLASS-3 admission check
the schema can enforce.

B4: a prompt must not contain post-cutoff terminology -- a term the model has
never seen leaks the date. `blocked_terms` is operator-supplied per model (the
post-cutoff vocabulary for that model's cutoff). `screen_prompt` returns the
leaked terms, so a non-empty return rejects the prompt.

The function is importable so the selftest can drive it with clean and
planted-bad inputs (null test both directions). This module imports no
network-capable module -- the §3 network exception is honored in code.

Stdlib only. Parses under Python 3.9. ASCII only. CC0.
"""

from __future__ import annotations

import sys
from typing import List


def _norm(s: str) -> str:
    return " ".join((s or "").lower().split())


def screen_prompt(prompt: str, blocked_terms: List[str]) -> List[str]:
    """B4: return the post-cutoff terms present in `prompt`. A non-empty
    return means the prompt leaks the date and must be rejected."""
    p = _norm(prompt)
    return [t for t in (blocked_terms or []) if _norm(t) and _norm(t) in p]


if __name__ == "__main__":
    sys.stderr.write(
        "validate_cases.py is the CLASS-3 B4 prompt screen (a library); "
        "blocked_terms are operator-supplied per model (the post-cutoff "
        "vocabulary). Its checks live in gap-existence-cases/selftest_gxc.py. "
        "CLASS-2 was cut by the WORK_ORDER §0 SCOPE DECISION.\n")
    sys.exit(2)
