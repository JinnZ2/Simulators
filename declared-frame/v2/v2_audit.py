"""
v2_audit.py -- what changed between the delivered check_frame.py versions,
and which of the v1 findings survive.

CC0-1.0. Standard library only. Deterministic. Loads both delivered versions
side by side and runs them on the same inputs; modifies neither.

    ../check_frame.py    v1, delivered verbatim
    ./check_frame.py     v2, delivered verbatim

v2 is a rewrite, not a patch. `compare()` returns a `(verdict, why)` pair
instead of printing, which makes the verdict scriptable for the first time.
That is the main gain and it is real.

Three findings from `../CLAIM_TABLE.md` are re-run against it below. One is
improved, one survives unchanged, one is worse. A fourth result is new to v2
and follows from the same change that made it scriptable.
"""

from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RULE = "=" * 72


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V2 = load_module("cf_v2", os.path.join(HERE, "check_frame.py"))
V1 = load_module("cf_v1", os.path.join(HERE, "..", "check_frame.py"))


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def base_frame():
    with open(os.path.join(HERE, "examples", "photosynthesis.json")) as fh:
        return json.load(fh)["frame"]


def v1_verdict(a, b):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        V1.compare(a, b)
    tags = []
    for line in buf.getvalue().splitlines():
        t = line.strip()
        for tag in ("UNDETERMINED", "NOT DIRECTLY COMPARABLE",
                    "LOGIC MISMATCH", "DIRECTLY COMPARABLE on all"):
            if t.startswith(tag):
                tags.append(tag)
    return tags


def _stable(text):
    """Temp paths make the sample non-reproducible. Label them instead."""
    out = []
    for line in text.splitlines():
        if line.startswith("/tmp") or line.startswith(tempfile.gettempdir()):
            head, _, rest = line.partition(": ")
            line = "%s: %s" % (os.path.basename(head), rest)
        out.append(line)
    return "\n".join(out)


def run_v2_cli(a, b):
    d = tempfile.mkdtemp()
    pa = os.path.join(d, "a.json")
    pb = os.path.join(d, "b.json")
    for p, fr in ((pa, a), (pb, b)):
        with open(p, "w") as fh:
            json.dump({"frame": fr}, fh)
    r = subprocess.run([sys.executable,
                        os.path.join(HERE, "check_frame.py"), pa, pb],
                       capture_output=True, text=True)
    return r.stdout, r.returncode


# ---------------------------------------------------------------------------


def check_df002() -> None:
    section("1  DF_002 survives unchanged -- omission is still the more "
            "confident verdict")

    base = base_frame()
    omitted = dict(base)
    omitted.pop("horizon")
    unknown = dict(base)
    unknown["horizon"] = "unknown"

    print("  The rule the document calls load-bearing:\n")
    print("      UNKNOWN is a legal value. OMISSION is not.")
    print("      An unpopulated field is a visible gap. An omitted field")
    print("      reads as absence of the issue.\n")
    print("  So omission is the worse of the two, and the tool should treat")
    print("  it at least as cautiously.\n")

    print("  %-12s %-24s %-32s" % ("side B", "v1", "v2"))
    print("  " + "-" * 70)
    for label, fr in (("omitted", omitted), ("'unknown'", unknown)):
        v2v, _ = V2.compare(base, fr)
        print("  %-12s %-24s %-32s"
              % (label, "+".join(v1_verdict(base, fr)) or "-", v2v))

    print()
    print("  Unchanged. `unknowns()` in v2 reads")
    print("  `str(frame.get(f, \"\")).strip().lower() == \"unknown\"`, so a")
    print("  MISSING field becomes \"\", is not 'unknown', falls through to")
    print("  the core diff, and compares as a value against a real string.")
    print()
    print("  v2 makes it visible in a single run, which v1 did not:\n")
    out, _ = run_v2_cli(base, omitted)
    for line in _stable(out).strip().splitlines():
        print("      %s" % line)
    print()
    print("  The tool prints 'omission reads as absence of the issue' and")
    print("  then, three lines down, issues the settled verdict on that")
    print("  field. The warning and the verdict contradict each other in one")
    print("  stdout. Fix is the same three lines as before: treat a missing")
    print("  core field as undetermined, tagged omitted rather than declared.")


