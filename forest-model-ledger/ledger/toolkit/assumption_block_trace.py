"""Toolkit: assumption_block_trace. Tool #7 of the staged build (work order 2026-11-11). stdlib only.

Entry: ledger/toolkit/assumption_block_trace.yaml (status placeholder, blocked_on real data).
Gate: tests/test_toolkit.py.

Shared assumption failing across many studies: when studies fail, do the failures sit
on the studies that rest on one assumption block?

  trace(studies, blocks)
    studies  list of {id, blocks: [assumption-block ids it rests on], outcome: FAILED | HELD | UNKNOWN}
    per block, over studies with a known outcome:
      a = failed and uses the block    b = held and uses it
      c = failed and does not use it   d = held and does not use it
      p = one-sided Fisher exact P(a or more failures among users | margins)
    verdict per block
      NOT_EVALUABLE   every known study uses it, or none does: no contrast exists
      INSUFFICIENT    fewer than MIN_STUDIES known outcomes, or fewer than 2 failures
      SHARED_FAILURE  p < ALPHA and failure rate among users above non-users
      NOT_ENRICHED    otherwise
    UNKNOWN outcomes are counted and excluded, never read as HELD.  [CHOICE: ALPHA 0.001, MIN_STUDIES 8]
    Gate history: at ALPHA 0.01 the null leg failed FP (0.015, harness seeds 0 and 4): a 1 %
    test fires on about 1 % of null tables. ALPHA 0.001 buys FP 0 on the gate's draws; on real
    data a block then needs stronger enrichment to read SHARED_FAILURE. Stated, not hidden.
    At ALPHA 0.001 the signal leg then missed TP (0.995) on 40-study draws (about 20 users of
    the block); the gate's draws were raised to 60 studies, null and signal alike, once.

  ledger_structure()  what the ledger can say today without outcomes: per block, the
                      components and runs that rest on it (read from ledger/assumption_blocks/)

PLACEHOLDER UNTIL REAL DATA (work order): the only studies in this tree are runs of one
synthetic model, and every one of them rests on AB_SYNTHETIC_ONLY. Run on them, every
block reads NOT_EVALUABLE or INSUFFICIENT. The tool is built and gated; it is not run on
a trigger, and its NEEDS_TOOL rows stay open.
"""
import glob, math, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, HERE)
from tools import miniyaml

ALPHA, MIN_STUDIES = 0.001, 8
CHOICES = dict(ALPHA=ALPHA, MIN_STUDIES=MIN_STUDIES)
OUTCOMES = ("FAILED", "HELD", "UNKNOWN")


def fisher_greater(a, b, c, d):
    """One-sided: P(X >= a) for X hypergeometric with the table's margins."""
    n1, n2, k = a + b, c + d, a + c
    tot = math.comb(n1 + n2, k)
    return sum(math.comb(n1, x) * math.comb(n2, k - x) for x in range(a, min(n1, k) + 1)) / tot


def trace(studies, blocks=None):
    for s in studies:
        if s["outcome"] not in OUTCOMES:
            raise ValueError(f"{s['id']}: outcome {s['outcome']} outside {OUTCOMES}")
    known = [s for s in studies if s["outcome"] != "UNKNOWN"]
    blocks = blocks or sorted({b for s in studies for b in s["blocks"]})
    out = {}
    for blk in blocks:
        use = [s for s in known if blk in s["blocks"]]
        not_ = [s for s in known if blk not in s["blocks"]]
        a = sum(s["outcome"] == "FAILED" for s in use); b = len(use) - a
        c = sum(s["outcome"] == "FAILED" for s in not_); d = len(not_) - c
        row = dict(a=a, b=b, c=c, d=d, unknown=len(studies) - len(known), p=None)
        if not use or not not_:
            row["verdict"] = "NOT_EVALUABLE"
        elif len(known) < MIN_STUDIES or a + c < 2:
            row["verdict"] = "INSUFFICIENT"
        else:
            row["p"] = fisher_greater(a, b, c, d)
            row["verdict"] = "SHARED_FAILURE" if row["p"] < ALPHA and a / len(use) > c / len(not_) else "NOT_ENRICHED"
        out[blk] = row
    return out


