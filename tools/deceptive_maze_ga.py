"""Goal-driven GA vs novelty search on a deceptive maze. Stdlib only, seeded.

Maze (y up), 15x15 with border walls:
  start (2,1) bottom-left, goal (2,13) top-left.
  Horizontal wall at y=7 from x=1..12; the only gap is at x=13 (far right).
  Greedy distance pulls straight up into the pocket under the goal (distance 7),
  a dead end. Reaching the goal means first moving AWAY (right) = deceptive.

Parameters were fixed BEFORE any run and are not tuned toward an expected answer.
Also logs per-locus allele entropy (bits, alphabet 4) = the erasure ledger.
"""
import math, random, sys

W = H = 15
START, GOAL = (2, 1), (2, 13)
WALLS = {(x, 0) for x in range(W)} | {(x, H - 1) for x in range(W)} \
      | {(0, y) for y in range(H)} | {(W - 1, y) for y in range(H)} \
      | {(x, 7) for x in range(1, 13)}
MOVES = {0: (0, 1), 1: (0, -1), 2: (1, 0), 3: (-1, 0)}  # N S E W

# fixed parameters
POP, GENS, L, MUT, TOUR, ELITE = 100, 150, 60, 0.05, 3, 2
K_NN, ARCHIVE_ADD = 15, 3
SEEDS = list(range(10))


def run_path(g):
    x, y = START
    reached = False
    for m in g:
        dx, dy = MOVES[m]
        if (x + dx, y + dy) not in WALLS:
            x, y = x + dx, y + dy
        if (x, y) == GOAL:
            reached = True
    return (x, y), reached


def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])


def objective(pos):
    return -dist(pos, GOAL)


def novelty(b, pool):
    ds = sorted(dist(b, p) for p in pool)
    return sum(ds[1:K_NN + 1]) / K_NN  # ds[0] is itself


def locus_entropy(pop):
    tot = 0.0
    for i in range(L):
        c = [0, 0, 0, 0]
        for g in pop:
            c[g[i]] += 1
        tot += -sum((n / len(pop)) * math.log2(n / len(pop)) for n in c if n)
    return tot / L  # mean bits per locus, max 2.0


def evolve(mode, seed):
    rng = random.Random(seed)
    pop = [[rng.randrange(4) for _ in range(L)] for _ in range(POP)]
    archive = []
    ent = []
    for gen in range(GENS):
        res = [run_path(g) for g in pop]
        ent.append(locus_entropy(pop))
        if any(r[1] for r in res):
            return gen, ent, len(archive)
        behav = [r[0] for r in res]
        if mode == "objective":
            score = [objective(b) for b in behav]
        else:
            pool = behav + archive
            score = [novelty(b, pool) for b in behav]
            for i in sorted(range(POP), key=lambda i: -score[i])[:ARCHIVE_ADD]:
                archive.append(behav[i])
        order = sorted(range(POP), key=lambda i: -score[i])
        nxt = [pop[i][:] for i in order[:ELITE]]
        while len(nxt) < POP:
            a = max(rng.sample(range(POP), TOUR), key=lambda i: score[i])
            b = max(rng.sample(range(POP), TOUR), key=lambda i: score[i])
            cut = rng.randrange(1, L)
            child = pop[a][:cut] + pop[b][cut:]
            child = [rng.randrange(4) if rng.random() < MUT else m for m in child]
            nxt.append(child)
        pop = nxt
    return None, ent, len(archive)


def half_gen(ent):
    for i, e in enumerate(ent):
        if e < ent[0] / 2:
            return i
    return None


