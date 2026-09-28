# quiet-failure

WO-2, delivered verbatim as `WORK_ORDER.md` (sha256
`89b70674ea89c65371dd27a95d79f14ccbf04a7a992eabd84af9c1400c46dfae`), and
built as an instrument to its four runnable next steps. The measurand, in
the order's own words:

```
Whether failures described afterwards as sudden or quiet were in fact
signalled, reported, and left unjoined — and whether the aggregation step
was unowned by construction rather than neglected.
```

The order is an instrument, not an argument, by its own first line, and
its scope limits are kept: case selection is illustrative and not a
sample, no base rate is claimed, and no claim is made that any
organisation neglected a duty. Stdlib only, parses under 3.9,
phone-buildable, CC0. No network module anywhere; nothing imported from
outside this folder.

## Contamination, declared before any number

`run_all.py` prints this first; repeated here so a reader meets it before
any table.

| axis | declaration |
|---|---|
| authorship | every file is model-authored in one session by the hand that wrote the checks AND the fixtures they are pinned to |
| position | the order places agentic AI infrastructure "at the pre-Tacoma stage: designed to calculated load, no accumulated margin"; the author is an instance of that class. The sentence is carried, not scored; the interest runs toward accepting it (a claim that one's own class lacks margin is the humble reading), so it is left unresolved rather than resolved either way |
| coding | the four codings of the order's cases are this session's reading of the order's own sentences, each code carrying the span it rests on; every one declares `saw_decomposition: True` and is refused by step 2's gate |
| parties | no claim that any organisation neglected a duty; authored files carry the order's case (event) names as lookup keys and no company or site name, which are parsed out of `WORK_ORDER.md` at call time and asserted absent from every authored file |
| records | no accident corpus, journal or archive was read: four hosts answered 403 to CONNECT, measured and timestamped in `decomposition.EGRESS`, `github.com` the connecting control; every corpus, null record and regulator record is CONSTRUCTED and says so |
| evidence | the order's "(fetched, verified)" is the order's verification; here every finding and number is `CARRIED_NOT_VERIFIED`, extracted as written with a span |
| rate | no base rate is computed anywhere and `base_rate()` refuses one (AST-asserted: it divides nothing) |

## The four steps

| step | file | input | what it returns |
|---|---|---|---|
| 1 corpus coding | `decomposition.py` | case records as JSON (`--corpus`), default the order's four cases coded from its text | per case `SIGNALLED_UNJOINED` / `SIGNALLED_JOINED` / `GENUINELY_UNSIGNALLED` / `REPORTED_NOWHERE` / `NOT_EVALUABLE` / `MALFORMED`; holder count and lead time declared or `UNDECLARED`; `separation()` within the corpus; `base_rate()` refused |
| evidence | `evidence.py` | `WORK_ORDER.md` | the three findings carried with numbers as written; the order's flat reading split into the clause the bullets state and the clause they do not |
| 3 inverse case, 4 regulator role | `ownability.py` | null records and role records as dicts | a null `BOUNDED` / `UNBOUNDED(lacks)`; a role `EXISTENCE_PROOF` / `ROLE_NOT_THE_JOIN` / `ROLE_WITHOUT_AUTHORITY` / `UNDECLARED`; the open question derived as `NEVER_ASSIGNED` or `UNDETERMINED`, never picked |
| 2 blind coding | `blind_coding.py` | coding pairs | admission by the one rule the step turns on; agreement per field, no composite; NOT RUN here |

```
python3 quiet-failure/run_all.py                  # declaration, then all four parts
python3 quiet-failure/selftest.py                 # the null-tested suite; prints its own count
python3 quiet-failure/decomposition.py --corpus cases.json
```

Every library module refuses `--selftest` (exit 2) and names the suite.

## Step 1 — the decomposition as a coder

```
signal_present   PRESENT | ABSENT (searched) | UNSEARCHED      missing field -> UNSEARCHED, never ABSENT
signal_reported  PRESENT | ABSENT | UNSEARCHED
join_assigned    ASSIGNED | UNASSIGNED | UNSEARCHED
holder_count     int | UNDECLARED          time_first_signal_to_event  {value, unit} | UNDECLARED
described_as     SUDDEN | QUIET | NEITHER | UNDECLARED

classify:  present? -no-> GENUINELY_UNSIGNALLED        (the contrast class step 1 wants)
           reported? -no-> REPORTED_NOWHERE              (part 1 does not hold)
           join assigned? -yes-> SIGNALLED_JOINED         (counter-case to part 3)
                          -no--> SIGNALLED_UNJOINED       (the decomposition's instance)
           any of the three UNSEARCHED -> NOT_EVALUABLE naming it

separation(corpus): described axis x signal axis, WITHIN a failure corpus
   one signal level -> NOT_EVALUABLE  (a corpus with nothing unsignalled cannot separate)
base_rate(corpus):  REFUSED_SAMPLING_FRAME -- selected on the outcome, no denominator over systems
```

The order's own four cases, coded from its sentences with the span each
code rests on:

```
SILVER BRIDGE        -> REPORTED_NOWHERE      'not inspectable without disassembly'
COLUMBIA             -> SIGNALLED_UNJOINED    'Imaging requests made and denied through proper channels'
TACOMA NARROWS       -> NOT_EVALUABLE         the text states no signal field
QUIET FAILURE CLASS  -> NOT_EVALUABLE         'inspectable in principle', reporting unstated
separation on the four: NOT_EVALUABLE (one signal level)
```

Two things the coding shows about the order's own material. The anchor
case, by the order's own sentence, is one where the signal existed and
reached no channel — part 1 of the decomposition does not hold on it, so
the case the order opens with is the contrast class its step 1 wants and
not an instance of the structure. And the one case that does instance
the structure rests, for `join_assigned`, on a reading: the order says
the imaging requests were *denied through proper channels*, which is
someone deciding, and whether that someone held the join is exactly the
field a blind coder is for. Both are readings of the order's text and
are declared as such; neither is a statement about either event.

## Evidence — what the bullets state and what the flat reading adds

```
finding 1          one number as written    states record absent: yes
finding 2          no number                 states record absent: yes
finding 3          no number                 states record absent: no
(names and the number are parsed from the order at call time; the render prints them)
flat reading  clause 1 "the reasoning was not recorded"   stated by 2 of 3
              clause 2 "no cost comparison was made"      stated by 0 of 3
```

A bullet reporting *no documented information* supports the first clause
and not by itself the second, which is a statement about what happened
off the record. The order's own next sentence about safety-economics
(costs traceable only at a cost to trace them) is the reason the second
clause is hard to establish either way, and it is carried beside it.

## Steps 3 and 4 — the null, the role, the open question

```
order's null: "Not found in two searches"   corpus? no  terms? no  date? no  hits? no
   -> UNBOUNDED lacks [corpus, terms, searched_on, hits]   carried, entering no count
bounded null  = corpus + terms + date + hits      hits 0 -> NULL_IN_STATED_CORPUS
                                                  hits absent -> UNBOUNDED  (zero is not absent)
role record   = regulator + role_name + authority + holds_the_join
   holds the join with authority     -> EXISTENCE_PROOF       (the order's ownability proof)
   holds the inspection or report    -> ROLE_NOT_THE_JOIN
   holds the join, authority ABSENT  -> ROLE_WITHOUT_AUTHORITY
open question:  any EXISTENCE_PROOF -> NEVER_ASSIGNED   otherwise UNDETERMINED
                UNOWNABLE is returned by no path: absence of a proof is not a proof of absence
```

The order asks that a null be reported rather than dropped. A null is
reportable when it is bounded, and the order's own is not — it names how
many searches and nothing they were of. From here it cannot be bounded
either, so step 3 is `NOT_MEASURED` and step 4 reads zero records; the
open question stays `UNDETERMINED` and the order's current read is
carried beside it as the order's.

## Step 2 — not run, and the gate that says why

Every coding in this folder declares that its coder saw the
decomposition, and the admission gate refuses each one by that field.
Agreement between two admitted codings is per field — `AGREE` /
`DISAGREE` / `UNSEARCHED_ON_ONE_SIDE` — and never one number, since the
fields are vocabularies of different kinds.

## Choices

| id | where | what |
|---|---|---|
| CHOICE 1 | `decomposition.separation` | SEPARATES iff every case described SUDDEN classifies SIGNALLED (strict; a single unsignalled SUDDEN case reads DOES_NOT_SEPARATE) |

## Found by running, not by reading

- The anchor case's `described_as` was first coded `SUDDEN` on the phrase
  *in under a minute*, which is the duration of the collapse and not how
  it was described afterwards; recoded `UNDECLARED` with the phrase kept
  as `event_duration`.
- The suite's check that no authored module carries a number from the
  evidence section wrote that number as a literal in the check and fired
  on itself; the check now reads the number through its span.
- The adjacent-sentence parser stopped at a line break inside the order's
  own sentence and returned `UNPARSED` on a sentence that is there.
