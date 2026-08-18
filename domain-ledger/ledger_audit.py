#!/usr/bin/env python3
"""ledger_audit.py -- checks on the domain-ledger drop.

Added, not delivered. ledger.py is the drop as received and is not
modified. Findings are recorded in AUDIT_NOTES.md as DL_001..DL_005.

    python3 ledger_audit.py

The drop is one file: a scorer with a selftest, no shapes/ directory, no
README and no claim table. Nothing here invents a shape.

stdlib only, deterministic. CC0.
"""

import contextlib
import io
import os

import itertools

import anchor as A
import ledger as L

import json


def wrap_local(t, w, ind=""):
    words, lines, cur = str(t).split(), [], ""
    for word in words:
        if len(cur) + len(word) + 1 > w:
            lines.append(ind + cur)
            cur = word
        else:
            cur = (cur + " " + word).strip()
    if cur:
        lines.append(ind + cur)
    return lines


HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BAR = "=" * 70


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


print("domain-ledger -- audit of the delivered drop")
print("delivered: ledger.py (drop 4 docstring), anchor.py, 1 shape, 1 anchor map")
print("not delivered: shapes/, README.md, CLAIM_TABLE.md")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = L.selftest()
print("selftest: %s, rc=%d" % (buf.getvalue().strip().splitlines()[-1], rc))

# ------------------------------------------------------------------ DL_001
head(1, "DL_001", "the load-bearing idea, and it is the one the repo needed")
print("""
    A coverage number is not portable without its denominator. 61 percent
    over one domain set is a different quantity than 61 percent over
    another. This records the set.

That is `criteria-drift` CD_008 and `anchor-interval` ANC_006 stated for a
confidence readout instead of a benchmark: a number is identified only up
to the reference it was taken against, so publish the reference. Here the
reference is a list of domains and it is carried in the file.

Two design choices follow from it and both are unusual enough to record.

FOUR READOUTS, NOT COMBINED. coverage / cycle_depth / adversarial /
truncated are returned separately, with the docstring stating why:
"Coverage and cycle depth are different currencies. A shape can be wide
and shallow." Every other scorer in this family reduces to one headline
number and gets a finding against it -- presented-binary PB_007
(documented_share merges two states), uninstrumented's SCALAR DEMAND.
This one refuses the reduction up front.

DENOMINATORS NAMED IN THE OUTPUT. The table footer prints what each
column divides by -- "cov: held / read", "cyc: holds that survived a
return / holds" -- so the two are visibly not over the same base. That is
the `measurement-fork` VOID RATIO check made unnecessary rather than
enforced: you cannot compare them because the tool says what they are.
""".strip())

# ------------------------------------------------------------------ DL_002
head(2, "DL_002", "the reservation is defined and never applied")
print("""
    RESERVATION: a standing fraction held as unknown, applied to every
    shape. It is not subtracted from coverage -- coverage is over what was
    read. It CAPS WHAT THE LEDGER WILL REPORT AS AVAILABLE HEADROOM, and
    it is why a shape with high coverage still does not coalesce.

`score()` computes `ceiling = 1 - reservation` and returns it. Nothing
compares anything to it. There is no headroom field, and coverage is free
to exceed the ceiling with no readout saying so:
""".strip())
s = L.score({"shape": "probe", "reservation": 0.2,
             "domains": [{"domain": d, "read": L.HOLD} for d in "abcdefghij"]})
print()
print("  ten domains, all hold, reservation 0.20")
print("    coverage %s   ceiling %s   coverage > ceiling: %s" % (
    L.fmt(s["coverage"]), L.fmt(s["ceiling"]), s["coverage"] > s["ceiling"]))
print("    fields naming headroom: %s" % (
    [k for k in s if "head" in k or "room" in k] or "none"))
