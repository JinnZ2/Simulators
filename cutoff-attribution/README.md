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


## Channel chain (Amendment A1, 2026-11-09)

No reading here is direct. Each candidate sits at one hop of the voice chain,
and its evidence is read through that hop.

| hop | candidates | known deviation sources | known-reference check |
|---|---|---|---|
| sensor | AMBIENT_NOISE, TASK_PAUSE | room noise, mic placement or clipping, the user's task | caller (`reference_checks`) |
| encoding | ENDPOINTING | endpointer / VAD timeout, codec concealment | caller |
| transmission | NETWORK_LAG | latency, drop, relay reconnect | caller (e.g. a known ping sequence echoed) |
| decoding | TRANSCRIPTION | ASR misrecognition, punctuation, [inaudible] tagging | caller (e.g. a known phrase read through ASR) |
| inference | MODEL_READ | partial utterance read as complete | caller |
| inference (this tool) | -- | punctuation rule, word list, [CHOICE] constants | built in, every run: a known cut must be detected |

A log event counts as `OBSERVED` only when its hop passed a reference check.
Through an unchecked hop it is `RECORDED_VIA_UNVERIFIED_HOP`, through a failed
one `RECORDED_VIA_FAILED_HOP`; both count as ESTIMATED. "OBSERVED" therefore
means "recorded at a hop that reproduced a known input", not a direct view.
Every cut is a `tools/channel_chain.py` record with a chain class that is never
DIRECT.

## Terms (Amendment A2)

ATTRIBUTION_DISPLACEMENT cites two terms from Cross-Domain-Toolkit
`telemetry_vocabulary/terms.md`, read from a sibling checkout at run time with
their line locator, and not re-coined: **Interiority substitution** (a channel
event attributed to the user's state) and **Care inversion** (the same,
delivered as care). Which phrase maps to which term is this tool's reading.
With no checkout the term reads `TERM_NOT_CHECKED`.

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
- breaks when (Note 2026-11-09, ICSC v0.2 T30): the null calibration's controls were written to the same rule set they test, so its output carries validity = CONDITIONAL(same_author) (renamed, see next line); its FP/TP figures show wiring, not that the rules separate sources on a real channel.
- Note 2026-11-09 (round 6): the label is now CONDITIONAL(circular_control); CONDITIONAL(same_author) is the old name for the same state, kept as `VALIDITY_OLD` in null_calibration.py.

## Four terms and null calibration (FINDER FOLLOW-UP, 2026-11-09)
Note 2026-11-09: added by FINDER FOLLOW-UP items A2 and C.

- **Terms.** All four chain terms from Cross-Domain-Toolkit `telemetry_vocabulary/terms.md` are cited, none re-coined:
  Telemetry refusal (:33), Interiority substitution (:49), Care inversion (:72), Unnamed universal (:88).
  Each ATTRIBUTION_DISPLACEMENT hit carries `terms` = its stage term plus "Unnamed universal". The second is this
  tool's reading (the unmarked default that a break starts in the user), not a detection. A new flag,
  TELEMETRY_REFUSAL, fires when a user condition ping is answered with ontological status and no condition word.
  Word lists; a paraphrase steps around them. Checks: `python3 cutoff-attribution/selftest_terms.py`.
- **Null calibration.** `null_calibration.py` wraps the tool as f(data) -> verdict (single separated source or NONE)
  and runs it through `null-harness` (imported; needs numpy). Controls plant one known source per candidate, plus an
  UNRESOLVED control, unchecked-hop rows, a two-source sensor collision and one measurement-only row the gating rule
  is expected to miss. Output: confusion matrix, forced-attribution rate, per-candidate FP/TP.
  ILLUSTRATIVE: the planted events are exactly what the rules accept, so the diagonal is close to true by
  construction. Sample: `samples/null_calibration.sample.txt`. Checks: `python3 cutoff-attribution/selftest_null.py`.

## Tested (append-only; never overwrite an older line)
tested: 2026-11-09 | model: WITHHELD (session rule: no model identifier is written into a pushed artifact; the operator holds it) | Claude Code, cloud session (claude.ai/code) | selftest.py 25/25, selftest_terms.py 11/11, selftest_null.py 10/10
tested: 2026-11-09 | commit 98ecd8f | Claude Code, cloud session (claude.ai/code) | model: see trailer | selftest.py 25/25, selftest_terms.py 11/11, selftest_null.py 11/11, selftest_radio.py 7/7

## Unflagged measurements and radio_log (FINDER ROUND 3, 2026-11-09)
Note 2026-11-09: added by FINDER ROUND 3 item 3.

- **Before:** the "network lag, unflagged" case (an rtt_ms spike with no flag) output status UNRESOLVED,
  candidate set `UNRESOLVED` only, and listed NETWORK_LAG under evidence as LOGGED_UNFLAGGED.
- **Now:** status still UNRESOLVED, candidate set `NETWORK_LAG, UNRESOLVED`. An unflagged measurement keeps its
  candidate in the set of an unseparated cut and never raises the status. The selftest pin moved on purpose.
  In `null_calibration.py` the measurement-only row is still a miss (verdict NONE), and the planted source is now
  retained in the candidate set on every one of those draws.
- **Optional `radio_log` input:** a list of `{"t": seconds, "dbm": number, "network": "wifi" | "lte" | "5g" | ...}`.
  - Each dBm row becomes an unflagged `rssi_dbm` measurement on the transmission hop (NETWORK_LAG). No dBm
    threshold is applied; a row may carry `"flag": true`.
  - A change of `network` between consecutive rows becomes a `network_handover` event, read through the
    transmission hop like any other event.
  - An entry with no `t` is refused. Schema text: `RADIO_SCHEMA` in the module.
  - Checks: `python3 cutoff-attribution/selftest_radio.py`.