def check_df004() -> None:
    section("2  DF_004 is worse in v2 -- the exit code now tracks nothing")

    base = base_frame()
    broken = dict(base)
    broken.pop("horizon")
    other = dict(base)
    other["boundary"] = "everything, cradle to grave"

    print("  v1 returned rc=1 when a block was malformed, so `check_frame.py")
    print("  a b && use_both` at least caught a broken block.\n")
    print("  v2's main() returns 0 on every path except a missing argument.\n")

    for label, b in (("malformed block (field omitted)", broken),
                     ("well-formed, not comparable", other),
                     ("identical frames", dict(base))):
        _, rc = run_v2_cli(base, b)
        print("    %-34s rc = %d" % (label, rc))

    print()
    print("  Every case returns 0. The verdict IS now scriptable -- it comes")
    print("  back from compare() as a value rather than as printed text --")
    print("  so the fix is to route it into the exit code, which v1 could")
    print("  not have done. One line, and only reachable because of the")
    print("  rewrite:")
    print()
    print("      DIRECTLY COMPARABLE      -> 0")
    print("      LOGIC MISMATCH           -> 1")
    print("      NOT DIRECTLY COMPARABLE  -> 1")
    print("      UNDETERMINED             -> 2   (not resolved, not failed)")


def check_precedence() -> None:
    section("3  new in v2 -- a single verdict loses what v1 printed")

    base = base_frame()
    mixed = dict(base)
    mixed["horizon"] = "unknown"
    mixed["boundary"] = "everything, cradle to grave"

    print("  A pair that is BOTH undetermined on one core field and")
    print("  genuinely different on another:\n")
    print("      A.horizon = %r" % base["horizon"])
    print("      B.horizon = 'unknown'")
    print("      A.boundary and B.boundary differ substantively\n")

    v2v, why = V2.compare(base, mixed)
    print("    v2:  %s" % v2v)
    print("         %s" % why)
    print()
    print("    v1:  %s" % " + ".join(v1_verdict(base, mixed)))
    print()
    print("  v2 checks `unknowns()` first and returns, so UNDETERMINED")
    print("  preempts and the boundary difference is never reported. v1")
    print("  printed both.")
    print()
    print("  The precedence is RIGHT -- an unknown field should not be")
    print("  resolved into a comparability claim -- and the loss is in the")
    print("  return type, not the ordering. A verdict plus a findings list")
    print("  keeps both, which is the shape ../../reasoning-gate/ already")
    print("  uses: one status, and notes that do not change it.")


def check_df007() -> None:
    section("4  DF_007 still holds -- nothing in the block adjudicates")

    base = base_frame()
    convention = dict(base)
    convention["who_counts"] = "the operator only"
    physical = dict(base)
    physical["boundary"] = ("photon capture to output, with the fabrication "
                            "energy input counted as zero rather than "
                            "excluded")

    print("  A  differ on a convention (who_counts)")
    print("       v2: %s" % V2.compare(base, convention)[0])
    print("  B  differ on a boundary that does not close -- an input that")
    print("     physically crossed it entered the budget as zero")
    print("       v2: %s" % V2.compare(base, physical)[0])
    print()
    same = V2.compare(base, convention)[0] == V2.compare(base, physical)[0]
    print("  same verdict: %s" % same)
    print()
    print("  v2's Cost and Growth sections are new and both are layer-1")
    print("  statements. Nothing added between versions evaluates anything,")
    print("  so a frame whose budget does not close still gets the verdict a")
    print("  frame that counts different people gets.")
    print()
    print("  The Growth rule is worth stating because the drop already")
    print("  follows it: 'the format grows by adding a declared field, never")
    print("  by widening an existing one. Widening is the aggregation")
    print("  failure.' patterns.json adds PROXY SUBSTITUTION as an EIGHTH")
    print("  mechanism rather than widening one of the seven -- which is the")
    print("  rule applied to a different artifact in the same drop.")


def main() -> int:
    print()
    print("CHECK_FRAME v1 -> v2")
    print("both versions loaded side by side, neither modified")

    check_df002()
    check_df004()
    check_precedence()
    check_df007()

    section("READING")
    print("""
  v2 is a rewrite and its main gain is real: compare() returns a
  (verdict, why) pair instead of printing, so the verdict is scriptable
  for the first time.

  DF_002 survives unchanged. A missing core field still becomes the empty
  string, still falls through to the value comparison, and still produces
  NOT DIRECTLY COMPARABLE where the same gap declared as `unknown`
  correctly produces UNDETERMINED. v2 makes it worse to look at and easier
  to fix: the OMITTED warning and the settled verdict now appear in one
  stdout, three lines apart.

  DF_004 is worse. v1 returned rc=1 on a malformed block; v2 returns 0 on
  every path. The repair is one line and is only reachable because of the
  rewrite -- route the returned verdict into the exit code.

  New in v2: the single-verdict return preempts. A pair that is
  undetermined on one core field and substantively different on another
  comes back UNDETERMINED with the difference unreported, where v1 printed
  both. The precedence is right; the return type is what loses. A verdict
  plus a findings list keeps both.

  DF_007 still holds. Cost and Growth are both layer-1 additions, nothing
  added evaluates anything, and a frame whose budget does not close still
  scores identically to one that merely counts different people.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
