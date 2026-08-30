# bridge-impoundment

GAP 15 from the operator's research-gaps register: the bridge as a
**transient impoundment** — clog, pond, fail, release — the term that
falls between transportation engineering and dam safety, with the
scour and clogging inputs quantified in the 2024–2025 record and the
impoundment/release term owned by neither field. `SOURCE_DROP.md` is
delivered verbatim and edited by nothing here.

The entry is a draft for `UNDERGRADUATE_RESEARCH_GAPS.md`, which this
repository does not hold; both coupling targets (Gaps 2 and 14) are
with it, while every repo-facing reference resolves — `CCC_007`,
Module F, the operator swap, the Columbia/Snake node list (`BI_001`).

## What is built (the scaffold, not the study)

`bridge_impoundment.py` — the file the drop names as the expected
deliverable, scoped to what its structure supports without data:

- **the parameter schema** — every parameter carries a knowledge state
  from a closed vocabulary and names what would move it, as a
  constructor rule; a value marked UNMEASURED refuses;
- **the clog flag** — three states, never two: FLAG at or under the
  carried 10 m threshold, CLEAR above, UNMEASURED when spacing is
  unknown (an unknown spacing is not a clear span);
- **the initiator interface** — the `CCC_007` requirement made
  checkable at the design layer: a breach initiator and a
  bridge-release initiator carry identical key sets, and a widened
  dict fails the check (`BI_004`); the engine half stays owed;
- **the sign caveat, enforced** — no release-path function takes a
  shielding parameter (asserted over signatures), and the protective
  successive-bridge finding lives only in a `StandingStructureRecord`
  whose `to_initiator()` raises (`BI_003`);
- **the conservation arithmetic** — peak-outflow gain equals
  accumulation time over release time, above one exactly when the
  release is faster; debris load gain is at least one by construction
  (`BI_005`);
- **both falsifiers, three-valued** — constructed data closes the gap
  in both directions and an unknown input never closes it; on the
  real chain every cell is UNMEASURED, hosts measured refused, no
  value supplied from memory into a flood-safety artifact (`BI_006`).

**No real bridge appears anywhere in this folder.** The NBI inventory
pass, the debris-supply coupling, the HEC-RAS backwater and release
modeling, and the routing run are the study — they need the reading
room and the engine this environment does not have.

## The audit

`audit.py` resolves every cross-reference by existence rather than
mention, checks the drop's two repo-facing sentences against the
record (*"Module F already proves"* carries an attribution drift and a
strength drift while its substance is right, `BI_002`), and pins the
egress state of the data hosts. The drop arrives with its own
citation hedge — *located by search, not asserted* — the first in the
flood family to carry its negative-provenance note itself (`BI_007`).

    python3 bridge-impoundment/bridge_impoundment.py   # scaffold state
    python3 bridge-impoundment/audit.py                # the audit
    python3 bridge-impoundment/selftest_bi.py          # the checks
    python3 bridge-impoundment/audit.py --measure      # re-probe hosts

| file | what |
|---|---|
| `SOURCE_DROP.md` | GAP 15, delivered verbatim, not edited |
| `bridge_impoundment.py` | the scaffold: schema, flag, interface, arithmetic, falsifiers |
| `audit.py` | cross-references by existence, the two sentences vs the record, egress |
| `selftest_bi.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `BI_001..BI_007` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs |

Both CLIs refuse `--selftest` rather than exiting 0. No `no_severity`
exemptions — every screen hit was reworded. Stdlib only, parses under
3.9, phone-buildable, CC0.
