<!-- landed verbatim 2026-09-27 from the FABLE WORK ORDER message; nothing below this line is edited here -->

# FABLE WORK ORDER — 2026-09-27
## Dependency chains, conversion points, and single-medium detectability

TARGET: Claude Fable 5.1
LOCATION: `Simulators/route-independence/` on the existing working branch (JinnZ2/route-independence still returns 403 on create; keep the folder promotable)
LICENSE: CC0. Stdlib only. Phone-buildable.
EXTENDS: FWO-2 `route_independence.py` (built, prior art imported from effective-redundancy-audit). Reuse it. Do not rebuild it.

---

## STANDING RULES (unchanged from 2026-09-26 packet)

- Instruments, not arguments. Nothing in this order asks you to show a conclusion is true.
- UNKNOWN is a first-class result. PARTIAL and NOT_TRANSFERABLE stay distinct. ABSENT_FIELD stays distinct from NO.
- SOURCE field on every demo value. If a value is carried rather than read, mark it CARRIED.
- Tag every claim OBSERVED / DERIVED / PROPOSED, and whose it is.
- PRIOR-ART CHECK FIRST on every item. A found instrument counts as a result. Import it; do not rebuild.
- No characterization of any person, in code, docs, or claim tables.
- State expected demo structure IN ADVANCE so the demo can fail. A demo that cannot fail is not a demo.

---

## CONTEXT (provenance marked)

- [HERS, stated] The money system is now the rules, the laws, and the medium science is shaped around. Any homogeneous system behaves as a monoculture (her crop case). Attempts to operate outside it — Bitcoin named — were pulled back in. Even barter routes back, because the tax on it settles in the one medium. So the dependencies cannot currently be separated, and that limits what ideas can come from inside. She frames the resulting blind spot as a national security risk.
- [VERIFIED 2026-09-26, IRS Topic 420] Barter is included in gross income at fair market value in dollars. The transaction is denominated in the single medium even when no dollars move.
- [DERIVED, Claude] This is ENCLOSED_PLURALITY (FWO-2) applied to a knowledge system: routes counted high, independent routes zero, because each route terminates in the same settlement node.
- [LITERATURE, one search, not exhaustive] Research-funding literature compares FUNDERS (government / market / philanthropy / tax credit / procurement). No source found counts whether any route in a finding's production is not a funder. UNCLAIMED JOIN.
- [INFERENCE, Claude, not a finding] Defect inheritance (Bommasani et al. 2021, cited in arXiv 2609.17320): a shared defect in a population of interacting systems compounds rather than replicates. Transfer to a single economic medium has not been run by anyone.

---

## FWO-5 — `dependency_chain_audit.py`

**Purpose.** Given one produced result (a finding, a build, a product), enumerate every dependency needed to produce it, and for each, whether any route to it can discharge its own obligations in its own medium.

**Prior art — CHECK FIRST.** Life-cycle inventory methods; bill-of-materials / supply-chain mapping; full economic costing of research; open-hardware and citizen-science infrastructure studies; commons scholarship (Ostrom lineage). Record found / not found per source. A found enumeration method is imported, not rebuilt.

**Dependency categories (minimum; extend if prior art has a better set):**
instrument, material/reagent, facility/space, energy, transport, labor (whoever runs it), data access, publication/dissemination, credential/authorization, legal compliance (incl. tax on any exchange).

**Per route, record:**
- `medium_of_account` — what the route is denominated in
- `medium_of_settlement` — what its obligations discharge in
- `status` — INDEPENDENT / CONVERTED / UNKNOWN
- `conversion_point` — for CONVERTED only: the step where the route re-enters the single medium (account, settlement, input purchase, credential, publication, tax)
- `SOURCE`

**Outputs:** per-dependency route_count, independent_count; per-result independence_ratio; ENCLOSED_PLURALITY flag carried from FWO-2; a list of conversion points ordered by how many dependencies route through each.

**Hard constraint.** "Permitted" must not merge with "independent" (same as FWO-2). A route that is legal but taxed at fair market value in dollars is CONVERTED.

**Demo — three cases, expected structure stated now:**

| Case | Expected |
|---|---|
| (a) Household-scale observation, no exchange (e.g. one person's phenology record from their own land) | Mostly INDEPENDENT; publication/dissemination UNKNOWN or CONVERTED. If this reads fully CONVERTED, the instrument is over-counting — record as finding. |
| (b) One open-access published lab finding (pick one reachable; name it) | independence_ratio near 0; ENCLOSED_PLURALITY on at least instrument, labor, and publication. If any dependency reads INDEPENDENT, record which and why — that is the interesting row. |
| (c) An exit attempt: Bitcoin acquired and disposed of for a physical need | Own ledger reads INDEPENDENT at account level; CONVERTED at settlement (disposal as taxable event, dollar-denominated penalty for non-reporting). conversion_point = settlement. If sources are unreachable, mark CARRIED. |

---

## FWO-6 — conversion-point register (no verdicts)

**Purpose.** Map where each known exit attempt re-entered the single medium. A map, not an evaluation of any attempt.

**Candidates:** Bitcoin / cryptocurrency; Amish and cooperative barter (cash-settlement case); time banks; LETS / local currencies; mutual-aid networks; open-hardware communities; gift economies within one household vs across households.

**Per entry:** what the attempt changed (account? ledger? exchange? production?), where it reconverted, by which mechanism (tax, input purchase, credential, legal recognition, publication), and SOURCE. UNKNOWN where not sourceable.

**What to look for, stated in advance:** whether conversion points cluster at one layer (hypothesis, Claude's: SETTLEMENT, not exchange) or spread across several. Either result is a finding. If they spread, the single-layer hypothesis is wrong and the claim table says so.

Prior-art check: complementary-currency literature and commons scholarship may already hold a failure-point taxonomy. Look first.

---

## FWO-7 — research design only: detecting a single-medium defect without a control world

**The problem.** The Emergence World mixed-population comparison worked because a world with a different configuration existed. A global single medium has no parallel world, so its blind spot cannot be read from inside by construction.

**Deliverable:** DESIGN_WRITTEN with scope, kill condition, and cheapest first run, for candidate control sources such as:
- historical periods or jurisdictions with a parallel medium in legal use (tax-in-kind, commodity money, local scrip)
- populations whose coordination does not settle in the medium (household production; the insect scaling comparison already filed)
- divergence-then-contact cases (fission/divergence object)

Do not run anything. Literature prior-art check on each design: NOT_RUN is an acceptable status, but state it.

---

## CARRIED FROM THE 2026-09-26 AUDIT — answer if in scope

1. `git diff 57b9cdf^1 57b9cdf` and `git diff 57b9cdf^2 57b9cdf` — was the merge loss confined to `tools/known_answer.py`?
2. FWO-3: how were "considered and rejected" alternatives coded against `options_not_tried`? Council distinction was options tried in the world vs not tried.
3. FWO-3 C5: does any read record type give an independent reviewer authority to add options?
4. ESP-1: C and NC tallies separately; how many NC rows carry a verdict.

---

## CLAIM TABLE REQUIREMENT

Every result lands in the claim table with: claim ID, status (BUILT / DESIGN_WRITTEN / NOT_RUN / CARRIED), what was read vs carried, and the sampling boundary of whatever was read (which hosts were reachable, and what that selects for).
