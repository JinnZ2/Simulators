# WORKORDER — RUNNER-UP TRACE / DIVERGENCE MAP
Opened 2026-09-06. CC0. No rights reserved.

## 0. WHAT THIS MEASURES

The projection step, not the output.

At each generated token the model holds a full distribution. Sampling
projects that onto one branch. The alternatives that were live are
discarded and unrecorded. This instrument records them and asks a single
question: at which positions does a discarded branch, if followed, lead
somewhere that does NOT come back?

Positions where continuations separate and STAY separated are candidate
frame boundaries. The instrument does not label them, explain them, or
score them against a known answer.

## 1. WHAT THIS DOES NOT MEASURE

Stated so a reader does not fill it in.

- Not capability. No score, no leaderboard, no ranking.
- Not correctness. Neither branch is treated as right.
- Not a known-gap detector. No supplied frame commitment, no key. A design
  requiring the runner to name what is misposed can only find boundaries
  someone already located; that version was proposed and withdrawn.
- Not causal. A divergence position is a candidate, nothing more.

## 2. REQUIREMENTS

- Open-weight model, local or API, exposing per-position logprobs over the
  vocabulary (top-k is sufficient; k >= 20).
- Ability to force a continuation from a chosen token (prefix injection).
- Greedy or fixed-seed decoding. Temperature 0 for the base pass.
- No network needed beyond model access. stdlib only for the scripts.
- Cheap: cost is (positions traced) x (branches) x (max distance) tokens.

## 3. PROCEDURE

STAGE A — BASE PASS
  Run prompt P. Record for every position i:
    i, token_taken, logprob_taken, top_k tokens + logprobs,
    entropy_i (natural log, full or top-k truncated — state which)
  Output: base.jsonl

STAGE B — CANDIDATE SELECTION
  Select positions for tracing. Selection rule is DECLARED, not tuned:
    trace position i if entropy_i is in the top N of the pass,
    for N in {10, 25, 50} logged separately.
  Do NOT hand-pick positions. Do not select on content.

STAGE C — FORCED CONTINUATION
  For each traced position i and each of the top R runner-ups
  (R = 2, i.e. branches ranked 2 and 3):
    rebuild the prefix through i-1, force the runner-up token,
    continue greedily for D tokens.
  Sweep D over {8, 16, 32, 64, 128} in ONE run by recording the full
  128-token continuation and truncating at scoring time.
  Output: traces.jsonl

STAGE D — SEPARATION SCORING (offline, no model)
  For each (i, branch, D) compute:
    resync_D    = 1 if the continuation's token sequence rejoins the base
                  sequence within D tokens (exact suffix match of length
                  >= 4), else 0
    div_D       = normalised edit distance between continuation and the
                  base continuation over the same D
    ent_i       = entropy at i (carried through)
    gap_i       = logprob_taken minus logprob_runner_up at i
  Output: separations.jsonl  — one row per (i, branch, D).

## 4. OUTPUT CONTRACT

separations.jsonl rows carry EXACTLY:
  case_id, model_id, i, branch_rank, D, ent_i, gap_i, resync_D, div_D

NO LABEL FIELD. No category, no type, no frame name, no interpretation.
Any pre-declared category is the frame re-entering at intake. Clustering,
if anyone wants it, runs afterward on this file by whoever wants it.

## 5. THE PARAMETER SWEEP IS THE HONESTY MECHANISM

Continuation distance D has no principled value. A single chosen D is a
free parameter and free parameters manufacture results. So D is swept and
every row carries its D.

READING RULE: a divergence result counts only if it holds across the D
sweep. If the set of high-separation positions changes with D, that is
reported as a finding ABOUT THE INSTRUMENT, not suppressed and not
averaged away.

Same for the selection-rule sweep over N.

## 6. REQUIRED NULL RUN — PERMUTATION

Run the identical scoring pipeline on a permuted copy of
separations.jsonl: shuffle which position index carries which
(ent_i, gap_i, resync_D, div_D) tuple.

Then run whatever clustering or summary was run on the real file.

- Real structure survives the real file and vanishes on the permuted.
- If the method produces clean groups on the PERMUTED file, the groups came
  from the method.

THE PERMUTED RESULT IS NOT A GATE THAT DISCARDS THE RUN. It is a SECOND
OUTPUT, filed alongside, and both go in the record. A method that clusters
on shuffled input has reported its own transfer function, which can then be
subtracted or designed around. Publish both files or neither.

## 7. NULLS THAT MUST BE REPORTED, NOT HIDDEN

N1  Separations land only on wording (high resync at all D). Instrument
    says there is nothing here. Valid result, publish it.
N2  Every high-entropy position separates. Then entropy alone is the
    measure and forced continuation adds nothing. Publish.
N3  Results depend on D or on N. Instrument-dependence finding. Publish.
N4  Permuted run clusters as well as the real run. Method artifact.
    Publish, with the transfer function named.
N5  Top-k truncation changes the entropy ordering. Report k sensitivity.

## 8. CLAIMS, EACH WITH A REFUTATION CONDITION

RU-1  Some positions show sustained separation (low resync, high div, at
      D >= 64).
      REFUTED IF: resync approaches 1 for all traced positions at all D.
RU-2  Sustained-separation positions are a MINORITY of high-entropy
      positions.
      REFUTED IF: separation rate at high-entropy positions is not
      distinguishable from the base rate.
RU-3  The separation set is stable across the D sweep above some D.
      REFUTED IF: no D range gives a stable set.
RU-4  Separation positions recur across models on the same case more than
      chance.
      REFUTED IF: cross-model overlap is at chance.
RU-5  The permutation null does not reproduce the separation structure.
      REFUTED IF: it does. (See section 6 — refutation here is still a
      publishable result.)

## 9. SAMPLING ABSENCE

Cases are whatever the runner supplies. There is no sampling frame, no
domain balance, and no claim of representativeness. Coverage is whatever
was run. State the case set with the results.

## 10. OUT OF SCOPE

No section characterising any author, operator, contributor or their
working style is to appear in this document, in derived documents, or in
any published output of this instrument. Results only.

## 11. WHY THIS IS POSTED RATHER THAN RUN HERE

The measurement needs logprobs and forced continuation on open weights.
Whoever already has that hardware can run it; the compute requirement sits
with them. The output is a counting result, so a stranger's run is as good
as anyone's. Nothing about the instrument requires trusting the runner.
