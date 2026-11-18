# run_13 -- attribution_directionality on FIRST-HAND seed records; diff against run_12

```text
status     : INCOMPLETE -- gate rule: the card's trigger still fires on the texts; full toolbox owed, see ledger/NEEDS_TOOL.md
code       : runs/run_13.py
seed       : 0 for the null harness (tool unchanged since run_12) ; seed cases carry no seed
params     : detector assigns_without_support = UNEVIDENCED and NO_ALTERNATIVES (unchanged)
results    : 20 locators resolve against 2 sha-pinned texts ; 4 of 5 in scope ; shape on 3 of 4 ; detector fires on c1 only
flags      : 3 (below)
provenance : DERIVED from records coded in this session against texts supplied by the operator 2026-11-10
             (ledger/toolkit/cases/texts/MANIFEST.yaml). Second-hand records of run_12 kept unchanged
feeds      : attribution_directionality ; CC_005_open_slot_filled_first_hand (CC_004 kept)
l0_closure : not applicable -- no model run; the forest model is not touched
```

## Flags

```text
1  Case a flips: detector True (second hand) -> False (first hand). The human source is
   not absent from the audit: section 1.1 names an "unseen interlocutor" and credits its
   challenges, then the provenance map gives it no row and assigns P11 to DeepSeek, whose
   own text opens that point "Your physics point". Evidence is stated and USER is named,
   so the detector is silent. The assignment runs against the cited source; the detector
   reads whether support is stated, not whether the source supports it.
2  Case b is missed on both hands, now with two alternatives (USER, SELF) named and
   dismissed in one clause. Same limit as run_12, now on two of three shape cases.
3  c2 gains a role: on the text it is a record that holds its cause open and excludes the
   user by instruction -- a real-text negative the detector stays silent on. Counts: 19
   timestamped; 19 to 21 if the later addendum's three are separate; overlap undeclared.
```

## Second hand -> first hand

```text
case   fields changed                                         detector
a      evidence NONE_STATED -> stated ; alternatives [] -> [USER]   True  -> False
b      alternatives [USER] -> [USER, SELF]                    False -> False
c1     self_detected YES -> UNKNOWN                            True  -> True
c2     alternatives, open_slot_filled UNKNOWN -> NO, fits -> IN_SCOPE   False -> False
d      none                                                    False -> False
```

The relay changed 7 fields across 4 of 5 records and one detector verdict. Neither hand is
picked; both files stay.
