#!/usr/bin/env python3
"""weld_audit.py -- checks on the category-weld drop.

Added, not delivered. Imports the DELIVERED weld.py and the term files;
modifies nothing. Findings are recorded in AUDIT_NOTES.md as CW_001..013.

    python3 weld_audit.py

weld.py and test_weld.py arrived in a second drop, after this audit had
already reconstructed both from the README's call sites. The reconstruction
is kept under reconstruction/ because the delivered-vs-reconstructed
comparison is what closes CW_001 and refutes CW_004.

stdlib only, deterministic. CC0.
"""

import importlib.util
import json
import os

import weld  # the delivered scorer

HERE = os.path.dirname(os.path.abspath(__file__))
BAR = "=" * 70


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


RECON = _load("recon_weld", os.path.join(HERE, "reconstruction", "weld.py"))

# The eight mechanisms already in ../uninstrumented/README.md, with the
# structure each one requires. C1's falsifier is "showing any of the eight
# already covers the two seed terms without adding a mechanism", so the
# check has to be against the structure, not against the label.
EIGHT = [
    ("MODALITY", "apparatus is in a different channel from the quantity"),
    ("STORAGE", "medium cannot hold the shape of the quantity"),
    ("SCALAR DEMAND", "ONE quantity's variation over a domain flattened to a scalar"),
    ("BUDGET BOUNDARY", "a closed budget compared against an open one"),
    ("AUTHORED REFERENCE", "the reference is produced by the measured party"),
    ("PROXY SUBSTITUTION", "a NAMED target displaced by a NAMED enforceable stand-in"),
    ("AUDIT ASYMMETRY", "the guard fires on one side of a comparison only"),
    ("SCORED AS WASTE", "a component enters the accounting as cost"),
]

# The six exit branches of the delivered rel_change(), as predicates on a
# readings dict, so coverage is counted rather than asserted.
BRANCHES = [
    ("B1 empty/absent reading", lambda r: not r),
    ("B2 before or after is null", lambda r: r and (r.get("before") is None or r.get("after") is None)),
    ("B3 non-numeric", lambda r: _nonnumeric(r)),
    ("B4 before == 0", lambda r: _num(r) and float(r["before"]) == 0),
    ("B5 after <= 0 or before < 0", lambda r: _num(r) and float(r["before"]) != 0
     and (float(r["after"]) <= 0 or float(r["before"]) < 0)),
    ("B6 usable, returns a ratio", lambda r: _num(r) and float(r["before"]) != 0
     and float(r["after"]) > 0 and float(r["before"]) > 0),
]


def _num(r):
    if not r or r.get("before") is None or r.get("after") is None:
        return False
    try:
        float(r["before"]), float(r["after"])
    except (TypeError, ValueError):
        return False
    return True


def _nonnumeric(r):
    if not r or r.get("before") is None or r.get("after") is None:
        return False
    return not _num(r)


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


terms = weld.load_welds()
by_name = {t["term"]: t for t in terms}

print("category-weld -- audit of the delivered drop")
print("%d term file(s): %s" % (len(terms), ", ".join(sorted(by_name))))
print("scorer under audit: weld.py as delivered")

# ----------------------------------------------------------------- CW_001
head(1, "CW_001", "the verification claim -- falsifier fired, claim holds")
print("""
CLAIM_TABLE.md, "Status of the readouts":

    max_spread and bias "are implemented and verified against synthetic
    fixtures in test_weld.py"

The first drop named weld.py and test_weld.py under Files and shipped
neither, so the statement was unverifiable from the folder. Both arrived
in a second drop. CW_001's own falsifier -- "the delivered files turning
up" -- fired.

The statement is now checkable and it holds. test_weld.py builds a
SYNTHETIC term with three quantified cases and one unquantified one, and
asserts n_cases, n_quantified, n_unquantified, max_spread and bias against
hand-computed values.
""".strip())
print()
recon_choices = sum(
    1
    for line in open(os.path.join(HERE, "reconstruction", "weld.py"), encoding="utf-8")
    if "[CHOICE]" in line
)
print("  reconstruction/weld.py made %d marked arithmetic choices." % recon_choices)
print("  One of them was wrong in a way that produced a finding (CW_004).")

