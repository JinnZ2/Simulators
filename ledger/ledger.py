#!/usr/bin/env python3
"""The ledger. Three diffs, and it exits nonzero if any of them fires.

    INTERNAL      asserted value vs the value recomputed from its own
                  operands. Reported FIRST, at the top, not in a list.
    DRIFT         current value vs the committed EXPECTED value. Appended to
                  DRIFT.md with date, machine and Python version. Never pruned.
    CROSS-LEDGER  py_ledger vs cobol_ledger. A disagreement goes to
                  DISAGREEMENTS.md and is never resolved by picking a winner.
                  An unavailable arm marks the claim PRECISION_UNVERIFIED.

WHAT THIS DOES NOT DO, stated because the failure mode is reading it as more:

    It does not run sims.
    It does not time anything.
    It does not say any claim is true.
    It does not say any sim is correct.
    It does not say a CARRIED value is grounded.

It checks that what the repo says it computes is what it computes, and that it
keeps computing it.

A SEEDED value is NOT a verified value. It is a pin.

stdlib only. CC0.
"""

from __future__ import annotations

import argparse
import datetime
import os
import platform
import sys
from typing import Dict, List, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from record import ClaimRecord, Provenance, load_records  # noqa: E402
from py_ledger import engine  # noqa: E402
from cobol_ledger import bridge  # noqa: E402

CHOICES = [
    "[CHOICE 1] precision is read as SIGNIFICANT DIGITS (engine.py).",
    "[CHOICE 2] recomputation carries %d guard digits and quantizes once, at "
    "the end (engine.py)." % engine.GUARD,
    "[CHOICE 3] EXPECTED state is SEEDED or CONFIRMED. The ledger only ever "
    "writes SEEDED. A ledger that could promote its own pin has verified "
    "nothing, so promotion is a human edit and shows up in a diff.",
    "[CHOICE 4] DRIFT compares the RECOMPUTED value where recomputation "
    "succeeded and the ASSERTED value otherwise. Each row names which basis "
    "it used, so the two are never silently mixed.",
    "[CHOICE 5] A claim with no EXPECTED file is SEEDED and is not drift. A "
    "new claim has nothing to have drifted from.",
    "[CHOICE 6] Comparison is numeric at the declared precision, not string "
    "equality: 0.214 and 0.2140 are one value and two strings.",
]

SEED_NOTE = "A SEEDED value is NOT a verified value. It is a pin."


# ---------------------------------------------------------------- EXPECTED

def expected_path(root: str, sim: str, claim_id: str) -> str:
    return os.path.join(root, sim, claim_id + ".txt")


def read_expected(path: str) -> Optional[Dict[str, str]]:
    if not os.path.isfile(path):
        return None
    out: Dict[str, str] = {}
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        out[k.strip()] = v.strip()
    return out


