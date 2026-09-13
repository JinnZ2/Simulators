# WORK ORDER — valence_divergence.py

CC0. Stdlib only. No network. No lexicon. Phone-buildable.

## What it does

Logs a term used by two parties, records the valence each party's decoder
assigns, records where each reading came from, and flags divergence.

It does NOT determine valence. It has no dictionary and no model of what
words mean. Both readings are supplied. The instrument's only job is to
detect that two decoders disagree and to preserve which is which.

This is the reason it is buildable at all. A valence dictionary would be one
decoder claiming to be the answer.

## Why divergence and not valence

Valence is a property of the decoder, not of the word. The same token can
carry anatomy, pathology and delight simultaneously, with different branches
live for different readers. An instrument that assigns one valence has
collapsed the branches and reports the collapse as a finding.

The scored failure is not disagreement. Disagreement is visible and gets
handled. The scored failure is AGREEMENT REACHED OVER AN UNFLAGGED MISMATCH —
both parties proceed, neither marks the term, and the divergence never
surfaces.

## Where decoder B comes from

The word's own history. Not a second living community — the record against
the word: etymology, historical usage, the mechanism the word carried when it
entered use, other cultures' use of the same root.

This is a WORKFLOW, not an algorithm. The instrument stores the result of the
lookup and its source. It does not perform the lookup and must not pretend to.

## Intake — structured only

```
entry = {
  "term": str,
  "utterance_id": str,          # where in the exchange
  "speaker": str,               # opaque label, not a role or rank

  "reading_A": {
     "valence": "POS" | "NEG" | "NEUTRAL" | "MIXED" | "UNREAD",
     "source": "DEFAULT" | "STATED" | "CONTEXT",
     "gloss": str               # free text, carried, never parsed
  },

  "reading_B": {
     "valence": "POS" | "NEG" | "NEUTRAL" | "MIXED" | "UNREAD",
     "source": "ETYMOLOGY" | "HISTORICAL_USE" | "OTHER_CULTURE"
             | "STATED" | "ABSENT",
     "citation": str,           # required unless source == "STATED"/"ABSENT"
     "date_or_period": str,     # required unless source == "STATED"/"ABSENT"
     "gloss": str
  },

  "flagged_by": "A" | "B" | "BOTH" | "NEITHER",
       # did either party mark the term as possibly carrying a different
       # reading, at the time of use

  "proceeded": bool
       # did the exchange continue past this term without resolution
}
```

`UNREAD` is a valid and important value. It means the decoder assigned no
valence, which is itself a reading and must not be recorded as NEUTRAL.
NEUTRAL means read and found flat. UNREAD means not read.

`ABSENT` for reading_B source means the history was not looked up. The entry
is still logged. An unchecked term is data.

## Checks

```
D1_DIVERGENT      reading_A.valence != reading_B.valence,
                  neither being UNREAD or ABSENT

D2_UNFLAGGED      D1 fired AND flagged_by == "NEITHER"

D3_SILENT_PASS    D2 fired AND proceeded == True
                  # the scored failure case

D4_UNCHECKED      reading_B.source == "ABSENT"
                  # not a failure; a queue entry

D5_ORPHAN_CANDIDATE
                  reading_B.source in {"ETYMOLOGY","HISTORICAL_USE"}
                  AND reading_B.valence in {"NEUTRAL","UNREAD"}
                  AND reading_A.valence in {"POS","NEG"}
                  # valence present now, absent at origin — feeds the
                  # orphaned-valence study
```

## Return

```
{
  "term": str,
  "utterance_id": str,
  "fired": [list of check codes],
  "reading_A": {...},          # returned intact
  "reading_B": {...},          # returned intact
  "decoder_attribution": "A" | "B" | "SPLIT"
}
```

`decoder_attribution` names which decoder produced the valence when only one
did. This field is the point of the instrument. A divergence report that does
not say whose reading is whose has thrown away the finding.

No field ranks the decoders. Neither is the correct one.

## Validation cases

**A — hysteria.** reading_A: NEG, DEFAULT. reading_B: NEUTRAL, ETYMOLOGY,
Greek hystera = womb, PIE root for abdomen; valence enters c.1610s as a
claimed mechanism; a positive branch ("very funny") live from 1939.
→ MUST fire D1 and D5. Note that reading_B here is properly MIXED once the
1939 branch is entered; log both branches as separate entries rather than
averaging them. Averaging branches is the failure this instrument exists to
prevent.

**B — the location set.** savage, pagan, feral, superstition.
reading_A: NEG, DEFAULT. reading_B: NEUTRAL, ETYMOLOGY — of the woods, rural,
wild animal, and an adjective meaning both pious and superstitious.
→ MUST fire D1 and D5 on each. Four entries, not one; the instrument logs
terms, and the observation that they share a shape is made by the reader.

**C — economy.** reading_A: NEUTRAL or POS, DEFAULT. reading_B: NEUTRAL,
ETYMOLOGY, oikonomia = household management.
→ MUST fire D1 only if the valences differ. If both read NEUTRAL, D1 does NOT
fire and the entry logs clean.
This is the required negative case. Economy's defect is scope collapse — the
referent shrank while the name and authority stayed — and this instrument
cannot see it. It must not fire on it. An instrument that flags every term
is a preference dressed as a method.

**D — FALSIFIER, silent pass.** A term where A reads NEG, B reads POS,
flagged_by NEITHER, proceeded True.
→ MUST fire D1, D2 and D3. If D3 does not fire, the instrument cannot detect
the only failure mode it was built for.

**E — no false symmetry.** reading_B.source == "ABSENT" with a strong
reading_A.
→ MUST fire D4 ONLY. Must NOT fire D1. An unchecked history is not a
divergence, and the instrument must not manufacture one from absence.

## Hard constraints

- No lexicon, no valence model, no sentiment scoring, no inference of
  valence from any text. Both readings are supplied or the entry is
  incomplete.
- No field for intent, motive, or what either party meant. The instrument
  records what a decoder returned, not why anyone said anything.
- Glosses and citations are carried verbatim and never parsed.
- No field ranking decoder A above decoder B or the reverse.
- Branches are logged separately. Never average, never resolve to a single
  valence, never pick a dominant sense.

## Open

- Reading_A currently requires someone to state the default reading. Self-
  reporting a default is exactly the thing that fails elsewhere in this
  ecosystem. Unresolved. Provisional handling: log reading_A only when it has
  been demonstrated in use — an actual utterance in the exchange — rather
  than introspected on request.
