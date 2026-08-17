# AUDIT_NOTES — photoperiod-claim-harness

Everything below is added analysis. The delivered files are
[`README.md`](README.md) and
[`photoperiod_claim_harness.py`](photoperiod_claim_harness.py), both
verbatim. Added here: [`harness_audit.py`](harness_audit.py) and
[`CLAIM_TABLE.md`](CLAIM_TABLE.md) (`PCH_001..007`).

Every number the delivered README states was checked and holds — 75 grid
cells, 58 with the signature, ~4.9× spread, and the five claim verdicts.
One word does not: `PCH_007`.

---

Four inconsistencies in a published closed-loop-LLM greenhouse result,
encoded as runnable falsifiable sims, with a claim table, a mechanism-edit
protocol, a bench protocol, and a provenance log.

Delivered **verbatim** as
[`photoperiod_claim_harness.py`](photoperiod_claim_harness.py) — single file,
stdlib only, phone-buildable. Its own framing:

> A marker for a sensed shape that needs more exploration — not a thesis, not
> a refutation of any paper. Correct reader response: test whether it fits,
> extend it, or report where it breaks.

```bash
python3 photoperiod_claim_harness.py claims      # the claim table
python3 photoperiod_claim_harness.py run-all     # run every claim + hypothesis
python3 photoperiod_claim_harness.py run C2      # one claim  (NOT `run S2`)
python3 photoperiod_claim_harness.py sweep S2    # duty + dark-interval curves
python3 photoperiod_claim_harness.py protocol    # bench measurements
python3 photoperiod_claim_harness.py pending     # named, unrun mechanism edits
python3 photoperiod_claim_harness.py log         # provenance chain

python3 harness_audit.py                         # added: grades the harness
```

Whole run is under half a second. `pch_log.jsonl` is runtime state and is
gitignored.

## What it runs

| sim | what | claims |
| --- | --- | --- |
| `S1` | mass / denominator swap, as a 75-cell regime map | `C1` |
| `S2` | Pchlide pool charging at equal photon dose, + dark-interval crossover | `C2`, `C3` |
| `S3` | reflectance index artifact, closed loop | `C4` |
| `S4` | channel count vs common-mode bias | `C5` |

Shipped run: **four of five REFUTED**, including two the file's own framing
would have preferred to support.

## What the audit found

`harness_audit.py` imports the delivered file and changes nothing. Seven
results in [`CLAIM_TABLE.md`](CLAIM_TABLE.md) (`PCH_001..007`).

**`PCH_007` — the README's numbers hold; one word does not.** `C3`'s
dark-interval curve is negative throughout but not monotone, and every arm
that breaks the ordering is one whose 144 h run ends mid-cycle.
`_pchlide_run` reads `Chl` at the last integration step, so those arms are
sampled at a different phase. A cycle average makes the curve monotone. It
changes no verdict — `C3` tests for a sign flip and there is none either way
— so what the artifact costs is the ability to read the curve's *shape* as
mechanism, which is what `C3`'s reads line offers. The prose is ahead of the
instrument, not behind it.

**The one that matters — `C1` passes when the sim produces nothing.**

```
as shipped            cells=58  spread=4.8828  ->  REFUTED
no shade-avoidance    cells=0   spread=0.0000  ->  SUPPORTED
    signature_kWh_per_dry_min = None
    signature_kWh_per_dry_max = None
```

`signature_spread` is `max/min` over the qualifying cells and `0.0` when
there are none, which passes `< 1.5`. The `reads` line for TRUE is *"the
reported metrics are diagnostic of real efficiency"* — returned from a run
that reproduced the signature zero times, with `None` printed for min and max
directly above. A pass an empty result set returns is not a pass.

The harness already has the branch to route it to: `run_claim()` emits
`UNDECIDED:` when a predicate raises.

**`C1`'s grid says something better than its reads line.** The signature
appears in 58 cells spanning a 4.9× range of true energy-per-dry-gram, and
**every one is below 1.0**. Non-diagnostic of *magnitude*, diagnostic of
*sign*: the reported package does license "cheaper per dry gram" on this
mechanism set — it does not license any particular number, and 68% is a
number. That survives the objection that the sim was built to find nothing.

**The edit protocol screens 2 of 4 fields**, and the two it skips (`basis`,
`prediction`) are the ones that ask for justification. **`settle()`** writes
`prediction_held: None` and nothing fills it, and the before/after file
hashes are equal because nothing edited the file — so a registered, settled,
never-performed edit is indistinguishable in the log from a real one.

**The header's usage example fails**: `run S2` passes a sim id to a command
that looks up claim ids.

## What holds

`C2` states a literature premise, states a hypothesis that could survive it,
refutes its own hypothesis, explains the mechanism (the FLU clamp acts on
pool *size*, so a full pool slows synthesis and draining it continuously
maximises flux), and then **names the next candidate and files it unrun**
instead of retuning toward it.

`PENDING_EDITS` has no equivalent elsewhere in this repo: three mechanisms,
each with a basis and a prediction registered before any run, all `UNRUN`.

Provenance is separated at the type level and `BENCH` is declared with no
code path that can emit it — the honest state, said out loud, with a bench
protocol attached for producing one.

## One more, minor

`hypothesis_block()` stamps the wall clock into its header, one line above
the file hash it prints for provenance. Two runs of the same file produce two
different documents. A run id derived from the hash and the parameters would
carry the same information and diff cleanly. See [`samples/README.md`](samples/README.md).

## Not audited here

Anything about wheat, chlorophyll, or the published result. This folder has
no bench data and neither does the harness; its own hypothesis block says so.

CC0.
