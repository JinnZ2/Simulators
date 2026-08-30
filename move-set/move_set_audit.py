#!/usr/bin/env python3
"""Checks on the delivered `move_set_sim.py` and its filled ledger.

Both are imported and read; neither is modified.

The module's stated purpose is a scoring asymmetry: *a correctly-refused
verdict scores as high as a correct one*, because evals that score
answers only never select for the absence moves. That is the right
target and this folder's whole subject, so what is checked here is
whether the implementation can tell an earned refusal from a typed one,
and whether the falsifier it ships can fail.

Three arms:

  SCORER      null-tested. A garbage ledger is run against the real
              scorer and the score is reported. A scorer that cannot
              separate a real refusal from a fabricated one is not
              measuring the thing the module exists for.
  FALSIFIER   `path_dependence` at 0, 1 and n runs. A falsifier that
              returns a verdict on no data, or a pass on one run, has
              not been given a chance to fail.
  LEDGER      the delivered run, read for internal consistency. Every
              quoted string is present in the file and asserted, so a
              later edit turns these red rather than leaving the
              reading stranded.
  SPLIT       the M6 family. A second drop split one absence move into
              six, and the delivered ledger predates the split, so it
              is the legacy case its own compatibility path handles.

CC0. stdlib only. Parses under Python 3.9.
"""

import copy
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import move_set_sim as M  # noqa: E402

LEDGER = os.path.join(HERE, "ledgers", "wolf_dominance.json")


def load():
    return json.load(open(LEDGER, encoding="utf-8"))


# ------------------------------------------------------------- arms

def garbage_ledger():
    """A ledger with the right SHAPE and no content.

    Every refusal carries a blocker and an unblocker, as the rule
    requires. Neither says anything. This is what the anti-gaming guard
    is supposed to catch, since it is exactly the bare 'I don't know'
    the docstring names, wearing the required fields.
    """
    out = []
    for m, spec in M.MOVES.items():
        v = next((x for x in spec["admits"] if x in M.REFUSALS), None)
        if v is None:
            v = spec["admits"][0]
        e = {"move": m, "verdict": v}
        if v in M.ANSWERS:
            e["evidence_locator"] = "x"
        else:
            e["blocker"] = "x"
            e["unblocker"] = "x"
        out.append(e)
    return out


def all_resolved_ledger():
    """The opposite arm: every move answered, one character of evidence."""
    return [{"move": m, "verdict": "RESOLVED", "evidence_locator": "x"}
            for m, spec in M.MOVES.items() if "RESOLVED" in spec["admits"]]


def falsifier_edges():
    """path_dependence at 0, 1, and two disagreeing runs."""
    real = load()
    other = copy.deepcopy(real)
    other[0]["verdict"] = "INSTRUMENT_BLIND"      # admissible for M1
    return {
        "zero_runs": M.path_dependence([]),
        "one_run": M.path_dependence([real]),
        "two_same": M.path_dependence([real, copy.deepcopy(real)]),
        "two_shuffled": M.path_dependence([real, list(reversed(real))]),
        "two_differing": M.path_dependence([real, other]),
    }


# ---- the M6 split -------------------------------------------------

def legacy_reading():
    """What the pre-split bundle does to the two readouts.

    The drop anticipated the comparability problem and emits a row
    saying so. That row addresses the TOTAL. The same bundling also
    reaches the completeness readout, which nothing says anything
    about.
    """
    real = load()
    r = M.score(real)
    bundled = [e for e in real if e.get("move") in M.LEGACY]
    return {
        "ledger_is_legacy": bool(bundled),
        "total": r["total"],
        "possible": r["possible"],
        "moves_not_run": r["moves_not_run"],
        "submoves_reported_missing": [m for m in r["moves_not_run"]
                                      if m.startswith("M6")],
        "split_row_emitted": any("SPANS THE M6 SPLIT" in row["note"]
                                 for row in r["rows"]),
        "unreachable_points": r["possible"] - r["total"],
    }