# ----------------------------------------------------------------- CW_004
head(2, "CW_004", "REFUTED by the delivered file -- correcting this audit")
print("""
The first pass read "ratio between component relative-changes" ADDITIVELY:
rel = (after - before) / |before|, so an unmoved component is 0 and a
ratio against it diverges. On that reading max_spread ran to infinity at
the paradigm weld -- the tracked component holding while the hidden one
collapses -- which was recorded as CW_004.

The delivered rel_change is MULTIPLICATIVE: after / before. An unmoved
component is 1.0, not 0. The spread converges.
""".strip())
print()
print("  hidden component halves; label walks toward unmoved")
print()
print("  %-14s %14s %16s" % ("label after", "delivered", "reconstruction"))
print("  " + "-" * 46)
for after in (50.0, 90.0, 99.0, 99.9, 99.99, 100.0):
    case = {"id": "p", "readings": {
        "label": {"before": 100.0, "after": after},
        "hidden": {"before": 100.0, "after": 50.0}}}
    d, _ = weld.case_spread(case, ["label", "hidden"])
    r, _ = RECON.case_spread(case)
    print("  %-14.2f %14s %16s" % (
        after, weld.fmt(d, 3), RECON.fmt(r, "%.3f")))
print()
print("""
CW_004 is REFUTED. The divergence was a property of the reconstruction's
[CHOICE], not of the mechanism.

The delivered choice is also the better one for a reason worth naming: a
ratio of multipliers is dimensionless, so it is comparable across
components carried in unlike units -- people per unit area against
independent operators per 1000 acres. An additive relative change is
dimensionless too, but its zero sits at "did not move", which is the
tracked component's expected state, and putting a statistic's singular
point where the data is expected to sit is the defect the first pass
introduced and then reported as a finding.

What survives is the shape, relocated: see CW_010.
""".strip())

# ----------------------------------------------------------------- CW_010
head(3, "CW_010", "max_spread is undefined at total collapse")
print("""
rel_change guards with `if a <= 0 or b < 0: return None`. A component that
goes to exactly zero has no ratio, so it is dropped from the case, and if
it was one of only two quantified components the whole case falls out of
max_spread and bias as unquantified.

Total collapse is the mechanism's maximal divergence. rural.json's own
employment-concentration note: "One packing facility closure ZEROES
regional employment at once."
""".strip())
print()
print("  label holds at 1.0x; hidden component approaches zero")
print()
print("  %-16s %14s %18s" % ("hidden after", "max_spread", "components read"))
print("  " + "-" * 54)
for ah in (10.0, 1.0, 0.1, 0.01, 0.0):
    case = {"id": "p", "readings": {
        "label": {"before": 100.0, "after": 100.0},
        "hidden": {"before": 100.0, "after": ah}}}
    d, ratios = weld.case_spread(case, ["label", "hidden"])
    print("  %-16.2f %14s %18d" % (ah, weld.fmt(d, 1), len(ratios)))
print()
print("""
The statistic rises monotonically toward the collapse and is undefined at
it. This is the shape the first pass was reaching for and put in the wrong
place: not at the tracked component holding, but at the hidden component
reaching zero.

It is a real guard, not an oversight -- a/b with a = 0 is 0, and a spread
of max/min with min = 0 is a division by zero. The question the guard
answers by silence is what a component reaching zero should score. A
count that hits zero is not missing data; it is the reading.
""".strip())

# ----------------------------------------------------------------- CW_013
head(4, "CW_013", "the fixtures reach 2 of 6 branches, and miss CW_010's")
import test_weld as TW  # noqa: E402

readings = []

for case in TW.SYNTH["divergences"]:
    for cid in [c["id"] for c in TW.SYNTH["components"]]:
        readings.append((case["id"], cid, (case.get("readings") or {}).get(cid)))
