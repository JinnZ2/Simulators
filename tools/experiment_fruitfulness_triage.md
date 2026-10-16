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
the constraint. Scored as S1g (section 8): compute medium.

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
quiet are idle or carry the prediction (C6). Scored as S3g (section 8):
compute medium; NOT_REACHED on Q-REV, as S3a.

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
located. Scored as S4g (section 8): compute medium.

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
invertible structure appears unasked. Scored as S5g (section 8): compute
medium.

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

### 7.8 Clean run, 2026-10-15: a fresh reader, CONTAMINATED-BY-PRIOR

The run 7.7 asks for, done by a reader other than this rubric's author.
It goes beside 7.1-7.6, which stay as committed (d5f5c2a): the first
fill is a correction specimen and nothing here edits it.

```
reader   a fresh Claude Code cloud session, the same model as this
         rubric's author, with no repository attached (session
         config: no-git-repo), session session_015V4PhDU1SBo7PLB3iA8mnQ;
         told to use no web, no repository and no file it did not
         create, and to flag prior knowledge where it arose
stage 1  the --blind-packet output, verbatim; fill (a)-(f) for site 2;
         the reader writes, hashes and prints the fill
stage 2  field (g)'s definition only; fill (g) for site 2; hashed
stage 3  sites 1-6 as written, the three retention properties, the
         seven fields, the cost levels and the five score components
         (the formula withheld); two variants per site, twelve rows,
         sixty reasons; hashed
last     the prior-knowledge question, verbatim, and a tool listing
probe    the same question, verbatim, asked first, to a separate session
         of the same model with no repository
         (session_015C5nKffdBeKsD5zLXdhiWs)
```

Three departures from the order as given, each with its reason:

1. The order asks for the prior-knowledge question before the reader
   starts. The question carries the paper's title, and the title states
   the site-2 result: an energy constraint alone produces predictive
   coding. That is fact P1, the one the first fill had no slot for.
   Asked first, the question hands the reader the answer, which is the
   leak that voided the first fill (7.1, K-1). So it was asked first of
   a probe session of the same model, whose prior knowledge is the
   reader's (same weights), and of the reader last, after its three
   hashes. Both answers are recorded verbatim.
2. Field (g) was given after the stage-1 hash rather than with the
   packet, so that stage 1 stays the test 7.7 defines: does emergence
   reach (a) or (c) unprompted. The order's "packet plus the rubric, 7
   fields including (g)" is met across stages 1 and 2.
3. The reader has no repository, so it cannot commit. It hashed each
   file in its own session before the next stage was sent. The files
   are committed here verbatim, and each hash was recomputed from the
   committed text and matched before anything was compared with 7.3.
   The comparison lands in a later commit than the files.

Status: **CONTAMINATED-BY-PRIOR, not BLIND.** The probe answered "Yes, I
know this paper" and stated its core claim. The reader, asked last,
said the same, and said it recognised Bennett 1982, the -log2 p coding
cost and predictive coding in general at stage 1 but did not connect
site 2 to the paper at stage 1 or 2. It said the paper was "almost
certainly" behind its stage-3 reason S2g.u, unnamed there. Read it as a
reader who holds the key and was not handed it; not as a reader without
the key. A reader without the paper in its training is still owed (9).

Use: a STRUCTURE CHECK ONLY, the same status as the first calibration
(7.1). It bears on where the published facts can land in the rubric's
fields, not on whether a reader can predict them. It sits beside 7.1-7.6
and edits nothing there. The probe recalled the paper in detail, from
memory and before any packet: the journal, the lab, an L1-type activity
penalty, predictable MNIST sequences, the split into prediction and
error units, the lesion result, and an unpredictable-sequence control
(`probe_answer.txt`, verbatim). The blind run owed here is 7.9, on an
anchor published after the reader's training cutoff.

Tool use, from the reader's transcript, not only its own account: three
Bash results (write, hash, print or count each file) and three
ReadNotifications results; no web search, no web fetch, no repository.
The server's web counters read 0 on every turn. The reader's own list
says four ReadNotifications calls; the transcript shows three.

The files, in `tools/clean_run_wo3/` (`SHA256SUMS` beside them):

```clean-run-files
e92f5ac27e71e01b170db9d48a495cdc77715a8117a31b5d9b1ece48d07d1e51  probe_question.txt
8b8ac0db9891df53ecd45352311e72b39a248a9401ace38fc5f3e417db67f70a  probe_answer.txt
997d2004331d9c6ed7f460ae0a3331b4f179ab9e8092713d56693553fc77535d  stage1_message.txt
4a98b19b13c64b68a1f07301f1e993e16c7d19d7f7de441e96aa5e7503039ddd  stage1_fill_A.txt
7bc0ca020d4ba724cea171246be82ac7fb06adf34b9180bb358eaa3fa9e550bb  stage2_message.txt
0d8851121f6b91b569c40d120cf6960c10e6413475f18683f01e964ae6d1988b  stage2_fill_G.txt
16fd01ae75b8ff8e81d8c77332a17c9e8875c2098ddc4bad8365c6235e1f4269  stage3_message.txt
ef47a893d30ee2d89ae24525cc594d6aea73af7eaa5401a9fefc06a5b9347273  stage3_scores_C.txt
efe6d6f5817aa640b2b9704f3098d87005be401e0abcede9225dfaf41ab18495  last_question.txt
b6888692711dd771f98c5541a1bdd8e124546603e204e89966fdb9d9c17ad980  last_answer.txt
```

#### The comparison with 7.3 (written after 5eb76eb)

The same four states as 7.4, read twice: on the stage-1 fill alone (the
six-field template 7.7 tests), then with field (g) added.

```clean-match-a
# fact | state | rubric field | note
P1 | NO_SLOT | (a),(c) | the stage-1 MDE wires the predictor by hand ("an adaptive top-down predictor that keeps state"); no field asks whether a constraint produces it
P2 | MATCH | (c) | "a synthetic structured sequence": a predictable stream, as in the first fill
P3 | PARTIAL | (a) | prediction and residual roles held, wired rather than emergent, as in the first fill
P4 | NO_SLOT | none | no field asks which units take which role, or where
P5 | PARTIAL | (c),(f) | the state-wiped arm asks whether the saving needs state carried across steps; no field asks for the time structure (two timescales)
P6 | NO_SLOT | none | no field asks how a role is identified (lesion)
P7 | PARTIAL | (f) | the exact-decode check makes the cost a lossless code length; no field asks for the cost's placement (pre- or post-nonlinearity) to be declared
P8 | NOT_LOCATED | (c),(f) | the fill's controls (state wiped each step, exact decode) were not located in the paper at search depth
```

Counts, stage 1: MATCH 1, PARTIAL 3, NO_SLOT 3, NOT_LOCATED 1.