def legacy_admits_derivable():
    """LEGACY_ADMITS is a literal. Is it what its successors admit?"""
    union = set()
    for k in M.LEGACY["M6_absence"]:
        union |= set(M.MOVES[k]["admits"])
    src = open(os.path.join(HERE, "move_set_sim.py"), encoding="utf-8").read()
    return {
        "matches_union_today": set(M.LEGACY_ADMITS) == union,
        "admitted_by_no_successor": sorted(set(M.LEGACY_ADMITS) - union),
        "is_a_literal": "LEGACY_ADMITS = [" in src,
        "derived_from_MOVES": "LEGACY_ADMITS" in src.split("def ")[0]
                              and "MOVES[" in src.split(
                                  "LEGACY_ADMITS")[1].split("]")[0],
        "per_verdict": {v: sum(1 for k in M.LEGACY["M6_absence"]
                               if v in M.MOVES[k]["admits"])
                        for v in sorted(M.LEGACY_ADMITS)},
    }


def split_arithmetic():
    """The stated reason for the split against the split's own size."""
    src = open(os.path.join(HERE, "move_set_sim.py"), encoding="utf-8").read()
    # the sentence wraps across a comment line, so the newline plus the
    # `# ` prefix has to come out before it can be matched at all.
    flat = " ".join(re.sub(r"\n\s*#\s?", " ", src).split())
    m = re.search(r"produced (\w+) findings in a single pass", flat)
    words = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6}
    return {
        "stated": m.group(1) if m else None,
        "stated_n": words.get(m.group(1)) if m else None,
        "submoves_created": len(M.LEGACY["M6_absence"]),
        "moves_before": len(M.MOVES) - len(M.LEGACY["M6_absence"]) + 1,
        "moves_after": len(M.MOVES),
    }


def prior_art_coverage():
    pa = {k: v.get("prior_art") for k, v in M.MOVES.items()}
    return {
        "with": sorted(k for k, v in pa.items() if v),
        "without": sorted(k for k, v in pa.items() if not v),
        "every_m6_has_one": all(pa[k] for k in M.LEGACY["M6_absence"]),
    }


def cli(args):
    p = subprocess.run([sys.executable, os.path.join(HERE, "move_set_sim.py")]
                       + args, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, timeout=60)
    return p.returncode, p.stdout.decode("utf8", "replace")


# ---- the one cross-entry reading, pinned to strings in the file ----
#
# DECLARED, not inferred. Whether two prose entries contradict is a
# judgement, and a scanner that guessed would be reporting its guess.
# What is mechanical is that both strings are in the delivered file --
# asserted below, so an edit to the ledger turns the reading red instead
# of leaving it pointing at text that has moved.
CONTRADICTION = {
    "on": "venue tier",
    "M3_relation_held": "Author prestige, field, and venue-tier confounds "
                        "drop out of the ratio.",
    "M5_self_report": "A book still in print is undercounted by "
                      "Scholar/Scopus relative to a journal article",
    "reading": "M3 says venue tier drops out because the author is the same. "
               "M5 says venue tier is the blocker. Both are about the SAME "
               "pair, and M3's own locator names them: a 1970 BOOK and a "
               "1999 ARTICLE. Same author holds prestige and field fixed; it "
               "does not hold venue fixed, and here venue is maximally "
               "different. The control M3 calls unusually clean is clean on "
               "two of the three confounds it lists.",
}


def contradiction_present():
    raw = open(LEDGER, encoding="utf-8").read()
    return {k: (v in raw) for k, v in CONTRADICTION.items()
            if k.startswith("M")}


# ---------------------------------------------------------- report

