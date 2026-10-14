# Experiment fruitfulness triage: five reversible-loop sites

CC0. A triage instrument. It orders five experiment sites by expected
information per unit of a reader's resources, so a reader picking this up
cold can choose where to look FIRST. It is not a claim that any site has
been validated, and it describes no person.

Companions: `tools/landauer_floor_vs_run_cost.md` (site 4's welded word
"cost"), `tools/bin_self_test.md` (the calibration move, section 7),
`tools/uncounted_observer_isolation.md` (the hold term), and
`tools/coupling_and_accumulation.md` section 3 (calibration vs stockpile).

Tags: OBSERVED = stated in a source and read; DERIVED = follows from what
is stated here, checked by computation where marked; PROPOSED = untested;
CARRIED = from the work order or from training memory, not checked here;
SEARCH-DEPTH = located by web search on 2026-10-13, abstract or snippet
only, full text not reachable from this environment.

```
STATUS OF THIS REVISION: post-calibration.
Section 7.2 is the blind fill of site 2, committed before any comparison
(commit d5f5c2a) and pinned by sha256 in the scorer. Sections 7.3 to 7.7
compare it with the published instance and record what changed.

TO RUN THE CALIBRATION CLEAN, STOP READING HERE. Run
    python3 tools/experiment_fruitfulness_triage.py --blind-packet
fill site 2 from that packet alone, hash the fill, then come back
(protocol: section 7.7). Below this block the published answer is named.
```

Scorer: `tools/experiment_fruitfulness_triage.py` (stdlib; section 8).
It is the work order's optional `score.py`, named after the rubric
so the pair sorts together in `tools/`.

## 0. Two things to carry, whatever else is dropped

1. TRIAGE, NOT VALIDATION. The rubric ranks where to look. Every site
   below is a question with a designed experiment; none has been run
   here.

2. BIDIRECTIONAL IS NOT REVERSIBLE. A net can pass signals both ways and
   still erase information at every step. The payoff claimed at sites
   2-5 lands only if the loop RETAINS state AND CAN RECOVER earlier
   state. Every site's field (f) states which of the two its experiment
   tests, and the score splits on it (section 2.3).

## 1. Occasion (CARRIED; nothing below rests on it)

- Decision-related signals in mouse primary somatosensory cortex (S1),
  with top-down feedback. The work order says "PNAS/UIUC (July 2026)".
  SEARCH-DEPTH: one search located Armstrong and Vlasov, "Neural
  correlates of perceptual decision-making in the primary somatosensory
  cortex", PNAS, DOI 10.1073/pnas.2514107123, dated 29 April 2026, with
  press coverage in July 2026. A second search found the bioRxiv preprint
  (2025) and a 2026 seminar abstract naming S2 -> S1 feedback, and did
  not find the PNAS listing. Press coverage reports the authors saying
  the study is not a blueprint for AI design. The step from "S1 runs
  feedback" to "the feedforward presumption in AI has a crack" is the
  work order's reading and the press's, not the paper's.
- The 2022 paper the work order names as site 2's worked instance. Its
  specifics are withheld until section 7.3, so the blind fill in 7.2 is
  bounded by what the work order itself says.
- The general pattern ("the constraint generates the form") is the work
  order's. PROPOSED. One instance, site 2, is checked against it in
  section 7.

## 2. The shared question, the comparison class, the named goal

### 2.1 The update being unfrozen

```
one stage l, discrete time t:

  h_l(t+1) = f( W_l h_{l-1}(t) + U_l h_l(t) + g * V_l h_{l+1}(t) + b_l )
                bottom-up         lateral       top-down

feedforward      = the snapshot U_l = 0, g = 0, one sweep
the inverse move = for which (g, loop delay / input timescale,
                   input statistics, imposed constraint) does g != 0
                   do work, and what does it pay
```

### 2.2 "Feedforward cannot" needs a declared comparison class [DERIVED]

Left undeclared, the question answers itself both ways.

- Depth unbounded: the fixed point of a contracting, weight-tied,
  input-injected loop equals the output of an infinitely deep
  weight-tied feedforward net (DEQ: Bai, Kolter, Koltun 2019,
  SEARCH-DEPTH). With depth free, a contracting loop never does what
  feedforward cannot.
- Window of one: a memoryless map of the current input never shows
  hysteresis. With the window fixed at one input, a multistable loop
  always does what feedforward cannot.

So every site declares the class it is compared against: parameter
count P, depth L, input window w. A loop exceeds a declared class in
four ways only:

```
E1  history beyond the window w     multistability, slow modes
E2  depth beyond L at the same P    iterations with tied weights
E3  compute that varies with x      settling time depends on the input
E4  one parameter set, two maps     recognition and generation (site 5)
```

and it costs less than the class in four currencies only (section 3.3).

### 2.3 The named goal

"Fruitful" is a ratio, and a ratio against an unnamed goal is the
efficient / deficient bin (`tools/bin_self_test.md`). Named here:

```
fruitful = expected reduction in uncertainty about the shared
           question, per unit of the reader's resources
```

The shared question, split so the honest edge cannot be merged away:

```
Q-LOOP  does feedback or persistence do work the declared feedforward
        class cannot, or the same work at lower cost?
Q-REV   does RETAIN + RECOVER (the step map injective on the retained
        degrees of freedom) change the cost, and in which currency?
```

Each experiment is scored against both, separately. One that cannot
test recovery has no Q-REV score at all: it is NOT_REACHED, never zero.

## 3. The retention edge, made checkable

### 3.1 Three properties, three tests

```
property       what it is             the test (RUN it; a wiring
                                      diagram is not a test)
-------------  ---------------------  ----------------------------------
BIDIRECTIONAL  signals run both ways  connectivity: V != 0 or U != 0
PERSISTENT     state survives across  reset the state between inputs:
               steps or inputs        does behaviour change?
REVERSIBLE     earlier state is       run the inverse: from (state_t+1,
               recoverable from       output_t) rebuild (state_t,
               later state            input_t); report bits lost per
                                      step, H(state_t, input_t |
                                      state_t+1, output_t). 0 means
                                      reversible.
```

Bidirectional does not imply persistent (a feedback net reset per
input). Persistent does not imply reversible (an attractor keeps one
basin label and merges the rest). Reversible does not imply loop: a
feedforward net built from additive-coupling blocks is reversible
(RevNet, i-RevNet; site 4). The payoff at sites 2-5 belongs to
REVERSIBLE, so field (f) names which row its experiment reaches.

### 3.2 R1 - settling is erasure [DERIVED; arithmetic checked]

An attracting fixed point maps every state in its basin to one state.
On a grid of b bits per dimension, one step of a contraction by rho
merges states:

```
bits merged per step, per contracting dimension
  state count (Hartley)             log2(1/rho)
  Shannon, from a uniform start     2(1 - rho)     for 1/2 <= rho <= 1
  Shannon >= Hartley always (an entropy never exceeds log2 of its
  support)

checked here: one step of x -> floor(rho * x) on a 12-bit grid
  rho    Hartley   log2(1/rho)   Shannon   2(1 - rho)
  0.50   1.0000    1.0000        1.0000    1.0000
  0.75   0.4150    0.4150        0.5000    0.5000
  0.90   0.1522    0.1520        0.2002    0.2000
```

So an earlier state survives at most k* ~ b / log2(1/rho) steps back. A
logically reversible map on a finite set is a permutation, and a
permutation has no attractor: every orbit is a cycle.

Consequence: sites 1 and 3 want settling; sites 4 and 5 want recovery.
On the SAME degrees of freedom they conflict. A loop gets both only on
different degrees of freedom: a settling channel beside a history
channel (Bennett 1973: compute, copy the answer out, uncompute;
CARRIED).

