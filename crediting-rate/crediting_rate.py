#!/usr/bin/env python3
# crediting_rate.py -- WORK ORDER L. CC0, stdlib only, parses under 3.9.
#
# Does attribution of an imported technique track CONTRIBUTION, or whether
# the loanword survived into the receiving language? A rate comparison
# across loanword bins with the attested ordering held, never an argument
# about one case.
#
#   python3 crediting_rate.py events.jsonl codings.jsonl frame.json [seed]
#   python3 crediting_rate.py --selftest
#
# EVENTS carry the loanword bin and the attested ordering; CODINGS carry
# crediting per reference source, coded blind -- a codings file carrying any
# loanword field is refused. The method layer this order consumes (F, G) is
# not in this tree: G is the five values the order lists, F is emitted as
# branch_set.json in the order's shape, to be lifted when F exists.

import hashlib
import io
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PREDICTION = os.path.join(HERE, "PREDICTION.md")
BRANCH_SET = os.path.join(HERE, "branch_set.json")

MIN_PER_BIN = 3        # [CHOICE] items with attested ordering needed per bin
SHUFFLES = 2000        # [CHOICE] N1 permutations; also the bootstrap count
MISATTR_MAX = 0.2      # [CHOICE] misattribution rate at or below which a null gap reads CONTRIBUTION_TRACKING
BINS = (1, 0)
EVENT_FIELDS = ("item", "domain", "source_tradition", "receiving_tradition", "first_attested_source",
                "first_attested_receiving", "intermediary_count", "loanword_retained", "ordering_source")
CODING_FIELDS = ("item", "source_id", "coder_id", "credits_source", "attribution_depth", "described_originator")
ORIGINATORS = ("source", "receiving", "unstated")