print()
print("  %-28s %s" % ("rel_change exit branch", "reached by test_weld.py"))
print("  " + "-" * 54)
hit = 0
for label, pred in BRANCHES:
    reached = any(pred(r) for _, _, r in readings)
    hit += 1 if reached else 0
    print("  %-28s %s" % (label, "yes" if reached else "no"))
print()
print("  %d of %d branches reached." % (hit, len(BRANCHES)))
print()
print("""
The unreached branches include B5, which is the one that decides CW_010 --
what happens when a component reaches zero. So "verified against synthetic
fixtures" is true and partial: the arithmetic that runs on ordinary data
is checked, and the arithmetic that runs at the mechanism's limit case is
not.

A fixture for it is two lines, and it would force the zero question to be
answered rather than guarded.
""".strip())

# ----------------------------------------------------------------- CW_011
head(5, "CW_011", "case_direction's docstring is inverted against its body")
print("""
weld.py, case_direction:

    \"\"\"+1 if the untracked component fell relative to the tracked one,
       -1 if it rose relative, 0 if not resolvable.\"\"\"
    ...
    d = math.log(far[1] / ratios[tracked])
    return -1 if d < 0 else 1

far < tracked means the untracked component FELL relative to the tracked
one, which makes d < 0, which returns -1. The docstring says +1.

test_weld.py's own comments side with the body:

    # a holds, b falls 10x  -> spread 10, direction -1 (b hidden below a)
""".strip())
print()
probe_fell = {"id": "p", "readings": {
    "a": {"before": 100, "after": 100}, "b": {"before": 100, "after": 10}}}
probe_rose = {"id": "p", "readings": {
    "a": {"before": 100, "after": 100}, "b": {"before": 10, "after": 40}}}
for name, case in (("untracked fell", probe_fell), ("untracked rose", probe_rose)):
    _, ratios = weld.case_spread(case, ["a", "b"])
    print("  %-16s -> case_direction = %+d" % (
        name, weld.case_direction(case, "a", ratios)))
print()
print("""
Blast radius is small: bias takes |sum(dirs)|, so the convention cancels
and every number in the drop is unaffected. It matters to a reader
deciding which side of a weld is being hidden, which is what the paragraph
under the function says the sign is for.

One word. The body is right and the docstring is backwards.
""".strip())

# ----------------------------------------------------------------- CW_006
head(6, "CW_006", "bias is 1.0 on one observation -- instance corrected")
one = {"term": "probe", "tracked_by_label": "a",
       "components": [{"id": "a"}, {"id": "b"}],
       "divergences": [{"id": "s1", "readings": {
           "a": {"before": 100, "after": 100},
           "b": {"before": 100, "after": 10}}}]}
s = weld.score(one)
print()
print("  a single resolvable direction:  bias = %s  on 1 case" % weld.fmt(s["bias"]))
print("""
bias is |sum of signs| / count and there is no floor in the delivered
file, so one directional case reads 1.0 -- the value MECHANISM_09.md
glosses as "one component is systematically standing behind another",
returned by a statistic that has watched one component move once.
null-harness calls this CONSTANT_FIRES. The claim stands.

CORRECTION to the first pass. It demonstrated this on capital /
socialized-downside with revenue_claim filled in, and that instance does
not hold against the delivered code: case_direction returns 0 when the
TRACKED component is unquantified, and ownership_title has no readings in
that case, so bias stays None there.
""".strip())
cap = json.loads(json.dumps(by_name["capital"]))
sd = next(d for d in cap["divergences"] if d["id"] == "socialized-downside")
sd["readings"]["revenue_claim"] = {"before": 1.0, "after": 1.2}
sc = weld.score(cap)
print()
print("  capital with revenue_claim filled:  bias = %s   max_spread = %s" % (
    weld.fmt(sc["bias"]), weld.fmt(sc["max_spread"], 3)))
print("""
So the delivered code is stricter than the reconstruction, and immune to
that particular one-observation reading. The floor is still absent, and
still reachable by any case in which the tracked component IS measured --
which is the likelier case, since the tracked component is by definition
the one the record already carries.
""".strip())