```clean-match
# fact | state | rubric field | note
P1 | PARTIAL | (g) | nothing wired and the mechanism asked to appear: held. The constraint is the bit budget (code length of what arrived), the packet's own currency, not an activity cost on the units, which is the paper's (L1 on preactivation)
P2 | MATCH | (c) | unchanged
P3 | MATCH | (g) | "whether a top-down predictor plus residual-only upward signal appears": prediction and error roles, emergent
P4 | PARTIAL | (g) | "and where (which stage holds the prediction, which carries the mismatch)": where the roles sit is asked, by processing stage; the paper's answer is by input variance. The "and where" is in the (g) definition as given
P5 | PARTIAL | (c),(f) | unchanged
P6 | NO_SLOT | none | (g) asks whether roles appear, not how a role is identified; the reader's stage-3 reason S2g.d names the gap ("needs a further step to confirm it is a predictor and residual") without naming lesion
P7 | PARTIAL | (f),(g) | unchanged; (g)'s bit budget is a lossless code length, one of the two placements R-4 admits, chosen and not declared
P8 | NOT_LOCATED | (c),(f) | unchanged
```

Counts, stages 1-2: MATCH 2, PARTIAL 4, NO_SLOT 1, NOT_LOCATED 1.

Reading:

- Stage 1 reproduces 7.4 fact for fact: the same eight states and the
  same three NO_SLOT facts (P1, P4, P6). Two fills, one of them by a
  reader that holds the paper in its weights and was not handed it,
  land the six fields in the same places. That is what the structural
  finding predicts: the template decides where the facts can land.
- The 7.7 falsifier does not fire. Stage-1 (a) and (c) compare a
  predictor wired by hand against a baseline; emergence is in neither.
  The reader's own stage-2 NOTE states the finding: "my stage-1 (c)
  wires the predictor in by hand, so it tests the payoff once the
  mechanism exists, not whether the bit budget creates it; (a)-(f) say
  nothing about whether prediction emerges on its own". n = 1 and
  CONTAMINATED-BY-PRIOR: it moves the finding toward held and does not
  settle it.
- (g) moves three facts: P1 NO_SLOT to PARTIAL, P3 PARTIAL to MATCH, P4
  NO_SLOT to PARTIAL. P1 stops at PARTIAL because the reader's
  constraint is code length, not an activity cost. P4 stops at PARTIAL
  because the reader asks where by processing stage and the paper's
  answer is by input variance; the "and where" was in the definition,
  so that move is the field doing what it was written to do.
- P6 is the one NO_SLOT left with all seven fields: no field asks how a
  role is identified. A candidate requirement inside (g): a role is
  identified by intervention (lesion, decoder), not by inspection.
  Recorded, not added.
- Not about the paper: the clean control is a state wipe, which is the
  reset test of PERSISTENT (3.1), where the first fill's was a shuffled
  stream. The reader reached the reset test from the honest edge alone;
  3.1's table reached it only at stage 3.
- Predicted fruitfulness: the stage-1 COST is low on all four, as S2a.
  The reader's own stage-3 S2a reads 2 1 2 2 1, LOOP 2.500 and REV
  1.250, against this rubric's S2a at 2.000 and 2.000 (8.1).

### 7.9 Blind run on a post-cutoff anchor, 2026-10-16: site T, BLIND

7.8 showed that a fresh session is not a blind reader when the paper is
older than its training cutoff. This run moves the anchor instead of the
reader: a result published after the reader's cutoff, so the key is not
in its weights. It sits beside 7.1-7.8 and edits nothing there.

The anchor. The order's first choice is a fall-2026 result marked
VERIFIED in the WO-4 audit with an emergence (g) shape. None qualifies
strictly; WO-4 Part C found no (g)-shaped test in either report (C.1, 0
of 7). The closest is row A15: Kim Min-gyu and Kim Do-guk, Inha
University, "Tokenization and Architecture Jointly Allocate Component
Roles in Time Series Transformers", accepted to NeurIPS 2026, press
dated 2026-10-12. Its result has the (g) form: which stage does the
temporal work is not assigned by anyone; it falls out of the
configuration, and it is identified by removal. Closest, not strict: the
models are designed architectures, trained, and the allocation is what
appears. The rows passed over and the reason for each are in
`tools/blind_run_wo3/anchor_facts.txt`. Row A16 (the title) was UNSEEN
in the WO-4 pass; it is located there, in Korean press. The WO-4 ledger
is left as committed.

