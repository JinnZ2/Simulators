# thermal-coupling — claim table

Claims are about the two delivered modules checked against their own
docstrings, claim tables and demos. Both are imported and never edited.
None is a claim about any slope, snowpack, avalanche, or the literature
the modules cite, which was not read (allowlist egress).

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its
text and gains an UPDATE paragraph. Nothing in either delivered module is
retuned — the modules' own protocol says the same.

| id | claim | status |
|---|---|---|
| TCA_001 | the CAL_FOS calibration sentence holds under a flag it does not name and not under the default | SUPPORTED |
| TCA_002 | TC-04 is refuted by the module's own function on the claim's own criterion: sensitivity falls toward 0 C by a factor of 3.7 | SUPPORTED |
| TCA_003 | "CAL_FOS is the ONLY free parameter" against a census of 35 numeric literals in function bodies, seven functions carrying literals with no source in their docstring | SUPPORTED |
| TCA_004 | TC-01 holds: five lag classes over 4.56 decades | SUPPORTED |
| TCA_005 | TC-02's product form is shown in the module's own arithmetic and not tested; its falsifier is an event set and none is here | SUPPORTED |
| TCA_006 | TC-03's freeze-thaw half is produced by the code (interior peaks at ±3, a dip at 0) and its snow half is asserted in a docstring the code does not implement | SUPPORTED |
| TCA_007 | TC-06's runout multiplier enters no downstream term; count falls while runout rises on the sweep, and coincidence tracks the count | SUPPORTED |
| TCA_008 | the module names a home folder that does not exist and cites the tree's most-cited absent object; one header source is used in no function | SUPPORTED |
| TCA_009 | the extension's meltwater calibration sentence is not produced by the function it sits on: the ratio is 6.00 by construction, the docstring says 2.3 | SUPPORTED |
| TCA_010 | the extension's coupling bounds reproduce (8.9–18.4) and its blast anchors do not (13.0 against >15, 3.9 against 2.5) | SUPPORTED |
| TCA_011 | the extension copies the core's LAG table rather than importing it, reads none of the core's terms, and TC-10's directional claim is in no function | SUPPORTED |
| TCA_012 | F1, F2 and F3 hold as facts about the core module | SUPPORTED |
| TCA_013 | nothing here bears on any hazard; every anchor is carried from the modules and unchecked | UNVERIFIED |

## TCA_001 — the calibration sentence

*"A 50 deg slope warmed from -4 C crosses FoS = 1 somewhere between -3
and -0.5 C. This value puts the crossing at -2 C."* With
`fracture_favorable=True` (critical angle 50, geometry factor 1) the
crossing is at −1.99 C. With the default (critical angle 62) a 50° slope
never crosses on the domain; FoS at −0.5 C is 1.29. The sentence is
true under the flag it does not name and false under the flag a caller
gets by default.

## TCA_002 — TC-04 against its own function

TC-04: *"strength loss is convex toward 0 C: sensitivity rises as
temperature approaches melting."* The function's loss is
`0.71 · x^0.55`, concave in x, so the loss flattens toward 0 C. The
first derivative of strength is −0.155 /K at −9.5 C and −0.042 /K at
−1 C: sensitivity FALLS toward melting by a factor of 3.7. The inline
comment reads *"convex: steeper near 0"* against code that is the
opposite. The claim states its own criterion, the module's function
fails it, and `creep_sensitivity` (an exponential) is the shape the
docstring describes and the strength function is not. Per the module's
own protocol: update the claim, do not retune; TC-04 as delivered is
refuted by its implementation, and the cited source's direction is what
the docstring says, not what the code does.

Falsifier for this audit: a reading of TC-04 under which a sensitivity
falling toward 0 C satisfies "rises as temperature approaches melting."

## TCA_003 — the only free parameter

Counted by AST over function bodies, excluding structural constants (0,
1, 2, 100, 365, 10.0): 35 numeric literals. Seven of ten functions
carry literals with no source named in their docstring — the logistic
widths 0.4 and 0.3, the 6.0 K diurnal amplitude, the 3.2 in the creep
exponent, the 60-year debuttress constant, the priming window (1.60,
0.80) and the coincidence weights. CAL_FOS is the only parameter
*labelled* free; it is not the only one that is.

