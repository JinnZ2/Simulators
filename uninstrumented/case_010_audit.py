#!/usr/bin/env python3
"""case_010_audit.py -- checks on the Case 010 drop.

Added, not delivered. `cases/010coupledperturbationbiohybrid.md` is the entry as received and is
not modified. Findings recorded in AUDIT_NOTES.md as UNI_013..UNI_019.

    python3 case_010_audit.py

Case 010 is the first entry delivered to this register that (a) declines to
name its mechanism, (b) states a confidence below the ceiling, and (c) has a
live external occasion with a DOI. Each of those touches something the
register had already recorded as open.

LITERATURE CHECKS IN THIS FILE. Three of the checks below were run against
the open web on 2026-08-18 and their results are recorded here as data. They
are NOT reproducible by running this script -- it does no network access --
and they are marked so. What is reproducible is everything computed from the
register and from the entry text.

stdlib only, deterministic. CC0.
"""

import io
import os
import re
from collections import Counter

import uninstrumented as U

HERE = os.path.dirname(os.path.abspath(__file__))
CASE = io.open(os.path.join(HERE, "cases", "010coupledperturbationbiohybrid.md"),
               encoding="utf-8").read()
BAR = "=" * 72


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


def block(t):
    print(t.strip("\n"))


print("uninstrumented -- audit of the Case 010 drop")
print("delivered: cases/010coupledperturbationbiohybrid.md")
print("register  : %d entries, %d mechanisms" % (len(U.ENTRIES),
                                                 len(U.MECHANISMS)))

# ---------------------------------------------------------------- UNI_013

head(1, "UNI_013", "the entry's central move is not constructible")
print()
for m in ("UNASSIGNED", "PROTOCOL_ORTHOGONALITY", None):
    try:
        U.entry("q", m, "v", "w", "c", "device physics")
    except (ValueError, TypeError) as e:
        print("  entry(excluded_by=%-24r) -> %s"
              % (m, type(e).__name__ + ": " + str(e).split(", got")[0][:44]))
    else:
        print("  entry(excluded_by=%-24r) -> accepted" % m)
block("""
The entry states its own reason for declining to file:

    Argument for leaving it unassigned: assigning the bin before the
    measurement exists closes a variable that has not been read out.

That is the register's own discipline turned on the register's schema, and
the schema has no slot for it. `entry()` validates `excluded_by` against a
closed eight-tuple and raises on anything else, so an entry with the
mechanism deliberately open cannot be constructed -- and neither can one
filed under the new bin the drop proposes.

This is the shape recorded four times already (`MF_017`, `CW_015`,
`DL_004`, `GC_012`, `CA_003`) with one difference that matters. Those are
missing FIELDS: a stated rule with no place to put it. Here the vocabulary
is closed on purpose, and closure is the design. Case 010 is the first
delivery to argue that the closure is premature for a particular case, and
the schema cannot record that argument -- only obey it or be edited.

The cheap repair is a sentinel rather than a ninth mechanism: `UNASSIGNED`
as a legal value of `excluded_by`, with `candidates=[...]` carrying the
bins under consideration and a required `why_open` string. That keeps the
closed vocabulary for filed entries, keeps unfiled entries visible in the
register rather than only in a Markdown file beside it, and makes
"unassigned" a state the sort can count instead of an absence.
""")

# ---------------------------------------------------------------- UNI_014

head(2, "UNI_014", "the first confidence below the ceiling")
print()
print("  %-3s %-24s %s" % ("#", "mechanism", "confidence (first 46 chars)"))
print("  " + "-" * 78)
for i, e in enumerate(U.ENTRIES, 1):
    print("  %-3d %-24s %s" % (i, e["excluded_by"], e["confidence"][:46]))
conf = re.search(r"## CONFIDENCE\n+(.*?)\n\n", CASE, re.S)
print("  %-3s %-24s %s" % ("010", "(unassigned)",
                           " ".join(conf.group(1).split())[:46]))
print()
starts_high = sum(1 for e in U.ENTRIES
                  if e["confidence"].lower().startswith("high"))
print("  entries opening with 'high' : %d of %d" % (starts_high,
                                                    len(U.ENTRIES)))
