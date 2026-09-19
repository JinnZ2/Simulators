# CLAIM_TABLE -- reporting-chain-loss

Permanent ids `RCL_NNN`. These are claims about the two instruments and their
behaviour on CONSTRUCTED data, distinct from the order's own OBSERVED /
DERIVED / PROPOSED tags and its Test A..E. Ids are permanent; a refuted claim
is updated in place, never renumbered. Status: SUPPORTED / REFUTED /
UNVERIFIED.

`WORK_ORDER.md` (WO-5) is landed **verbatim** and edited by nothing here.
Nothing in this folder is a measurement of any plant or any operator: the
chains and operators are constructed and seeded, the coefficients carry no
units, and the order's runnable tests over real operators, a real CMMS, and
published ecology are NOT_RUN here.

| id | status | claim |
|---|---|---|
| RCL_001 | SUPPORTED | **The composition is closed form and it is the load-bearing metric.** In the linear-Gaussian chain `x_n = a_n x_{n-1} + c_n + e_n`, the terminal's expected offset from the scaled ground is `B = sum_k (prod_{j>k} a_j) c_k`. `composed_bias` computes it; the by-hand cases (single hop = its own offset via the empty product; two hops at gain 0.9 same sign = 1.9; identity gain = 2.0) are registered in `tools/known_answer.py`. The order says the per-hop pieces are documented and the composition is not; this is the composition, made a number. |
| RCL_002 | SUPPORTED | **The terminal is an estimator of the incentive stack, and the reader who takes it AS the ground carries a bias that grows with the chain.** A reader rescaling by the retained gain (`ground_hat = x_N / G`) carries bias `B / G`; a lossy chain has `|G| <= 1`, so the rescaling AMPLIFIES. On the shipped directed chain B/G runs 1.11 (N=1) -> 5.24 (N=4) -> 43.97 (N=16). That is the order's "estimator of the incentive stack, not the ground". |
| RCL_003 | SUPPORTED | **Directed loss compounds; random loss cancels; the classifier is not constant.** Same-sign offsets accumulate (directed mean |B| grows with N); random-sign offsets are mean-zero and their spread grows only as sqrt(N), so the directed/random ratio grows with the chain (1.0 at N=1 -> 4.60 at N=16). At offset magnitude 0 both arms return exactly 0 with verdict `NO_INCENTIVE`, so a run reading `DIRECTED_BIAS` everywhere is a property of the offsets, not of the code. |
| RCL_004 | SUPPORTED | **The DPI floor holds in the model and is used as the null, not re-derived.** With every `|a_n| <= 1` the partial-product magnitude is non-increasing hop by hop (`gain_is_nonincreasing` True on `[0.9]*8`, False on a gain above 1). The order states the data processing inequality is a theorem, not a finding; the module treats it that way -- the finding is entirely in what DIRECTED loss does that random loss does not, which the DPI does not cover because it assumes a fixed transform. |
| RCL_005 | SUPPORTED | **A zero and an absence are kept apart, on every return.** No incentive (all `c=0`) gives an EXACT `0.0`; an unspecified gain gives `None` (NOT_EVALUABLE), never a bias of zero; a dead hop (`prod a == 0`) makes the ground unrecoverable, so the rescaled bias is `None` with `GROUND_UNRECOVERABLE` rather than an infinity manufactured by the division. The registered case set pins the exact-0 against the None. |
| RCL_006 | SUPPORTED | **The pre-entry register carries the order's seven gates, none logged, and draws the order's structural reading.** L0, L0', L1, L1', L2, delegation, form-field, each with its cost and whether it conditions which reports arrive: 7 gates, 0 logged, 6 conditioning the sample. The reading the counts license is the order's -- arriving reports are a sample past a per-operator threshold, not a sample of machine conditions -- and the threshold is recorded as unestimated. |
| RCL_007 | SUPPORTED | **Test B's calibration classifier separates the two worlds and is not constant.** On CONSTRUCTED operators, a world where the reporting rate tracks the operator's own (acted on)/(filed) ratio reads `TRACKS_calibrated` (rho ~0.998); a world where the rate is independent reads `DOES_NOT_TRACK` (rho ~0.18). Both branches reachable. The order's inverted finding -- non-reporting as calibrated inference, not disengagement -- is the TRACKS branch. |
| RCL_008 | SUPPORTED | **The order's STATED LIMITATION is built in as a refusal, and the delegation confound is made a number.** With the proxy-filed count undeclared, `calibration` returns `UNESTIMABLE_PROXY_UNDECLARED` rather than a rho -- the per-operator prior is unestimable for exactly the operators it matters most for. `delegation_corruption` reads a calibrated world two ways: declared-and-excluded stays calibrated (rho ~0.999, TRACKS), pooling proxy-filers as zero-reporters pulls it down (rho ~0.56, DOES_NOT_TRACK). The confound can flip the verdict; that is the cost of not declaring. |
| RCL_009 | SUPPORTED | **`spearman` is imported from `readout-count`, not restated.** The correlation used in Test B is the same object `readout-count` registered and tested; `preentry_register.py` imports it and defines no `spearman` of its own, so the two folders cannot drift. |
| RCL_010 | UNVERIFIED | **Nothing here is a measurement, and two sibling orders are named-and-absent.** The order's Test A (operators + a shift), the real Test B (one plant's CMMS), Test C (a plant willing to change one thing), Test D (app entry records) and Test E (published ecology, a coding study) are NOT_RUN: the first four need operators or plant access this session does not have, and the ecology corpus is egress-blocked. The order opens "Companion to WO-2" and cites WO-4's term-gap; neither is in this tree, and both are carried as named references, not reconstructed. The DERIVED incentive-composition claim is established as ARITHMETIC here and remains unrun on any real chain. |

## What this folder does not establish

- That any real reporting chain estimates its incentive stack. The
  composition is exact in a constructed linear-Gaussian model; whether a real
  chain has directed per-hop loss of a size that matters is the order's
  DERIVED claim and is unrun.
- That any operator's non-reporting is calibrated. Test B's calibration is
  demonstrated on constructed operators to show the classifier separates the
  two worlds; the order's real Test B needs a CMMS.
- Anything about governance or municipal code chains, which the order says
  lose the independently recoverable ground truth that makes maintenance
  scorable.
