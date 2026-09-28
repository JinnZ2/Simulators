# FABLE WORK ORDER — 2026-09-27b — Single-channel additions (FWO-8 … FWO-14)

Target: Claude Fable 5.1
Repo: Simulators, branch `claude/coupling-check-disaster-twiklx`, folder `route-independence/`
(JinnZ2/route-independence still 403 on create — build here, promote later)
License: CC0. Python stdlib only. Phone-buildable. No network calls at run time.
Relation to prior orders: EXTENDS FWO-5 (`dependency_chain_audit.py`) and FWO-6 (conversion-point register). Do not rebuild either.

---

## STANDING RULES (carried verbatim from prior orders)

- Instruments, not arguments. Nothing in this packet is a conclusion to be supported.
- UNKNOWN is a first-class value. Never coerce it to NO or to a default.
- Keep PARTIAL distinct from NOT_TRANSFERABLE, and ABSENT_FIELD distinct from NO.
- SOURCE on every demo value. A value with no source is marked UNSOURCED, not filled.
- CARRIED marking on anything taken from an earlier order or file.
- Prior-art check FIRST for every item; record what was searched and what was found, including nothing.
- No characterization of any person, in any file.
- Expected demo structure stated IN ADVANCE, so the demo can fail.

## NEW STANDING RULE (this packet) — the key-holder rule

Finding from the FWO-5 first run: every prediction held, but the same agent wrote the demo inputs and the expected bands. A prediction scored against inputs its author also coded measures agreement with itself.

For every instrument in this packet:

1. Write the EXPECTED block and commit it BEFORE any demo input is coded. Record the commit id in the claim table.
2. Demo inputs must come from an external document with SOURCE, not be constructed to fit.
3. At least ONE fixture per instrument is built to make the check FAIL. A suite with no failing fixture reports `NO_FAIL_FIXTURE` in its summary line.
4. If a prediction holds, the claim table says which of 1–3 were satisfied. "Held" without that is recorded as `HELD_UNINDEPENDENT`.

---

## PROVENANCE KEY

- OBSERVED — reported from direct operation (her material), or measured in a run.
- DERIVED — follows from stated material by a named step.
- PROPOSED — a hypothesis or design choice; may be wrong.
- Her material is tagged OBSERVED where it is a report from operation, including multi-sentence builds where no English term exists.

---

## FWO-8 — Edge taxonomy on the dependency chain

Extend FWO-5's per-route record with two new fields.

**`edge_class`** — how the money medium enters this step (taxonomy CARRIED from a pasted third-party model output; content audited, not authored here):

| class | meaning |
|---|---|
| DIRECT | money is physically required for the transformation |
| INSTITUTIONAL | physically possible without money; a rule requires it |
| ACCESS | resource exists; access is monetarily gated |
| MEASUREMENT | money decides what is counted, funded, sampled |
| TEMPORAL | money decides whether time can be allocated |
| RECURSIVE | money required to produce the mechanism that produces money |
| UNKNOWN | — |

**`coupling_side`** — PROPOSED, new:

| value | meaning |
|---|---|
| SURVIVAL | money reaches the person's needs; the choice of work is untouched (early Unix/Linux volunteers paid by a separate job) |
| SELECTION | money reaches the choice of what to work on |
| BOTH | — |
| UNKNOWN | — |

Hard constraint: a route coupled on SURVIVAL only is scored independent at the selection layer. Do not merge the two sides into one coupling score. (This is the meld found in the C_A coefficient: counting any path to money scores almost everything as coupled and discriminates nothing.)

Expected (PROPOSED, commit before coding): `DIRECT` comes back empty or near-empty across all three FWO-5 demos. Money is not a physical input to any transformation. If a DIRECT row appears, record exactly what it is.

Re-run the three FWO-5 cases under the new fields. Report where FWO-5's two-layer schema (account / settlement) mis-placed a conversion. The first run showed `input_purchase` leading `settlement` 3:1 in case (c), which the two-layer schema had no slot for.

Carried question: FWO-5 case (b) read 0.200. Name the independent dependency, or dependencies. That row is the interesting one by the order's own rule.

---

## FWO-9 — Question-space column

For each conversion point found in FWO-5/FWO-6/FWO-8, add a column listing the class of question that stops being askable at that point.

Candidate classes (PROPOSED, extend or replace):

- instrument needing no funder;
- result with no product downstream;
- timescale longer than any grant or contract cycle;
- question whose answer would reduce demand for the funder's output;
- question arising only from a constraint the funded population does not live under.

That last class is carried from her material (OBSERVED): what gets experimented on is set by which constraints the person has actually run. Cold at sixty below, hunger, direct threat all generate a different problem list than provided conditions do.

Output: per conversion point, the classes it closes, with UNKNOWN allowed. The tool does not estimate how much was lost. It records where the door is.

---

## FWO-10 — Three-standards register

One row per field whose OWN written standard addresses single-channel or single-path dependency.

| field | standard (to be sourced) | what it requires | applied to the monetary medium? |
|---|---|---|---|
| structural engineering | redundancy / fracture-critical single-load-path designation; independent inspection | second load path, or mandated inspection regime | ? |
| negotiation / mediation / diplomacy | durability of settlements; expanding issues beyond one dimension | more than one channel of exchange | ? |
| ecology / agronomy | monoculture vulnerability; genetic diversity requirements | diversity at the dependency layer | ? |

Expected (PROPOSED): the last column reads NOT_APPLIED in all three rows. If any field has applied its own standard to the medium, that source is the finding.

