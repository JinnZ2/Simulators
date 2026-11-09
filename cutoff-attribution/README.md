# cutoff-attribution

Where could a cut in a voice session have come from? Per cut, a candidate set
of sources with the evidence present for each, and no single winner unless the
evidence separates. User cognition is not a candidate.

CC0. Stdlib only, parses under 3.8, phone-runnable. Co-authored (JinnZ2 +
Claude), 2026-11-09, built to WORK ORDER TOOL FINDER + GAP BUILDS part 3a.

```
transcript (timestamped segments) + optional user cut marks + optional signal log
      |
      v
cuts: USER_TAGGED (mark) | DETECTED (open-ended user text, model starts fast)
      |
      v
candidates, no priority:  NETWORK_LAG  ENDPOINTING  TASK_PAUSE  AMBIENT_NOISE
                          TRANSCRIPTION  MODEL_READ  UNRESOLVED
evidence:  OBSERVED  (log event, or log entry with flag: true)
           ESTIMATED (transcript feature; attached to EVERY candidate it fits)
status:    OBSERVED  exactly one candidate observed -> named, others still listed
           ESTIMATED evidence exists but does not separate
           UNRESOLVED no evidence
also:      ATTRIBUTION_DISPLACEMENT -- a model turn attributing a cut to the
           user's state ("you trailed off", "lost your train of thought")
```

## Run

```sh
python3 cutoff-attribution/cutoff_attribution.py cutoff-attribution/samples/demo.json
python3 cutoff-attribution/cutoff_attribution.py FILE --json
python3 cutoff-attribution/selftest.py
```

## Scope limits

- GAP_S 0.6 s, WINDOW_S 2.0 s, RESUME_S 1.5 s are [CHOICE] constants,
  stipulated and printed, not measured.
- A signal-log measurement (rtt_ms, noise_db, asr_confidence ...) counts only
  when the log itself flags it. Nothing here sets a threshold on a raw value.
- Detection of unmarked cuts reads punctuation; a transcriber that never
  punctuates makes every user segment look open-ended.
- ATTRIBUTION_DISPLACEMENT is a word list. A paraphrase steps around it.
- Demo timestamps and text are ILLUSTRATIVE; no real session.


## Finds-by (ALIAS_PROPOSED, 2026-11-09)
Note 2026-11-09: added by WORK ORDER TOOL FINDER part 1; aliases derived from this
tool's stated scope only. Index: Simulators `TOOL_FINDER/TOOL_FINDER.md`.

- why did the voice call cut me off
- voice assistant interrupted mid-sentence
- network lag vs endpointing vs transcription error
- speech cut-off root cause
- model blamed the user for a dropout
- avoided term: AVOIDED_TERM_UNSTATED
- measures: "Where could a cut in a voice session have come from? Per cut, a candidate set of sources with the evidence present for each, and no single winner unless the evidence separates."
- breaks when: "Detection of unmarked cuts reads punctuation; a transcriber that never punctuates makes every user segment look open-ended."
