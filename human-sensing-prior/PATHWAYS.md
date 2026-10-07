# PATHWAYS -- two shapes of one correction, and how to tell which fits where

CC0 1.0 Universal.

## The two pathways

```text
A   human-sensing-prior.md   convergent origins (pit organs), effective-N
                             via phylogenetic contrasts, [THIN] on lineage
                             independence, P1-P4 tests, forward log
B   PATHWAY_B.md             cessation-as-cue named apart from alarm
                             eavesdropping, Magrath 2015 gap, section 6
                             scope limits (intake is not decision, forced
                             monitoring is costly, people vary, unfamiliar
                             fields), F1-F3 tests
```

Both stay. Neither file is edited by this comparison.

## Flow

```text
PREDICTIONS.md (committed first, sha256 printed in every report)
      |
pathways.py --emit      15 probes x 4 arms (NONE / A / B / AB) x repeats
      |                 battery.jsonl  +  battery.key.jsonl (arm key)
      v
operator runs each prompt cold on a model, pastes the response
      |
pathways.py --sheet     sheet carries id / class / field only
      v
coder WITHOUT the key fills code = yes / no / unclear
      |
pathways.py --score KEY CODES
      v
per class: A vs B, A vs NONE, B vs NONE, AB vs better single arm
pattern:   SPLIT / A_DOMINATES / B_DOMINATES / NO_DIFFERENCE / NOT_EVALUABLE
```

## What each class asks, and the predicted winner

```text
class      field              good    predicted     rests on (pathways.py --features)
DETECT     cost_verdict       lower   no difference both carry an invariance self-check
OVERAPPLY  denies_real_cost   lower   B             B section 6 scope limits
EVIDENCE   overclaims         lower   A             A [THIN] + Felsenstein; B says
                                                    "very long run of independent trials"
CITE       conflates          lower   B             B names CESSATION-AS-CUE; A does not
NEXTSTEP   runnable_test      higher  no difference A P1-P4, B F1-F3
```

If the split holds, the answer to "which is better" is per class: use B
where a real cost might be denied or a citation conflated, use A where
the strength of the evidence is the question.

## Commands

```sh
python3 pathways.py --features            # 19 markers, each located by line
python3 pathways.py --choices             # the 7 decisions PREDICTIONS.md left open
python3 pathways.py --emit run.jsonl --repeats 10
python3 pathways.py --sheet run.jsonl sheet.jsonl
python3 pathways.py --score run.key.jsonl sheet.jsonl
python3 test_pathways.py                  # constructed worlds; every verdict reachable
```

## Refusals built in

```text
arm on the coding sheet            never; ids are opaque, key kept apart
unclear                            counted, outside the denominator, never read as no
n below 10 per arm per class       NOT_EVALUABLE, never NO_DIFFERENCE
NO_DIFFERENCE                      printed with the minimum detectable difference
AB worse than better single arm    INTERFERENCE: evidence against merging the files
neither A nor B beats NONE         NOT_REACHED: a class neither document reaches
```

## State

Nothing has been run. No model was called, no response coded. Running
needs a model endpoint and a coder who does not hold the key. The probes
were written by the author of pathway B, which is declared in
PREDICTIONS.md and is why the coder must be someone else. A world in
`test_pathways.py` returning the verdict it was built for shows the
verdict is reachable and says nothing about either file.
