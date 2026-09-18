# CLAIM_TABLE.md — failure-mode-register

Claims `FMR_001..FMR_056` are properties of this build and of the three
delivered orders. `FMR_001..FMR_025` read `WORK_ORDER.md`;
`FMR_026..FMR_039` read `WORK_ORDER_V2.md`, the revised order, landed
verbatim beside it so both stay inspectable; `FMR_040..FMR_043` are the
value-and-source gate (`tools/sourced.py`) that replaced the three
`FMR_036` defects, and the fourth defect it found; `FMR_044..FMR_056`
read `WORK_ORDER_V3.md`, the third order, landed verbatim beside the
other two. They are distinct from the
orders' own `F_A..F_M`, which are falsifiers the orders state; those are
reported by `register.falsifier_status()` and are not renumbered here.

Every number below is printed by `python3 register.py`,
`python3 register_v2.py` or `python3 register_v3.py` and pinned by the
suite of the same number. Nothing here is a statement about any deployed ML
component — see `FMR_025`.

---

**FMR_001 — Step 0 is BLOCKED and the register is not cleared to ship.**
STATUS: BLOCKED. The order's first step is a prior-art check: verify whether a
durability-scoped catalogue already exists, and if one does, *"say so and stop,
or scope to the residual. Do not build a second copy of an existing list."*
`F_B` adds that the absence of prior art *"must be established, not assumed."*
Outbound egress here is an allowlist and every catalogue and registry host
refuses CONNECT — measured, not assumed. `step0_prior_art()` returns BLOCKED
with `substituted: False`. Nothing in this folder establishes that the work
order is not duplication, and no substitute search was run from memory.
FALSIFIER: an environment that reaches the catalogues, and the search.

**FMR_002 — Step 1 was never run: no deployment class is declared.**
Step 1 exists because *"'ML system' is too broad to load-rate"*, and both Step 5
(reconstruction scoring) and section 5 (load rating) rest on it. Across the four
delivered entries, `load_condition` is stated at four different breadths and
`DUR-002` declines to narrow in as many words: *"In practice: all of them."*
`step1_deployment_class()` returns NOT_RUN with that entry named as the explicit
refusal. Every downstream figure therefore rates a class nobody fixed.