print()
print("""
The sentence names a function -- cap the reported headroom -- and the code
carries the constant without the function. `ceiling` is printed in
`detail()` beside `RESERVATION` and read by nothing.

Not a wrong number: the docstring is explicit that reservation is NOT
subtracted from coverage, and it is not. What is missing is the readout
the same paragraph promises. One line: headroom = min(coverage, ceiling),
or a flag when coverage exceeds it.
""".strip())

# ------------------------------------------------------------------ DL_003
head(3, "DL_003", "coverage merges break with mixed")
print()
for label, r in (("all break", L.BREAK), ("all mixed", L.MIXED)):
    sc = L.score({"shape": label,
                  "domains": [{"domain": "a", "read": r},
                              {"domain": "b", "read": r}]})
    print("  %-10s coverage %s   breaks %d   mixed %d" % (
        label, L.fmt(sc["coverage"]), sc["breaks"], sc["mixed"]))
print("""
coverage is holds / read, and `mixed` is in the denominator and not the
numerator. So a shape that broke everywhere and a shape that read mixed
everywhere both return 0.00 -- and those are different results. A break is
the shape failing; a mixed read is the shape doing something the two-value
vocabulary cannot hold.

The information is not lost: `break_domains` and `mixed_domains` are
returned separately and `detail()` prints both under their own headings.
The loss is in the derived scalar only, which is precisely the shape
PB_007 records one folder over -- and DL_001 credits this tool with
refusing exactly that reduction on the other three readouts.

Cheapest fix is not a fifth ratio. It is the footer: "cov: held / read"
does not say that mixed sits in the denominator, and one clause would.
""".strip())

# ------------------------------------------------------------------ DL_004
head(4, "DL_004", "the guard field is read and not in the skeleton -- again")
print("""
`detail()` reads two top-level fields the SKELETON does not carry:
""".strip())
print()
print("  SKELETON keys            : %s" % ", ".join(sorted(L.SKELETON)))
print("  read by detail(), absent : criterion_fixed_in_advance, open")
print("""
`criterion_fixed_in_advance` is `category-weld` CW_015's pre-registration
guard promoted to a first-class schema field -- there it lived as prose
inside a term's `open` list, here it has its own key and its own heading
in the detail view. That is the right direction and it is the same author
reaching the same discipline a third time (reasoning-gate G-PRE,
photoperiod MechanismEdit, CW_015).

And it repeats CW_015's gap exactly: `--new` emits a skeleton without it,
so the field a new shape most needs prompting for is the field the
template is silent about. Two folders, same author, same drop family, same
miss.

What is different here, and better: the SKELETON is deep-copied.
""".strip())
import json as _json
srcs = {
    "category-weld/weld.py": "TEMPLATE",
    "generation-capacity/capacity.py": "SKELETON",
    "domain-ledger/ledger.py": "SKELETON",
}
print()
print("  %-34s %s" % ("tool", "--new deep-copies its template"))
print("  " + "-" * 66)
for path in srcs:
    src = open(os.path.join(ROOT, path), encoding="utf-8").read()
    print("  %-34s %s" % (path, "json.loads(json.dumps(" in src))
print("""
`weld.py` and `capacity.py` both use `dict(TEMPLATE)`, a shallow copy that
shares the nested lists with the module global. Harmless as called -- both
only assign the top-level name -- but one line of future editing away from
mutating the template. `ledger.py` round-trips through JSON. Recorded
because it is the correct one of the three and the difference is invisible
until it is not.
""".strip())

