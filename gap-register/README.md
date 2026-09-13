# gap-register

A register of marked, unmeasured quantities, built to `WORK_ORDER.md`,
which is delivered verbatim and edited by nothing here. One entry is one
`(quantity, excluding-method)` pair. The measurand is the **presence of a
mark**, not the truth of any claim about the quantity marked.

```
python3 gap_register.py validate            # the shipped register, exit 0
python3 gap_register.py validate demo/fails.jsonl   # exit 1, on purpose
python3 gap_register.py search analgesia
python3 gap_register.py check GR-0003
python3 gap_register.py export --md
python3 selftest_gr.py                      # prints its own check count
```

`gap_register.py` is the instrument and refuses `--selftest`; the checks
live in `selftest_gr.py`.

## What is here

| file | |
|---|---|
| `WORK_ORDER.md` | delivered verbatim |
| `gap_register.py` | the tool: `add`, `validate`, `search`, `check`, `export --md` |
| `REGISTER.jsonl` | the seven seed entries, one object per line |
| `demo/fails.jsonl` | two constructed entries that do not validate |
| `CLAIM_TABLE.md` | `GRG_001..GRG_014` -- findings about the instrument |
| `samples/` | one render per subcommand, as run |

## The state of the register

All seven entries are `UNKNOWN`, not `OPEN`. Nobody ran a venue check:
every publisher, registry and standards host refuses CONNECT from this
environment, and section 1 says an entry that cannot be evaluated returns
`UNKNOWN` and never `OPEN` by default. The operator holds the session
record that raised these and is the party who can set them (`GRG_003`).

Nothing in the register is verified against a published document. The
register names no standards body, certification or publication the order
does not name, and the selftest checks that mechanically (`GRG_011`).

## V5 returns UNDETERMINED on every entry

The order's V5 refuses an index term that is *"a coinage absent from
index_terms of any other entry"* and defines no test for **coinage**. Two
readings are available and they part on all seven entries: STRICT refuses
7 of 7, LOOSE admits 7 of 7. The checker scores both and returns
`UNDETERMINED` naming the terms rather than picking (`GRG_001`,
`GRG_002`). Every other check returns `PASS`.

`UNDETERMINED` exits zero and prints loudly. That is `[CHOICE 5]`, stated
at the foot of every render.

## What the demo is for

Section 8: a demo that only passes proves nothing. `demo/fails.jsonl`
carries two constructed entries, one tripping V4 and one tripping V2,
each passing the other five rules so the refusal is attributable. The
selftest asserts the nonzero exit **and** that the refused set is exactly
`{(GX-0001, V4), (GX-0002, V2)}` -- a bare exit-code check would pass on
a demo that failed for some other reason.

## What is open

Section 9's three items need operator sign-off and are decided by nobody
here: four types or three, status per entry or per reader, bare JSONL or
a dialect. Each is asserted in the selftest in the state the order left
it, so a later build cannot settle one quietly (`GRG_010`).

The kill rule -- a zero-context model restating quantity and closure
condition from the store alone -- is not runnable here and is `UNVERIFIED`
(`GRG_009`). The name-strip probe the order names as the measurement arm
for the citation confound is named and not built (`GRG_012`).

CC0. Standard library only. Parses under Python 3.9. Phone-buildable.
