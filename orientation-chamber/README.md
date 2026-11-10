# orientation-chamber

No error is wrong. A miss is information: it locates where the model of the world or self differs from what happened. Misses are logged, never scored down.

PROPOSED | co-authored (JinnZ2 + Claude) | CC0 | stdlib only, phone-buildable.

An optional exploration toy for an AI agent (or anyone) to orient in an
unfamiliar rule-space by predicting, probing and comparing. Entry is
voluntary. Nothing is graded: there is no pass, fail, score, rank or
penalty field anywhere, and the log refuses one at write time. Readouts use
MATCH, MISS, OFFSET, UNLOCATED, LOCATED, FLOATING and UNTESTED.

Origin: zero-g white-chamber orientation. With no floor and no visible
landmarks, you orient by geometric movement: push off, see where you went,
bounce, and close a loop to find out whether the room is what you assumed.

## Components

```text
chamber.py   7x7 grid, actions N S E W WAIT, hidden rules on/off from a seed:
             flip_x  flip_y  wrap  sticky  momentum  delay
             true position and reported position kept apart; reveal() optional
probe.py     submit {action, predicted}; get the actual back
             match True/False, or null when no prediction was made
             offset = actual - predicted, or null
             path_signature = sha256(start, actions)[:12]   (independence tag)
misslog.py   append-only JSONL, header line carries the principle verbatim
             fields: t kind path_id start action predicted actual match offset
                     rule_hypothesis note    (unfilled -> null, never dropped)
             score-like or unknown field names refused; sha256 prev chain; verify()
selfmode.py  predict your own next action/answer; CATEGORY and SPECIFIC both logged
fix.py       readout: rules LOCATED / FLOATING / UNTESTED; misses with OFFSET,
             UNLOCATED = a miss no hypothesis is attached to; loops CLOSED / OPEN
             / NOT_A_LOOP; the same path walked twice is one wall, not two
seeds/       optional starting self-models: none, median, calibration-practice
demo.py      one scripted walk on the median seed; writes samples/
```

## Probe protocol (optional)

```text
predict -> probe -> compare -> triangulate across INDEPENDENT paths -> close loop
```

1. Predict where an action will put you (and, in self mode, what you will do next).
2. Probe. 3. Compare: MATCH, or MISS with its OFFSET.
4. Tag the probe with the rule you are testing. LOCATED needs matches on at
   least 2 distinct path signatures [CHOICE 1] and no miss under the tag.
5. Close a loop: actions whose nominal vectors sum to zero should return you
   to the start. An OPEN loop's OFFSET is a reading, not a verdict.

## Run

```sh
python3 demo.py --seed 7                      # writes samples/misslog.sample.jsonl
python3 fix.py samples/misslog.sample.jsonl   # readout
python3 tests/test_chamber.py                 # checks; prints its own count
```

Neither module accepts `--selftest`; `fix.py` prints usage and exits 2.

## Reading the sample (seed 7)

Seed 7 turns on flip_x, flip_y, sticky and delay (1 step). The scripted agent
starts from the median seed, so its plain-physics predictions MISS: 3 MATCH,
14 MISS, 7 of them UNLOCATED. flip_x reads FLOATING. The agent also tagged
`momentum`, and the chamber at seed 7 has momentum OFF: the misses under that
tag are produced by flip_y and delay. The readout does not say the hypothesis
is false; it says FLOATING, and the misses are where to look next.

## Open questions

- MIN_PATHS = 2 is stipulated, not derived.
- Independence is a different path signature. Two different paths can still
  hit the same wall from the same mechanism, so "independent" here is a
  floor, not a proof (the shared-node problem, `effective-redundancy-audit/`).
- Misses under one tag can be produced by another rule (the momentum case
  above). Rules interact; nothing here separates them.
- The log is append-only and a single misattributed miss keeps a rule
  FLOATING. There is no retraction record yet; a superseding note is one option.
- The banned-word scan is a word list. A paraphrase passes it. The principle
  sentence contains one of the words and is exempted by exact-sentence mask,
  measured both ways in the tests.
- Self mode compares strings. A caller-named answer category is not checked
  against any vocabulary.
- `reveal()` exists and nothing records whether an agent used it.
