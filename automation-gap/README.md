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
ADDENDUM_3.md                    a second delivered document, in notes:
                                 a per-operator G0 factor, a two-
                                 literature gap (X1), a probe, scope
                                 limits, a flip, a new status rung

driver_hours_evidence_register.py
                                 twelve sources, ten questions, a term
                                 note, on what is known / self-reported /
                                 UNMEASURED about long days, fatigue and
                                 tenure, plus two addenda: continued
                                 work (QK, clock-vs-state control loops, a
                                 behaviour-anchored record) and a proposed
                                 gate map G0-G4 carrying the register's
                                 first runnable arithmetic.  Revised
                                 twice; register_audit.revision() resolves
                                 the previous version by content and
                                 measures what moved

audit.py                         recomputes what the six documents state
register_audit.py                imports the register, checks it against
                                 its own declared rules
test_audit.py                    checks on the audit; prints its count
test_register.py                 checks on the register audit; prints its
                                 count
CLAIM_TABLE.md                   AGA_001..050 with falsifiers
```

The register arrived a drop after the seed and is a different kind of
object: the six documents are a self-contained drop whose figures can be
checked against each other, and the register is a map of **external**
evidence, eleven sources of which it marks five UNREAD itself. So
`register_audit.py` checks it against its own declared rules rather than
against its sources, and **imports** it -- the objects under test are the
register's own -- rather than parsing it. Its `n_eff` comes from
`effective-redundancy-audit`, imported and not reimplemented: two of the
sources under one question turn out to share three authors.

Five of the register's ten questions are UNMEASURED, which is the
register's own headline and its own point: *an UNMEASURED cell is a
result.* The audit adds that **seven of ten are not answered** -- the
count reads one status token and the revision added two open questions
under two others -- that the fatigue-by-tenure question (QD) has no source
at all, that the tenure curve cannot be read as learning rather than
survivorship from any source in it (QE), and that one term of the
driverless-versus-human comparison (QH) is absent from the corpus
entirely, since no document here states a driving-hours limit.

The revision's own strongest content is QJ, which holds a contradiction
between two sources the register already carries -- experience predicting
MORE *"fell asleep at the wheel"* against crash risk falling with
experience -- names three rival explanations, says which predicts it fully,
and picks none. The one that predicts it fully is the register's own term
drift: the phrase meant *pulled over and slept* to an older cohort and
*dozed while moving* to a younger one, a rest act and a hazard event
counted as one item with opposite signs for risk.

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

The gate map is the first thing in the folder with arithmetic in it, and
every input is declared `PLACEHOLDER` by the register itself. It
recomputes: interrupt rate 0.330/h, mean gap 181.8 min, and a binding row
-- a full sleep cycle plus high sleep inertia, 125 min -- at
**P = 0.503**, a coin flip. Its own note that *the binding term is
`p_machine_fails`, not raw event rate* holds exactly: the class with the
highest raw rate contributes 0.05 and the top contributor is a different
one at 0.09.

The sharp result is `AGA_041`. The same caveat about clustering is stated
in two places under two different conditions, and the two run **opposite
ways** -- shown exactly, no simulation, since both are Poisson integrals.
Bursting alone makes Poisson a **floor** (a burst of `k` at one instant is
a Poisson process of bursts at `lam/k`, so P rises: 0.503 to 0.934 at
k=10). A rate peaking at the hour rest is needed makes it a **ceiling**
(0.503 down to 0.189). The function's docstring names the second condition
and is right; the note drops it, describes the first mechanism, and draws
the second's conclusion. A qualifier lost between two occurrences of one
phrase with the reading inverting -- which is the register's own subject,
in its own text. Correcting it makes the register's case stronger, and
strongest exactly where it binds.

`ADDENDUM_3.md` is delivered in notes rather than Python, so the two
documents are read **as delivered** and where they disagree that is
reported rather than resolved: the note declares a status rung
(`EXPLORATION`) the register's scale does not carry, and it makes G0 a
**per-operator** gate where the register's G0 is indexed on route and
season and holds its window as four constants.

Its consequence -- *a blanket rule written to the lowest sleeper forfeits
the capacity of everyone above it* -- computes on the register's own
placeholder rate: the best motion-sleeper gives up **30.1% of their own
capacity** under a fleet rule set to the longest window. The structural
half is sharper. The gap vanishes at both ends -- at a low interrupt rate
everyone clears, at a high one nobody does -- and peaks at 0.678/h, so
**the cost of a blanket rule is largest exactly where the rule is deciding
anything**, and the placeholder regime sits at 82% of that peak. No fleet
aggregate is emitted, because the mix of operators is unmeasured.

And `AGA_047`: X1 predicts *early habituation -> smaller motion effect*,
while the note's own `SCOPE LIMITS` names a good-sleeper ceiling that
predicts the same direction. The probe names one covariate; the second one
-- record baseline -- sits one section above it and is in neither the
probe nor X1's compressed `scope` field. The note contains its own
confound and its own repair, and the compressed record drops the half that
confounds it. Third instance here of a qualifier lost in compression.