# ------------------------------------------------------------------ DL_005
head(5, "DL_005", "an empty ledger prints a clean report")
print("""
There is no shapes/ directory in the drop. `load()` returns [] when the
directory is absent, `table([])` prints headers and the full explanatory
footer, and main() returns None:
""".strip())
print()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    L.table([])
out = buf.getvalue()
print("    rows printed  : %d" % max(0, len(out.strip().splitlines()) - 2 - 7))
print("    lines printed : %d" % len(out.strip().splitlines()))
print("    exit code     : 0")
print()
print("  the three sibling tools on the same state:")
for path, msg in (("category-weld/weld.py", "no weld files in ... -> rc 1"),
                  ("presented-binary/binary_audit.py", "no case files in ... -> rc 1"),
                  ("generation-capacity/capacity.py", "no cases/ directory -> rc 1")):
    src = open(os.path.join(ROOT, path), encoding="utf-8").read()
    refuses = "stderr" in src and "return 1" in src or "sys.exit(1)" in src
    print("    %-38s refuses: %s" % (path, refuses))
print("""
Every sibling refuses and says so on stderr. This one prints a well-formed
report with no content and exits clean, so an empty ledger is
indistinguishable from a populated one at a glance -- and the footer's
closing line, "Unpushed domains are not neutral. Each is an untested
surface", prints over zero domains.

The tool's own subject is confidence readouts that do not carry their
denominator. Its empty state is a report whose denominator is zero,
rendered as if it had one.

Nothing else here is unverified: the selftest is 13/13, it covers the
empty-ledger case at the score() level ("empty ledger gives none not
zero", "empty mismatch is none"), and those are the right two checks. The
gap is one level up, at the presentation layer the selftest does not
reach.
""".strip())

# ------------------------------------------------------------------ DL_006
head(6, "DL_006", "the first shape, and the asserted number sitting beside no derived one")
shapes = L.load()
print("""
Drop 2 delivers shapes/hierarchy-cut-generation.json: 30 domains, an
asserted coverage of 0.61, and a source field stating what the file is
for.

    Coverage asserted at 0.61 over a domain set carried in working memory
    rather than written down. This file exists to convert the asserted
    number to a derived one; until the read column is filled the derived
    number is unavailable, and that unavailability is the current state,
    not a failure.
""".strip())
print()
for sh in shapes:
    sc = L.score(sh)
    print("  %-26s domains %d   read %d   asserted %s   derived %s   mismatch %s" % (
        sc["shape"], sc["domains_total"], sc["read"],
        L.fmt(sc["asserted_coverage"]), L.fmt(sc["coverage"]),
        L.fmt(sc["coverage_mismatch"])))
print("""
The tool's whole argument, instanced on its first shape: a number that was
being carried as 0.61 now sits next to a derived column reading `--`, and
`detail()` prints "derived -- ledger not yet populated" rather than
substituting the asserted value or a zero.

That is the branch DL_002 and DL_005 are about, used correctly. It is also
the one place in this repo where an author has written down a number they
were already using and then built the instrument that refuses to confirm
it.

The gap it exposes is the one the file names: 30 domains, 0 read, so
every ratio is `--` and the reservation's ceiling has nothing to cap. The
readouts are live and the corpus is empty -- which is the honest state and
is what the source field says.
""".strip())

# ------------------------------------------------------------------ DL_007
head(7, "DL_007", "the cross-folder run order is met, for the first time in this family")
print("""
The shape's statement does something no other artifact in this drop family
has done:

    Runs on the imposed_ordering sense only -- see category-weld
    welds/hierarchy.json for the other four senses, which are not this
    claim.
""".strip())
weld_path = os.path.join(ROOT, "category-weld", "welds", "hierarchy.json")
import json
weld = json.load(open(weld_path, encoding="utf-8"))
comps = [c["id"] for c in weld["components"]]
print()
print("  category-weld/welds/hierarchy.json components (%d):" % len(comps))
print("      %s" % ", ".join(comps))
print("  minus imposed_ordering = %d; the statement says four: %s" % (
    len(comps) - 1, len(comps) - 1 == 4))
print()
print("  domains pre-classified by weld sense before being read:")
for sh in shapes:
    for d in sh.get("domains", []):
        if "sense lives here" in (d.get("note") or ""):
            print("      %-42s %s" % (d["domain"], d["note"]))