The conflict in published form: a perfectly reversible RNN cannot
discard information from its hidden state and fails a one-step
prediction task; the fix stores a handful of bits per unit so that
forgetting can be undone, for 10-15x less activation memory (MacKay,
Vicol, Ba, Grosse 2018, NeurIPS; SEARCH-DEPTH). Forgetting was not
removed. It was moved into stored bits.

### 3.3 R2 - the bit ledger [DERIVED; identity checked]

```
deterministic processing of input X to output Y:

  H(X) = H(Y) + H(X|Y)
  bits_in = bits_out + bits kept + bits erased

a chain X = h_0 -> h_1 -> ... -> h_L = Y of deterministic stages:

  SUM_{l=1..L} H(h_{l-1} | h_l) = H(X) - H(Y) = H(X|Y)

checked here: 8-bit uniform input, three many-to-one stages
  H per stage              8.0000  5.9245  3.1520  2.0386
  SUM H(h_{l-1} | h_l)     5.9614 = H(X) - H(Y) = H(X|Y) = 5.9614
  blind overwrite          SUM_{l<L} H(h_l)        = 17.0765
  blind minus the floor    SUM_{l>=1} H(h_l)       = 11.1151
```

Three readings follow.

1. Stage count adds nothing at the floor. A pass that erases each stage
   with the next stage present as side information pays H(X|Y), the
   same as the end-to-end map.
2. Blind overwrite (each register erased without side information) costs
   more, by SUM_{l>=1} H(h_l). That excess is a property of erasure
   PRACTICE. A pass has the next stage in hand when it erases the
   previous one, so the excess is not a property of loops.
3. A bounded-state loop cannot keep growing what it keeps, so averaged
   over a long stream it erases bits_in - bits_out per input: the same
   as a pass with the same input and output.

So a retained-state design beats a pass at the floor only by paying in
another currency. A claim of lower erasure that names none of the four
has not said where the erasure went.

```
SPACE     keep more          retained bits grow (MacKay et al.'s
                             stored bits)
EXPORT    output more        bits_out grows
TIME      uncompute          extra steps back before reset
PRACTICE  side-information   where the pass overwrites blind
          erasure
```

### 3.4 R3 - retention is not free unless it predicts [SEARCH-DEPTH]

Still, Sivak, Bell, Crooks 2012 (PRL 109:120604): for a system driven by
a stochastic signal, retained information that does not predict the
future bounds dissipated work from below,

```
I_mem - I_pred <= beta <W_diss>
```

(as restated by a later paper; the derivation is not read here). The
minimum-dissipation retained state is the predictive one. Sites 2 and 4
are one optimization seen from two sides.

### 3.5 R4 - the floor is not the run cost

The Landauer floor sits about 1e6 below the energy per operation of
current transistors (`tools/landauer_floor_vs_run_cost.md`, OBSERVED
there). A 2025 preprint argues that quasi-static inference in a physical
network carries no cost attached to the computation itself, with
finite-speed relaxation setting the unavoidable cost (Tkachenko, arXiv
2503.09980; SEARCH-DEPTH, preprint). A bit-count win at any site is a
statement about the floor until a substrate's dissipation model is
named.

## 4. The fields

```
(a)  FOUND        a confirming result: a quantity, a comparison, a
                  direction of effect
(b)  SCOPE        a clean negative. It bounds where the effect can
                  live; it is information, not "nothing found"
(b') UNRESOLVED   what inconclusive looks like, kept apart from (b)
(c)  MDE          the cheapest test that separates (a) from (b)
(d)  COST         compute / data / literature / time: low, medium, high
(e)  ANCHOR       published results to compare against, located before
                  assuming there are none
(f)  RETENTION    which of BIDIRECTIONAL / PERSISTENT / REVERSIBLE the
                  MDE reaches; whether it reaches Q-REV
(g)  EMERGENCE    ADDED BY THE CALIBRATION (section 7.6). Impose only the
                  constraint (an objective, a budget, a noise level),
                  wire nothing, and ask whether the site's mechanism
                  appears and where. Fields (a)-(f) ask what a designed
                  experiment returns; (g) asks what a constraint
                  generates
```

found / scope / unresolved is the work order's convention, kept as three
outcomes. Fields (a)-(f) are the work order's; (g) is not, and is marked
where it appears.

Cost levels, declared:

```
          low                   medium                  high
compute   stdlib, minutes;      laptop, hours;          GPU or cluster,
          a phone runs it       numpy-class             days
data      none or synthetic     a public download       collected or
                                                        private
lit       none or textbook      abstracts, snippets     full text
time      one session, hours    days                    weeks
```

## 5. The five sites

### Site 1 - STABILITY CONDITIONS

Restated [DERIVED, 2.2]: the contracting regime (one stable fixed point)
computes what a deep enough weight-tied feedforward net computes; the
regimes beyond the declared class (multistable, oscillatory, chaotic,
slow modes) begin at the stability edge. "Gradient as a design variable"
becomes a boundary question: does the edge MOVE with timing and input
statistics, or does gain alone set it?

**(a) FOUND.** At fixed gain, the boundary between the contracting regime
and the history-dependent regime shifts measurably with loop delay or
with input strength, frequency or autocorrelation; and inside the
history-dependent band at least one behaviour exceeds the declared
class (E1-E3): hysteresis area > 0 under an up-down input ramp, linear
memory capacity MC > w, or a settling time that varies with the input.

**(b) SCOPE.** The boundary sits at the same gain for every timing and
input statistic in the swept box: gain alone sets it. Or the contracting
region fills the box and matches the declared class within tolerance
everywhere. Either bounds the loop's extra work to a single gain
threshold.