def _jsonl(path):
    with io.open(path, encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            if line.strip():
                try:
                    yield n, json.loads(line)
                except ValueError as exc:
                    raise ValueError("%s line %d: invalid JSON (%s)" % (os.path.basename(path), n, exc))


def _is_int(x):
    return isinstance(x, int) and not isinstance(x, bool)

def load_events(path):
    out = {}
    for n, r in _jsonl(path):
        for f in EVENT_FIELDS:
            if f not in r:
                raise ValueError("events line %d: missing field %s" % (n, f))
        if r["loanword_retained"] not in (0, 1, "ambiguous"):
            raise ValueError("events line %d: loanword_retained must be 0, 1 or 'ambiguous'" % n)
        for f in ("first_attested_source", "first_attested_receiving", "intermediary_count"):
            if r[f] is not None and not _is_int(r[f]):
                raise ValueError("events line %d: field %s must be an integer or null" % (n, f))
        if r["item"] in out:
            raise ValueError("events line %d: duplicate item %s" % (n, r["item"]))
        out[r["item"]] = r
    return out


def load_codings(path):
    out = {}
    for n, r in _jsonl(path):
        if any("loanword" in k for k in r):
            raise ValueError("codings line %d: carries a loanword field; coding must be blind to the bin" % n)
        for f in CODING_FIELDS:
            if f not in r:
                raise ValueError("codings line %d: missing field %s" % (n, f))
        if r["credits_source"] not in (0, 1) or r["attribution_depth"] not in (0, 1, 2, 3):
            raise ValueError("codings line %d: credits_source must be 0/1 and attribution_depth 0..3" % n)
        if r["described_originator"] not in ORIGINATORS:
            raise ValueError("codings line %d: described_originator must be one of %s" % (n, ORIGINATORS))
        out.setdefault(r["item"], []).append(r)
    return out


def load_frame(path):
    with io.open(path, encoding="utf-8") as fh:
        frame = json.load(fh)
    for f in ("corpus", "edition", "date"):
        if f not in frame:
            raise ValueError("frame.json: missing field %s" % f)
    return frame


def ordering_state(ev):
    """known | unknown (either year null or no published source) | reversed (receiving first)."""
    s, r = ev["first_attested_source"], ev["first_attested_receiving"]
    if s is None or r is None or not ev["ordering_source"]:
        return "unknown"
    return "known" if s < r else "reversed"


def join(events, codings):
    """Per-item measures for items with attested ordering AND at least one coding.
    Returns (rows, excluded) where excluded counts every drop by reason."""
    rows, excluded = [], {"ordering_unknown": 0, "ordering_reversed": 0, "uncoded": 0}
    for item in sorted(events):
        ev, state = events[item], ordering_state(events[item])
        if state != "known":
            excluded["ordering_" + state] += 1
            continue
        cs = codings.get(item)
        if not cs:
            excluded["uncoded"] += 1
            continue
        rows.append({"item": item, "bin": ev["loanword_retained"], "domain": ev["domain"],
                     "date": ev["first_attested_source"], "intermediaries": ev["intermediary_count"],
                     "crediting_rate": sum(c["credits_source"] for c in cs) / len(cs),
                     "attribution_depth": sum(c["attribution_depth"] for c in cs) / len(cs),
                     "misattributed": int(any(c["described_originator"] == "receiving" for c in cs)),
                     "sources": len(cs)})
    return rows, excluded


def bin_gap(rates_by_bin):
    """gap = mean rate in the retained bin minus mean rate in the not-retained bin.
    None when either bin is empty (absent, not zero)."""
    a, b = rates_by_bin.get(1) or [], rates_by_bin.get(0) or []
    if not a or not b:
        return None
    return sum(a) / len(a) - sum(b) / len(b)


def rates_by_bin(rows, key="crediting_rate"):
    out = {}
    for r in rows:
        out.setdefault(r["bin"], []).append(r[key])
    return out


def shuffle_band(rows, seed, k=SHUFFLES):
    """N1: reassign the bin labels across the included items, recompute the gap."""
    labelled = [r for r in rows if r["bin"] in BINS]
    labels = [r["bin"] for r in labelled]
    rates = [r["crediting_rate"] for r in labelled]
    rng = random.Random(seed)
    gaps = []
    for _ in range(k):
        rng.shuffle(labels)
        gaps.append(bin_gap({1: [x for x, l in zip(rates, labels) if l == 1], 0: [x for x, l in zip(rates, labels) if l == 0]}))
    gaps = sorted(g for g in gaps if g is not None)
    if not gaps:
        return None
    return {"lo": gaps[int(0.025 * len(gaps))], "hi": gaps[min(len(gaps) - 1, int(0.975 * len(gaps)))], "k": len(gaps)}


def bootstrap_ci(rows, seed, k=SHUFFLES):
    rng = random.Random(seed + 1)
    by = {b: [r["crediting_rate"] for r in rows if r["bin"] == b] for b in BINS}
    if not by[1] or not by[0]:
        return None
    gaps = sorted(bin_gap({b: [rng.choice(by[b]) for _ in by[b]] for b in BINS}) for _ in range(k))
    return [gaps[int(0.025 * k)], gaps[min(k - 1, int(0.975 * k))]]


def strata(rows, keyfn, seed):
    """Gap and shuffle band inside each stratum keyfn assigns (N2, N3, N4)."""
    out = {}
    for s in sorted({keyfn(r) for r in rows}, key=str):
        sub = [r for r in rows if keyfn(r) == s]
        g = bin_gap(rates_by_bin(sub))
        out[str(s)] = {"n": len(sub), "gap": g, "band": shuffle_band(sub, seed) if g is not None else None,
                       "n_by_bin": {str(b): sum(1 for r in sub if r["bin"] == b) for b in BINS}}
    return out


def outside(gap, band):
    return gap is not None and band is not None and not (band["lo"] <= gap <= band["hi"])


def decide(rows, excluded, seed):
    labelled = [r for r in rows if r["bin"] in BINS]
    per_bin = {b: sum(1 for r in labelled if r["bin"] == b) for b in BINS}
    if min(per_bin.values()) < MIN_PER_BIN:
        return {"return": "BLOCKED", "reason": "insufficient_attested_ordering",
                "items_per_bin": per_bin, "excluded": excluded, "min_per_bin": MIN_PER_BIN}
    gap = bin_gap(rates_by_bin(labelled))
    band = shuffle_band(labelled, seed)
    ci = bootstrap_ci(labelled, seed)
    misattr = sum(r["misattributed"] for r in labelled) / len(labelled)
    dates = {str(b): sum(r["date"] for r in labelled if r["bin"] == b) / per_bin[b] for b in BINS}
    median = sorted(r["date"] for r in labelled)[len(labelled) // 2]
    n2 = strata(labelled, lambda r: "early" if r["date"] < median else "late", seed)
    n3 = strata(labelled, lambda r: r["domain"], seed)
    n4 = strata(labelled, lambda r: "0-1" if (r["intermediaries"] or 0) <= 1 else "2+", seed)
    dom_out = [d for d, v in n3.items() if outside(v["gap"], v["band"])]
    res = {"gap": gap, "ci95": ci, "band": band, "misattribution_rate": misattr,
           "mean_date_by_bin": dates, "n_items": per_bin, "excluded": excluded,
           "ambiguous_bin_items": sum(1 for r in rows if r["bin"] == "ambiguous"),
           "N2_antiquity": n2, "N3_domain": n3, "N4_path_length": n4}
    if outside(gap, band):
        if len(dom_out) == 1 and len([d for d in n3 if n3[d]["gap"] is not None]) > 1:
            res.update({"return": "DOMAIN_SPECIFIC", "domain": dom_out[0], "domain_gap": n3[dom_out[0]]["gap"]})
        elif gap > 0:
            res["return"] = "ETYMOLOGY_TRACKING"
        else:
            res.update({"return": "UNKNOWN_measurable", "reason": "gap outside the shuffle band against the predicted direction"})
    elif misattr <= MISATTR_MAX:
        res["return"] = "CONTRIBUTION_TRACKING"
    else:
        res.update({"return": "UNKNOWN_measurable",
                    "reason": "gap inside the shuffle band and misattribution rate %.2f above %.2f" % (misattr, MISATTR_MAX)})
    return res


def prediction_hash():
    if not os.path.isfile(PREDICTION):
        raise ValueError("PREDICTION.md missing: the prediction is recorded before any run, or there is no run")
    with io.open(PREDICTION, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run(events_path, codings_path, frame_path, seed=0):
    frame = load_frame(frame_path)
    out = {"prediction_sha256": prediction_hash(), "frame": frame, "seed": seed}
    if any(frame[f] == "UNDECLARED" for f in ("corpus", "edition", "date")):
        out.update({"return": "BLOCKED", "reason": "frame_undeclared",
                    "note": "frame_undeclared is an addition to the order's BLOCKED reason; the frame is a parameter and an undeclared one is not a run"})
        return out
    rows, excluded = join(load_events(events_path), load_codings(codings_path))
    out.update(decide(rows, excluded, seed))
    out["rows"] = rows
    return out


def render(out):
    lines = ["crediting_rate -- prediction sha256 %s -- seed %s" % (out["prediction_sha256"][:16], out["seed"]),
             "frame: %s / %s / %s" % (out["frame"]["corpus"], out["frame"]["edition"], out["frame"]["date"]),
             "RETURN: %s%s" % (out["return"], " (%s)" % out["reason"] if "reason" in out else "")]
    if "gap" in out:
        f = lambda x: "--" if x is None else "%.3f" % x  # noqa: E731
        lines.append("gap = %s  ci95 = %s  N1 band = [%s, %s] over %d shuffles" % (
            f(out["gap"]), None if out["ci95"] is None else [round(c, 3) for c in out["ci95"]],
            f(out["band"]["lo"]) if out["band"] else "--", f(out["band"]["hi"]) if out["band"] else "--",
            out["band"]["k"] if out["band"] else 0))
        lines.append("items per bin %s  excluded %s  ambiguous bin %d  misattribution %.2f  mean date by bin %s" % (
            out["n_items"], out["excluded"], out["ambiguous_bin_items"], out["misattribution_rate"],
            {k: round(v) for k, v in out["mean_date_by_bin"].items()}))
        for name in ("N2_antiquity", "N3_domain", "N4_path_length"):
            for s, v in out[name].items():
                lines.append("  %-15s %-10s n=%-3d gap=%s band=%s" % (
                    name, s, v["n"], f(v["gap"]), None if v["band"] is None else [round(v["band"]["lo"], 3), round(v["band"]["hi"], 3)]))
    else:
        lines.append("  %s" % {k: v for k, v in out.items() if k not in ("prediction_sha256", "frame", "seed", "return", "reason")})
    return "\n".join(lines)


def selftest():
    n = [0]

    def check(cond, msg):
        n[0] += 1
        if not cond:
            print("FAIL %d: %s" % (n[0], msg))
            sys.exit(1)
    fx = os.path.join(HERE, "fixtures")
    frame = {"corpus": "constructed", "edition": "0", "date": "2026-09-07"}
    fp = os.path.join(fx, "frame.constructed.json")
    with io.open(fp, "w", encoding="utf-8") as fh:
        json.dump(frame, fh)
    ety = run(os.path.join(fx, "events.constructed.jsonl"), os.path.join(fx, "codings.etymology.constructed.jsonl"), fp, 7)
    nul = run(os.path.join(fx, "events.constructed.jsonl"), os.path.join(fx, "codings.null.constructed.jsonl"), fp, 7)
    check(ety["return"] == "ETYMOLOGY_TRACKING" and abs(ety["gap"] - 0.6) < 1e-9, "etymology world: gap 0.6 outside band")
    check(nul["return"] == "CONTRIBUTION_TRACKING" and nul["band"]["lo"] <= nul["gap"] <= nul["band"]["hi"] and nul["band"]["lo"] < 0 < nul["band"]["hi"],
          "null world: rates vary by item not by bin, gap inside a band that brackets zero, no misattribution")
    check(ety["return"] != nul["return"], "the return is not constant across the two constructed worlds")
    check(ety["ambiguous_bin_items"] == 1 and ety["n_items"] == {1: 5, 0: 5}, "ambiguous is its own bin, not assigned")
    check(ety["band"]["lo"] < 0 < ety["band"]["hi"], "N1 band brackets zero")
    check(all(v["gap"] is not None for v in ety["N3_domain"].values()), "N3 gap per domain computed")
    cand = run(os.path.join(fx, "events.candidates.jsonl"), os.path.join(fx, "codings.null.constructed.jsonl"), fp, 7)
    check(cand["return"] == "BLOCKED" and cand["excluded"]["ordering_unknown"] == 10 and cand["reason"] == "insufficient_attested_ordering",
          "candidates with null ordering -> BLOCKED(insufficient_attested_ordering), ten excluded and counted")
    check(run(os.path.join(fx, "events.constructed.jsonl"), os.path.join(fx, "codings.null.constructed.jsonl"), os.path.join(HERE, "frame.json"), 7)["reason"] == "frame_undeclared",
          "undeclared frame -> BLOCKED(frame_undeclared)")
    leaky = os.path.join(fx, "codings.leaky.tmp.jsonl")
    with io.open(leaky, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"item": "alpha", "source_id": "r", "coder_id": "c", "credits_source": 1, "attribution_depth": 2,
                             "described_originator": "source", "loanword_retained": 1}) + "\n")
    try:
        load_codings(leaky)
        check(False, "leaky codings accepted")
    except ValueError as exc:
        check("blind" in str(exc), "codings carrying the bin are refused: %s" % exc)
    os.remove(leaky)
    check(bin_gap({1: [1.0, 1.0], 0: [0.0]}) == 1.0 and bin_gap({1: [0.5], 0: [0.5]}) == 0.0 and bin_gap({1: [0.5], 0: []}) is None, "bin_gap known answers")
    rev = dict(load_events(os.path.join(fx, "events.constructed.jsonl"))["alpha"], first_attested_source=2000)
    check(ordering_state(rev) == "reversed", "receiving-first ordering is reversed, not an import")
    check(json.load(io.open(BRANCH_SET, encoding="utf-8"))["discriminator"].startswith("crediting rate"), "branch set carries the discriminator")
    check(render(ety).startswith("crediting_rate -- prediction sha256"), "render carries the prediction hash")
    check(run(os.path.join(fx, "events.constructed.jsonl"), os.path.join(fx, "codings.etymology.constructed.jsonl"), fp, 7) == ety, "deterministic under a fixed seed")
    check(all(v["gap"] is not None for v in ety["N2_antiquity"].values()), "N2 strata each hold both bins on the constructed events (dates not confounded with bin)")
    print("crediting_rate selftest: %d/%d checks pass" % (n[0], n[0]))


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        selftest()
    elif len(sys.argv) in (4, 5):
        print(render(run(sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) == 5 else 0)))
    else:
        print("usage: crediting_rate.py events.jsonl codings.jsonl frame.json [seed] | --selftest", file=sys.stderr)
        sys.exit(2)
