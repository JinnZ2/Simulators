# WORK-ORDER ASSESSMENT

Candidate work orders that fall out of the report and its audit. These are
proposals for the operator to accept, change or drop. None is started.

| id | work order | buildable here? | why it matters | first deliverable |
|---|---|---|---|---|
| OSC-WO1 | **Barrier-per-bit calculator with declared terms.** A stdlib module that computes stripe period, coherent Δ and energy per bit, where absorbed fraction, spot geometry and the population-vs-single-bit criterion are required inputs. An undeclared term is refused, not defaulted. | yes | Closes OSC_004, OSC_005 and OSC_008 as a class: the defects are terms the report used without stating them. | `barrier_per_bit.py` + known-answer cases pinned to the report's reproducible rows |
| OSC-WO2 | **Decision table as a three-state readout.** Turn the §6.4 table into a function of measured Δ with `UNMEASURED` as a first-class state, a single-bit/population switch, and the depinning discount as a declared factor, not an assumed ~100×. | yes | Today the roadmap is gated on one unmeasured number; the readout should say so mechanically rather than in prose. | `decision.py`, all branches reachable on constructed inputs |
| OSC-WO3 | **The measurement itself.** Sharrock time-dependent coercivity, or MFM decay tracking, on vector-beam-written bits in N = 5–9 Co/Pt. | no (needs a lab) | The report's terminal node. Everything downstream waits on it. | A protocol card: sample, temperatures, waiting times, fit form, and what each Δ band routes to. Written, not run. |
| OSC-WO4 | **Citation sweep.** Locate the roughly 30 cited sources at search depth, starting with the load-bearing ones: arXiv:1312.7301, Vomir 2017 (the 7.6 µJ/cm² origin), and Kimel & Li 2019 (6 J/cm³, 120 aJ). | partly (egress is an allowlist) | OSC_005 and OSC_006 turn on what those sources actually state. | `SOURCES.md` rows with FOUND / NOT_LOCATED / CONTRADICTED |

Suggested order: WO4 (cheap, settles OSC_005/006), then WO1 and WO2. WO3
needs an outside party and is posted as a protocol only.
