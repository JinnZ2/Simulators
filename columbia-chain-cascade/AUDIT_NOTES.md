# AUDIT_NOTES — the kill list under audit, and the cold-start test

`CCA_001..CCA_009`. All audit content is here and in `kill_audit.py` /
`selftest_kill.py`; the delivered package is edited by nothing. The
package arrived with its own kill list, sent as **claims under test**
with the instruction *"a kill Fable overturns is a better outcome than
a kill it confirms."* All three hold; none is overturned. Two further
findings the landing turned up are recorded, and the cold-start test is
run over the fifteen gaps.

Nothing here runs HEC-RAS or touches real terrain. The spec's actual
subject stays untested (`CCC_008`); this is what a text-only
environment can say about the package.

## REFUTATION_PROTOCOL

Every claim names what would overturn it. A failed check updates the
claim, never the delivered package.

| id | claim | status |
|---|---|---|
| `CCA_001` | KILL 1 (a self-correction trace left in `contributing_inflow.render()`) is CONFIRMED as an overlay artifact — and it carries an intended, arithmetically sound conclusion. | SUPPORTED |
| `CCA_002` | KILL 2 (the stated decisive condition differs from the coded one) is CONFIRMED — prose reads the max-flip, code computes the sum-tip, and they diverge on 226 of 540 swept cases — and RESOLVED by physics: the code is right. | SUPPORTED |
| `CCA_003` | KILL 3 (tribal supplied from memory, asymmetric discipline) is CONFIRMED and sharper than stated; its second claim (the fix is not to drop tribal) is CONFIRMED too. | SUPPORTED |
| `CCA_004` | The kill list is itself under audit: all three hold, KILL 2's OPEN was closed by the sender's physics and this audit upholds that closure rather than re-opening it. | SUPPORTED |
| `CCA_005` | `CCC_017` is REFUTED on its delivered instance: `module_f.render()` trips the repo's own `no_severity` screen. | SUPPORTED |
| `CCA_006` | The delivered `selftest_ccc_v2.py` exercises v1 `eap_coverage` + v1 `audit` + the new `module_f`; the revised `eap_coverage_v2.py` and `audit_v2.py` are delivered and **unexercised** — and the tribal list is exactly where KILL 3 lives. | SUPPORTED |
| `CCA_007` | The cold-start test discriminates: all fifteen gaps name a stranger-evaluable falsifier and a deliverable interface, while the flags cluster on public-data access (Q1) and one-semester scope (Q4). | SUPPORTED |
| `CCA_008` | The gap file carries one bare `if published` pre-closure (Gap 6), the shape the cover note flags; the sender's TIER + ROUTES + IF REFUSED replacement applies. | SUPPORTED |
| `CCA_009` | Nothing here bears on any hazard field, breach, or exposure — the spec's subject — and no claim rests on a hydraulic result or a literature fact. | UNVERIFIED |

---

## CCA_001 — KILL 1 confirmed; the trace carries a sound conclusion

`contributing_inflow.render()` prints a reasoning trace that starts to
state the opposite verdict, catches itself (`Wait —`), and lands on the
right answer. Checked as arithmetic: at wave 6, `pool_effective` 5.2,
crest 10, the coupled operator breaches (6 + 5.2 ≥ 10) and the
independent operator does not (`max(6, 5.2)` = 6 < 10). So the
correction is sound; the false start and the `Wait —` are the overlay
artifact. The TEST the kill posed — *is it an artifact, or does it
carry something intended?* — resolves **both**: it is an artifact, and
what it carries is the intended, correct conclusion. The correction
(excise the false start, keep the corrected line) is **shown, not
applied** — the delivered file stays as delivered.

**Falsifier:** the corrected line being arithmetically unsound, or no
trace in the render. Both are pinned in `selftest_kill.py`.

## CCA_002 — KILL 2 confirmed and resolved by physics

