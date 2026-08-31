# AUDIT_NOTES — the kill list under audit, and the cold-start test

`CCA_001..CCA_014`. All audit content is here and in `kill_audit.py` /
`selftest_kill.py`; the delivered package is edited by nothing. The
package arrived with its own kill list, sent as **claims under test**
with the instruction *"a kill Fable overturns is a better outcome than
a kill it confirms."* All three hold; none is overturned — but the
second pass **sharpens** each at its root rather than ratifying it
(`CCA_011`, `CCA_012`), which is what the sender asked for. The audit
runs on two axes: **arithmetic** (the three kills, `CCA_001..003`) and
**cold-start** (can a stranger start from this). On the cold-start axis
the sender corrected Q1 — *every source tiered and routed, not "is it
public"* — and under that corrected criterion **all 15 gaps carry the
same open item** (`CCA_010`): 0 of 76 data sources are tiered. Two
findings the landing turned up (`CCA_005`, `CCA_006`) and the three new
package cards (`CCA_014`) complete it.

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
| `CCA_010` | The corrected cold-start Q1 (every source tiered, every non-open source routed) fails for **all 15 gaps**: 0 of 76 sources carry a tier or a route, and the tier discipline START_HERE declares is applied to no source bullet. This supersedes the first pass's Q1. | SUPPORTED |
| `CCA_011` | KILL 3 sharpened at its root: the six tribal rows match `DEEP_RESEARCH.md` §6.1, and the same doc pushed owner-from-memory (§3/§6.2, "overly broad"); the code declined it for owners and took it for tribal — the asymmetry winning where no external constraint held it. | SUPPORTED |
| `CCA_012` | KILL 1 and KILL 2 are one contiguous prose zone in `contributing_inflow.render()`, and the `urban_sensitivity` docstring states the sum reading correctly — so the drift is confined to the rendered narrative, not the arithmetic and not even the docstring. | SUPPORTED |
| `CCA_013` | The two GAP 14 provenance flags (Padhy 2026, Piao 2024) are the model of the citation discipline; a scan finds no other unflagged dead reference; GAP 15 hedges per-block where GAP 14 hedges per-citation. | SUPPORTED |
| `CCA_014` | The three cards land (`START_HERE.md`, `GAP_14_mining_hydrology.md`, `GAP_15_bridge_impoundment.md`); a declared [CHOICE] keeps them as cards 14/15 beside the byte-identical delivered 13-gap file. | SUPPORTED |

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

## CCA_010 — the corrected cold-start Q1 fails for all fifteen gaps

The first pass scored Q1 as *"startable on public data alone"*. The
sender's corrected Q1 rules that question out: *"every source tiered,
every non-open source names ≥1 route; an untiered source is the item,
NOT 'is it public'."* Rescored mechanically over the data-source bullet
lists: **76 sources across the 15 gaps, 0 carrying a tier or a route.**
The tier vocabulary (OPEN / REQUESTABLE / GATED / UNKNOWN) is declared
in `START_HERE.md`'s table and attached to no source bullet in any gap
— the two new cards included. The only tier-shaped marks on a source
are the two bare `if published` pre-closures (Gap 6 in the delivered
file; the rim-stability line in the GAP 14 card), and both pre-close a
route by parenthesis rather than tiering it. So on the data-path axis
every gap carries the same open item, the remedy is uniform and cheap
(tier each source; for every non-open one, name a route), and this
supersedes the first pass's Q1. `tier_scan()` computes it; the detector
is null-tested both ways (it fires on a tiered+routed line, stays
silent on an untiered one).

**Falsifier:** any gap whose sources are all tiered-or-routed — which
would be the first, and is the state the remedy produces. Pinned at 0.

## CCA_011 — KILL 3 sharpened at its root: the deep-research prose

