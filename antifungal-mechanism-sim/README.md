# antifungal-mechanism-sim

Interactive CLI for exploring antifungal drug combinations by
**genetic-style crossover** of multiple-choice interaction targets.
Seven predefined interaction types, each scored on efficacy / toxicity
/ resistance risk; the user assembles named "mechanisms" from subsets of
those seven, then crosses any two to discover a new combination whose
gene pool is the union of both parents.

CC0. Python stdlib only.

## What it is

A design-space explorer, not an audit tool. The seven interaction codes
are pharmacological categories:

| code | target |
|---|---|
| `CW` | Inhibit cell wall synthesis (β-glucan synthase) |
| `EG` | Inhibit ergosterol synthesis (azole target) |
| `MD` | Disrupt fungal membrane (polyene) |
| `PS` | Inhibit protein synthesis (EF-Tu) |
| `NA` | Inhibit nucleic acid synthesis (5-FC) |
| `SS` | Stress response sabotage (Hsp90) |
| `QP` | Quorum sensing / biofilm disruption |

A `Mechanism` is a set of these codes. Its `evaluate()` returns
`(efficacy, toxicity, resistance, score)` where `score = efficacy -
toxicity - resistance`. `crossover(a, b)` returns a new Mechanism
whose interaction set is a random subset (size ≥ 1) of `a ∪ b`.

## Run it

```
python3 antifungal_mechanism_sim.py
```

Interactive menu:

1. Show the seven interactions and their scores.
2. Create a mechanism from codes (`CW MD` etc.).
3. View library.
4. Evaluate any stored mechanism.
5. **Cross two mechanisms** — the core discovery step.
6. Quit.

## Run the tests

```
python3 -m unittest discover tests
```

15 tests. Cover the deterministic surface:

- `INTERACTIONS` shape (seven codes, four fields each, non-negative int
  scores).
- `Mechanism.evaluate()` math (empty → all zeros; single/multi-code sums
  correctly; duplicates deduplicate through the set).
- `Mechanism.__str__` shape (name + score labels present).
- `crossover()` invariants under seeded RNG:
  offspring only uses parent genes, size bounded by |A ∪ B|, ≥ 1 when
  the union is non-empty, deterministic under a fixed seed, offspring
  name preserved.

The interactive `main()` menu is not covered by these tests — it reads
stdin.

## Note on scoring

The three-component score is a design-exploration heuristic, not a
pharmacological prediction. The score is a decision aid for combinations
you want to look at more closely — it does not, by itself, say anything
about clinical viability.

## License

CC0 / public domain. See the repo root `LICENSE`.
