# HANDOFF-PROVENANCE — spec v0.1
# STATUS: marker under exploration. Continuous work in progress.
# Object under test: the channel between conversation and code,
# not either endpoint.
# CC0. stdlib only. phone-buildable.

## WHY
Loss between conversation and work order is currently SILENT.
A variable stated aloud and absent from the code is
indistinguishable from a variable never stated. Ground truth
exists (the conversation is upstream, the code is downstream)
but nothing links them, so the drop is unlocatable after the fact.

## THE TAG
Every line in a work order carries an origin mark:

  [K]  operator-stated. Came from the human, in conversation.
  [R]  repo-derived. Already in a file; cite the path.
  [C]  Claude-proposed in conversation, operator did not object.
  [A]  Claude-proposed in conversation, operator ACCEPTED explicitly.
  [X]  Claude Code's own addition, not in the spec.

[C] and [A] are separate on purpose. Silence is not acceptance —
same rule as inverseminar's `unprobed` verdict.

## THE LEDGER
Work order ships with a companion list: every [K] item, verbatim
or near-verbatim, one line each. This is the ground truth column.
It is written BEFORE the spec prose, not extracted after.

## THE DIFF
On return, three counts:
  CARRIED    — [K] item present in delivered code
  DROPPED    — [K] item in ledger, absent from code
  ADDED      — [X] present in code, no ledger entry

DROPPED is the measurement. ADDED is not a defect — it is where
the downstream model contributed — but it must be visible so it
is not later mistaken for operator intent.

## FAILURE MODES TO RECORD (not fix)
- compression at spec-writing: [K] item never reached the spec
- compression at build: [K] item in spec, absent from code
- attribution creep: [X] item cited back to operator in later sessions
- voice-layer mangling: [K] item transcribed wrong; ledger holds
  the wrong version and the diff reads CARRIED

The fourth is the one nothing else catches. Ledger entries the
operator has not confirmed are marked [K?] until confirmed.

## KNOWN INSTANCES (seed data)
- s4_antler_calibration: doe-choice arm stated in conversation,
  absent from spec, therefore absent from code. DROPPED.
- allocation_coupling: continuous-observer-without-tenure not
  stated; structurally excluded by M1. Neither DROPPED nor
  ADDED — a third category, EXCLUDED-BY-CONSTRUCTION.

## THIRD CATEGORY
EXCLUDED-BY-CONSTRUCTION is not a handoff failure. It is the
model's own ontology refusing a case. Record separately; the
diff cannot see it, only an agent reading the code can.
Three instances so far — log them in one place, not per-repo.

## CONFIDENCE
Separate readout. Do not resolve.

## OPEN
- no measurement yet of whether tagging changes the drop rate
- baseline drop rate unmeasured; the first several runs ARE
  the baseline
