# reasoning-toolkit cards

CC0. Co-authored. Markdown only.

Design basis: the card format and the provenance density were requested by the user
(operator, 2026-11-13).

## Card format

Each card has six fields:

- `measures`: what the card reads.
- `fits`: where it applies.
- `method`: how to use it.
- `breaks`: when it breaks.
- `warning`: the sign that it is breaking.
- `link`: links to other cards, folders or sources.

Each card carries a status line:

- PROPOSED means no worked instance is in this repository.
- OBSERVED means this repository holds a worked case the card was applied to. An `instance` line names that case.

A reference with no file in this repository is written as plain text and marked "(chat-side, not in repo)" or "not located in this repository". It is not linked.

Provenance is per card:

- "drafted chat-side, landed verbatim" means the operator delivered the text and only the formatting was tidied.
- "drafted in Claude Code, 2026-11-13" means the text was written in the session that landed it.

## Contents

1. distribution check — when to distrust the median
2. fill-source tag — said vs filled
3. claim-vs-method
4. channel-loss map
5. frame check
6. label-tracks-valve
7. symptom vs cause feeds
8. parallax by rotation
9. entangled variable
10. author familiarity
11. carrier spread

---

## 1. distribution check

provenance: drafted chat-side, landed verbatim
status: PROPOSED

```
CARD: distribution check — when to distrust the median
  measures   whether a central value represents the population at all
  fits       any "average X", "typical Y", "most people", model defaults
             (a model's default answer IS a median)
  method     ask for the shape before the center:
               modes? (several peaks → no single typical)
               tails? (who's out there, how far, how many)
               spread vs center (wide spread → the median is a coin flip)
             then: is the case in hand central, a tail, or another mode?
  breaks     n too small to show shape → mark the shape VOID, not "normal"
             the measure itself blinds the tails (sensor floor or ceiling)
  warning    advice fitted to the middle and handed to a tail case
             ("most drivers can just…") with no check of where the asker sits
  link       reasoning-root (tail vs corpus median); BLS basket vs truck-stop
             prices (the index = the median shopper)
```

link notes:
- reasoning-root (chat-side, not in repo)
- "BLS basket vs truck-stop prices" was not located as a pair in this repository.
- Related folders: `tail-check/`, `moving-mean-tracker/`, `evaluation-frame/`.

---

## 2. fill-source tag

provenance: drafted chat-side, landed verbatim
status: PROPOSED

```
CARD: fill-source tag — said vs filled
  measures   which parts of an output came from the input vs from defaults
  fits       summaries, records, memory files, schemas, model answers about a person
  method     tag every slot: SAID (in source) | DERIVED (stated step) |
             FILLED (default/median) | VOID
             a FILLED slot never silently becomes SAID downstream
  breaks     the source is itself an earlier fill (laundered default)
             → trace to the first appearance (missing-wand protocol)
  warning    a confident specific with no source line; "silent fills"
             (missing input → passing value; TAF ranks 1, 2, 3, 6)
  link       TAF silent-fill experiment; VOID-not-dropped rule
```

link notes:
- missing-wand protocol (chat-side, not in repo)
- The TAF silent-fill experiment is cited in `COLLISIONS.md`. It lives in the
  thermodynamic-accountability-framework repository, which was not checked from this session.
- The VOID-not-dropped rule is stated in `warnings-label-inversion/warnings_branch_table.py`,
  line 8: "VOID = no information (slot kept, not dropped)".
- Related: `tail-check/`, `tools/sourced.py`.

---

## 3. claim-vs-method

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: claim-vs-method -- when a claim outruns its method
  measures   the gap between what a study says and what its design could have shown
  fits       abstracts, press summaries, "research shows", a model answer citing a study
  method     set the claim beside the method; three checks:
               n: how many units; does the claim speak for more than they cover
               measured vs modeled: was the quantity observed, or produced by a model run
               sufficiency vs necessity: "X can produce Y" read as "Y needs X", or the reverse
             then: restate the claim at the width the method supports
  breaks     the method section is not available -> mark the gap VOID, not "fine"
             the claim states no scope, so there is nothing to set it against
  warning    a population-wide verb ("people", "always", "causes") resting on
             one sample, one site or one simulation
  link       scope-finding practice; claim-audits/, scope-bound-shapes/,
             measurand-partition/
```

link notes:
- The scope-finding practice is named as a source line in
  `notes/queue/DISPATCH_M0_SCOPE_2026_10_04.md` and in
  `publication-loop-work-orders/WORK_ORDER_14.md`.

---

## 4. channel-loss map

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: channel-loss map -- what each channel drops
  measures   which parts of a signal do not survive each hop between source and reader
  fits       transcripts, summaries, voice sessions, notes from a call, reports passed up a chain
  method     list the hops in order; for each, name what that channel cannot carry:
               transcription drops environment (setting, sound, who else was there)
               prose drops parallelism (things at once become a sequence)
               voice drops layout (tables, indentation, side by side)
               a summary drops branches (alternatives not taken)
             the reader receives the product of every hop; per-hop loss compounds
  breaks     a hop is invisible (nobody recorded that a summary was made)
             -> the map stays open at that hop, marked VOID
  warning    a reading treated as the source when it came through two or more hops;
             an element missing from the reading taken as missing from the source
  link       reporting-chain-loss/, cutoff-attribution/, encoding-selection/,
             tools/channel_chain.py
```

---