Add rows for any other field found with a written single-path standard (reliability engineering common-mode failure, power grid N-1, aviation dual systems). Prior-art check: has anyone applied a common-mode / N-1 criterion to a currency or payment system? Record what is found, including central-bank payment-system resilience literature, and state whether it addresses the medium or only the plumbing.

Carried from her material (OBSERVED): the inspector is paid through the same path as the structure inspected.

---

## FWO-11 — Lag count

Cases where a system operating under direct constraint produced a result, and the funding-coupled system later reached it late, partially, or not at all.

Record per case: what was produced; by whom (population, not person); approximate date; date the coupled system reached equivalent; `reached` = FULL / PARTIAL / NOT_REACHED / RECOVERED_NOT_REDISCOVERED / UNKNOWN; SOURCE.

Seed cases (from her list; verify, do not assume):

- terra preta vs biochar reconstruction;
- willow bark / salicylates vs aspirin;
- the Antikythera mechanism (RECOVERED_NOT_REDISCOVERED is the expected class);
- aqueducts;
- bamboo gas piping;
- Machu Picchu drainage/terracing.

Known weakness (DERIVED): the record is survivor-filtered. Only what lasted or was recovered can be counted. State this in every output header.

Her selector for contemporary material (OBSERVED), usable to reduce survivor bias: anything not patented, not sold, not produced for revenue. Apply it, and check the settlement layer with FWO-5 before marking anything independent.

The output is a lag distribution, not an impossibility claim. The strong counterfactual ("none of it would exist inside") is unrunnable; the lag is countable.

---

## FWO-12 — Unpaid maintenance as the discretionary-effort measure

Design plus prior-art check. Run only if a public dataset is found.

Measurand (her material, OBSERVED): fixing tools, machines or processes that are not yours, that nobody asked you to fix, and that return nothing under the wage token.

Why this one (DERIVED): it is high value to the plant, invisible in pay records, and entirely voluntary. That makes it the cleanest indicator of whether anything flows outside the token.

Prior-art check: does the employee-engagement or discretionary-effort literature COUNT behavior, or only survey attitude? Expected (PROPOSED): attitude by survey only.

Candidate sources: CMMS/maintenance work-order logs with requester ≠ assignee ≠ asset owner; unplanned-repair records; suggestion-system logs.

Also record her mechanism statement (OBSERVED, energetic, not moral): if the token is the only return and effort above the token threshold returns nothing, conservation of energy selects for effort at the threshold. The measured "disengagement" is the correct solution to the payoff structure. Testable prediction (PROPOSED): unpaid maintenance falls as token-coupling rises.

Measured anchor already found (CARRIED, web search 2026-09-27, citations in session): Linux kernel volunteer share fell from about 15% to about 6%; corporate-authored commits were 84.3% in 2025. Not yet split by whether the employer had a stake in the subsystem. That split is the selection-side test.

---

## FWO-13 — The tax step as its own conversion point

Register the tax step as a named conversion point with its own row type.

Appearances so far:

| # | route | how the tax step converts it | provenance |
|---|---|---|---|
| 1 | barter for materials | taxable event; settlement requires money | OBSERVED (hers) |
| 2 | non-monetary recognition (gift, meal, gift card) | assigned dollar value, reported as compensation, employer pays to give it | OBSERVED (hers) |
| 3 | volunteer or unpaid repair | candidate only | PROPOSED (Claude's); verify or drop |

Consequence to record (her material, OBSERVED): the cheapest permitted recognition channel is the paycheck. People reachable only through other channels go flat or leave. The remaining population then confirms that money is what motivates people. This is self-validating, and is the same shape as the melds in `meld-as-error-class`.

Prior-art check: fringe-benefit / de minimis rules as a documented constraint on non-monetary recognition. Record what exists and whether anyone has treated it as channel removal rather than compliance.

---

## FWO-14 — Reference-instability series (DESIGN ONLY, nothing run)

Enumerate every redefinition of the monetary unit's anchor, convertibility, or governing regime from 1971 to present, with SOURCE per row: date, what changed, who decided, and what measurement series crossed the change.

Her framing (OBSERVED): a structural reference that changes shape periodically is not a reference. It is like concrete that changes shape mid-span.

Design question: for any long-run series denominated in the unit, how many redefinitions does it cross, and is any series adjusted for them in the way physical metrology adjusts for a change of standard? (Compare `labor-statistic-instrument-drift`: the same instrument-change problem, applied to the unit itself.)

Also design the graph time series G(t) at 1971, 1980, 1990, 2000, 2010, 2020 and 2026 for the dependency topology, to test whether coupling increased, decreased, or changed form. Do not assume the direction.

---

## CARRIED AUDIT QUESTIONS — answer these in the return report

1. Noise branch: were the four local files (`check_claims.py`, `CLAIM_TABLE.md`, `README.md`, RUN_NOTE CHOICE 4) pushed? The remote is code-vs-claims inconsistent until they are.
2. Does any NC check have a fixture built to make it FAIL? The predicted NC tally is all HOLDS.
3. ESP-1: add a sub-period-lead fixture to exercise NC_023. Retune nothing. Record the first-run result as a finding before any repair.
4. FWO-5 case (b): which dependency read INDEPENDENT?
5. Restore the CC0 SPDX header on METHOD_SPEC.md and SHAPE_SPEC.md, the README layer table, and the notes/README paragraph from blob ids.
6. RIN_024 (which substrate-alternative build to keep) is the repo owner's decision. Do not resolve it.

## RETURN FORMAT

For each FWO:

- status: BUILT / DESIGN_WRITTEN / PRIOR_ART_FOUND / BLOCKED;
- prior-art result;
- EXPECTED commit id and whether it preceded input coding;
- failing-fixture present Y/N;
- result per claim, tagged as above.

Where a prediction failed, say so first.