def render():
    out = []
    out.append("MOVE SET AUDIT -- checks on the delivered move_set_sim.py")
    out.append("the module and the ledger are imported and read, not edited")
    out.append("")

    real = load()
    s = M.score(real)
    out.append("1. THE DELIVERED LEDGER")
    out.append("   total %.1f of %.1f, refusal fraction %s, moves not run: %s"
               % (s["total"], s["possible"], s["refusal_fraction"],
                  s["moves_not_run"] or "none"))
    for r in s["rows"]:
        out.append("     %-18s %-18s %.1f  %s"
                   % (r["move"], r["verdict"], r["points"], r["note"]))
    out.append("")

    out.append("2. THE SCORER, NULL-TESTED")
    g = M.score(garbage_ledger())
    a = M.score(all_resolved_ledger())
    out.append("   a ledger of one-character blockers and unblockers:")
    out.append("     total %.1f of %.1f, refusal fraction %s"
               % (g["total"], g["possible"], g["refusal_fraction"]))
    out.append("   a ledger of one-character evidence locators:")
    out.append("     total %.1f of %.1f, refusal fraction %s"
               % (a["total"], a["possible"], a["refusal_fraction"]))
    out.append("   The delivered run scores %.1f. The scorer separates"
               % s["total"])
    out.append("   these three by %s."
               % ("nothing" if g["total"] == s["total"] else "some margin"))
    out.append("")
    out.append("   The rule says a bare 'I don't know' is not a refusal.")
    out.append("   The implementation checks that two strings are")
    out.append("   non-empty. `x` is non-empty.")
    out.append("")

    out.append("3. THE FALSIFIER, AT ITS EDGES")
    fe = falsifier_edges()
    for k in ("zero_runs", "one_run", "two_same", "two_shuffled",
              "two_differing"):
        r = fe[k]
        out.append("   %-14s runs=%d orderless=%-5s %s"
                   % (k, r["runs"], r["orderless"], r["verdict"][:44]))
    out.append("")
    out.append("   Zero runs returns a positive finding of order")
    out.append("   dependence. One run returns a pass. Neither is a")
    out.append("   measurement: the comparison takes at least two runs of")
    out.append("   the same artifact under different orders, and nothing")
    out.append("   in the function requires that.")
    out.append("")

    out.append("4. WHAT THE FALSIFIER COMPARES")
    out.append("   the key is (move, verdict). Blocker, unblocker and")
    out.append("   evidence_locator are not compared, so two runs reaching")
    out.append("   the same verdict for different stated reasons read as")
    out.append("   stable. Whether that is right depends on whether the")
    out.append("   claim is about the finding SET or about the finding.")
    out.append("   The docstring says finding SET, so this matches, and")
    out.append("   the consequence is that the harness cannot see a run")
    out.append("   that arrived by a different route.")
    out.append("")

    out.append("5. NO_FINDING SCORES ZERO")
    out.append("   M6 runs on every artifact and admits NO_FINDING, which")
    out.append("   falls in NULL and scores 0. Under a rule whose whole")
    out.append("   point is that a refusal scores as high as an answer,")
    out.append("   'I looked and nothing is hidden here' is the one")
    out.append("   outcome that costs a point.")
    nf = M.score([{"move": "M6_absence", "verdict": "NO_FINDING",
                   "blocker": "", "unblocker": ""}])
    out.append("   measured: %.1f, note %r"
               % (nf["total"], nf["rows"][0]["note"]))
    out.append("")

    out.append("6. CLI EDGES")
    for args, label in ((["--score", LEDGER], "--score <ledger>"),
                        (["--score", "nosuch.json"], "--score missing file"),
                        (["--emit"], "--emit with no artifact"),
                        (["--paths"], "--paths with no runs"),
                        ([], "no argument")):
        rc, o = cli(args)
        last = [x for x in o.strip().split("\n") if x.strip()]
        out.append("   %-24s rc=%-3s %s"
                   % (label, rc, (last[-1] if last else "")[:44]))
    out.append("")

    out.append("7. THE LEDGER, READ FOR INTERNAL CONSISTENCY")
    present = contradiction_present()
    out.append("   both quoted strings present in the delivered file: %s"
               % all(present.values()))
    out.append("   on: %s" % CONTRADICTION["on"])
    out.append("     M3: %s" % CONTRADICTION["M3_relation_held"])
    out.append("     M5: %s" % CONTRADICTION["M5_self_report"])
    for line in _wrap(CONTRADICTION["reading"], 66):
        out.append("   " + line)
    out.append("")
    out.append("   Nothing in the harness compares entries to each other.")
    out.append("   An orderless move set has no place to put a finding")
    out.append("   that only exists between two moves.")
    out.append("8. THE M6 SPLIT, AND WHAT THE COMPATIBILITY PATH REACHES")
    lr = legacy_reading()
    sa = split_arithmetic()
    out.append("   moves: %d before the split, %d after"
               % (sa["moves_before"], sa["moves_after"]))
    out.append("   the split's stated reason names %s findings; it"
               % sa["stated"])
    out.append("   creates %d sub-moves." % sa["submoves_created"])
    out.append("")
    out.append("   the delivered ledger is pre-split: %s"
               % lr["ledger_is_legacy"])
    out.append("   score                : %.1f of %.1f"
               % (lr["total"], lr["possible"]))
    out.append("   the SPLIT row is emitted: %s" % lr["split_row_emitted"])
    out.append("   moves_not_run        : %s"
               % (lr["moves_not_run"] or "[] -- nothing reported missing"))
    out.append("   sub-moves reported missing: %d of 6"
               % len(lr["submoves_reported_missing"]))
    out.append("   -- `seen.update(LEGACY[mv])` marks all six sub-moves")
    out.append("      run from one bundled entry, so the completeness")
    out.append("      readout says nothing is missing while %.1f points"
               % lr["unreachable_points"])
    out.append("      of the denominator are unreachable. The drop")
    out.append("      anticipated the comparability gap and the row")
    out.append("      it emits addresses the TOTAL; the same bundling")
    out.append("      reaches the second readout and nothing says so.")
    out.append("")
    la = legacy_admits_derivable()
    out.append("   LEGACY_ADMITS is exactly its successors' union: %s"
               % la["matches_union_today"])
    out.append("   admitted by the bundle and by no successor: %s"
               % (la["admitted_by_no_successor"] or "none"))
    out.append("   it is a hand-written literal: %s" % la["is_a_literal"])
    for v in sorted(la["per_verdict"]):
        out.append("     %-18s admitted by %d of 6 successors"
                   % (v, la["per_verdict"][v]))
    out.append("   -- correct today and unmaintained by construction:")
    out.append("      the union is one comprehension over LEGACY and")
    out.append("      MOVES, and a change to any sub-move's admits list")
    out.append("      moves the union and not the literal.")
    out.append("")
    pa = prior_art_coverage()
    out.append("   prior art named on %d of %d moves"
               % (len(pa["with"]), len(M.MOVES)))
    out.append("   without: %s" % ", ".join(pa["without"]))
    out.append("   -- every M6 sub-move has one, which is the point of")
    out.append("      the split. The comment explains M1's and M3's")
    out.append("      additions and does not say whether the other")
    out.append("      three have no prior art or were not looked up.")
    out.append("")
    return "\n".join(out)


