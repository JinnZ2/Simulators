# divergence-playground

**The object under test is not the cosmology. It's the spread across readers.**

Given a fork point (a place in a piece of work where the raw data
admits more than one honest reading), multiple readers commit their
readings independently under a hash-locked seal, and only then does
the ensemble get revealed. Anti-anchoring by construction. What comes
out is a *structured* spread — not a variance — plus a run queue of
collapse conditions the readers already agree on.

CC0. Stdlib only. Phone-buildable.

## The loop

1. **Serve a fork point** (from a `FORKS.jsonl`) with the raw data —
   **not** the prior readings.
2. **Reader commits** a `Reading`: verdict, mechanism (as a DAG),
   collapse condition (the experiment that would resolve the fork),
   confidence.
3. **The commit is sealed** (SHA-256 hash + XOR-obfuscated payload)
   before any other reader is shown anything.
4. **Only when everyone has committed** is `reveal()` called; the
   playground unseals every payload and verifies every hash.
5. **The ensemble is logged and scored.**

The seal in step 3 is load-bearing. Without it you get anchoring, and
the ensemble collapses into the first reading posted. That's the
single failure mode that kills the whole thing.

## Files

```
divergence-playground/
  fork.py            Fork dataclass + FORKS.jsonl I/O
  reading.py         Reading dataclass (verdict, mechanism, collapse, confidence)
  seal.py            commit / reveal — the anti-anchoring seal
  spread.py          3-axis spread metric + agree-by-accident detector
  coincidence.py     C1-C4 tests (structured elicitation)
  null_ensemble.py   shuffle / resample / permutation nulls
  samples/           end-to-end worked example
```

## The three axes of spread

Readings are structured, not scalar. Compare on three axes
independently, each in `[0, 1]`:

| axis | test | strength |
|-----:|------|----------|
| **1. Verdict**   | do they name the same branch of the fork? | categorical; cheap; **weakest signal** |
| **2. Mechanism** | same causal chain? Jaccard on the DAG-edge set. Two readings using different notation for the same chain compare equal. | structural |
| **3. Collapse**  | would the same experiment resolve them? | operational; **strong axis** |

The interesting cell: **same verdict, different collapse**. Two
readers agree by accident — they reach the same conclusion via
different routes. Variance would never catch this;
`spread.agreement_accident()` flags it.

## Coincidence tests (C1–C4)

Run in order. C1 collapses the most spurious "convergences."

| test | catches | example |
|------|---------|---------|
| **C1** SAME OBJECT, TWO SHADOWS | quantities related by a deterministic map | `rs_ratio = 0.9886` and `E_ede_frac = 0.0114` are one number (`A = 1 − B`), not two |
| **C2** TRIALS FACTOR | look-elsewhere effect | `p_eff = 1 − (1−p)^N` — state N *before* claiming surprise |
| **C3** ELASTIC TARGET | post-hoc tolerance windows | fix the match window *before* looking; log the timestamp |
| **C4** REAL COMMON CAUSE | the only kind worth having | state an out-of-sample prediction it makes; hold to it |

C1–C3 are **structured elicitation** — the tool cannot infer the
maps, the trial counts, or the tolerances. It refuses to certify a
coincidence claim without them. C4 requires pre-registration and a
falsifiable prediction.

## Null ensemble

The only rigorous version. `null_ensemble.null_hits()` runs your
search rule on synthetic nulls (shuffle labels, IID resample, or
group permutation) and reports the empirical p — trials factor
included by construction because you ran the search on the null.

## Worked example

[`samples/worked_example.sample.txt`](samples/worked_example.sample.txt)
runs the full loop on **FK-2** (the generative CPL-recovery fork
from the `energy/` audit). Three readers commit blind; verdict
spread 0.33, mechanism spread 1.00, **collapse spread 0.33 (strong
axis)**. The verdict-cluster (`reader_B + reader_C`) does **not**
match the collapse-cluster (`reader_A + reader_B`) — the axes
measure different things. The run queue auto-ranks the collapse
condition two of three readers converged on.

The same run then applies C1 to the `rs_ratio / E_ede_frac`
"convergence" this audit already flagged — residual 0.0 under
`A = 1 − B`, so it collapses to one hit — plus C2 (p=0.05 becomes
p=0.99 under N=100 trials) and a shuffle-null on a basis-echo
scenario.

## FORKS.jsonl

Any project can carry its own `FORKS.jsonl`. The energy/ audit
harvested seven:
[`energy/FORKS.jsonl`](../energy/FORKS.jsonl). Status snapshot:

```
FK-1  θ* engine split           RESOLVED   (DP-13)
FK-2  generative CPL recovery   RESOLVED   (F2)
FK-3  H0 orthogonality           PARTIAL    (DP-14 option, OB-8 rerun)
FK-4  fs8 ≈ 8× ΛCDM              OPEN
FK-5  α wall classification      OPEN
FK-6  certificate validity r̂    RESOLVED   (DP-17)
FK-7  D as distance              STAKED     (DP-15 caveat)
```

## What it does not do

- **No LLM calls.** Readers commit through Python API or CLI; the
  playground is what shows up when the humans and AIs have already
  written their answers.
- **No inference of coincidence.** C1–C4 refuse to certify without
  pre-declared maps, trial counts, and tolerances.
- **No cryptographic seal.** The XOR obfuscation in `seal.py`
  defends against accidental peeking, not against a determined
  attacker. For adversarial multi-agent settings, swap the XOR
  layer for real crypto; the commit/reveal API stays the same.
- **No storage of raw model output.** Only structured `Reading`s.
  Prose goes in the `notes` field.

## Storage layout (created at runtime)

| file | contents | provenance |
|------|----------|------------|
| `SEALED.jsonl`   | one record per sealed commit: fork id, reader id, timestamp, sha256, XOR-obfuscated payload | append-only |
| `REVEALED.jsonl` | one record per reveal: same fields + decoded reading | append-only |
| `.nonces.json`   | per-fork XOR nonces used by seal | opaque |

Both `SEALED.jsonl` and `REVEALED.jsonl` are runtime state; add them
to `.gitignore` wherever the playground is being run so private
readings do not leave the machine.

## License

CC0 1.0 Universal. Public domain.
