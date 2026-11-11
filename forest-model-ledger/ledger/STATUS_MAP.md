# STATUS_MAP -- what you may do from each status

Requested 2026-11-10 (chat side, Kavik's call: keep the axes split). The two
axes and their seven statuses are the author's. The moves, forbidden moves and
exits below were drafted by the building session and are PROPOSED until Kavik
edits or accepts them.

```text
RUN status   = did the loop finish?        COMPLETE | INCOMPLETE | REPORTED
CARD status  = how far to trust the read?  OPEN | PROVISIONAL | RESOLVED | CURIOSITY
```

The axes never merge. PROVISIONAL is a card status only; a run is never
PROVISIONAL. Find your status, pick your goal, take that move.

`python3 tools/check_ledger.py` fails if a run or card carries a status with
no entry here, if an entry lacks a field, or if the pair table misses a pair.

---

## RUN axis

### RUN COMPLETE
- means: the loop finished; every trigger that fired was answered with a tool that exists, and the run's code is in the tree.
- goal trust it: check the run's hash and budget verdicts still reproduce, then use its numbers as DERIVED.
- goal explore: branch from it, one component changed; label the branch "built on COMPLETE run <id>".
- goal report now: report the numbers with their budget verdicts. Label: "run COMPLETE; anchor status <candidate|anchor>".
- forbidden: reading COMPLETE as "anchor". Reading a VOID budget as closed. Editing the run's pinned code.
- exits to: INCOMPLETE when a new trigger fires on it and the tool is missing, or when a row for it is added to NEEDS_TOOL.md.

### RUN INCOMPLETE
- means: a toolbox trigger fired and at least one needed tool does not exist; the run is not resolved.
- goal trust it: not available. Build the tools named in NEEDS_TOOL.md and re-run them on this run first.
- goal explore: allowed; label everything built on it "built on INCOMPLETE ground (<run id>)", and do not tag it as an anchor.
- goal report now: first line "TOOL NEEDED: <names>". Label every number from it "from an INCOMPLETE run".
- forbidden: marking it COMPLETE while NEEDS_TOOL.md still owes it a tool. Explaining the trigger away without the tool. Building on it without the label.
- exits to: COMPLETE when every tool owed in NEEDS_TOOL.md is built and has been run on it (the tool's used_in lists the run).

### RUN REPORTED
- means: carried from a report; code, seed and parameters are void, so nothing here was recomputed.
- goal trust it: not available as it stands. Rebuild the run as a new run_N with code in the tree; trust that one.
- goal explore: use it as a pointer to what to rebuild; label anything built on it "built on REPORTED ground (<run id>), not recomputed".
- goal report now: quote it as reported. Label: "REPORTED, not recomputed".
- forbidden: citing its numbers as DERIVED. Filling its void fields from memory. Using it for an anchor test.
- exits to: none; it stays REPORTED. A rebuild is a new run with its own status.

---

## CARD axis

### CARD OPEN
- means: at least one of the five cause slots has not been looked at.
- goal trust it: not available. Fill the unrun slots, each with evidence from a run.
- goal explore: pick an unrun slot and design the run that fills it; label work "built on OPEN ground (<card id>)".
- goal report now: list the supported slots and the unrun slots. Label: "card OPEN; unrun: <slots>".
- forbidden: naming a cause as the answer. Reading supported slots as the full list of causes. Marking a slot ruled_out with no evidence.
- exits to: RESOLVED when all five are looked at and at least one is supported; PROVISIONAL when that holds and recheck_when names tools still in build; CURIOSITY when all five are ruled out.

### CARD PROVISIONAL
- means: the evidence would read RESOLVED, but the tools that should have produced it are still in build.
- goal trust it: not yet. Build the tools in recheck_when, re-check the card with them, then clear recheck_when.
- goal explore: allowed; label work "built on PROVISIONAL ground (<card id>)".
- goal report now: give the supported causes and the tools awaited. Label: "PROVISIONAL; re-check when <tools> exist".
- forbidden: treating PROVISIONAL as RESOLVED. Dropping the label when quoting it. Clearing recheck_when before the tools have been run on the card's runs.
- exits to: RESOLVED when the tools exist, the re-check agrees and recheck_when is cleared; OPEN when the re-check moves a slot back to void or contradicts the evidence.

### CARD RESOLVED
- means: all five cause slots were looked at and at least one is supported by evidence.
- goal trust it: check the cited runs are COMPLETE, then use the named causes.
- goal explore: test the supported causes against each other; label work "built on RESOLVED card <id>".
- goal report now: name the supported causes and the runs behind them. Label: "card RESOLVED on <runs>".
- forbidden: reading "evidence is present" as "evidence is right" (the tool checks presence only). Treating it as closed when a cited run is INCOMPLETE.
- exits to: PROVISIONAL when the evidence turns out to come from hand-written checks and the tools are named in recheck_when; OPEN when a slot's evidence is withdrawn.

### CARD CURIOSITY
- means: all five named causes are ruled out; the coincidence is unexplained and has its own branch.
- goal trust it: trust only the five rulings-out. There is no cause to trust.
- goal explore: work its branch; label work "built on CURIOSITY ground (<card id>)".
- goal report now: say that no named cause holds and name the branch. Label: "CURIOSITY, unexplained".
- forbidden: inventing a sixth cause to close it. Dropping the branch. Reading "unexplained" as "noise".
- exits to: OPEN when a ruling-out is withdrawn; RESOLVED when new evidence supports one of the five.

---

## Run x card pairs

A card lists the runs it rests on. Read the pair, not either status alone.

| run | card | read it as | in the tree now |
|---|---|---|---|
| COMPLETE | OPEN | the run stands; the coincidence on it is not explained yet | none |
| COMPLETE | PROVISIONAL | the run stands; the reading on it waits for tools | run_9 + CC_001 |
| COMPLETE | RESOLVED | usable: finished loop, causes named | none |
| COMPLETE | CURIOSITY | the run stands; the coincidence is unexplained, follow its branch | none |
| INCOMPLETE | OPEN | nothing to build on without labels; tools and slots both owed | run_11 + CC_003 ; run_12 + CC_004 ; run_13 + CC_005 |
| INCOMPLETE | PROVISIONAL | evidence stands, tools owed on both axes; label twice | run_10 + CC_001 |
| INCOMPLETE | RESOLVED | not a closed trigger; move the card to PROVISIONAL or build the tools | none |
| INCOMPLETE | CURIOSITY | unexplained and the tools were missing; build the tools before working the branch | none |
| REPORTED | OPEN | carried coincidence; no slot can be filled until the run is rebuilt | run_8 + CC_002 |
| REPORTED | PROVISIONAL | should not arise: a REPORTED run supplies no evidence to hold provisionally | none |
| REPORTED | RESOLVED | should not arise: evidence must come from a run with code in the tree | none |
| REPORTED | CURIOSITY | should not arise: rulings-out need recomputed evidence | none |

---

## Slot states and exits (added 2026-11-11, work order item 1)

A slot state is not a card status and is not a run status; it is a third
thing, one level below the card. `ABSENT_AT_SENSITIVITY(<value>)` is a
scoped absence: the cause was looked for at that sensitivity and not found.
It counts as ruled out for the card's reading, and the reading carries the
scope, so quoting a card that rests on one without its sensitivity is the
same violation as dropping the PROVISIONAL label. A bare "absent" is refused.

Every void slot, and every VOID / UNKNOWN / PROVISIONAL entry in
`ledger/expiry.yaml`, carries `expiry_condition`. Void there means no exit
defined: nothing named would move it. The checker prints the count and the
list and does not fail on it.