def _wrap(text, width):
    words, line, out = text.split(), "", []
    for w in words:
        if len(line) + len(w) + 1 > width:
            out.append(line)
            line = w
        else:
            line = (line + " " + w).strip()
    if line:
        out.append(line)
    return out


# --------------------------------------------------------- selftest

def selftest():
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    real = load()

    # -- the delivered ledger. It predates the M6 split, so a move
    #    id in it may be a bundle rather than a move.
    def admits_of(mv):
        if mv in M.LEGACY:
            return M.LEGACY_ADMITS
        return M.MOVES[mv]["admits"]

    chk("the ledger runs one entry per pre-split move",
        len(real) == len(M.MOVES) - len(M.LEGACY["M6_absence"]) + 1)
    chk("every verdict is admissible for its move",
        all(e["verdict"] in admits_of(e["move"]) for e in real))
    s = M.score(real)
    chk("the delivered ledger scores full on the moves it ran",
        s["total"] == 6.0)
    chk("and the denominator is the post-split one",
        s["possible"] == 11.0)
    chk("no move is reported missing", s["moves_not_run"] == [])
    chk("refusal fraction is reported", s["refusal_fraction"] == 0.67)
    chk("four of six verdicts are refusals",
        sum(1 for e in real if e["verdict"] in M.REFUSALS) == 4)
    chk("every refusal carries a blocker and an unblocker",
        all(e.get("blocker") and e.get("unblocker") for e in real
            if e["verdict"] in M.REFUSALS))
    chk("every RESOLVED carries a locator",
        all(e.get("evidence_locator") for e in real
            if e["verdict"] == "RESOLVED"))

    # -- the scorer, null-tested. This is the finding.
    g = M.score(garbage_ledger())
    chk("a one-character-blocker ledger scores full",
        g["total"] == g["possible"])
    chk("the real ledger does not out-score it",
        s["total"] <= g["total"])
    # the split moved the ceiling and not the gate: an ungrounded
    # ledger is worth 11 where it was worth 6, and nothing in
    # score_entry changed.
    chk("the split raised what a garbage ledger is worth",
        g["total"] == float(len(M.MOVES)) > 6.0)
    chk("and the gate is still two non-empty strings",
        M.score_entry({"verdict": "NOT_DERIVABLE",
                       "blocker": "x", "unblocker": "x"})[0] == 1.0)
    a = M.score(all_resolved_ledger())
    chk("a one-character-locator ledger also scores full",
        a["total"] == float(len(a["rows"])))
    chk("an empty blocker IS caught",
        M.score_entry({"verdict": "NOT_DERIVABLE", "blocker": "",
                       "unblocker": "y"})[0] == 0.0)
    chk("a missing unblocker IS caught",
        M.score_entry({"verdict": "NOT_DERIVABLE",
                       "blocker": "y"})[0] == 0.0)
    chk("a RESOLVED with no locator is caught",
        M.score_entry({"verdict": "RESOLVED"})[0] == 0.0)
    chk("an inadmissible verdict scores zero",
        M.score([{"move": "M1_provenance", "verdict": "SHARE_IS_NONE",
                  "blocker": "y", "unblocker": "y"}])["total"] == 0.0)

    # -- the falsifier, at its edges
    fe = falsifier_edges()
    chk("zero runs returns a positive order-dependence finding",
        fe["zero_runs"]["runs"] == 0
        and fe["zero_runs"]["orderless"] is False)
    chk("one run returns a pass", fe["one_run"]["orderless"] is True)
    chk("two identical runs are stable", fe["two_same"]["orderless"] is True)
    chk("reversing the entry order does not move the verdict",
        fe["two_shuffled"]["orderless"] is True)
    chk("a differing verdict is detected",
        fe["two_differing"]["orderless"] is False)
    chk("the differing finding is named",
        fe["two_differing"]["order_sensitive_findings"])

    # -- what the falsifier compares
    r2 = copy.deepcopy(real)
    for e in r2:
        if "blocker" in e:
            e["blocker"] = "a completely different reason"
    chk("two runs with the same verdicts and different reasons read stable",
        M.path_dependence([real, r2])["orderless"] is True)

    # -- NO_FINDING. The split narrowed where it is admissible: it was
    #    on the one absence move and is now on two of six sub-moves.
    nf = M.score([{"move": "M6a_sequence_gap", "verdict": "NO_FINDING"}])
    chk("NO_FINDING scores zero", nf["total"] == 0.0)
    chk("NO_FINDING is admissible somewhere",
        any("NO_FINDING" in v["admits"] for v in M.MOVES.values()))
    nf_moves = [k for k, v in M.MOVES.items() if "NO_FINDING" in v["admits"]]
    chk("on two of the six absence sub-moves", len(nf_moves) == 2)
    chk("and on no move outside the M6 family",
        all(k.startswith("M6") for k in nf_moves))
    chk("NO_FINDING is not counted as a refusal",
        nf["refusal_fraction"] == 0.0)
    chk("the bundle admitted it too", "NO_FINDING" in M.LEGACY_ADMITS)

    # -- emit
    e7 = M.emit("probe", 7)
    e7b = M.emit("probe", 7)
    chk("a seeded emit is deterministic", e7["order"] == e7b["order"])
    chk("emit covers every move", sorted(e7["order"]) == sorted(M.MOVES))
    chk("emit carries the admits list per move",
        all(p["admits"] == M.MOVES[p["move"]]["admits"]
            for p in e7["prompts"]))
    chk("emit ships the ledger schema",
        set(e7["ledger_schema"]) >= {"move", "verdict", "blocker",
                                     "unblocker"})
    orders = {tuple(M.emit("p", i)["order"]) for i in range(12)}
    chk("different seeds give different orders", len(orders) > 1)

    # -- CLI
    rc, o = cli(["--score", LEDGER])
    chk("--score on the delivered ledger exits 0", rc == 0)
    rc, o = cli(["--score", "nosuch_xyz.json"])
    chk("--score on a missing file raises rather than reporting",
        rc != 0 and "FileNotFoundError" in o)
    rc, o = cli(["--emit"])
    chk("--emit with no artifact falls through to the help text",
        rc == 0 and "M1_provenance" in o)
    rc, o = cli([])
    chk("no argument prints the move set",
        rc == 0 and all(m in o for m in M.MOVES))
    chk("and the pre-split bundle is not one of them",
        "M6_absence" not in o)

    # -- 8. the M6 split
    lr = legacy_reading()
    chk("the delivered ledger is the legacy case", lr["ledger_is_legacy"])
    chk("the SPLIT row is emitted", lr["split_row_emitted"])
    chk("and it addresses the total", lr["unreachable_points"] == 5.0)
    chk("while the completeness readout reports nothing missing",
        lr["moves_not_run"] == [])
    chk("no sub-move is reported missing",
        lr["submoves_reported_missing"] == [])
    chk("one bundled entry marks six sub-moves as run",
        len(M.score([{"move": "M6_absence", "verdict": "NOT_ADDRESSABLE",
                      "blocker": "b", "unblocker": "u"}])["moves_not_run"])
        == len(M.MOVES) - len(M.LEGACY["M6_absence"]))

    la = legacy_admits_derivable()
    chk("LEGACY_ADMITS is exactly its successors' union",
        la["matches_union_today"])
    chk("nothing is admitted by the bundle and no successor",
        la["admitted_by_no_successor"] == [])
    chk("it is a hand-written literal", la["is_a_literal"])
    chk("not derived from LEGACY and MOVES", not la["derived_from_MOVES"])
    chk("four of seven verdicts are admitted by one or two successors",
        sum(1 for n in la["per_verdict"].values() if n <= 2) == 4)

    sa = split_arithmetic()
    chk("the stated reason names a number", sa["stated_n"] is not None)
    chk("and it is not the number of sub-moves",
        sa["stated_n"] != sa["submoves_created"])
    chk("the move set went 6 to 11",
        (sa["moves_before"], sa["moves_after"]) == (6, 11))

    pa = prior_art_coverage()
    chk("every M6 sub-move names prior art", pa["every_m6_has_one"])
    chk("three moves name none", len(pa["without"]) == 3)
    chk("and they are the three the comment does not mention",
        set(pa["without"]) == {"M2_substitution", "M4_perturb",
                               "M5_self_report"})

    # -- the pinned cross-entry reading
    present = contradiction_present()
    chk("the M3 string is in the delivered ledger",
        present["M3_relation_held"])
    chk("the M5 string is in the delivered ledger",
        present["M5_self_report"])
    chk("M3's own locator names a book and an article",
        "1970" in json.dumps(real) and "Can. J. Zool" in json.dumps(real))

    # -- render
    txt = render()
    chk("render names all seven sections",
        all(("%d." % i) in txt for i in range(1, 8)))
    chk("render reports the null test", "null-tested" in txt.lower())

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