def main():
    print(f"params POP={POP} GENS={GENS} L={L} MUT={MUT} TOUR={TOUR} ELITE={ELITE} "
          f"K={K_NN} ARCH+={ARCHIVE_ADD} seeds={len(SEEDS)}\n")
    for mode in ("objective", "novelty"):
        hits, gens = 0, []
        print(f"--- {mode} ---")
        for s in SEEDS:
            g, ent, arch = evolve(mode, s)
            hg = half_gen(ent)
            if g is not None:
                hits += 1
                gens.append(g)
            print(f" seed {s}: solved_gen={g}  entropy start={ent[0]:.2f} "
                  f"end={ent[-1]:.2f} bits/locus  half-entropy gen={hg}")
        med = sorted(gens)[len(gens) // 2] if gens else None
        print(f" => solved {hits}/{len(SEEDS)}   median solve gen={med}\n")


if __name__ == "__main__":
    main()


# WO-8 PASSIVE OBSERVATION EXTENSION -- CC0-1.0
# The original source above is preserved byte-for-byte. Bare execution still
# reproduces its original report. Thresholds in the fitness_bin_self_test.py
# header: strict < half initial occupancy; early <= budget//4. The descriptor
# changes observations ONLY, never selection or its RNG draws.


def _ledger_tool():
    import importlib.util
    from pathlib import Path
    path = Path(__file__).with_name("fitness_bin_self_test.py")
    spec = importlib.util.spec_from_file_location("_wo8_ledger", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def path_descriptor(genome, descriptor):
    if descriptor == "final_cell":
        return run_path(genome)[0]
    if descriptor != "visited_cells":
        raise ValueError("descriptor must be final_cell or visited_cells")
    x, y = START
    visited = {(x, y)}
    for move in genome:
        dx, dy = MOVES[move]
        if (x + dx, y + dy) not in WALLS:
            x, y = x + dx, y + dy
        visited.add((x, y))
    return tuple(sorted(visited))


def evolve_ledger(mode, seed, descriptor="final_cell"):
    """Original search plus passive observations; same RNG draws.

    Evaluates populations 0..GENS-1, stops at first ANYTIME goal visit,
    and does not evaluate the last offspring after an unsuccessful last
    iteration. Descriptor control keeps the original final-cell selection.
    """
    if mode not in ("objective", "novelty"):
        raise ValueError("mode must be objective or novelty")
    ledger = _ledger_tool()
    rng = random.Random(seed)
    pop = [[rng.randrange(4) for _ in range(L)] for _ in range(POP)]
    archive, ent, observations, scores = [], [], [], []
    solved = None
    for gen in range(GENS):
        res = [run_path(g) for g in pop]
        ent.append(locus_entropy(pop))
        observations.append([path_descriptor(g, descriptor) for g in pop])
        scores.append(max(objective(r[0]) for r in res))
        if any(r[1] for r in res):
            solved = gen
            break
        behav = [r[0] for r in res]
        if mode == "objective":
            score = [objective(b) for b in behav]
        else:
            pool = behav + archive
            score = [novelty(b, pool) for b in behav]
            for i in sorted(range(POP), key=lambda i: -score[i])[:ARCHIVE_ADD]:
                archive.append(behav[i])
        order = sorted(range(POP), key=lambda i: -score[i])
        nxt = [pop[i][:] for i in order[:ELITE]]
        while len(nxt) < POP:
            a = max(rng.sample(range(POP), TOUR), key=lambda i: score[i])
            b = max(rng.sample(range(POP), TOUR), key=lambda i: score[i])
            cut = rng.randrange(1, L)
            child = pop[a][:cut] + pop[b][cut:]
            child = [rng.randrange(4) if rng.random() < MUT else m for m in child]
            nxt.append(child)
        pop = nxt
    return {"mode": mode, "seed": seed, "solved_gen": solved,
            "genotype_entropy_bits_per_locus": ent,
            "genotype_half_generation": half_gen(ent),
            "behavior": ledger.behavior_ledger(observations, GENS, descriptor),
            "best_endpoint_objective": scores, "archive_size": len(archive),
            "archive_kind": "final-cell descriptors, NOT discarded genomes",
            "fact_kind": "INSTRUMENT"}


# WO-9 SELECTOR-SWAP EXTENSION -- CC0-1.0, co-authored 2026-10-14
# BEFORE RUN: F Euclidean endpoints; V Jaccard visited sets; P absolute
# closest-approach scalar differences (the explicit OBJ-V compressed input).
# Strict half-distance threshold 0.50 of gen 0; sensitivity 0.40 and 0.60.
# Params/seeds unchanged. P2: report raw V AND declared path-derived P;
# never choose a new descriptor or threshold after observing the result.
DISTANCE_THRESHOLD = 0.50
DISTANCE_SENSITIVITY = (0.40, 0.50, 0.60)
SELECTOR_CONDITIONS = ("OBJ-F", "NOV-F", "OBJ-V", "NOV-V")


def _bits(value):
    method = getattr(int, "bit_count", None)
    return method(value) if method is not None else bin(value).count("1")


def jaccard_distance(a, b):
    """Set Jaccard distance; empty/empty is declared identical (zero).

    Internal masks encode exactly the same cell sets, not an approximation.
    """
    if isinstance(a, int) and isinstance(b, int):
        union = _bits(a | b)
        return 1 - _bits(a & b) / union if union else 0.0
    a, b = set(a), set(b)
    union = len(a | b)
    return 1 - len(a & b) / union if union else 0.0


def mean_pairwise(values, space):
    """All unordered population-slot pairs, including duplicate zero pairs."""
    from collections import Counter
    if len(values) < 2:
        return None
    if space == "F":
        counts = Counter(tuple(v) for v in values)
        distance = dist
    elif space == "V":
        counts = Counter(v if isinstance(v, int) else frozenset(v) for v in values)
        distance = jaccard_distance
    elif space == "P":
        counts = Counter(values)
        distance = lambda a, b: abs(a - b)
    else:
        raise ValueError("space must be F, V or P")
    items = list(counts.items())
    total = sum(n * m * distance(a, b)
                for i, (a, n) in enumerate(items) for b, m in items[i + 1:])
    return total / (len(values) * (len(values) - 1) / 2)


def half_distance_gen(series, fraction=DISTANCE_THRESHOLD):
    if not 0 < fraction < 1:
        raise ValueError("fraction must be strictly between zero and one")
    if not series or series[0] is None or series[0] == 0:
        return None  # no baseline to halve; report initial value alongside
    return next((i for i, value in enumerate(series)
                 if value is not None and value < fraction * series[0]), None)


def _path_observation(genome):
    x, y = START
    mask = 1 << (y * W + x)
    closest = dist(START, GOAL)
    reached = False
    for move in genome:
        dx, dy = MOVES[move]
        if (x + dx, y + dy) not in WALLS:
            x, y = x + dx, y + dy
        mask |= 1 << (y * W + x)
        closest = min(closest, dist((x, y), GOAL))
        if (x, y) == GOAL:
            reached = True
    return (x, y), mask, closest, reached


def _novelty_visited(value, pool, cache):
    distances = []
    for other in pool:
        key = (value, other) if value <= other else (other, value)
        if key not in cache:
            cache[key] = jaccard_distance(value, other)
        distances.append(cache[key])
    distances.sort()
    return sum(distances[1:K_NN + 1]) / K_NN


def selector_run(condition, seed):
    """Four fixed selectors, passive F/V/P measurement, original search budget.

    OBJ-V input is the whole path compressed to closest Euclidean approach,
    NOT its endpoint. NOV-V scores visited-set Jaccard novelty. F modes retain
    the exact original objective/novelty helpers and stable tie ordering.
    """
    if condition not in SELECTOR_CONDITIONS:
        raise ValueError("unknown selector condition")
    rng = random.Random(seed)
    pop = [[rng.randrange(4) for _ in range(L)] for _ in range(POP)]
    archive, rows = [], []
    solved = None
    for generation in range(GENS):
        observations = [_path_observation(g) for g in pop]
        endpoints = [r[0] for r in observations]
        visited = [r[1] for r in observations]
        approach = [r[2] for r in observations]
        rows.append({"generation": generation,
                     "F_distance": mean_pairwise(endpoints, "F"),
                     "V_distance": mean_pairwise(visited, "V"),
                     "P_distance": mean_pairwise(approach, "P"),
                     "F_distinct": len(set(endpoints)),
                     "V_distinct": len(set(visited)),
                     "P_distinct": len(set(approach)),
                     "genotype_entropy_bits_per_locus": locus_entropy(pop)})
        if any(r[3] for r in observations):
            solved = generation
            break
        if condition == "OBJ-F":
            score = [objective(v) for v in endpoints]
        elif condition == "NOV-F":
            score = [novelty(v, endpoints + archive) for v in endpoints]
        elif condition == "OBJ-V":
            score = [-v for v in approach]
        else:
            cache = {}
            pool = visited + archive
            score = [_novelty_visited(v, pool, cache) for v in visited]
        if condition.startswith("NOV"):
            descriptors = endpoints if condition == "NOV-F" else visited
            for i in sorted(range(POP), key=lambda i: -score[i])[:ARCHIVE_ADD]:
                archive.append(descriptors[i])
        order = sorted(range(POP), key=lambda i: -score[i])
        nxt = [pop[i][:] for i in order[:ELITE]]
        while len(nxt) < POP:
            a = max(rng.sample(range(POP), TOUR), key=lambda i: score[i])
            b = max(rng.sample(range(POP), TOUR), key=lambda i: score[i])
            cut = rng.randrange(1, L)
            child = pop[a][:cut] + pop[b][cut:]
            child = [rng.randrange(4) if rng.random() < MUT else m for m in child]
            nxt.append(child)
        pop = nxt
    half = {str(fraction): {space: half_distance_gen(
        [r[space + "_distance"] for r in rows], fraction) for space in ("F", "V", "P")}
            for fraction in DISTANCE_SENSITIVITY}
    return {"condition": condition, "seed": seed, "solved_gen": solved,
            "rows": rows, "half": half, "archive_size": len(archive),
            "fact_kind": "INSTRUMENT", "last_observed_generation": len(rows) - 1}
