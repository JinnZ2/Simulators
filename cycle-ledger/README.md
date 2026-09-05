# cycle-ledger

`WORK_ORDER.md` is a delivered work order (verbatim, CC0). It asks for **two
independent instruments**, either buildable alone, that generalize the
`routing-data-layer` marker's findings so any party — carrier, vendor,
regulator, researcher — can run them against their **own** operation and get
a number out. Not an argument; not a critique. An instrument with a null per
readout.

Framed as an argument against automation this does not travel and should not
be built. Framed as an envelope instrument with a null per readout it travels
to the people building the layer — who have no access to this data. Every
absence carries either a test or an explicit "unrecoverable", never an
implication.

## Deliverable 1 — `cycle_ledger.py`

A cycle is a list of ordered **elements**, each with a `rate_setter`
(HARDWARE / TERMINAL / COUNTERPARTY / ADMINISTRATIVE / SPATIAL / DECISION),
`decision_latency_binds` (TRUE only if DECISION — enforced by
`validate_element`), `currently_absorbed_by`, `notated`, `parallel_with`,
`relocation_target`, and `fault_alternates`. Five outputs:

1. **Rate-setter histogram** — counts by class, and the **KEY READOUT**: the
   fraction of elements where `decision_latency_binds` is TRUE. On the SEED
   it is **0/16 = 0.00**, so a faster decision layer cannot move the cycle;
   the saving claim must name its mechanism elsewhere. An empty cycle returns
   `None`, not 0.
2. **TIED / BEHIND / AHEAD** — AHEAD (decision-bound) is the claim's required
   support. On the SEED **AHEAD == 0**, so the tool says the support is
   absent, without hedging. This is the **null**: a cycle carrying a
   DECISION-bound element returns AHEAD > 0, and the tool returns
   "the claim holds here."
3. **Unnotated work register** — every element with `notated` FALSE (SEED:
   14 of 16), with the **safety-relevant** subset counted apart (SEED: 7).
   The work missing from the comparison sheet, not the cost missing from it.
4. **Relocation ledger** — for every OPERATOR-absorbed element, its
   `relocation_target` grouped into standing functions: what leaves the sheet
   (wage lines) vs what arrives on it (standing functions).
5. **Serial-interface condition** — for every TERMINAL element, the condition
   for a faster sender to help (that interface rebuilt as parallel), summed
   into the saving claim's stated precondition (SEED: 3 interfaces).

The **SEED** is the marker's observed cycle, marked **ONE operator's
corridor, Upper Midwest**, so a user **replaces** it rather than inheriting
it. Every classification is a reading carried from the marker, not verified.

## Deliverable 2 — `rate_gap.py`

The marker's Section 5 rate form, on a data layer. Input is two dated lists
for one jurisdiction over one construction season: `environment_events`
(closures, reopenings, structure removals, weight-restriction changes,
repaints, resurfacings) and `record_updates` (when each appeared in a routing
data source, matched by `event_id`). Output:

- **dE/dt** (events per window) vs **dM/dt** (record updates per window), a
  paired series binned by `WINDOW_DAYS` `[CHOICE 1]`.
- **lag distribution, per event class** — min/median/max over recorded events
  only. A record dated before its event is **anomalous**, counted apart, not
  folded in as a negative lag.
- **unrecorded set** — events that never entered the record, lag state
  **UNRECORDED** (absent, not a large lag); a class with no recorded event is
  **NO_RECORDED**.

**Readout** (marker Section 5), keeping the two inputs visible and not
collapsing them:

- dE/dt > dM/dt **sustained** AND a **nonzero** unrecorded set → **STRUCTURAL**.
  Not a maturity gap; a faster refresh does not close it.
- dM/dt ≥ dE/dt with the unrecorded set **empty** → **MATURITY_GAP**. Closes
  with funding.
- anything else → **UNDETERMINED**, with the failing condition named — a
  sustained excess with an empty unrecorded set is a refresh gap, *not* a
  structural absence.

`sustained_excess` and `rate_verdict` are **imported** from
`routing-data-layer/rate_form.py` (not copied) — the verdict this instrument
returns is the same object that folder registered and tested. This is the
repo's recurring rate-mismatch shape (`rigidification-sensor`,
`closure-cost`, `revision-mechanism`) on a data layer. Nothing here is a
result: no county's events or updates are measured (egress-blocked); the
example series is **constructed** and marked so. The marker's cheapest test —
both rates for one county over one season — is named and **not run here**.

## Files

| file | what |
|---|---|
| `WORK_ORDER.md` | the delivered work order, verbatim |
| `cycle_ledger.py` | Deliverable 1 — the five outputs, the SEED, the null |
| `rate_gap.py` | Deliverable 2 — dE/dt vs dM/dt, per-class lag, the unrecorded set (imports `rate_form`) |
| `demo_cll.py` | a worked pass on both deliverables, screened through `no_severity` |
| `selftest_cll.py` | 169 checks — validation, both nulls, the lag states, the ≤60-column constraint, the `--selftest` refusals |
| `CLAIM_TABLE.md` | `CLL_001..CLL_009` |
| `samples/cll_demo.sample.txt` | one constructed report |

## Run

```
python3 cycle-ledger/selftest_cll.py     # 169 checks
python3 cycle-ledger/cycle_ledger.py     # the SEED ledger
python3 cycle-ledger/rate_gap.py         # a constructed structural season
python3 cycle-ledger/demo_cll.py         # both, screened through no_severity
```

Both instruments refuse `--selftest` with rc 2. The demo screens clean
through `sheet-structure-scan/no_severity` with no exemption. Every output is
readable under a 60-column terminal. Stdlib only, parses under Python 3.9,
phone-buildable, CC0.

## Open, not graded

Continuous-operation duration for a driving stack is unpublished — industry
reports uptime against a maintenance-bay operating model, not
hours-to-degradation — so the 14-hour regulated figure and the 24-hour claim
are **not comparable quantities**. No equivalence between operator fatigue
and model degradation is asserted: different mechanism, unmeasured from
inside, recorded here as an open question with the missing measurement
(hours-to-degradation) named. There is no author or working-style section
(OUT OF SCOPE, honored); instances are observations only.
