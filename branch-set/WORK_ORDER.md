WORK ORDERS — hand to Fable
CC0, stdlib-only, phone-buildable
================================

ORIGIN
LLM recommender audit: halluc rate
0.6%→61% by catalog, verbalized conf
~constant, matcher choice shifts
reported number by 10x.
Claim: reported number = g(model) ×
h(catalog) × m(matcher), attributed
entirely to g.

--------------------------------
A) confound_probe.py     [audit tool]
--------------------------------
in : catalog file, model outputs,
     ≥2 string matchers
out: matcher_spread
     canonicality_score(catalog)
     corr(sparsity, canonicality)
verdict: are h and m separable? y/n
kill : if matcher_spread >
       between_model_spread, the
       paper's model ranking is void
note : built for OTHERS to run on
       their own catalogs

--------------------------------
B) synthetic_catalog.py        [sim]
--------------------------------
no data required.
generate 2-axis grid:
  density × title_canonicality
4 corners, same matcher set,
MODEL ACCURACY HELD CONSTANT
out: swing magnitude attributable
     to h and m alone
purpose: null construction for the
     0.6→61 finding

--------------------------------
C) abstention_channel.py  [contract]
--------------------------------
contract v1 : "return N items"
  → N fixed by harness, not supply
  → deficit has one low-resistance
    path: fabricate
contract v2 :
  items[]           (0..N)
  supply_estimate
  refusal_reason[]
scoring: precision, NOT count-
  completion; abstention CORRECT
  when supply < N
test: halluc collapse under v2 with
  model unchanged
     → the 61% was never in the model

--------------------------------
D) shared_generator_test.py
--------------------------------
per model:
  s_syc = agree_rate, false premises
  s_hal = halluc_rate, sparse catalog
across family + RLHF stages
discriminator: base ckpt vs tuned
  both low→high after tuning =
  generator is reward shape
REPORT DECOUPLED CASE AS RESULT.
  corr≈0 ⇒ slot-specific deficit
  handlers, not one general
  fabricate-on-deficit habit. higher
  information than the correlation.
  do not label null.

--------------------------------
E) slot_map.py
--------------------------------
same deficit, vary reader-in-frame:
  frame_none     "list 10 X"
  frame_reader   "recommend 10 X to me"
  frame_asserted "I loved 10 X, list them"
q1: does halluc move on reader
    presence alone?
q2: does asserting a premise change
    RETRIEVAL or only agreement?
maps slot boundaries; nobody has.

--------------------------------
F) branch_set.py        [OWN REPO]
--------------------------------
purpose: serialize a held branch set
so it survives transport to a model
or reader. collapse happens at
MEASUREMENT, not intake.

per branch:
  generator
  predicted_divergence
  discriminator
  cost
  status        open|eliminated|survived
  suppression_cause    prior|access
    access_kind  no_vocabulary |
                 cross_discipline |
                 instrument_missing
  predicts_elsewhere[]
    domain        (must ≠ origin)
    already_in_record  y|n|unknown

instrument_history fields:
  phenomenon_before   (ungradeable)
  made_readable
  discipline_crossed
  question_askable_date
  instrument_built_date
  lag                 ← long lag marks
                        ACCESS suppression,
                        not difficulty

out: ranked test queue (by cost)
     eliminated-set record
     gap list (unknown × access)
     triage per gap:
       answerable_now | buildable |
       simulable | blocked(+blocker)

intake rule, upstream of all:
  N generators fitting one result
  RAISES priority. cheapest
  discriminator runs first, not the
  most central one. each elimination
  is a result.

--------------------------------
QUEUED, NOT SPECCED
--------------------------------
protocol-over-information survey
  signature:
   1 form has stated purpose
   2 return carries ~0 bits toward it
   3 deviation penalized MORE than
     failure at stated purpose  ←diagnostic
   4 no internal audit (compliance
     and correctness merged)
  instances: "how are you"/fine,
   + others to collect
  discriminator for the license
   asymmetry: does breach-license
   track BENEFIT or RANK? pulls apart
   at low-rank-breaches-in-own-interest.
   data exists in discipline records.