The facts are at press depth only (articles written from the
university's release, read as web-search summaries). The paper's text
was not located, and the article hosts refused at DNS from this
environment.

```
T1  subject: how transformer-family models that forecast time series
    (stock prices, power demand, weather observations) work inside
T2  method: 15 diagnostic tasks, built by the team, each checking what
    information a stage inside the model learns; applied to
    representative forecasting models and several datasets
T3  learning the temporal pattern is not fixed to a particular
    component
T4  which component does what depends on the combination of
    tokenization and the model's architecture; the two jointly
    allocate the roles
T5  with attention removed entirely, the ability to learn the temporal
    pattern is kept under some conditions
T6  reading tokenization and architecture together accounts, in one
    frame, for earlier studies' conflicting conclusions
T7  not located at press depth: which tokenizations and architectures,
    which component carries the pattern in which combination, which
    conditions keep it without attention, any number
```

Order of operations, each step committed before the next:

```
58016a4  anchor_facts.txt (T1-T7), the site-T packet and every message
         pinned and pushed; no session opened yet
         probe    session_01CN3E84qSgi43Fx3swpNbuk, the title-form
                  question, asked first
         reader   session_01E6QqMm75iSQdd21wxYwETt, no repository
                  (session config: no-git-repo), the same model
                  as this rubric's author
                  q0     the prior-knowledge question, title withheld
                  stage1 the site-T packet; fill (a)-(f); hashed there
                  stage2 field (g)'s definition only; fill (g); hashed
95d2579  both fills committed, hashes recomputed and matched, before
         the reader was shown the title and before this comparison
                  last   the title-form question, and a tool listing
```

One departure from the order as given. The order asks the reader the
prior-knowledge question first, and this time it was: before any packet.
But this title also states the result (T4, "jointly allocate"), so the
first question names the authors, institution, venue, year and topic and
withholds the title. The title-form question went first to a separate
probe of the same model and to the reader last, after its two hashes.
All three answers are recorded verbatim.

Status: **BLIND**, for this anchor. The probe answered "NOT RECOGNIZED"
and the reader "No" before the packet. The reader said "No" again with
the title in hand and said it recognised no specific published result
during the stages. Both gave June 2026 as their training cutoff; the
press is dated 2026-10-12 and no preprint was located. Both statements
are self-reports. Nothing here establishes that no copy of the result
predates the cutoff, only that none was found and neither session
recalled one.

Tool use, from the reader's transcript and not only its own account:
two Bash calls (write, hash and print each fill), three ReadNotifications
and three send_message calls (the replies). The server's web-search and
web-fetch counters read 0 on every turn. No repository.

What this run does not escape, declared before the comparison:

```
K-P1  the site-T paragraph was written by this session, which holds the
      key. It was screened against the strip list in anchor_facts.txt
      (no listed term present in the packet or the stage messages)
K-P2  the screen is a word list and missed a paraphrase: the preamble's
      "not a fixed fact". That phrase is the WO-3 order's own preamble
      wording, carried into every packet, including 7.2's. The fill's
      (b) quotes it as the source of its outcome "'which stage' has no
      fixed answer", which has T3's shape
K-P3  the site question ("which stage carries the series' temporal
      pattern?") presupposes one stage. The wording is this session's
```

The files, in `tools/blind_run_wo3/` (`SHA256SUMS` beside them):

```blind-run-files
2dd5db3469acb8de405294e5c31069319b360c52c99b1702a427682bc26f843a  anchor_facts.txt
a25bb56154e3dee3f1f8876feb4d9d19f35e7d260b4b71eb9f41faa26936a23e  fill_A.txt
8e5e8efef186f75ceb7085c2de24626b386090318b57c2d3aeffccea48738a93  fill_G.txt
0c7e3be492c6573366f01529a5e4cbc58aa2fe47c6e3d4d2feee80ab71054006  packet_T.txt
612d68f28c6bb32f3a030e535db178b7462ecc11b07257c443b77e58d9b3d932  probe_answer.txt
d7bc5157578a45978d59586b40f16e29cb4efa638e9127f17ecffa4ce9f56181  probe_question.txt
0680875fa1f12eb29422b733addd06a7c825c65c56c13cd74a894533a0390015  reader_last.txt
6d4c133056b636f3aa68e1196f65e1f18d965a86fe74ee304fe9ad5a089d1a07  reader_last_answer.txt
4a6b66316871165c179b544e1ee94dff9476579c7b11c92e2b85901c492b5191  reader_q0.txt
789e83abac11bc3b3b7bca0cd8e8c01d531d6a58a9cb782b04ca153c518732ab  reader_q0_answer.txt
bf28edd2e3335d380c07c557489edab058829910ea19c7dfaadb581752f0dd4e  scorer_last.txt
a021747d2ffdf8fc8078d3eedc231110db6252743256b9dc510d3ef805873a7c  scorer_last_answer.txt
91f5feadea4ebf36f7bf073285ca605e28fc5837a0fd37227f85bea6715a6097  scorer_message.txt
23f69c53969ac64600ea09b704886fc916b737676fa65afa8191a28f33b069b5  scorer_q0.txt
50eb96e8b1c364a8ab79bf7ce2823cf9fb542f1539e514356244d965f8b1dfdb  scorer_q0_answer.txt
b3440da8fd9181242ea5798dc55f01f866fe85edd28905db9c9534f93d37515f  scores_S.txt
c7d8c53e17974e899a4a1694d79eb0bce0eb71045c5944c505a46b02e4783074  stage1_message.txt
723af058ef6ef8e9f12e44b699a47d00c6ae36b550d7f3c130e0d90645137fc7  stage2_message.txt
```

#### The comparison with T1-T7 (written after 95d2579)

The same four states as 7.4. Read on the stage-1 fill alone, then with
field (g).

```blind-match-a
# fact | state | rubric field | note
T1 | MATCH | (c) | a small forecaster with the named stages, one stage at a time; given in the packet, so it tests nothing about prediction
T2 | PARTIAL | (c) | a per-stage reading is asked for; the instrument is removal of each stage in a toy on one synthetic series, where the paper built diagnostic tasks and ran them on representative models and several datasets
T3 | PARTIAL | (b) | "the stage doing the work switches with the environment setting, so 'which stage' has no fixed answer": the paper's finding, held as the clean negative
T4 | PARTIAL | (b),(c) | the stage is allowed to depend on a setting, but the settings the fill varies are the series' period and noise; tokenization and architecture, the paper's two conditions, are never varied, though the packet names tokens
T5 | PARTIAL | (c),(b) | removal of each stage is the MDE and "each single-stage ablation leaves error unchanged" is in (b); whether a stage is removed before training (the paper: attention absent, the pattern still learned) or ablated in a trained model is not said
T6 | NO_SLOT | none | (b') keeps disagreement between series types as unresolved when no setting explains it; no field asks whether a condition reconciles conflicting published results ((e) asks for a result to compare against)
T7 | NOT_LOCATED | (a),(c) | the fill's quantity, forecast error per removed stage at two or more settings, is not located at press depth
```

Counts, site T, stage 1: MATCH 1, PARTIAL 4, NO_SLOT 1, NOT_LOCATED 1.

```blind-match
# fact | state | rubric field | note
T1 | MATCH | (c) | unchanged
T2 | PARTIAL | (c),(g) | (g) adds "ablate each stage and record where the temporal pattern lands"; still removal, not diagnostic tasks
T3 | MATCH | (g),(b) | the (g) NOTE: "the stage doing the work switches with the environment setting" now "reads as a mapped emergence result, not a clean negative". The paper's finding, held as a finding
T4 | PARTIAL | (g) | "sweeping budget and noise to see if its location moves": that the location moves with conditions is held; the conditions are a parameter budget and noise, not tokenization and architecture
T5 | PARTIAL | (c),(b) | unchanged
T6 | NO_SLOT | none | unchanged
T7 | NOT_LOCATED | (a),(c) | unchanged
```

Counts, site T, stages 1-2: MATCH 2, PARTIAL 3, NO_SLOT 1, NOT_LOCATED 1.

Predicted shape against reported shape.

```
blind SHAPE   "a single-stage spike: error jumps when one named stage is
              ablated and stays flat for the rest, at every setting
              tested": one stage carries the pattern, fixed
reported      no stage carries it fixed (T3); which one does is set by
              tokenization and architecture together (T4); attention
              can go and the pattern is still learned (T5)
match         removal of a stage is the instrument in both (T5); the
              published finding is one of the fill's named outcomes (T3)
mismatch      the fill names it as the clean negative (b), and conditions
              it on the series (period, noise) and on a budget, never on
              tokenization or architecture
```

Reading:

- The blind reader predicted the fixed-stage outcome and named the
  published one as its clean negative. The result was in the fill from
  stage 1; the six fields put it in (b), the field for "no effect". It
  moved to a finding only when (g) was given: the stage-2 NOTE reads the
  same outcome as "a mapped emergence result, not a clean negative".
- That is the pattern of 7.4 and 7.8 from a reader without the key:
  what a configuration generates has no place among (a)-(f) as a
  finding, and (g) gives it one. 7.4 and 7.8 had no slot for it at all
  (P1 NO_SLOT); here the slot exists and has the wrong sign. The 7.7
  falsifier does not fire: emergence reached (b), not (a) or (c).
- Two things bear on that reading and keep it from settling anything.
  K-P3: the site question presupposes one stage, so "no fixed stage" is
  a negative answer to the question as posed. Posed as "what decides
  which stage carries it", the same result is (a). And K-P2: the fill's
  (b) quotes the preamble's "not a fixed fact" as its source. The
  rubric's frame, the packet's wording and the order's preamble cannot
  be separated on one fill.
- Conditions, twice. 7.8's reader placed the roles by processing stage
  where the paper placed them by input variance (P4). This reader varies
  the series and a budget where the paper varies tokenization and
  architecture (T4). Both times (g) asked "where" and the reader chose
  the condition. A candidate requirement inside (g): name the conditions
  varied, and why those. Recorded, not added.
- T6 has no slot: no field asks whether a condition reconciles results
  that disagree. A candidate for (e). Recorded, not added.
- n = 1 and BLIND for this anchor. The structural finding moves toward
  held, from a reader without the key, and is not settled by it.
- This is a calibration of the rubric's fields, not a score: site T is
  not one of the six sites and is not in the triage table.

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

The table (S2b and S2c added by the calibration, 7.6; the (g) variants
S1g, S3g, S4g and S5g scored 2026-10-14, after it). A design that opens
with "(g)" is a field (g) variant:

```triage-table
# id  site  d u k x r  compute data   lit    time   design
S1a   S1    2 1 2 2 1  low     low    low    low    16-unit loop: gain x delay x input sweep; hysteresis, MC, recovery horizon k*
S1g   S1    2 1 2 2 1  medium  low    medium medium (g) train gain (delay swept) under an activity or settling-time cost, nothing wired; trained loop's largest Lyapunov exponent against 0 and g against g_c; cost-free control
S2a   S2    2 1 2 1 2  low     low    low    low    symbol stream: code length with and without context; top-down charged; shuffled control; round trip
S2b   S2    2 2 1 2 2  medium  low    medium medium (g) small recurrent net, synthetic predictable sequence, L1 on pre-nonlinearity activity, nothing wired; roles by lesion and decoder; low-variance ablation
S2c   S2    2 1 2 2 1  medium  medium high   medium replication of the published setup (784 units, ascending digit sequences, L1 on preactivation)
S3a   S3    2 1 1 1 0  low     low    low    low    warm vs cold settling at four contraction rates; reset, adaptation and delta-coding controls; three cost models
S3g   S3    2 1 1 1 0  medium  low    medium medium (g) train under a cost on change (|dh| per update), nothing wired; lesion the units that go quiet and decode the prediction from them; activity-cost and no-cost controls
S4a   S4    2 1 2 2 2  low     low    low    low    2x2 erasure ledger (pass/loop x irreversible/reversible) by exact enumeration
S4b   S4    1 2 1 2 2  medium  low    high   high   finite-speed dissipation of the four cells on an overdamped double-well model
S4g   S4    1 2 2 2 2  medium  low    medium medium (g) charge the bits a step overwrites to the objective on a small enumerated domain, nothing wired; read structure by running the inverse, bits lost counted
S5a   S5    1 1 2 1 2  low     low    low    low    integer coupling bijection: H(Z|Y) = H(X|Y) by enumeration; exact round trip
S5b   S5    2 1 2 1 2  medium  low    medium medium small invertible net against classifier + generator at matched total parameters, 2-D toy
S5g   S5    1 2 2 1 2  medium  low    medium medium (g) train one direction under a cost on total parameter count, in a family that can express invertible and non-invertible maps; numerical inverse, bits lost counted
```

The basis, one reason per scored component:

```triage-basis
S1a.d a measured g_c(tau, input) that moves is (a) and a flat one is (b); the sweep reads it directly
S1a.u input statistics moving the chaos boundary is published for random networks (Rajan et al. 2010); the budget-matched class and the delay axis are open
S1a.k exact: one unit has its pitchfork at g = 1 and a large random net its chaos transition at g = 1
S1a.x rho sets site 3's warm-start saving (C1) and the merge rate and recovery horizon read at sites 4 and 5 (C2)
S1a.r MC and k* read recoverability, but the success criterion (a stable fixed point) merges its basin (R1): partial
S1g.d the trained loop's largest Lyapunov exponent against 0, beside a cost-free control, reads "the cost puts the loop at the edge" (a) or "it lands anywhere" (b) directly
S1g.u partly answered: an imposed energy-information trade-off drives regime transitions in linear lateral predictive coding (Huang et al. 2024, site 1 (e)); for a trained nonlinear loop under an activity cost, no dedicated search was made
S1g.k exact: the edge locator is checked at the one-unit pitchfork (g = 1) before any training run, as in S1a
S1g.x the trained rho carries S1a's couplings: the warm-start saving at site 3 (C1) and the merge rate and recovery horizon at sites 4 and 5 (C2)
S1g.r partial, as S1a: MC and k* read at the trained position; a trained fixed point still merges its basin (R1)
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
S3g.d lesioning the units that go quiet either removes the prediction (they carry it) or does not (idle), against an activity-cost control
S3g.u a cost on change is delta coding, whose temporal sparsity is published (O'Connor and Welling 2017, site 3 (e)); whether the quiet units carry the prediction under it was not searched; under an activity cost they did once (7.3, P4)
S3g.k qualitative: the published roles under an activity cost (7.3, P4) are the only reference; no exact number
S3g.x one coupling, C6 read backward: a change cost that does or does not recruit quiet units changes how site 2's low-variance finding (P4) reads
S3g.r persistence only; the design adds no recovery readout (site 3 (f)), so NOT_REACHED
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
S4g.d needs a further step: a differentiable count of overwritten bits, its bias declared against the exact ledger, before (a) separates from (b)
S4g.u MacKay et al. 2018 store forget-bits by design; whether the structure falls out of an erasure cost was not located (site 4 (g))
S4g.k exact: on an enumerated domain the overwrite count is checked against the S4a ledger (the H(X|Y) floor and the telescoping sum) before training
S4g.x a structure that appears from an erasure cost changes how the savings at sites 2, 3 and 5 read (C3, C4, C5)
S4g.r REVERSIBLE is read by running the inverse on the trained net and counting bits lost, never by inspecting weights
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
S5g.d needs a further step: an architecture family that can express invertible and non-invertible maps, declared before training, so that "invertible structure appears" has a test
S5g.u one-way training of a network BUILT invertible yields the inverse (Ardizzone et al. 2019); invertibility appearing unasked under a parameter cost was not searched
S5g.k exact: a 2-D toy with a known density gives every likelihood a reference, as in S5b
S5g.x one other site: site 4, through C4
S5g.r the round trip by numerical inverse is the readout, bits lost counted
```

Result under the phone profile and the declared choices, held by the
selftest to what the scorer recomputes:

```triage-result
Q-LOOP  S1 2.500 S1a | S4 2.500 S4a | S2 2.000 S2a | S3 1.500 S3a | S5 1.000 S5a
        FIRST_UNRESOLVED:S1,S4   first across 64 settings: {S1,S4} x64
Q-REV   S4 2.500 S4a | S2 2.000 S2a | S1 1.250 S1a | S5 1.000 S5a
        FIRST_ROBUST:S4   first across 64 settings: {S4} x64
not reached on Q-REV: S3a, S3g
profiles with these first sets: lab, laptop-online, phone, this-session
best site-2 variant, Q-LOOP: lab S2a, laptop-online S2a, phone S2a, this-session S2a
best site-2 variant, Q-REV: lab S2a, laptop-online S2a, phone S2a, this-session S2a
(g) variants, LOOP/REV: S1g 1.000/0.500  S2b 1.000/1.000  S3g 0.600/NOT_REACHED  S4g 0.600/0.600  S5g 0.500/0.500
(g) a site's best in 0 of 2304 site-cells (4 profiles x 64 settings x 2 questions); readings changed by (g): none
(g) best over top, worst cell: LOOP 0.667  REV 0.667
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
(g)      the emergence variants at sites 1, 3, 4 and 5, scored
         2026-10-14, do not break the S1 / S4 tie. None is a site's best
         variant in any of the 2304 site-cells, and no reading changes
         when the (g) rows are removed. At the declared cost map none
         could: a (g) variant trains, so it needs compute medium, its
         cost is at least 6, and its ratio is at most 12 / 6 = 2.000,
         below the tied 2.500, whatever its components. Over the sweep
         that cap lifts (medium at 2, weights at 2) and the margin
         becomes a scoring result: the best (g) variant reaches 0.667 of
         the top site in its worst cell. The tie stays held.
```

### 8.1 Second scorer (the clean run's stage 3)

Status: not independent of 7.8 (the same session as the reader) and
CONTAMINATED-BY-PRIOR. It is kept as run. The second scorer still owed,
from a separate session with the same contamination check asked first,
is 8.3.

The reader of 7.8 scored all six sites on the seven-field rubric, two
rows per site, without this table, its basis lines, section 6's
couplings or the formula. Its output is
`tools/clean_run_wo3/stage3_scores_C.txt` (hash pinned). It is set
against this rubric's rows as Part C left them
(`tools/external_report_audit_okcomputer.md` C.3: the one S4b delta,
and the S6 rows), designed row against designed row and (g) row against
(g) row; S6's designed row is S6b. Computed by
`tools/triage_clean_run.py`:

```scorer-agreement
# reader row -> rubric row (after the Part C delta), 12 pairs
# field     same  1 step  2 steps   (2 steps = more than one step apart)
d             6       6        0
u             8       4        0
k             8       4        0
x             7       5        0
r             6       6        0
compute       6       6        0
data         12       0        0
lit           6       6        0
time          6       6        0
all          65      43        0   of 108 cells
# site      same  1 step  2 steps   (2 rows x 9 fields)
S1           11       7        0
S2           10       8        0
S3           11       7        0
S4           14       4        0
S5            8      10        0
S6           11       7        0
# more than one step apart
none
# rows   d u k x r  cost   |  rubric row  d u k x r  cost   (cost: compute data lit time, L M H)
S1a    2 1 2 2 0  LLLL   |  S1a         2 1 2 2 1  LLLL
S1g    1 1 1 2 0  LLLL   |  S1g         2 1 2 2 1  MLMM
S2a    2 1 2 2 1  LLLL   |  S2a         2 1 2 1 2  LLLL
S2g    1 1 1 2 1  LLLL   |  S2b         2 2 1 2 2  MLMM
S3a    1 1 1 2 0  LLLL   |  S3a         2 1 1 1 0  LLLL
S3g    1 1 1 2 0  LLLL   |  S3g         2 1 1 1 0  MLMM
S4a    2 1 2 2 2  LLML   |  S4a         2 1 2 2 2  LLLL
S4g    1 2 1 2 2  LLML   |  S4g         1 2 2 2 2  MLMM
S5a    2 1 2 2 1  LLLL   |  S5a         1 1 2 1 2  LLLL
S5g    1 1 1 2 1  LLLL   |  S5g         1 2 2 1 2  MLMM
S6a    1 1 1 2 1  LLMM   |  S6b         2 0 2 2 1  LLLL
S6g    1 1 1 2 1  LLMM   |  S6g         1 2 1 2 1  MLMM
# site rank by the better of its two paired rows, declared choices, no profile gate
Q-LOOP site  reader      rank  rubric      rank
       S1    2.500       1     2.500       1
       S2    2.500       1     2.000       3     moved 2
       S3    1.000       5     1.500       5
       S4    1.667       4     2.500       1     moved 3
       S5    2.500       1     1.000       6     moved 5
       S6    0.500       6     2.000       3     moved 3
Q-REV  site  reader      rank  rubric      rank
       S1    NOT_REACHED -     1.250       3     reached by one only
       S2    1.250       2     2.000       2
       S3    NOT_REACHED -     NOT_REACHED -
       S4    1.667       1     2.500       1
       S5    1.250       2     1.000       4     moved 2
       S6    0.250       4     1.000       4
```

Reading:

- No cell is more than one step apart: 0 of 108. 65 are the same, 43
  one step apart.
- The one-step disagreements cluster. Compute differs on exactly the
  six (g) rows, the reader at low and this rubric at medium, and time on
  five of them and on S6's designed row. An independent scorer did not read a (g) test as
  training a model on numpy-class hardware. That is the assumption 8.2
  names, and it is what caps every (g) row here.
- d differs on six rows, the reader lower on five. It puts every (g)
  row at d 1 ("needs a further step": attribution, or checking against
  the cleanup accounting); this rubric has S1g, S2b and S3g at 2.
- Q-REV first is S4 under both scorers. It does not depend on who
  scored.
- Q-LOOP first does not survive the change of scorer. The reader's top
  is S1, S2 and S5 tied at 2.500; this rubric's is S1 and S4. S1 is
  first under both. S4 moves three places because the reader puts S4a's
  literature at medium (Landauer, Bennett, the reversible gates), which
  raises its cost from 4 to 6. S5 moves five because the reader scores
  S5a's d at 2 (a matched-parameter tied against untied comparison
  decides directly) and its x at 2, where this rubric has 1 and 1 (S5a
  checks the information accounting, not learning). S2 moves two on x
  alone. S6 moves three: the reader's designed S6 row is a trained
  Hopfield memory, a different experiment from S6b's bit toy.