print("""
moral-decomposer MD_004 records the opposite state one folder over: a
stated RUN ORDER requiring welded terms decomposed first, seven terms
named, zero decomposed. Here the weld exists, the shape names which of its
five senses the claim runs on, and two of the thirty domains are
pre-classified as probably belonging to a different sense -- before
reading, which is the only time that classification is not closure by
construction.

The `criterion_fixed_in_advance` field carries the same discipline for the
read itself:

    Reclassifying a case as not-really-hierarchy after seeing which way it
    read is closure by construction and is not permitted; such a case is
    MIXED with the reason recorded.

That names the failure, names the routing for the ambiguous case, and
fixes both before any domain is read. DL_004's finding stands unchanged --
SKELETON still carries neither field, so a shape created by `--new` starts
without them -- and the delivered shape shows what the fields are for.
""".strip())


# ------------------------------------------------------------------ DL_008
head(8, "DL_008", "anchor.py builds the repair as its stated reason for existing")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = A.selftest()
print("anchor.py selftest: %s, rc=%d" % (
    buf.getvalue().strip().splitlines()[-1], rc))
print("""
The companion's PROVENANCE CHAINS section keeps three routing states apart:

    routed              a path to the next link exists and is stated
    unrouted            no path found yet. Alternate paths not exhausted.
    absent_established  investigated and the link genuinely does not ground
                        that way. Not a failure -- a finding, and its own
                        measurement problem needing instrumentation.

    Collapsing unrouted and absent_established into "blocked" loses the
    distinction the map exists for.

That is the fifth instance of one repair in this drop family, and the
second built in rather than found:

    PB_004   frame_sim option_gain        0 options found == never ran
    PB_012   binary_audit handoff()       above ceiling == never checked
    GC_004   MECHANISM_10 R3              not cited == no corpus searched
    MD_002   moral-decomposer reduces_to  irreducible == routed elsewhere
    GC_010   SUBCASE_10A S1               absent vs zero, designed in
    here     anchor.py routing states     unrouted vs absent_established
""".strip())
d = {"anchors": [{"corroboration": {"class": A.NONE}, "chain": [
    {"link": "u", "state": A.UNROUTED}, {"link": "a", "state": A.ABSENT}]}]}
sc = A.score(d)
print()
print("  one unrouted link + one absent_established link ->")
print("    unrouted_total %d   absent_total %d   reported apart" % (
    sc["unrouted_total"], sc["absent_total"]))
print("""
GC_010 was the first time the distinction was specified ahead of code.
This is the first time it is implemented, counted separately in the
readout, and restated in the output -- `blocking()` closes with the
paragraph rather than assuming the reader remembers it.

What it is not: a reading. No anchors/ file has been recorded, so the
three states have never been assigned to a real link.
""".strip())

# ------------------------------------------------------------------ DL_009
head(9, "DL_009", "two fields are described as band-setting; one is aggregated")
print("""
The opening paragraph and the BANDS heading name different fields:

    What sets the band is where the shape ANCHORS: what it grounds to, and
    what band THAT ANCHOR ALREADY OCCUPIES.

    BANDS -- set by the CLASS OF SUPPORT, not by sampling effort.

The schema carries both. `target_band` is what the anchor already occupies;
`corroboration.class` is the class of support for reaching it. Measured on
an anchor where they differ:
""".strip())
doc = {"shape": "s", "sense": "x", "anchors": [
    {"target": "thermodynamics", "target_band": A.CYCLE_PERSISTENT,
     "corroboration": {"class": A.EXTERNAL, "study_count": 200},
     "chain": [{"link": "a", "state": A.ROUTED}]}]}
sc = A.score(doc)
a0 = sc["anchors"][0]
print()
print("  target_band          %s (%.2f)" % (a0["target_band"], a0["target_ceiling"]))
print("  corroboration class  %s (%.2f)" % (
    a0["corroboration_class"], a0["corroboration_ceiling"]))
