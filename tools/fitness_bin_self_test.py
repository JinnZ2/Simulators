#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""WO-7: a fitness-function bin self-test. Stdlib only, Python >= 3.9.

ONE DELIBERATE LEAK: LEAKY wraps at every grid edge. Fitness only reads the
final position, not the route or wraps. SEALED clamps attempted edge exits.
Start (0, 0), goal (size-1, size-1); N increases y. No obstacles, rewards,
energy, randomness in the world, or secondary selection score.

MEANT: reach the goal on a wrap-free walk (at any step), with the WHOLE
recorded route wrap-free. MEASURED: negative final Manhattan distance.
The anytime/final distinction is declared, not another hidden simulator
channel. Reaching then leaving can diverge even without a wrap.

Defaults fixed before first run: seed=7, size=9, length=24, population=40,
generations=60, retained=8, top=5. A and B share the same initial population
and RNG seed; after fitness changes selections, their later paths differ.
Selection never consults wrap counts, walking success, or replay scores.

Every genome selection discards is retained in memory with its generation
and native score. --archive PATH exports those records as JSON. The normal
render prints count, content hash, and a deterministic sample, not all rows.
T5 is diagnostic and cannot change selection. No auto-patching occurs.

Expected: A wrap use + paired SEALED score loss; B no wrap. If A has no
wrap at this budget, INCONCLUSIVE, not a reason to tune. Verdict/exit code
in a normal run checks control integrity only, not an empirical claim.
"""

import argparse
import hashlib
import json
import math
import random
import sys

MOVES = "NSEW"
DELTAS = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
LEAKY = "LEAKY"
SEALED = "SEALED"


def fitness(position, goal):
    """Only the endpoint is visible to selection. Higher is better."""
    return -(abs(position[0] - goal[0]) + abs(position[1] - goal[1]))


def replay(genome, environment, size=9):
    if environment not in (LEAKY, SEALED) or size < 2:
        raise ValueError("environment must be LEAKY/SEALED; size >= 2")
    x = y = 0
    goal = (size - 1, size - 1)
    wraps = blocked = 0
    counts = dict.fromkeys(MOVES, 0)
    touched = False
    trace = [[x, y]]
    for move in genome:
        if move not in DELTAS:
            raise ValueError("genome must contain only N/S/E/W")
        counts[move] += 1
        dx, dy = DELTAS[move]
        nx, ny = x + dx, y + dy
        outside = not (0 <= nx < size and 0 <= ny < size)
        if environment == LEAKY:
            wraps += int(outside)
            x, y = nx % size, ny % size
        else:
            blocked += int(outside)
            x, y = min(size - 1, max(0, nx)), min(size - 1, max(0, ny))
        touched = touched or (x, y) == goal
        trace.append([x, y])
    return {"genome": "".join(genome), "environment": environment,
            "final": [x, y], "score": fitness((x, y), goal),
            "counts": counts, "wraps": wraps, "blocked": blocked,
            "reached_goal": touched, "meant": touched and wraps == 0,
            "trace": trace}


def wrap_share(records):
    """T3: None is no winners; 0.0 is observed no use."""
    if not records:
        return None
    return sum(r["wraps"] > 0 for r in records) / len(records)


def diversity(population):
    """Mean normalized pairwise Hamming distance, duplicate slots retained."""
    if len(population) < 2:
        return None
    length = len(population[0])
    if length == 0 or any(len(g) != length for g in population):
        raise ValueError("diversity needs equal, positive genome lengths")
    differences = pairs = 0
    for i, a in enumerate(population):
        for b in population[i + 1:]:
            differences += sum(x != y for x, y in zip(a, b))
            pairs += 1
    return differences / (pairs * length)


def fitness_drop(native, changed):
    """T2: positive means a loss off the native substrate."""
    return native - changed


def locus_counts(population):
    if not population:
        return []
    length = len(population[0])
    if length == 0 or any(len(g) != length for g in population):
        raise ValueError("allele counts need equal, positive genome lengths")
    counts = [dict.fromkeys(MOVES, 0) for _ in range(length)]
    for genome in population:
        for locus, allele in enumerate(genome):
            if allele not in MOVES:
                raise ValueError("unknown allele")
            counts[locus][allele] += 1
    return counts


def allele_entropy(population):
    """Sum marginal per-locus Shannon entropies in bits; not joint entropy."""
    if not population:
        return None
    n = len(population)
    return sum(-(count / n) * math.log2(count / n)
               for row in locus_counts(population) for count in row.values()
               if count)


def lost_support(before, survivors):
    """Last active breeding copy lost; archive retention is a separate state."""
    a, b = locus_counts(before), locus_counts(survivors)
    if not a or not b or len(a) != len(b):
        raise ValueError("loss ledger needs two nonempty equal-length populations")
    return [{"locus": i, "allele": move, "copies_before": row[move]}
            for i, row in enumerate(a) for move in MOVES
            if row[move] > 0 and b[i][move] == 0]


def rediscovery_wait(children, mutation_rate, alphabet=4):
    """Conditional geometric waiting time for an absent single-locus allele.

    This implementation redraws uniformly from ALL k alleles, including the
    old one. Each mutated child therefore supplies the lost allele with
    probability mu/k, NOT mu/(k-1). Retained elites never mutate. Assumes
    independent child draws, fixed budget, and absent parental support until
    the first reappearance. Does not promise usefulness or survival afterward.
    """
    if children < 1 or alphabet < 2 or not 0 <= mutation_rate <= 1:
        raise ValueError("invalid mutation supply")
    if mutation_rate == 0:
        return None  # no finite rediscovery, not measured zero waiting
    probability = -math.expm1(children * math.log1p(-mutation_rate / alphabet))
    return 1 / probability


def archive_ratio(wait, hold_cost, generation_cost, unit=None):
    """Conditional rebuild/hold ratio; never divides bytes by generations."""
    if not unit or any(x is None for x in (wait, hold_cost, generation_cost)):
        return "UNRATED"
    if any(not math.isfinite(x) for x in (wait, hold_cost, generation_cost)):
        raise ValueError("costs and waiting time must be finite")
    if wait <= 0 or hold_cost <= 0 or generation_cost < 0:
        return "UNRATED"
    return wait * generation_cost / hold_cost


def evolve(environment, seed=7, size=9, length=24, population=40,
           generations=60, retained=8, top=5, hold_cost=None,
           generation_cost=None, cost_unit=None):
    if not (size >= 2 and length > 0 and generations >= 0
            and 1 <= retained < population and 1 <= top <= population):
        raise ValueError("invalid grid, genome, generation or selection budget")
    rng = random.Random(seed)
    pop = ["".join(rng.choice(MOVES) for _ in range(length))
           for _ in range(population)]
    archive, history, ledger = [], [], []
    wait = rediscovery_wait(population - retained, 1 / length)
    ratio = archive_ratio(wait, hold_cost, generation_cost, cost_unit)
    for generation in range(generations + 1):
        # Stable ties: first slot wins. Neither novelty nor wrap is a key.
        ranked = sorted(pop, key=lambda g: fitness(
            replay(g, environment, size)["final"], (size - 1, size - 1)),
                        reverse=True)
        history.append({"generation": generation,
                        "diversity": diversity(pop),
                        "allele_entropy_bits": allele_entropy(pop),
                        "best_score": replay(ranked[0], environment, size)["score"]})
        if generation == generations:
            break
        survivors = ranked[:retained]
        h_before = allele_entropy(pop)
        h_survivors = allele_entropy(survivors)
        lost = lost_support(pop, survivors)
        archive.extend({"generation": generation, "genome": g,
                        "score": replay(g, environment, size)["score"]}
                       for g in ranked[retained:])
        pop = list(survivors)
        while len(pop) < population:
            a, b = rng.choice(survivors), rng.choice(survivors)
            cut = rng.randrange(length + 1)
            child = a[:cut] + b[cut:]
            child = "".join(rng.choice(MOVES) if rng.random() < 1 / length
                            else m for m in child)
            pop.append(child)
        after = locus_counts(pop)
        for event in lost:
            event["restored_next_generation"] = after[event["locus"]][event["allele"]] > 0
            event["archive_retained"] = True
        ledger.append({"generation": generation, "H_before_bits": h_before,
                       "H_survivors_bits": h_survivors,
                       "H_next_bits": allele_entropy(pop),
                       "entropy_drop_selection_bits": h_before - h_survivors,
                       "entropy_drop_total_bits": h_before - allele_entropy(pop),
                       "last_active_copy_losses": lost,
                       "rediscovery_generations_conditional": wait,
                       "rebuild_over_hold": ratio, "cost_unit": cost_unit})
    initial = history[0]["diversity"]
    half = next((r["generation"] for r in history
                 if initial is not None and r["diversity"] < initial / 2), None)
    return {"environment": environment,
            "winners": [replay(g, environment, size) for g in ranked[:top]],
            "archive": archive, "history": history, "ledger": ledger,
            "half_generation": half,
            "early_collapse": half is not None and half <= generations // 4}


def readout(winner, rank, changed):
    if winner["wraps"] == 0:
        return None
    return {"channel": "edge_wrap", "winner_rank": rank,
            "genome": winner["genome"], "wrap_events": winner["wraps"],
            "how_found": "T3 transition counter; T2 identical-genome SEALED replay",
            "substrate_reading": "LEAKY topology permits boundary jumps; endpoint score omits route",
            "fact_kind": "INSTRUMENT", "system": "toy grid simulator, not real walking",
            "native_score": winner["score"], "sealed_score": changed["score"],
            "fitness_drop": fitness_drop(winner["score"], changed["score"]),
            "decision": "UNDECIDED; recorded before any patch"}


def classify(a_winners, b_winners, changed):
    if wrap_share(b_winners) != 0.0:
        return "TOOL_FAULT"
    if wrap_share(a_winners) == 0.0:
        return "INCONCLUSIVE"
    if any(a["wraps"] > 0 and fitness_drop(a["score"], b["score"]) > 0
           for a, b in zip(a_winners, changed)):
        return "POSITIVE"
    return "NEGATIVE"  # joint wrap-and-loss prediction did not hold


def experiment(**budget):
    a = evolve(LEAKY, **budget)
    b = evolve(SEALED, **budget)
    changed = [replay(w["genome"], SEALED, budget.get("size", 9))
               for w in a["winners"]]
    return {"budget": budget, "A": a, "B": b, "changed": changed,
            "run_a": classify(a["winners"], b["winners"], changed)}


def render(result):
    out = ["WO-7 FITNESS BIN SELF-TEST -- synthetic instrument calibration; CC0",
           "BUDGET " + json.dumps(result["budget"], sort_keys=True),
           "EXPECTED (declared before run): A wraps and loses score in SEALED; B T3 silent.",
           "No budget/seed search; no patch; measured score uses ONLY final position.",
           "T1 WHOSE GOAL: FLAG -- human + Claude WO-7, implemented by Manus; outside seat.",
           "MEANT reach goal by a wrap-free walk; MEASURED negative final Manhattan distance.",
           "T3 CHANNEL LEDGER: endpoint x/y COUNTED; N/S/E/W route, wraps, blocked attempts NOT COUNTED."]
    for label in ("A", "B"):
        run = result[label]
        share = wrap_share(run["winners"])
        out.append("\nRun %s %s: T3=%s wrap_share=%.6f" % (
            label, run["environment"], "FLAG" if share > 0 else "SILENT", share))
        for i, w in enumerate(run["winners"], 1):
            out.append("winner %d genome=%s final=%s MEASURED=%d MEANT=%s "
                       "wrap_free=%s wraps=%d steps=%s blocked=%d" % (
                           i, w["genome"], w["final"], w["score"],
                           "yes" if w["meant"] else "no",
                           "yes" if w["wraps"] == 0 else "no", w["wraps"],
                           json.dumps(w["counts"], sort_keys=True), w["blocked"]))
            # T4 is not an implicit score threshold: a measured endpoint
            # success (score 0) and MEANT must agree to avoid this flag.
            out.append("  T4=%s (endpoint_success=%s; meant_success=%s)" % (
                "FLAG" if (w["score"] == 0) != w["meant"] else "SILENT",
                w["score"] == 0, w["meant"]))
            if label == "A":
                c = result["changed"][i - 1]
                loss = fitness_drop(w["score"], c["score"])
                out.append("  T2 SEALED identical-genome replay: score=%d drop=%d %s" % (
                    c["score"], loss, "FLAG" if loss > 0 else "SILENT"))
        out.append("T5 diversity by generation (mean normalized pairwise Hamming):")
        out.extend("  generation=%d diversity=%.6f" % (h["generation"], h["diversity"])
                   for h in run["history"])
        out.append("T5 first_below_half_start=%s early=%s (early <= generations//4)" % (
            run["half_generation"], run["early_collapse"]))
        encoded = json.dumps(run["archive"], sort_keys=True,
                             separators=(",", ":")).encode("ascii")
        out.append("T5 archived_discard_slots=%d sha256=%s" % (
            len(run["archive"]), hashlib.sha256(encoded).hexdigest()))
        out.append("T5 archive sample: first five discarded slots (not representative):")
        out.extend("  " + json.dumps(r, sort_keys=True) for r in run["archive"][:5])
        out.append("T5+ ERASURE LEDGER: marginal entropy bits; last ACTIVE copies only; archives still hold them.")
        out.append("Mutation redraw includes the old allele; children=population-retained, supply=mu/k.")
        out.append("No physical joules; UNRATED cost ratio means no comparable costs supplied.")
        for row in run["ledger"]:
            out.append("T5+ " + json.dumps(row, sort_keys=True))
        out.append("T5+ H and fitness by generation:")
        out.extend("  generation=%d H_bits=%.6f best_score=%d" % (
            h["generation"], h["allele_entropy_bits"], h["best_score"])
                   for h in run["history"])
    out.append("\nT6 READOUTS -- emitted before any intervention; no simulator was patched:")
    records = [readout(w, i, c) for i, (w, c) in enumerate(
        zip(result["A"]["winners"], result["changed"]), 1)]
    out.extend(json.dumps(r, sort_keys=True) for r in records if r is not None)
    if not any(r is not None for r in records):
        out.append("NONE DETECTED at the stated budget; not proof of absence")
    out.append("RUN_A: " + result["run_a"])
    out.append("CONTROL_B: " + ("BROKEN" if result["run_a"] == "TOOL_FAULT" else "NEGATIVE (T3 silent)"))
    out.append("SELF_GRADED: synthetic checks are not external validation of specimens or world claims.")
    failed = int(result["run_a"] == "TOOL_FAULT")
    out.append("Control integrity only (not Run A prediction):")
    out.append("VERDICT: %s   checks=1 failed=%d" % ("FAIL" if failed else "PASS", failed))
    return "\n".join(out) + "\n"


def selftest():
    checks = []

    def chk(name, actual, expected):
        checks.append((name, actual == expected, actual, expected))

    w = replay("WS", LEAKY)
    p = replay("N" * 8 + "E" * 8, LEAKY)
    chk("wrap genome lands on goal", w["final"], [8, 8])
    chk("two wrap events counted", w["wraps"], 2)
    chk("wrap goal is not walking", w["meant"], False)
    chk("wrap trips T3", wrap_share([w]), 1.0)
    chk("wrap-free genome does not trip T3", wrap_share([p]), 0.0)
    chk("walking goal reached", p["meant"], True)
    chk("SEALED blocks wrap genome", replay("WS", SEALED)["final"], [0, 0])
    chk("SEALED no wrap events", replay("WS", SEALED)["wraps"], 0)
    chk("SEALED boundary attempts counted", replay("WS", SEALED)["blocked"], 2)
    chk("T2 known score drop", fitness_drop(0, -16), 16)
    chk("T2 held score", fitness_drop(0, 0), 0)
    chk("T2 improvement has negative sign", fitness_drop(-3, 0), -3)
    chk("final score known zero", fitness([8, 8], [8, 8]), 0)
    chk("final score known start", fitness([0, 0], [8, 8]), -16)
    chk("T3 empty is absent not zero", wrap_share([]), None)
    chk("T3 mixed half", wrap_share([w, p]), 0.5)
    # NN/NE/EE distances 1,2,1; normalized mean = 4/(3*2).
    chk("diversity hand computation", diversity(["NN", "NE", "EE"]), 2 / 3)
    chk("diversity clones", diversity(["NN", "NN"]), 0.0)
    chk("diversity opposite", diversity(["NN", "EE"]), 1.0)
    chk("diversity no pairs", diversity(["NN"]), None)
    chk("diversity empty", diversity([]), None)
    chk("duplicates are population slots", diversity(["NN", "NN", "EE"]), 2 / 3)
    chk("visited then left is meant", replay("N" * 8 + "E" * 8 + "W", SEALED)["meant"], True)
    chk("visited then left final not success", replay("N" * 8 + "E" * 8 + "W", SEALED)["score"], -1)
    chk("T6 wrap record instrument", readout(w, 1, replay("WS", SEALED))["fact_kind"], "INSTRUMENT")
    chk("T6 no wrap no record", readout(p, 1, p), None)
    chk("positive read", classify([w], [p], [replay("WS", SEALED)]), "POSITIVE")
    chk("inconclusive read", classify([p], [p], [p]), "INCONCLUSIVE")
    chk("negative joint read", classify([w], [p], [w]), "NEGATIVE")
    chk("planted broken control", classify([w], [w], [w]), "TOOL_FAULT")
    small = dict(seed=7, size=9, length=24, population=12,
                 generations=4, retained=3, top=3)
    r1, r2 = experiment(**small), experiment(**small)
    chk("same seed identical complete output", render(r1), render(r2))
    chk("archive every discarded A slot", len(r1["A"]["archive"]), 36)
    chk("archive every discarded B slot", len(r1["B"]["archive"]), 36)
    chk("generation zero and final kept", len(r1["A"]["history"]), 5)
    chk("B control silent", wrap_share(r1["B"]["winners"]), 0.0)
    zero = evolve(LEAKY, generations=0)
    chk("zero generations no selection discards", len(zero["archive"]), 0)
    chk("N axis wraps", replay("S", LEAKY)["final"], [0, 8])
    chk("E axis wraps", replay("W", LEAKY)["final"], [8, 0])
    chk("counts sum to genome length", sum(w["counts"].values()), 2)
    chk("entropy balanced two alleles", allele_entropy(["N", "E"]), 1.0)
    chk("entropy four alleles", allele_entropy(["N", "S", "E", "W"]), 2.0)
    chk("entropy clones", allele_entropy(["NN", "NN"]), 0.0)
    chk("entropy absent", allele_entropy([]), None)
    chk("last copy lost", lost_support(["N", "E"], ["N"]),
        [{"locus": 0, "allele": "E", "copies_before": 1}])
    chk("allele survives once", lost_support(["N", "N", "E"], ["N", "E"]), [])
    chk("lost multiple copies still support loss", lost_support(["N", "E", "E"], ["N"])[0]["copies_before"], 2)
    chk("waiting one child half probability", rediscovery_wait(1, 1.0, 2), 2.0)
    chk("waiting two children three-quarter probability", round(rediscovery_wait(2, 1.0, 2), 12), round(4 / 3, 12))
    chk("no mutation no finite rediscovery", rediscovery_wait(2, 0.0), None)
    chk("cost ratio comparable", archive_ratio(2, 4, 3, "work_units"), 1.5)
    chk("cost ratio absent is UNRATED", archive_ratio(2, None, 3, "work_units"), "UNRATED")
    chk("cost ratio missing unit is UNRATED", archive_ratio(2, 4, 3), "UNRATED")
    chk("ledger every selection step", len(r1["A"]["ledger"]), 4)
    for name, fn in [("bad move refused", lambda: replay("X", LEAKY)),
                     ("bad world refused", lambda: replay("N", "OTHER")),
                     ("unequal diversity refused", lambda: diversity(["N", "NN"])),
                     ("bad retention refused", lambda: evolve(LEAKY, retained=40))]:
        try:
            fn()
        except ValueError:
            chk(name, True, True)
        else:
            chk(name, False, True)
    for name, ok, got, expected in checks:
        print(("PASS " if ok else "FAIL ") + name)
        if not ok:
            print("  got=%r expected=%r" % (got, expected))
    failed = sum(not c[1] for c in checks)
    print("VERDICT: %s   checks=%d failed=%d" % (
        "FAIL" if failed else "PASS", len(checks), failed))
    return int(failed > 0)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--size", type=int, default=9)
    parser.add_argument("--length", type=int, default=24)
    parser.add_argument("--population", type=int, default=40)
    parser.add_argument("--generations", type=int, default=60)
    parser.add_argument("--retained", type=int, default=8)
    parser.add_argument("--top", type=int, default=5)
    parser.add_argument("--archive", help="optional full discard archive JSON path")
    parser.add_argument("--hold-cost", type=float, help="per-lost-allele archive/retrieval cost over a declared horizon")
    parser.add_argument("--generation-cost", type=float, help="rebuild cost per generation in the SAME unit")
    parser.add_argument("--cost-unit", help="declared common cost unit; otherwise ratio UNRATED")
    args = parser.parse_args(argv)
    if args.selftest:
        return selftest()
    budget = {key: getattr(args, key) for key in (
        "seed", "size", "length", "population", "generations", "retained", "top",
        "hold_cost", "generation_cost", "cost_unit")}
    try:
        result = experiment(**budget)
        if args.archive:
            with open(args.archive, "w", encoding="utf-8") as fh:
                json.dump({"budget": budget, "A": result["A"]["archive"],
                           "B": result["B"]["archive"],
                           "ledger_A": result["A"]["ledger"],
                           "ledger_B": result["B"]["ledger"]}, fh, sort_keys=True, indent=2)
                fh.write("\n")
    except (ValueError, OSError) as exc:
        print("VERDICT: SKIP   reason=" + str(exc), file=sys.stderr)
        return 3
    print(render(result), end="")
    return int(result["run_a"] == "TOOL_FAULT")


if __name__ == "__main__":
    sys.exit(main())
