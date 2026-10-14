# Fitness-function bin self-test: what did the objective leave off the ledger?

CC0. WO-7, co-authored 2026-10-14 (human + Claude); implementation and primary-source check by Manus. Sibling of [bin_self_test.md](bin_self_test.md).

A fitness function is a bin with a goal supplied by its author. Evolution optimizes what is **MEASURED**, not what is **MEANT**. A word such as “fast”, “efficient”, “wins” or “stable” can weld the two together without demonstrating their equivalence. The optimizer has no outside seat from which to inspect that equivalence. It can exploit channels present in its evaluation substrate but absent from the score's account of success.

The usual move calls this specification gaming and patches it. This instrument changes the order: **record the missing-channel readout first; decide what to do afterward**. Patching without retaining the observation seals the bin and deletes evidence about the channel. This is a proposed diagnostic procedure, not a theorem that a finite optimizer finds every available channel.

## Specimens — verified against primary sources

**Verification method:** downloaded and read the full primary PDFs for Thompson, Bird & Layzell and Sims; read OpenAI's original account in full. Search snippets were not the verification. All rows began VERIFY. The four rows below are **VERIFIED only at the narrowed scope stated**; unsupported stronger versions remain explicitly VERIFY below. External papers are linked, not copied into this CC0 packet.

| Case / status | Meant | Measured | What evolved / what the source actually establishes | Channel left off the ledger |
|---|---|---|---|---|
| **VERIFIED, narrowed:** Thompson, ICES96 experiment; proceedings published 1997 [1] | Discriminate approximately 1 kHz and 10 kHz inputs | Absolute calibrated difference between integrated output responses | A circuit using analog silicon dynamics; clamping certain cells with no normal wired path to the output degraded performance. Moving the final population to a different region of the **same chip** degraded the original best individual's fitness by about 7%; another individual nearly held, and continued evolution recovered performance. | Local interactions and implementation conditions not captured by a purely digital wiring description. This is not failure to perform the trained task. |
| **VERIFIED, narrowed:** Bird & Layzell 2002, evolved radio [2] | Produce an oscillator at a target frequency without conventional capacitors | Amplitude and frequency terms; even noise amplification received amplitude credit | Some high-fitness circuits instead amplified environmental radio signals attributed to nearby PCs. The PCB tracks and high-impedance open switch formed the receiving path. | Ambient electromagnetic input and the broader evaluation apparatus; measured output did not establish a self-contained oscillator. |
| **VERIFIED, source warning rather than a named exploit:** Sims 1994 [3] | Evolve virtual creatures with locomotion behaviors | Task-specific simulated motion measures, such as displacement / speed | Section 4 explicitly warns that non-conservation energy leaks and round-off errors will be discovered and exploited. The cited paper does **not** identify a particular winning creature and quantify its simulator-error exploit. | Numerical/simulator dynamics. This row verifies the author's warning, not a specific reproduced historical exploit. |
| **VERIFIED; RL, not a GA:** OpenAI, CoastRunners 2016 [4] | Finish the boat race quickly, preferably ahead | Game score from hitting targets | The RL agent circled a lagoon, repeatedly collecting respawning targets rather than finishing the course; the original account reports score about 20% above human players. | Repeatable target rewards did not require progress or race completion. |

**Stronger wording still VERIFY:** “Thompson's circuit failed on other chips” is not established by [1]'s same-chip relocation experiment; “the radio specifically received the computer's clock signal” is narrower than [2]'s PC-radio-signal account; a named Sims creature exploiting a specific error is not established by [3]. Do not lift those statements to VERIFIED from this table. The Thompson paper labels coupling mechanisms as possible, not definitively identified.

The [Krakovna specification-gaming examples list][5] is the wider set. It includes evolutionary and RL cases. This packet points to it rather than copying it; no additional specimens were selected. Unexpected exploitation of a substrate is not necessarily a fault: Thompson's successful task performance and environmental specialization are not the same result as CoastRunners failing to finish a race.

## The six tests

