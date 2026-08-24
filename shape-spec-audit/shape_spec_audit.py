#!/usr/bin/env python3
"""Checks on ../SHAPE_SPEC.md. stdlib only. CC0.

SHAPE_SPEC.md is delivered verbatim and is not modified by this module.
Everything here is either a computation or a scan of this tree.

The spec is a DEFINITION, so most of it is not the kind of thing that can
be refuted. Three parts of it are:

    section 4   the removal test, and its worked example
    section 6   independent recurrence as the evidence
    section 9   the NOTE ON COST
    section 10  "a repo that says SHAPE means section 1", and the
                four required fields

Those are what this file addresses. Sections 1, 2, 3, 5, 7 and 8 are read
in README.md, where the reading is argument rather than measurement --
except section 7, which has one consequence that is stateable without data
and is stated there.

usage:
    python3 shape_spec_audit.py
    python3 shape_spec_audit.py --selftest
"""
import glob
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SPEC = os.path.join(ROOT, "SHAPE_SPEC.md")


# --------------------------------------------------------------------------
# SS_009 / SS_010 -- section 10's four required fields, applied mechanically.
#
# Section 10:  "a shape entry should carry: solving-for, constraint list,
#               why-not-the-other-shape, and the removal test from
#               section 4"
#              "an entry missing the removal test is a geometry note, not
#               a shape entry; mark it as such"
#
# For a JSON entry the key set is a real schema property, not a word list,
# so this test is not the `nonidentity-census` T1-1 failure. For markdown
# it would be, and no markdown entry is scored here.
# --------------------------------------------------------------------------

REQUIRED = {
    "solving_for": ("solving_for", "solvingfor", "quantity", "distributes"),
    "constraints": ("constraints", "constraint_list", "bounds"),
    "why_not_other": ("why_not", "why_not_the_other_shape", "rival",
                      "other_shape"),
    "removal_test": ("removal_test", "removal", "if_removed",
                     "load_bearing_constraint"),
}


def shape_entries():
    """Every file in this tree filed as a shape entry.

    Two routes in: a file under a `shapes/` directory, or a JSON object
    with a top-level `shape` key. Both are structural, not lexical.
    """
    found = {}
    for p in glob.glob(os.path.join(ROOT, "**", "shapes", "*.json"),
                       recursive=True):
        found[os.path.relpath(p, ROOT)] = "under shapes/"
    for p in glob.glob(os.path.join(ROOT, "**", "*.json"), recursive=True):
        if ".git" in p:
            continue
        try:
            d = json.load(open(p))
        except Exception:
            continue
        if isinstance(d, dict) and "shape" in d:
            found.setdefault(os.path.relpath(p, ROOT), "top-level `shape` key")
    return sorted(found.items())


def score_entry(path):
    d = json.load(open(os.path.join(ROOT, path)))
    keys = set(k.lower() for k in d.keys())
    out = {}
    for field, aliases in REQUIRED.items():
        out[field] = any(a in keys for a in aliases)
    return out, sorted(d.keys())


def required_fields_report():
    rows = []
    for path, route in shape_entries():
        got, keys = score_entry(path)
        rows.append({"path": path, "route": route, "got": got,
                     "n": sum(got.values()), "keys": keys})
    return rows


# --------------------------------------------------------------------------
# SS_006 -- section 9's NOTE ON COST, and whether it survives section 4.
#
# Section 4 says the lung's 2^(-1/3) follows from a fixed enclosing volume.
# Section 9 says to state the second working group as DISSIPATION and not
# as a cost, because cost imports a pricing model.
#
# The literature derivation (Murray 1926) minimises
#     dissipation + K * volume
# and K is a metabolic cost coefficient -- the term section 9 rejects. So
# the question is whether the exponent survives its removal.
#
# It does, and the reason is worth stating: minimising dissipation SUBJECT
# TO a fixed volume and minimising dissipation PLUS a price on volume are
# the same stationarity problem. The cost coefficient is the Lagrange
# multiplier on a physical constraint. Section 9 is right and the proof is
# a duality it does not state.
#
# Everything below is a symmetric bifurcation: one parent carrying Q=2,
# two children carrying Q=1, all segments length L. Poiseuille.
# --------------------------------------------------------------------------

