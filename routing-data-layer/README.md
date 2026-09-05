# routing-data-layer

`MARKER.md` is a delivered marker (verbatim, CC0): an **envelope
specification** for the DATA LAYER that heavy-vehicle automated routing
requires. It states what the layer must contain (R1–R10), the failure classes
observed in service (F1–F7), a claim table each carrying a refutation
condition, and the standing cost to close the gap. **Scope: the data layer
only** — sensing, control, and reasoning architecture are out of scope; every
claim is about what the reasoning would be reasoning *over*.

The marker's claim table spans **RDL-1..RDL-17**. This folder's instruments
address the data-layer envelope, the rate form, and the F6 upstream pattern
— the **RDL-1..RDL-7** territory. The **RDL-8..RDL-17** claims (Sections
5B–5F: nominal-case cycle accounting, the serial-interface condition, the
cold-climate energy envelope, the unnotated parallel-executed work, the
receiving interface and dead-wait recovery, cross-party overlap and fault
workarounds) are the cycle-accounting content built out by the sibling
`cycle-ledger/`.

"The null falls out of the envelope." Every real input — DOT feeds,
dock-geometry datasets, routing outputs — is egress-blocked, so **nothing
here is a result**. What the folder builds is the envelope structure plus the
runnable instruments (the rate form, the F6 upstream discriminator) on
constructed data.

## The two structural absences

`envelope.py` classifies each required content by **record state**:
INCOMPLETE (R1–R7, R10 — a reporting chain exists and could be funded) or
NEVER_CREATED (**R8** per-door dock geometry, **R9** per-field update latency
— no originating record anywhere). Closing a NEVER_CREATED record means
paying to CREATE it, a different cost class than funding an existing chain.
This is the `uninstrumented` / `generation-capacity` shape: "not answerable
at that instrument," not a gap. Every claim in the RDL-1..RDL-7 table carries
a REFUTED-IF, and `validate_claim` refuses one that does not (a claim with no
falsifier is a position).

## The rate form (Section 5) — the load-bearing instrument

`rate_form.py`. State the constraint as a rate comparison, not a maturity
claim: **dE/dt** (environment state-change rate) against **dM/dt**
(sustainable model refresh rate, bounded by jurisdiction reporting capacity —
not by compute). Where dE/dt > dM/dt **sustained**, the null is STRUCTURAL,
not a maturity gap — "not yet" and "different answer" are distinguishable, and
`rate_verdict` distinguishes them (STRUCTURAL / MATURITY_GAP / UNDETERMINED).
A single crossing is not structural; `sustained_excess` (registered in
`tools/known_answer.py`) is the fraction the verdict turns on. This is the
repo's recurring rate-mismatch shape (`rigidification-sensor`, `closure-cost`,
`revision-mechanism`) on a data layer. The marker's cheapest test — measure
both rates for one county over one construction season — is named and **not
run here**.

**RDL-5** (the cost is standing, not capital) is demonstrated by
`survey_decay`: a one-time survey falls below the accuracy floor within one
season (0.40, does not hold) while a periodically refreshed one holds (0.85) —
so the cost recurs and grows with network size.

## F6 — the upstream pattern

`upstream.py`. The load-bearing failure class: two independently maintained
systems, both wrong, indicates a defect **upstream** of either vendor.
`upstream_verdict` returns UPSTREAM_INCOMPLETE (both wrong, opposite
directions — a source gap each vendor filled differently), SHARED_BIAS,
VENDOR_DEFECT, or BOTH_CORRECT; `single_vendor_fix_closes` is True only for a
lone vendor defect. This is the `effective-redundancy-audit` shared-node shape
(two channels marketed as independent, both failing on one input → a shared
upstream node), and it is the marker's RDL-2.

## Files

| file | what |
|---|---|
| `MARKER.md` | the delivered marker, verbatim |
| `envelope.py` | R1–R10 with record state, F1–F7, the RDL-1..RDL-7 claim table + refutation-required validator |
| `rate_form.py` | the dE/dt vs dM/dt rate form + `sustained_excess` + the RDL-5 survey decay |
| `upstream.py` | the F6 upstream-defect discriminator |
| `demo_rdl.py` | a worked pass on constructed data, screened through `no_severity` |
| `selftest_rdl.py` | 30 checks — the envelope, the rate form, the survey decay, the four upstream verdicts |
| `CLAIM_TABLE.md` | `RDL_001..RDL_007` (distinct from the marker's own RDL-1..RDL-7) |
| `samples/rdl_demo.sample.txt` | one constructed report |

## Run

```
python3 routing-data-layer/selftest_rdl.py    # 30 checks
python3 routing-data-layer/demo_rdl.py        # the worked pass
python3 tools/known_answer.py                 # sustained_excess known-answer
```

Library modules refuse `--selftest` with rc 2. The demo screens clean through
`sheet-structure-scan/no_severity` with no exemption. Stdlib only, parses
under Python 3.9, phone-buildable, CC0.

## Out of scope, and what would change the reading

No author or working-style section (OUT OF SCOPE, honored). The marker is
falsifiable rather than a position: Section 6 lists what would change the
reading (a funded per-jurisdiction reporting function; a located/maintained
per-door dock-geometry dataset; canopy-penetrating sensing with a published
error rate on road STATE; a demonstrated safe action set at F1–F3 discovery in
a committed-lane case). Every failure-class instance is carried, not verified;
if someone runs a column against real data, that is a finding and should be
posted.
