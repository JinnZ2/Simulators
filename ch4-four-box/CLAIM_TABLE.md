# ch4-four-box — claim table

Claims are about the two delivered scripts read against each other and
against their own arithmetic. Every published figure (lifetimes,
exchange parameters, ice-core concentrations, emissions) is carried from
the scripts and was not checked against the paper they cite, which is
not reachable from here. Nothing is a claim about the atmosphere.

## REFUTATION_PROTOCOL

A refuted claim is updated forward with a new id; the old id keeps its
text and gains an UPDATE paragraph. Neither delivered script is edited.

| id | claim | status |
|---|---|---|
| FB_001 | the constants' identities hold, and Tg-per-ppb per box is exactly a quarter of the global 2.848 | SUPPORTED |
| FB_002 | the RATES reading reproduces the published polar-only emissions to within 4.2 Tg/yr per box; the TIMES reading misses by 47.7 and produces a negative southern source | SUPPORTED |
| FB_003 | the two scripts' transport matrices agree under the rates reading, so the diagnostic runs on the forward model's operator | SUPPORTED |
| FB_004 | with the tropical box prescribed at the SCA value and the southern box at WAIS, the forward model returns a negative southern source; the diagnostic's closure gap is 59.3 ppb | SUPPORTED |
| FB_005 | the consistency scan and the emissions fit do not select the same transport: the reading that fits the emissions yields a polar gradient about 3.1× the observed one | SUPPORTED |
| FB_006 | the forward operator passes two known answers: no transport gives E = C/lifetime, and a uniform concentration moves nothing between boxes | SUPPORTED |
| FB_007 | nothing here bears on any emission or gradient; every published number is carried | UNVERIFIED |

## FB_001 — identities

IPD is 700 − 652 = 48. SCA at 746 is GISP2 + 46 and WAIS + 94, both as
the comment says. The +SCA TS emission, 125, is 213 − 88. The published
attenuation is 163/213 = 0.765. Moles of air × 16 g/mol × 1e-9 gives
2.848 Tg per ppb globally and the scripts' per-box value is that over
four, 0.712, to machine precision.

## FB_002 — which reading

The forward script offers the transport parameters two ways and prints
both. Under the rates reading the polar-only run returns 34.5 / 83.8 /
79.3 / 14.2 against a published 36 / 82 / 81 / 10, largest residual 4.2
Tg/yr in the southern box. Under the times reading the northern box
reads 83.7 against 36 and the southern box is −6.0, a negative source.
The closure script's header says the rates reading reproduces the
published run; the residuals say the same.

## FB_003 — one operator

The forward script's matrix under the rates reading and the closure
script's matrix differ by at most 2e-16. The two scripts declare the
same lifetimes, the same box order and the same Tg-per-ppb; the
diagnostic is a diagnostic of the forward model, not of a variant.

## FB_004 — the closure gap

With TS at 746 and SH at 652 the forward model returns a southern
emission of −10.8 Tg/yr; the paper is described as holding it at +10.
The diagnostic asks what TN reproduces the published tropical-north
emission (733.0 ppb, against a linear interpolation of 684.0) and then
what SH keeps the southern source at 10 with TS at SCA: 711.3 ppb,
59.3 ppb above the WAIS value. A prescribed southern concentration and
a prescribed southern source cannot both hold in a forward model; the
gap is the size of the disagreement in the concentration unit. The
resulting attenuation is 0.774 against 0.765.

## FB_005 — the scan and the fit disagree

The consistency scan scales the TIMES base and inverts the published
polar emissions for concentrations; the implied NH−SH gradient is 12.5
ppb at scale 1 and reaches the observed 48 at scale 4.34. The rates
reading is the times base scaled by 1/0.22² = 20.66, and there the
implied gradient is 150.5 ppb, 3.1× the observed. So the transport that
reproduces the published emissions from the published concentrations
is not the transport that reproduces the published gradient from the
published emissions. The scripts print the scan and the fit on
separate pages; this is the two read together.

## FB_006 — known answers

With no transport the operator is diagonal and E_b = C_b / τ_b exactly.
With transport, a uniform concentration across the four boxes returns
the same emissions as with none: the off-diagonal terms cancel in every
row, which is what a conservative exchange matrix has to do.

## FB_007 — UNVERIFIED

Lamantia et al. 2026 is named and not read; the lifetimes, the 0.22 /
0.45 parameters, the ice-core values and the published emissions are
the scripts' statements of the paper. Nothing here is a statement
about methane.