MU = 1.0
L = 1.0


def dissipation(r_p, r_c):
    """8*mu*L*Q^2/(pi*r^4), summed over parent + two children."""
    k = 8.0 * MU * L / math.pi
    return k * (2.0 ** 2 / r_p ** 4 + 2.0 * (1.0 ** 2 / r_c ** 4))


def volume(r_p, r_c):
    return math.pi * L * (r_p ** 2 + 2.0 * r_c ** 2)


def _golden(f, lo, hi, iters=300):
    """Minimise a unimodal f on [lo, hi]. No numpy."""
    g = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = lo, hi
    c, d = b - g * (b - a), a + g * (b - a)
    for _ in range(iters):
        if f(c) < f(d):
            b, d = d, c
            c = b - g * (b - a)
        else:
            a, c = c, d
            d = a + g * (b - a)
    return (a + b) / 2.0


def constrained_ratio(V=10.0):
    """Minimise dissipation at FIXED total volume. No cost term anywhere.

    Eliminates r_p through the volume constraint and searches over r_c.
    """
    def r_p_of(r_c):
        inner = V / (math.pi * L) - 2.0 * r_c ** 2
        return math.sqrt(inner) if inner > 1e-12 else 1e-6

    hi = math.sqrt(V / (math.pi * L) / 2.0) * 0.999
    r_c = _golden(lambda x: dissipation(r_p_of(x), x), 1e-4, hi)
    return r_c / r_p_of(r_c), r_c, r_p_of(r_c)


def priced_ratio(K=1.0):
    """Murray's own form: minimise dissipation + K*volume. K is a cost."""
    def total(r_c):
        # for fixed r_c, minimise over r_p analytically is awkward; nest.
        return _nested(r_c, K)

    def _nested(rc, k):
        return _golden(lambda rp: dissipation(rp, rc) + k * volume(rp, rc),
                       1e-3, 50.0)

    def f(rc):
        rp = _nested(rc, K)
        return dissipation(rp, rc) + K * volume(rp, rc)

    r_c = _golden(f, 1e-3, 50.0)
    r_p = _nested(r_c, K)
    return r_c / r_p, r_c, r_p


def unconstrained_has_no_optimum(scales=(1.0, 10.0, 100.0, 1000.0)):
    """Pure dissipation, nothing else. Strictly decreasing in radius.

    Returned so the claim 'the second term is doing the work' is a
    measurement rather than an assertion.
    """
    return [(s, dissipation(s, s)) for s in scales]


MURRAY = 2.0 ** (-1.0 / 3.0)


# --------------------------------------------------------------------------
# SS_005 -- section 6's recurrence list, and what independence means in it.
#
# The list is grouped by SUBSTRATE. Section 1 says two systems sharing a
# constraint set share a shape. So the count of independent confirmations
# has to be a count of distinct constraint sets, not of distinct materials.
#
# The family assignment below is HAND-ASSIGNED by this audit and is the
# weak point of the finding. It is stated per item so it can be argued
# with rather than inherited.
# --------------------------------------------------------------------------

RECURRENCE = [
    ("vasculature", "transport-under-volume-constraint",
     "Murray class: minimise dissipation at fixed total volume"),
    ("river networks", "erosional-minimum-dissipation",
     "optimal channel networks; erosion sets the boundary it flows in"),
    ("lightning", "laplacian-growth",
     "growth velocity from the gradient of a field obeying nabla^2 phi = 0"),
    ("root systems", "transport-under-volume-constraint",
     "same class as vasculature; foraging term added"),
    ("mycelium", "transport-under-volume-constraint",
     "same class; no enclosing volume, so section 5 external"),
    ("crack propagation", "laplacian-growth",
     "quasi-static brittle case: stress field is harmonic ahead of the tip"),
    ("dendritic solidification", "laplacian-growth",
     "Mullins-Sekerka instability on a diffusion field"),
]


def recurrence_families():
    fam = {}
    for name, f, why in RECURRENCE:
        fam.setdefault(f, []).append(name)
    return fam