The six tribal rows in `eap_coverage_v2.TRIBAL_JURISDICTION` match
`DEEP_RESEARCH.md` §6.1's entry (*"Add: a tribal_jurisdiction() function
… Colville Reservation (upstream of Grand Coulee), Spokane (near Wells),
Yakama (near Priest Rapids), Warm Springs (near The Dalles), Umatilla
(near McNary)"*) line for line, plus Nez Perce which §6.1's own list
also names. And the **same document** argues, in §3 and §6.2, for adding
owner assignments from memory — *"Grand Coulee → USBR (public,
uncontroversial) … These are not 'invented from memory' … The current
refusal is overly broad."* The code declined that push for owners (every
owner `UNASSIGNED`, and the delivered selftest walks the AST to assert
it) and took it for tribal (no check, no source, no knowledge state,
unused in the bound). The asymmetry KILL 3 names is the translation
layer winning exactly where no external constraint held it — the
sharpest instance of the provenance thesis the package states about
itself (*"defects cluster in the prose and comments, not the physics"*).
This sharpens KILL 3 rather than overturning it, and it corrects the
picture: the from-memory tribal data is not a stray, it is the
deep-research doc's recommendation reaching the code where the AST check
did not guard.

**Falsifier:** the tribal rows not matching §6.1, or the deep-research
doc not pushing owner-from-memory. Both are pinned against the delivered
text.

## CCA_012 — KILL 1 and KILL 2 are one prose zone; the docstring is right

KILL 1 (the `Wait —` self-correction trace) and KILL 2 (the
`wave < pool_effective < crest` max-reading formula) are not two
independent items: they are one contiguous passage in
`contributing_inflow.render()` (the urban_increment 0.3 example through
the "decisive when" formula). And the code's own docstring for
`urban_sensitivity` states the coupled/sum reading correctly — *"makes
coupled breach where independent does not"*. So the drift is confined to
the **rendered narrative**: not the arithmetic (the sweep and null tests
use the functions, not the render), and not even the docstrings. *Trust
the code over the comment* holds and sharpens — here the comment is
right too, and only the story told about the numbers drifted back to the
independent-node default. This is the cleanest confirmation of the
provenance thesis: the least-constrained artifact (rendered prose)
carries the drift, the constrained artifacts (arithmetic, docstrings)
do not.

**Falsifier:** the two kills sitting in different functions, or the
docstring carrying the max reading. Both are pinned.

## CCA_013 — the citation axis: no unflagged dead reference

The two GAP 14 provenance flags — *"Padhy et al. 2026"* and *"Piao et
al. 2024"*, both marked *"could not be confirmed"* with the confirmed
Knothe anchor (Zhang 2022) kept and the unconfirmed pairing set aside —
are the model of the discipline the sender points to (*"see the two
UNVERIFIED-PROVENANCE flags in GAP 14"*). A scan of the 15 gaps finds no
other citation asserted without a hedge that a stranger would chase into
a dead reference. GAP 15 hedges per-block (*"located by search, not
asserted"*) where GAP 14 hedges per-citation; the per-citation form is
the stronger one, because it names which reference is unconfirmed rather
than casting doubt on the whole block, and GAP 15 would carry it better.
No dead citation is left unmarked in either card.

**Falsifier:** a citation asserted flat that a search cannot resolve —
which the scan did not find. The two GAP 14 flags are the discipline
working, not a defect.

## CCA_014 — the three cards land; the assembly is a declared choice

`START_HERE.md`, `GAP_14_mining_hydrology.md`, and
`GAP_15_bridge_impoundment.md` land verbatim. The GAP 15 card is a
revision of the earlier bridge material — it reframes the NVE note as an
INDEX-TERM NOTE (a retrieval barrier, tier OPEN, the source in English)
and carries two sign caveats, neither present in the earlier
`bridge-impoundment/SOURCE_DROP_V2.md`. The sender's instruction *"slot
GAP 14 / 15 into UNDERGRADUATE_RESEARCH_GAPS.md as entries 14 and 15"* is
met by a declared **[CHOICE]**: the two gaps land as standalone cards
numbered 14 and 15 — their own headers read *"Draft entry for
UNDERGRADUATE_RESEARCH_GAPS.md"*, and both already have full folders
(`mining-increment/`, `bridge-impoundment/`) — while the delivered
13-gap file is kept **byte-identical**, which the repo's version-audit /
self-scan discipline relies on. `START_HERE.md`'s reading order binds
all 15. Physically appending the two entries into the delivered file is
one instruction away if the sender prefers it over the byte-identical
guarantee.

**Falsifier:** the delivered 13-gap file differing from its committed
form — the selftest asserts `git diff --quiet` on it.