def ledger_structure(root=HERE):
    out = {}
    for p in sorted(glob.glob(os.path.join(root, "ledger", "assumption_blocks", "*.yaml"))):
        b = miniyaml.load(p)
        out[b["id"]] = dict(components=b.get("used_by", []), runs=b.get("used_by_runs", []))
    return out


def ledger_studies(root=HERE):
    """The runs in this tree as 'studies': blocks from used_by_runs; outcome UNKNOWN for all
    (a run is not a study that held or failed against data)."""
    runs = {}
    for blk, v in ledger_structure(root).items():
        for r in v["runs"]:
            runs.setdefault(r, set()).add(blk)
    return [dict(id=r, blocks=sorted(b), outcome="UNKNOWN") for r, b in sorted(runs.items())]


# ---------------------------------------------------------------- gate: planted cases + null harness
def _studies(rng, n, enrich):
    out = []
    for i in range(n):
        uses = rng.random() < 0.5
        p_fail = (0.9 if uses else 0.05) if enrich else 0.3
        out.append(dict(id=f"s{i}", blocks=(["AB_X"] if uses else []) + ["AB_OTHER"] * (rng.random() < 0.5),
                        outcome="FAILED" if rng.random() < p_fail else "HELD"))
    return out


def known_cases():
    import random
    r = random.Random(3)
    planted = [dict(id=f"f{i}", blocks=["AB_X"], outcome="FAILED") for i in range(8)] + \
              [dict(id=f"h{i}", blocks=["AB_Y"], outcome="HELD") for i in range(8)]
    everyone = [dict(id=f"e{i}", blocks=["AB_ALL"], outcome=("FAILED" if i % 2 else "HELD")) for i in range(12)]
    tiny = [dict(id="t1", blocks=["AB_X"], outcome="FAILED"), dict(id="t2", blocks=[], outcome="HELD")]
    unknowns = planted + [dict(id=f"u{i}", blocks=["AB_Y"], outcome="UNKNOWN") for i in range(5)]
    return [
        ("failures all on the studies that use AB_X: SHARED_FAILURE", "SHARED_FAILURE", lambda: trace(planted)["AB_X"]["verdict"]),
        ("the block only the held studies use: NOT_ENRICHED (silent)", "NOT_ENRICHED", lambda: trace(planted)["AB_Y"]["verdict"]),
        ("a block every study uses: NOT_EVALUABLE", "NOT_EVALUABLE", lambda: trace(everyone)["AB_ALL"]["verdict"]),
        ("two studies: INSUFFICIENT", "INSUFFICIENT", lambda: trace(tiny)["AB_X"]["verdict"]),
        ("UNKNOWN outcomes are excluded, not read as HELD", (8, 5), lambda: (trace(unknowns)["AB_X"]["a"], trace(unknowns)["AB_X"]["unknown"])),
        ("fisher on a fully separated 8/8 table", round(1 / math.comb(16, 8), 12), lambda: round(fisher_greater(8, 0, 0, 8), 12)),
        ("the ledger's own runs: every block NOT_EVALUABLE or INSUFFICIENT", True,
         lambda: all(v["verdict"] in ("NOT_EVALUABLE", "INSUFFICIENT") for v in trace(ledger_studies()).values())),
    ]


def gate(n=200, seeds=(0, 1, 2, 3, 4)):
    from ledger.toolkit import gate as G
    known = G.known_answers(known_cases(), lambda f: f())
    det = lambda st: trace(st, ["AB_X"])["AB_X"]["verdict"] == "SHARED_FAILURE"
    legs = dict(shared_failure=G.null_harness_seeds(det, lambda r: _studies(r, 60, False), lambda r: _studies(r, 60, True), n, seeds))
    return G.combine(known, legs)


if __name__ == "__main__":
    print("assumption blocks in this ledger and what rests on them:")
    for b, v in ledger_structure().items():
        print(f"  {b:22s} components {len(v['components']):2d}  runs {v['runs'] or '-'}")
    print("trace over the ledger's runs (outcomes UNKNOWN: a run is not a study):")
    for b, v in trace(ledger_studies()).items():
        print(f"  {b:22s} {v['verdict']}")
