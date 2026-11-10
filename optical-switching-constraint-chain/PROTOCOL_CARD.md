# OSC-WO3 protocol card: the barrier of an optically written bit

Written, not run. This is the measurement the report names as its
terminal node (§6.4). It needs a lab with a vector-beam write setup, a VSM
or MFM, and a temperature stage. Everything below is a specification for
whoever has those.

## What is measured

Δ = E_B / k_B T of a bit **written by light** in a continuous Co/Pt
multilayer. This is not the barrier of the field-saturated film, which is
a different energy and the one the literature usually reports.

## Sample

- [Pt(0.7 nm)/Co(0.6 nm)]_N with N = 5, 7 and 9, the range where the UCSD
  work writes deterministically at NA ≥ 0.8.
- Write conditions recorded per bit: NA, spot diameter, fluence (measured
  at the sample, not borrowed from another experiment; see OSC_005),
  pulse count, repetition rate, helicity.

## Three forms, in increasing directness

| form | what it reads | cost | what it cannot separate |
|---|---|---|---|
| A. ensemble decay | net magnetisation of a dense written array vs time, at several temperatures | days | written-bit barrier from film barrier |
| B. Sharrock on the written state | remanent coercivity of the written array vs waiting time | days to a week | per-bit spread |
| C. MFM tracking | individual written bits, repeatedly imaged at 60–80 °C | weeks | nothing; this is the object itself |

## Controls (run on the same sample, same day)

1. **Field-saturated film, same N.** Sharrock on the film, to separate the
   written-bit barrier from the film's own.
2. **Unwritten neighbourhood.** Tracks spontaneous nucleation that has
   nothing to do with the write.
3. **A planted check of the fit.** Run `sharrock.py` on the logged
   (t, H_c) pairs, and on constructed data with a known Δ, before reading
   any real Δ.

## Fit and declared terms

- Fit form: H_c(t) = H_c0 (1 − √((k_B T / E_b) ln(f₀ t / ln 2))). Plotted
  against √(ln(f₀ t / ln 2)) this is a line, and Δ = (intercept/slope)²
  (`sharrock.py`).
- **f₀ is declared, not fitted.** Report Δ as a band over a declared f₀
  range, e.g. 10⁹–10¹⁰ Hz. At Δ ≈ 50, one decade of f₀ moves Δ by about 2.
- Waiting times span at least four decades (1 s to 10⁴ s or longer).
- Temperatures: at least three, with the stage reading logged.

## Routing (fixed now, before any data)

Feed the Δ band into `decision.py`, with the single-bit line at
ln(t/τ₀) for 10 years and τ₀ declared, and the population line declared
with its basis:

| readout | route the report assigns |
|---|---|
| ABOVE_POPULATION_LINE | Co/Pt plus a plasmonic amplifier becomes the recording route |
| BETWEEN_LINES | cache-class with refresh or ECC |
| BELOW_SINGLE_BIT_LINE | continuous film is a physics platform, not a medium |
| STRADDLES | no route; narrow the f₀ range or the measurement uncertainty |

## Kill condition for the card itself

If form C gives a Δ outside the band from form B on the same sample, the
Sharrock form does not describe these bits. The card is then wrong for
this system, and that result is the finding.