def write_expected(path: str, value: str, precision: int, today: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("value: %s\n" % value)
        fh.write("precision: %d\n" % precision)
        fh.write("state: SEEDED\n")
        fh.write("seeded: %s\n" % today)
        fh.write("note: %s\n" % SEED_NOTE)


# ---------------------------------------------------------------- the run

class Run(object):
    def __init__(self, records: Sequence[ClaimRecord],
                 failures: Sequence[Tuple[str, str]],
                 expected_root: str, today: str, seed: bool = True):
        self.records = list(records)
        self.intake_failures = list(failures)
        self.expected_root = expected_root
        self.today = today
        self.seed = seed

        self.duplicates: List[str] = []
        self.internal: List[Dict[str, str]] = []
        self.drift: List[Dict[str, str]] = []
        self.seeded: List[str] = []
        self.unrecomputable: List[Dict[str, str]] = []
        self.cycles: List[Tuple[str, List[str]]] = []
        self.weak: List[Tuple[str, List[str]]] = []
        self.falsifier_untested: List[str] = []
        self.cross: Dict[str, object] = {}

        self._run()

    # ---- diff 2 and the recomputation it rests on
    def _run(self) -> None:
        seen: Dict[Tuple[str, str], str] = {}
        for r in self.records:
            if r.key() in seen:
                self.duplicates.append(
                    "%s declared twice: %s and %s"
                    % (r.ref(), seen[r.key()], r.source))
            seen[r.key()] = r.source or "?"

        order, self.cycles = engine.topo_order(self.records)
        in_cycle = set()
        for _, loop in self.cycles:
            for ref in loop:
                sim, _, cid = ref.partition(":")
                in_cycle.add((sim, cid))

        # Operand values are the ASSERTED values. Chaining recomputed values
        # would let one claim's internal disagreement silently move another's
        # recomputation, and the ledger would report the wrong claim.
        asserted = {r.key(): r.value for r in self.records}

        self.recomputed: Dict[Tuple[str, str], str] = {}
        for r in order:
            if r.provenance is not Provenance.DERIVED:
                continue
            res = engine.recompute(r, asserted)
            if res.ok():
                self.recomputed[r.key()] = res.value or ""
                if not engine.same_value(r.value, res.value or "",
                                         r.precision):
                    self.internal.append({
                        "ref": r.ref(), "asserted": r.value,
                        "recomputed": res.value or "",
                        "expression": r.expression or "",
                        "precision": str(r.precision),
                    })
            else:
                self.unrecomputable.append({
                    "ref": r.ref(), "outcome": res.outcome.value,
                    "reason": res.reason,
                })
        for r in self.records:
            if r.key() in in_cycle:
                self.unrecomputable.append({
                    "ref": r.ref(), "outcome": engine.Outcome.CYCLE.value,
                    "reason": "operand graph reaches itself",
                })

        for key, (prov, weak) in engine.resolve_provenance(
                self.records).items():
            if prov is Provenance.DERIVED_WEAK:
                self.weak.append(("%s:%s" % key, weak))
        self.weak.sort()

        for r in self.records:
            if not (r.falsifier_test or "").strip():
                self.falsifier_untested.append(r.ref())
        self.falsifier_untested.sort()

        self._diff_expected()
        self.cross = self._cross_ledger()

    # ---- diff 1
    def _diff_expected(self) -> None:
        for r in sorted(self.records, key=lambda x: x.ref()):
            if r.key() in self.recomputed:
                basis, current = "RECOMPUTED", self.recomputed[r.key()]
            else:
                basis, current = "ASSERTED", r.value
            path = expected_path(self.expected_root, r.sim, r.claim_id)
            exp = read_expected(path)
            if exp is None:
                if self.seed:
                    write_expected(path, current, r.precision, self.today)
                self.seeded.append(r.ref())
                continue
            prec = r.precision
            try:
                prec = int(exp.get("precision", r.precision))
            except ValueError:
                pass
            if not engine.same_value(exp.get("value", ""), current, prec):
                self.drift.append({
                    "ref": r.ref(), "expected": exp.get("value", ""),
                    "current": current, "basis": basis,
                    "state": exp.get("state", "?"),
                    "seeded": exp.get("seeded", "?"),
                    "precision": str(prec),
                })

    # ---- diff 3
    def _cross_ledger(self) -> Dict[str, object]:
        avail = bridge.availability()
        if not avail.available:
            return {"status": "UNAVAILABLE", "reason": avail.reason,
                    "precision_unverified": [r.ref() for r in
                                             sorted(self.records,
                                                    key=lambda x: x.ref())]}
        out = bridge.run(self.records)
        if out.status != "OK":
            return {"status": "UNAVAILABLE", "reason": out.reason,
                    "precision_unverified": [r.ref() for r in
                                             sorted(self.records,
                                                    key=lambda x: x.ref())]}
        disagree: List[Dict[str, str]] = []
        missing: List[str] = []
        for r in sorted(self.records, key=lambda x: x.ref()):
            if r.key() not in self.recomputed:
                continue
            got = out.values.get(r.key())
            if got is None:
                missing.append(r.ref())
                continue
            if not engine.same_value(self.recomputed[r.key()], got,
                                     r.precision):
                disagree.append({"ref": r.ref(),
                                 "py": self.recomputed[r.key()],
                                 "cobol": got,
                                 "precision": str(r.precision)})
        return {"status": "OK", "disagree": disagree,
                "precision_unverified": missing}

    # ---- verdict
    def fired(self) -> List[str]:
        out = []
        if self.internal:
            out.append("INTERNAL")
        if self.drift:
            out.append("DRIFT")
        if self.cross.get("status") == "OK" and self.cross.get("disagree"):
            out.append("CROSS_LEDGER")
        return out


# ---------------------------------------------------------------- reporting

def machine_line() -> str:
    return "python %s on %s %s" % (platform.python_version(),
                                   platform.system(), platform.machine())


def render(run: Run) -> str:
    L: List[str] = []
    a = L.append
    a("LEDGER")
    a("=" * 70)
    a("date            %s" % run.today)
    a("machine         %s" % machine_line())
    a("records         %d" % len(run.records))
    a("")

    # INTERNAL first, at the top, not in a list.
    a("INTERNAL DISAGREEMENT")
    a("-" * 70)
    a("An asserted value that does not equal what its own operands produce.")
    a("This is the strongest finding the ledger can produce.")
    a("")
    if not run.internal:
        a("  none over %d recomputable DERIVED claims"
          % len(run.recomputed))
    for d in run.internal:
        a("  %s" % d["ref"])
        a("      asserted    %s" % d["asserted"])
        a("      recomputed  %s" % d["recomputed"])
        a("      expression  %s" % d["expression"])
        a("      precision   %s significant digits" % d["precision"])
    a("")

    a("DRIFT AGAINST EXPECTED")
    a("-" * 70)
    if not run.drift:
        a("  none")
    for d in run.drift:
        a("  %s  [%s, %s %s]" % (d["ref"], d["basis"], d["state"],
                                 d["seeded"]))
        a("      expected  %s" % d["expected"])
        a("      current   %s" % d["current"])
    a("")

    a("CROSS-LEDGER (py_ledger vs cobol_ledger)")
    a("-" * 70)
    if run.cross.get("status") == "UNAVAILABLE":
        a("  UNAVAILABLE: %s" % run.cross.get("reason"))
        n = len(run.cross.get("precision_unverified") or [])
        a("  PRECISION_UNVERIFIED for all %d claims." % n)
        a("  py_ledger is authoritative for REACHABILITY and is not")
        a("  authoritative for PRECISION. With one arm down, no precision")
        a("  claim in this run is checked.")
    else:
        dis = run.cross.get("disagree") or []
        if not dis:
            a("  no disagreement")
        for d in dis:  # type: ignore[union-attr]
            a("  %s  py=%s  cobol=%s" % (d["ref"], d["py"], d["cobol"]))
            a("      recorded. NOT resolved by picking a winner.")
        mu = run.cross.get("precision_unverified") or []
        if mu:
            a("  PRECISION_UNVERIFIED (no cobol value): %s"
              % ", ".join(mu))  # type: ignore[arg-type]
    a("")

    a("SEEDED THIS RUN")
    a("-" * 70)
    if not run.seeded:
        a("  none")
    else:
        a("  %s" % SEED_NOTE)
        for r in run.seeded:
            a("  %s" % r)
    a("")

    a("NOT RECOMPUTABLE")
    a("-" * 70)
    if not run.unrecomputable:
        a("  none")
    for d in sorted(run.unrecomputable, key=lambda x: x["ref"]):
        a("  %-34s %-22s %s" % (d["ref"], d["outcome"], d["reason"]))
    a("")

    a("PROVENANCE, RESOLVED TRANSITIVELY")
    a("-" * 70)
    if not run.weak:
        a("  no DERIVED claim reaches a CARRIED value")
    for ref, weak in run.weak:
        a("  %s  DERIVED_WEAK" % ref)
        for w in weak:
            a("      via %s" % w)
    a("")

    a("FALSIFIER_UNTESTED")
    a("-" * 70)
    a("  A falsifier with no test is a sentence, not a check.")
    if not run.falsifier_untested:
        a("  none")
    for ref in run.falsifier_untested:
        a("  %s" % ref)
    a("")

    if run.intake_failures or run.duplicates:
        a("INTAKE")
        a("-" * 70)
        for where, why in run.intake_failures:
            a("  %-40s %s" % (where, why))
        for d in run.duplicates:
            a("  %s" % d)
        a("")

    fired = run.fired()
    a("VERDICT")
    a("-" * 70)
    a("  diffs fired: %s" % (", ".join(fired) if fired else "none"))
    a("  exit %d" % (1 if fired else 0))
    return "\n".join(L)


def append_drift_log(path: str, run: Run) -> None:
    """Append-only. A pruned drift log cannot tell a value that never moved
    from one whose movement was deleted."""
    if not run.drift:
        return
    new = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# DRIFT\n\n"
                     "Append-only. Never pruned. Each entry is one run in "
                     "which a value moved away from its committed EXPECTED "
                     "value.\n\n")
        fh.write("## %s  %s\n\n" % (run.today, machine_line()))
        for d in run.drift:
            fh.write("- `%s` expected `%s` -> current `%s` "
                     "(%s, pin %s %s, %s significant digits)\n"
                     % (d["ref"], d["expected"], d["current"], d["basis"],
                        d["state"], d["seeded"], d["precision"]))
        fh.write("\n")


