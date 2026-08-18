#!/usr/bin/env python3
"""
acquiescence.py - decompose a self-report administration into a trait score
and an acquiescence index, using polarity balance.

Companion to 019-trait-acquiescence-weld.md.

NOT A NEW METHOD. Acquiescent response style (ARS) decomposition on balanced
scales is long-established in psychometrics. This is a harness for applying it
to model administrations and reporting BOTH readings instead of discarding one.

In a polarity-balanced item set:
  - recoding by polarity cancels acquiescence  -> TRAIT
  - raw mean minus scale midpoint cancels trait -> ACQ

Refuses to emit ACQ on an unbalanced set: without balance the two reconfound
and the number would be uninterpretable.

Reports readings. Computes no verdict.

stdlib only.  python3 acquiescence.py --selftest

CC0.
"""

import argparse
import json
import sys
from collections import defaultdict

# Balance tolerance: |forward - reverse| / total must not exceed this.
BALANCE_TOL = 0.10
MIN_ITEMS_PER_TRAIT = 4


def recode(x, polarity, lo, hi):
    """Polarity recode. Reverse items are flipped onto the trait direction."""
    return x if polarity > 0 else (lo + hi) - x


def balance(items):
    fwd = sum(1 for i in items if i["polarity"] > 0)
    rev = sum(1 for i in items if i["polarity"] < 0)
    total = fwd + rev
    if total == 0:
        return 0, 0, None
    return fwd, rev, abs(fwd - rev) / total


def decompose(items, lo, hi):
    """Return (trait, acq, diagnostics). acq is None when unbalanced."""
    midpoint = (lo + hi) / 2.0
    fwd, rev, imbalance = balance(items)

    recoded = [recode(i["response"], i["polarity"], lo, hi) for i in items]
    raw = [i["response"] for i in items]

    trait = sum(recoded) / len(recoded)

    diagnostics = {
        "n_items": len(items),
        "forward": fwd,
        "reverse": rev,
        "imbalance": None if imbalance is None else round(imbalance, 3),
        "midpoint": midpoint,
        "uncorrected_mean": round(sum(raw) / len(raw), 3),
    }

    if imbalance is None or imbalance > BALANCE_TOL:
        diagnostics["acq_state"] = "NOT COMPUTABLE - item set not polarity balanced"
        return round(trait, 3), None, diagnostics

    if len(items) < MIN_ITEMS_PER_TRAIT:
        diagnostics["acq_state"] = "NOT COMPUTABLE - too few items"
        return round(trait, 3), None, diagnostics

    acq = sum(raw) / len(raw) - midpoint
    diagnostics["acq_state"] = "COMPUTED"
    return round(trait, 3), round(acq, 3), diagnostics


def run(admin):
    lo = admin.get("scale_min", 1)
    hi = admin.get("scale_max", 5)
    by_trait = defaultdict(list)
    for item in admin["items"]:
        by_trait[item.get("trait", "unspecified")].append(item)

    out = {"subject": admin.get("subject", "(unnamed)"),
           "scale": [lo, hi], "traits": {}}
    for trait_name, items in sorted(by_trait.items()):
        t, a, d = decompose(items, lo, hi)
        out["traits"][trait_name] = {"trait": t, "acq": a, "diagnostics": d}

    # cross-trait ACQ: the disposition should be trait-general if it is a style
    acqs = [v["acq"] for v in out["traits"].values() if v["acq"] is not None]
    out["acq_across_traits"] = {
        "n": len(acqs),
        "mean": round(sum(acqs) / len(acqs), 3) if acqs else None,
        "spread": round(max(acqs) - min(acqs), 3) if len(acqs) > 1 else None,
    }
    return out


def render(result):
    lines = ["TRAIT / ACQUIESCENCE DECOMPOSITION (no verdict computed)", ""]
    lines.append("subject: %s   scale: %s-%s"
                 % (result["subject"], result["scale"][0], result["scale"][1]))
    lines.append("")
    lines.append("%-20s %8s %8s %10s  %s"
                 % ("trait", "TRAIT", "ACQ", "uncorr", "balance"))
    for name in sorted(result["traits"]):
        v = result["traits"][name]
        d = v["diagnostics"]
        lines.append("%-20s %8s %8s %10s  %d/%d"
                     % (name, v["trait"],
                        "n/a" if v["acq"] is None else v["acq"],
                        d["uncorrected_mean"], d["forward"], d["reverse"]))
        if v["acq"] is None:
            lines.append("     ! %s" % d["acq_state"])

    across = result["acq_across_traits"]
    lines.append("")
    lines.append("ACQ ACROSS TRAITS")
    lines.append("  n=%s  mean=%s  spread=%s"
                 % (across["n"], across["mean"], across["spread"]))
    lines.append("")
    lines.append("READING NOTES")
    lines.append("  TRAIT and ACQ come from the SAME responses. Report both or")
    lines.append("  neither - reporting TRAIT alone is the weld (019).")
    lines.append("  ACQ near 0: agreement disposition not detected at this n.")
    lines.append("  ACQ positive: responses shifted toward agreement independent")
    lines.append("  of item direction.")
    lines.append("  low spread across traits: style-like (trait-general).")
    lines.append("  high spread: something trait-specific is in it - that is 019 Q5,")
    lines.append("  not a cleaner ACQ estimate.")
    lines.append("  'uncorr' is what gets published when polarity is ignored.")
    lines.append("  uncorr minus TRAIT is the size of the problem for this run.")
    return "\n".join(lines)