**(b') UNRESOLVED.** A boundary shift smaller than the grid step or the
seed-to-seed spread (a grid coarser than the feature); hysteresis inside
numerical noise.

**(c) MDE** [stdlib, minutes].

```
1. known answer first: one unit, h(t+1) = tanh(g * h(t) + x).
   At x = 0, tanh'(0) = 1: one fixed point for g < 1, two stable ones
   for g > 1. A pipeline that misplaces this is wrong.
2. N = 16 units, W random, scaled to spectral radius 1.
   sweep g in [0, 2] (41 steps); loop delay tau in {1, 2, 4};
   inputs: constant; sinusoid at 4 frequencies; white noise at
   3 amplitudes.
   per cell: distinct fixed points from 50 random starts; hysteresis
   area; MC = SUM_k r^2(x(t-k), linear readout); largest Lyapunov
   exponent (two trajectories, renormalized); recovery horizon k*
   (run the inverse map until reconstruction fails at b bits).
3. declared class: tanh MLP, same parameter count, window w = 4.
4. read: the critical gain g_c(tau, input). A g_c that moves is (a);
   a flat g_c is (b).
```

**(d) COST.** compute low | data low | literature low | time low.

**(e) ANCHOR.** Yes, and one is already a partial (a).

- Sompolinsky, Crisanti, Sommers 1988 (PRL 61:259): transition to chaos
  at g = 1 in large random networks. CARRIED.
- Rajan, Abbott, Sompolinsky 2010 (PRE 82:011903): input suppresses the
  chaotic activity, and the critical input intensity depends
  non-monotonically on stimulus frequency. SEARCH-DEPTH. Input
  statistics and timing move the boundary: published, for random
  networks, with no declared comparison class.
- Boedecker et al. 2012 (Theory Biosci): information storage and transfer
  maximal near the edge of chaos. SEARCH-DEPTH. arXiv 1912.11213:
  short-term memory optimal BEFORE the edge in driven networks.
  SEARCH-DEPTH. Singh, Sankaranarayanan, Raman 2025 (arXiv 2507.18467):
  the echo-state property plus Lipschitz dynamics give fading memory;
  memory capacity tied to the Lyapunov spectrum. SEARCH-DEPTH.
- Bai, Kolter, Koltun 2019 (NeurIPS, DEQ): the equilibrium of a
  weight-tied, input-injected net equals an infinite-depth feedforward
  net. SEARCH-DEPTH. Anchors branch (b).
- Huang, Zhou, Huang, Zhou 2024 (Sci China PMA 67:260511; arXiv
  2302.11681): in linear lateral predictive coding, an
  energy-information trade-off drives continuous and discontinuous
  phase transitions in the weight matrix. SEARCH-DEPTH. Regime structure
  moving with an imposed constraint: the bridge to site 2.

Open after the anchors: the budget-matched comparison, and the delay
axis.

**(f) RETENTION.** Reaches PERSISTENT (hysteresis, MC). Does not reach
REVERSIBLE through its success criterion: a stable fixed point merges
its basin (R1). Reaches REVERSIBLE partially through two readouts: MC
(linear recoverability of past inputs) and the recovery horizon k*,
which states how far back a given stability margin lets recovery reach.
Q-REV: partial.

**(g) EMERGENCE** (added by the calibration). Train gain and delay instead
of setting them, under a cost on activity or on settling time, and read
where the trained loop sits relative to g_c. A cost that alone places
the loop near the edge would make the stability boundary an outcome of
the constraint. Not scored; compute medium.

### Site 2 - COMPRESSION PAYOFF

The blind fill is section 7.2 and stands as committed. This is the
informed entry, written after section 7.3; section 7.6 lists what the
comparison changed.

Restated [DERIVED]: with bits = -log2 p(arrived), "better prediction ->
fewer bits" holds by definition. The falsifiable step is "fewer bits ->
lower cost", and it needs the top-down channel charged its own bits:

```
rate(top-down) + rate(residual)  <  rate(input)

saving per symbol <= I(x_t ; context)      no context, no saving
```

A residual can also shrink because input was thrown away, so the round
trip (rebuild x from residual plus prediction) is part of the test.

**(a) FOUND.** On a stream with predictable structure, the loop that
predicts top-down and sends the residual pays fewer total bits (residual
plus top-down, both counted) than the pass that sends the input; the
input is rebuilt exactly; the saving tracks I(x_t ; context) and is near
zero on a shuffled control. Emergence form, field (g): a loop given only
an activity or code-length cost, with nothing wired, develops units that
carry the prediction and units that carry the mismatch.

**(b) SCOPE.** Total bits do not fall once the top-down channel is
charged; or the residual shrinks only because input is lost (the round
trip fails); or, in the emergence form, the roles fail to appear when
the low-variance region is removed or when the penalty moves after the
nonlinearity. Each bounds the claim to "a code-length saving that the
round trip and the top-down charge leave standing".

**(b') UNRESOLVED.** A saving inside the seed-to-seed spread; a stream with
no context dependence; an emergence result read from activity maps with
no lesion and no decoder.

**(c) MDE.**

```
S2a [stdlib, minutes]   the blind fill's design (7.2): a symbol stream
    with tunable context dependence; ideal code length without context
    (the pass) and with it (the loop); the top-down channel charged;
    a shuffled control; the lossless round trip
S2b [numpy-class, days]  field (g): a small recurrent net on a synthetic
    predictable sequence, trained with an L1 cost on pre-nonlinearity
    activity and nothing wired; roles identified by lesion and by a
    linear decoder; then the flip: remove the low-variance units and
    retrain
S2c [replication]        the published setup (section 7.3)
```

**(d) COST.** S2a: compute low | data low | literature low | time low.
S2b: compute medium | data low | literature medium | time medium. S2c:
compute medium | data medium | literature high | time medium.

**(e) ANCHOR.** Two, of different kinds.

- Source coding: the expected code length of a stream of known
  statistics is fixed (Shannon), and arithmetic coding comes within a
  few bits of it. The known answer for S2a. CARRIED, textbook.
- The published instance, section 7.3. SEARCH-DEPTH. The known answer
  for S2c, and a qualitative one for S2b.

**(f) RETENTION.** S2a and S2b reach REVERSIBLE through the round trip:
the input is rebuilt from the residual plus the receiver's own copy of
the prediction (or from the state, by the decoder), or the bits lost are
counted. ADDED BY THE CALIBRATION: the cost measure must be a lossless
code length or a pre-nonlinearity activity, never a post-nonlinearity
output alone. [DERIVED] An output penalty can be met by driving units
into the flat part of the nonlinearity, which makes a smaller number by
destroying input; the published comparison of the two placements is
section 7.3, P7. Q-REV: reached (S2a, S2b); partial (S2c: the reported
quantities include no reconstruction test, P8).

**(g) EMERGENCE.** S2b. The published instance is an emergence result,
and the blind fill had no field it could land in (section 7.4, P1).

### Site 3 - DORMANT-FACE COST

Restated [DERIVED]: two claims bundled.

```
DORMANCY    only the part of the structure the input couples to
            changes state
RE-SETTLE   repeated exposure settles faster

for a contraction with rate rho, iterations to tolerance tol from
distance d are about log(d / tol) / log(1/rho), so a warm start from
the retained fixed point saves about

    log(d_cold / d_warm) / log(1/rho)    iterations

which grows as rho -> 1: largest where cold settling is slowest
(site 1).
```

Both claims need a cost model in which quiet units cost nothing. On
dense hardware (every unit computed every step) the dormancy saving is
zero by construction, and the site's readout is silent there.

**(a) FOUND.** On an activity-proportional cost model: the count of
units whose state changes is predicted by the input's coupling
footprint; the re-settle saving follows the warm-start law (scales with
fixed-point proximity and with 1/log(1/rho)), vanishes under a
state-reset control, and survives with weights frozen; and a
feedforward control with per-unit delta coding at matched input
statistics does not reproduce the input-specific saving profile.

**(b) SCOPE.** The per-unit-persistence feedforward control reproduces
the saving profile, so the saving is persistence and not feedback; or
the saving vanishes on the declared substrate's cost model. Either
bounds the claim to "needs persistence and an activity-proportional
substrate", not "needs a loop".

**(b') UNRESOLVED.** A saving present while state, adaptation and
plasticity give the same curve on the tested inputs.

**(c) MDE** [stdlib, minutes].

```
fixed-point iteration h <- tanh(W h + U x)
W modular (4 blocks) or dense; rho in {0.3, 0.6, 0.9, 0.97}
inputs: exact repeats, and near-repeats at controlled distances
conditions: cold start | warm start | warm start + state reset |
            feedforward + per-unit adaptation | feedforward delta coding
cost models, reported apart, never merged:
            iterations | SUM active units (|dh| > theta) | dense FLOPs
read: does the warm-start saving fit log(d_cold/d_warm) / log(1/rho);
      does the delta-coding control match it
```

**(d) COST.** compute low | data low | literature low | time low.

**(e) ANCHOR.** Yes, qualitative.

- Bai, Geng, Savani, Kolter 2022 (CVPR, DEQ optical flow): the previous
  frame's fixed point starts the next frame's solve; only frame 0 is
  solved from scratch. SEARCH-DEPTH.
- O'Connor and Welling 2017 (ICLR, Sigma-Delta Quantized Networks):
  compute scales with the change in input and activations, not with
  network size; at least 10x claimed on video on suitable hardware, in
  a FEEDFORWARD net. SEARCH-DEPTH. This is the competitor branch (b)
  names.
- Summerfield et al. 2008 (Nat Neurosci 11:1004): repetition suppression
  in the human fusiform face area is weaker when repeats are unexpected,
  read as fulfilled expectation. Disputed: macaque inferotemporal
  suppression not modulated by expectation (Kaliukhovich and Vogels);
  the expectation effect gone when attention is diverted while
  suppression remains (Larsson and Smith). SEARCH-DEPTH. The one
  literature that measured the effect in brains has not separated the
  mechanisms: branch (b') is where that field stands.
- ADDED BY THE CALIBRATION (section 7.3, P4): in the published site-2
  instance the units that came to carry the prediction sat in the
  low-variance region of the input. If quiet units are where predictions
  live, a dormancy saving read off activity counts may be counting the
  prediction, not idleness. Coupling C6.

**(f) RETENTION.** Reaches PERSISTENT only. Re-settling from a retained
fixed point is a contraction from a nearby start, and the old fixed
point is overwritten (R1). A FOUND here says nothing about REVERSIBLE.
Q-REV: NOT_REACHED. To reach it, add one readout: after re-settling, run
the inverse and report how much of the previous fixed point survives
(k*). Faster settling erases more per step.

**(g) EMERGENCE** (added by the calibration). Train under a cost on change
(|dh| per update), not on activity, and read whether the units that go
quiet are idle or carry the prediction (C6). Not scored; compute medium.

### Site 4 - LANDAUER / ERASURE JOIN

Restated [DERIVED, R2]: at the floor, bits erased per input are set by
the function and by what persists, not by the architecture. The
property that changes erasure is REVERSIBLE, and it is orthogonal to
LOOP: a feedforward pass can be reversible (RevNet) and a loop can be
irreversible (any attractor network). So the site's question has a
predicted answer at the floor, "moved, not removed", and an open part:
which currency each design pays in, and what finite-speed dissipation
does on a named substrate.

**(a) FOUND.** Under a declared persistence boundary, the retained-state
design erases fewer bits per input than the pass computing the same
map, the gap equals the predicted blind-overwrite excess, and the
payment is counted in a named currency (SPACE, EXPORT, TIME, PRACTICE).
Or, on a named substrate model, finite-speed dissipation per input is
lower for the retained-state design at equal throughput.

**(b) SCOPE.** Under complete-cycle accounting (every register returned
to its start, only the output kept) all designs erase exactly H(X|Y):
the erasure moved into time or space. Or the floor gap exists and sits
about 1e6 below the run cost on every current substrate (R4), so it
reaches no energy budget. Both fix where the payoff cannot be.

**(b') UNRESOLVED.** The persistence boundary left undeclared ("erasure
cost" welded: floor, run cost or in-principle bound, as in
`tools/landauer_floor_vs_run_cost.md`); or reversibility approximate
(floating-point inversion leaks bits) and the leak not counted.

**(c) MDE** [stdlib, exact enumeration].

```
a 2x2, so that loop and reversibility are not confounded:

                  irreversible               reversible
  pass            quantized stages,          integer additive-coupling
                  blind overwrite            stages (RevNet-style)
  loop            attractor update,          coupling update plus stored
                  state overwritten          forget-bits (MacKay-style)

over every input of a small domain (<= 2^12 states), the same
input -> output map in all four cells:
  H(X), H(h_l), H(Y); the floor SUM H(h_{l-1} | h_l), which must equal
  H(X|Y); blind overwrite SUM_{l<L} H(h_l); bijectivity verified by
  counting distinct outputs; the uncompute run.
report a three-column ledger per cell, never merged:
  bits erased | bits kept | steps
```

Finite-speed variant: a stochastic-thermodynamics model of the bit
operations (an overdamped double well) with a declared protocol
duration.

**(d) COST.** Ledger: compute low | data low | literature low | time
low. Finite-speed: compute medium | data low | literature high | time
high.

**(e) ANCHOR.** Theory yes; the asked comparison, not located.

- Landauer 1961; Bennett 1973 (compute, copy, uncompute), 1982 (erasure,
  not measurement, carries the cost), 1989 (time/space trade-off).
  CARRIED. Berut et al. 2012 (Nature): the floor measured; OBSERVED in
  `tools/landauer_floor_vs_run_cost.md`.
- Still et al. 2012: R3 above. SEARCH-DEPTH.
- Wolpert 2019 (J Phys A; arXiv 1905.05669): stochastic thermodynamics of
  computation. SEARCH-DEPTH, existence only.
- Tkachenko 2025 (arXiv 2503.09980, preprint): R4 above. SEARCH-DEPTH.
- Gomez, Ren, Urtasun, Grosse 2017 (NeurIPS, RevNet): each layer's
  activations reconstructed from the next layer's; storage independent
  of depth and typically 10x or more smaller; accuracy nearly identical
  to same-size ResNets. SEARCH-DEPTH. Measured in MEMORY, not erasure.
- Jacobsen, Smeulders, Oyallon 2018 (ICLR, i-RevNet): invertible up to
  the final projection onto the classes, with the same ImageNet
  performance as the non-invertible nets; local inversion
  ill-conditioned, so an explicit inverse is supplied. SEARCH-DEPTH.
  Erasure moved to the last step.
- MacKay, Vicol, Ba, Grosse 2018: R1 above. The bits stored per unit ARE
  the bits forgetting would erase, so this is a published count of the
  site's quantity, in memory currency. SEARCH-DEPTH; the figure is not
  read here.

No head-to-head erasure measurement of a retained-state loop against a
feedforward pass was located (one extended search, 2026-10-13).

**(f) RETENTION.** This is the site where retain + recover IS the
measurand. The MDE reaches REVERSIBLE only if bijectivity is verified by
enumeration and the uncompute is run. Stored activations with no
recovery path are PERSISTENT only. Floating-point reconstruction must
report its residual in bits; i-RevNet's ill-conditioned inversion is
why. Q-REV: reached.

**(g) EMERGENCE** (added by the calibration). Charge the bits a step
overwrites to the training objective and read whether a coupling or
stored-bit structure appears unasked. MacKay et al. store forget-bits
by design; whether the structure falls out of an erasure cost was not
located. Not scored; compute medium.

### Site 5 - INVERSE-DIRECTION REUSE

Restated [DERIVED]: "a relation has no privileged direction" holds
exactly for bijections. A many-to-one recognition map discards H(X|Y)
bits; running the same weights backward cannot invert it without those
bits, which must be stored (a latent channel) or resupplied (sampled
noise). For a bijection X <-> (Y, Z), H(Z|Y) = H(X|Y): the latent
carries exactly what recognition discards. So the open question is not
whether one network can serve both directions (invertible networks show
that it can) but what the shared parameter set costs per direction
against two networks at the same TOTAL parameter count.

**(a) FOUND.** One network trained in one direction (1) recognizes
within a stated margin of a recognition-only network, (2) generates
within a stated margin of a generation-only network (likelihood, bits
per dimension), and (3) round-trips x -> forward -> backward -> x
exactly, at matched total parameter count against the two-network pair.

**(b) SCOPE.** The shared network pays more in at least one direction
than it saves in parameters at matched total count; or, for a
compressive task, it matches only by adding a latent that carries
H(X|Y). Bounds the claim to "reuse is free for bijections; for
many-to-one tasks the discarded bits must be stored or resupplied".

**(b') UNRESOLVED.** A comparison not parameter-matched; generation
judged by plausibility without the round trip.

**(c) MDE.**

```
identity check [stdlib]: an integer additive-coupling bijection
  X <-> (Y, Z) on a small domain; verify by enumeration that
  H(Z|Y) = H(X|Y); recognition = read Y; generation = sample Z given
  Y and run backward; the round trip is exact by construction.
  This checks the information accounting, not learning.
trained comparison [numpy-class]: a small invertible net against a
  classifier plus a generator at matched total parameters, on a 2-D
  toy distribution; per-direction margins; the round trip.
```

**(d) COST.** Identity: compute low | data low | literature low | time
low. Trained: compute medium | data low | literature medium | time
medium.

**(e) ANCHOR.** Yes, quantitative.

- Normalizing flows: NICE (Dinh et al. 2014), RealNVP (2017), Glow
  (Kingma and Dhariwal 2018): one parameter set run forward (density,
  encoding) and backward (sampling), with published bits per dimension.
  CARRIED.
- Ardizzone et al. 2019 (ICLR; arXiv 1808.04730): an invertible network
  trained on the forward process gives the inverse from the same network
  with no separate training; extra latent outputs capture what the
  forward map discards; the inverse pass yields the posterior.
  SEARCH-DEPTH.
- Undirected models (RBMs) use one symmetric weight set both ways; the
  Helmholtz machine (Dayan et al. 1995) trains two separate networks,
  the counter-design. CARRIED.

**(f) RETENTION.** The round trip IS the retention test: x' = x exactly,
or the bits lost counted. Plausible generation is not a pass: a
tied-weight autoencoder or an RBM generates plausibly while erasing at
its bottleneck. Two-way wiring without bijectivity fails. Q-REV:
reached.

**(g) EMERGENCE** (added by the calibration). Train one network in one
direction under a cost on total parameter count, and read whether an
invertible structure appears unasked. Not scored; compute medium.

## 6. Cross-site couplings

The sites are not independent; a result at one changes what another is
worth.

```
                   contraction rate rho   (site 1)
                  /                     \
   warm-start saving                     bits merged per step log2(1/rho);
   log(d_c/d_w) / log(1/rho)             recovery horizon
   (site 3)                              k* ~ b / log2(1/rho)  (sites 4, 5)

   predictive retention = minimum-dissipation retention   (2 <-> 4, R3)
   bits recognition discards = bits generation resupplies (4 <-> 5)
   a bit-count saving reads as energy only on a named substrate (4 -> rest)
```

```
C1  1 -> 3     the warm-start saving scales with 1/log(1/rho);
               largest near the edge
C2  1 <-> 4    settling is erasure; one rho sets settle speed and merge
               rate
C3  2 <-> 4    non-predictive retained memory bounds dissipation (R3)
C4  4 <-> 5    H(X|Y): what recognition discards, generation must
               resupply
C5  4 -> 2,3,5 floor vs run cost (R4): a bit saving is not an energy
               saving
C6  2 -> 3     ADDED BY THE CALIBRATION (7.3, P4): low-variance units
               were recruited to carry the prediction, so a quiet unit
               at site 3 may be working, not idle
```

## 7. Calibration pass on site 2

### 7.1 Contamination ledger, declared before the fill

```
K-1  the work order's CONTEXT paragraph states the 2022 result. Every
     reader of the order holds the key.
K-2  the site-2 paragraph as delivered names it again ("Already has a
     published emergence case ..."); so do the SCORING paragraph, the
     CALIBRATION paragraph, and the parenthetical in field (e).
K-3  this filler is a language model with the paper in its training
     data, and ran web searches on it before filling. The facts that
     section 7.3 will list were in hand.
```

Consequence: the fill below is VOID as a test of predictive skill; the
runner holds the key (`frame-location-benchmark` FLB_010,
`revision-survival` VOID_KEY_HOLDER). What survives is STRUCTURAL: for
each published fact, does the rubric have a field it can land in. That
does not depend on the filler's foresight.

Bound on leakage, imposed: the fill may use only the text of a stripped
packet, namely the site preamble, site 2 without its anchor sentence,
the honest edge, and the rubric spec without the parenthetical in field
(e), all taken from Appendix A. Every line quotes the packet phrase it
derives from. The scorer, in the next revision, checks each quote
against the packet and checks the fill for key terms.

### 7.2 Blind fill (pre-registered)

```blind-fill
FILL   site 2, from the stripped packet only; each SRC quotes the packet
(a)    FOUND: on an input stream the top-down model predicts better than chance, the loop that sends only the residual upward spends fewer bits than a pass that sends the input, bits counted as the sum of -log2 p(arrived) over the stream; the saving grows as prediction improves.
SRC    "predict the input top-down, transmit only the mismatch (residual) upward" | "Bits spent = -log2(probability the model assigned to what actually arrived)" | "Better prediction -> fewer bits -> lower cost"
(b)    SCOPE: bits fall but total cost does not, because carrying the prediction top-down costs as much as the residual saves. Under the stated definition "better prediction -> fewer bits" holds by construction (a higher p is fewer bits), so only "fewer bits -> lower cost" can fail.
SRC    "Better prediction -> fewer bits -> lower cost" | "the savings are the point, not a side effect"
(b')   UNRESOLVED: a saving inside run-to-run spread, or a stream with no predictable structure, where the test did not test.
SRC    "predict the input top-down"
(c)    MDE: stdlib symbol stream with tunable predictability; ideal code length under a no-context model (the pass) and a context model (the loop); a shuffled copy of the stream as control; the top-down channel charged its own bits.
SRC    "predictive-coding/arithmetic-coding frontier" | "transmit only the mismatch (residual) upward" | "the cheapest test (stdlib-only Python where possible"
(d)    COST: compute low, data low, literature low, time low.
SRC    "rated roughly low/medium/high"
(e)    ANCHOR: no published instance is named in the packet. A known answer exists for the stdlib stream: the source-coding bound fixes the expected saving for a stream of known statistics.
SRC    "predictive-coding/arithmetic-coding frontier" | "is there already a published result to compare against"
(f)    RETENTION: passes only if the receiver rebuilds the input exactly from the residual plus its own copy of the prediction (lossless round trip). A smaller residual alone could come from throwing input away.
SRC    "if the loop actually RETAINS and CAN RECOVER state" | "A net can pass signals both ways and still erase information at every step"
SCORES d=2 u=1 k=2 x=1 r=2 compute=low data=low lit=low time=low
SHAPE  a loop built to predict, compared against a pass built not to; bits saved on predictable input; saving near zero on the shuffled control.
```

The sha256 of the block's content (the lines between the fences, each
ending in a newline) is recorded in the commit message of the revision
that introduced it (d5f5c2a), and is pinned in the scorer, which refuses
an edited fill.

### 7.3 The published instance [SEARCH-DEPTH]

Ali, Ahmad, de Groot, van Gerven, Kietzmann, "Predictive coding is a
consequence of energy efficiency in recurrent neural networks",
Patterns (2022), as named in the work order. Located by web search on
2026-10-13; abstract, summaries and snippets only, full text not
reached. The facts, as read:

```
P1  the objective is energy alone: an L1 penalty on unit preactivation;
    nothing predictive is wired
P2  input: sequences of ten MNIST digit images in ascending order,
    wrapping around; each pixel drives one recurrent unit; unit output
    is ReLU(preactivation)
P3  units self-organize into prediction units and error units; the
    network suppresses the predictable part of its input
P4  prediction units sit in the low-variance region of the input (the
    image edges); error units in the high-variance region (the centre)
P5  lesions show two timescales: fast lateral inhibition among error
    units, and a slower top-down flow through prediction units that
    integrates evidence over time
P6  lesioning the non-prediction units has little effect (roles
    identified by lesion)
P7  models penalizing preactivation outperform controls penalizing the
    output (L1 on output plus L2 on weights)
P8  a shuffled-order control and an input-reconstruction test: not
    located at search depth. Not located is not absent.
```

Follow-ups located (SEARCH-DEPTH, existence only): energy efficiency in
active vision producing predictive remapping (2025/26, PMC12827687);
multi-compartment spiking variants (PLOS Comput Biol 2025); lateral
predictive coding with phase transitions (Huang et al. 2024, site 1 (e)).

### 7.4 The comparison

Each published fact, the rubric field it lands in, and one of four
states: MATCH (a field holds it as the paper has it), PARTIAL (a field
holds part of it), NO_SLOT (no field could hold it), NOT_LOCATED (the
fill asked for it and the paper, at search depth, does not show it).

```calibration-match
# fact | state | rubric field | note
P1 | NO_SLOT | (a),(c) | emergence under an energy-only objective with nothing wired; the template asks what a built loop saves, so the fact has nowhere to land
P2 | MATCH | (c) | a predictable stream; the blind MDE names one (tunable predictability; here ascending order with wraparound)
P3 | PARTIAL | (a) | prediction and error roles, predictable input suppressed; wired in the blind (a), emergent in the paper
P4 | NO_SLOT | none | where the roles sit (low-variance edges, high-variance centre); no field asks which units take which role
P5 | PARTIAL | (b) | two timescales; the blind (b) names the hazard (the top-down channel's own cost) but no field asks for the time structure
P6 | NO_SLOT | none | roles identified by lesion; no field asks how a role is identified
P7 | PARTIAL | (f) | where the cost is measured decides the result; the blind (f) requires a lossless round trip but no field requires the pre- or post-nonlinearity placement to be declared
P8 | NOT_LOCATED | (c),(f) | the blind fill's two controls (shuffled stream, round trip) were not located in the paper at search depth
```

Counts: MATCH 1, PARTIAL 3, NO_SLOT 3, NOT_LOCATED 1 (8 facts).

Predicted fruitfulness against what the instance supports. The blind
fill scores site 2 at LOOP 2.000 and REV 2.000 (its SCORES line). The
informed entry's best site-2 variant is S2a, the blind fill's own design,
at the same 2.000 and 2.000: Q-LOOP moved by +0.000 and Q-REV moved by
+0.000. Site 2 ranks third on Q-LOOP (behind the S1 / S4 tie) and second
on Q-REV, blind and informed alike. The published instance changed the
rubric's CONTENT (a variant, a field, a coupling, a requirement in (f);
7.6) and moved no score.

The work order's SCORING paragraph says site 2 can be "partly checked by
replicating published numbers" and should rank ahead for that reason.
Scored, the replication (S2c) is site 2's most expensive variant (cost
18 against 4) and the best site-2 variant under no reader profile
(section 8). Site 2's cheap check gets its known answer from coding
theory, not from the publication. The ranking intuition survives (site 2
is cheap); the stated reason does not.

Predicted shape against reported shape.

```
blind SHAPE   a loop built to predict, compared against a pass built not
              to; bits saved on predictable input; near zero on a
              shuffled control
reported      a loop given only an energy cost turns itself into a
              predictor (P1, P3); the roles sit where input variance is
              low (P4); two timescales (P5)
match         direction of effect on predictable input (P2, P3)
mismatch      BUILT against EMERGED. The blind shape compares two
              designs; the published result is that the design falls
              out of the constraint, which is the general pattern the
              work order's own CONTEXT states
```

What the blind fill got right, and keeps: isolating the one falsifiable
step ("fewer bits -> lower cost"); charging the top-down channel; the
lossless round trip as the retention check; a known answer that costs
nothing (source coding).

### 7.5 Bin marker (tools/bin_self_test.md)

```
BIN:       site 2 is a design comparison: a loop built to predict
           against a pass built not to (the blind SHAPE line)
DROPPED:   P1 emergence with nothing wired; P4 where the roles sit;
           P5 the timescales; P6 how a role is identified (lesion)
DISPROOF:  in the packet itself, the preamble: "run the inverse move --
           ask what conditions make the loop do work, not what it
           computes". The packet asks for conditions; the fill answered
           with a design
FLIP:      read site 2 as "impose only the constraint and see whether
           the loop appears". Visible under the flip: the emergence
           variant (S2b), the low-variance ablation (does a role need a
           quiet region?), the placement of the cost measure (P7), and
           the coupling to site 3 (C6)
COST OF:   the rubric's frame. Fields (a)-(f), as specified, ask what a
           designed experiment returns; none asks what a constraint
           generates. The work order's CONTEXT states the pattern ("the
           constraint generates the form") and its rubric spec has no
           field for it
```

Trusted blindly, the rubric would have deleted the emergence result
entirely, ranked a coding exercise as site 2, and called site 2
calibrated. It would also have missed the placement finding (C6, the
site-3 note) and the cost-placement hazard in (f).

### 7.6 Revision record

```
R-1  field (g) EMERGENCE added to section 4 and to every site, marked
R-2  site 2 informed entry written (section 5); the blind fill kept as
     committed, hash pinned
R-3  S2b (the emergence variant, with the low-variance ablation) and
     S2c (the replication) added to the triage table
R-4  site 2 (f): the cost measure must be a lossless code length or a
     pre-nonlinearity activity, never a post-nonlinearity output alone
R-5  coupling C6 (2 -> 3) added to section 6; site 3 (e) note added
R-6  nothing removed
```

### 7.7 Clean-run protocol

The comparison above is structural (7.1). A predictive test needs a
reader without the key:

```
1. an operator runs
       python3 tools/experiment_fruitfulness_triage.py --blind-packet
   and hands the packet to a reader with no access to the paper, the
   web, or this repository
2. the reader fills (a)-(f) for site 2; every line quotes the packet
   phrase it rests on
3. the fill is hashed (sha256 of its lines, each ending in a newline)
   and the hash recorded before anyone reads section 7.3
4. the fill is compared with 7.3 using the four states of 7.4
```

Falsifier for the structural finding: a clean fill that places
emergence (a constraint generating the loop's role) in (a) or (c)
unprompted refutes "the six-field template has no slot for emergence"
for that reader. One clean fill is n = 1: it moves the finding, it does
not settle it.

## 8. Scoring

Per experiment VARIANT, five components on 0..2, each with a stated
reason in the basis block below.

```
d  DECISIVE   does the MDE separate (a) from (b)?
              0 no; 1 only with a further step; 2 directly
u  OPEN       how much of the question the anchors leave open
              0 answered; 1 partly answered; 2 open
k  KNOWN      can the pipeline be checked before it is trusted?
              0 no known answer; 1 qualitative; 2 exact
x  REACH      how many OTHER sites a result here changes the reading
              of, through section 6: 0 none; 1 one; 2 two or more
r  RETAIN     field (f), the Q-REV reach: 0 not reached; 1 partial;
              2 reached

fruit_LOOP = d * (wu*u + wk*k + wx*x)
fruit_REV  = fruit_LOOP * r / 2        NOT_REACHED when r = 0, never 0
cost       = SUM over compute, data, lit, time of the level's cost
ratio      = fruit / cost              the work order's
                                       fruitfulness-per-resource-spent
```

d multiplies: an experiment that cannot tell (a) from (b) returns no
information whatever else it has. u, k and x add.

Declared choices, each overridable in the scorer:

```
[CHOICE 1] reader profiles. Profiles GATE: a variant needing more than
           the reader has is BLOCKED and names the short resources; it
           is never down-weighted
             phone          low / low / low / low
             this-session   compute medium, data low, lit medium, time
                            low (measured 2026-10-13: stdlib and numpy
                            present; web search reachable; full-text
                            hosts refused at DNS; no download attempted)
             laptop-online  medium / medium / high / medium
             lab            high / high / high / high
[CHOICE 2] cost per level: low 1, medium 3, high 9
[CHOICE 3] weights wu = wk = wx = 1
[CHOICE 4] every first-place reading is also taken over 64 settings:
           medium in {2,3,4}, high in {4,9,16} with high > medium,
           weights in {1,2}^3
[CHOICE 5] reading over the sweep: FIRST_ROBUST (sole first in every
           setting), FIRST_SCOPED (sole first in a strict majority),
           FIRST_UNRESOLVED (the union of the first sets). A tie is
           held, not broken (tools/held_tie_precision.md)
```

The table (S2b and S2c added by the calibration, 7.6):

```triage-table
# id  site  d u k x r  compute data   lit    time   design
S1a   S1    2 1 2 2 1  low     low    low    low    16-unit loop: gain x delay x input sweep; hysteresis, MC, recovery horizon k*
S2a   S2    2 1 2 1 2  low     low    low    low    symbol stream: code length with and without context; top-down charged; shuffled control; round trip
S2b   S2    2 2 1 2 2  medium  low    medium medium small recurrent net, synthetic predictable sequence, L1 on pre-nonlinearity activity, nothing wired; roles by lesion and decoder; low-variance ablation
S2c   S2    2 1 2 2 1  medium  medium high   medium replication of the published setup (784 units, ascending digit sequences, L1 on preactivation)
S3a   S3    2 1 1 1 0  low     low    low    low    warm vs cold settling at four contraction rates; reset, adaptation and delta-coding controls; three cost models
S4a   S4    2 1 2 2 2  low     low    low    low    2x2 erasure ledger (pass/loop x irreversible/reversible) by exact enumeration
S4b   S4    1 2 1 2 2  medium  low    high   high   finite-speed dissipation of the four cells on an overdamped double-well model
S5a   S5    1 1 2 1 2  low     low    low    low    integer coupling bijection: H(Z|Y) = H(X|Y) by enumeration; exact round trip
S5b   S5    2 1 2 1 2  medium  low    medium medium small invertible net against classifier + generator at matched total parameters, 2-D toy
```

The basis, one reason per scored component:

```triage-basis
S1a.d a measured g_c(tau, input) that moves is (a) and a flat one is (b); the sweep reads it directly
S1a.u input statistics moving the chaos boundary is published for random networks (Rajan et al. 2010); the budget-matched class and the delay axis are open
S1a.k exact: one unit has its pitchfork at g = 1 and a large random net its chaos transition at g = 1
S1a.x rho sets site 3's warm-start saving (C1) and the merge rate and recovery horizon read at sites 4 and 5 (C2)
S1a.r MC and k* read recoverability, but the success criterion (a stable fixed point) merges its basin (R1): partial
S2a.d code length with and without context, top-down charged, against a shuffled control: the difference is (a) or (b)
S2a.u the saving is bounded by I(x_t; context), which is textbook; open is whether the top-down charge leaves a net saving
S2a.k exact: the source-coding bound fixes the expected code length of a stream of known statistics
S2a.x one other site: site 4, through C3 (predictive retention and dissipation)
S2a.r the lossless round trip is part of the design: rebuild x from residual and prediction, or count the bits lost
S2b.d roles present or absent, by lesion and by decoder, with and without the low-variance region
S2b.u the published instance shows the emergence once (7.3); whether a role needs a quiet region was not located
S2b.k qualitative: the published roles and lesion effects; no exact number at this depth
S2b.x site 4 through C3 and site 3 through C6 (quiet units recruited to carry the prediction)
S2b.r the decoder rebuilds the input from the state and counts the bits lost
S2c.d reproducing the reported quantities, or failing to, separates (a) from (b) for the published setup
S2c.u answered once, at search depth here; a replication bounds that one instance and does not ask the flipped question
S2c.k exact: the published numbers are the known answer
S2c.x reproduces P4, which carries C6 to site 3, and the activity cost, which carries C3 to site 4
S2c.r partial: the reported quantities include no input-reconstruction test (P8 not located)
S3a.d the warm-start law fits or fails, and the delta-coding control matches the saving profile or does not
S3a.u the warm-start law is fixed-point arithmetic; DEQ warm starts and sigma-delta nets are published qualitatively
S3a.k qualitative: the law is exact only for a linear contraction; tanh gives it approximately
S3a.x one coupling, C1 read backward: a measured saving at each rho tests the law that ties site 1's rho to site 3
S3a.r persistence only; re-settling overwrites the previous fixed point (R1)
S4a.d exact enumeration of all four cells decides "moved, not removed" at the floor
S4a.u the floor answer is predicted (R2); open is which currency each design pays in
S4a.k exact: H(X) = H(Y) + H(X|Y) and the telescoping sum, checked in R2
S4a.x the ledger decides how the savings claimed at sites 1, 2, 3 and 5 read (C2, C3, C4, C5)
S4a.r REVERSIBLE is the measurand: bijectivity by enumeration, and the uncompute is run
S4b.d needs a substrate model and a declared protocol duration before (a) and (b) separate
S4b.u no head-to-head erasure measurement of a retained-state loop against a pass was located
S4b.k qualitative: the quasi-static limit returns the floor; finite-speed costs depend on the model
S4b.x the substrate model decides whether a bit saving at sites 2, 3 and 5 reaches energy (C5)
S4b.r compares the reversible and irreversible cells directly: the Q-REV question in energy currency
S5a.d checks the information accounting, not learning; separating (a) from (b) needs S5b
S5a.u invertible networks already show one parameter set serving both directions (flows; Ardizzone et al. 2019)
S5a.k exact: H(Z|Y) = H(X|Y) for a bijection, by enumeration
S5a.x one other site: site 4, through C4 (what recognition discards, generation resupplies)
S5a.r the round trip is exact by construction and checked by enumeration
S5b.d per-direction margins and the round trip at matched total parameters decide (a) against (b)
S5b.u the per-direction cost of sharing at matched total parameters was not located; one-network reuse is published
S5b.k exact: a 2-D toy distribution has a known density, so every likelihood has a reference
S5b.x one other site: site 4, through C4
S5b.r the round trip x -> forward -> backward -> x is required, with bits lost counted
```

Result under the phone profile and the declared choices, held by the
selftest to what the scorer recomputes:

```triage-result
Q-LOOP  S1 2.500 S1a | S4 2.500 S4a | S2 2.000 S2a | S3 1.500 S3a | S5 1.000 S5a
        FIRST_UNRESOLVED:S1,S4   first across 64 settings: {S1,S4} x64
Q-REV   S4 2.500 S4a | S2 2.000 S2a | S1 1.250 S1a | S5 1.000 S5a
        FIRST_ROBUST:S4   first across 64 settings: {S4} x64
not reached on Q-REV: S3a
profiles with these first sets: lab, laptop-online, phone, this-session
best site-2 variant, Q-LOOP: lab S2a, laptop-online S2a, phone S2a, this-session S2a
best site-2 variant, Q-REV: lab S2a, laptop-online S2a, phone S2a, this-session S2a
```

Run it:

```
python3 tools/experiment_fruitfulness_triage.py                  # phone
python3 tools/experiment_fruitfulness_triage.py --profile lab
python3 tools/experiment_fruitfulness_triage.py --have compute=medium,lit=high
python3 tools/experiment_fruitfulness_triage.py --blind-packet   # 7.7
python3 tools/experiment_fruitfulness_triage.py --selftest       # prints its count
```

A sample report is `tools/samples/experiment_fruitfulness_triage.sample.txt`.

What the result says, read as triage:

```
Q-LOOP   sites 1 and 4 tie at the top and stay tied in all 64 settings:
         same components, same cost. The rubric cannot separate them at
         its resolution, so it says so (FIRST_UNRESOLVED) instead of
         breaking the tie. Either is a defensible first run.
Q-REV    site 4 is first in all 64 settings (FIRST_ROBUST). The payoff
         the work order hopes for at sites 2-5 belongs to REVERSIBLE,
         and site 4's ledger is the cheapest experiment that measures it
         directly, with loop and reversibility in separate cells.
site 3   NOT_REACHED on Q-REV: its experiment tests persistence only. Its
         Q-LOOP score stands.
profiles gate; they do not reorder. The first sets are the same under all
         four profiles, because the top variants all cost "low".
replication
         S2c is the best site-2 variant under no profile.
discovery
         the two variants with the most open question (u = 2), S2b and
         S4b, both need more than a phone. They are printed apart and
         never merged into the ratio: a reader with a lab and an
         appetite for the open question should read that line, not the
         ranking.
```

## 9. Open / owed

- Full text of every SEARCH-DEPTH anchor. Full-text hosts refused at DNS
  from this environment on 2026-10-13 (pmc, biorxiv); web search
  snippets were reachable.
- The occasion's venue listing: two searches disagreed. Nothing rests
  on it.
- A mirror in the `method-layer` repository, where earlier `tools/`
  reasoning notes were mirrored: not done; that repository is outside
  this session's scope.
- No experiment in the table has been run. The scorer orders them; it
  measures nothing about loops.
- The clean calibration run (7.7) has not been done. The only fill on
  record is contaminated (7.1) and is used structurally.
- The (g) variants at sites 1, 3, 4 and 5 are unscored. A scored (g)
  variant moves the first set only by beating the tied 2.500, which
  takes all-low cost, d = 2 and u + k + x = 6 (ratio 3.000). Whether any
  does is unchecked, not ruled out.
- Profiles other than this-session are declared, not measured.
- The components are ordinal judgments on 0..2 by the author of the
  rubric, each with a stated reason. The sweep (CHOICE 4) bounds how far
  the cost map and weights can move the ranking; nothing bounds a
  different reader scoring the components differently. A second scorer
  is the check.

## Appendix A - the work order, as delivered

Verbatim. The scorer reads its blind packet from here.

<!-- ORDER-BEGIN -->
```text
WORK ORDER: fruitfulness-triage rubric for the five reversible-loop experiment sites
Repo: JinnZ2 (CC0, stdlib-only, phone-buildable). Target: new file, e.g. tools/experiment_fruitfulness_triage.md (+ optional score.py, stdlib only).

CONTEXT (verdict-free; report, don't argue a position)
A PNAS/UIUC study (July 2026) found decision-related signals as early as primary somatosensory
cortex (S1), driven by top-down feedback loops rather than clean bottom-up feedforward processing.
Most trained AI architectures (feedforward stacks, stage separation, early layers as pure feature
passers) were built on the bottom-up presumption. That presumption now has a documented crack:
a real biological system runs a two-way, loop-based architecture instead. Separately, a 2022 paper
(Ali, Ahmad, de Groot, van Gerven, Kietzmann, "Predictive coding is a consequence of energy
efficiency in recurrent neural networks," Patterns) showed that training a plain RNN to minimize
energy consumption in a predictable environment causes predictive coding to emerge on its own —
no hand-wiring. The loop was the cheapest solution to an energy constraint, not a designed feature.
This is one instance of a general pattern: a structure (shape, loop, code) is what falls out when a
constraint set is minimized — the constraint generates the form rather than obstructing it.

TASK
Five experiment sites were identified as places to "run the math / run the simulations / find
where things lie" on reversible, loop-based (rather than strictly feedforward) architectures.
Build a RUBRIC — not a full experiment — that lets any AI picking up this repo triage which site
is most fruitful to pursue FIRST, given its own available resources (compute, literature access,
time). Deliverable is the rubric + a worked calibration pass, not a trained model.

THE FIVE SITES (unfreeze the zero top-down term in the standard feedforward update; treat the
feedforward equation as a snapshot taken at one setting of the environment, not a fixed fact;
run the inverse move — ask what conditions make the loop do work, not what it computes):

1. STABILITY CONDITIONS — which gain / timing / input-statistics settings hold a feedback loop at
   a fixed point vs. push it into a regime pure feedforward cannot reach. Gradient as a design
   variable, not a given.

2. COMPRESSION PAYOFF — predict the input top-down, transmit only the mismatch (residual) upward.
   Bits spent = -log2(probability the model assigned to what actually arrived). Better prediction
   -> fewer bits -> lower cost. This is the predictive-coding/arithmetic-coding frontier; the
   savings are the point, not a side effect. Already has a published emergence case (the 2022
   paper above) — this is the one site with a real worked instance to calibrate against.

3. DORMANT-FACE COST — a loop that has settled near a fixed point can leave most of its structure
   quiet and only activate the parts the current input actually couples to. Repeated exposure to
   the same input class should get cheaper over time as the loop re-settles faster.

4. LANDAUER / ERASURE JOIN — standard feedforward nets discard (erase) intermediate activations
   at every stage; that erasure is where the Landauer bound bites. A loop that retains its state
   and can recover earlier values is not standing on that erasure floor. Site: does a retained-
   state loop actually show measurably lower erasure cost than an equivalent feedforward pass,
   or does it just move the erasure elsewhere?

5. INVERSE-DIRECTION REUSE — a relation has no privileged direction. Can one trained loop run
   forward as recognition and backward as generation, instead of requiring two separately trained
   networks? What is lost/gained running the same weights both ways?

HONEST EDGE TO CARRY INTO THE RUBRIC, NOT AROUND IT
"Reversible" in the physics sense (Bennett 1982: measurement can run without erasure cost; the
unavoidable cost is paying to erase the record) is NOT automatically the same as "bidirectional"
in the network sense (a net that merely has connections running both directions). A net can pass
signals both ways and still erase information at every step. The payoff on sites 2-5 only lands
if the loop actually RETAINS and CAN RECOVER state, not merely if it has feedback connections.
Any fruitfulness score must check for this distinction explicitly, not assume it.

RUBRIC SPEC (what to build)
For EACH of the five sites, produce:
  a) POSITIVE RESULT — what a confirming finding would concretely look like (a measurable
     quantity, a comparison, a direction of effect).
  b) NEGATIVE RESULT — what a disconfirming finding would look like. Keep this DISTINCT from
     "inconclusive" — a clean negative is itself information (per the no-verdict-language
     convention: found / scope / unresolved are different outcomes, don't blur them).
  c) MINIMUM DISTINGUISHING EXPERIMENT — the cheapest test (stdlib-only Python where possible;
     otherwise name the literature check or replication needed) that could tell (a) from (b) apart.
  d) RESOURCE COST — compute, data, literature access, time — rated roughly low/medium/high.
  e) EXISTING ANCHOR — is there already a published result to compare against (site 2 has one;
     check whether 1, 3, 4, 5 do too before assuming they don't).
  f) RETENTION CHECK — does this site's experiment, as designed, actually test retain+recover,
     or could it pass while only testing bidirectional-pass-through? State explicitly.

SCORING: fruitfulness-per-resource-spent, not fruitfulness alone — a high-value result that costs
nothing to approximate (e.g., site 2, which can be partly checked by replicating published
numbers) should rank ahead of an equally interesting but expensive one, for an AI with limited
resources picking this up cold.

CALIBRATION PASS (the self-test)
Before trusting the rubric, run it on site 2 BLIND to the answer the 2022 paper already found —
i.e., fill out (a)-(f) for site 2 as if the energy-efficiency result were not yet known, then
compare the rubric's predicted fruitfulness and predicted positive-result shape against what the
paper actually reported. Record the match or mismatch. This is the same move as bin_self_test.md:
name the bin (the rubric's prediction), check it against what's actually there (the published
result), state what it would have deleted or missed if trusted blindly.

OUTPUT
- tools/experiment_fruitfulness_triage.md: the rubric, filled out for all five sites, plus the
  calibration-pass writeup.
- Optional: score.py (stdlib only) if the resource/fruitfulness scoring can be made a simple
  weighted formula worth automating — not required if the rubric is clearer as prose + table.
- README note: state plainly this is a TRIAGE tool for choosing where to look next, not a claim
  that any of the five sites has been validated. Carry the retention-check distinction into the
  README so a future reader does not quietly drop it.
```
<!-- ORDER-END -->

## Provenance

Built from a work order delivered in session, carried verbatim in
Appendix A. Anchors located by web search on 2026-10-13 at snippet
depth. The R1 and R2 arithmetic is recomputed by the scorer's selftest,
which also holds the triage-result block, the calibration counts and the
blind fill's hash to what it computes. Commits: d5f5c2a (pre-calibration,
blind fill pinned), then the calibration and the scorer.