**FMR_003 — Step 5's headline is computable for one entry of four.**
Step 5 calls the YES/PARTIAL/NO distribution *"a headline result on its own."*
Counting declared vocabulary tokens per cell ([CHOICE 5], mechanical, no word
list): `DUR-004` states one value (NO); `DUR-001` and `DUR-003` state two each;
`DUR-002` states none of the three (*"Not applicable directly; DUR-002 governs
USE, not rebuild"*). `distribution_over_all` is `None` with the reason, not a
four-entry distribution taken over a mixture. Section 8 predicts that most
components score PARTIAL rather than NO and *"PARTIAL is the interesting
class"*; on one computable entry, at NO, that prediction is untested here.

**FMR_004 — the two multi-value cells are not one axis.**
`DUR-001` reads *"NO as deployed. PARTIAL with the control"* — a CONTROL axis.
`DUR-003` reads *"Degrades from PARTIAL toward NO"* — a TIME axis. A
distribution built by taking each cell's first token, or its last, would put a
control state and a date in one column. `multi_value_axes()` reports the pair
per entry and emits no merged distribution.

**FMR_005 — the register is two registers superimposed.**
`detection_channel`, `detection_latency` and `reconstruction` each carry both
the state of current practice and the state under a control the same entry
proposes, in one cell, and the section 2 schema has no axis for the difference.
`control_state_split()` measures six of twelve cells carrying both
([CHOICE 4], a marker list over delivered English; the markers found are
returned with every verdict, and a paraphrase steps around them).

**FMR_006 — the high-priority set has two sizes and the difference is whether a
proposed control counts as an existing one.**
Section 1 defines the high-priority set on `detection_channel = NONE` and calls
it *"the modes that cannot generate the evidence that would make them mandatory
to fix."* Three of four entries open that field with NONE and propose a channel
in the same cell. As-is: 3 of 4. With-control: 0 of 4. `high_priority()` returns
both with `picked: None` ([CHOICE 8]).

**FMR_007 — one of the two priority transports is gated out of the requirement
set by its own honesty.**
Section 2 defines `existing_control` as *"what current practice does about it,
or NONE"*, and `DUR-002` introduces a third value on purpose: *"Score as
PARTIAL, not NONE — this is the null-set discipline in Step 7."* Step 6 gates on
`existing_control = NONE`, so `DUR-002` produces no requirement under a literal
reading, while its own `detection_channel` specifies one (stamped validity
envelope plus a RETURN CONTRACT). `step6_requirements()` reports it in
`excluded` with `states_requirement_anyway: True` rather than dropping it.

**FMR_008 — Step 6's second conjunct has no test anywhere in the order.**
The gate is *"existing_control = NONE and consequence non-trivial."* The order
states no scale, no threshold and no comparison for the second. The gate runs on
the first alone and the second is returned NOT_EVALUABLE per entry rather than
assumed met ([CHOICE 6]).

**FMR_009 — three of the order's own rules jointly forbid Step 4 on a short
register.**
Section 2 caps the PROJECTED share at a stated fraction; Step 4 says populate
section 3C and *"flag all as PROJECTED"*; section 8 says the register is
expected to be short and *"a long one is a warning sign, not a result."* With
k non-projected entries the cap is `f·k/(1−f)` — at k=4 and f=0.2, **one entry**.
`fraction_cap` is registered in `tools/known_answer.py` with four
distinct-valued cases. Step 4 is NOT_RUN and none is authored here, because
authoring projected entries from inside is exactly what `F_D` names.

**FMR_010 — F_D passes because Step 4 was not run, not because projection was
resisted.**
`projected_fraction()` is 0.0 of 4. Recorded so the zero is not read as a
result about the register's discipline.

**FMR_011 — F_C's random 20 percent is 0.8 of an entry.**
`F_C` asks for *"a random 20% of entries"* audited against the three mandatory
fields, and a rejection rate computed from n < 1 has no resolution. A full
census is run instead and the substitution is stated on the render rather than
taken quietly: 0 rejected of 4, every entry carrying a mechanism, a detection
channel and a consequence.

**FMR_012 — ENTRY 0 is named by the order, was not delivered, and is not
constructible under the order's own schema.**
Section 1: *"ENTRY 0 OF THE REGISTER IS THE DETECTION GAP ITSELF."* No `ENTRY`
block for it exists. It is not authored here and the reason is structural
rather than a preference: its mechanism is a property of the register rather
than of a deployment, so it has no `load_condition`, and its `detection_channel`
is the field itself. The record-level refusal shape recorded at
`uninstrumented` `UNI_095`. `entry_zero()` reports it absent; `DUR-000` appears
in neither module, asserted.

**FMR_013 — `NOTE` is used by half the register and is not a field.**
`DUR-003` and `DUR-004` each carry a `NOTE`. Section 2 lists twelve fields and
has a state for an entry MISSING one (*"an UNRATED PART... filed as such, not
discarded"*) and no state for an entry carrying an EXTRA one. `filing()` reports
`extra` on its own line and never merges it into `missing`, because a field the
schema lacks and a field the entry lacks are different facts. The `GM_011`
shape.

**FMR_014 — DUR-004 carries MEASURED's label with neither MEASURED's cite nor
TRANSPORTED's justification, and the word the transport rule rejects.**
Section 2: `MEASURED (cite)` and `TRANSPORTED (name source domain + justify)`.
`DUR-004` reads *"MEASURED by analogy in software generally"* — no cite, no
`TRANSPORT JUSTIFICATION`, no source domain named, and the TRANSPORT RULE says
in as many words *"Transports that rest only on analogy are rejected at
review."* The direction matters: it inflates evidence strength on the one entry
whose own `existing_control` is NONE. `evidence_class_audit()` returns
`meets_label: False` with the reason. The mechanical vocabulary check in
`conformance()` **passes** this cell, because a label is not a requirement —
the check's own limit shown rather than described.

**FMR_015 — this build's own F_A screen struck the entry that disclaims
resemblance, on the sentence disclaiming it.**
The first version required structural language AND no resemblance marker.
`DUR-001` states *"This is not resemblance between industries; it is the same
insufficiency and the same closure"* — and the `resembl` marker fired on the
disclaimer, removing the strongest transport in the register from the survivor
set. The `UNI_009` / `T1-1` shape, committed after both were recorded here.
Repaired: survivors turn on structural language and a stated justification; a
resemblance mention is reported **with its surrounding clause** and is not
subtracted. `F_A`'s `limit` field carries the record so the repair is not
silent. Three of three transports survive.

**FMR_016 — the order's own "roughly fifty" is the low end of its own band.**
Section 6B delivers classical at ~20 hops over 500 years and ML at ~20–50 hops
over 10 years, then states *"SAME N. Compressed by roughly fifty."* Computed:
classical 0.04 hops/yr, ML 2.0–5.0 hops/yr, a band of **50 to 125**. Fifty is
the equal-N reading and the conservative end, not the midpoint.

**FMR_017 — F_I is enforced by there being no single-number accessor.**
Section 6B-2: *"Check both appear together or neither does."*
`volume_vs_correlation()` returns both; no `volume()` or `expected_losses()`
accessor exists on the module, asserted from the AST, so a caller wanting the
volume figure alone has to build the product itself and it is visible in a diff.
Section 6B-2 also says correlation *"needs its own entry"* and none was
delivered; that is reported as `correlation_entry_exists: False` and no entry is
authored.

**FMR_018 — the REGISTER RULE is the sibling's n_eff, imported.**
Section 6B-2: *"any entry claiming redundancy as an existing_control must state
what the redundant copies DO NOT SHARE. Copies on the same platform, in the same
format, under the same dependency stack are one copy."* That is exactly
`effective-redundancy-audit`'s `Channel.survives_all_shared_nodes` and its
`n_eff`, so the arithmetic is imported rather than restated — five stale copies
of one gate across three drops is this repo's measurement of what restating
costs (`MF_019`). A copy that does not state what it does not share makes the
claim UNRATED: not scored as shared, which would be a measurement, and not
scored as independent, which is the claim under test. It fires on **nothing** in
the delivered register (0 of 4), reported as a visible zero and shown reachable
in both directions on constructed claims.

**FMR_019 — a scheduled shock with an undeclared budget is a third state.**
Section 6B-3: *"A planned shock with no budget line behaves exactly like an
unplanned one."* So `scheduled` mitigates nothing on its own. `shock_split()`
takes budget lines as a caller-declared argument and keeps three states apart —
declared budget (mitigated), declared absence (not mitigated, per the order's
rule), and UNDECLARED (undetermined), because an undeclared budget is not a
missing one. Both declared branches are exercised.

**FMR_020 — F_G cannot run here, and its proxy is labelled a proxy.**
`F_G` asks that the schema be handed to a reader outside the domain who
classifies five entries. There is no second reader, and the order asks for five
entries where four were delivered — both blockers are returned. The computable
proxy: a field whose delivered values do not conform to its own declared
vocabulary is underspecified by the order's own test and needs no second reader.
It flags exactly `reconstruction` and `evidence_class`.

**FMR_021 — F_E is a claim about the world and is stated rather than measured.**
*"The deliverable must state what would make it binding... If the honest answer
is 'nothing currently would,' that is the finding."* The answer returned is that
one: bridge codes became mandatory because failures were attributable and
expensive, and the entries here are selected for producing no attributable
event. `claims_publishing_sufficient` is `False`, asserted.

**FMR_022 — F_F: no entry names a where.**
*"Any entry that assumes something recoverable exists must name what and
where."* Three entries name WHAT (a probe-response record, a hop log, a stamped
envelope). One names a holder (*"a party that is not the operator"*). **None**
names a location. Reported per entry rather than as a rate.

**FMR_023 — the two cross-references the order asks for resolve unevenly.**
Section 6B-2 asks for the correlated-failure-at-scale marker: RESOLVED to
`effective-redundancy-audit` and `design-basis-ai`, both holding a shared-node
account of nominally independent channels, and the first supplying the `n_eff`
this module imports. Section 5 asks for the silent-substitution marker:
**AMBIGUOUS** across `model-provenance`, `criteria-drift` and
`machine-record-format`, candidates named and **no pick made**, since picking
one would put a citation in the author's mouth.

**FMR_024 — two delivery facts recorded as delivered, not repaired.**
Section 3B-W's header says *"the two priority transports, schema filled"* and
delivers four entries, one of which (`DUR-004`) is not a transport at all.
Section 7 lists `F_I` before `F_H`. Both are kept in delivered order; the
falsifier report prints `F_I` before `F_H` and a check asserts it.

**FMR_025 — UNVERIFIED, and it covers the folder.**
No deployed ML component was inspected, no retained record examined, no
reconstruction attempted, no probe run, no hop log read. The register's content
is the four entries the order delivered and nothing else; every computation here
is a property of those entries, of the order's own rules, or of this build's
arithmetic. `FMR_001` is the load-bearing part of that: with Step 0 blocked, it
is not established that the enumeration is not already written somewhere else.
FALSIFIER: run Step 0, fix a deployment class under Step 1, and score one real
deployment.

---

# THE REVISED ORDER — `WORK_ORDER_V2.md`

Every number below is printed by `python3 register_v2.py` and pinned by
`python3 test_register_v2.py`. Neither order is edited. Nothing here rates
any firm, product, arrangement or person, and no function takes an entity
as an argument.

---

**FMR_026 — the revision is purely additive, measured.**
SUPPORTED, by difflib rather than by reading: **694 lines inserted, 0
deleted, 0 replaced**. Four falsifiers are added (`F_K`, `F_M`, `F_L`,
`F_J`), every v1 falsifier body survives verbatim, and v1's `F_I`-before-
`F_H` ordering (`FMR_024`) is carried unchanged rather than tidied. A
revision that quotes or re-renders an earlier document is a COPY and
copies drift (`OE_011`, `DBK_010`, `MI_011`, `CAC_9`); here none did.

---

**FMR_027 — the amended map gives four protective variables and F3 names two.**
SUPPORTED, computed.

    amended protective set   V5  V7  V9  V13
    F3 names as wins             V7      V13
    unaccounted              V5          V9

`V9` is argued away **by name** in F2 — *the protective variable is maxed
and does not protect*. **`V5` is left out by nothing stated anywhere.**
Section 1B's own rule is that the amended score is authoritative and the
original is retained, which is what makes this checkable at all.

---

**FMR_028 — and V5 is where A-01's correction was not applied.**
SUPPORTED, from the delivered text.

`A-01` is a definitional correction: *a carrier is not someone in the
field, a carrier is SOMEONE WHO CAN READ THE REPRESENTATION*. It is
applied to `V3`. `V5`'s own gloss is **REGENERATION CYCLE — how often it
is actually RE-TAUGHT or re-performed**, which is the same carrier-side
reading, and it still scores `+` on *continuous*. `DUR-004` STRANDED
UNDER LOAD is precisely the state where execution is continuous and the
carrier population has gone to near zero. So `V5`'s `+` scores machine
re-execution, not carrier re-performance — the same slip `A-01` fixed,
in the variable next to it.

FALSIFIER: a reading of `V5` on which continuous execution is
re-performance in the sense the gloss states.

---

**FMR_029 — F_L states a direction and the direction is backwards.**
SUPPORTED, provably, and it changes no conclusion.

Under any model preserving the marginals, survival is non-decreasing in
correlation. For the model used here — with probability `rho` all `n`
terms take one common draw, otherwise they draw independently; marginals
exactly `p`, pairwise correlation exactly `rho` — the derivative is
`p - p^n >= 0`. So joint FAILURE is non-increasing:

    p = 0.9, n = 7     rho 0.00   failure 0.5217
                       rho 0.50   failure 0.3109
                       rho 1.00   failure 0.1000

`F_L` says *Correlation makes the joint failure probability HIGHER than
the naive product of independent terms*. On the like-for-like reading
that is backwards at every parameter. On the cross-type reading — a
failure probability against a survival product — it is true at 1 of 5
sweep points, so it is not a general claim either. Neither reading
rescues it.

**`A-07` states the same correction WITHOUT a direction and is right**,
and §9 is the authoritative record by the order's own rule. The
conclusion is untouched: it rests on the inability to ENSURE each term,
not on arithmetic, and `F_L`'s own last line — *do not put a number on
it* — is followed here, the model existing to check a direction and
nothing else. The correction cuts against the naive case rather than for
it: the independent product OVERSTATES the case against a single
custodian.

---

**FMR_030 — F_K cannot be applied to the set it bounds.**
SUPPORTED, computed. `F_K` admits a condition *only if its expected
lifetime is within the retention horizon being claimed*, and the order
states neither quantity: **0 of 7** artifact-side conditions carry an
expected lifetime, though the prose says each has one, and *retention
horizon* appears 4 times carrying no value. State
`NOT_APPLICABLE_AS_DELIVERED`. The `MF_017` shape — a stated rule with
no field — on a falsifier rather than a field.

---

**FMR_031 — F_M empties the candidate set delivered with it.**
SUPPORTED, and it is the headline of the revision.

`F_M` admits a carrier-side condition only with (a) a named producing
mechanism and (b) a currently measurable production rate. On
`DUR-005-B`'s own five candidates, **0 of 5 state a rate value**; exactly
one names a rate in words (*at replacement rate*) with no value. So the
**active carrier-side set is empty**, and the falsifier and the set it
empties are delivered in the same document.

`DUR-005-C` states its own `CONSTANT_FIRES` property and calls it
intended — *the screen has no null result, every capacity scores PRODUCED
or FLAGGED, nothing scores clean*. The two are not contradictory; they
are two stages, and what they produce together on the delivered set is:
the screen admits everything, `F_M` admits none of it.

FALSIFIER: a production rate, with a value, for any one of the five.

---

**FMR_032 — Step 5 recounted on six entries, and the axes still do not merge.**
SUPPORTED.

    single-valued   3 of 6   DUR-004, DUR-005, DUR-006   all NO
    multi-valued    2 of 6   DUR-001, DUR-003
    no value        1 of 6   DUR-002

`FMR_003`'s finding improves from 1-of-4 to 3-of-6 and its structural
half stands: the two multi-valued cells vary along **different axes** —
`DUR-001` on control state (without / with the control), `DUR-003` on
time (degrades from PARTIAL toward NO) — so no merged distribution is
emitted, one count over both being a count across unlike objects.

---

**FMR_033 — the register sits exactly at the PROJECTED cap.**
SUPPORTED. One entry states `PROJECTED` (`DUR-005`, alongside MEASURED),
five do not, and `fraction_cap(5, 0.2)` is 1 — so the register is AT the
cap and a seventh projected entry would breach a fraction the order
declines to state. The cap is imported from `register.py`, not
reimplemented. Two entries state more than one evidence class where §2
defines one of three (`DUR-001`, `DUR-005`).

---

**FMR_034 — F_J directs a marking at entries that do not exist.**
SUPPORTED. `F_J` says *mark every 6C entry evidence_class = PROJECTED*.
Section 6C carries **7 subsections and 0 ENTRY blocks**, and §9-1
separately records that PROVENANCE REGRESS has no entry. Of the five
still-open items, three name a missing entry.

---

**FMR_035 — the amendment record is complete, and it is what makes the rest checkable.**
SUPPORTED. Eleven amendments, all eleven carrying `superseded`,
`replacement`, `forcing case` and `consequence`; §9's own rule is that
silent overwrite is not permitted and a withdrawn claim stays visible.
`FMR_027` and `FMR_029` are both only reachable because the superseded
statements are retained.

---

**FMR_036 — three defects in this build, all found by running.**
SUPPORTED. Recorded rather than quietly fixed.

1. `amended_scores` read the amendment cell with `lstrip("-> ")`. `lstrip`
   takes a CHARACTER SET, so on `-> --   A-01` it strips the value's own
   leading `--` and returned the **unamended** score — on the map whose
   rule is that the amended score is authoritative.
2. `F_K`'s first check used a bare numeral test and scored
   `(see DUR-006)` as a stated lifetime and `exceeds ~1` as a retention
   horizon value. Both false positives ran toward reporting the bound as
   APPLICABLE. Repaired with numeral-adjacent-to-a-time-unit, pinned in
   both directions. The `UNI_009` / `T1-1` lexical-proxy shape.
3. The `joint_survival` registration landed as dead code inside a helper
   after its `finally`, so the metric count did not move — the **second**
   instance of that in `tools/known_answer.py` in this folder's history.

---

**FMR_037 — DUR-006-C stated as arithmetic.**
SUPPORTED. Seven terms at `p = 0.90` give a conjunction survival of
`0.4783`; four holders at `q = 0.50` give a disjunction survival of
`0.9375`. The distributed arrangement is modelled with a **lower**
per-holder number and survives more often — *the difference between a
product of probabilities and a complement of a product*, and it does not
depend on the values. The term count and the mode count come from the
order's own tables (7 and 6), not from literals here.

---

**FMR_038 — the v1 readings v2 does not move.**
SUPPORTED. Section 6B parses byte-identically in both, so `FMR_016`
carries unchanged: *compressed by roughly fifty* is the LOW end of its
own band (50 to 125) and the equal-N reading. Nothing in the revision
touches it.

---

**FMR_039 — UNVERIFIED, and it covers the revision too.**
No deployed component was inspected and no entity was rated. The
probability model is named in `[CHOICE 9]`, its parameters are returned
alongside every value, no function takes an entity as an argument, and
`F_L`'s instruction to put no number on the conjunction is followed.
`FMR_025` stands: with Step 0 blocked, it is still not established that
this enumeration is not already written somewhere else, and the revision
does not change that.

---

## THE VALUE-AND-SOURCE GATE — `tools/sourced.py`

The three defects at `FMR_036` are one defect. Each produced a value whose
stated source does not support it, and none was found by reading the code.
The general repair is a shared primitive rather than three patches: three
fields on every extracted value — the **value**, the **literal source
text**, the **locator** (which document, which line, which columns) — and
one gate returning `UNRATED` for anything lacking all three. Not zero, not
clean, not a default.

---

**FMR_040 — containment is not sufficient, and the V6 row proves it.**
SUPPORTED, and it is the design decision the primitive turns on. The
obvious rule is that the value must appear somewhere in the source text.
On `V3` it works: the buggy value `+` does not occur in `-> --   A-01`.
On `V6` it fails: the buggy value `-` **does** occur in `-> --   A-02`,
through the hyphen of the arrow and the hyphen of the amendment id. So the
primitive is a **span** — offsets into the source text, verified by
slicing — and under the buggy path no span exists at all, because the
value was never located in the cell it names as its source. Both rows
refuse for the same reason, `no_provenance`, rather than one refusing by
luck. A value that is COMPUTED declares a `derivation` instead; exactly
one of the two, never both and never neither.

---

**FMR_041 — the three defects replayed, each returning `UNRATED`.**
SUPPORTED, in `test_register_v2.py` section 17 rather than in prose.
(1) `amended_scores` now slices the amendment cell and the sliced value
cannot disagree with its own span; a row with no amendment keeps the ML
cell as the source of its authoritative score rather than being
re-attributed to a cell it did not come from, which is the defect. The
`lstrip` check is read from the **AST**, because a substring scan fires on
the docstring in which the function names the construct it refuses —
`UNI_009`/`T1-1` inside the checker written against it — and it is
null-tested with a planted `lstrip`. (2) `_has_duration` delegates to
`numeral_with_unit`, so `(see DUR-006)` and `exceeds ~1` return a refusal
naming `no_unit_adjacent_to_numeral` rather than a `False` that reads like
a measurement, and `F_K`'s reading is unchanged: 0 of 7 conditions carry a
lifetime, now with seven stated reasons. (3) `tools/known_answer.py`
declares `EXPECTED_METRICS` and asserts it against the registry at end of
run; a count taken from the `register(...)` calls cannot catch a call that
did not execute, because the call is not there to be counted.

---

**FMR_042 — a fourth defect, found BY the gate and not by reading.**
SUPPORTED. The `V2` row of the loss-variable map runs its ML cell past
column 57, so the fixed-width slice **cuts a token**: the ML cell is
truncated at `data st` and the amendment column reads `ate, hw)` — text
belonging to the cell on its left. One row of fourteen, cutting on both
sides of the same boundary. A locator is a CLAIM about where a cell ends,
and a boundary falling inside a token makes the claim false, so
`Locator.boundary_clean` reports it and every row carries the finding.
**No published score moves** — the truncated cell begins with the same
sign run the full cell does — so what is false is the LOCATOR and not the
value, which is exactly the class an output check cannot see. The spill is
filed `UNPARSED` and kept apart from `EMPTY`: a cell holding text that is
not an amendment is a different finding from a cell holding nothing. The
check is not `CONSTANT_FIRES` — thirteen rows are clean.

---

**FMR_043 — what the gate does not do.**
It does not check that the source is TRUE, or that the locator points at
the right cell. It checks that the three fields are mutually consistent. A
locator naming the wrong line, with source text copied from that same
wrong line, passes; `boundary_clean` addresses one narrow form of that
(a column boundary cutting a token) and nothing addresses the rest. The
numeral rule is a word list of time units, stated at the top of the module
rather than the bottom, and a paraphrase steps around it. 41 checks in
`tools/sourced.py --selftest`, plus 20 in `tests/test_sourced.py` and 20
in section 17.

---

## WORK_ORDER_V3.md — the third order

`FMR_044..FMR_056`. The order is landed verbatim beside the first two.
Every number is printed by `python3 register_v3.py` and pinned by
`python3 test_register_v3.py`, which prints its own check count.

---

**FMR_044 — v3 is a rewrite, and it is shorter while carrying more.**
SUPPORTED, measured with `difflib` rather than described. v2 against v1
was a pure insertion — 694 lines in, 0 out. v3 against v2 is **338 equal
lines, 122 inserted, 54 deleted, 1072 replaced, similarity 0.2911**, and
**1104 lines against v2's 1218**: shorter, while carrying three sections
v2 does not have (`0-1` the prior-art result, `0-2` ENTRY 0, `6` the
parser gate) and six numbered subsections under compounding where v2 had
seven unnumbered. So prose was compressed rather than added to, which is
the order's own `EXPECTED YIELD` rule — *"The register is expected to be
SHORT. A long one is a warning sign, not a result"* — applied to the
order rather than to the register.

---

**FMR_045 — Step 0 is reported RUN, and the report is not verifiable from
here.** `FMR_001` held the register NOT CLEARED TO SHIP because the
prior-art gate had not been run and `step0_prior_art()` returned BLOCKED.
v3 §0-1 reports it run on 2026-09-13, tables **four adjacent artifacts**,
marks one `CLOSEST PRIOR ART. CITE.`, and states `GATE RESULT: not
redundant. Residual scope is custody, identifiability, reconstruction.`
Step 0 in the procedure now reads `DONE`. **The blocker is removed by the
order's own report**, and the report is `NOT_VERIFIABLE_HERE`:
`arxiv.org` and `export.arxiv.org` both refuse CONNECT with 403 (measured
2026-09-14T00:57Z; `github.com` reaches its origin and is the connecting
control), and no probe runs at audit time because no network is a house
rule. So the closure is **by declaration** — and the order says so
itself, in the same paragraph: *"Verify before citing."* `[CHOICE 12]`.
`FMR_001` is SUPERSEDED, not refuted: what it recorded was that Step 0
had not been run, and it has now been reported run by the only party who
could run it.

---

**FMR_046 — the four-protective-variables reading survives the rewrite
unchanged.** SUPPORTED. F3 names two wins after amendment (`V7`, `V13`)
and the amended map computes **four** (`V5`, `V7`, `V9`, `V13`). `F2`
argues `V9` away by name — *"the protective variable is maxed and does
not protect"* — and **nothing anywhere in the order argues `V5` away**.
This is `FMR_027` recomputed on a document that shares 338 lines with the
one it was found in; the finding did not move, and neither did the gloss
it turns on. `FMR_028` also stands: `A-01` redefines a carrier as
**SOMEONE WHO CAN READ THE REPRESENTATION**, `V5`'s gloss still counts
**re-teaching and re-performance**, and `DUR-004 STRANDED UNDER LOAD` is
precisely the state where performance is continuous and reading is gone
— *"Artifact present, demand maximal, comprehension absent."* The same
slip `A-01` repairs, one variable over, in a register whose own entry
names the state it produces. One further loss in the rewrite: v2's
definition fence carried `(see A-01)`, `(see A-02)`, `(see A-03)` back-
references on the three amended variables and v3's does not, so the
amendment is reachable from the score column and no longer from the
gloss.

---

**FMR_047 — the column-boundary defect recurs, and a second instance
arrives in the section v3 adds.** SUPPORTED. The `V2` row of the loss-
variable map still runs its ML cell past column 57, so the fixed-width
slice cuts a token and the amendment cell files `UNPARSED` — `FMR_042`,
unmoved. New: §0-1's prior-art table has the same shape, and one of its
lines cuts on both sides of the boundary at column 66 — the `scope` cell
reads `-> ambient-adjacent, see DUR-` and the `misses` cell reads `005`,
so a cross-reference is truncated mid-token and its right-hand neighbour
is prefixed with somebody else's text. **Found by the same check on new
material**, which is what a boundary rule is for: the first instance was
found by the gate rather than by reading, and so was this one. 1 of 14
score rows and 2 of 18 prior-art lines; the check is not
`CONSTANT_FIRES`.

---

**FMR_048 — the id moved out of the fence, and the order's own UNRATED
PART rule now fires on 6 of 6 entries.** SUPPORTED. §2 declares twelve
fields, the first of which is `id`. v3 delivers every entry as a
`### DUR-00n — TITLE` heading followed by a fence that begins at
`mechanism`, so **each block carries eleven of twelve and it is the same
field missing on all six**. §2's rule is *"An entry missing any field is
an UNRATED PART, filed as such, not discarded"*, and read literally the
whole register is UNRATED PARTs against a **format change rather than an
omission** — the id is present, in the heading, where a parser reading
the fence alone cannot see it. One line of §2 closes it either way
(restore the field, or say the heading carries it). The rewrite does
close `FMR_013`: v2 carried a `NOTE` field used by half the register and
absent from the schema, and v3 moves every note outside the fence, so no
block now carries a field the schema does not declare.

---

**FMR_049 — §6 is this session's own repair delivered back as a control,
and it restates it one field short.** SUPPORTED, and it is the sharpest
result in this pass. §6 THE PARSER GATE states the rule this repository
implemented in `tools/sourced.py` two commits earlier: a value and its
source travel together, **THREE FIELDS** (the value, the literal source
text, the locator), **ONE GATE** returning UNRATED — *"not zero, not
clean, not a default"* — plus the numeral rule and the completeness
assert. All four of those hold of the implementation and are checked
against it. The gate takes **four** requirements, not three: value,
source text, locator, and a **span** (offsets into the source text,
verified by slicing) or an explicit derivation. `span` and `offset`
appear **zero times** in §6.

That omission is demonstrable rather than pedantic, and the demonstration
returns **three readings of the same two rows**:

```
row  amendment cell   buggy  true   containment  searched span   produced span
V3   '-> --   A-01'   '+'    '--'   refuses      refuses         no_provenance
V6   '-> --   A-02'   '-'    '--'   passes       passes at (0,1) no_provenance
```

CONTAINMENT — the value appears somewhere in the source text — is what
§6's three fields buy, and it **misses V6**, where the buggy `-` occurs
in the cell through the hyphen of the arrow. A SEARCHED SPAN — locate the
value afterwards and record where — also misses V6, and points at
**offset 0, the arrow**, where the score sits at offset 3: a span found
after the fact can name the wrong occurrence. What refuses both rows is a
span **PRODUCED BY THE EXTRACTION**, because the buggy path never located
the value in the amendment cell at all and has no offsets to offer.
§6 names neither the span nor where it has to come from. `[CHOICE 14]`.

---

**FMR_050 — Step 6's first conjunct is an equality against a free-text
field.** SUPPORTED. Step 6 gates on `existing_control = NONE`, and
`existing_control` is prose with no declared vocabulary — the six
delivered cells lead with `NONE` five times and `PARTIAL` once. Read off
the head token, Step 6 gates in five entries and excludes `DUR-002`,
which scores PARTIAL deliberately (*"null-set discipline"*) and states a
requirement anyway — `FMR_007`, recurring. Read by whole-word scan for
`NONE`, it gates in **six**, because `DUR-002`'s own cell reads *"Scored
PARTIAL, not NONE"*: the word is there, in the sentence saying it does
not apply. The lexical-proxy shape (`UNI_009`, `T1-1`), avoided here
rather than found, and reported as a measured false positive.
`FMR_008` stands unchanged: the second conjunct, *consequence
non-trivial*, has **no scale, no threshold and no comparison anywhere in
the order**, so it returns `NOT_EVALUABLE` per entry and the gate runs on
the first conjunct alone.

---

**FMR_051 — F_D asks for the fraction in the header and the header does
not carry one.** SUPPORTED. `F_D` reads *"State the fraction in the
header"*, and the header states `draft register, six entries, prior-art
gate passed.` — an entry count and a gate status, no fraction. The count
itself checks out (six stated, six delivered). The recount is unchanged
from `FMR_033`: **1 PROJECTED of 6**, cap 1 at `register.py`'s
`[CHOICE 7]` fraction of 0.2, so the register sits **exactly at the
cap**. Two entries declare more than one evidence class at once
(`DUR-001` TRANSPORTED and partially MEASURED, `DUR-005` MEASURED
historically and PROJECTED for its own candidate set) and both are
reported as two rather than resolved to one.

---

**FMR_052 — F_J's exemption is named and not exercised.** SUPPORTED.
v2's `F_J` directed a marking at *"every 6C entry"* and §6C carried seven
subsections and zero ENTRY blocks (`FMR_034`). v3 states the marking at
section level instead — *"Mark all of Section 5 PROJECTED unless a
current instance is cited"* — and then names two subsections as
**observable now**. Observable is not cited: §5 carries **six
subsections, zero ENTRY blocks and zero cited instances**, and its one
worked case is introduced as a case (*"Worked case: adjacent segments of
an electrical grid"*) rather than cited as an instance. So under `F_J`'s
own rule all of §5 stays PROJECTED, including the two named, and the
exemption exists in the text without being taken. `[CHOICE 13]`.

---

**FMR_053 — F_L still states a direction, and the direction is still
backwards.** SUPPORTED. `F_L` reads *"Correlation makes joint failure
HIGHER than the naive product"*. Under any model preserving the
marginals, survival is non-decreasing in correlation, so joint failure is
non-**in**creasing: at p=0.9 and n=7 the failure probability runs
**0.5217 → 0.1000** as rho goes 0 to 1. `A-07`, which §10's own
no-silent-overwrite rule makes authoritative, states the same correction
**without a direction** and is right. `FMR_029` unmoved by the rewrite,
and the conclusion is untouched either way: it rests on the inability to
ENSURE each of the seven terms, and `F_L`'s own *"DO NOT PUT A NUMBER ON
IT"* is followed here.

---

**FMR_054 — F_K and F_M are unchanged, and F_M's active set is still
empty.** SUPPORTED. `F_K` bounds the ambient set by expected lifetime
within the retention horizon: **0 of 7** artifact-side conditions state a
lifetime and **no retention horizon carries a value**, so the bound
compares two quantities the order states neither of and returns
`NOT_APPLICABLE_AS_DELIVERED` with seven stated reasons — while the prose
introducing the set says *"each with finite lifetime"*. `F_M` admits a
carrier-side condition only with a named producing mechanism **and** a
currently measurable production rate: **0 of 5** state a rate value, one
names a rate in words (*"at replacement rate"*) and carries none, so the
active set is EMPTY and the falsifier and the set it empties are still
delivered in the same document. `DUR-005-C` states its own
`CONSTANT_FIRES` property — *"The screen has NO NULL RESULT"* — and calls
it intended; v3 capitalises where v2 did not, so the reader is now
case-insensitive.

---

**FMR_055 — one parser, three documents.** SUPPORTED, and checked from
the AST. `entries_v3.py` defines **none** of the cell parsers, the gutter
parser or the fence walker; the gated score map, the column-boundary
report and the F3 reader are `entries_v2.amended_scores_from`,
`vmap_boundary_report_from` and `f3_claim_from`, which were
**generalised to take a document rather than copied** — five stale copies
of one gate across three drops (`MF_006`, `MF_011`, `MF_019`) is what
copying costs, and `tools/check_gate_drift.py` exists to catch exactly
that. The audit's counts and arithmetic come from `register_v2` the same
way. The generalisation moved no reading in v2: its own F3 claim, its own
score map and its own 142 checks are unchanged, and the one check that
had to move is the planted-`lstrip` null test, retargeted at the function
that now carries the body. The two documents word one sentence
differently — v2 *"ORIGINAL FORM of F3 listed"*, v3 *"Original F3
listed"* — so the shared reader takes a tuple of markers and a document
matching neither returns an empty `original_wins` rather than silently
reporting that nothing was withdrawn.

---

**FMR_056 — UNVERIFIED, and it covers the folder.** No deployed
component has been inspected, no retained record examined, no
reconstruction attempted, and **no entity is rated** — no function here
takes an entity as an argument. Every computation is a property of the
three delivered orders, of this build's arithmetic, or of this
repository's own instruments. The four prior-art artifacts are CARRIED
and unread (`FMR_045`); `FMR_025`'s scope statement stands unchanged. The
one thing this pass adds to the standing UNVERIFIED set is that the
register's own ship gate now turns on a claim nobody here can check,
which is a state the order anticipated and labelled.

---

## The fourth order

`WORK_ORDER_V4.md` landed verbatim beside the other three. Claims
`FMR_057..FMR_069` are properties of the v4 instrument and of the
delivered document; the order's own `F_A..F_N` and `D-01..D-10` are
distinct from them. Counts printed by `python3 test_register_v4.py`.

---

**FMR_057 — v4 is a REWRITE of v3, and the longest of the four.** 1104
lines against 1235, **727 equal, 67 inserted, 12 deleted, 534 replaced,
ratio 0.6216**. v2 against v1 was a pure insertion; v3 against v2 was a
rewrite; this is a rewrite too, and unlike v3 it does not compress. The
order's own §9 says the register is expected to be SHORT and that a long
one is a warning sign, which is a statement about ENTRIES and not about
the document: entries stay at six.

---

**FMR_058 — the prior-art gate REOPENS, and `FMR_045` is withdrawn as a
closure.** `FMR_045` recorded v3 reporting Step 0 `DONE` and removing the
ship blocker, which took `FMR_001` off the standing blocker list on the
strength of a report that could not be checked. v4 reverses it: §0-1
reads `STATUS RUN`, `REPORT STATUS NOT_VERIFIABLE_HERE`, `SHIP BLOCKER
FMR_001 OPEN`, and the version line reads `SHIP BLOCKED`. **All three
statements of the gate's status agree** — §0-1, the version line, and
§7's Step 0 — which is what `[CHOICE 5]` reads them apart to establish.
Four artifacts, four UNVERIFIED ids, one marked `CLOSEST PRIOR ART`. So
`FMR_001` is OPEN again by the order's own declaration rather than by
this audit's. arXiv still refuses CONNECT from this environment and
`github.com` is still the control, so the refusal is arXiv-specific and
not general egress failure — the same measurement, now stated in the
document.

---

**FMR_059 — the reversal is in no amendment, and its one
cross-reference points at the wrong one.** §10's own rule is *"Each
entry retains the superseded statement. Silent overwrite is not
permitted; a withdrawn claim is evidence about the method and stays
visible."* A gate status moving `DONE` to `RUN` is a superseded
statement. Of eighteen amendments, **none is about the gate** — the only
one mentioning prior art at all is `A-13`, which is about the table's
format — and the `SHIP BLOCKER` line's own cross-reference reads *"See
A-12"*, which is `ID MOVED OUT OF THE FIELD BLOCK, ALL ENTRIES UNRATED`.
The reversal is recorded in §0-1 and in `D-01`, where a reader looking
for it in the amendment record will not find it. Not a defect in the
reversal, which is the right call; a defect in where it is filed.

---

**FMR_060 — `F3` restated, and V5 is still undisposed.** `FMR_046`
recorded F3 claiming two wins over a table showing four, with `V5`
argued away by nothing. v4's `A-14` restates it: four PROT after
amendment (`V5, V7, V9, V13`), `F2` disposes of `V9`, `F3` claims `V7`
and `V13`, `V5` UNDISPOSED and routed to `D-04`. **The restatement
reproduces from the table** — the recount gives the same four and the
same residue, computed rather than read. What did not move is `V5`
itself: still PROT, still unargued either way, and `D-04` is open by the
order's own admission. The claim is SUPPORTED as a restatement and the
underlying gap is unchanged, which is the honest pair.

---

**FMR_061 — and the block restating it carries an arrow in a status
cell.** §1's format rule, applied one section earlier, is that *no
hyphen, arrow or punctuation glyph appears in any score or status cell*.
F3's own restatement block reads `UNDISPOSED    V5    -> D-04`. The
document-wide scan does not reach it, and the reason is stated rather
than repaired: a two-column fixed-width block and a gutter block are the
same shape, `entries_v4` `[CHOICE 5]` declares the cost, and this is the
instance of it. Reported by name, with the scan's blind spot reported
beside it, rather than tuning a threshold to catch one block.

---

**FMR_062 — `D-06`'s mechanical check is built, and it fires where
`D-06` says it should.** `D-06` asks for *"a mechanical check in the
harness, not a rule in the text."* `format_rule_scan` walks **every**
fixed-width table in the whole document, because the recurrence `D-06`
records was in a table the V-map check did not look at. Run on all three
documents that carry the rule or its defect:

```
       tables  cuts  glyphs  col0 wraps
  v2      2      0      1        3
  v3      3      2      5        3
  v4      5      0      1        3
```

The two v3 cuts are both on **line 50**, across columns `SCOPE` and
`MISSES` — the prior-art table, cutting a cross-reference at `see DUR-`
and prefixing its neighbour with `005`, which is exactly what `D-06`
records. v4 has **zero**. Null-tested in four directions on constructed
documents (a clean table reads clean; a planted cut, a planted arrow and
a planted first-column-only row are each caught), so the v4 zero is a
result and not a silence.

---

**FMR_063 — the glyph class is in v2, v3 and v4 alike, which is `D-06`'s
own finding measured.** §5-1's rate table carries a **hyphenated line
wrap inside a rate cell** (`bound, unsynchro-`) in every version, and
three rows whose first column is filled while every other column is
blank — a first-column wrap and a one-cell row written the same way,
with nothing in the table saying which. Neither was repaired across
three revisions, because the rule was stated in prose and the only check
looked at the V-map. `D-06`'s sentence is *"a format rule stated in prose
does not propagate to new tables"*; this is that, with a denominator.

---

**FMR_064 — `F_N` passes: the rating vector is restored.** `FMR_048`
recorded v3 moving the id into the markdown heading, dropping the `id`
field, and making **every entry an UNRATED PART** under the register's
own rule against a change that altered no content. v4's `A-12` puts the
id back in the field block; `F_N` is the falsifier added so the next
reformat is checked against the vector rather than inspected. Computed on
both documents with the **same rule** (`[CHOICE 2]`), so a difference is
a property of the format and not of two readers: **v3 6 of 6 UNRATED, v4
0 of 6**, with every id matching its own heading. The rule is shown to
reach both verdicts on constructed entries, so neither reading is
structural.

---

**FMR_065 — `note` is declared now. `name` is not.** `A-15` records a
field used without being declared in v2 and then removed in v3 without
the removal being recorded, and repairs it by declaring `note` a
DECLARED OPTIONAL field — present on 5 of 6 entries, absent on the sixth,
firing nothing. `FMR_013` closes on that. **The class does not.** `name`
is carried by **6 of 6** entries, appears in no schema, and is the field
a reader looks up first. Same shape, one field over, in the revision that
names it. It fires no rule either, and correctly so: the UNRATED PART
rule is about absence, not about presence (`[CHOICE 3]`). Eighth
instance in this family of a stated rule with no schema field, and the
first where the missing field is one every entry already uses.

---

**FMR_066 — §6's fourth requirement is stated, and the tool it describes
still cannot enforce it.** `A-18` is this session's own `FMR_049`
delivered back as a control: the three fields buy CONTAINMENT and not
PROVENANCE, a post-hoc span satisfies all three, and the discriminator is
the offset. v4 adds the fourth requirement — *the span must be EMITTED BY
THE EXTRACTION, carrying the offset the extractor read from* — and the
check is run by CONSTRUCTING both spans on the row the defect was first
found on (`[CHOICE 4]`), rather than by reading `tools/sourced.py`:

```
cell                      '-> --   A-02'
searched span             (0, 1)   offset 0     passes the gate
span emitted by the read  (3, 5)   offset 3     passes the gate
```

The order's stated failure signature — *locator resolves to offset 0
while the value sits at offset 3* — reproduces **exactly**. And the gate
passes both, because **provenance is a property of the CONSTRUCTOR and
the gate sees fields**: no check of the three fields can refuse a
searched span, whatever a fourth field is called. `tools/sourced.py`
already ships both constructors (`find_span`, `slice_sourced`); what it
does not do is refuse the searched one. `entries_v4` calls `find_span`
nowhere and `slice_sourced` everywhere, which is the requirement met at
the only layer that can meet it.

---

**FMR_067 — `F_L` prohibits a sign now, and the conclusion is where it
always was.** `FMR_053` recorded `F_L` asserting that correlation makes
joint failure HIGHER, which computing survival across rho does not
support — survival is non-decreasing in correlation, so joint failure is
non-increasing. `A-17` retains the superseded statement, records *found
by: computing survival across rho against the asserted sign*, and widens
the prohibition from a number to **a number and a sign**. `A-07` is
marked *correct as written*, which it was. The `DUR-006-B` conclusion is
unchanged and still rests on the inability to ensure each term.

---

**FMR_068 — the active ambient set is empty, and the header says so.**
`A-16` records both candidate sets having been presented as the ambient
set when neither satisfies the register's own admission rules. v4 marks
them EXCLUDED with the empty columns visible and states `ACTIVE AMBIENT
SET   EMPTY` in the header. The recount agrees through `register_v2`'s
own bounds, imported: **7 artifact-side candidates, every lifetime cell
reading `not stated`, F_K admits 0**; **5 carrier-side candidates, every
rate cell `none` and every mechanism cell `not named`, F_M admits 0**.
Both bounds are shown able to admit something on constructed conditions,
so the zeros are measurements. The falsifiers and the set they empty are
still delivered in one document, which is what makes the reading
checkable from inside it at all. Two smaller readings alongside: the
header states the PROJECTED fraction as a SCOPE rather than a count over
entries, which is what `F_D` asks for and is not the same quantity as the
entry-level recount; and the V-map legend declares three score tokens
while `V14`'s amended cell reads a fourth, `SPLIT`, which is `A-03`'s
split recorded in the amendment record and not in the legend.

---

**FMR_069 — UNVERIFIED, and it covers the folder.** No deployed
component has been inspected, no retained record examined, no
reconstruction attempted, and **no entity is rated** — asserted from the
AST, no function in `register_v4` takes an entity as an argument. Every
computation is a property of the four delivered orders, of this build's
arithmetic, or of this repository's own instruments. The four prior-art
artifacts are CARRIED and unread; `FMR_025`'s scope statement stands
unchanged; and the register's ship gate is blocked again on a claim
nobody here can check, which `D-01` states itself. Nothing is registered
in `tools/known_answer.py` from this build, and the reason is stated
rather than left as an absence: every function here returns a structure
or a declared vocabulary member, and the one counting function's known
answer is the enumeration it walks — the reasoning
`internal-reference-boundary` `IRB_011` records. The classifiers are
null-tested in both directions instead.
