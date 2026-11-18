"""Pins for the section 9c REUSE items (1, 5, 6, 10, 11): repo, commit, path, sha256, anchor.

No logic is copied from the pinned files. resolve() checks a pin against a local checkout of its
repo (commit object present, blob at the path hashes to the pinned sha256, anchor text present);
with no checkout it returns NOT_TESTABLE, never RESOLVED.

Search roots for checkouts: COMBINED_PIN_ROOTS (os.pathsep-separated), else the parent directory
of this repository and that parent's 'jinnz2' subdirectory.
"""
import hashlib
import os
import subprocess
from collections import namedtuple

Pin = namedtuple("Pin", "pin_id item repo commit path sha256 anchor note")

PINS = (
    Pin("P1-taf-unknown-axis", 1, "thermodynamic-accountability-framework",
        "16285cccdd48d608067b9bca50bd6ac683fe860a", "calibration/unified_audit.py",
        "fcccb9af8d8edb01940a09a639be2ff376c53781097b5562f8745a084c368a49",
        "UNKNOWN is deliberately absent (2026-11-11, decided by Kavik)",
        "no composite: UNKNOWN moved off the severity rank onto its own coverage axis"),
    Pin("P5-ladder-shared-ancestry", 5, "formula-audit",
        "4345de69c19429a876f5b16aaf32666a1b00db59", "infer/ladder.py",
        "ef3b9a7ae996f8639345311d0c6e56b102dedf9776d5fb5c5842846e954a01f0",
        "SHARED ANCESTRY  evidence that shares a tag with earlier evidence on the same",
        "branch 5 shared_ancestry tags; the tag set is free-form there, the six categories are ours"),
    Pin("P6-ladder-cross-domain", 6, "formula-audit",
        "4345de69c19429a876f5b16aaf32666a1b00db59", "infer/ladder.py",
        "ef3b9a7ae996f8639345311d0c6e56b102dedf9776d5fb5c5842846e954a01f0",
        "cross_domain evidence must declare its constraints",
        "branch 5 cross_domain rule: every declared constraint matched, else no update"),
    Pin("P6-card-constraint-reasoning", 6, "Simulators",
        "b128fd03cf27d421045f7eb0336133fd319e4626", "reasoning-toolkit/CARDS.md",
        "19535eab9b732a7bc959b0c51fce850f9446010cce1efe1c084b6f0316ee5b93",
        "constraint",
        "constraint-reasoning card (TOOL_CARDS id constraint_reasoning)"),
    Pin("P10-numcheck", 10, "formula-audit",
        "337289d12d81460c8f11265b8e270fdbc0224e58", "numcheck/check.py",
        "f6df0dc196f5ac273f864f1cab1a5a0d6c67fa88eaba53ca822f94412fb7fd83",
        "Fraction intervals",
        "outward-rounded Fraction intervals; TOOL_CARDS pin; identical bytes on main 4345de6"),
    Pin("P11-taf-expiry-register", 11, "thermodynamic-accountability-framework",
        "16285cccdd48d608067b9bca50bd6ac683fe860a", "calibration/expiry_register.py",
        "ddaf2cc5b6539df340ceb84dab98e249d00a5def9f5d9f374a8ff875a04db0ae",
        'EXPIRY_KEYS = ("instrument_class", "sensitivity", "protocol", "provenance")',
        "expiry_condition register; keys differ from cplay ExpiryTrigger (kind, target, condition)"),
    Pin("P11-taf-expiry-field", 11, "thermodynamic-accountability-framework",
        "16285cccdd48d608067b9bca50bd6ac683fe860a", "calibration/unified_audit.py",
        "fcccb9af8d8edb01940a09a639be2ff376c53781097b5562f8745a084c368a49",
        "expiry_condition (VOID allowed). UNKNOWN is not a severity.",
        "the main 16285cc expiry_condition field on coverage entries"),
)

NOT_FOUND = (
    ("item 1", "ai-metrology 'weights not bins'",
     "no repo JinnZ2/ai-metrology reachable; code search for the phrase found no such file; "
     "item 1 rests on P1 and R-A2"),
)

_HEX = set("0123456789abcdef")


def well_formed(p):
    return (len(p.commit) == 40 and set(p.commit) <= _HEX and len(p.sha256) == 64
            and set(p.sha256) <= _HEX and p.path and not p.path.startswith("/") and p.anchor)


def _roots():
    env = os.environ.get("COMBINED_PIN_ROOTS")
    if env:
        return [r for r in env.split(os.pathsep) if r]
    here = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    parent = os.path.dirname(here)
    return [parent, os.path.join(parent, "jinnz2"), here]


def _checkout(repo):
    for root in _roots():
        for cand in (os.path.join(root, repo), os.path.join(root, repo.lower())):
            if os.path.isdir(os.path.join(cand, ".git")):
                return cand
        if os.path.basename(os.path.abspath(root)).lower() == repo.lower() and \
                os.path.isdir(os.path.join(root, ".git")):
            return root
    return None


def resolve(p):
    """RESOLVED / MISMATCH(reason) / NOT_TESTABLE(reason)."""
    co = _checkout(p.repo)
    if co is None:
        return "NOT_TESTABLE", "no local checkout of %s under %s" % (p.repo, os.pathsep.join(_roots()))
    try:
        blob = subprocess.run(["git", "-C", co, "show", "%s:%s" % (p.commit, p.path)],
                              capture_output=True, check=True).stdout
    except subprocess.CalledProcessError:
        return "NOT_TESTABLE", "commit %s not in the local checkout %s (shallow?)" % (p.commit[:7], co)
    got = hashlib.sha256(blob).hexdigest()
    if got != p.sha256:
        return "MISMATCH", "sha256 %s != pinned %s" % (got[:12], p.sha256[:12])
    if p.anchor.encode("utf-8") not in blob:
        return "MISMATCH", "anchor text not found"
    return "RESOLVED", co


def render():
    out = ["pin                           item  repo@commit                                 state"]
    for p in PINS:
        st, why = resolve(p)
        out.append("%-29s %-5s %-43s %s%s" % (p.pin_id, p.item, "%s@%s" % (p.repo, p.commit[:7]),
                                              st, "" if st == "RESOLVED" else " (%s)" % why))
    for item, what, why in NOT_FOUND:
        out.append("NOT_FOUND  %s  %s: %s" % (item, what, why))
    return "\n".join(out)


if __name__ == "__main__":
    print(render())