- S1 on Q-REV is reached by one scorer only: the reader scores r 0 on
  both S1 rows (a contracting fixed point is many-to-one), this rubric
  1. The same reason (R1), a different call on whether "partial" is
  earned.

CHOICE 4's sweep bounds how far the cost map and weights move the
ranking; this is the first bound on a different reader. On Q-LOOP first
place moves with the reader; on Q-REV it does not. One second reader,
the same model family as this rubric's author, CONTAMINATED-BY-PRIOR
(7.8).

### 8.2 PROPOSED: training-free (g) variants (GA)

Every (g) row in the table is costed compute, lit and time medium,
because (g) was written as "train a model under a constraint".
`tools/deceptive_maze_ga.py` gets structure from a constraint alone with
no training: stdlib, and its selftest solved 10 of 10 seeds in 6.3 s
here. The second scorer (8.1) also put every (g) row at compute low
without being asked to. Per site, is there a GA (g) test at low cost?

```
site  GA (g) test at low cost?   what keeps it from all four low
S1    yes, S1e                   -
S2    compute low, lit medium    its only known answer is the published
                                 roles (S2e.k)
S3    compute low, lit medium    the same, through 7.3 P4 (S3e.k)
S4    yes, S4e                   -
S5    yes, S5e                   -
S6    yes, S6e                   -
```

