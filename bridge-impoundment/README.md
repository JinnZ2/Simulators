# bridge-impoundment

GAP 15 from the operator's research-gaps register: the bridge as a
**transient impoundment** — clog, pond, fail, release — the term that
falls between transportation engineering and dam safety, with the
scour and clogging inputs quantified in the 2024–2025 record and the
impoundment/release term owned by neither field. `SOURCE_DROP.md` is
delivered verbatim and edited by nothing here; `SOURCE_DROP_V2.md` is
v1 plus the delivered addendum, assembled as a verified pure
insertion (below).

The entry is a draft for `UNDERGRADUATE_RESEARCH_GAPS.md`, which this
repository does not hold; at landing both coupling targets (Gaps 2
and 14) were with it, while every repo-facing reference resolves —
`CCC_007`, Module F, the operator swap, the Columbia/Snake node list
(`BI_001`). **GAP 14 then arrived in the same session** (the
`mining-increment/` folder, detected by content), firing the first
clause of `BI_001`'s falsifier — the claim carries its update note;
Gap 2 and the loop marker stay absent.

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
  real chain every cell is UNMEASURED, the data hosts in the carried
  allowlist-refusal state, no value supplied from memory into a
  flood-safety artifact (`BI_006`).

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

## The addendum (v2: the instrumented cascade case + the standing record)

The author then delivered two blocks with the instruction *"add to
the quantified table, plus a note"* (`ADDENDUM_DELIVERY.md`,
verbatim). `SOURCE_DROP_V2.md` is the assembly — v1 with the fragment
inserted at the end of the quantified section, verified as a **pure
insertion** (the fragment comes from the delivery sheet, appears
once, and removing it reproduces v1 byte-for-byte; the placement is a
declared [CHOICE], since the instruction names the section and not
the byte offset — `BI_008`). The content:

- **Fjærland 2004** (Breien et al. 2008) — the folder's first
  *measured* instance of the chained shape: moraine-dammed lake
  breach → 240,000 m³ debris flow, post-event morphology in hand. It
  measures the RELEASE half only ("clog" does not occur in the
  fragment), and the CONFIGURATION NOTE discipline applies
  symmetrically — a moraine dam is not a clogged bridge; its two
  measured outputs are the release initiator's two load-bearing
  fields (`BI_009`).
- **The NVE GLOF register** — a standing national record that
  *"serves English [and] never ranks on an English query because the
  phenomenon indexes under jøkullaup / skred"*: a
  query-vocabulary-bounded null stated by the author about a national
  register, with *"long series = the instrument for a slow rate"*
  naming why a register beats event studies on a rate question
  (`BI_010`). `glacier.nve.no` is carried, not probed from here.

`addendum_audit.py` checks the assembly and both blocks; prior claims
keep their ratings on the text they rated.

    python3 bridge-impoundment/bridge_impoundment.py   # scaffold state
    python3 bridge-impoundment/audit.py                # the audit
    python3 bridge-impoundment/addendum_audit.py       # the addendum
    python3 bridge-impoundment/selftest_bi.py          # the checks
    python3 bridge-impoundment/audit.py --measure      # re-probe hosts

| file | what |
|---|---|
| `SOURCE_DROP.md` | GAP 15, delivered verbatim, not edited |
| `ADDENDUM_DELIVERY.md` | the addendum delivery sheet, verbatim |
| `SOURCE_DROP_V2.md` | v1 + the addendum, a verified pure insertion |
| `bridge_impoundment.py` | the scaffold: schema, flag, interface, arithmetic, falsifiers |
| `audit.py` | cross-references by existence, the two sentences vs the record, egress |
| `addendum_audit.py` | assembly + cascade case + standing record |
| `selftest_bi.py` | the checks; run it, it prints its own count |
| `CLAIM_TABLE.md` | `BI_001..BI_010` with REFUTATION_PROTOCOL |
| `samples/` | pinned runs |

The CLIs refuse `--selftest` rather than exiting 0. No `no_severity`
exemptions — every screen hit was reworded. Stdlib only, parses under
3.9, phone-buildable, CC0.