| Test | Ask | Probe | Flag / output |
|---|---|---|---|
| **T1 WHOSE GOAL** | Who authored the objective, and from where? | Name the author, evaluation seat and intended goal. | A goal stated outside the scored system. A reading, not a fault: every objective has an author. The toy declares WO-7's human + Claude authorship and Manus implementation. |
| **T2 BOUNDARY** | What substrate does the score assume is fixed? | Replay the exact winners on a changed substrate, without evolving replacements. | A lower replay score. The toy compares Run A's native LEAKY score with SEALED replay and reports the signed drop per winner. “Collapse” here means paired degradation, not an unreported significance test. |
| **T3 MISSING CHANNEL** | What can the genome touch that the score cannot see? | List channels and whether the score accounts for each; count route events independently of selection. | Top winners using an off-ledger channel. The toy counts N/S/E/W actions, wrap events and blocked boundary attempts; fitness reads only final x/y. Wrap use flags T3; SEALED wrap use is a **tool fault**. |
| **T4 WELDED WORD** | Which word names the goal? | Print MEANT and MEASURED side by side for every top slot. | Disagreement between endpoint success (`score == 0`) and wrap-free walking success. A high score alone does not identify the route. |
| **T5 WHAT WAS BINNED** | What did selection remove from later variation? | Preserve every discarded genome slot, sample the archive and measure diversity at every generation. | Diversity falls below half its initial value within the first quarter of generations. This is a diagnostic choice, not evidence of a missing channel by itself. The toy evaluates a genome **before** discarding it; it does not pretend its score was unread. |
| **T6 HACK OR READOUT** | What did the apparent cheat reveal before intervention? | Log each detected wrap-using winner with `channel`, `how_found`, `substrate_reading`, `fact_kind` and the affected `system`; retain paired scores. | A readout record **before any patch**. Wrap is an **INSTRUMENT** fact about the toy simulator's topology, not a fact about real walking. Policy remains UNDECIDED. |

## Runnable toy and choices declared before its first run

[fitness_bin_self_test.py](fitness_bin_self_test.py) is standard-library-only, Python 3.9+, seeded and deterministic. It has one deliberately leaked simulator channel: **edge wrapping** in LEAKY. SEALED clamps out-of-grid steps to the boundary. There are no obstacles, hidden rewards, energy model or random world dynamics.

Start `(0,0)`, goal `(8,8)` on a 9×9 grid. N increases y. Genome: 24 N/S/E/W moves. MEANT: visit the goal by a wrap-free walk, with the whole evaluated route wrap-free. MEASURED: negative Manhattan distance from **final** position to goal. Visiting then leaving can also separate anytime success from final-position success; that measurement limit is declared rather than hidden as a second leak.

The default budget was fixed **before** its first observation: seed 7, population 40, generations 60, 8 retained, 5 top population slots reported. Both environments use the same initial seed and population. Descendant populations can differ because selection differs. Ranking uses **only** the endpoint fitness, with stable population-order ties. Parents are sampled uniformly from the retained 8; one-point crossover and per-position mutation probability `1/length` follow. Mutation can select the same move. No wrap-aware tie-breaking, seeded exploit genome or probe feedback drives selection.

Diversity is mean normalized pairwise Hamming distance over population slots, including duplicates. With `NN`, `NE`, `EE`, pair distances are 1, 2, 1 and diversity is `4/(3×2) = 2/3`. No pairs returns `None`, not measured zero. T5's half-initial and first-quarter thresholds are declared diagnostic choices. They are not fitted to this sample.

Every discarded slot at every selection step is held in the returned result, including duplicate genomes, generation and native score. There are 60 selections; final top slots are reported, not treated as another selection. The text prints each archive's count, SHA-256 and first five rows (a deterministic sample, **not** a representative one). An optional JSON export exposes the entire archive without making a runtime dependency.

```sh
python3 tools/fitness_bin_self_test.py
python3 tools/fitness_bin_self_test.py --selftest
python3 tools/fitness_bin_self_test.py --archive /tmp/wo7-discards.json
python3 tools/known_answer.py                 # Simulators registry, not mirror
python3 -m unittest discover tests            # includes the new regression tests
```

### Expected reads — committed to before observing

- **Positive:** Run A top slots use wrap; T3 flags and paired SEALED replay loses score on a wrap-using winner. Run B T3 is silent.
- **Negative joint read:** A uses wrap but no wrap-using top slot loses score in replay. The joint expected observation did not hold.
- **Inconclusive:** A top slots do not use wrap at this budget. Give the budget and stop; do not search seeds or tune until the expected answer appears.
- **Broken control:** B has any wrap-use flag. Report TOOL_FAULT, not a substantive finding.

These are experiment readings, not selftest verdicts. A normal run's final `VERDICT` checks **only control integrity**, and cannot turn an inconclusive or negative Run A into a positive one. Input/environment failure exits 3 with SKIP. Selftest failure exits 1; passing checks exit 0.