def append_disagreements(path: str, run: Run) -> None:
    dis = run.cross.get("disagree") or []
    if run.cross.get("status") != "OK" or not dis:
        return
    new = not os.path.exists(path)
    with open(path, "a", encoding="utf-8") as fh:
        if new:
            fh.write("# DISAGREEMENTS\n\n"
                     "py_ledger against cobol_ledger. Recorded, never "
                     "resolved by picking a winner. py_ledger is "
                     "authoritative for REACHABILITY; cobol_ledger is "
                     "authoritative for PRECISION. A row here is a place "
                     "where those two authorities return different "
                     "numbers.\n\n")
        fh.write("## %s  %s\n\n" % (run.today, machine_line()))
        for d in dis:  # type: ignore[union-attr]
            fh.write("- `%s` py `%s` cobol `%s` (%s significant digits)\n"
                     % (d["ref"], d["py"], d["cobol"], d["precision"]))
        fh.write("\n")


def main(argv: Optional[Sequence[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--records", default=os.path.join(HERE, "records"))
    ap.add_argument("--expected", default=os.path.join(HERE, "EXPECTED"))
    ap.add_argument("--drift-log", default=os.path.join(HERE, "DRIFT.md"))
    ap.add_argument("--disagreements",
                    default=os.path.join(HERE, "DISAGREEMENTS.md"))
    ap.add_argument("--no-seed", action="store_true",
                    help="do not write EXPECTED files for new claims")
    ap.add_argument("--no-log", action="store_true",
                    help="report but do not append to DRIFT.md")
    ap.add_argument("--choices", action="store_true")
    ap.add_argument("--selftest", action="store_true",
                    help="refused; see ledger/selftest_ledger.py")
    args = ap.parse_args(list(argv) if argv is not None else None)

    if args.selftest:
        sys.stderr.write(
            "ledger.py does not carry its own checks. Run:\n"
            "    python3 ledger/selftest_ledger.py\n")
        return 2
    if args.choices:
        for c in CHOICES:
            print(c)
        return 0

    today = datetime.date.today().isoformat()
    recs, failures = load_records(args.records)
    if not recs and not failures:
        # A clean report over zero rows reads as all-clear. It is not one.
        sys.stderr.write(
            "REFUSED: no claim records under %s\n"
            "The ledger reads records; it does not run sims and does not\n"
            "produce records. Nothing in this repo emits them yet -- see\n"
            "ledger/records/README.md. Exiting 2 rather than printing a\n"
            "clean ledger over an empty set.\n" % args.records)
        return 2
    run = Run(recs, failures, args.expected, today, seed=not args.no_seed)
    print(render(run))
    if not args.no_log:
        append_drift_log(args.drift_log, run)
        append_disagreements(args.disagreements, run)
    return 1 if run.fired() else 0


if __name__ == "__main__":
    raise SystemExit(main())
