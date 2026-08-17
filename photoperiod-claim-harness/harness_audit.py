"""
harness_audit.py -- grade the harness, not the greenhouse.

CC0-1.0. Standard library only. Deterministic. Imports the harness and reads
its source; changes nothing at run time.

The delivered harness is a claim table with runnable predicates and a
refutation protocol. Its subject is a published greenhouse result. THIS file
does not touch that subject -- it has no plants and no bench data, and
neither does the harness. What it checks is whether the harness can fail in
the ways it says it can.

REPAIRED. Every defect below is fixed in the harness and pinned by
tests/test_repairs.py (29 tests). Each section reproduces the pre-repair
behaviour where it can, so the cost stays measured rather than quoted, and
says what the current code does. The repairs were chosen by one rule: make
the code do what the delivered README already says it does.

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

  7  the delivered README's numbers all check out. One word did not: the
     dark-interval curve was negative but NOT monotone, because arms whose
     run ends mid-cycle were sampled at a different phase. Repaired by
     reading a cycle average; the curve is monotone and no verdict moved.

  8  three things the README describes that the code did not do.
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
    section("1  C1 used to pass when the sim produced nothing")

    # The pre-repair predicate, reproduced so the cost stays measured.
    shipped = lambda o: o["signature_spread"] < 1.5   # noqa: E731

    print("  was:  signature_spread < 1.5")
    print("  spread = max/min over cells that reproduce the signature")
    print("         = 0.0 when there are no such cells\n")

    live = H.s1_mass_denominator()

    orig = H._s1_run
    H._s1_run = lambda scale, sae, sink_k, days=8, dt=0.5: orig(
        scale, 0.0, sink_k, days=days, dt=dt)
    try:
        dead = H.s1_mass_denominator()
        dead_rec, _, _ = H.run_claim("C1")
    finally:
        H._s1_run = orig
    live_rec, _, _ = H.run_claim("C1")

    print("  %-24s %-8s %-10s %-14s %s"
          % ("world", "cells", "spread", "pre-repair", "now"))
    print("  " + "-" * 66)
    print("  %-24s %-8d %-10.4f %-14s %s"
          % ("as shipped", live["signature_cells"], live["signature_spread"],
             "SUPPORTED" if shipped(live) else "REFUTED", live_rec["status"]))
    print("  %-24s %-8d %-10.4f %-14s %s"
          % ("no shade-avoidance", dead["signature_cells"],
             dead["signature_spread"],
             "SUPPORTED" if shipped(dead) else "REFUTED",
             dead_rec["status"].split(":")[0]))
    print()
    print("    (min and max printed as %s and %s in the dead world)"
          % (dead["signature_kWh_per_dry_min"],
             dead["signature_kWh_per_dry_max"]))
    print()
    print("  C1's reads line for TRUE was:\n")
    print("      the reported metrics are diagnostic of real efficiency\n")
    print("  A run in which the sim reproduced the reported signature ZERO")
    print("  times returned that verdict, with None for min and max on the")
    print("  line above. A pass an empty result set returns is not a pass --")
    print("  ../null-harness/ CONSTANT_SILENT one level up.")
    print()
    print("  REPAIRED with the harness's own vocabulary. run_claim() already")
    print("  emitted `UNDECIDED:` when a predicate raises, so C1's predicate")
    print("  calls require() on a non-empty cell set first, and the empty")
    print("  case routes to the third verdict it always had a slot for:\n")
    print("      %s" % dead_rec["status"])
    print()
    print("  The README's own extension rule is the invariant this restores:")
    print("  'append to CLAIM_TABLE with a predicate that can fail'.")


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
    print()
    print("  REPAIRED, by updating the CLAIM rather than the sim -- which is")
    print("  what the protocol says to do. C1's reads line now separates")
    print("  MAGNITUDE from SIGN and names the field that backs it:\n")
    print("      signature_sign_agreement = %s"
          % out["signature_sign_agreement"])
    print("      signature_cells_below_1  = %d of %d"
          % (out["signature_cells_below_1"], out["signature_cells"]))
    print()
    print("  The field is None when there is nothing to agree on, so it")
    print("  cannot be read as unanimity in the empty case section 1 covers.")


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
    print("  REPAIRED: the screen reads the concatenation of all four.")
    print()
    print("  Worth saying what the guard gets right: it is a PRE-registration")
    print("  gate, it fires at construction rather than at settle time, and")
    print("  the refusal message names the protocol. Refusing on a substring")
    print("  is crude and it is a real deny branch, which most such rules")
    print("  are not.")


def check_settle() -> None:
    section("4  settle() used to record a prediction and never adjudicate it")

    e = H.MechanismEdit("S2", mechanism="add photoinhibition at high "
                                        "instantaneous irradiance",
                        basis="photoinhibition literature",
                        prediction="low duty is penalised further",
                        affects=["C2"], reason="mechanism addition")

    print("  Pre-repair, settle(observed) wrote:\n")
    print("    prediction_held   None   # 'human or model fills this in'")
    print("    file_hash_after   equal to file_hash_before, unremarked\n")
    print("  So a registered prediction could be settled with the")
    print("  comparison never made, and the protocol -- which exists to gate")
    print("  SIM EDITS -- could not tell whether the edit it gated had")
    print("  happened. An edit registered, settled and never performed was")
    print("  indistinguishable in the log from one carried out.")
    print()
    print("  REPAIRED. Three behaviours, each demonstrated:\n")

    for label, call in (
        ("settle without a verdict",
         lambda: e.settle({"best_duty": 1.0}, None)),
        ("settle with a non-bool",
         lambda: e.settle({"best_duty": 1.0}, "yes")),
        ("settle an edit that did not happen",
         lambda: e.settle({"best_duty": 1.0}, True)),
    ):
        try:
            call()
            print("    %-38s ACCEPTED" % label)
        except ValueError as exc:
            print("    %-38s refused: %s"
                  % (label, str(exc).splitlines()[0][:34]))

    rec = e.abandon("photoinhibition needs an irradiance ceiling the spec "
                    "does not declare")
    print("    %-38s logged as %s"
          % ("abandon(reason)", rec["kind"]))
    print("      file_changed = %s" % rec["file_changed"])
    print()
    print("  `abandon` is the path for an edit decided against, so the trail")
    print("  stays intact either way -- registered, then not made, and the")
    print("  log says which.")
    print()
    print("  Same shape as ../reasoning-gate/'s declared control that was")
    print("  never scored. Its repair was to refuse an empty observation and")
    print("  write a record either way; this is that, on a prediction.")


def check_usage() -> None:
    section("5  the header's usage example used to fail")

    line = [l for l in SRC.splitlines()
            if l.strip().startswith("#   python3") and " run " in l]
    print("  the file header now reads:\n")
    for l in line:
        print("     " + l.strip("# ").rstrip())
    print()
    print("  It used to document `run S2`. `run` dispatches to run_claim(),")
    print("  which looks the argument up in CLAIM_TABLE by claim id, and S2")
    print("  is a SIM id.\n")
    ids = [c["id"] for c in H.CLAIM_TABLE]
    sims = sorted(H.SIMS)
    print("    claim ids : %s" % ", ".join(ids))
    print("    sim ids   : %s" % ", ".join(sims))
    print()
    try:
        H.run_claim("S2")
        print("    run_claim('S2') -> returned")
    except StopIteration:
        print("    run_claim('S2') -> StopIteration, uncaught (unchanged;")
        print("                       the fix is to the documentation, since")
        print("                       the two registries are separate on")
        print("                       purpose)")
    print()
    print("  `sweep S2` takes a sim id and `run C1` takes a claim id, which")
    print("  is defensible -- they are different commands over different")
    print("  registries. The header documents `run S2`.")
    print()
    print("  REPAIRED: the header documents `run C2` and labels `sweep S2`")
    print("  as a different registry on purpose. Same class as")
    print("  ../reasoning-gate/ D1, and the same fix.")


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


def _run_avg(duty, dark_block_h, days=6, dt=0.1, k_syn=0.06, P_max=1.0,
             k_cat=0.50, Km=0.30, K_light=0.60, I_on=1.0,
             k_deg_light=0.002, k_deg_dark=0.012):
    """
    _pchlide_run's integrator, unchanged, returning the mean over the FINAL
    COMPLETE PERIOD instead of the value at the last step. Nothing about the
    mechanism differs; only where the number is read.
    """
    import math
    I_eff = I_on / duty
    period = dark_block_h / max(1e-9, (1.0 - duty)) if duty < 1.0 else 1.0
    P, Chl, t = P_max * 0.5, 0.10, 0.0
    T = days * 24
    start = period * (math.floor(T / period) - 1) + (
        T - period * math.floor(T / period))
    acc, n = 0.0, 0
    for _ in range(int(T / dt)):
        phase = math.fmod(t, period) / period if period > 0 else 0.0
        lit = phase < duty
        I = I_eff if lit else 0.0
        v = k_cat * (P / (P + Km)) * (I / (I + K_light)) if lit else 0.0
        P = max(0.0, P + (k_syn * (1.0 - P / P_max) - v) * dt)
        Chl = max(0.0, Chl + (v - (k_deg_light if lit else k_deg_dark) * Chl) * dt)
        t += dt
        if t >= start:
            acc += Chl
            n += 1
    return acc / max(n, 1)


def check_readme() -> None:
    section("7  the README's numbers hold; one word does not")

    import math
    out = H.s1_mass_denominator()
    print("  %-38s %-10s %s" % ("delivered README says", "stated", "measured"))
    print("  " + "-" * 66)
    print("  %-38s %-10s %d" % ("grid cells", "75", len(out["grid"])))
    print("  %-38s %-10s %d" % ("cells reproducing the signature", "58",
                                out["signature_cells"]))
    print("  %-38s %-10s %.4f" % ("spread of true kWh per dry gram", "~4.9x",
                                  out["signature_spread"]))
    for cid, want in (("C1", "REFUTED"), ("C2", "REFUTED"), ("C3", "REFUTED"),
                      ("C4", "REFUTED"), ("C5", "SUPPORTED")):
        rec, _, _ = H.run_claim(cid)
        print("  %-38s %-10s %s" % (cid, want, rec["status"]))

    print()
    print("  The one that does not:\n")
    print("      C3 REFUTED. No crossover in this regime; dark is")
    print("      MONOTONICALLY WORSE under C2's mechanism set.\n")

    s2 = H.s2_pool_charging()
    dc = s2["dark_interval_curve"]
    duty, days = 0.5, 6
    print("  %-8s %-10s %-14s %-14s" % ("block h", "periods", "endpoint",
                                        "cycle-average"))
    print("  " + "-" * 52)
    cont_avg = _run_avg(1.0, 4.0)
    avg = []
    for b, d in dc:
        per = b / (1.0 - duty)
        n = days * 24 / per
        a = _run_avg(duty, b) - cont_avg
        avg.append(a)
        mark = "" if abs(n - round(n)) < 1e-9 else "   <- ends mid-cycle"
        print("  %-8.1f %-10.2f %-14.5f %-14.5f%s" % (b, n, d, a, mark))

    ep_mono = all(dc[i][1] <= dc[i - 1][1] for i in range(1, len(dc)))
    av_mono = all(avg[i] <= avg[i - 1] for i in range(1, len(avg)))
    breaks = [dc[i][0] for i in range(1, len(dc)) if dc[i][1] > dc[i - 1][1]]
    partial = [b for b, _ in dc
               if abs((days * 24 / (b / (1.0 - duty)))
                      - round(days * 24 / (b / (1.0 - duty)))) > 1e-9]
    print()
    print("  endpoint curve monotone      %s" % ep_mono)
    print("  cycle-average monotone       %s" % av_mono)
    print("  arms that break monotonicity %s" % breaks)
    print("  arms that end mid-cycle      %s" % partial)
    print("  every breaking arm ends mid-cycle: %s"
          % set(breaks).issubset(set(partial)))
    print("  (the converse does not hold -- %s ends mid-cycle and happens"
          % ", ".join(str(b) for b in sorted(set(partial) - set(breaks))))
    print("   not to break the ordering, so ending mid-cycle is necessary")
    print("   here and not sufficient)")
    print()
    print("  REPAIRED. `_pchlide_run` now returns the mean over the final")
    print("  complete period, and the shipped curve is monotone -- so the")
    print("  README's sentence is true of the output for the first time.")
    print("  `Chl_endpoint` is still returned, because the repair adds a")
    print("  readout rather than removing one.")
    print()
    print("  Registered as an InstrumentEdit, not a MechanismEdit. The")
    print("  protocol governed MECHANISM changes and had no category for a")
    print("  change to WHERE a number is read -- which alters sim output")
    print("  while altering no mechanism and no parameter. That axis was")
    print("  already implicit in the provenance types, and is now explicit.")
    print()
    print("  Pre-repair, `_pchlide_run` returned Chl at the last")
    print("  integration step, and at duty=0.5 the period is 2 x dark_block,")
    print("  so a 144 h run ends mid-cycle for the blocks that do not divide")
    print("  it. Reading the mean over the final complete period")
    print("  instead of the endpoint makes the curve monotone.")
    print()
    print("  It changes no verdict. C3's predicate looks for a SIGN FLIP;")
    print("  both curves are negative throughout, so `crossover_h` is None")
    print("  either way. What the artifact costs is the ability to read the")
    print("  curve's SHAPE as mechanism -- which is what C3's reads line")
    print("  offers when it says 'one process dominates throughout'.")
    print()
    print("  Same class as ../aperiodic-order-sim-stack/: a commensurability")
    print("  between the sampling grid and the structure being measured, and")
    print("  the fix is to read a quantity the grid cannot alias.")


def check_prose() -> None:
    section("8  three things the README described that the code did not do")

    print("  The repairs above were chosen by one rule: make the code do")
    print("  what the delivered README already says it does. Three of them")
    print("  were promises with no implementation at all.\n")

    print("  (a) 'run -> provenance record -> RESIDUAL ROUTER -> hypothesis")
    print("      block'. residual_route() was defined and never called.\n")
    ref, _, _ = H.run_claim("C2")
    sup, _, _ = H.run_claim("C5")
    print("      C2 %-10s residual_route attached: %s"
          % (ref["status"], "residual_route" in ref))
    print("      C5 %-10s residual_route attached: %s"
          % (sup["status"], "residual_route" in sup))
    print()
    print("      It attaches where it is the point -- a claim that did not")
    print("      hold, or one the predicate could not decide. Four questions,")
    print("      unanswered by construction. The router routes; it does not")
    print("      resolve.\n")

    print("  (b) 'Provenance never merges: REPORTED, PHYSICS, SIM, BENCH.")
    print("      BENCH is empty until someone runs one.' Three types had")
    print("      code paths. BENCH was declared and unreachable, so 'empty'")
    print("      was true by absence rather than by construction.\n")
    import tempfile as _tf
    log = os.path.join(_tf.mkdtemp(), "bench.jsonl")
    old, H.LOGPATH = H.LOGPATH, log
    try:
        print("      before: %d BENCH record(s)" % len(H.bench_records(log)))
        H.record_bench("C1", "kWh_per_g_dry", 0.42, "kWh/g",
                       method="65 C to constant mass, 72 h",
                       kit="scale 0.01 g, kWh meter on the lamp circuit")
        print("      after:  %d BENCH record(s)" % len(H.bench_records(log)))
        try:
            H.record_bench("C1", "q", 1.0, "u", method="   ", kit="k")
            print("      a number with no method: ACCEPTED")
        except ValueError:
            print("      a number with no method: refused -- that is SIM")
            print("                               provenance wearing a BENCH")
            print("                               label")
    finally:
        H.LOGPATH = old
    print()
    print("      The hypothesis block now reports BENCH coverage per claim,")
    print("      so 'no physical exit yet' is a printed line rather than an")
    print("      absence the reader has to notice.\n")

    print("  (c) the hypothesis block stamped the wall clock one line above")
    print("      the file hash it printed for provenance, so two runs of the")
    print("      same file produced two different documents.\n")
    res = [H.run_claim(c["id"]) for c in H.CLAIM_TABLE]
    a = H.hypothesis_block(res)
    b = H.hypothesis_block(res)
    print("      identical across two calls: %s" % (a == b))
    print("      run id: %s" % H.run_id(res))
    print()
    print("      The id is the file hash plus the claim statuses, so it moves")
    print("      when either does and not otherwise. The clock is in the log,")
    print("      where every record already carries one.")


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
    check_readme()
    check_prose()

    section("READING")
    print("""
  REPAIRED, all of it, pinned by tests/test_repairs.py. The rule for what
  to fix was the delivered README: make the code do what the prose already
  says it does.

  C1's predicate returned SUPPORTED -- "the reported metrics are
  diagnostic" -- from a run in which the sim reproduced the signature zero
  times, because the spread of an empty set was 0.0. It now calls
  require() and routes to UNDECIDED, the third verdict run_claim() always
  had a branch for. The README's own extension rule is what this restores:
  a predicate that can fail.

  C1's reads line was updated rather than the sim, which is what the
  protocol says to do. The grid finds the signature in 58 cells spanning a
  4.9x range of true energy-per-dry-gram and ALL of them below 1.0, so it
  is non-diagnostic of magnitude and diagnostic of sign. signature_sign_-
  agreement carries that, and is None when there is nothing to agree on.

  The edit guard screens all four fields it is given. settle() requires a
  bool and refuses when the file hash has not moved, with abandon() as the
  path for an edit decided against -- so a registered, settled,
  never-performed edit is no longer indistinguishable in the log from a
  real one.

  The dark-interval readout is a cycle average, so the curve is monotone
  and the README's C3 sentence is true of the output for the first time.
  Registered as an InstrumentEdit: the protocol governed MECHANISM changes
  and had no category for a change to where a number is READ, which alters
  sim output while altering no mechanism. No verdict moved.

  And three promises with no implementation: the residual router is in the
  pipeline, BENCH has an ingest path that refuses a number with no method,
  and the hypothesis block carries a deterministic run id instead of a wall
  clock stamped one line above the hash it prints for provenance.
""")
    return 0


if __name__ == "__main__":
    sys.exit(main())