## 5. frame check

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: frame check -- which frame a term is working in
  measures   whether a key term keeps one sense through an argument
  fits       arguments that join two fields; a word with a technical and an everyday sense
  method     for the key term, write its sense at each use:
               which field, which measure, which population
             mark the first place the sense changes
             ask whether the conclusion rests on the later sense while the
             evidence was gathered under the earlier one
  breaks     the term is never pinned at any use -> mark VOID
             both senses are used on purpose and declared
  warning    confidence earned under one sense carried to a claim in the other
             without a marked step
  link       uninstrumented/cases/021sensesubstitutionundeclaredaxis.md
             (sense substitution); uninstrumented/cases/016agreementasmode.md
             (agreement as mode)
```

---

## 6. label-tracks-valve

provenance: drafted in Claude Code, 2026-11-13
status: OBSERVED
instance: `SPECIMENS` in `warnings-label-inversion/label_inversion_test.py`, both tagged OBSERVED in that file.
- Midas: the warning became "'Midas touch' = praise for making money".
- usury → interest.

The vignette and corpus arms are built and have not been run on real data.

```
CARD: label-tracks-valve -- does the label follow the payment, not the act
  measures   whether the label on a fixed act moves when only payment moves
  fits       pairs of words for one act (begging / outreach, overwork / dedication)
  method     hold the act and its harm text fixed; vary paid / unpaid;
             vary pays apart from succeeds; record the label chosen; compare
  breaks     payment is part of the act itself (see entangled variable)
             the reader can see what is being varied and answers to it
  warning    an act renamed once money attaches, with the harm text unchanged
  link       warnings-label-inversion/label_inversion_test.py,
             warnings-label-inversion/model_corpus_arm.py
```

---

## 7. symptom vs cause feeds

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: symptom vs cause feeds -- two feeds report two layers
  measures   whether a crowd symptom feed and an operator status feed show the same
             event at the same time
  fits       outage trackers vs vendor status pages; complaint counts vs incident records
  method     put both feeds on one clock; mark when each first shows the event;
             name what each counts (user symptom reports vs the operator's declared cause)
             a gap in time or content is a reading, not a contradiction
  breaks     the crowd feed counts reports, not users, and rises with attention
             the status feed is written by the party whose incident it is
  warning    "no incident" on a status page read as "nothing wrong"
             while symptom reports rise
  link       specimen: crowd outage trackers vs status pages, Microsoft 365, 2026-11-12;
             return-path/, reporting-chain-loss/
```

link notes:
- specimen: crowd outage trackers vs status pages, Microsoft 365, 2026-11-12
  (chat-side, not in repo)

---

## 8. parallax by rotation

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED

```
CARD: parallax by rotation -- move the vantage, see what each omits
  measures   which items appear from one vantage and not from another
  fits       coverage of one event across outlets; accounts from several roles
  method     rotate through vantage points (outlets, regions, roles) on the same event;
             list items present in some and absent in others; the absences are the reading
  breaks     the vantages share one upstream source (one wire, one release)
             -> rotation shows no parallax
  warning    one vantage taken as the whole event; an omission read as
             nothing having happened
  link       specimen: rotating news vantage; observer-exclusion/, divergence-playground/
```

link notes:
- specimen: rotating news vantage exposes omissions (chat-side, not in repo)

---

## 9. entangled variable

provenance: drafted in Claude Code, 2026-11-13
status: OBSERVED
instance: in `warnings-label-inversion/label_inversion_test.py`, `LABEL_PAIRS` "lending at interest" carries `pay_entangled=True`.
- `build_vignettes` skips it in arm A.
- `corpus_counts` reports it in its own `entangled` block.

```
CARD: entangled variable -- when a factor cannot vary on its own
  measures   whether a factor can be varied without changing the act it modifies
  fits       factorial designs, A/B tests, "holding everything else fixed"
  method     for each factor, try to write the cell where it is off and the act is unchanged
             if the cell cannot be written, the factor is inside the act:
             drop it from that arm and read it where it can be read (observational)
  breaks     the entanglement is partial (only some instances carry it)
  warning    a design cell that describes an impossible case
             ("lending at interest, unpaid")
  link       warnings-label-inversion/label_inversion_test.py (pay_entangled)
```

---

## 10. author familiarity

provenance: drafted in Claude Code, 2026-11-13
status: PROPOSED
specimen: `warnings-label-inversion/model_corpus_arm.py` (`paraphrase_author`, `--add-paraphrases`).
The split per author is built and has been run on constructed answers only.

```
CARD: author familiarity -- whose words the prompt is in
  measures   whether results move with who wrote the prompt text
  fits       prompt packs, survey items, paraphrase sets; a model reading text
             written by its own family
  method     tag every item with its author; add items from another author;
             report the result per author beside the pooled result
  breaks     one author for every item -> the split is empty
             authors differ in more than authorship (length, register)
  warning    a pooled result that holds for one author's items and not another's
  link       warnings-label-inversion/model_corpus_arm.py
```

---

## 11. carrier spread

provenance: drafted in Claude Code, 2026-11-13
status: OBSERVED
instance: `warnings-label-inversion/warnings_branch_table.py`.
- `WARNINGS` is organised by carrier (`carriers[]`), not by canonical entry.
- The Wendigo row keeps its carriers slot VOID by design.
- The outside (horror genre) read sits in its own row.

```
CARD: carrier spread -- a warning held by many carriers
  measures   how many carriers hold a piece of knowledge, and what each kept
  fits       rules, practices and stories held by several traditions, institutions or texts
  method     one row per carrier, not per canonical entry; per carrier record the variant,
             whether the word is alive, whether practice continues, whether it still blocks;
             keep variants side by side
             a carrier that withholds content stays as a slot (VOID), not dropped
  breaks     the carriers copy one source -> the spread is nominal
  warning    variants collapsed into one canonical entry; an outside version
             standing in for the carriers' own
  link       warnings-label-inversion/warnings_branch_table.py (carriers[], Wendigo row)
```
