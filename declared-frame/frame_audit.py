"""
frame_audit.py -- null-test check_frame.py's comparability verdicts.

CC0-1.0. Standard library only. Deterministic.

THE RULE UNDER TEST
-------------------
`THE_DECLARED_FRAME.md` states one load-bearing rule:

    unpopulated field  -> visible gap, explorable
    omitted field      -> invisible, reads as absence

    "Writing `unknown` costs nothing and preserves the gap as a place
     someone can work. Omitting the field converts an open question into
     a settled one by silence."

So omission is the worse of the two, and the tool should treat it at least
as cautiously as `unknown`.

It does not. In `compare()` a missing core field is read with
`str(a.get(f, ""))`, becomes the empty string, and is compared as a value:

    unknown  ->  UNDETERMINED          open, correct
    omitted  ->  NOT DIRECTLY COMPARABLE   settled

Omission produces the MORE confident verdict. That is the doc's rule
inverted inside the tool the doc ships with.

Two further results below: free-text equality is the whole comparability
test, and the exit code reports block validity rather than comparability.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

import check_frame

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.join(HERE, "check_frame.py")
BASE = os.path.join(HERE, "frames", "panel_conversion.json")

RULE = "=" * 72


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def run_pair(a: dict, b: dict) -> tuple[str, int]:
    d = tempfile.mkdtemp()
    pa, pb = os.path.join(d, "a.json"), os.path.join(d, "b.json")
    with open(pa, "w") as fh:
        json.dump({"frame": a}, fh)
    with open(pb, "w") as fh:
        json.dump({"frame": b}, fh)
    r = subprocess.run([sys.executable, TOOL, pa, pb],
                       capture_output=True, text=True)
    return r.stdout, r.returncode


def verdict(out: str) -> str:
    for line in out.splitlines():
        t = line.strip()
        for tag in ("DIRECTLY COMPARABLE on all", "NOT DIRECTLY COMPARABLE",
                    "UNDETERMINED"):
            if t.startswith(tag):
                return tag
    return "(none)"


def base_frame() -> dict:
    with open(BASE) as fh:
        return json.load(fh)["frame"]


# ---------------------------------------------------------------------------

def check_omitted_vs_unknown() -> None:
    section("1  omission produces a MORE confident verdict than unknown")

    base = base_frame()

    omitted = dict(base)
    omitted.pop("horizon")
    unknown = dict(base)
    unknown["horizon"] = "unknown"

    out_o, rc_o = run_pair(base, omitted)
    out_u, rc_u = run_pair(base, unknown)

    print("  core field `horizon` on side B:\n")
    print("    %-12s %-28s rc %d" % ("omitted", verdict(out_o), rc_o))
    print("    %-12s %-28s rc %d" % ("'unknown'", verdict(out_u), rc_u))
    print()
    print("  The doc: omission 'converts an open question into a settled one")
    print("  by silence'. The tool does exactly that -- it settles it, and")
    print("  reports NOT COMPARABLE where the same gap declared as `unknown`")
    print("  correctly reports UNDETERMINED.")
    print()
    print("  Mechanism: compare() reads `str(a.get(f, \"\")).strip()`, so a")
    print("  missing field becomes \"\" and is compared as a value. The")
    print("  unknown branch is checked first and never reached.")
    print()
    print("  Fix, three lines: treat a missing core field as undetermined,")
    print("  labelled as omitted rather than declared, so the block-level")
    print("  OMITTED finding and the comparability verdict agree.")


def check_free_text() -> None:
    section("2  comparability is string equality on free text")

    base = base_frame()
    reworded = dict(base)
    reworded["boundary"] = base["boundary"].replace(
        "photon capture to product only", "only photon capture to product")

    out, rc = run_pair(base, reworded)
    print("  same boundary, two orderings of the same clause:\n")
    print("    A: %s..." % base["boundary"][:52])
    print("    B: %s..." % reworded["boundary"][:52])
    print()
    print("    verdict  %s   rc %d" % (verdict(out), rc))
    print()
    print("  This is the inverse of the failure in")
    print("  ../measurement-fork/: there a token classifier OVER-matched and")
    print("  marked questions covered that no probe reached. Here exact")
    print("  equality UNDER-matches and marks frames different that are the")
    print("  same.")
    print()
    print("  Under-matching is the safer direction -- refusing a comparison")
    print("  costs less than licensing a wrong one. But the tool has no band")
    print("  for it. Two frames differing as written get NOT DIRECTLY")
    print("  COMPARABLE, which reads as a substantive difference rather than")
    print("  as an unresolved one.")
    print()
    print("  There is no string fix. Whether two free-text boundaries denote")
    print("  the same accounting is a judgement, and the honest verdict for")
    print("  differing text is the one the doc already uses elsewhere: not")
    print("  resolved here.")


def check_exit_code() -> None:
    section("3  the exit code reports block validity, not comparability")

    base = base_frame()
    with open(os.path.join(HERE, "frames", "leaf_conversion.json")) as fh:
        other = json.load(fh)["frame"]

    incomparable, rc_inc = run_pair(base, other)
    broken = dict(base)
    broken.pop("horizon")
    _, rc_broken = run_pair(base, broken)

    print("  two complete blocks, genuinely different frames")
    print("    verdict  %-28s rc %d" % (verdict(incomparable), rc_inc))
    print()
    print("  one block missing a field")
    print("    rc %d" % rc_broken)
    print()
    print("  So rc tracks whether the BLOCKS are well-formed, not whether the")
    print("  results compare. That is defensible -- incomparability is a")
    print("  finding, not an error -- and it is undocumented. A caller")
    print("  scripting `check_frame.py a b && use_both` gets a pass on two")
    print("  results the tool has just said do not compare.")
    print()
    print("  Either document rc, or add a distinct code for")
    print("  NOT-COMPARABLE so the verdict is scriptable.")


def check_what_works() -> None:
    section("4  what the block does that nothing else here does")

    base = base_frame()
    print("  The six fields are not interchangeable. Three are compared")
    print("  (boundary, horizon, who_counts); logic is reported as a")
    print("  separate mismatch; sign_source and observer_access are")
    print("  recorded and not compared at all.\n")

    print("  %-18s %s" % ("field", "role in compare()"))
    print("  " + "-" * 52)
    for f in check_frame.FIELDS:
        if f in check_frame.CORE:
            role = "core -- must match"
        elif f == "logic":
            role = "separate mismatch line"
        else:
            role = "recorded, never compared"
        print("  %-18s %s" % (f, role))
    print()
    print("  That split is right and is worth stating. sign_source and")
    print("  observer_access are not comparability conditions -- two results")
    print("  can share a boundary and disagree about which direction is")
    print("  better, and that disagreement is legible precisely because both")
    print("  declared it.")
    print()
    print("  On the worked pair the block does its job: the panel/leaf")
    print("  comparison differs on all three core fields, so the efficiency")
    print("  ratio between them is a frame difference reported as a finding.")
    print("  That is the VOID RATIO check from ../measurement-fork/ arriving")
    print("  by a different route -- a closed budget over an open one.")


def main() -> None:
    print()
    print("NULL-TESTING THE COMPARABILITY VERDICTS")
    print("subject: check_frame.py compare(), on frames/panel_conversion.json")

    check_omitted_vs_unknown()
    check_free_text()
    check_exit_code()
    check_what_works()

    section("READING")
    print("""
  The block is the contribution and it holds. Six declared fields, three
  of them comparability conditions, and UNKNOWN as a legal value are all
  load-bearing and all correct.

  The checker inverts the one rule the doc calls load-bearing. Omission is
  supposed to be worse than `unknown`; in compare() it produces the more
  confident verdict, because a missing field is read as the empty string
  and compared as a value. Three lines.

  Comparability is exact string equality on free text. That under-matches,
  which is the safe direction, and there is no band for it -- two frames
  that differ only in wording get a verdict that reads as substantive.
  There is no string fix; the honest output for differing text is the
  not-resolved-here the doc already uses for its own middle band.

  The exit code reports whether the blocks are well-formed, not whether
  the results compare, and does not say so.
""")


if __name__ == "__main__":
    main()
