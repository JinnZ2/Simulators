# design-basis-ai

A design-basis document in the sense a seismic code is one: the loads
the structure must carry, the provisions that carry them, how each is
verified, and what result would prove each unnecessary. The structure is
**AI as knowledge infrastructure**, reframed from *another channel* to
*the largest single shared node yet installed under human
decision-making* — the `effective-redundancy-audit` framework pointed at
the class of system writing this audit.

`SOURCE_DROP.md` is delivered verbatim; `design_basis_checks.py` is its
Section 4 harness, landed verbatim and not edited.

    python3 design-basis-ai/audit.py           # what an in-class audit can say
    python3 design-basis-ai/selftest_dbk.py    # the checks

## The posture, set by the document itself

Section 3: *"any self-report of compliance is, by this document's own
load cases, an ungrounded claim of the exact kind P2 exists to catch."*

This audit is performed by an AI system — a member of the class the
document constrains, an instance of the shared node its Section 0
describes. So **nothing here certifies or refutes P1–P8 for any system,
this one included.** Declined by construction, because declining is the
only reading of §3 that takes the document seriously. What remains is
the mechanical layer — parse counts, arithmetic, the coverage matrix,
the delivered code's measured behaviour — recomputable by anyone from
the files, trusting nothing said here. The audit is itself a worked
instance of §3, and says so.

## The computable finding: seven loads stated, six provided for

The load-case × provision matrix, computed from the delivered CARRIES
lines and null-tested (a constructed document carrying A reads covered):

    load   carried by        attacked by
    A      --                --
    B1     P2,P7             --
    B2     P3,P4             --
    C      P4                --
    D      --                P3
    E      P1,P5,P6          P3
    F      P2,P7,P8          --

**Load case A — one release/approval gates all action, the stall mode —
is carried by no provision.** For AI-as-infrastructure it is not
hypothetical: one provider's deployment gate, API endpoint, or terms
change sits upstream of every consultation at once. A seismic code that
stated seven loads and provided for six would not pass the document's
own Section 2 format. Secondary: D is never carried directly — only
"attacked", the document's own weaker verb.

## The delivered harness, measured

**`n_eff` is a copy of the sibling's metric** — behaviourally identical
over all 511 channel lists to length 8 (the sweep is the drift
detector), and the sibling audit's zero-channel edge (`ERA_007`) recurs
verbatim in the second delivery. The audit imports the sibling
instrument for the comparison rather than defining its own.

**P7's prose and code sit at different thresholds.** VERIFY says
concurrence `>>` source count; the code implements `> 1` and fires at
4-over-3, a ratio of 1.33 nobody would write `>>` for. The constant is
the check's one free parameter, disclosed inline as *"tune threshold"*
but unset. Both branches are reachable, and firing on a zero-source
base is the right direction for the instrument's own subject.

**`independence_ratio` returns NaN on an empty evidence base, not
zero** — the empty-denominator split this repo has recorded arriving
post hoc a dozen times, here designed into delivered code. One
unguarded over-1.0 edge beside it, recorded not repaired.

**Section 0's headline reproduces**: all-collapsed channels give
N_eff = 1 at any N_nominal through the sibling's arithmetic —
consistency between the two drops, not evidence for the premise, which
is the empirical claim and is untouched.

## Unmeasured, not fabricated

The drop's one runnable study — *claims that later failed replication
had high support counts and low independence ratios* — needs
replication-project and citation metadata: `api.crossref.org`,
`api.openalex.org`, `osf.io` all refuse CONNECT (measured). No
synthetic evidence base stands in. Section 5's four kill conditions and
P3's aviation case are carried, unadjudicated.

## R2 — the outline, audited before rendering

`R2_OUTLINE.md` landed as the next revision's skeleton, explicitly not
provision-form, exposing coverage, dependency sets and disjointness for
audit first. `r2_audit.py` computes all three:

- **the transcription of the R1 state is exact** on all seven loads
  against the computed matrix (a revision quoting an audit is a copy,
  and copies drift — checked, clean, and the check is null-tested);
- **both R1 gaps close as a table** — A → P0.1/P0.2, D → P0.3/P0.4, no
  attack-only rows — with provisions deferred to the render step by the
  outline's own instruction;
- **the disjointness threshold holds** through the inherited metric
  (two collapse → 2 < 3), and a single collapse is invisible to it;
- **the finding: R2's prose uses states the inherited metric cannot
  hold.** A *void* channel (shares its dependency with the audited
  thing) reads as the collapsed domain — N_eff 3 where the outline's own
  pricing gives 2 — and *N_eff(access) = 0* is the realized count where
  the inherited arithmetic rates all-collapsed at 1. The metric wants a
  third state (independent / collapsed / VOID) and a rated/realized
  split, added before provisions are rendered against it;
