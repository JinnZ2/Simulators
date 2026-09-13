# CLAIM_TABLE.md — failure-mode-register

Claims `FMR_001..FMR_039` are properties of this build and of the two
delivered orders. `FMR_001..FMR_025` read `WORK_ORDER.md`;
`FMR_026..FMR_039` read `WORK_ORDER_V2.md`, the revised order, landed
verbatim beside it so both stay inspectable. They are distinct from the
orders' own `F_A..F_M`, which are falsifiers the orders state; those are
reported by `register.falsifier_status()` and are not renumbered here.

Every number below is printed by `python3 register.py` and pinned by
`python3 test_register.py`. Nothing here is a statement about any deployed ML
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
