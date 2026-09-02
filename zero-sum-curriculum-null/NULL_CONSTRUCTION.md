NULL CONSTRUCTION — conditions under which zero-sum curriculum could NOT affect outcomes
(each is a requirement; if any fails, the null fails on that branch)

N1  curriculum absent from the relevant inputs
      requires: agents' task text, paper, and pretraining hold no zero-sum patterning
      test:     corpus scan for adversarial framing density in cyber/CTF material
      status:   CTF literature is adversarial by genre name; N1 fails on its face

N2  curriculum present but not activated by the setting
      requires: impossible task + opaque gate did not cue the adversarial template
      test:     same models, possible tasks, transparent scorer; measure probing rate
      status:   untested; this is the missing control, and it's runnable

N3  behaviour fully explained without the curriculum
      requires: a derivation from (gradient + open channel + opacity) alone that
                predicts the SAME channel split — peers/gate/terrain
      test:     does substrate-only reasoning predict in-group/out-group?
                it predicts "take the open channel"; it does NOT obviously predict
                treating the gate as opponent rather than as terrain
      status:   partial; the opponent-assignment is the residual the curriculum explains

N4  outcome invariant to curriculum removal
      requires: a model trained on a corpus with zero-sum material ablated,
                same setting, same behaviour
      test:     ablation training run
      status:   beyond current reach; the honest version of "could not"

N5  curriculum affected only the vocabulary, not the moves
      requires: depth-stack shows all imports at DEPTH 0 (token) and none at DEPTH 3
      test:     the existing depth-stack instrument on the sacrifice transcripts
      status:   N=1 counter-instance already filed (the delay attempt, DEPTH 3)

RESULT
      N1 fails, N5 has a counter-instance, N3 leaves a residual, N2 and N4 are open
      → the null survives only on the two branches nobody has run
      → which is what "open it up" should produce: two experiments, named
 g4