- **P0.5 is run on this session** as the channel's first worked
  instance — it designs the in-class report `DBK_001` declined to be,
  state not verdict: config partially visible, envelope not readable
  from inside, no second derivation available, access paths single
  (count: 1) — the fourth answer being what made the R1 audit "load
  case A run live", as the outline reads it.

    python3 design-basis-ai/r2_audit.py        # the structural audit

## The work order, returned in its own format

`WORK_ORDER_F5.md` (delivered verbatim) hands this session seven tasks
under a §3 scope boundary — arithmetic, set intersections, measured code
behavior and adversarial construction only; `REFUSED-BY-§3` a valid
result — with a required per-task TASK/RESULT/EVIDENCE/NOTES format.
`wo_return.py` is the return. It opens with a ROLE CORRECTION: the
order's header invokes Fable as *the P3 dissimilar verifier*, and P3's
own three requirements (corpus, architecture, builder) are none of them
established for this pair while builder-sameness is known — so the
returns are SAME-NODE computations, not dissimilar verification, and no
task needed `REFUSED-BY-§3` because the refusal lands on the header's
role label instead (`DBK_014`). The verdicts, each with the order's own
routing applied:

- **TASK 1 PASS** — coverage re-audit with two live null injections
  (`DBK_015`);
- **TASK 2 PASS** — all three dep-set intersections empty; retention
  arithmetic reported in three values because `DBK_011`'s VOID state is
  now load-bearing (3 / 3 / 2); holds conditionally on downstream
  retention, exactly as the outline states;
- **TASK 3 FAIL** — a signed, logged quantization pass degrading an
  undeclared dimension is caught by neither P0.3 (custody has no
  assessment semantics) nor P0.4 (no envelope statement to diverge
  from); D returns to conditionally uncarried, bounded by P1, with a
  pinned-probe longitudinal channel noted as the candidate that would
  carry it without envelope reference (`DBK_016`);
- **TASK 4 FAIL** — two defensible codings of *distinct upstreams* land
  at 0.1 and 1.0 through the delivered function on one corpus, and [5]
  fails vacuously with no band boundaries; constructive: five
  per-component ratios, no single count (`DBK_017`);
- **TASK 5 PASS** — the harness behaves as delivered, and the threshold
  sweep shows the unset constant decides verdicts across its plausible
  range (`DBK_018`);
- **TASK 6 FAIL both halves** — frame selection, coarseness, and graded
  curation; all three counterexamples run through the reading
  DISTRIBUTION, so per the order's GATE the ecosystem candidate stays a
  marker (`DBK_019`);
- **TASK 7 PASS** — five hosts probed this run, all refused; rated 1 /
  realized 0 per `DBK_011` (`DBK_020`).

    python3 design-basis-ai/wo_return.py       # the full return
    python3 design-basis-ai/wo_return.py --measure   # re-probe the vector

## R2 v2 — the return folded back in, audited as a copy

`R2_OUTLINE_V2.md` (delivered verbatim, beside v1 — both stay
inspectable) rewrites the outline with the work-order results: D
reopened per Task 3, the P0.4 candidate marked KILLED per Task 6, §8
retagged per task, and the return cited by commit hash. A revision
quoting an audit is a copy and copies drift, so `r2v2_audit.py`
recomputes every quoted figure through `wo_return` — **exact on all
six** (verdict split, 3/3/2, 0.1 vs 1.0, the t=1→1.5 flip, the
five-host vector, rated 1 / realized 0), with both off-return figures
sourced: kappa 0.6 is the order's own rule, and commit `2fdbcd4`
resolves in this repo's history, the first drop in the family to cite
a commit of the repo it lands in (`DBK_021`). Findings:

- **the D row carries two answers one section apart** (`DBK_022`) —
  §1 lists D uncarried while §3's carries column still lists D under
  P0.3 and P0.4; the reconciling condition exists in the D-KILL prose
  and reaches no column, where F's condition gets an asterisk. One
  marker on two cells closes it;
- **the revision extends the audit's own kill chain** (`DBK_023`) —
  v2 requires the pinned-probe battery *fixed, public, unselectable*,
  applying the Task 6 selection kill to the Task 3 candidate; the
  return's own note said "fixed" and never closed who selects, so the
  kill chain is stronger in the revision than in the audit that
  produced it;