# ----------------------------------------------------------------- CW_012
head(7, "CW_012", "the --new template scores on the only live readout")
t = dict(weld.TEMPLATE)
t["term"] = "employed"
print("""
README.md documents:

    python3 weld.py --new employed > welds/employed.json

TEMPLATE carries a placeholder divergence with id "". score() counts
len(divergences), so the blank file scores before anyone has named a case
-- on n_cases, which is the only readout returning a number for either
seed term.
""".strip())
print()
print("  blank template -> n_cases = %d, placeholder id = %r" % (
    weld.score(t)["n_cases"], t["divergences"][0]["id"]))
print()
print("""
MECHANISM_09.md defines the readout as "how many divergence cases can be
NAMED". A case with no id has not been named. Filtering on a non-empty id
is faithful to that sentence, not a patch to it.
""".strip())

# ----------------------------------------------------------------- CW_002
head(8, "CW_002", "the mechanism's test condition 2, read two ways")
print("""
MECHANISM_09.md, Test:

    2. The language provides no separate handle for the components that
       diverged.

Read as a statement about English, the drop's own files refute it: every
component is named, in plain English, with a unit.
""".strip())
print()
for name in sorted(by_name):
    t = by_name[name]
    print("  %s -- %d components, all with an English name and a unit:" % (
        name, len(t["components"])))
    for c in t["components"]:
        print("      %-18s %s (%s)" % (c["id"], c["name"], c["unit"]))
    print()
print("""
Read as a statement about the RECORD -- the statistic, the census category,
the accounting line -- it holds: there is no census field for ownership
distribution riding under `rural`, and no line on a balance sheet for
decision authority riding under `capital`. Naming a component in a JSON
file is not the same as the record carrying it.

The second reading is the one the register is for, and it is the reading
the seed files are written under (`tracked_by_label` is a field about what
the record reads, not about what English can say). The doc states the
first. One word -- "record" for "language" -- separates a refuted
condition from a live one.
""".strip())

# ----------------------------------------------------------------- CW_003
head(9, "CW_003", "the two-part test has one part instrumented")
print("""
Two conditions, four score fields, and every one of them is about
condition 1 (divergence cases exist). Condition 2 (no separate handle)
has no readout in the delivered scorer.
""".strip())
print()
print("  %-16s %-36s %s" % ("score field", "measures", "condition"))
print("  " + "-" * 66)
for r, m in [
    ("n_cases", "how many divergences are named"),
    ("n_quantified", "how many carry paired readings"),
    ("max_spread", "how far components moved apart"),
    ("bias", "whether they moved apart consistently"),
]:
    print("  %-16s %-36s %s" % (r, m, "1"))
print("  %-16s %-36s %s" % ("(none)", "whether the record carries a handle", "2"))
print()
print("""
Consequence: a term with divergence cases and perfectly good separate
handles in the record scores identically to a weld. By the doc's own test
that term is "a summary, not a weld" -- and the scorer cannot tell them
apart. The missing readout has a shape: count the components for which the
record has an independently reportable field, over the total.
""".strip())

# ----------------------------------------------------------------- CW_005
head(10, "CW_005", "the only live readout does not separate the two seed terms")
print()
print("  %-10s %6s %6s %6s %6s %10s %6s" % (
    "term", "comp", "cases", "quant", "unq", "max_spread", "bias"))
print("  " + "-" * 58)
for name in sorted(by_name):
    s = weld.score(by_name[name])
    print("  %-10s %6d %6d %6d %6d %10s %6s" % (
        s["term"], s["n_components"], s["n_cases"], s["n_quantified"],
        s["n_unquantified"], weld.fmt(s["max_spread"]), weld.fmt(s["bias"])))
print()
print("""
Both seed terms return n_cases = 4 and n_quantified = 0. The two live
readouts return --. On the set as delivered the scorer assigns the two
terms an identical score, and the number it agrees on is the count of
paragraphs someone wrote.

This is C3 ("n_cases alone is insufficient") shown from the drop's own
data rather than argued. It does not CLOSE C3 -- C3's stated falsifier
needs a populated set, and there is none -- but it moves the claim from
asserted to demonstrated on a set of size 2.
""".strip())