def n_eff_upper_bound():
    """Distinct constraint families in the list. An UPPER bound on how
    many independent confirmations the list can carry, not a measurement
    of how many it does carry -- the families could themselves be related.
    """
    return len(recurrence_families())


# --------------------------------------------------------------------------
# SS_002 -- section 10's "a repo that says SHAPE means section 1",
# measured on this tree.
#
# NOT a lexical classifier. A keyword scan deciding word sense is exactly
# `nonidentity-census` T1-1, where 10 of 12 judgements came off a word
# list. The senses below are HAND-CODED from a sample, the sample size is
# reported, and the total is a raw count with no sense attached.
# --------------------------------------------------------------------------

WORD = re.compile(r"\bshapes?\b", re.I)
EXTS = (".md", ".py", ".json")

HAND_CODED = [
    ("shape signature", "sha1 of a record's sorted top-level key names",
     "data-structure fingerprint", "uninstrumented/specimens/"),
    ("the same shape as", "a recurring structural pattern across audits",
     "pattern-across-cases", "throughout"),
    ("distribution shape", "the functional form of a curve",
     "geometry (section 1's readout)", "uninstrumented/, energy/"),
    ("shape in {NEW, FLAT, WALKING}", "an enum label on a residual",
     "enum tag", "instrument-bias-sims/"),
    ("shapes/ directory", "a coverage ledger over a claim",
     "claim-with-a-domain-set", "domain-ledger/"),
    ("the barrier SHAPE is universal", "form-stable across parameters",
     "geometry (section 1's readout)", "simulation-hypothesis-budget/"),
    ("SHAPE BEING TESTED", "a proposed formal family",
     "constraint set (section 1)", "alignment-under-coupling/"),
]


def word_census():
    """Raw count only. No sense assigned mechanically."""
    files, hits = 0, 0
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames
                       if d not in (".git", "__pycache__")]
        for fn in filenames:
            if not fn.endswith(EXTS):
                continue
            p = os.path.join(dirpath, fn)
            if os.path.relpath(p, ROOT) in ("SHAPE_SPEC.md",):
                continue
            try:
                txt = open(p, errors="replace").read()
            except Exception:
                continue
            n = len(WORD.findall(txt))
            if n:
                files += 1
                hits += n
    return files, hits


def senses_in_sample():
    return sorted(set(s for _, _, s, _ in HAND_CODED))


# --------------------------------------------------------------------------
# SS_008 -- the "see also" at the end of section 10.
# --------------------------------------------------------------------------

def reading_protocol_present():
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d != ".git"]
        for fn in filenames:
            if fn.lower().startswith("reading_protocol"):
                return os.path.relpath(os.path.join(dirpath, fn), ROOT)
    return None


def spec_present():
    return os.path.exists(SPEC)


# --------------------------------------------------------------------------

