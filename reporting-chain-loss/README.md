# reporting-chain-loss

WO-5: how much of a physical signal survives each hop between the machine and
the node that acts on it, and what never enters the record at all. Two
components, kept separate exactly as the order keeps them:

- **TRANSIT LOSS** (`hop_compose.py`) -- what degrades per hop once inside.
- **PRE-ENTRY LOSS** (`preentry_register.py`) -- what never enters the form.

`WORK_ORDER.md` is the order, landed **verbatim**. It opens "Companion to
WO-2" and cites WO-4's term-gap; neither sibling is in this tree, and both are
carried as named references rather than reconstructed. Everything built here
runs on CONSTRUCTED data -- nothing is a measurement of any plant or any
operator.

## TRANSIT LOSS -- the composition made a number

The order's formal floor is the data processing inequality: information about
a source cannot increase along a chain. That is a theorem and is used here as
the null, not re-derived. The order's GAP is that the DPI assumes a FIXED
transform, while organizational hops each carry their own objective function;
random loss cancels toward noise, DIRECTED loss compounds. The order asks what
the terminal output is an estimator OF.

`hop_compose.py` answers it in the one model where the answer is closed form,
a linear-Gaussian hop chain `x_n = a_n x_{n-1} + c_n + e_n`:

```
E[x_N | g] = (prod a_n) g  +  sum_k (prod_{j>k} a_j) c_k
             \___retained___/    \____incentive stack B____/
```

A reader who takes the terminal AS a scaled ground reading carries bias
`B / G`, and a lossy chain has `|G| <= 1`, so the rescaling AMPLIFIES: on the
shipped directed chain the reader's bias runs 1.11 (N=1) -> 5.24 (N=4) ->
43.97 (N=16). Directed offsets (same sign) compound with N; random offsets
(mean zero) cancel, their spread growing only as sqrt(N), so the
directed/random ratio grows with the chain. `composed_bias` is the
load-bearing metric and is registered in `tools/known_answer.py`. A zero and
an absence stay apart: no incentive gives an exact `0.0`, an unspecified gain
gives `None`, a dead hop gives `GROUND_UNRECOVERABLE` rather than an infinity.

## PRE-ENTRY LOSS -- the gates upstream of the form

`preentry_register.py` carries the order's seven gates (L0, L0', L1, L1', L2,
delegation, form-field), none logged, six of them conditioning which reports
arrive -- so the reports that arrive are a sample past a per-operator
threshold, not a sample of machine conditions, and the threshold is
unestimated.

It then builds the order's **Test B** on CONSTRUCTED operators: does a
reporting rate track the operator's own (acted on)/(filed) ratio? A calibrated
world reads `TRACKS_calibrated`, an independent world reads `DOES_NOT_TRACK`,
both reachable. The order's inverted finding -- non-reporting as a calibrated
estimate, not disengagement -- is the TRACKS branch.

The order's **STATED LIMITATION** is built in as a refusal: delegation-as-null
makes the per-operator prior unestimable for the operators it matters most for
(the ones who proxy-file read as zero-reporters), so with the proxy-filed
count undeclared `calibration` returns `UNESTIMABLE_PROXY_UNDECLARED` rather
than a number. `delegation_corruption` makes the cost a number: declared and
excluded stays calibrated (rho ~0.999), pooling proxy-filers as zero-reporters
pulls the correlation down (rho ~0.56) and flips the verdict. `spearman` is
imported from `readout-count`, not restated.

## Running it

```
python3 hop_compose.py            # the transit-loss composition
python3 preentry_register.py      # the register + Test B
python3 <module>.py --choices     # the [CHOICE n] markers
python3 test_hop.py               # the checks; prints their count
```

Both modules refuse `--selftest` (exit 2) and render on bare invocation. Both
renders screen clean through `sheet-structure-scan/no_severity` with no
exemption.

## Scope, carried from the order

The composition is exact ARITHMETIC on a constructed model; the order's DERIVED
claim -- that a real chain estimates its incentive stack -- is unrun on any
real chain. Test A (operators + a shift), the real Test B (a plant's CMMS),
Test C (a plant willing to change one thing), Test D (app entry records) and
Test E (published ecology) are NOT_RUN: the first four need access this session
does not have, the ecology corpus is egress-blocked. Permanent-id findings in
`CLAIM_TABLE.md` (`RCL_`). Stdlib only, parses under 3.9, phone-buildable, CC0.