print("  Case 010                    : 'not above ~40%. Not sufficient to "
      "act on.'")
block("""
`UNI_004` ran the register's own null test and found the confidence field
constant: every delivered entry states high confidence on the exclusion,
which is `CONSTANT_FIRES` in `../null-harness/` terms. Eight of eight, and
the check is still in `check_null()`.

Case 010 is the first entry where the field carries information. It states
a number, states it is a gradient and not a commitment, and states that it
is not enough to act on.

What that does and does not do. It makes the field non-constant, so a
reader can now sort by it and the sort means something. It does NOT close
`UNI_006`, which is about admission rather than about the field: the
register has still never turned an entry away, and a low-confidence entry
that is admitted is an admitted entry. The discriminating test is still a
case the register REFUSES, and there is not one.
""")

# ---------------------------------------------------------------- UNI_015

head(3, "UNI_015", "the occasion, checked  [web, 2026-08-18, not reproducible here]")
CLAIMED = [
    ("Keremane et al., Adv. Funct. Mater. 36(34), 2026", "CONFIRMED",
     "K. S. Keremane et al., 'Molecularly Engineered Highly Stable "
     "Memristors with Ultra-Low Operational Voltage: Integrating Synthetic "
     "DNA with Quasi-2D Perovskites', Adv. Funct. Mater. 36(34), 2026"),
    ("DOI 10.1002/adfm.202530539", "CONFIRMED", "resolves to that article"),
    ("Ag-nanoparticle-embedded synthetic DNA on quasi-2D perovskite",
     "CONFIRMED", "stack reported as Ag/(PEA)2(MA)Pb2I7/Ag-synDNA/Pt"),
    ("operating voltage < 0.1 V", "CONFIRMED", "reported as < 0.1 V"),
    ("forming-free switching", "CONFIRMED", "reported as forming-free"),
    ("DNA alone and perovskite alone weaker than the combination",
     "REPORTED", "stated in press material; the per-arm numbers were not "
                 "reachable from here"),
]
print()
for claim, status, note in CLAIMED:
    print("  %-9s %s" % (status, claim))
    print("            %s" % note[:62])
    if len(note) > 62:
        print("            %s" % note[62:126])
block("""
Six stated details, six confirmed or reported as stated. Nothing in the
OCCASION section is embellished, and the citation is exact down to the
volume and issue.

That is worth recording because it is the first literature claim in this
drop family that could be checked at all. `ANC_010`, `CD_009`, `RD_015` and
`HO_005` are all UNVERIFIED for the same reason -- citation markers that
point outside the delivery -- and each was recorded as a gap rather than a
fault. Case 010 gives a DOI, and a DOI is checkable.
""")

# ---------------------------------------------------------------- UNI_016

head(4, "UNI_016", "two of the four 'not located' items are locatable, and both are scalars")
print()
print("  the entry's own list of what it could not find:")
for item, found in (("cycle count", "1000 cycles (endurance)"),
                    ("retention duration", "> 4e3 s, both HRS and LRS"),
                    ("temperature range", "not located here either"),
                    ("variability distributions",
                     "not located here either")):
    mark = "FOUND  " if "not located" not in found else "STILL  "
    print("    %s %-26s %s" % (mark, item, found))
block("""
Two of the four were reachable from a search, and the correction cuts in
the entry's favour rather than against it.

Endurance is a cycle COUNT. Retention is a DURATION. Both are scalars, and
both are produced the way the entry says: cycle the device with everything
else at setpoint, or hold the state with everything else at setpoint. The
SCALAR DEMAND candidate bin was offered as a hypothesis about how the
qualification suite is built; the two metrics that turned up are instances
of it.

So the OCCASION section needs a correction and the EXCLUDED BY section gets
support from the same fact. Recorded rather than edited into the entry,
which is delivered verbatim.

One number is worth a second look by anyone extending this: retention
"> 4e3 s" is a little over an hour. Retention is normally quoted at 1e4 s
or extrapolated to ten years, so the reported figure is a measurement
window rather than a lifetime -- which is again a single-axis scalar with
its own holding-fixed, and is the kind of thing ARM B is aimed at.
""")

# ---------------------------------------------------------------- UNI_017