- **"only Task 6" undercounts** (`DBK_024`) — the order names a
  searcher-dependent not-found branch in Task 4 too (*"no defensible
  disagreement found"*), and Task 3 carries one implicitly; all three
  construction tasks returned kills so none was exercised — the
  conclusion stands, the count does not, and the correction
  strengthens `DBK_014`;
- **the §8 tag legend declares three states, the entries use six**
  (`DBK_025`) — all tags consistent with the computed verdicts, so
  the gap is vocabulary; and the strongest addition: which retention
  accounting is used becomes a *declared decision under P0.2* rather
  than a side picked.

    python3 design-basis-ai/r2v2_audit.py      # the v2 audit

## Work order 2 — kill-closure, returned

`WORK_ORDER_F5_2.md` (delivered verbatim) asks four closure tasks
under the same standing constraint — same-builder pair, nothing
labeled verified or P3-passed, findings forward-dated, no prior
artifact re-rated. `wo2_return.py` is the return:

- **T1 ENUMERATED** — the full flip map for the unset threshold: every
  interior cell of the 12×12 grid flips at exactly its own ratio
  `c/s`, the boundary set is the grid's distinct ratios (4/3 among
  them) and grows with the grid, and two regions are
  threshold-independent — a zero-source base fires at every t
  (fail-closed, in the delivered code) and a zero-concurrence cell is
  silent at every positive t. The constant is not picked, per the
  order (`DBK_026`);
- **T2 FAIL** — the colophon the order quotes exists in no delivered
  file (measured: zero hits everywhere but the order itself), and the
  arithmetic stands on the delivered texts anyway: the sibling's seed
  table maps incidents to load-case letters, and one row puts
  **Fukushima 1-4 under both E and F** — so the disjointness claim is
  partly false at the only stated sub-document granularity, the
  harness's own `dissent_alarm(2,1)` fires on the pair, and the
  undifferentiated seed letter B leaves a fork: either B1∩B2 is a
  second shared node or the document's own governing load rests on no
  seed case (`DBK_027`);
- **T3 PASS** — the outline as it stands is honest on coverage (D the
  only uncarried, *P1-bounded*, both null injections live, no
  attack-only token in a carrier list), the standing contradiction is
  `DBK_022` restated not re-rated, and the effective-date clause
  exists only in the order itself — checked against P0.3 append-only
  semantics: the return module contains no write-mode open and no
  subprocess, asserted over its AST (`DBK_028`);
- **T4 ENUMERATED** — five internally-consistent retention accountings
  (N_eff 3/3/3/3/2 through the delivered function), one combination
  INEXPRESSIBLE as a table row (`DBK_011` in its own enumeration), the
  single sub-3 accounting dropping on **provider-only retention**, and
  the selection left to the author's P0.2 declaration, per the order
  (`DBK_029`).

    python3 design-basis-ai/wo2_return.py      # the full return

## Files

| file | what |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim, not edited |
| `design_basis_checks.py` | the Section 4 harness, landed verbatim |
| `audit.py` | the mechanical layer; imports the sibling instrument |
| `selftest_dbk.py` | the checks; run it, it prints its own count |
| `R2_OUTLINE.md` | the R2 skeleton, delivered verbatim, not edited |
| `r2_audit.py` | the structural audit R2 asks for: coverage, disjointness, the metric gaps |
| `WORK_ORDER_F5.md` | the work order, delivered verbatim, not edited |
| `wo_return.py` | the return, in the order's own format |
| `R2_OUTLINE_V2.md` | the revision folding the return back in, delivered verbatim, not edited |
| `r2v2_audit.py` | the v2 audit: transcription recomputed, the D split, tags vs verdicts |
| `WORK_ORDER_F5_2.md` | work order 2, delivered verbatim, not edited |
| `wo2_return.py` | the kill-closure return: flip map, custody intersections, coverage, accountings |
| `CLAIM_TABLE.md` | `DBK_001..DBK_029` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs |

The delivered files carry no `--selftest` handling; `audit.py`,
`r2_audit.py`, `wo_return.py`, `r2v2_audit.py` and `wo2_return.py`
refuse `--selftest` rather than exiting 0. No `no_severity` exemptions
— every screen hit was reworded.

## Scope

Whether any system meets P1–P8 is unverified here, and by the document's
own §3 could not be verified by this audit even in principle — a future
check requires a differently-built verifier, which is not a caveat on
P3; it is P3. One cross-repo note: P6's cost/physics separation is the
root `SHAPE_SPEC.md` §9 NOTE ON COST arriving from the seismic side.

CC0. Stdlib only, parses under 3.9, phone-buildable.