The prose says the increment is decisive when `wave < pool_effective <
crest` — a reading in which the pool overtaking the wave is what
matters, i.e. the `max` (independent-node) operator. The code computes
`urban_decisive = (not coup_base) and coup_urb` — the increment tipping
the `sum` (coupled) verdict from no-breach to breach. Swept over 540
synthetic cases the two **disagree on 226**. The sender resolved it by
physics rather than by author intent: the reservoir does not empty to
receive the wave, so the displacement wave rides on a surface already
at pool elevation and the combined quantity is `wave + pool`; `max`
would be correct only if the wave *replaced* the pool, and nothing does
that. The code (sum) is right; the prose diverged. The interesting part
is the shape of the divergence — **the independent-node default
reasserting itself in the translation layer of a module written to
refute it**, which is the repo's own *prose drifts, code is
constrained* thesis instanced in a module about exactly that. The prose
correction is recorded, not applied. The sweep also confirms the code's
one-sidedness: the urban increment never causes an independent-only
breach.

**Falsifier:** zero prose/code disagreements across the sweep, or the
sweep producing an independent-only breach. Both are pinned.

## CCA_003 — KILL 3 confirmed, and sharper than stated

The asymmetry is real and the audit sharpens it. Owner data is refused
from memory (every owner field `UNASSIGNED`, an AST check in the
delivered v1 selftest asserting no other value appears) **and** each
node row carries a `knowledge_state` field (`UNKNOWN_ATM`). The six
tribal rows are supplied from memory as bare 4-tuples — nation,
reservation, upstream node, downstream node — with **no
`knowledge_state` field and no source**, at a finer granularity than
the owner data the module refuses. And the authority bound is invariant
to the tribal list (2 with it, without it, or emptied), while the prose
asserts tribal *"adds additional sovereign authorities, strengthening
the claim"* — a claim the computed number does not carry, so the tribal
list is **computationally unused** in the bound it is said to
strengthen.

The second claim holds too: `knowledge_state.py` rejects
`INSTITUTIONAL_EXCLUSION` as an invalid epistemic state, so removing the
sovereign nations to tidy the asymmetry would re-commit exactly that.
The correction that overturns neither of the kill's claims: bring tribal
**under the same discipline the owners already carry** — a
`knowledge_state` per row and a named source or an explicit refusal,
symmetric with the owner `UNASSIGNED` / `UNKNOWN_ATM` treatment. Keep
the nations; type the data. This is the repo's own memory-refusal rule
(`CCC_005`, `PB_001`/`CW_004` at its highest stakes) meeting its own
anti-exclusion rule, and the resolution honors both.

**Falsifier:** the tribal rows carrying a `knowledge_state`, or the
authority bound moving with the tribal list. Both are pinned against the
delivered `eap_coverage_v2.py`.

## CCA_004 — the kill list is itself under audit