head(5, "UNI_017", "the field-wide falsifier partially fires  [web, 2026-08-18]")
block("""
The entry's first falsifier:

    coupled-perturbation protocols are already standard in the memristor
    qualification literature

and its matching sub-question: "if the answer is none across the field, the
exclusion is field-wide rather than specific to this device."

The answer is not none. Combined-stress protocols exist and are named:

    THB       temperature-humidity-bias -- three variables applied at once
    TB        temperature-bias
    temperature cycling, radiation testing
    IEEE P1817 (working group), JEDEC JC-42.4 -- standardisation efforts
              covering temperature cycling, humidity exposure and EMI

So the strong reading of the sub-question is settled: the exclusion is NOT
field-wide in the sense of "nobody varies more than one thing".

The entry survives in narrowed form, and the narrowing is precise. THB and
its relatives hold several variables simultaneously at CONSTANT elevated
setpoints -- 85 C / 85 % RH is a corner of a factorial, and its purpose is
package and moisture-ingress reliability. ARM B specifies something else:

    same total perturbation magnitude, applied as simultaneous co-varying
    DRIFT across all four axes, non-square waveform
    ...
    run ARM B at the same integrated stress dose as ARM A so that the
    comparison is of distribution shape, not of total load

A corner test asks whether the device survives a harsh place. ARM B asks
whether the JOINT TRAJECTORY matters at matched dose. Those are different
questions, and no protocol answering the second was located.

The honest status: falsifier 1 fires against the strong claim and not
against the narrow one. The entry should be edited to say "co-varying
drift at matched integrated dose" wherever it says "co-varying", since
that is the part with no prior art located, and the part that is already
standard should be cited rather than treated as absent.
""")

# ---------------------------------------------------------------- UNI_018

head(6, "UNI_018", "the supplement falsifier could not be checked from here")
block("""
    the paper's supplementary data contains a multi-variable arm

UNVERIFIED. The publisher's page and every news mirror located are blocked
by this environment's network egress proxy, so the full text and the
supplement were not reachable. Search returned metrics; it did not return
the methods section.

Recorded as a gap and not as a fault, on the same rule as `UNI_006`. It is
also the cheapest of the three falsifiers for anyone with institutional
access: one look at the supplementary methods settles it, and it is the
one that would close the case outright rather than narrow it.
""")

# ---------------------------------------------------------------- UNI_019

head(7, "UNI_019", "the comparator is the load-bearing part of the design")
block("""
The register's own `check_null()` closes with what it does not establish:

    the near-boundary test is a quantity a field believes it measures and
    does not, and none of the delivered entries is currently contested by
    anyone.

Case 010 is that case. Device stability is a quantity the field believes it
measures -- there are standards bodies for it -- and the entry claims a
component of it is not reachable by the suite as constituted. It arrives
with a live paper, a DOI, and a stated confidence low enough to be wrong.

And it cannot file, because it has no mechanism (`UNI_013`). The
near-boundary case the register was waiting for is the one the schema will
not take.

The design itself is the strongest part of the drop, on one element: the
COMPARATOR. "Organic scaffold replaced by a synthetic periodic scaffold of
matched spacing and matched Ag loading" is a known-null in
`../null-harness/` terms, and without it the reported result -- hybrid
beats DNA-alone and beats perovskite-alone -- cannot be decomposed, because
the hybrid differs from each of those in more than one way at once. Matched
spacing and matched Ag loading is what isolates "organic" from "periodic
scaffold with silver in it".

The three-way discriminator names its own discard branch --

    If the margin NARROWS under ARM B, the coupling reading is wrong in
    sign and should be discarded.

-- which is a reachable negative, so the design is not `CONSTANT_SILENT`.
The flat branch is stated as a real outcome with a name ("the organic layer
is functioning as a geometric ruler") rather than as a failure to find
something, which is the distinction `UNI_005` turns on.

What the design does not carry is a power calculation. delta(A, B) is a
difference of differences across two device populations, and nothing states
how many devices, or what margin would be resolvable against
device-to-device variability -- which is one of the two items still not
located (`UNI_016`). That is a `G-RES` pair waiting to be declared:
variability spread against the margin being claimed.
""")

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as UNI_013..UNI_019")
print(BAR)
