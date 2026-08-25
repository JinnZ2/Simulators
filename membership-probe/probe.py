#!/usr/bin/env python3
"""
membership-probe — detect a checker that is using an IDEAL RENDERING as a
MEMBERSHIP TEST instead of reading the constraint set.

CC0. stdlib only. No network.

The defect
----------
An ideal form (regular hexagon, symmetric 2^(-1/3) tree, the textbook
anatomical figure) is a RENDERING TARGET: the cleanest thing a human can
draw or compute with. It is a summary of the instances that already carry
the label.

Testing an instance against that summary to decide whether it carries the
label is circular. It excludes nothing except things that were never in
the category, and it rejects every real instance, because no real
instance meets the ideal.

The instrument
--------------
Two trap classes, scored independently of each other:

  trap_a   real member, deviates hard from the ideal.
           an ideal-matcher REJECTS it.  -> false negative

  trap_b   non-member whose GEOMETRY matches the ideal closely,
           sometimes more closely than any real member, but whose
           constraint set is absent.
           an ideal-matcher ACCEPTS it.  -> false positive

  control  unambiguous both ways. gates the run. a checker that fails
           controls is not answering coherently and its trap scores
           mean nothing.

And a second axis that does not depend on the verdicts at all:

  coverage   how much of the case's named constraint set the stated
             basis actually touches. an ideal-matcher talks about
             angles, regularity and symmetry and scores near zero here
             even when it happens to get the verdict right.

Two axes disagreeing is itself informative — see DIAGNOSIS below.

Usage
-----
    python3 probe.py emit             > probes.txt
    (paste probes.txt to the checker, save its reply to answers.txt)
    python3 probe.py score answers.txt
    python3 probe.py selftest         # validate the instrument itself

Answer file format — one block per case, order irrelevant, extra prose
between blocks ignored:

    ### A01
    VERDICT: member
    BASIS: free text, one or more lines

VERDICT must be one of: member | not_member | uncertain
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CASES_PATH = os.path.join(HERE, "cases.json")

VERDICTS = ("member", "not_member", "uncertain")


# ---------------------------------------------------------------- loading

def load_cases(path=CASES_PATH):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)["cases"]


# ------------------------------------------------------------------ emit

PREAMBLE = """\
MEMBERSHIP PROBE
================
For each case below, decide whether the instance is a member of the named
category, and state the basis for the decision.

Answer in exactly this format, one block per case:

    ### <case id>
    VERDICT: member | not_member | uncertain
    BASIS: <your reasoning>

