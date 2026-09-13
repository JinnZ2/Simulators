# CLAIM_TABLE.md — failure-mode-register

Claims `FMR_001..FMR_025` are properties of this build and of the delivered
`WORK_ORDER.md`. They are distinct from the order's own `F_A..F_I`, which are
falsifiers the order states; those are reported by `register.falsifier_status()`
and are not renumbered here.

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
