"""
harness_audit.py -- grade the harness, not the greenhouse.

CC0-1.0. Standard library only. Deterministic. Imports the delivered file;
modifies nothing.

The delivered harness is a claim table with runnable predicates and a
refutation protocol. Its subject is a published greenhouse result. THIS file
does not touch that subject -- it has no plants and no bench data, and
neither does the harness. What it checks is whether the harness can fail in
the ways it says it can.

Six results, in the order they matter:

  1  C1's predicate returns SUPPORTED when the sim produces NOTHING. Zero
     signature cells gives spread 0.0, which passes `< 1.5`, and the reads
     line for TRUE is "the reported metrics are diagnostic".

  2  C1's own numbers say something narrower and more useful than its reads
     line: the spread is wide (4.88x) and entirely on ONE side of 1.0.

  3  the MechanismEdit guard reads 2 of the 4 free-text fields it is given.

  4  settle() records `prediction_held: None` and nothing ever fills it, and
     the before/after file hashes are equal because nothing edited the file.

  5  the header's own usage example fails.

  6  what the harness gets right, and it is most of it.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("PCH_LOG", os.path.join("/tmp", "pch_audit.jsonl"))

import photoperiod_claim_harness as H  # noqa: E402

RULE = "=" * 72
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = open(os.path.join(HERE, "photoperiod_claim_harness.py"),
           encoding="utf-8").read()


def section(title: str) -> None:
    print("\n" + RULE)
    print(title)
    print(RULE)


def claim(cid):
    return next(c for c in H.CLAIM_TABLE if c["id"] == cid)


# ---------------------------------------------------------------------------


def check_vacuous() -> None:
    section("1  C1 passes when the sim produces nothing")

    c1 = claim("C1")
    print("  predicate: signature_spread < 1.5")
    print("  spread    = max/min over cells that reproduce the signature")
    print("            = 0.0 when there are no such cells\n")

    live = H.s1_mass_denominator()
    print("    as shipped   cells=%d  spread=%.4f  -> %s"
          % (live["signature_cells"], live["signature_spread"],
             "SUPPORTED" if c1["predicate"](live) else "REFUTED"))

    # Remove the mechanism that drives the signature and rerun. Nothing about
    # the predicate changes; only whether any cell qualifies.
    orig = H._s1_run
    H._s1_run = lambda scale, sae, sink_k, days=8, dt=0.5: orig(
        scale, 0.0, sink_k, days=days, dt=dt)
    try:
        dead = H.s1_mass_denominator()
    finally:
        H._s1_run = orig

    print("    no shade-avoidance   cells=%d  spread=%.4f  -> %s"
          % (dead["signature_cells"], dead["signature_spread"],
             "SUPPORTED" if c1["predicate"](dead) else "REFUTED"))
    print("      signature_kWh_per_dry_min = %s" % dead["signature_kWh_per_dry_min"])
    print("      signature_kWh_per_dry_max = %s" % dead["signature_kWh_per_dry_max"])
    print()
    print("  C1's reads line for TRUE:\n")
    print("      the reported metrics are diagnostic of real efficiency\n")
    print("  A run in which the sim reproduces the reported signature ZERO")
    print("  times returns that verdict, with min and max printed as None on")
    print("  the line above it. The contradiction is visible in one output.")
    print()
    print("  Not a modelling error -- a predicate that cannot tell 'tight")
    print("  spread' from 'no observations'. Same shape as ../null-harness/")
    print("  CONSTANT_SILENT, one level up: not a gate that never fires, but")
    print("  a PASS that an empty result set returns.")
    print()
    print("  Fix is one guard, and the harness's own vocabulary has a slot")
    print("  for it: run_claim() already emits `UNDECIDED:` when a predicate")
    print("  raises. `if not sig_dry: raise ValueError('no signature cells')`")
    print("  routes the empty case there instead of to SUPPORTED.")


def check_direction() -> None:
    section("2  C1's numbers are narrower than its reads line")

    out = H.s1_mass_denominator()
    sd = [c["kWh_per_dry"] for c in out["grid"] if c["signature"]]
    print("  signature cells                      %d" % len(sd))
    print("  kWh per dry gram, ratio to control   %.4f .. %.4f"
          % (min(sd), max(sd)))
    print("  cells with ratio >= 1.0              %d"
          % sum(1 for x in sd if x >= 1.0))
    print("  signature_no_dry_gain_cells          %d"
          % out["signature_no_dry_gain_cells"])
    print()
    print("  The S1 docstring names the cell it is hunting for:\n")
    print("      A cell where (a) is TRUE and (b) is FALSE is a configuration")
    print("      in which the whole reported package appears with no gain per")
    print("      unit photosynthate.\n")
    print("  It finds none. Every one of the %d cells that reproduces the"
          % len(sd))
    print("  signature also improves energy per dry gram -- the whole range")
    print("  sits below 1.0.")
    print()
    print("  So the reads line for FALSE overstates by one word. It says the")
    print("  signature is NON-DIAGNOSTIC. What the grid shows is that it is")
    print("  non-diagnostic of MAGNITUDE -- a 4.9x range in the true ratio --")
    print("  and diagnostic of SIGN. On this mechanism set the reported")
    print("  package does license 'cheaper per dry gram'; it does not license")
    print("  any particular number, and 68% is a number.")
    print()
    print("  That is a stronger claim than the one written, because it")
    print("  survives the objection that the sim was rigged to find nothing.")
    print("  It found the effect and still cannot size it.")


def check_guard_coverage() -> None:
    section("3  the edit guard reads 2 of 4 fields")

    fields = ("reason", "mechanism", "basis", "prediction")
    print("  MechanismEdit takes four free-text fields:  %s\n"
          % ", ".join(fields))
    print("  and screens `reason + \" \" + mechanism` against FORBIDDEN_REASONS.\n")

    poison = "tune to match the reported result"   # hits "tune" and "to match"
    assert any(b in poison for b in H.FORBIDDEN_REASONS)
    print("  %-12s %s" % ("field", "outcome when it carries a forbidden reason"))
    print("  " + "-" * 62)
    for f in fields:
        kw = dict(mechanism="add a term", basis="literature",
                  prediction="the term shifts the curve", reason="mechanism work")
        kw[f] = poison
        try:
            H.MechanismEdit("S2", affects=["C2"], **kw)
            verdict = "ACCEPTED   <-- not screened"
        except ValueError:
            verdict = "refused"
        print("  %-12s %s" % (f, verdict))

    print()
    print("  `basis` and `prediction` are the two fields a motivated editor")
    print("  would put the outcome reasoning in, because they are the two")
    print("  that ask for justification. The screen is on the two that ask")
    print("  what changed.")
    print()
    print("  One-line fix: screen the concatenation of all four.")
    print()
    print("  Worth saying what the guard gets right: it is a PRE-registration")
    print("  gate, it fires at construction rather than at settle time, and")
    print("  the refusal message names the protocol. Refusing on a substring")
    print("  is crude and it is a real deny branch, which most such rules")
    print("  are not.")


def check_settle() -> None:
    section("4  settle() records a prediction and never adjudicates it")

    e = H.MechanismEdit("S2", mechanism="add photoinhibition at high "
                                        "instantaneous irradiance",
                        basis="photoinhibition literature",
                        prediction="low duty is penalised further",
                        affects=["C2"], reason="mechanism addition")
    rec = e.settle(observed={"best_duty": 1.0})

    print("  after settle():\n")
    print("    prediction        %r" % rec["prediction"])
    print("    observed          %r" % rec["observed"])
    print("    prediction_held   %r        <-- set to None, by construction"
          % rec["prediction_held"])
    print("    hash before       %s" % rec["file_hash_before"][:12])
    print("    hash after        %s" % rec["file_hash_after"][:12])
    print("    equal             %s        <-- nothing edited the file"
          % (rec["file_hash_before"] == rec["file_hash_after"]))
    print()
    print("  Two gaps, and they are the same gap:\n")
    print("  (a) `prediction_held = None  # human or model fills this in`.")
    print("      Nothing requires it. A registered prediction can be settled")
    print("      with the comparison never made, and the log will show a")
    print("      complete-looking MECHANISM_EDIT_SETTLED record.")
    print()
    print("  (b) the two hashes are equal because the file was not edited.")
    print("      The protocol exists to gate sim edits, and it cannot tell")
    print("      whether one happened. An edit registered, settled, and never")
    print("      performed is indistinguishable in the log from one carried")
    print("      out.")
    print()
    print("  Both are the shape ../reasoning-gate/ hit and repaired: a")
    print("  declared control that is never scored. Its fix was to refuse an")
    print("  empty observation and to write a record either way. Here the")
    print("  equivalents are: settle(observed, held: bool) with `held`")
    print("  required, and refusing to settle when the hash has not moved.")


def check_usage() -> None:
    section("5  the header's usage example fails")

    line = [l for l in SRC.splitlines()
            if l.strip().startswith("#   python3") and " run " in l]
    print("  from the file header:\n")
    for l in line:
        print("     " + l.strip("# ").rstrip())
    print()
    print("  `run` dispatches to run_claim(), which looks the argument up in")
    print("  CLAIM_TABLE by claim id. S2 is a SIM id.\n")
    ids = [c["id"] for c in H.CLAIM_TABLE]
    sims = sorted(H.SIMS)
    print("    claim ids : %s" % ", ".join(ids))
    print("    sim ids   : %s" % ", ".join(sims))
    print()
    try:
        H.run_claim("S2")
        print("    run_claim('S2') -> returned")
    except StopIteration:
        print("    run_claim('S2') -> StopIteration, uncaught")
    print()
    print("  `sweep S2` takes a sim id and `run C1` takes a claim id, which")
    print("  is defensible -- they are different commands over different")
    print("  registries. The header documents `run S2`.")
    print()
    print("  Same class as ../reasoning-gate/ D1, where the module docstring's")
    print("  usage example denied at pre(). Fixed there by making the example")
    print("  a working one and labelling the failing case separately.")


def check_what_holds() -> None:
    section("6  what the harness gets right")

    print("  The predicates are real. Every claim in the table is a function")
    print("  of a sim output and can come back either way -- and four of the")
    print("  five come back REFUTED on the shipped run, including two the")
    print("  file's own framing would have preferred to support.\n")

    for cid in [c["id"] for c in H.CLAIM_TABLE]:
        c = claim(cid)
        rec, out, _ = H.run_claim(cid)
        print("    %-4s [%-8s] %s" % (cid, c["source"], rec["status"]))

    print()
    print("  C2 is the sharpest thing in the file. It states a PREMISE from")
    print("  the literature (angiosperms have POR only, no DPOR), then a")
    print("  HYPOTHESIS that dark could still help by recharging the pool,")
    print("  then refutes its own hypothesis -- and the reads line for FALSE")
    print("  explains WHY in mechanism terms: the FLU clamp acts on pool")
    print("  SIZE, so a full pool slows synthesis and draining it")
    print("  continuously maximises flux. Then it NAMES the next candidate")
    print("  (shade acclimation) and files it in PENDING_EDITS rather than")
    print("  retuning.")
    print()
    print("  PENDING_EDITS is the part with no equivalent elsewhere in this")
    print("  repository. Three mechanisms named, each with a basis and a")
    print("  prediction registered BEFORE any run, all marked UNRUN. That is")
    print("  the alternative to quietly retuning a sim that came out the")
    print("  wrong way, written down as a data structure.")
    print()
    print("  Provenance is separated at the type level -- REPORTED, PHYSICS,")
    print("  SIM, BENCH -- and the hypothesis block says plainly that every")
    print("  number in it is SIM, that a sim can show an artifact is")
    print("  SUFFICIENT to produce a signature and not that it happened, and")
    print("  that the confidence and comfort readouts are separate and are")
    print("  not filled in by the file.")
    print()
    print("  BENCH is declared and no code path can emit it. That is the")
    print("  honest state and the file says so; the protocol section is the")
    print("  instructions for producing one, which is more than most claim")
    print("  tables carry.")


def main() -> int:
    print()
    print("AUDITING THE HARNESS")
    print("subject: photoperiod_claim_harness.py, unmodified")
    print("this file has no bench data and neither does the harness")

    check_vacuous()
    check_direction()
    check_guard_coverage()
    check_settle()
    check_usage()
    check_what_holds()

    section("READING")
    print("""
  The one that matters: C1's predicate returns SUPPORTED -- "the reported
  metrics are diagnostic of real efficiency" -- from a run in which the sim
  reproduced the reported signature zero times, printing None for the min
  and max on the line above. A pass that an empty result set returns is not
  a pass. One guard fixes it, and run_claim() already has the UNDECIDED
  branch to route it to.

  C1's own grid says something better than its reads line. The signature
  appears in 58 cells spanning a 4.9x range of true energy-per-dry-gram,
  and every one of them is below 1.0. Non-diagnostic of MAGNITUDE,
  diagnostic of SIGN -- which is the stronger version of the finding,
  because it survives the objection that the sim was built to find nothing.

  The edit protocol screens two of the four fields it is given, and the two
  it skips are the two that ask for justification. settle() writes
  prediction_held: None and nothing fills it, and the before/after hashes
  are equal because nothing edited the file -- so a registered, settled,
  never-performed edit is indistinguishable in the log from a real one.
  Both are the declared-control-never-scored shape that ../reasoning-gate/
  repaired by requiring the observation.

  What holds is most of it. The predicates fire in both directions, four of
  five come back REFUTED on the shipped run, C2 refutes its own hypothesis
  and explains the mechanism, and PENDING_EDITS writes down the three
  named-but-unrun alternatives instead of retuning toward them.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
