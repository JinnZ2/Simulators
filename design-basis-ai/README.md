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

## Files

| file | what |
|---|---|
| `SOURCE_DROP.md` | delivered verbatim, not edited |
| `design_basis_checks.py` | the Section 4 harness, landed verbatim |
| `audit.py` | the mechanical layer; imports the sibling instrument |
| `selftest_dbk.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `DBK_001..DBK_009` with REFUTATION_PROTOCOL |
| `samples/` | pinned run |

The delivered file carries no `--selftest` handling; `audit.py` refuses
`--selftest` rather than exiting 0. No `no_severity` exemptions — every
screen hit was reworded.

## Scope

Whether any system meets P1–P8 is unverified here, and by the document's
own §3 could not be verified by this audit even in principle — a future
check requires a differently-built verifier, which is not a caveat on
P3; it is P3. One cross-repo note: P6's cost/physics separation is the
root `SHAPE_SPEC.md` §9 NOTE ON COST arriving from the seismic side.

CC0. Stdlib only, parses under 3.9, phone-buildable.