## TCA_004 — TC-01

Five classes; the ratio of the longest to shortest tau is 36,500, which
is 4.56 decades. Holds as arithmetic on the module's own table.

## TCA_005 — TC-02

On Demo D's three scenarios the product returns 0 for the unprimed slope
and an additive mean of the same four factors returns 0.23; the ranking
is the same under both. The product form is the claim, demonstrated in
the module's own arithmetic. Its falsifier is an event set on which
additive scoring predicts as well, and no event enters the module.

## TCA_006 — TC-03, half and half

Freeze-thaw cycles against mean temperature: 98 at ±12, peaks of 222 at
±3, a dip to 169 at 0, symmetric about zero. Non-monotone, produced by
the code. The snow half — *"warming THINS the pack at low elevation,
which RAISES the gradient"* — lives in a docstring; `depth_m` is an
input, is never assigned in the module, and `weak_layer_index` returns
the same value at any temperature for a fixed gradient. The elevation
non-monotonicity TC-03 claims for snow is asserted, not produced.

## TCA_007 — TC-06 and the coincidence term

Sweeping snow temperature at Demo D's primed slope, the total count
falls from 0.400 to 0.367 between −4 and −1 C while the runout
multiplier rises from 1.00 to 1.18 — count down, runout up, which is
TC-06's mechanism. Coincidence tracks the count (0.133 → 0.122), because
`runout_multiplier` is computed in `avalanche_activity` and read by no
downstream term. What TC-06 says rises is a quantity the module's own
headline number does not contain.

## TCA_008 — referents

The module calls itself a MARKER for `earth-systems-physics`, a folder
that does not exist. It cites `[[rate-mismatch-polytope]]`, which
thirteen other files in the tree cite and which exists nowhere — now the
most-cited absent object in the repository. Biskaborn's +0.19 C is in the
header's PARAMETER SOURCES and used in no function.

## TCA_009 — the extension's calibration sentence

`meltwater_index` is `k · max(0, t_air + 5) · duration`. Its docstring
says it is *calibrated so the Langtang case reproduces the published
ratio 74,000 t at −1 C → 170,000 t at +19 C (2.3×)*. The ratio of the
function at 19 C to −1 C is (19+5)/(−1+5) = 6.00, whatever the coupling
coefficient, and the module's own demo prints 6.00 on the row beside
"published 2.30". No parameter in the function can make the ratio 2.3
except `t_core_c`, which the sentence does not name as calibrated. The
sentence is not produced by the function it sits on.

## TCA_010 — the anchors

`(0.30/0.07)^1.5 = 8.87` and `(0.30/0.07)^2.0 = 18.37`: the header's
8.9–18.4 reproduces. At 57 m/s with full snow entrainment the mean
pressure is 13.0 kPa against an anchor of ">15"; with none it is 3.9
against 2.5. The footprint anchor (0.8 km² at 10 kPa) reproduces
exactly, because it is the formula's own normalisation. The diurnal
maximum falls at 15 h and the minimum at 3 h, as the docstring says.

## TCA_011 — a copy, not an extension

The extension's header reads *"Extends thermal_coupling.py, does not
replace it"*. It does not import the core. It re-declares `LAG` with
the core's five classes plus one; the five are identical today, and
identical is the state a copy starts in (`MF_019`). It reads none of the
core's terms: the runout multiplier TC-06 turns on is not consumed, and
TC-10's lateral/longitudinal split appears in no function of either
module. What the extension adds is real (a blast term, an air term, an
hour term) and it is attached to the core by prose.

## TCA_012 — F1, F2, F3

Read from the core's source: the thermal driver is `t_snow_c` and no
air temperature appears (F1); the string "blast" does not occur (F2);
the fastest lag class is snowpack at 1/365 yr (F3). The extension's
diagnosis of the core is exact on all three.

## TCA_013 — UNVERIFIED

Every physical number is carried from the modules' docstrings and
demos. None was checked against Mamot, Steinkogler, Zhuang or any other
cited source, and nothing here is a statement about any slope.
