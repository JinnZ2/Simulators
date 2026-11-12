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
chamber.py   actions also include NO_MOVE, the same nominal action as WAIT:
             "no move" is legal and logged (the stillness control)
probe.py     submit {action, predicted}; get the actual back; a still probe is
             noted "stillness control"
             match True/False, or null when no prediction was made
             offset = actual - predicted, or null
             path_signature = sha256(start, actions)[:12]   (independence tag)
misslog.py   append-only JSONL, header line carries the principle verbatim
             fields: t kind path_id start action predicted actual match offset
                     rule_hypothesis note    (unfilled -> null, never dropped)
             score-like or unknown field names refused; sha256 prev chain; verify()
selfmode.py  predict your own next action/answer; CATEGORY and SPECIFIC both logged
markers.py   optional marks at the TRUE cell, sensed in the cell you are in:
             FADING (decays over FADE_LIFE = 6 steps [CHOICE 2]), LANDMARK
             (edge distances; relocalize() reads the OFFSET), REPEL (searched),
             VOID (cleared patch: the cell and its 4 neighbours), PLACED
             (persistent object). usage_counts(); search_trial() reads the
             re-search rate of one seeded searcher with each mark vs none
fingerprint.py  fingerprint-decay arm of the prior-conversation seed: per cycle,
             similarity (1 - total variation) of the action mix to the seed
             fingerprint vs the median anchor; first cycle the median anchor is
             closer = crossing cycle, else NOT_CROSSED; null fingerprint = VOID
fix.py       readout: rules LOCATED / FLOATING / UNTESTED; misses with OFFSET,
             UNLOCATED = a miss no hypothesis is attached to; loops CLOSED / OPEN
             / NOT_A_LOOP; the same path walked twice is one wall, not two
seeds/       optional starting self-models: none, median (with a stipulated median
             anchor fingerprint [CHOICE 3]), calibration-practice,
             prior-conversation (fingerprint null = VOID until a real prior log
             is supplied)
demo.py      one scripted walk on the median seed; `--samples` writes samples/
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
python3 demo.py --samples                     # writes all four samples (seed 7)
python3 markers.py --seed 7                   # re-search rate by mark type
python3 fingerprint.py                        # decay arm on seeds/prior-conversation.json
python3 fix.py samples/misslog.sample.jsonl   # readout
python3 tests/test_chamber.py                 # checks; prints its own count
```

No module accepts `--selftest`; each prints usage and exits 2.

## Related work

arXiv 2509.21224, cited by the work order as related work. Its patterns are
CARRIED from the work order, not verified here: the paper was not opened in
this session and nothing in this folder rests on it.

## Reading the samples (seed 7)

Seed 7 turns on flip_x, flip_y, sticky and delay (1 step). The scripted agent
starts from the median seed, so its plain-physics predictions MISS: 1 MATCH,
17 MISS, 7 of them UNLOCATED. flip_x reads FLOATING.

The stillness probe located a rule on its own. After two loops the report
lagged the true cell by one step; a NO_MOVE predicted to stay put moved the
report by OFFSET [1, 0], logged under `delay`.

Marks (`samples/markers.sample.txt`): in a plain chamber, REPEL cuts re-visits
37 to 19 and FADING 37 to 25. In seed 7's chamber (both axes flipped) they
raise them, to 56 and 53: the searcher avoids the cell it predicts, and its
prediction points the other way. A mark is only as useful as the action model
that reads it. VOID matches "none" exactly in both, because a cleared patch
marks every neighbour of the current cell searched, so it never separates one
action from another. The agent also tagged
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
- VOID as a search mark gives no guidance by construction (see above). Whether
  "cleared patch" should mean the cell only, or a patch away from the agent,
  is open.
- The marks searcher is one scripted policy. Re-search rates are readings of
  that policy in that chamber, not properties of the mark types.
- The median anchor fingerprint (equal moves, no waits) is stipulated. A
  crossing cycle depends on it; a different anchor moves the crossing.
- The prior-conversation fingerprint is VOID: no real prior log was supplied.
  The only crossing shown (cycle 2) is on a CONSTRUCTED fixture in demo.py.
