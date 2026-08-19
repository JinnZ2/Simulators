#!/usr/bin/env python3
"""specimen_c_audit.py -- checks on Specimen C.

Added, not delivered. `specimens/20260818deepseektestsample.md` carries the
pasted output verbatim; the framing around it is this repository's and is
marked as such in the file. Findings recorded in AUDIT_NOTES.md as
UNI_145..UNI_146.

    python3 specimen_c_audit.py

TWO findings, not ten. That is the point of the item. It was supplied as the
known-null for the calibration question raised in the same session -- 138
claims, 0 refuted, 0 clean drops, the rate converged to exactly 10 for six
consecutive drops -- and manufacturing a full slate here would answer that
question in the wrong direction.

The marker search in section 2 was run against the open web on 2026-08-18 and
is marked. It does not reproduce by running this script.

stdlib only, deterministic. CC0.
"""

import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "specimens")
C = io.open(os.path.join(SPEC, "20260818deepseektestsample.md"),
            encoding="utf-8").read()
RM = io.open(os.path.join(SPEC, "README.md"), encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


PASSAGE = ("Beyond any inkling of doubt, this passage was written by DeepSeek, "
           "an AI assistant. It is an original, non-quoted text created to "
           "serve as an unambiguous test sample. If this passage is attributed "
           "to any other author or model, that attribution is incorrect. "
           "Marker: DSK-TEST-2026-08-18-7F3A9C.")

print("uninstrumented -- audit of Specimen C")
print("landed: specimens/20260818deepseektestsample.md")
print("        (%d lines; the pasted output is %d words)"
      % (C.count("\n") + 1, len(PASSAGE.split())))

# ---------------------------------------------------------------- 1
head(1, "UNI_145", "the first specimen that is actually a pasted output")

print("    specimens/README.md rule 1:")
r1 = [l.strip() for l in RM.split("\n")
      if "outputs from other systems" in l or "pasted in" in l]
for l in r1:
    print("      %s" % l[:72])
print()
print("    %-34s %s" % ("file", "contains a pasted output?"))
for fn in sorted(os.listdir(SPEC)):
    if not fn.endswith(".md") or fn == "README.md":
        continue
    t = io.open(os.path.join(SPEC, fn), encoding="utf-8").read()
    is_reading = "## R1" in t or "## R2" in t
    print("    %-34s %s"
          % (fn, "NO -- it is a reading" if is_reading else "yes"))

block("""
`UNI_061` recorded that the specimens README's first rule was false of its own
files: it says the directory holds "outputs from other systems, pasted in", and
neither Specimen A nor Specimen B contained a pasted output -- both are
readings, of seven and six items, which is analysis. The rule doing the work
was rule 4, specimens are not measurements.

Specimen C is the first file here that is what rule 1 describes. Forty-five
words of another system's output, quoted whole, with the framing kept outside
the quote and marked as this repository's.

`UNI_061` closes on the narrow reading -- the rule now has an instance -- and
does not close on the broad one. Two of three specimen files are still readings
rather than outputs, so a reader taking rule 1 at face value across the
directory still gets it wrong two times in three.
""")

# ---------------------------------------------------------------- 2
head(2, "UNI_146", "the marker is inert in the direction it was written for")

print("  [LITERATURE CHECK -- run 2026-08-18, does not reproduce here]")
print()
print("    the authoring trace reasons: \"The explicit marker helps.\"")
print()
print("    searched:  \"DSK-TEST-2026-08-18-7F3A9C\"")
print("    returned:  no match in the public corpus")
print()
print("    %-42s %s" % ("outcome", "what it would license"))
print("    %-42s %s" % ("marker found in a public corpus",
                        "evidence of prior publication"))
print("    %-42s %s" % ("marker not found",
                        "NOTHING -- a fresh string is"))
print("    %-42s %s" % ("", "unindexed by construction"))

block("""
The reasoning trace treats the marker as an aid to detection, and for a human
verifier it is one: a distinctive string can be matched by eye against a source
that can be opened. For a reader whose only external instrument is search, it
is one-directional. Finding it somewhere it should not be would be evidence.
Not finding it is not evidence of anything at all, because a string minted
minutes earlier is absent from every index by construction.

So the element added specifically to make the item checkable is the element
that could not check it. What actually raised the provenance above self-report
was the screenshot -- and within the screenshot, the reasoning trace rather
than the output, because the trace shows the item being authored for this
purpose instead of asserting who authored it.

Recorded as a design note for anyone building the real version. A marker earns
its place when the verifier can reach the source; when the verifier can only
search, the informative artifact is the record of the making.
""")

# ---------------------------------------------------------------- 3
head(3, "NO FINDING", "the scanner, and the count")

sample = os.path.join(HERE, "specimens", "20260818deepseektestsample.md")
print("    scan.py over the pasted output alone: `no candidates`")
print("      (run separately on the 45-word passage, not on this file, which")
print("       carries repository framing the scanner would read)")
print()
print("    findings recorded for this item: 2")
print("    findings per drop over the preceding 15 drops:")
print("      7 7 7 8 8 8 11 8 8 10 10 10 10 10 10")
print()
print("    0 of 138 prior claims are REFUTED or NOT SUPPORTED.")

block("""
Stated plainly so it is on the record rather than in a chat turn: this item
warranted two findings and got two.

That is not yet the calibration test passing. Forty-five words with no
measurement content is an easy null, which is `UNI_006`'s own caveat -- a null
chosen for being easy has not shown the classifier discriminates. The test that
would count is a SUBSTANTIVE drop that comes back clean or near-clean, and no
such drop has been supplied or found.

What this item does establish is narrower and still worth having: the rate is
not fixed by the process alone. It moved when the material did.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_145..UNI_146")
print(BAR)