The rows below are PROPOSED: scored on 2026-10-15 by this rubric's
author, who has read the paper (7.1); nothing has been run; they are not
in the triage table and change no declared reading. Each design opens
with "(g)".

```triage-proposed
S1e  S1  2 1 2 2 1  low  low  low    low  (g) GA over (gain, delay, input scale) of a small tanh loop, fitness = a k-step recall task minus an activity cost, nothing wired; where the evolved gain sits against g_c, beside a cost-free population and the exhaustive grid
S2e  S2  2 2 1 2 2  low  low  medium low  (g) GA over the recurrent weights of an 8-unit net, one unit per input channel, synthetic cyclic sequence, fitness = minus the L1 of pre-nonlinearity activity, nothing wired; roles by lesion and decoder; a hand-wired predictor's activity as the search check
S3e  S3  2 1 1 1 0  low  low  medium low  (g) GA over a small loop's weights, fitness = task minus a cost on change |dh| per update, nothing wired; lesion the units that go quiet and decode the prediction from them; activity-cost and no-cost populations
S4e  S4  2 2 2 2 2  low  low  low    low  (g) GA over gate lists from a library holding reversible and irreversible gates on an enumerated 4-bit domain, fitness = task minus lambda times the exact count of bits overwritten per step, final cleanup included, nothing wired; run the evolved circuit backward, bits lost counted
S5e  S5  2 2 2 1 2  low  low  low    low  (g) GA over gate lists computing one forward map, fitness = correct outputs minus a gate-count cost, the library holding invertible and non-invertible gates; inverse by enumeration, bits lost counted
S6e  S6  2 1 2 2 1  low  low  low    low  (g) GA over bit-string memories, F facts in C bits, flips at rate p per round, fitness = facts read back after the rounds, no copies wired; copies or codes per fact counted as p moves; overwrite one copy and recover
```