Three kills, three confirmations, none overturned — which is the less
welcome outcome by the sender's own standard, and it is recorded as
such rather than softened. KILL 2 arrived with an OPEN (*"which is
correct is not Claude's to call"*) that the sender then closed by
physics; this audit upholds that closure rather than re-opening it,
because the physics is checkable and the audit checked it. Each verdict
is bounded to what a text-only environment can establish — the
arithmetic and the module structure — and none is a statement about any
hydraulic magnitude.

**Falsifier:** a fourth reading of any kill that overturns the verdict
here. The kills travel as claims under test precisely so that reading
is welcome.

## CCA_005 — CCC_017 refuted on its delivered instance

`CCC_017` asserts the `module_f` report carries no flagged language.
The repo's own `no_severity` screen disagrees: the report's closing
line trips it on a certainty verb (the token `proves`, in *"This module
proves the mechanism is load-bearing when it is"*). The delivered
claim's own falsifier fires on the delivered artifact. Recorded, not
corrected — `module_f.py` is delivered. This is the one delivered
`CCC_*` claim that does not hold against its delivered code, and it
holds against everything else in the module-F block (the ordering
proof, the 19,200 sweep, the four nulls all reproduce).

**Falsifier:** the screen coming back clean on `module_f.render()` —
which it does not, pinned in `selftest_kill.py`.

## CCA_006 — the delivered v2 selftest exercises the v1 modules

`selftest_ccc_v2.py` imports the bare `eap_coverage` and `audit` — the
v1 files — unpacks `NODES` as a 4-tuple, and reads the v1 truncation
key `module_f_body_complete`. So it exercises **v1 `eap_coverage` + v1
`audit` + the new `module_f`**. The revised `eap_coverage_v2.py` (a
5-tuple `NODES` carrying the tribal list) and `audit_v2.py` (the key
renamed to `..._in_source_drop`) are delivered and **not exercised** by
the delivered selftest — a 4-tuple unpack against the 5-tuple would
raise, and the renamed key is absent from the v2 audit. The tribal list
is exactly where KILL 3 lives, so the asymmetric-discipline row ships
untested: the selftest that would catch it is pointed at the module
without it. This is the strongest structural finding, because it is the
reason the KILL 3 defect could ship at all.

**Falsifier:** the v2 selftest importing the `_v2` modules or unpacking
a 5-tuple. It does neither; both are pinned.

## CCA_007 — the cold-start test discriminates

The sender's five questions, coded per gap in `kill_audit.COLD_START`
with a one-line basis each (declared as data, so a reader disagrees row
by row): Q1 public-data-startable, Q2 stranger-evaluable falsifier, Q3
named deliverable interface, Q4 one semester not five, Q5 no
dead-reference. Over the fifteen gaps (13 in the file + GAP 14
`mining-increment/` + GAP 15 `bridge-impoundment/`): **Q2 and Q3 are
clean throughout** — every gap names a falsifier a stranger can
evaluate and a deliverable that drops into a named interface, the two
the agenda most has to get right. The flags cluster on **Q1** (the
hydraulic gaps that want HEC-RAS or gated dam data — 7 of 15 are not
public-data-startable) and on **Q4** (tribal EAP, breach params,
Vanport — three gaps that read as more than one semester). Q5 flags
once, on the Gap 6 pre-closure below. Eight of fifteen are startable on
public data alone; seven are clean on all five.

**Falsifier:** a gap with no stranger-evaluable falsifier or no
deliverable interface — which would flag Q2 or Q3 and is worth more
than the Q1/Q4 flags, since Q1/Q4 are cost, and Q2/Q3 are whether the
gap is a research question at all.

## CCA_008 — one pre-closure in the gap file

The cover note's access-tier discipline: **state the barrier, name
known routes, stop there** — never a conclusion about what a reader can
reach. A bare `if published` pre-closes a route by parenthesis, telling
the reader to check and move on with no route and no tier. The
delivered gap file carries exactly one, at Gap 6 (*"Dam-specific
seismic vulnerability assessments (if published)"*) — the same shape
the cover note flags on the Gap 14 data line. The sender's replacement
applies: `TIER: GATED`, `ROUTES:` the district office file, the dam
safety program manager, university holdings of USACE reports, the FERC
licensing record (which is open); `IF REFUSED:` document the refusal,
which is itself a finding on the Gap 3 EAP-coverage question. Recorded;
the delivered file is not edited.

**Falsifier:** a second `if published` (or any bare pre-closure) in the
gap file. Exactly one is present, pinned.

## CCA_009 — nothing here is a hydraulic result (UNVERIFIED)

No hazard field, no breach, no exposure, no velocity band, no time
slice. The whole subject of the spec is untested here and inherits
`CCC_008`. The deep-research roadmap's literature claims are carried
and egress-blocked, and nothing in `CCA_001..CCA_008` rests on a
hydraulic result or a literature fact — every verdict is a property of
the delivered arithmetic, the delivered module structure, or the
delivered text.

**Falsifier:** the spec run with the engine and the data. That is the
project; this is the reading a text-only environment can give of its
kill list.
