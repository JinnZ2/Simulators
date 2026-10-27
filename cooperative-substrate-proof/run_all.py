#!/usr/bin/env python3
"""Run P1-P5 and report per-part PASS / ABSENT, which is the order's
requested return.

    PASS    the part ran and produced a reading
    ABSENT  the part could not run because an input it requires is not
            present in this environment; the reason is named

A part is never reported PASS on a substitute for its input. P1's
pipeline is the one ABSENT row and it stays ABSENT: the order names
open-access methods sections, and no such host answers here.

    python3 run_all.py            # every part, short
    python3 run_all.py --full     # every part, whole output

Refuses --selftest; checks live in test_proof.py.
"""

import os
import sys

import p1_records
import p2_substrate
import p3_comprehension
import p4_coherence
import p5_lag
import scope

HERE = os.path.dirname(os.path.abspath(__file__))
FRAMING = os.path.join(HERE, "FRAMING.md")

FRAMING_LINES = (
    "Competition is a framework but a narrow one",
    "cooperative substrate required for the competitive frame",
    "Coverage argument, not values argument",
    "Do not strip the competition frame. Add the layer underneath it",
)


def framing_present():
    """The framing is load-bearing, so its presence is checked before
    any part reports. A stripped framing is reported, not worked
    around."""
    if not os.path.exists(FRAMING):
        return False, "FRAMING.md is not present"
    with open(FRAMING, "r", encoding="utf-8") as fh:
        text = fh.read()
    missing = [ln for ln in FRAMING_LINES if ln not in text]
    if missing:
        return False, "FRAMING.md is present and stripped: %r" % (missing[0],)
    return True, "present, un-stripped"


def parts(full=False):
    rows = []

    record = p1_records.from_json(p1_records.DEMO)
    rows.append({
        "part": "P1", "name": "dependency records",
        "status": "PASS", "detail": (
            "the move runs on a CONSTRUCTED record; "
            "unstated_fraction %.4f" % record.unstated_fraction()),
        "render": p1_records.render(record)})
    rows.append({
        "part": "P1*", "name": "dependency records -- PIPELINE",
        "status": "ABSENT", "detail": (
            "open-access methods sections: no publisher or preprint host "
            "answers in this environment, and none is paraphrased from "
            "memory"),
        "render": ""})

    path = os.path.join(HERE, "p2_substrate.py")
    with open(path, "r", encoding="utf-8") as fh:
        src = fh.read()
    prows = p2_substrate.call_contracts(src)
    rows.append({
        "part": "P2", "name": "substrate check",
        "status": "PASS", "detail": (
            "%d call sites, unverified share %.4f, %d layer contracts"
            % (len(prows), p2_substrate.unverified_fraction(prows),
               len(p2_substrate.LAYERS))),
        "render": p2_substrate.render(path, prows,
                                      p2_substrate.sha256_of(path))})

    corpus_dir = os.path.join(HERE, "fixtures", "corpus")
    if os.path.isdir(corpus_dir):
        corpus = p3_comprehension.read_corpus(corpus_dir)
        res = p3_comprehension.check(corpus)
        rows.append({
            "part": "P3", "name": "comprehension check",
            "status": "PASS", "detail": (
                "%d documents, %d pairs, corpus verdict %s"
                % (res["n_docs"], len(res["pairs"]), res["verdict"])),
            "render": p3_comprehension.render(res, corpus_dir)})
    else:
        rows.append({
            "part": "P3", "name": "comprehension check",
            "status": "ABSENT",
            "detail": "no corpus directory at %s" % corpus_dir,
            "render": ""})

    results = []
    for obj in p4_coherence.CHAINS:
        chain = p4_coherence.read_chain(obj)
        results.append((chain, p4_coherence.settle(chain)))
    verdicts = ", ".join("%s=%s" % (c["label"], r["verdict"])
                         for c, r in results)
    rows.append({
        "part": "P4", "name": "goal-coherence check",
        "status": "PASS", "detail": verdicts,
        "render": p4_coherence.render(results)})

    lrows = [p5_lag.read_action(o) for o in p5_lag.ANCHORS]
    counts = {}
    for r in lrows:
        counts[r["verdict"]] = counts.get(r["verdict"], 0) + 1
    rows.append({
        "part": "P5", "name": "lag declaration check",
        "status": "PASS",
        "detail": ", ".join("%s %d" % (k, counts[k])
                            for k in sorted(counts)),
        "render": p5_lag.render(lrows)})
    return rows


def render(rows, full=False):
    ok, why = framing_present()
    lines = []
    lines.append("COOPERATIVE SUBSTRATE PROOF -- P1-P5")
    lines.append("")
    lines.append("  LOAD-BEARING FRAMING: %s -- %s"
                 % ("OK" if ok else "FAILED", why))
    lines.append("")
    head = "  %-5s %-40s %-8s %s" % ("part", "name", "status", "detail")
    lines.append(head)
    lines.append("  " + "-" * (len(head) - 2))
    for r in rows:
        lines.append("  %-5s %-40s %-8s %s"
                     % (r["part"], r["name"], r["status"], r["detail"][:120]))
    lines.append("")
    lines.append("  Each part also runs standalone:")
    for name in ("p1_records.py", "p2_substrate.py", "p3_comprehension.py",
                 "p4_coherence.py", "p5_lag.py", "scope.py"):
        lines.append("    python3 %s" % name)
    if full:
        for r in rows:
            if r["render"]:
                lines.append("")
                lines.append("=" * 72)
                lines.append("")
                lines.append(r["render"])
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "run_all.py does not carry its own checks.\n"
            "Run: python3 test_proof.py\n")
        return 2
    full = "--full" in argv
    rows = parts(full)
    sys.stdout.write(render(rows, full) + "\n")
    ok, _ = framing_present()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
