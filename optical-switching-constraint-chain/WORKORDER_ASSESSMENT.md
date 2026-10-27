# WORK-ORDER ASSESSMENT

Candidate work orders that fall out of the report and its audit. These are
proposals for the operator to accept, change or drop. None is started.

| id | work order | buildable here? | why it matters | first deliverable |
|---|---|---|---|---|
| OSC-WO1 (DONE) | **Barrier-per-bit calculator with declared terms.** A stdlib module that computes stripe period, coherent Δ and energy per bit, where absorbed fraction, spot geometry and the population-vs-single-bit criterion are required inputs. An undeclared term is refused, not defaulted. | yes | Closes OSC_004, OSC_005 and OSC_008 as a class: the defects are terms the report used without stating them. | `barrier_per_bit.py` + known-answer cases pinned to the report's reproducible rows |
| OSC-WO2 (DONE) | **Decision table as a three-state readout.** Turn the §6.4 table into a function of measured Δ with `UNMEASURED` as a first-class state, a single-bit/population switch, and the depinning discount as a declared factor, not an assumed ~100×. | yes | Today the roadmap is gated on one unmeasured number; the readout should say so mechanically rather than in prose. | `decision.py`, all branches reachable on constructed inputs |
| OSC-WO3 | **The measurement itself.** Sharrock time-dependent coercivity, or MFM decay tracking, on vector-beam-written bits in N = 5–9 Co/Pt. | no (needs a lab) | The report's terminal node. Everything downstream waits on it. | A protocol card: sample, temperatures, waiting times, fit form, and what each Δ band routes to. Written, not run. |
| OSC-WO4 (DONE) | **Citation sweep.** Locate the roughly 30 cited sources at search depth, starting with the load-bearing ones: arXiv:1312.7301, Vomir 2017 (the 7.6 µJ/cm² origin), and Kimel & Li 2019 (6 J/cm³, 120 aJ). | partly (egress is an allowlist) | OSC_005 and OSC_006 turn on what those sources actually state. | `SOURCES.md` rows with FOUND / NOT_LOCATED / CONTRADICTED |

Suggested order: WO4 (cheap, settles OSC_005/006), then WO1 and WO2. WO3
needs an outside party and is posted as a protocol only.

## Status

- **OSC-WO4 done.** `citations.py` holds 14 rows at search depth, with
  states derived by `tools/check_citations.citation_state` (imported):
  7 VERIFIED, 0 CORRECTED, 1 NOT_FOUND, 6 UNREACHABLE.
  - arxiv.org does not resolve here, so primary depth needs that domain
    allowed in the session's network settings.
  - The sweep added OSC_011..014.
  - OSC_005 and OSC_006 stay open: the 7.6 µJ/cm² and 120 aJ values were
    not reached.
- **OSC-WO1 done.** `barrier_per_bit.py` gives stripe period, coherent Δ,
  retention line and energy per bit.
  - Spot shape, ledger (incident or absorbed), absorbed fraction, and
    single-bit vs population criterion are required. An undeclared term
    raises `UndeclaredTerm`; there are no defaults.
  - It reproduces the report wherever the report is reproducible.
  - It refuses every "absorbed" energy row the report prints, since no
    absorbed fraction is declared.
  - It refuses the report's 60 line unless a basis is given.
  - `energy_per_bit` and `retention_line` are registered in
    `tools/known_answer.py`.
  - The registry caught two wrong expected values in my own first cases
    (an argument slip, and a 3.156e7 s year against the module's Julian
    3.15576e7 s). Both were corrected from hand arithmetic, not from the
    module's output.
- **OSC-WO2 done.** `decision.py` turns the §6.4 table into a readout.
  - Two lines, imported from `barrier_per_bit`: one bit surviving ten
    years (40.3), and a population line that must be declared with its
    basis (60 as carried).
  - States: ABOVE_POPULATION_LINE, BETWEEN_LINES, BELOW_SINGLE_BIT_LINE,
    STRADDLES and UNMEASURED.
  - A measured Δ must carry its uncertainty, and an interval crossing a
    line reads STRADDLES with no route.
  - A coherent estimate is refused without a declared discount range and
    basis, and is labelled ESTIMATED.
  - On the report's own inputs the readout is UNMEASURED. With an
    illustrative 30–100× discount, the 12 nm bit straddles two bands and
    the 5.4 nm bit falls below the single-bit line.
