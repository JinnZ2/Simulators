# automation-gap

Six documents landed verbatim: a measured-deployment audit of where
automation's dependency chain still runs through a person, a 16-record
harness run over automation demos, a per-input ledger for the one deployment
with a long third-party record, a field-evidence spec written after an
operator killed its first version, that spec's first live ledger, and -- one
drop later -- the road-wear seed that is WP1 and WP2, the two objects the
ledger reads its value against and `AGA_009` had recorded as absent.

```
AUTOMATION_GAP_AUDIT.md          10 domains, measured deployments only;
                                 forecasts and vendor claims quarantined
DEMO_CORPUS_AUDIT.md             16 records x 6 checks; curated corpus,
                                 declared as such
KOMATSU_AHS_INPUT_SCAFFOLD.md    per-truck-year input ledger + a v2 unmeld
                                 pass separating four melded variables
FIELD_LAYER_ZERO_BURDEN_SPEC.md  the worker never fills out a form
FIELD_LEDGER_001.md              seven entries, one discrepancy resolved by
                                 pixels, one mechanism corrected by the
                                 operator
FIELD_LAYER_SEED_ROADS.md        WP1 unpaved-vs-paved wear + WP2 the
                                 infrastructure bill autonomy asks for
audit.py                         recomputes what the documents state
test_audit.py                    checks on the audit; prints its count
CLAIM_TABLE.md                   AGA_001..019 with falsifiers
```

**Everything in the drop is CARRIED.** Every figure is sourced to reporting
this environment cannot reach -- the egress gate refuses every publisher
host. `audit.py` checks whether the documents agree with themselves and with
each other. It checks no claim about the world, and the suite asserts it
carries no function that would.

## What the recomputation found

```
distribution table       all six columns reconcile with the matrix, 16 each
6/6 records              exactly one, and F1 names it
F1 second sentence       REFUTED -- two humanoid records fail exactly two
Komatsu derived cells    6 of 6 agree at the precision the ledger prints
tire +40%                the TOP of the 6,000-7,000 vs 5,000 range it cites;
                         the midpoint gives 0.77, not 0.71
field ledger 2 of 6      denominator agrees with the headed entries
seed tire ratio          2.5x and 3.7x recompute from the cents-per-mile
                         figures printed in the same cell
seed, two rows           maintenance FREQUENCY ~4x against county
                         EXPENDITURE 140x -- 35x apart, different
                         quantities, neither adjudicated
seed provenance          INDUSTRY-STATED used on 7 rows and declared in no
                         header; it is the label WP2's argument turns on
seed cross-cites         Komatsu V2.1 resolves; the Aurora row cites the
                         demo-corpus audit for text that is in the gap audit
AGA_009                  half closes: WP1 and WP2 arrive, two ledgers do not
```

The tolerance is the **documents' own shipped precision**, not a constant
chosen here: `+12%` reports 12 +/- 0.5, so 11.77 agrees; stated to two places
it would not, and a check pins that. `_halfwidth` is imported from
`move-set/`, where it is already registered in `tools/known_answer.py` --
a second copy is the drift this tree has a checker for.

## What the audit does not touch

The drop's substantive arguments -- that automation's wins share a shape
(structured environment, validated envelope, repetitive task) and its
failures share the opposite; that AHS converts a regulated distributed
generalist input into a concentrated specialist one on a rebuilt surface;
that the wear comparison is confounded by the rebuild -- are not scored
here. They rest on carried figures. Where an argument is arithmetic over
figures the documents supply, it is checked; where it is a reading, it is
left as one.

Nothing is registered in `tools/known_answer.py` from this folder, and the
reason is stated rather than left as a silent absence: every function here
parses or counts over a fixed corpus, so its known answer is the enumeration
it walks, and the one genuine arithmetic helper is imported already
registered. The classifiers are null-tested in both directions instead --
including that an emptied document breaks the checks rather than passing
them.

Stdlib only, parses under 3.9, no network. CC0.