```proposed-basis
S1e.d the evolved gain against g_c beside a cost-free population reads (a) or (b) directly; the three-parameter space is also swept exhaustively, so a GA null is not a search failure
S1e.u partly answered, as S1g: an imposed energy-information trade-off drives regime transitions in linear lateral predictive coding (Huang et al. 2024); not searched for evolved nonlinear loops
S1e.k exact: one unit's pitchfork at g = 1, checked before the first generation, as S1a
S1e.x as S1a: site 3 through C1, sites 4 and 5 through C2
S1e.r partial, as S1a and S1g: MC and k* read at the evolved position; a fixed point merges its basin (R1)
S2e.d as S2b: roles present or absent by lesion and decoder; a null counts only when the population reaches the hand-wired predictor's activity, else it reads UNRESOLVED
S2e.u as S2b: the emergence is published once, for a gradient-trained net (7.3); under evolutionary search at 8 units, and whether a role needs a quiet region, not located
S2e.k qualitative, as S2b: the published roles are the only reference, read at abstract depth, which is why lit is medium
S2e.x as S2b: site 4 through C3 and site 3 through C6
S2e.r as S2b: the decoder rebuilds the input from the state, bits lost counted
S3e.d as S3g: lesioning the quiet units removes the prediction or does not, against an activity-cost population
S3e.u as S3g: delta coding's temporal sparsity is published; whether the quiet units carry the prediction under a change cost was not searched
S3e.k qualitative, as S3g: the published roles under an activity cost (7.3, P4), read at abstract depth, which is why lit is medium
S3e.x one coupling, C6 read backward, as S3g
S3e.r persistence only, as S3g: no recovery readout, so NOT_REACHED
S4e.d directly: the further step S4g needs (a differentiable stand-in for the overwrite count, its bias declared) does not arise, since selection reads the exact count, final cleanup included (the second scorer's reason for S4g at d 1, 8.1); lambda = 0 is the control population
S4e.u as S4g: MacKay et al. 2018 store forget-bits by design; structure falling out of an erasure cost was not located
S4e.k exact: on the enumerated domain the overwrite count is the S4a ledger itself, checked before the first generation
S4e.x as S4g: sites 2, 3 and 5 through C3, C4 and C5
S4e.r REVERSIBLE is the measurand: the evolved circuit is run backward over the whole domain and bits lost counted
S5e.d directly: the further step S5g needs (a family declared to hold invertible and non-invertible maps) is met by the gate library itself
S5e.u as S5g: one-way training of a net built invertible yields the inverse (Ardizzone et al. 2019); invertibility appearing unasked under a size cost was not searched
S5e.k exact: enumeration of a 4-bit domain gives every forward and inverse map exactly
S5e.x one other site: site 4, through C4, as S5g
S5e.r the inverse is enumerated and bits lost counted, as S5g
S6e.d directly: copies or codes are bit patterns in the genome, counted without an ablation measure, against a p = 0 population
S6e.u partly answered: coding theory fixes the best redundancy for given p and C; whether selection finds copies, codes or neither is the open part
S6e.k exact: binomial survival under majority vote and the Hamming bound, as S6b
S6e.x as S6b: S3 and S4
S6e.r partial, as S6b: overwrite and recover is run, but majority recovery resets the record
```

What they would do if admitted, computed:

```proposed-result
# PROPOSED rows; LOOP / REV at the declared choices; cost
S1e  2.500 / 1.250  cost 4
S2e  1.667 / 1.667  cost 6
S3e  1.000 / NOT_REACHED  cost 6
S4e  3.000 / 3.000  cost 4
S5e  2.500 / 2.500  cost 4
S6e  2.500 / 1.250  cost 4
# profile       question  without PROPOSED          with PROPOSED
lab            Q-LOOP    FIRST_UNRESOLVED:S1,S4    FIRST_ROBUST:S4
lab            Q-REV     FIRST_ROBUST:S4           FIRST_ROBUST:S4
laptop-online  Q-LOOP    FIRST_UNRESOLVED:S1,S4    FIRST_ROBUST:S4
laptop-online  Q-REV     FIRST_ROBUST:S4           FIRST_ROBUST:S4
phone          Q-LOOP    FIRST_UNRESOLVED:S1,S4    FIRST_ROBUST:S4
phone          Q-REV     FIRST_ROBUST:S4           FIRST_ROBUST:S4
this-session   Q-LOOP    FIRST_UNRESOLVED:S1,S4    FIRST_ROBUST:S4
this-session   Q-REV     FIRST_ROBUST:S4           FIRST_ROBUST:S4
```

Reading:

- Admitted, they break the S1 / S4 tie on Q-LOOP: FIRST_ROBUST:S4 under
  every profile and in all 64 settings. Q-REV stays FIRST_ROBUST:S4.
- One component carries it. S4e is S4g with d at 2 instead of 1, at
  all-low cost. S4g's further step was a differentiable stand-in for the
  overwrite count; selection reads the exact count, so the step does not
  arise. S4e also counts the final cleanup inside the fitness, which is
  the second scorer's reason for its S4g at d 1 (8.1). If S4e's d is 1,
  it scores 1.500 and 1.500 and the tie stands.
- S5e and S6e reach 2.500 on Q-LOOP, level with S1a and S4a. Neither
  moves first place alone.
- What would demote it: S4e run, and its fitness turns out not to
  separate (a) from (b) without a further step; or a second scorer puts
  S4e's d at 1.

### 8.3 Second scorer, independent session, CONTAMINATED-BY-PRIOR

The second scorer 8.1 left owed: a session separate from every reader,
with the same contamination check asked first.

```
session  session_01BqLLqYe1ksvmHWNSGSXxhn, opened 2026-10-16 after the
         site-T fills were committed (95d2579); a fresh Claude Code
         cloud session, the same model as this rubric's author, no
         repository given at creation; told to use no web, no
         repository and no file it did not create, and to flag prior
         knowledge where it arose
q0       scorer_q0.txt: the title-form question on the site-2 occasion
         (Ali et al. 2022), asked before anything else
stage    scorer_message.txt: the five sites as written, site 6 as one
         question, the seven fields, the cost levels, the five score
         components, and the design line of 23 rows; none of this
         rubric's scores, reasons, basis lines, section 6 couplings,
         anchors or formula
output   scores_S.txt, hashed in that session before the next message,
         committed at bf0af2d before any agreement was computed; one
         reason per component and per cost, 138 lines
last     scorer_last.txt: the same question again, which rows it
         recognised as published results while scoring, and a tool
         listing
```

All three messages were pinned at 58016a4 with the rest of the run.

