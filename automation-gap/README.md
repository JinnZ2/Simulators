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
                                 first runnable arithmetic, an EXPLORATION
                                 list (X1, X2) and an imported-skill arm on
                                 QE.  Revised four times;
                                 register_audit.revision() resolves the
                                 previous version by content and measures
                                 what moved

audit.py                         recomputes what the six documents state
register_audit.py                imports the register, checks it against
                                 its own declared rules
test_audit.py                    checks on the audit; prints its count
test_register.py                 checks on the register audit; prints its
                                 count
CLAIM_TABLE.md                   AGA_001..066 with falsifiers
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

## The v6 and v7 revisions

`ADDENDUM_3.md`'s material then arrived **as code**, and `AGA_044` closed
by arrival: `EXPLORATION` is the register's seventh docstring rung, so a
reader of the register alone can discover it. The second half did not
close -- the rung is carried by **no entry field**, applied by the name of
the section its entries sit in, and `status_vocabulary` reports it
`unused_anywhere`, the first rung ever to read that way. Beside it
`SLEEP_QUALITY_FACTORS` puts the per-operator term `AGA_045` named into
the file: four factors each stating a status, *operator* now in `G0_NOTES`
and still not in the G0 gate entry, and the only function reading the list
is a print -- `g0_window_needed`, the function the gate's window comes out
of, reads `REST_BLOCK`'s four constants and nothing else. Declared, and
absent from the number.

**Two faults in this audit's own machinery, both found by running.**
`_declared()` split a vocabulary block on two-or-more spaces where the
rung names are padded to a column, so the **longest** name -- eleven
characters, `EXPLORATION`, the newest -- was dropped: six rungs read
against seven declared, which would have reported `AGA_044` as still open.
A parser that drops the longest entry drops the newest, because a new name
is what pushes a column. And `AGA_020`'s falsifier reads *a source carrying
`DERIVED`*: v7 put `[DERIVED]` inside S10's `holds`, so it **fired a second
time by the same mechanism** -- in a claim whose own body records the first
firing and then restates the ambiguous wording verbatim. The falsifier now
names the field, and the fault is read out of git rather than recalled, so
the repair turns the check red on purpose -- and **`AGA_066`**: the first
version of that reader read `HEAD`, so committing the repair erased the
record of the firing, which is `AGA_033`'s own shape committed one hour
after amending the claim that states it. It now walks back until the
falsifier stops naming the token only.

The v6 delivery also shipped a **duplicated tail** -- two `__main__`
blocks, the addendum-3 header printed three times -- with the importable
surface intact throughout: 15 top-level objects, none defined twice, so the
cost fell on a reader of stdout and not on this audit. Recorded rather than
repaired, the file being delivered, and **the v7 delivery removed it
anyway** -- the audit was never sent, so the repair is independent of it.

**What v7 adds is a third explanation for the tenure curve.** S10 gains
two entries -- ran nights as a trainee, using exercises, katas, stretches
and scents for state regulation -- and QE gains an IMPORTED-skill arm:
*CDL tenure counts months licensed, not state-regulation skill brought from
elsewhere*, so a novice by tenure can be adapted by practice and the screen
measures a proxy. The register's own rule says an `N_OF_1` record **bounds
what is possible and does not estimate a rate**, and the arm states a
possibility, estimates nothing, and carries a `[DERIVED]` tag -- the rule
obeyed on the one source where breaking it would be cheapest. The cost is
in the slot: QE's source list is empty and its next-step field leans on S10
by name, so a reader counting off the structured map gets six questions
resting on the N=1 record and misses this one.

X2 gains a `channels` field, and three things follow. `EXPLORATION` is a
**sixth inline-tag site** the vocabulary checker does not scan, and
`X2.channels` is the first field in the register to carry **two rungs in
one string** (`[DERIVED]` on one clause, `[PROPOSED]` on another) -- the
omission is silent today, because every token there also occurs at a
scanned site, which is exactly what makes it invisible. The two entries now
carry **different field sets with no schema**, and `addendum3` guards with
`if k in x`, so an absent field and a field nobody thought to fill print
identically; the substantive cost is that `channels` names **motion** as a
portable sleep cue and motion is X1's entire subject, with X1 carrying no
such field and the cross-reference running one way only. And the anchor
records *"categories only, specifics not shared, none requested"* -- the
scope field declares a consent limit, the anchor records it being
exercised, and **a record of an ask that was not made** has no precedent
here, where the usual failure is a record that does not say the ask
happened.