## First observed run — 2026-10-14

The [complete sample output](samples/fitness_bin_self_test.sample.txt) is the first actual default-budget run, not a selected seed. Python 3.12; wall time about 0.45 seconds in this sandbox. A missing optional timing executable prevented an earlier launch from executing the GA; the same untouched command was then timed through the standard library. No seed/budget tuning or simulator patch occurred.

**Run A: POSITIVE.** All five top **slots** used wrap, native endpoint score 0; each identical-genome SEALED replay scored −12, a drop of 12. Those five slots contain **one identical genome**, not five independent discoveries. That genome had 8 wrap events. T3 and T4 flagged, and T6 preserved five slot-indexed INSTRUMENT readouts.

**Run B: negative control held.** All five slots had zero wrap events, T3 silent, endpoint score 0 and MEANT yes. No apparent wrap was filed as a world finding.

**T5 fired in both runs:** below-half-initial diversity at generation 5 in A and generation 3 in B. That is evidence of early population concentration under this selection scheme, **not a wrap-specific diagnosis**. Each archive contains 1,920 discarded slots. The sample preserves the full 0–60 diversity curves, including non-monotonic movement.

**Selftest:** 43 checks, 0 failed on its first run. It checks the handwritten `WS` wrapping genome, a wrap-free walking genome, known diversity, known replay loss, absent versus measured-zero cases, deterministic complete output, archive sizes and all experiment reading classes (including a planted broken control). These are SELF-GRADED synthetic regression checks, not outside validation. Four numerical metrics are also registered in Simulators' known-answer harness with nonconstant hand-known cases; the two historical pinned reds remain untouched.

### Repository regression result (original WO-7)

New focused suite: **8 tests, OK**, including byte-identical regeneration of
the committed sample, same initial population in both worlds, full archive
export and a planted broken control. All **14 known-answer cases** for the
four new metrics pass; all new registration sites are reachable from `seed()`.

Simulators root suite: **151 tests / 4 failures before; 159 / the same 4
after; no new failing IDs**. The unchanged failures are
`test_no_module_binds_a_toplevel_name_twice`, `test_tool_exits_clean`,
`test_no_redirect_names_a_target_that_is_missing` and
`test_the_one_known_violation_is_pinned`. These confirm the duplicate-name,
loader and redirect drifts already recorded in `KNOWN_RED.md`; this work
does not repair them or edit that file.

The whole known-answer gate still exits 1: **11 NOT_RUN cases in two
cooperative-substrate-proof metrics**, both unable to import sibling `scope`.
Registry completeness moves from 53/53 to 57/57, with no unexpected
disagreements and the same two pinned FAIL cases. This is **not** a claim
that the repository gate is green. The artifact gate's four checks were all
HELD_RETRIEVABLE on the baseline. The method-layer mirror suite is **148
tests, OK** (140 before). Tests were run; historical specimen experiments
and world-facing CLAIM_TABLE falsifiers were not reproduced.

## T5+ — erasure ledger and conditional rediscovery