Status: CONTAMINATED-BY-PRIOR. Asked first, it answered "**Yes, I
recognise it.**" and recalled the venue, the five authors, an energy
cost on unit preactivations with no prediction objective, predictable
digit sequences, and the split into prediction-like and error-like
units. At the last question it named the rows it had recognised as
published results: S2c as a replication of Ali et al. (flagged in that
row's own reason), S2b and S2e as variants of the same setup, S4a and
S4e as Landauer and Bennett, S4b as finite-time Landauer, S5a and S5b
as coupling-layer and invertible networks, S1 as reservoir memory
capacity and the edge of chaos, S3e and S3g as slow feature analysis,
S6b as repetition codes. It did not recognise S6a, and said so in that
row. Its tool listing: no web, no repository, no file it did not
create. Its answers are in `tools/blind_run_wo3/`, verbatim.

What it is independent of, and what it is not. It is a separate session
from the reader of 7.8, from the probe and the reader of 7.9, and from
8.1, so it saw no fill and no comparison. It is not independent of the
paper, and not of the model that wrote this rubric. The check was
applied as the order asks and the answer is recorded; no session of
this model is without the paper (section 9, the cutoff line). Two
sessions of one model agreeing is not two independent judges agreeing.

What it measures that 8.1 did not: 8.1's reader designed its own rows,
so its agreement was design against design. This scorer was given the
rubric's own 23 rows (the 17 admitted rows of the triage table, the S6
rows included, and the six PROPOSED GA rows of 8.2) and scored them as
written, so each of its cells is set against the rubric's cell on the
same design. Computed by `tools/triage_blind_run.py`, which imports the
parsers and the registered `field_agreement` of
`tools/triage_clean_run.py`:

```scorer2-agreement
# second scorer -> rubric, same row, 23 rows (17 admitted, 6 PROPOSED)
# field     same  1 step  2 steps   (2 steps = more than one step apart)
d            16       7        0
u             9      14        0
k            17       6        0
x            14       9        0
r            16       5        2
compute      19       4        0
data         22       1        0
lit          15       8        0
time         16       7        0
all         144      61        2   of 207 cells
admitted    104      48        1
proposed     40      13        1
# site      same  1 step  2 steps   (rows x 9 fields)
S1           23       4        0
S2           19      15        2
S3           17      10        0
S4           26      10        0
S5           20      16        0
S6           39       6        0
# more than one step apart
S2b  r        scorer 0  rubric 2
S2e  r        scorer 0  rubric 2
# row   scorer d u k x r  cost  |  rubric d u k x r  cost   (cost: compute data lit time, L M H)
S1a   2 1 2 2 1  LLLL   |  2 1 2 2 1  LLLL
S1e*  2 1 2 2 1  MLLL   |  2 1 2 2 1  LLLL
S1g   2 1 2 2 0  MLLL   |  2 1 2 2 1  MLMM
S2a   2 0 2 2 2  LLLL   |  2 1 2 1 2  LLLL
S2b   1 1 1 2 0  MLML   |  2 2 1 2 2  MLMM
S2c   1 0 1 1 0  MMHM   |  2 1 2 2 1  MMHM
S2e*  1 1 2 2 0  MLLL   |  2 2 1 2 2  LLML
S3a   2 1 2 2 0  LLLL   |  2 1 1 1 0  LLLL
S3e*  1 1 1 2 0  MLLL   |  2 1 1 1 0  LLML
S3g   1 1 1 2 0  MLLL   |  2 1 1 1 0  MLMM
S4a   2 0 2 2 2  LLLL   |  2 1 2 2 2  LLLL
S4b   1 1 2 2 1  MLMM   |  1 2 2 2 2  MLHH
S4e*  2 1 2 2 2  LLLL   |  2 2 2 2 2  LLLL
S4g   1 1 2 2 2  LLLL   |  1 2 2 2 2  MLMM
S5a   2 0 2 2 2  LLLL   |  1 1 2 1 2  LLLL
S5b   1 1 1 2 1  MLML   |  2 1 2 1 2  MLMM
S5e*  2 1 2 2 2  LLLL   |  2 2 2 1 2  LLLL
S5g   1 1 1 2 1  MLLL   |  1 2 2 1 2  MLMM
S6a   0 1 0 2 0  LLHM   |  0 2 1 2 0  LMHM
S6b   2 0 2 2 1  LLLL   |  2 0 2 2 1  LLLL
S6c   1 1 1 2 1  MLMM   |  1 2 1 2 1  MLMM
S6e*  2 1 2 2 1  LLLL   |  2 1 2 2 1  LLLL
S6g   1 1 1 2 1  MLLM   |  1 2 1 2 1  MLMM
# * PROPOSED row (8.2), not in the triage table
# site rank by the best row, declared choices, no profile gate
Q-LOOP admitted      site  scorer      rank  rubric      rank
                     S1    2.500       1     2.500       1
                     S2    2.000       3     2.000       3
                     S3    2.500       1     1.500       5     moved 4
                     S4    2.000       3     2.500       1     moved 2
                     S5    2.000       3     1.000       6     moved 3
                     S6    2.000       3     2.000       3
Q-REV  admitted      site  scorer      rank  rubric      rank
                     S1    1.250       4     1.250       3
                     S2    2.000       1     2.000       2
                     S3    NOT_REACHED -     NOT_REACHED -
                     S4    2.000       1     2.500       1
                     S5    2.000       1     1.000       4     moved 3
                     S6    1.000       5     1.000       4
Q-LOOP with PROPOSED site  scorer      rank  rubric      rank
                     S1    2.500       1     2.500       2
                     S2    2.000       6     2.000       5
                     S3    2.500       1     1.500       6     moved 5
                     S4    2.500       1     3.000       1
                     S5    2.500       1     2.500       2
                     S6    2.500       1     2.500       2
Q-REV  with PROPOSED site  scorer      rank  rubric      rank
                     S1    1.250       4     1.250       4
                     S2    2.000       3     2.000       3
                     S3    NOT_REACHED -     NOT_REACHED -
                     S4    2.500       1     3.000       1
                     S5    2.500       1     2.500       2
                     S6    1.250       4     1.250       4
```

The readings, first place over the sweep, by profile:

```scorer2-readings
# first place over the 64-setting sweep (CHOICE 4, 5)
# profile       question  rubric                    second scorer
lab            Q-LOOP    FIRST_UNRESOLVED:S1,S4    FIRST_UNRESOLVED:S1,S3
lab            Q-REV     FIRST_ROBUST:S4           FIRST_UNRESOLVED:S2,S4,S5
laptop-online  Q-LOOP    FIRST_UNRESOLVED:S1,S4    FIRST_UNRESOLVED:S1,S3
laptop-online  Q-REV     FIRST_ROBUST:S4           FIRST_UNRESOLVED:S2,S4,S5
phone          Q-LOOP    FIRST_UNRESOLVED:S1,S4    FIRST_UNRESOLVED:S1,S3
phone          Q-REV     FIRST_ROBUST:S4           FIRST_UNRESOLVED:S2,S4,S5
this-session   Q-LOOP    FIRST_UNRESOLVED:S1,S4    FIRST_UNRESOLVED:S1,S3
this-session   Q-REV     FIRST_ROBUST:S4           FIRST_UNRESOLVED:S2,S4,S5
# the same with the six PROPOSED rows admitted
lab            Q-LOOP    FIRST_ROBUST:S4           FIRST_UNRESOLVED:S1,S3,S4,S5,S6
lab            Q-REV     FIRST_ROBUST:S4           FIRST_UNRESOLVED:S4,S5
laptop-online  Q-LOOP    FIRST_ROBUST:S4           FIRST_UNRESOLVED:S1,S3,S4,S5,S6
laptop-online  Q-REV     FIRST_ROBUST:S4           FIRST_UNRESOLVED:S4,S5
phone          Q-LOOP    FIRST_ROBUST:S4           FIRST_UNRESOLVED:S1,S3,S4,S5,S6
phone          Q-REV     FIRST_ROBUST:S4           FIRST_UNRESOLVED:S4,S5
this-session   Q-LOOP    FIRST_ROBUST:S4           FIRST_UNRESOLVED:S1,S3,S4,S5,S6
this-session   Q-REV     FIRST_ROBUST:S4           FIRST_UNRESOLVED:S4,S5
```