# ----------------------------------------------------------------- CW_007
head(11, "CW_007", "one retrieved pair from the first real number")
rows = []
for name in sorted(by_name):
    for d in by_name[name].get("divergences", []):
        r = d.get("readings") or {}
        have = [k for k, v in r.items()
                if weld.rel_change(v) is not None]
        rows.append((name, d["id"], len(r), len(have)))
print()
print("  %-10s %-32s %8s %8s" % ("term", "case", "keys", "usable"))
print("  " + "-" * 62)
for t_, c, k, h in rows:
    print("  %-10s %-32s %8d %8d" % (t_, c, k, h))
print()
print("  %d of %d named cases carry a readings block." % (
    sum(1 for _, _, k, _ in rows if k), len(rows)))
print("  %d carry a usable ratio on any component." % sum(
    1 for _, _, _, h in rows if h >= 1))
print("  %d carry two, which is what a spread needs." % sum(
    1 for _, _, _, h in rows if h >= 2))
print()
print("""
The delivered CLAIM_TABLE.md says "no paired before/after readings
attached", which is accurate. The sharper statement is that the state is
not empty, and the distance to the first number is now measurable rather
than described:

  capital / socialized-downside has risk_bearing at 14.1 -> 2.5 and
  revenue_claim null, with its own source line reading "reported as risen,
  no paired figure retrieved". Its note says the divergence between those
  exact two components "is the entire structure".
""".strip())
print()
print("  fill that one pair (synthetic 1.0 -> 1.2, to size the effect only):")
print("    capital max_spread = %s   -- the folder's first non-'--' readout" %
      weld.fmt(sc["max_spread"], 3))
print("    bias stays %s, per CW_006" % weld.fmt(sc["bias"]))

# ----------------------------------------------------------------- CW_008
head(12, "CW_008", "C1 against the eight, by structure")
print("""
C1's falsifier: showing any of the eight already covers the two seed terms.
The one that gets closest is PROXY SUBSTITUTION -- density is enforceable
and stands where ownership distribution is not read.
""".strip())
print()
for label, structure in EIGHT:
    print("  %-20s %s" % (label, structure))
print()
print("""
The separation is in what each requires to exist. PROXY SUBSTITUTION needs
two named things and a substitution: "fitness to drive" is a phrase, and
"hours since last drive" was written into a rule in its place. The register
entry can name the target it lost.

CATEGORY WELD is the case where there is no second name to point at. There
is one word, and the components were never separately carried, so there is
no substitution event to date and no displaced target to name.

SCALAR DEMAND is the other near miss and it is a different collapse: one
quantity's variation over a domain flattened to a scalar. A weld flattens
N quantities to one handle. Both lose a dimension; they lose different
ones.

C1 survives the check. What the check also shows is that the distinction
runs through CW_002 -- if condition 2 is read as being about English
rather than about the record, PROXY SUBSTITUTION absorbs both seed terms
and C1 falls.
""".strip())

# ----------------------------------------------------------------- CW_009
head(13, "CW_009", "C5 has no denominator")
print("""
C5: "Language models are more prone to welds than to retrieval errors."

That is a comparison of two rates. Neither rate has a denominator here:
prone per what -- per term encountered, per query, per output? And the
stated falsifier ("a model separating components on a term whose corpus
never separates them, without external tooling") requires establishing
that a corpus never separates them, which requires the corpus.

The generation rule the claim rests on is separately statable and does not
need the comparison: a representation summarising contexts of occurrence
has no gradient pulling apart components the contexts never separate. That
is a mechanism, and it is testable on one term at a time -- present a
model a divergence case for a welded term and score whether the components
are held apart without being handed the decomposition.

C5 as written compares two rates with no null. The mechanism under it does
not need the comparison to be checkable. Recorded as a claim that should
be split, not as a claim that is wrong.
""".strip())

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as CW_001..CW_013")
print(BAR)
