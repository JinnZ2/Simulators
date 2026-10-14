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