def report():
    print("CHECKS ON SHAPE_SPEC.md -- the spec is not modified here\n")

    print("SS_009/010  section 10's four required fields, applied to")
    print("            every shape entry in this tree")
    rows = required_fields_report()
    if not rows:
        print("  no shape entries found")
    for r in rows:
        print("  %s   (%s)" % (r["path"], r["route"]))
        for f in ("solving_for", "constraints", "why_not_other",
                  "removal_test"):
            print("    %-16s %s" % (f, "present" if r["got"][f] else "ABSENT"))
        print("    score            %d of 4" % r["n"])
        print("    keys it has      %s" % ", ".join(r["keys"]))
    print("  Section 10 offers two outcomes: a shape entry, or a geometry")
    print("  note missing the removal test. The entry found is neither --")
    print("  it has no geometry to note. A third state, with no label.")
    print()

    print("SS_002  'a repo that says SHAPE means section 1', measured")
    files, hits = word_census()
    print("  files using the word : %d" % files)
    print("  occurrences          : %d" % hits)
    print("  senses in a hand-coded sample of %d:" % len(HAND_CODED))
    for use, gloss, sense, where in HAND_CODED:
        print("    %-34s %s" % (use, sense))
    print("  distinct senses in the sample: %d" % len(senses_in_sample()))
    print("  The count above is RAW. No sense was assigned mechanically:")
    print("  a keyword scan deciding word sense is T1-1's failure. The")
    print("  sample is hand-coded, n=%d, and is not a rate." % len(HAND_CODED))
    print()

    print("SS_006  section 9's NOTE ON COST, against section 4's exponent")
    ratio_c, rc, rp = constrained_ratio()
    ratio_p, prc, prp = priced_ratio()
    print("  Murray exponent 2^(-1/3)                = %.6f" % MURRAY)
    print("  min dissipation at FIXED VOLUME, no cost = %.6f" % ratio_c)
    print("  min dissipation + K*volume (a cost)      = %.6f" % ratio_p)
    print("  pure dissipation, nothing else -- W as radius scales:")
    for s, w in unconstrained_has_no_optimum():
        print("    r = %-8.1f W = %.6e" % (s, w))
    print("  strictly decreasing, so no interior optimum and no exponent.")
    print("  The second term is load-bearing. But the de-costed form")
    print("  returns the SAME exponent, because minimising dissipation at")
    print("  fixed volume and minimising dissipation plus a price on")
    print("  volume are one stationarity problem: the cost coefficient IS")
    print("  the Lagrange multiplier on a physical constraint.")
    print("  Section 9 is right, and this is the proof it does not state.")
    print()

    print("SS_005  section 6's recurrence list, counted by constraint set")
    fam = recurrence_families()
    print("  items listed as independent : %d" % len(RECURRENCE))
    print("  distinct constraint families: %d  (upper bound on N_eff)"
          % n_eff_upper_bound())
    for f in sorted(fam):
        print("    %-38s %s" % (f, ", ".join(fam[f])))
    print("  The list is grouped by SUBSTRATE. Section 1 says systems")
    print("  sharing a constraint set share a shape -- so two items in one")
    print("  family are not two confirmations, they are one shape seen")
    print("  twice. The family assignment here is HAND-ASSIGNED and is the")
    print("  weak point; it is stated per item so it can be argued with.")
    print()

    print("SS_008  section 10's 'see also'")
    rp_ = reading_protocol_present()
    print("  READING_PROTOCOL.md : %s" % (rp_ or "NOT IN TREE"))
    print("  SHAPE_SPEC.md       : %s" % ("present" if spec_present()
                                          else "NOT IN TREE"))
    print()


def selftest():
    fails = []

    # SS_006: the two derivations agree with each other and with 2^(-1/3).
    rc, _, _ = constrained_ratio()
    rp_, _, _ = priced_ratio()
    if abs(rc - MURRAY) > 1e-4:
        fails.append("constrained minimisation no longer gives 2^(-1/3): "
                     "%.6f" % rc)
    if abs(rp_ - MURRAY) > 1e-4:
        fails.append("priced minimisation no longer gives 2^(-1/3): "
                     "%.6f" % rp_)
    if abs(rc - rp_) > 1e-4:
        fails.append("the duality claim fails: constrained %.6f vs "
                     "priced %.6f" % (rc, rp_))

    # SS_006: pure dissipation must have no interior optimum.
    ws = [w for _, w in unconstrained_has_no_optimum()]
    if not all(ws[i] > ws[i + 1] for i in range(len(ws) - 1)):
        fails.append("pure dissipation is no longer strictly decreasing; "
                     "SS_006's 'the second term is load-bearing' restated")

    # SS_009: the falsifier is an entry scoring above 0.
    rows = required_fields_report()
    if not rows:
        fails.append("no shape entry found at all; SS_009 has no subject")
    for r in rows:
        if r["n"] > 0:
            fails.append("%s now scores %d of 4; SS_009 must be restated"
                         % (r["path"], r["n"]))

    # SS_005: the falsifier is the families collapsing or splitting.
    if n_eff_upper_bound() >= len(RECURRENCE):
        fails.append("every recurrence item is now its own family; "
                     "SS_005 must be restated")

    # SS_002: the falsifier is one sense across the sample.
    if len(senses_in_sample()) < 2:
        fails.append("the hand-coded sample now carries one sense; "
                     "SS_002 must be restated")

    # SS_008 is a state, not a constant. Assert only that we can read it.
    reading_protocol_present()
    if not spec_present():
        fails.append("SHAPE_SPEC.md is not at the repo root")

    for f in fails:
        print("FAIL: " + f)
    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    report()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
