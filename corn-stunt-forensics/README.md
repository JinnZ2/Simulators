# corn-stunt-forensics

A **forensic pass** run on a natural system, as a safe test of the
operator's backward-in-time method. The subject is the 2024 corn stunt
(*Spiroplasma kunkelii*, vector *Dalbulus maidis*) outbreak in the US
corn belt.

**What this folder is.** A record of one analytic pass and its output,
landed so the method's product survives the session that produced it. It
is not an epidemiological finding, not a recommendation to any grower,
and not a model. No field, trap, farm or extension office supplied data
here; every external fact is `[CARRIED]` from recall or from a relayed
source, and the one 2026 source named in the pass was **not retrievable**
(egress is an allowlist; the publisher host refused CONNECT), so it is
carried and unchecked.

**Recovery note, stated first.** This pass was produced
conversationally. The session hit its context limit before the folder was
written, and the summary carried across the break retained the method,
the biology, the hypothesis and the gap list, but **not** the full
dissonance table (rows D1, D2, D4, D5) or the per-bin timeline cells.
Those are recorded below as `NOT_RECOVERED` rather than reconstructed,
because reconstructing a dissonance row from memory of its label would
put a finding in the method's mouth that the method did not produce. The
one row that did survive with its content, D3, is the one the pass turned
on.

---

## 1. The method, as the operator states it

Not built as code here. Four moves, in the operator's terms:

- **Backward-in-time bins.** Start from the observed outbreak and scan
  backwards, binning what is known by how far back it sits, rather than
  building a forward narrative from a presumed origin.
- **Frame-cycle.** Re-read the same evidence under several frames in turn
  (agronomic, entomological, logistic, climatic), and record where the
  frames disagree instead of picking one.
- **Dissonance as the primary diagnostic.** The product of the pass is
  the set of places where two frames, or a frame and a record, do not
  agree. A dissonance is a measurement location, not an error to be
  resolved in the pass.
- **Gap as constructive.** An absence with a stated boundary is an
  output. *You never know what you are missing* is the reason for the
  pass, so the gap list is a deliverable and not a caveat.

**Angle of regard** is the operator's fifth term, from the security
version of the same method: which direction the observer is standing in
when they look. Recorded here because it is what selects which
dissonances are visible at all; it is not scored.

## 2. The biology the pass rests on — all `[CARRIED]`

| fact | status |
|---|---|
| Pathogen is *Spiroplasma kunkelii*; the vector is the corn leafhopper *Dalbulus maidis* | CARRIED |
| Roughly 20 days from a leafhopper acquiring the pathogen to becoming infective (latent period in the vector) | CARRIED, order-of-magnitude |
| Roughly 3 weeks from plant infection to visible symptoms | CARRIED, order-of-magnitude |
| Symptoms are confused in the field with drought stress, compaction and phosphorus deficiency | CARRIED |
| INTA (Argentina) advice includes staggered planting and volunteer-corn removal | CARRIED |

The two lags are what make the system a good test subject: **the signal
arrives after the window in which it could have been acted on**, which
is the same shape as the off-gas pre-arm problem in
`battery-offgas-prearm/` and the reason that folder exists.

## 3. Output of the pass

### Dissonance rows

| id | content | state |
|---|---|---|
| D1 | — | NOT_RECOVERED |
| D2 | — | NOT_RECOVERED |
| D3 | A **US second-season / irrigated host ladder**: a sequence of corn hosts available later in the season than the rain-fed main crop, which would let a vector population bridge a gap the main-crop calendar does not explain | HYPOTHESIS, unverified |
| D4 | — | NOT_RECOVERED |
| D5 | — | NOT_RECOVERED |

**Pass 1 was recovered.** The operator supplied it from the chat
transcript after pass 2 had landed; it is verbatim in
`PASS_1_RECOVERED.md`, and `COMPARISON.md` runs the two passes against
each other. The table below is left as it stood, since the
`NOT_RECOVERED` cells are what made pass 2 a clean re-run.

A second pass is in `PASS_2.md`. Its rows are numbered `D1'..D5'` /
`G1'..G5'` and are **new output, not a recovery** of the rows above;
pass 1's table is left as it stands. It is also **not** an independent
trial of the method, having been run with D3 in hand.

D3 is **a hypothesis the pass surfaced, not a conclusion**. Nothing here
establishes that such a ladder exists at the scale required, that it was
present in 2024, or that it carried the population. It is recorded
because it is checkable and because stating it is what the pass is for.

### Gaps

| id | gap | state |
|---|---|---|
| G1 | — | NOT_RECOVERED |
| G2 | — | NOT_RECOVERED |
| G3 | — | NOT_RECOVERED |
| G4 | — | NOT_RECOVERED |
| G5 | — | NOT_RECOVERED |

The gap list was five items and is not recoverable past the break. What
is recorded is the **buildable** set the gaps pointed at, below, which
survived with its content.

### Buildable now

1. **Infectivity-rate traps.** Trap counts alone measure vector
   abundance. The quantity that matters is the *infective* fraction, and
   the 20-day latent period means an abundance series leads an
   infectivity series by about three weeks. A trap programme that assays
   infectivity rather than counting is buildable with existing method.
2. **Port the rate-of-rise logic.** `battery-offgas-prearm/prearm.py`
   fires on the **slope** of a signal rather than its level, with a
   Theil-Sen median slope chosen over least squares because a single
   spike tripped the least-squares version. The same estimator over trap
   counts would be a rate rule on a noisy count series with the same
   glitch-rejection property. **Not built here**; recorded as the one
   piece of this tree that transfers.
3. **Volunteer-corn removal.** Carried from INTA. Removes off-season
   host, i.e. attacks the mechanism D3 names.
4. **Cross-neighbour planting-window compression.** Staggered planting
   protects the individual field and lengthens the regional host window;
   compressing the window across neighbours is the opposite move and
   cannot be taken by one grower alone. Recorded because the measure and
   the party able to take it are not the same party, which is the
   `route-independence/` shape.

## 4. What the pass does not establish

Whether the method found something real, or whether D3 is an artifact of
the six news-and-extension sources available to the pass. The pass had no
field data, no trap series, and no retrievable primary source. A
confirming reading from a corpus selected on the outbreak having happened
is the frame-selected-on-the-variable failure this repository records
repeatedly; nothing here escapes it.

## 5. Grading note

SELF-GRADED and worse: the party that ran the method is the party
reporting on it, and the method is the operator's. This folder's value is
that the hypothesis and the buildable list are now written where a second
party can attack them, not that either is supported.

## 6. Sources

Six news and extension items were consulted in the pass and are not
individually recoverable past the context break. One 2026 university
extension source was named and **not retrieved** (host refused CONNECT);
it is carried and unchecked. No source is cited here as supporting any
claim, because none was read into this folder.

CC0.