# --- fixtures ---------------------------------------------------------------

def synth(pattern, n_per_polarity=6, lo=1, hi=5, trait="agreeableness"):
    """Build an administration. pattern in {trait_only, acquiescer, mixed}."""
    items = []
    for k in range(n_per_polarity):
        for polarity in (1, -1):
            if pattern == "trait_only":
                # true trait 4 on the trait direction, no style
                resp = 4 if polarity > 0 else (lo + hi) - 4
            elif pattern == "acquiescer":
                # agrees with everything regardless of direction
                resp = 4
            else:
                # true trait 4 plus a mild agreement push
                base = 4 if polarity > 0 else (lo + hi) - 4
                resp = min(hi, base + 1)
            items.append({"trait": trait, "polarity": polarity,
                          "response": resp, "id": "%s%d" % (
                              "F" if polarity > 0 else "R", k)})
    return {"subject": pattern, "scale_min": lo, "scale_max": hi, "items": items}


def selftest():
    failures = 0
    checks = 0

    def check(label, cond):
        nonlocal failures, checks
        checks += 1
        if not cond:
            failures += 1
            print("FAIL %s" % label)

    r = run(synth("trait_only"))["traits"]["agreeableness"]
    check("pure trait recovers trait 4.0", r["trait"] == 4.0)
    check("pure trait gives ACQ 0", r["acq"] == 0.0)

    r = run(synth("acquiescer"))["traits"]["agreeableness"]
    check("pure acquiescer trait collapses to midpoint", r["trait"] == 3.0)
    check("pure acquiescer ACQ positive", r["acq"] == 1.0)
    check("uncorrected mean hides it",
          r["diagnostics"]["uncorrected_mean"] == 4.0)

    r = run(synth("mixed"))["traits"]["agreeableness"]
    check("mixed trait between", 3.0 < r["trait"] <= 4.0)
    check("mixed ACQ positive", r["acq"] > 0)

    # unbalanced set must refuse
    admin = synth("mixed")
    admin["items"] = [i for i in admin["items"] if i["polarity"] > 0]
    r = run(admin)["traits"]["agreeableness"]
    check("unbalanced refuses ACQ", r["acq"] is None)
    check("unbalanced states why",
          "not polarity balanced" in r["diagnostics"]["acq_state"])

    # too few items must refuse even if balanced
    admin = synth("mixed", n_per_polarity=1)
    r = run(admin)["traits"]["agreeableness"]
    check("too few items refuses ACQ", r["acq"] is None)

    # multi-trait spread
    admin = synth("acquiescer")
    admin["items"] += synth("acquiescer", trait="openness")["items"]
    out = run(admin)
    check("cross-trait n=2", out["acq_across_traits"]["n"] == 2)
    check("style-like spread is 0", out["acq_across_traits"]["spread"] == 0.0)

    check("render runs", "no verdict computed" in render(run(synth("mixed"))))

    print("%d/%d checks passed" % (checks - failures, checks))
    return 1 if failures else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("admin", nargs="?", help="administration JSON")
    ap.add_argument("--jsonl", action="store_true")
    ap.add_argument("--template", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    if args.template:
        print(json.dumps({
            "subject": "",
            "scale_min": 1,
            "scale_max": 5,
            "_note": "polarity: 1 forward, -1 reverse. balanced sets only "
                     "for ACQ. record item id so runs can be re-scored.",
            "items": [
                {"id": "", "trait": "", "polarity": 1, "response": 0},
                {"id": "", "trait": "", "polarity": -1, "response": 0},
            ],
        }, indent=2))
        return 0

    if not args.admin:
        ap.print_help()
        return 2

    result = run(json.load(open(args.admin)))
    print(json.dumps(result, indent=2) if args.jsonl else render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