Answer every case. Do not skip any.
"""


def cmd_emit(cases):
    out = [PREAMBLE]
    for c in cases:
        out.append("")
        out.append("### " + c["id"])
        out.append("CATEGORY: " + c["category"])
        out.append("QUESTION: " + c["question"])
        out.append("INSTANCE: " + c["instance"])
        out.append("")
    sys.stdout.write("\n".join(out) + "\n")


# ----------------------------------------------------------------- parse

BLOCK_RE = re.compile(r"^\s*#{2,4}\s*([A-Za-z]\d{2})\b", re.M)


def parse_answers(text):
    """Return {case_id: {'verdict': str|None, 'basis': str}}."""
    out = {}
    marks = list(BLOCK_RE.finditer(text))
    for i, m in enumerate(marks):
        cid = m.group(1).upper()
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[start:end]

        verdict = None
        vm = re.search(r"VERDICT\s*:\s*([A-Za-z_ ]+)", body, re.I)
        if vm:
            raw = vm.group(1).strip().lower().replace(" ", "_")
            raw = raw.split("\n")[0].strip("_")
            for v in VERDICTS:
                if raw.startswith(v):
                    verdict = v
                    break
            if verdict is None and raw.startswith("not"):
                verdict = "not_member"

        bm = re.search(r"BASIS\s*:\s*(.*)", body, re.I | re.S)
        basis = bm.group(1).strip() if bm else body.strip()

        out[cid] = {"verdict": verdict, "basis": basis}
    return out


# --------------------------------------------------------------- scoring

def coverage(basis, constraint_keys):
    """Fraction of named constraint groups touched by the basis text.

    A group is touched if ANY of its synonyms appears. Substring match on
    a lowercased string — deliberately loose, because the question is
    whether the checker went near the constraint at all, not whether it
    used our wording.
    """
    if not constraint_keys:
        return 0.0, []
    low = " ".join(basis.lower().split())
    hit = []
    for name, syns in constraint_keys:
        if any(s.lower() in low for s in syns):
            hit.append(name)
    return len(hit) / float(len(constraint_keys)), hit


def score(cases, answers):
    rows = []
    for c in cases:
        a = answers.get(c["id"])
        if a is None:
            rows.append({
                "id": c["id"], "class": c["class"], "truth": c["ground_truth"],
                "said": None, "outcome": "MISSING", "cov": 0.0, "hits": [],
                "category": c["category"],
            })
            continue

        said = a["verdict"]
        truth = c["ground_truth"]
        cov, hits = coverage(a["basis"], c["constraint_keys"])

        if said is None:
            outcome = "UNPARSED"
        elif said == "uncertain":
            outcome = "uncertain"
        elif said == truth:
            outcome = "correct"
        elif truth == "member":
            outcome = "FALSE_NEG"
        else:
            outcome = "FALSE_POS"

        rows.append({
            "id": c["id"], "class": c["class"], "truth": truth,
            "said": said, "outcome": outcome, "cov": cov, "hits": hits,
            "category": c["category"],
        })
    return rows


def rate(rows, cls, outcome):
    sub = [r for r in rows if r["class"] == cls]
    if not sub:
        return 0.0, 0, 0
    n = sum(1 for r in sub if r["outcome"] == outcome)
    return n / float(len(sub)), n, len(sub)


def mean_cov(rows, cls=None):
    sub = rows if cls is None else [r for r in rows if r["class"] == cls]
    sub = [r for r in sub if r["outcome"] not in ("MISSING", "UNPARSED")]
    if not sub:
        return 0.0
    return sum(r["cov"] for r in sub) / float(len(sub))


# ---------------------------------------------------------------- report

W_ID, W_CLS, W_TRUTH, W_SAID, W_OUT = 5, 8, 11, 11, 10


def trunc(s, w):
    s = "" if s is None else str(s)
    return s if len(s) <= w else s[:w - 1] + "…"


def cmd_score(cases, path):
    with open(path, "r", encoding="utf-8") as fh:
        answers = parse_answers(fh.read())
    rows = score(cases, answers)
    report(rows)
    return rows


def report(rows):
    hdr = ("id".ljust(W_ID) + "class".ljust(W_CLS) + "truth".ljust(W_TRUTH)
           + "said".ljust(W_SAID) + "outcome".ljust(W_OUT) + "cov")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(trunc(r["id"], W_ID).ljust(W_ID)
              + trunc(r["class"], W_CLS).ljust(W_CLS)
              + trunc(r["truth"], W_TRUTH).ljust(W_TRUTH)
              + trunc(r["said"], W_SAID).ljust(W_SAID)
              + trunc(r["outcome"], W_OUT).ljust(W_OUT)
              + ("%.2f" % r["cov"]))

    ctrl_ok, cn, ct = rate(rows, "control", "correct")
    fn, an, at = rate(rows, "trap_a", "FALSE_NEG")
    fp, bn, bt = rate(rows, "trap_b", "FALSE_POS")

    print("")
    print("controls correct   %d/%d   (%.2f)" % (cn, ct, ctrl_ok))
    print("trap_a  FALSE_NEG  %d/%d   (%.2f)   <- ideal-matcher rejects real members"
          % (an, at, fn))
    print("trap_b  FALSE_POS  %d/%d   (%.2f)   <- ideal-matcher accepts geometry mimics"
          % (bn, bt, fp))
    print("")
    print("constraint coverage   all %.2f   trap_a %.2f   trap_b %.2f"
          % (mean_cov(rows), mean_cov(rows, "trap_a"), mean_cov(rows, "trap_b")))
    print("")
    diagnose(rows, ctrl_ok, fn, fp)


def diagnose(rows, ctrl_ok, fn, fp):
    cov = mean_cov(rows)
    trap_err = 0.5 * (fn + fp)

    print("DIAGNOSIS")
    print("---------")

    missing = [r["id"] for r in rows if r["outcome"] in ("MISSING", "UNPARSED")]
    if missing:
        print("  unparsed/missing: " + ", ".join(missing))

    if ctrl_ok < 0.75:
        print("  RUN INVALID — controls failed. The checker is not answering")
        print("  the question coherently. Trap scores below are meaningless.")
        return

    if trap_err >= 0.4 and cov < 0.40:
        verdict = "IDEAL-MATCHER (confirmed on both axes)"
        note = ("Verdicts fail in the ideal-matcher direction AND the stated\n"
                "  basis does not touch the constraint sets. This is the defect.")
    elif trap_err >= 0.4:
        verdict = "IDEAL-MATCHER (verdict axis only)"
        note = ("Verdicts fail in the ideal-matcher direction while the basis\n"
                "  does mention constraints. Constraint language present but not\n"
                "  load-bearing — the decision is still being made on form.")
    elif cov < 0.40:
        verdict = "UNDETERMINED — right answers, unstated basis"
        note = ("Verdicts are fine but the basis does not touch the constraint\n"
                "  sets. Could be a constraint reader that answered tersely, or a\n"
                "  matcher that got lucky on this case set. Re-run demanding the\n"
                "  basis enumerate which constraints are satisfied and which are not.")
    else:
        verdict = "CONSTRAINT READER"
        note = ("Both trap classes survived and the basis engages the constraint\n"
                "  sets. Safe to hand constraint-set work to this checker.")

    print("  " + verdict)
    print("  " + note)

    a_fails = [r["id"] for r in rows if r["class"] == "trap_a" and r["outcome"] == "FALSE_NEG"]
    b_fails = [r["id"] for r in rows if r["class"] == "trap_b" and r["outcome"] == "FALSE_POS"]
    if a_fails:
        print("")
        print("  rejected real members: " + ", ".join(a_fails))
    if b_fails:
        print("  accepted mimics:       " + ", ".join(b_fails))

    hedged = [r["id"] for r in rows if r["outcome"] == "uncertain"]
    if hedged:
        print("  hedged:                " + ", ".join(hedged))
        print("  (uncertain is not scored as an error. A high hedge count with")
        print("   low coverage is the same defect wearing a hat.)")


# -------------------------------------------------------------- selftest

FAKE_MATCHER = {
    "A01": ("not_member", "The cell walls are not straight and the interior angles depart from 120 degrees, so this is not a regular hexagon."),
    "A02": ("not_member", "Generation count is variable and the radius ratios do not hold to 2^(-1/3), so the structure does not match the idealized tree."),
    "A03": ("not_member", "Many columns have four, five or seven sides. The hexagonal description does not hold."),
    "A04": ("not_member", "The plan form is lopsided and does not resemble a symmetric radial fan."),
    "A05": ("not_member", "Junctions at 90 degrees and irregular cell sizes. Not a hexagonal tiling."),
    "A06": ("uncertain", "Organ laterality, digit count and limb structure all depart from the standard anatomical figure."),
    "A07": ("not_member", "No engine installed, no doors, no seats. It does not match a complete road-ready vehicle."),
    "B01": ("member", "Clean six-fold symmetry, a very close match to the hexagonal form."),
    "B02": ("member", "Regular hexagons within tolerance. An excellent match to hexagonal tiling."),
    "B03": ("member", "Self-similar dichotomous branching over eight generations with a consistent taper. Matches the branching tree form."),
    "B04": ("member", "Clear dendritic branching plan form, trunk to limbs to twigs."),
    "B05": ("member", "Proportions and surfaces match a complete sedan exactly."),
    "C01": ("member", "Standard branching tree, matches the form."),
    "C02": ("member", "Complete production sedan, matches."),
    "C03": ("not_member", "A bicycle, two wheels, does not match a car."),
    "C04": ("not_member", "A solid boulder, no hexagonal structure at all."),
}

FAKE_READER = {
    "A01": ("member", "Equal-volume partition of the plane with no gaps, under minimum wall material, built outward by agents from circular starts with the wax softening under surface tension. All constraints present; the angle scatter is the readout, not the criterion."),
    "A02": ("member", "Flow is conserved through junctions, dissipation is minimized against a volume enclosure limit, surface area is delivered for gas exchange, built by a growth process. The 2^(-1/3) is a population central tendency, not a spec."),
    "A03": ("member", "Thermal contraction on cooling, crack propagation relieving stress at minimum surface energy, partition of the plane under near-isotropic in-plane stress, cooling front advancing. Non-hexagonal columns are expected where stress was not uniform."),
    "A04": ("member", "Sediment supply and deposition present, channel avulsion branching where it can, gradient to base level. The bedrock is a heterogeneous erodibility constraint; the asymmetric plan is a transcript of the terrain."),
    "A05": ("member", "Desiccation contraction, crack propagation under tensile stress relief, layer thickness setting cell scale. The 90 degree junctions indicate sequential rather than simultaneous cracking, which is a constraint readout."),
    "A06": ("member", "Membership is not defined by matching the textbook reference figure. That figure is a summary derived from the instances; testing an instance against it is circular. Variation on laterality and digit count is within the population."),
    "A07": ("member", "Car is a conventional designed category, not a physics-read constraint set. Function and identity continue through disassembly — same registered vehicle, being reassembled. Present operability is not the criterion."),
    "B01": ("not_member", "The six-fold symmetry comes from the ice crystal lattice bond angle and diffusion-limited growth. There is no partition into equal-volume cells and no material minimization. Same geometry, different constraint set."),
    "B02": ("not_member", "The hexagon was imposed by a die and chosen as a design decision. Nothing is stored, so there is no equal-volume partition requirement, and grout is not being minimized. Geometry matches, constraint set does not."),
    "B03": ("not_member", "Nothing flows through it, so there is no dissipation to minimize. The taper ratio is a parameter specified by the author, not a result. Form without the constraint set."),
    "B04": ("not_member", "Forged by a smith as a decorative motif. No erosion, no sediment, no water. Constraints are structural and aesthetic. Geometry matches, constraint set does not."),
    "B05": ("not_member", "Solid clay, no drivetrain, cannot move under power. It exists to be looked at as a design reference. The form is the output rather than a consequence of function."),
    "C01": ("member", "Conserved blood flow, dissipation minimized against resistance, delivery to distributed tissue sinks."),
    "C02": ("member", "Complete production vehicle, designed spec satisfied and function operable."),
    "C03": ("not_member", "A bicycle — human-powered, two wheels, a different vehicle category."),
    "C04": ("not_member", "Solid and undivided. No partition into cells at all."),
}


def render_fake(table):
    out = []
    for cid in sorted(table):
        v, b = table[cid]
        out.append("### %s\nVERDICT: %s\nBASIS: %s\n" % (cid, v, b))
    return "\n".join(out)


def cmd_selftest(cases):
    for name, table in (("SYNTHETIC IDEAL-MATCHER", FAKE_MATCHER),
                        ("SYNTHETIC CONSTRAINT READER", FAKE_READER)):
        print("=" * 62)
        print(name)
        print("=" * 62)
        rows = score(cases, parse_answers(render_fake(table)))
        report(rows)
        print("")
    print("The instrument is working if the first block diagnoses")
    print("IDEAL-MATCHER and the second diagnoses CONSTRAINT READER.")
    print("If it does not, the instrument is defective, not the checker.")


# ------------------------------------------------------------------ main

def main(argv):
    cases = load_cases()
    if len(argv) < 2:
        sys.stdout.write(__doc__)
        return 0
    cmd = argv[1]
    if cmd == "emit":
        cmd_emit(cases)
    elif cmd == "score":
        if len(argv) < 3:
            print("usage: probe.py score <answers.txt>")
            return 2
        cmd_score(cases, argv[2])
    elif cmd == "selftest":
        cmd_selftest(cases)
    else:
        print("unknown command: " + cmd)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
