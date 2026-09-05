# labor-instrument

Two parts, built to `WORK_ORDER.md`. **PART 1** is an instrument-drift
decomposer for BLS CES — a join that answers *how much of this delta is the
instrument*. **PART 2** is a substrate-neutral labor schema with the
framework pushed into the read layer, plus three posted gaps.

## The egress fact sets PART 1's data status

PART 1 is "buildable from published sources today" — but its sources (ALFRED
observation vintages, the BLS CES history page, Census NAICS crosswalks,
QCEW) all require network, and this environment's egress is an allowlist:
those hosts answered no on CONNECT (probed 2026-09-05T14:02Z). So **no data
was fetched**, the vintage store ships **empty**, the registry seed is
**carried, not verified** (BLS history-page egress-blocked, every entry
`verified=False`), and the **acceptance test is NOT RUNNABLE here** — on an
empty store the reconstruction returns `UNRECOVERABLE`, recorded not faked,
with the 2026-08-28 target stored for when real vintages land. Nothing is
fabricated into the store or the registry.

**What is built and verified is the machinery**, correct by construction on
constructed data.

## PART 1 — the decomposer

- **M1 `vintage_store.py`** — keys every observation by `(series_id, period,
  release_date)`; the cell holds every version ever published; `revision()`
  is latest − earliest. The revision history is the signal.
- **M2 `instrument_registry.py`** — one record per methodology change; the
  work order's seed set carried verbatim (unverified), with the rolling
  5-year seasonal re-estimation registered as a **recurring** change.
- **M3 `decompose.py`** — joins M1 × M2 × a NAICS crosswalk and splits a
  two-period delta into **real_change | revision | boundary_crossing**.
  **Where the crosswalk splits ambiguously the boundary is a band and
  real_change inherits it; `as_point()` raises — never a point estimate
  where the crosswalk is ambiguous.** A single-vintage endpoint yields
  revision `UNKNOWN` (not zeroed); a missing endpoint is `UNRECOVERABLE`.

## PART 2 — the substrate-neutral schema

`labor_schema.py`. The base layer records units of work substrate-agnostically;
the framework goes in the read layer. The invariants are **enforced in code**:

- exposure is declared per substrate class (person-hours / substrate-hours /
  area-time / animal-hours) and **never converted** across classes —
  `convert_exposure` raises (conversion imports a valuation);
- efficiency is **two numbers** (`output_per_joule`, cross-class;
  `output_per_exposure_hour`, per-class) **never collapsed** —
  `combined_efficiency` raises;
- **capital stays out** — no `capital` field; `balance_on_capital` raises;
- the **allocation model** (augmentation / substitution / oversight-limited)
  is a declared field, never a default — a record that omits it is flagged.

The joule denominator crosses classes with no convention. The
money-vs-joule **ranking flip** is demonstrated on constructed operations
(the real hyperaccumulator number is GAP 2). The read-layer query
`complementarity()` reports where a combined operation's output-per-joule
beats either substrate alone — the query the instrument is built for.

## Run

```
python3 labor-instrument/selftest.py       # 36 checks on constructed data
```

Stdlib only, parses under Python 3.9, phone-buildable. The modules refuse
`--selftest` with rc 2; `selftest.py` prints `selftest: N checks, M failed`.

| file | what |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `vintage_store.py` | M1 — observation vintages, all versions retained |
| `instrument_registry.py` | M2 — methodology changes, seed carried (unverified) |
| `decompose.py` | M3 — the three-way split, band where the crosswalk is ambiguous |
| `labor_schema.py` | PART 2 — substrate-neutral record + enforced invariants + read layer |
| `GAPS.md` | the three posted gaps + the task-boundary open item |
| `selftest.py` | the checks |
| `CLAIM_TABLE.md` | `LI_001..LI_008` |

## Gaps and the open item

Three gaps are **posted, not filled** (`GAPS.md`): metabolic joules per task
class, insolation-captured → metal-recovered for hyperaccumulators, and
compute joules per task-instance — each needs data not in joined/published
form, egress-blocked, and nothing is fabricated to close them. The
task-boundary definition ("output delivered", drift-free across
architectures) is recorded **unresolved**; GAP 3 cannot be filled cleanly
until it is settled. CC0.
