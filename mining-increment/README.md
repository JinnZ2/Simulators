# mining-increment

GAP 14 from the operator's research-gaps register: mining-induced
subsurface alteration coupled to reservoir loading — the mining
literature stops at the aquifer, the dam literature starts at the
reservoir, and the connecting term for the Columbia/Snake chain sits
on the seam between them. `SOURCE_DROP.md` is delivered verbatim and
edited by nothing here.

The coupling pair closed from the other side within the session: GAP
15 landed naming Gap 14 absent, and Gap 14 then arrived — firing the
first clause of `BI_001`'s falsifier, which is updated forward in the
sibling folder rather than rewritten (`MI_001`). Still absent: the
register, `SCOPE_BOUNDARY.md`, `knowledge_state.py`,
`contributing_inflow.py`, Gaps 1 and 2.

## What is built (the scaffold, not the study)

`mining_increment.py` — the file the drop names as the expected
deliverable, scoped to what its structure supports without data. No
real mine, watershed, or reservoir appears anywhere in this folder.

- **the transfer gate, enforced** — a coal-basin parameter applied to
  a basin whose transfer is not established returns `UNDEFINED` as a
  code path; the two carried porosity deltas reach no basin today, and
  the falsifier refuses to read UNDEFINED as a low value (`MI_004`);
- **the stock/flow separation as schema** — the water-balance link
  carries two distinct named sides and no function returns one scalar
  for the pair (`MI_005`);
- **the interface equation** as delivered
  (`pool_effective = pool_natural · (1 + increment_fraction)`), with
  UNDEFINED propagating as UNDEFINED; the interface's home module
  (`contributing_inflow.py`) is among the absent artifacts, so
  plugging in is the student's step;
- **both subsidence forms** with the drop's stated shared properties
  computed rather than quoted, anchored on the confirmed Knothe form
  per the drop's own provenance flag (`MI_003`, `MI_006`);
- **both falsifiers** — the transfer one with **three outcomes**
  (closes / stands / NARROWS), the first in this family whose firing
  narrows a gap to a measurement problem instead of closing it
  (`MI_007`);
- the parameter schema **imported from `bridge-impoundment`**, not
  copied — one constructor for the shared deliverable condition
  (`MI_008`).

## The audit

`audit.py` resolves cross-references by existence, checks the drop's
provenance flag by containment (both flagged names occur only inside
the flag that disclaims them — per-citation negative provenance with
anchors, stronger than the sibling's blanket hedge, `MI_003`), and
quotes the one internal tension from both ends: the headline says the
coupling term is NOT_STUDIED while the drop's own appendix lists the
Kuye-basin record carrying subsidence into a coupled basin-scale
model — the surviving reading is the TRANSFER CAVEAT's own (not
studied *for this basin and rock*), recorded without deciding the
headline for the author (`MI_002`).

## The revision — MI_002 folded back, audited

`SOURCE_DROP_V2.md` (delivered verbatim, beside v1 — both stay)
resolves `MI_002` in a stronger form than the audit's suggested
parenthetical: the sentence the finding keyed on is gone, the carries
are stated precisely (*"stop one node short of each other"*), the
headline's referent is defined — what no record carries is reservoir
pool loading on a multi-dam surface chain — and the appendix is
promoted to a primary source table (`MI_009`). Two new devices:

- **the READ CEILING** — a per-source read-depth declaration (the CWIM
  boundary-condition formulation is not visible at abstract depth; a
  capability limit on the audit, not an open question about the
  work) — with the scaffold's compliance checked: no CWIM formulation
  appears in `mining_increment.py` (`MI_010`);
- **the CONFIGURATION NOTE** — mechanism transfers, configuration does
  not (the FIRM/SOFT split in the author's own source table), plus the
  ranking rule: the language of the source carries no weight, the
  geology of the basin carries all of it (`MI_012`).

`revision_audit.py` verifies six sections **byte-identical** across
the revision (equations, flag, method, falsifiers, deliverable, the
subsurface table) while the three sections the revision is about all
changed — the epistemics moved and the arithmetic did not, so the
scaffold stands unchanged on an unchanged specification (`MI_011`).

    python3 mining-increment/mining_increment.py   # scaffold state
    python3 mining-increment/audit.py              # the audit
    python3 mining-increment/revision_audit.py     # the revision audit
    python3 mining-increment/selftest_mi.py        # the checks
    python3 mining-increment/audit.py --measure    # re-probe hosts

| file | what |
|---|---|
| `SOURCE_DROP.md` | GAP 14 as first delivered, verbatim, not edited |
| `SOURCE_DROP_V2.md` | the revision with MI_002 folded back, verbatim, not edited |
| `mining_increment.py` | the scaffold: transfer gate, stock/flow link, interface, forms, falsifiers |
| `audit.py` | cross-references by existence, the provenance flag contained, the headline tension |
| `revision_audit.py` | the revision audit: the MI_002 resolution, the two new devices, the invariants |
| `selftest_mi.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `MI_001..MI_012` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs |

All three CLIs refuse `--selftest` rather than exiting 0. No
`no_severity` exemptions — every screen hit was reworded. Stdlib only,
parses under 3.9, phone-buildable, CC0.