print("  document ceiling     %.2f" % sc["ceiling"])
print()
print("  document-level fields score() computes: %s" % ", ".join(
    k for k in ("ceiling_class", "ceiling", "anchor_spread",
                "chains_complete", "unrouted_total", "absent_total")))
print("  ... none of them reads target_band.")
print("""
`target_band` is computed per anchor, printed by `detail()`, and
aggregated by nothing. Anchoring to thermodynamics -- a cycle-persistent
target -- yields a document ceiling of 0.80 because the corroboration is
external.

The selftest pins exactly this: its `thermo` anchor has
target_band=cycle_persistent and the asserted check is `ceiling == 0.80`.
So the choice is deliberate and the BANDS heading is the one the code
follows.

The residue is in the opening paragraph, which says anchor proximity sets
the band and that "anchoring near something that has survived generational
cycles raises the number". On the delivered code it does not: proximity to
a cycle-persistent target raises `target_ceiling`, which no readout uses.
One of the two sentences describes the code and the other describes a
quantity the code records and does not aggregate.

Which is right is a design question, not an audit one. What is checkable
is that a field the docstring calls band-setting reaches no readout.
""".strip())

# ------------------------------------------------------------------ DL_010
head(10, "DL_010", "the refusal is real; the constants under it are stipulated")
print("""
    No composite figure is emitted. Weighting near against far anchors is
    not specified, and a number produced by guessing at it would be less
    honest than the anchors themselves.

The selftest asserts it -- `("no composite emitted", "confidence" not in s)`
-- so the refusal is enforced rather than promised. That is DL_001's
refusal-of-reduction taken one step further than ledger.py takes it, and
it is the strongest instance in the family.

Two numbers are emitted, and both are functions of three stipulated
constants:
""".strip())
print()
print("  BAND_CEILING  %s" % A.BAND_CEILING)
vals = set()
for combo in itertools.combinations_with_replacement(A.BAND_ORDER, 2):
    dd = {"anchors": [{"corroboration": {"class": c}, "chain": []}
                      for c in combo]}
    vals.add(A.score(dd)["anchor_spread"])
print("  anchor_spread can take exactly %d values: %s" % (
    len([v for v in vals if v is not None]),
    sorted(v for v in vals if v is not None)))
print("""
0.30, 0.80 and 0.99 have stated rationales -- no external body behind it,
one reading of outside material, held across cycles -- and no derivation.
`anchor_spread` is a difference of two of them, so it inherits that.

Same shape as `presented-binary`'s `HANDOFF_CEILING`, which B10 discloses
in its own weak-point line: "the ceiling is set at 2 by constant, which is
a judgment call and not a measurement." Here the equivalent line is not
written. The tool refuses to guess at the weighting BETWEEN bands and
stipulates the bands themselves, which is a defensible split and is not
stated as one.

Cheap to close in the direction the folder already uses: the three bands
are ordinal by construction (BAND_ORDER), and `ceiling_class` is the
ordinal readout. `ceiling` converts the ordinal to a number, which is the
step with nothing behind it -- and is exactly what `criteria-drift`
CD_002 records as ordinal-compared-as-nominal, arriving here from the
opposite direction.
""".strip())

# ------------------------------------------------------------------ DL_004 update
head(11, "DL_004", "half the skeleton gap closes in the next tool")
print()
print("  ledger.py SKELETON : %s" % ", ".join(sorted(L.SKELETON)))
print("  anchor.py SKELETON : %s" % ", ".join(sorted(A.SKELETON)))
print()
for f in ("open", "criterion_fixed_in_advance"):
    print("  %-28s ledger: %-6s anchor: %s" % (
        f, f in L.SKELETON, f in A.SKELETON))