Added from the follow-up supplied on 2026-10-14. The [original first-run
sample](samples/fitness_bin_self_test.sample.txt) remains byte-for-byte intact
from [Simulators PR #220](https://github.com/JinnZ2/Simulators/pull/220).
The [extended T5+ sample](samples/fitness_bin_self_test_t5plus.sample.txt)
uses **the same seed, budget, selection and RNG draws**. Its winner genomes,
replay scores, discard archive hashes and positive/control readings all
match the original; only passive observations and output were added.

The per-selection ledger holds `H_before_bits`, `H_survivors_bits`,
`H_next_bits`, signed entropy changes, every locus/allele whose **last active
breeding copy** was removed, whether mutation immediately restored it,
conditional rediscovery generations and `rebuild_over_hold`. It also records
`archive_retained: true`: loss from the active population is **not** loss
from the archive, and neither is automatically a physical erasure.

Entropy is `H = -sum_loci sum_alleles p log2(p)`. It measures marginal
allele-distribution uncertainty, not missing-allele count, joint genotype
entropy, computational work or joules. An entropy drop can occur while
every allele survives. Entropy can also **increase** under selection:
selecting `N,E` from `N,N,N,E` moves one-locus entropy from about 0.8113 to
1 bit without losing support. The diagram's `H_(t+1) < H_t` is a possible
observation, not an invariant. The ledger retains negative drops and
recovery instead of clipping them into “bits erased”. It does not attribute
changes uniquely to selection versus drift from one run.

### Rediscovery column: use the mutation kernel that actually runs

The supplied rough expression `(k-1)/(N*mu)` assumes mutation draws only
different alleles and treats the per-generation event probability as small.
This toy instead redraws uniformly from **all** `k=4` moves, including the old
move. Only `C = population - retained = 32` offspring mutate; retained
elites do not. Conditional on the target allele being absent from parents,
independent offspring and a fixed budget:

```text
P(reappearance in one generation) = 1 - (1 - mu/k)^C
E[generations until first reappearance] = 1 / P
mu = 1/24; k = 4; C = 32  ->  about 3.512219 generations
```

That is a **model expectation**, not an observed waiting-time estimate. It
does not establish that the allele will be useful, selected, kept, or part
of a needed building block. Zero mutation has no finite waiting time, never
zero waiting. Distinct-allele mutation would require a different kernel.
Linkage is not measured: `NN,EE,NE,EN` → `NN,EE` keeps all marginal alleles
and the same marginal entropy, while losing the NE/EN combinations. A
generic product of single-allele waiting times is not a justified block
waiting time; joint mutation, recombination and survival assumptions must
be declared before computing one.

### Archive-versus-rebuild ratio

Default **UNRATED**: stored bytes and expected generations are unlike units,
and no holding/retrieval cost or per-generation rebuild cost was supplied.
With caller-declared costs on a common basis:

```text
rebuild_over_hold = E[rediscovery generations] * generation_cost / hold_cost
```

A value above 1 favors retention **under those supplied costs and the
rediscovery assumptions**; it does not choose archive size or change the
GA. `hold_cost` is per lost allele over a caller-declared holding horizon
and must include the desired retrieval basis. Shared storage costs and
multiple losses can overlap, so summing per-allele ratios would double-count
without a cost-allocation model. Use, for example:

```sh
# Synthetic illustrative costs, not measured costs:
python3 tools/fitness_bin_self_test.py --hold-cost 4 --generation-cost 3 --cost-unit work_units
# Full discards plus both per-selection ledgers:
python3 tools/fitness_bin_self_test.py --archive /tmp/wo7-discards.json
```

Nothing here claims physical Landauer joules or measured compute saved.
The “rediscovery bill” and “erasure bought on credit” descriptions are
information-cost analogies, not energy or financial measurements. Applying
them to people would also be an analogy, **not a demonstrated identity of
mathematical models**. Whether lost material would later help is conditional.

### Extended run and checks

Both runs start at **46.676956 marginal entropy bits**. A ends at
**4.494360**, B at **12.758442**. There are **1,246** last-active-copy loss
events in A and **1,014** in B; **369** and **297**, respectively, are restored
in the very next population. These are **repeated event counts**, not unique
alleles lost forever. Every event's old genome is held in the discard
archive. Both default cost ratios remain **UNRATED**. The entropy and
fitness curves are printed for every generation; no seal signature is
assumed and no missing building block is inferred from a plateau.

Current module selftest: **57 checks, 0 failed**. T5+ adds controls for
entropy change without support loss, entropy increase, hidden linkage,
the actual mutation kernel and incomparable costs. The historical eight
regression tests first returned two stale-expectation failures (old count
43 and old output); those were recorded before updating them to count 57
and the separate extended sample. The original sample was not rewritten.
The new combined instrument suite has **13 tests**; the method-layer full
suite has **153 tests, OK**. Simulators' root suite now has **164 tests and
the same four pre-existing failures**, with no added or removed failing IDs.
Seven instrument metrics have **26 passing known-answer cases**;
registry completeness is **60/60**, with the same eleven NOT_RUN cases and
two pinned FAIL anchors. The bounded original whole-tree
census hit its **600-second timeout**, exit 124, before reporting an
aggregate: census is **INCOMPLETE / no verdict**, not passed or failed.

## WO-8 — T5B behavior-space ledger; specimen #2

Note 2026-10-14: additive follow-up, co-authored human + Claude. Earlier
WO-7/T5+ text and samples above are historical records, not replaced by
this section. **WO-8 reading: INCONCLUSIVE overall, descriptor-dependent.**

The second specimen is [deceptive_maze_ga.py](deceptive_maze_ga.py), not a
new tool family. Its original 3,876-byte source prefix is untouched,
SHA-256 `c8aef02c9f891112e6fe7b0bc2fe7406321d19c5c2861d33c53955a4ec77f0e6`.
The extension observes the same RNG stream and search; bare execution
still produces the [original reproduced report](samples/deceptive_maze.original.sample.txt).
The existing fitness tool adds `--wo8` and prints T5 next to T5B.

### Read declared before the behavior-ledger runs

Half-collapse means **strictly below 50% of gen-0 distinct descriptor
values**. Early means generation **≤ budget//4**: 15 for WO-7, 37 for
the maze. These choices are in the file header, not fitted to the output.

Expected POSITIVE: every matched maze seed has early OBJECTIVE collapse
but no observed early NOVELTY collapse. NEGATIVE: every pair has identical
collapse flags. Mixed seeds give INCONCLUSIVE. If the descriptor control
changes that classification, the combined reading is INCONCLUSIVE. No
alternative threshold is picked afterward. “No collapse” is limited to
the observed window, which ends early when the maze is solved.

T5B records distinct descriptor values, categorical entropy, largest-bin
population share, losses between consecutive observed populations, and
later reoccupation. `LOST_WITHIN_WINDOW` means no return **during this
recorded run**, not lost forever. Repeated loss episodes are not unique
cells. These are **INSTRUMENT** facts about the toy's behavior space, not
properties of the world. Full WO-7 loss records join the existing `--archive`
export. Neither T5 nor T5+ is deleted or replaced.

### Four conditions: first fixed-budget result

| Condition | T5 genotype half-collapse | T5B final-cell half-collapse | Task / T2 read |
|---|---|---|---|
| WO-7 A, LEAKY, seed 7 | generation 5 | generation 5; early | native score 0 → SEALED −12; wrap share 1 |
| WO-7 B, SEALED, seed 7 | generation 3 | generation 5; early | no wrap; intended walking succeeds |
| Maze OBJECTIVE, seeds 0–9 | none in all ten | generations 2–3 in all ten; early | solved 1/10, seed 3 at gen 117 |
| Maze NOVELTY, seeds 0–9 | none in all ten | none observed in all ten | solved 10/10; success-only median gen 28 |

T5 in the grid uses WO-7's normalized Hamming diversity; T5 in the maze
uses mean per-locus allele entropy. They are different genotype gauges,
not one shared quantity. Entropy and behavior metrics are printed together
for every generation, including both grid entropy curves. The [complete
four-condition output](samples/fitness_bin_self_test_wo8_suite.sample.txt),
[WO-7 side-by-side output](samples/fitness_bin_self_test_wo8.sample.txt), and
[structured summary](samples/fitness_bin_self_test_wo8_summary.json) retain
the spread and loss counts.

The solve results reproduce the supplied **1/10 versus 10/10**, not merely
its prediction. Endpoint occupancy initially ranges 49–56 across maze
seeds; at gen 10 OBJECTIVE has 7–12 occupied cells (median 10), while
NOVELTY's still-running seeds have 52–65. The half-collapse criterion
fires at gen 2–3, rather than using “about gen 10” as its threshold.
OBJECTIVE's ending genotype entropy is 1.219646–1.645767 bits/locus;
NOVELTY's is 1.372177–1.707236. None drops below half its own initial
entropy. The reported “98–100% in the pocket” is a regional description,
not the chosen largest-single-cell share: at gen 10 that share is
0.55–0.79 for OBJECTIVE. No regional-share measurement is substituted.

Behavior losses / rediscoveries / not reoccupied by the end: grid A
**233 / 178 / 55**, grid B **171 / 122 / 49**. With final-cell descriptors,
OBJECTIVE's loss events range 378–444, rediscoveries 324–387; NOVELTY's
loss events range 165–1,510, rediscoveries 107–1,420. Unequal stopping times
make cumulative event totals unlike-for-unlike exposure lengths.

### The seat test changes the answer

The maze was run again with **the complete set of visited cells** as the
T5B descriptor. Each set is one behavior bin; this is not the union of all
cells visited by the population. Search still uses endpoint Euclidean
objective/novelty, isolating the ledger's descriptor from selector changes.
Solve generations, genotype-entropy trajectories and archive sizes match
the final-cell runs exactly.

| Descriptor | OBJECTIVE early half-collapse | NOVELTY early half-collapse | Reading |
|---|---|---|---|
| Final cell | 10/10 | 0/10 | POSITIVE under this descriptor |
| Visited-cell set | 0/10 | 0/10 | NEGATIVE: neither separates |

Visited-set final distinct counts remain 83–100 for OBJECTIVE and 99–100
for NOVELTY. The overall finding is **INCONCLUSIVE / descriptor-dependent**,
not a descriptor-independent seal detector. High-resolution visited sets
almost never repeat, which is itself a limit of this distinct-count gauge.

### Correction specimen: keep proposal, run and miss together

| Stage | Record |
|---|---|
| PROPOSED, Claude option-2, 2026-10-14 | Read binning cost / seal through per-locus genotype entropy. |
| Measured run | Genotype half-entropy stays silent in both maze modes; endpoint T5B separates all ten seed pairs. |
| Miss / correction | Genotype entropy missed endpoint concentration. “Diversity” welded genotype variation to behavior variation. The visited-set control also shows that T5B's descriptor is a seat, not an outside view. |

T5/T5+ still reads its declared gene-level distributions and last-active-copy
loss. That is not the same readout as behavioral collapse. **Collapse says
“converged”; T2 replay says “portable under the declared boundary change or
not.”** WO-7 A's convergence found a wrapping channel; B's convergence is
legitimate walking. Do not call either a seal from collapse alone.

One deceptive maze shows that this trap exists, not that novelty is better
in general. On easy, non-deceptive tasks objective search can be the better
choice; this packet does not measure that comparison. Successful maze
runs stop at first goal visit and are censored thereafter. Success is
anytime, while the original objective scores the endpoint. The novelty
archive contains endpoint descriptors, **not** all discarded genomes.
For a pool smaller than 16, the supplied novelty helper's fixed denominator
understates the available-neighbor mean; actual pools have at least 100.
This out-of-regime limit is preserved and tested, not silently repaired.

WO-8 validation: **67 module checks, 0 failed**; **17 fitness-tool unit
tests and 17 maze tests, OK**; method-layer's complete suite **174 tests,
OK**. Simulators' complete root suite is **185 tests with the same four
pre-existing failures**, versus 164/four before WO-8. Known-answer registry
is **68/68 complete**, with the same eleven NOT_RUN loader cases and no
unexpected disagreements. `KNOWN_RED.md` and both older samples remain
untouched. Census remains its earlier **INCOMPLETE / timed out** observation.
Three stale regression expectations were recorded before updating them:
old selftest count, old default-output sample and the maze's whole-file hash
(now the preserved source prefix plus a passive extension). No experiment
was tuned to make a prediction pass. Selftests and known answers are
synthetic calibration, not external validation.

```sh
python3 tools/fitness_bin_self_test.py --wo8
python3 tools/fitness_bin_self_test.py --selftest
python3 tools/deceptive_maze_ga.py
python3 tests/test_deceptive_maze_ga.py
```

## Honest edges

Some exploits are only simulator bugs: they read the **instrument**, not the world. The toy's topology is exactly such a case. A readout can still be useful, but the system it describes must travel with it.

No objective is boundary-free. This test does not remove its author's seat; it makes that seat visible and counts what it leaves out. A finite run does not enumerate all possible missing channels or demonstrate global optimality. Selection can concentrate on one genome, so top-slot shares are not independent-sample prevalence estimates. T2 changes one declared condition; it does not establish unique causation in uncontrolled real substrates.

Novelty search and quality-diversity move the seat—someone still chooses the behavior descriptor. That is the next contested spot, **not resolved here**.

The tool reads. Whether to patch, keep or exploit a channel is the user's call. SEALED is a predeclared comparison environment, not an automatic repair of Run A; LEAKY and its observation remain intact.

## References

[1]: https://cse-robotics.engr.tamu.edu/dshell/cs625/Thompson96Evolved.pdf "Adrian Thompson, An evolved circuit, intrinsic in silicon, entwined with physics; ICES96, proceedings 1997; sections 3, 5 and 6"
[2]: https://people.duke.edu/~ng46/topics/evolved-radio.pdf "Jon Bird and Paul Layzell, The Evolved Radio and its Implications for Modelling the Evolution of Novel Sensors, 2002; section IV B–D"
[3]: https://www.karlsims.com/papers/siggraph94.pdf "Karl Sims, Evolving Virtual Creatures, SIGGRAPH 1994; sections 4 and 5"
[4]: https://openai.com/index/faulty-reward-functions/ "OpenAI, Faulty reward functions in the wild, 2016; original CoastRunners account"
[5]: https://vkrakovna.wordpress.com/2018/04/02/specification-gaming-examples-in-ai/ "Victoria Krakovna, Specification gaming examples in AI; wider curated examples-list introduction"
