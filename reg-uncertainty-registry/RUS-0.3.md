# RUS-0.3 -- Regulatory Uncertainty Standard (PROPOSED revision)

Status: PROPOSED by this registry (WO-REG-1 Part D). Not adopted by any body.
A revision of RUS-0.2 (`bundle/source/current/regulatory_uncertainty_standard_v02.md`,
pinned in `bundle_pins.json`). Sections not named here are unchanged from 0.2
and are not restated.

Every clause below is a switch in `tools/grade.py`, so each one is computed
alone and in combination over every graded row (`REVISED_REPORT.md` F4,
`python3 tools/stats.py components`). No count appears in this file: counts
live in the report, which is rendered from the registry and re-checked by
`tools/validate.py`.

## Changes from 0.2

| clause | 0.2 | 0.3 | from |
|---|---|---|---|
| M7 | margin above the floor only (R2) | one class below the floor also conforms by margin | REVIEW_v2 R7, REVIEW_v3 R13 |
| SUB | "alternatives exist" lowers C_restrict, unchecked | credit stands only for a named alternative graded below the case | REVIEW_v2 R9 |
| R6a | restriction re-graded annually, two cycles max | overlay status `R6_SELF_SEALING`; justification must be independent of the blocked evidence | REVIEW_v2 R8 |
| R6b | absent | loosening a self-sealing restriction: U one class lower | REVIEW_v2 R8 (D01) |
| R1 scope | R1 wherever harm is resolved | R1 where the resolution sets market status; level-setting rows excluded | NCR-N06 |
| BASIS | unstated; Annex A mixes action and outcome | every grade states `action` or `outcome` | NCR-N02 |
| R3 record | one compulsion flag | compulsion recorded for the action and the outcome separately | NCR-N04 |
| one-directional claim | stated from tallies | requires `over_possible`; at zero it reads `HOLDS_UNTESTABLE` | REVIEW_v3 R13 |
| sweep | variants named by label | each variant states its column rule and its U3 row | NCR-N07, NCR-N08 |

The matrix values, the three consequence axes and their bands, the direction
classes D1-D5, R4 and R5 are unchanged.

## 3. Terms and definitions (additions)

- **Basis.** What a direction class is read from: `action`, the agency's own
  move; `outcome`, the legal status of the product or exposure at the coding
  date. The two differ where a court, a statute or a sponsor moved the outcome
  away from the agency's action.
- **Substitution credit.** A reduction in C_restrict justified by the
  existence of alternatives to the restricted product.
- **Self-sealing restriction.** A restriction, or a declined monitoring
  requirement, that prevents generation of the evidence that would resolve the
  uncertainty it rests on.
- **Cycle.** One year held at the decision date.
- **over_possible.** The number of graded rows whose own actual direction
  could fire R2's over-restrictive branch under some matrix: C_restrict >
  C_permit, the floor set by the matrix, no R3 compulsion, and actual D3 or
  above.

## 8. The decision matrix -- overlays (revised)

**M7 (symmetric tolerance).** A decision one class below its floor is
`CONFORM (within symmetric margin)`. Two or more classes below is
`NON-CONFORM: below floor`. Reason: under 0.2, R2 grants one class of margin
above the floor and none below it, so the published matrix counts deviations
in one direction more strictly than the other, by construction.

**SUB (substitution).** Before the gap is taken, a C_restrict that carries a
substitution credit is checked:

```text
credit claimed, alternative named, alternative's C_permit grade < the case's C_permit grade
    -> credit stands
otherwise
    -> C_restrict + 1 (capped at 9), and the reason is recorded on the row
```

The alternative's name and grade are recorded on the case
(`consequence.C_restrict.substitution`). An alternative graded nowhere counts
as ungraded; it does not inherit a grade from the case. The rule is called SUB
because Rule S is the work order's cost-bearer rule (NCR-N25).

**R1 (resolved-harm override, scope stated).** Evidence at U1-U2 of actual
harm or absent benefit makes D5 the required class where the decision sets
market status. A decision that sets a level (a tolerance, an intake limit) is
graded on the matrix; R1 does not apply to it. The literal 0.2 reading, R1 on
every flagged row, is reported beside as `R1L` and is not part of 0.3.

**R3 (statute and judicial exception, recorded twice).** Compulsion is a
property of the case and is recorded separately for the action and for the
outcome (`forced_action`, `forced_outcome`). On the action basis R3 reads the
first; on the outcome basis, the second. Declaration is still required: an
undeclared compelled departure stays non-conforming.

**R6a (self-sealing prohibition, as an overlay).** A self-sealing restriction
held more than two cycles, with no justification on record that is
independent of the evidence it blocks, carries the overlay status
`R6_SELF_SEALING`. The overlay sits beside the R2 status and never replaces
it. Justification is coded `none`, `self_sealed_only` (justified by the absence
of the evidence the restriction blocks) or `independent`; only `independent`
counts. Unrecorded cycles give `R6 not evaluable`, never `R6 not triggered`.

**R6b (loosening a self-sealing restriction).** For a decision that loosens a
self-sealing restriction, uncertainty maintained by that restriction is not
credited toward the floor: U is taken one class lower for that decision. The
case declares that it is such a decision. R6b changes the floor; it does not
grade the earlier restriction.

## 11. Calibration (addition)

A calibration variant states its column rule and its U3 row. A variant that
states neither cannot be reproduced. A variant whose published counts no
stated or searched U3 row reproduces is reported as not reproducing, not as
computed.

## 12. Conformity assessment (addition)

A table of conformity statuses states its basis, one basis per table. A claim
that non-conformity is one-directional reports `over_possible` with the
tallies:

```text
over_possible = 0                       HOLDS_UNTESTABLE   the rows cannot show the other side
over_possible > 0, no over-restrictive  HOLDS
over-restrictive rows present           FAILS
```

The reliability requirement of 0.2 section 12 is unchanged and is **not met
by this registry**. The 0.2 text names a human second coder as the first
requirement of any 0.3 revision. The second coding prepared here
(`second_coder/`) is a session of the same model class as the first coder,
contamination probe first, and it covers ten rows. It does not satisfy the
clause (NCR-N24 open).

## What 0.3 does not do

- It does not set the matrix values from data. They are 0.2's, unchanged.
- It does not grade any agency. A status is the output of these rules applied
  to recorded inputs, and it carries their assumptions.
- It does not establish that the revisions are improvements. F4 in the report
  shows what each switch moves. Whether the moved rows are better graded is a
  judgment this file does not make.