print("""
DL_004 recorded that `detail()` reads `open` and
`criterion_fixed_in_advance` while `SKELETON` carries neither, so `--new`
never prompts for the pre-registration guard.

anchor.py carries `open` in its skeleton. Same author, next tool, half the
gap closed without being asked. `criterion_fixed_in_advance` is in neither
skeleton -- and anchor.py does not read it at all, which is consistent:
the field belongs to a read that classifies domains, and an anchor map
does not classify.

DL_004 stands for ledger.py unchanged, and the direction of travel is
recorded with it. DL_005 also recurs unchanged: anchor.py with no
anchors/ directory prints headers and its full footer and exits 0.
""".strip())


# ------------------------------------------------------------------ DL_009 corrected
head(12, "DL_009", "CORRECTED -- the two band fields are different quantities")
adoc = json.load(open(os.path.join(HERE, "anchors",
                                   "hierarchy-imposed-ordering.json"),
                      encoding="utf-8"))
print("""
DL_009 read the docstring's two band-setting sentences as a possible
defect: target_band is computed per anchor and reaches no document-level
readout, while the opening paragraph says anchor proximity sets the band.

The first real anchor map settles it, in a note the schema already had a
field for:
""".strip())
print()
a0 = adoc["anchors"][0]
print("  target: %s" % a0["target"])
print("    target_band         %s" % a0["target_band"])
print("    corroboration class %s" % a0["corroboration"]["class"])
for line in wrap_local(a0["corroboration"]["note"], 66, "    "):
    print(line)
print("""
The two fields are not two descriptions of one thing. `target_band` is
where the TARGET sits; `corroboration.class` is the class of support for
the CONNECTION between the shape and that target. Anchoring to
thermodynamics does not inherit thermodynamics' band — what is external is
the link from imposed ordering to maintenance cost.

So aggregating `corroboration.class` and not `target_band` is correct, and
DL_009's substantive worry dissolves. This audit read a tension in the
prose as a possible defect in the code; the code is right.

What survives is one paragraph. "Anchoring near something that has
survived generational cycles raises the number" describes something the
code does not do and, on the anchor map's own reading, should not do --
proximity to a cycle-persistent target is context, not corroboration. One
sentence in the docstring, and the data is the authority.
""".strip())

# ----------------------------------------------------------------- DL_011
head(13, "DL_011", "the third routing state is implemented and unassigned")
from collections import Counter
states = Counter(l["state"] for a in adoc["anchors"] for l in a["chain"])
print()
for st in A.STATES:
    print("  %-20s %d" % (st, states.get(st, 0)))
print("""
DL_008 recorded that `absent_established` is the first implementation of a
repair specified five times. On the first real map it is used zero times
out of nine links.

Not a defect and not an oversight -- the culture anchor's second link
carries a note describing exactly what assigning it would mean:

    If this establishes as ABSENT -- the construct genuinely does not
    ground in biology -- that is a finding requiring its own
    instrumentation and scientific method, not a failure of the shape.

So the state is understood, its consequence is written down, and no link
has yet been investigated far enough to earn it. `absent_established`
requires having looked; `unrouted` is what you have before you look. The
map is at the before-you-look stage throughout, which the next section
measures.
""".strip())

# ----------------------------------------------------------------- DL_012
head(14, "DL_012", "unrouted holds three de-facto states and the readout merges them")
unr = [(a["target"], l) for a in adoc["anchors"] for l in a["chain"]
       if l["state"] == A.UNROUTED]
print()
print("  %-44s %9s %6s" % ("link", "attempted", "open"))
print("  " + "-" * 62)
for _, l in unr:
    print("  %-44s %9d %6d" % (
        l["link"][:44], len(l.get("paths_attempted") or []),
        len(l.get("paths_open") or [])))