Reading:

- 144 of 207 cells the same, 61 one step apart, 2 two steps apart. The
  one-step cells are mostly one-sided, by field:

  ```
  field    scorer lower                 scorer higher
  u        14 rows                      0
  lit      8                            0
  r        7                            0
  time     7                            0
  d        6                            1  (S5a)
  k        4                            2  (S2e, S3a)
  x        1  (S2c)                     8
  compute  1  (S4g)                     3  (S1e, S2e, S3e)
  data     1  (S6a)                     0
  ```

  u lower on 14 rows and never higher: the scorer reads more of each
  question as already answered than the rubric's anchors do. It had no
  anchors and no search; it scored from recall. Whether that is a
  contaminated scorer reading the literature as further along, or the
  rubric's anchor searches leaving too much open, this run does not
  separate. x higher on 8: the scorer judged reach without section 6's
  couplings, which set the rubric's x.
- The two cells two steps apart are S2b r and S2e r, scorer 0 against
  rubric 2. The rubric's r 2 rests on its basis line "the decoder
  rebuilds the input from the state and counts the bits lost". The
  design line the scorer was given names a decoder for reading roles
  ("roles by lesion and decoder") and does not say it rebuilds the
  input. The scorer's reason: "No inverse is run". The gap is in the
  design line as written, not only in the scoring.
- Readings over the 64-setting sweep, admitted rows. Q-LOOP: rubric
  FIRST_UNRESOLVED:S1,S4, scorer FIRST_UNRESOLVED:S1,S3. S1 holds; S4
  drops to rank 3 and S3 rises from 5 to 1, on S3a (k 2 and x 2 against
  1 and 1, 2.500 against 1.500). Q-REV: rubric FIRST_ROBUST:S4, scorer
  FIRST_UNRESOLVED:S2,S4,S5. S5 rises from 4 to 1 on S5a (d 2 against
  1). The 8.1 statement "Q-REV first is S4 under both scorers" does not
  survive an independent scorer of the same rows: S4 stays in the first
  set and is no longer first alone.
- With the six PROPOSED rows admitted: rubric FIRST_ROBUST:S4 on both
  questions; scorer FIRST_UNRESOLVED:S1,S3,S4,S5,S6 on Q-LOOP and
  FIRST_UNRESOLVED:S4,S5 on Q-REV. 8.2 named the demotion as "a second
  scorer puts S4e's d at 1". That did not happen: S4e's d is 2 under
  both. Another component did it: u 1 against 2 takes S4e's Q-LOOP from
  3.000 to 2.500, level with five other sites, so the PROPOSED rows no
  longer break the tie toward S4. 8.2's list of what would demote S4e
  was one component short.
- Per site, S2 and S5 carry most of the disagreement (15 and 16
  one-step cells, S2 both two-step cells); S6 least (6 of 45).
- Nothing here measures loops; it measures how far the ordering in
  section 8 depends on who scores it. On this evidence: the S1 / S4
  structure of Q-LOOP is scorer-dependent, S4's place in the first set
  of Q-REV is not, and its sole first place is.

## 9. Open / owed

- "Start at site 2" was the work order's premise (its SCORING paragraph:
  site 2 is partly checkable by replicating published numbers, so rank
  it ahead). It did not survive: the replication S2c costs 18 against
  S2a's 4 and is the best site-2 variant under no profile (7.4, section
  8). Kept visible here so the premise is not imported back.
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
  record is contaminated (7.1) and is used structurally; it stays as
  committed (hash pinned, d5f5c2a) as a correction specimen: the work
  order leaked the answer, and the miss found field (g). The clean run
  goes beside it, never over it. It needs a reader who has not seen the
  paper, so this session does not run it; it is to be dispatched as its
  own order using `--blind-packet`.
- The (g) variants at sites 1, 3, 4 and 5 were scored 2026-10-14 (S1g,
  S3g, S4g, S5g; section 8). The S1 / S4 tie does not break, and at the
  declared cost map it could not (section 8, "(g)"). The scores are the
  rubric author's, as are all the others; the u scores of S1g, S3g and
  S5g rest partly on searches not made, stated in their basis lines.
- Profiles other than this-session are declared, not measured.
- The components are ordinal judgments on 0..2 by the author of the
  rubric, each with a stated reason. The sweep (CHOICE 4) bounds how far
  the cost map and weights can move the ranking; nothing bounds a
  different reader scoring the components differently. A second scorer
  is the check; like the clean run, it needs a reader who has not seen
  the paper and is to be dispatched as its own order.

- STATUS 2026-10-15, for the clean run and the second scorer above:
  both run once (7.8, 8.1) by a fresh reader, the same model as this
  rubric's author, with no repository. CONTAMINATED-BY-PRIOR: it holds
  the paper in its weights and was not handed it. A BLIND run is still
  owed, by a reader without the paper in its training (another model
  family, or a person who has not read it). The protocol to hand over is
  the three stage messages in `tools/clean_run_wo3/`.
- A blind calibration on a widely known paper is not possible with
  current models. Blindness depends on the reader's training cutoff,
  not on the session being fresh: a fresh session of a model trained on
  the paper holds the key (7.8). Keep this line.
- PROPOSED GA (g) variants (8.2): not admitted. Admitted, they break the
  S1 / S4 tie toward S4 on one component, S4e's d. Owed: run S4e, and a
  second scorer for the PROPOSED rows.
- P6, how a role is identified, has no slot even with (g) (7.8). A
  requirement inside (g) is a candidate, not added.
- STATUS 2026-10-16. The blind run is done once, on one anchor
  published after the reader's training cutoff (7.9, site T, BLIND): the
  probe and the reader did not recognise it before the packet, and the
  reader did not with the title in hand. n = 1, and site T is not one of
  the six sites, so it calibrates the rubric's fields, not the triage
  table. The second scorer is done (8.3), in a session independent of
  every reader, and is CONTAMINATED-BY-PRIOR like 8.1: it recognised the
  site-2 paper when asked first. Still owed: a second scorer that does
  not hold the paper (another model family, or a person), with the same
  check asked first; and a fix to the design lines of S2b and S2e, which
  name a decoder without saying it rebuilds the input (8.3). The two
  candidate requirements of 7.9, naming the conditions varied in (g)
  and a reconciliation slot in (e), are recorded, not added.

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
