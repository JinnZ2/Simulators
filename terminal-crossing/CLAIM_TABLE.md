# CLAIM_TABLE — terminal-crossing

Ids are permanent and are never renumbered. `TCR_*` are claims about THIS
build and its reading of the delivered order; they are distinct from the
order's own numbered steps. Every claim below is checked by
`test_terminal.py` unless its status says otherwise.

---

**TCR_001 — SUPPORTED.** The six conditions are parsed out of the delivered
order at call time and the channel vocabulary is derived from them
mechanically (the first word after `no ` in each bullet, `[CHOICE 2]`), not
assigned in the module.
*Support:* `conditions()` returns six bullets, each occurring verbatim in
`WORK_ORDER.md` whitespace-flattened; an AST walk over the module's string
literals finds no bullet retyped; a document with no `### Conditions`
section raises rather than returning an empty list.
*Falsifier:* a channel id that does not fall out of a bullet, or a bullet
text present as a literal in the module.

**TCR_002 — SUPPORTED, with the counter-reading UNRESOLVED.** The order's
step 1 asks for a medium the six conditions do not cover, and one is
proposed: gravitational coupling. It is named by none of the six and is
closed by no expenditure, so the falsifier moves from UNSATISFIED (stated
conditions, nothing meets them) to **UNSATISFIABLE_IF_COUNTED** — a
different epistemic object, because no search closes it.
*Support:* `covered()` returns no hits; `falsifier_state()` returns
`UNSATISFIABLE_IF_COUNTED`; a shieldable variant returns `UNSATISFIED` and a
variant the six do name returns `COVERED_BY_CONDITIONS`, so the classifier
is not constant.
*Not claimed:* whether gravitational coupling counts as a crossing under the
order's own usage. Both readings are stated in `PROPOSED_SEVENTH` and the
item is carried `UNRESOLVED`; the proposal is held in its own constant and
is never merged into the parsed six (`[CHOICE 5]`).
*Falsifier:* a reading of the order's usage that settles the question, or a
shielding method.

**TCR_003 — SUPPORTED.** The three asymptotes return three distinct
arithmetic shapes and none returns a total of zero. `UNBOUNDED_HORIZON` is a
state carrying `None`, never a large number.
*Support:* `discriminates(_asymptotes())` is true and two identical records
fail it; `shape()` returns `(state, None, None)` off `COMPUTED`; no
asymptote's total is `0.0` while the control's is.
*Reading:* this is the order's *"No instance found. Only asymptotes"* as
arithmetic. It is a property of the CONSTRUCTED rates, not evidence about
any repository, spacecraft or black hole.
*Falsifier:* any of the three totalling zero under its declared rates, or
two of the three sharing a shape.

**TCR_004 — SUPPORTED, and it is reachability and not existence.**
`TERMINAL` is reachable: a constructed control whose six channels are all
`ABSENT_MEASURED` returns it, so the verdict is not `CONSTANT_FIRES`.
*Support:* all three verdicts occur across the corpus.
*Not claimed:* that any terminal system exists. The control is constructed
precisely to show the branch is reachable, which is the opposite of an
instance.
*Falsifier:* a corpus in which `TERMINAL` cannot be returned at all.

**TCR_005 — SUPPORTED.** `UNSEARCHED` is not `ABSENT_MEASURED`, and an
undeclared channel never reads TERMINAL. `expected_crossings` returns `None`
for an absent rate, an unknown unit, an absent horizon and the `UNBOUNDED`
sentinel, and `0.0` for a rate measured at zero (`[CHOICE 1]`, `[CHOICE 3]`).
*Support:* a partially declared system fills the rest `UNSEARCHED` and its
verdict is `NOT_ESTABLISHED`; each `None` branch is checked against the
`0.0` branch.
*Reading:* the standing absent-vs-known-negative repair, on the field where
it decides the verdict — a system nobody searched and a system searched and
found clean would otherwise read alike.
*Falsifier:* any path returning `0` where nothing was measured.

**TCR_006 — SUPPORTED.** The order's three failed candidates carry three
distinct mechanisms over **two** distinct channels — both the A/B test and
the air gap land on `operator` — and three of the six conditions
(`physical`, `shared`, `maintenance`) are exercised by no delivered
candidate.
*Support:* `mechanism_channel_map()` returns 3 and 2 with the collision on
`operator`; `conditions_unexercised()` returns those three.
*Reading:* the order gives all three candidates one verdict (FAILS) and a
different reason for each; the metric records a channel and has no field for
a reason, so what the mapping shows is which of the two a reader keeps. The
mechanism field is this audit's reading and the order's verdict is carried
beside it (`[CHOICE 6]`).
*Falsifier:* a fourth candidate landing on an unexercised condition, or a
reading under which the three mechanisms map one-to-one.

**TCR_007 — DERIVED, not independently checked here.** The order's finding —
*"it is an ACCOUNTING BOUNDARY MISTAKEN FOR A PHYSICAL ONE... cost
comparisons are therefore not comparisons"* — is the VOID RATIO shape
(`reasoning-gate` G-DIM, `measurement-fork`, `declared-frame` `DF_005`)
arriving by a third route: two costs taken over two boundaries are not one
quantity, so the ratio between them is void rather than unfavourable.
*Status:* a cross-reading of the order against instruments already in the
tree. Nothing here recomputes a cost comparison; that is step 3 and it is
NOT RUN.
*Falsifier:* a declined engineering standard whose two costs are shown to
share a boundary.

**TCR_008 — SUPPORTED.** The contamination marker is carried as a third
state, `UNKNOWN`, kept apart from a measured zero and from a measured
crossing, in the order's own words (*"Not resolved in either direction"*).
*Support:* `CONTAMINATION["state"]` is `UNKNOWN` and its order line occurs
verbatim in `WORK_ORDER.md`.
*Falsifier:* the marker resolved in either direction by anything in this
folder.

**TCR_009 — SUPPORTED, and it bounds the order.** Step 4's *"Two searches
did not find one"* is an absence claim with **no corpus and no terms**
stated, which is the `QA_004` status; `SEARCH_STATUS` records both as
`NOT_STATED` rather than treating the absence as a result.
*Support:* the order line occurs verbatim; neither a corpus nor a term list
appears anywhere in the order.
*Reading:* the order's own next sentence is the stronger finding — what was
found instead was evidence the comparison often is not run at all — and that
one does not depend on the search being exhaustive.
*Falsifier:* a corpus and a term list stated for the two searches.

**TCR_010 — UNVERIFIED, and it covers the folder.** Every rate, count and
horizon here is CONSTRUCTED. No cost comparison has been redrawn (step 3),
no search has been rerun (step 4), and nothing in this folder is a statement
about any repository, spacecraft, black hole or organisation. What is
established is that the parser reads the delivered order, that the metric
discriminates the three shapes the order names, and that the proposed
seventh medium is uncovered by the six conditions.
*Falsifier:* step 3 run on one organisation's decision record.