noopen = [l for _, l in unr if not (l.get("paths_open") or [])]
print()
print("  every unrouted link has 0 attempted paths")
print("  %d of %d have no open path named either" % (len(noopen), len(unr)))
print("""
The docstring defines unrouted as "no path found yet. Alternate paths not
exhausted", which covers three situations the map distinguishes in its
data and the readout does not:

    paths attempted, none worked, others open    -- work has been done
    nothing attempted, open paths named          -- work is queued
    nothing attempted, no path nameable          -- no instrument exists

`unrouted_total` counts all three as one number, 6. The two links in the
third group are the ones whose notes ask for new instrumentation
("No instrument identified"), which is the same distance from a reading as
`absent_established` and arrives at it from the other side.

The schema already carries what separates them -- `paths_attempted` and
`paths_open` are fields, and `blocking()` prints both. The gap is at the
readout, and it is the same shape as DL_003: the information survives per
item and the derived scalar merges it.
""".strip())

# ----------------------------------------------------------------- DL_013
head(15, "DL_013", "the map states three numbers about itself and all three hold")
sc = A.score(adoc)
nq = [l for a in adoc["anchors"] for l in a["chain"] if l.get("quantified")]
print()
print("  %-42s %-10s %s" % ("claim in the file's own open list", "computed", "holds"))
print("  " + "-" * 64)
print("  %-42s %-10s %s" % ("Anchor spread is 0.5", sc["anchor_spread"],
                            sc["anchor_spread"] == 0.5))
print("  %-42s %-10s %s" % ("The ceiling reported is 0.80", sc["ceiling"],
                            sc["ceiling"] == 0.80))
print("  %-42s %-10s %s" % ("No link anywhere in this file is quantified",
                            len(nq), not nq))
print("""
Three self-reported numbers, three exact. The second is stated with its
own qualification -- "It is a ceiling on the whole sense, not a report
that the shape is near it" -- which is the distinction DL_010 turns on,
made by the author in the file.

The fourth open item is the one that matters, and it is the folder's
thesis instanced:

    The load-bearing unrouted link is cost-gradient-by-depth-of-ordering
    on the thermodynamic anchor. Routing it with a number would do more
    than reading further domains, because it converts the near anchor from
    stated to measured.

ledger.py's new paragraph says coverage "resolves position inside a band
that anchor distance already set ... Reading further domains moves the
number within a band; it does not promote a shape between bands." The map
then names which single measurement beats more coverage, and it is a link
in a provenance chain rather than a domain in a ledger.

That is the two tools doing the job the pair was built for, on one shape,
with no reading taken in either.
""".strip())

# ----------------------------------------------------------------- DL_002 update
head(16, "DL_002", "the reservation constant gets a source; the finding stands")
print("""
Drop 4 changes ledger.py by docstring only -- the code is byte-identical
after stripping the module docstring -- and one of the two additions is a
derivation for the constant DL_010 flagged as stipulated:

    The 0.2 default here encodes only the external-band ceiling of 0.8.
    The 30 floor for shapes with no external support, and the 99 band
    requiring generational cycle survival, live in anchor.py where the
    source class is recorded. Do not read a ceiling off this file alone.
""".strip())
print()
print("  1 - SKELETON reservation = %.2f" % (1 - L.SKELETON["reservation"]))
print("  anchor.py BAND_CEILING['external'] = %.2f" % A.BAND_CEILING[A.EXTERNAL])
print("  the default is now derived, not free: %s" % (
    abs((1 - L.SKELETON["reservation"]) - A.BAND_CEILING[A.EXTERNAL]) < 1e-9))
print("""
One of DL_010's three constants now has a stated source. 0.30 and 0.99
remain stipulated.

DL_002 itself stands unchanged: `ceiling` is still computed, returned,
printed beside RESERVATION, and read by nothing. The disclosure sharpens
it rather than closing it -- the file now says "do not read a ceiling off
this file alone" and `detail()` still prints `RESERVATION 0.20 ceiling
0.80` as a line of the report. A number that no readout applies and the
docstring warns against reading is the one line in the output with no
consumer.
""".strip())


print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as DL_001..DL_013")
print(BAR)
