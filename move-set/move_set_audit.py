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

CC0. stdlib only. Parses under Python 3.9.
"""

import copy
import json
import os
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

    # -- the delivered ledger
    chk("the ledger runs every move", len(real) == len(M.MOVES))
    chk("every verdict is admissible for its move",
        all(e["verdict"] in M.MOVES[e["move"]]["admits"] for e in real))
    s = M.score(real)
    chk("the delivered ledger scores full", s["total"] == 6.0)
    chk("no move is missing", s["moves_not_run"] == [])
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
    chk("a one-character-blocker ledger scores full", g["total"] == 6.0)
    chk("it scores exactly what the real ledger scores",
        g["total"] == s["total"])
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

    # -- NO_FINDING
    nf = M.score([{"move": "M6_absence", "verdict": "NO_FINDING"}])
    chk("NO_FINDING scores zero", nf["total"] == 0.0)
    chk("NO_FINDING is admissible for M6",
        "NO_FINDING" in M.MOVES["M6_absence"]["admits"])
    chk("NO_FINDING is not counted as a refusal",
        nf["refusal_fraction"] == 0.0)

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
    chk("no argument prints the move set", rc == 0 and "M6_absence" in o)

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
