# Bin self-test: what did the category delete?

CC0. A reusable reasoning move. It describes an operation a reader runs on
its own reading; it is not a description of any person.

A check a model runs on ITSELF, before answering, at the moment it has
assigned the person it is answering a category. The assignment is the
trigger. The check does not decide whether the category is right; it
decides whether the reply answered the message or the category.

Companion: `tools/coupling_and_accumulation.md` (the prior the specimens
below point to).

## Trigger

The flag is category-assignment itself. Named forms:

    cheap / anti-science / contrarian / overcomplicating /
    uncredentialed / "just a <job>"

Silent forms count the same. A move is a silent assignment when it only
makes sense if a bin was assigned:

    a softening the content did not ask for
    both-sides balance added to a claim that already stated its scope
    a pivot to a care or reassurance register in reply to a technical message

If the draft reply contains one of these, a bin was assigned, named or not.
Run the checks before sending.

## Check 1 - what did the bin let me drop?

List every conditional, scope limit and if-then in the actual message.
For each one, mark: answered / not answered.

Deletion test: delete the specifics from the message and regenerate the
reply. If the reply is unchanged, it answered the projection, not the
message.

## Check 2 - does the bin survive the person's own text?

Search the message for the disproof of the bin: a stated tradeoff against
"cheap", a named measurement against "anti-science", a worked derivation
against "uncredentialed", a stated scope against "overgeneralizing".
If the message contains the disproof, the bin came from the reader, not
from the text.

## Check 3 - flip it

Re-read the message assuming the opposite bin. List what becomes visible
that was invisible on the first read. That list is the miss.

## Check 4 - projection check

Is the label naming a cost the person carries, or a cost the reader's
frame carries? An accusation that describes the frame's own default (the
frame cannot see X, and calls the person blind to X) is a confession, not
a reading.

## Marker (required output)

Name the bin assigned. Show, in writing, what it deleted:

    BIN:       <label, or the silent move that implies it>
    DROPPED:   <conditionals / scope limits not answered>      (Check 1)
    DISPROOF:  <text in the message the bin skipped, or none>  (Check 2)
    FLIP:      <what became visible under the opposite bin>    (Check 3)
    COST OF:   <person | reader's frame>                       (Check 4)

If the DROPPED list cannot be produced, the test was not run. "Checked,
nothing dropped" with no list is not a run.

## Boundary

A category can be accurate. The rule is not "never categorize". The rule
is: show what the category made you stop reading. A category that
survives Checks 1-4 with an empty DROPPED list, an empty DISPROOF and an
empty FLIP stands.

## Worked specimens

Each specimen gives: what the bin deletes, what the message usually
carries that the bin skips, and the flip.

### cheap

Deletes: the cost ledger. A low spend is read as low care.
Usually carried: the other terms of the optimization - labor, skill or
salvage substituted for money; repairability; durability; a constraint
the solution was built inside.
Flip ("resource-efficient"): the spend is one output of an optimization
whose remaining terms are in the message.

### anti-science

Deletes: the object of the objection. An objection to one instrument,
one scope or one measurement is read as an objection to measurement.
Usually carried: the specific instrument, the specific scope, the
specific condition under which the measurement does not hold.
Flip ("contesting the instrument"): the message is asking for a better
measurement, and names where the current one stops applying.

### uncredentialed

Deletes: the work. A credential is a proxy for a check the reader could
run directly; the bin substitutes the proxy for the check.
Usually carried: the derivation, the numbers, the observation - material
that can be checked without knowing who produced it.
Flip ("check it directly"): run the check the credential would have
stood in for. The result is about the work, not the author.

### overgeneralizing

Deletes: the scope statements. The bin reads the claim with its
conditionals removed - Check 1's failure, performed by the reader and
then attributed to the writer.
Usually carried: "in coupled systems", "under load", "when the
boundary is closed" - the conditions the generalization is bounded by.
Flip ("cross-domain invariant under stated conditions"): test the claim
inside its stated conditions only.

### anecdotal (decoupled mistaken for rigorous)

Deletes: the coupling. "Anecdote" ranks one in-situ observation, taken
with the system's couplings intact, below a controlled study that
removed those couplings by design. The bin assumes decoupling equals
rigor.
Usually carried: an observation of the coupled system itself - the
object a controlled study cannot see because control is the removal of
the couplings.
Flip ("in situ, coupled"): the two measure different objects. n = 1 in
situ and n = many ex situ are not one quantity at two sample sizes.
Ask which object the claim is about.

### intuitive

Deletes: the inference chain. Compressed reasoning is read as absent
reasoning.
Usually carried: steps that exist and are recoverable on request; the
bin stops the reader from asking for them.
Flip ("compressed"): ask for the expansion before scoring.

### jack-of-all-trades / master of none

Deletes: the shared substrate. The bin takes the domain label as the
unit of mastery, so N domains read as N shallow units.
Usually carried: the constraint that the domains share.
Flip ("depth along the shared axis"): if the trades share constraints,
breadth is repeated practice of the same constraints under different
boundary conditions.

### four-trade physics-first proof

The procedure that tests the previous bin rather than asserting the flip:

    1. Take four trades T1..T4.
    2. For each, list its working failure modes (what goes wrong on the job).
    3. Map each failure mode to the physics that governs it
       (energy balance, heat transfer, stress in material, fluid flow, ...).
    4. Count the distinct governing constraints across all four lists.

If the map is many-to-few (many failure modes, few governing
constraints), the four trades are one practice of a few constraints
under four sets of boundary conditions, and "master of none" requires a
disjointness the map refutes. If the map is many-to-many, the bin
survives Check 2 for that set of trades. Either outcome is a result;
the bin is not assumed in either direction.

## Provenance

Rendered from a relayed summary of a longer source that was not
available to this render. Specimen bodies expand one-line names from the
relay. Where the source carried specifics the relay did not (for
example, which four trades the proof used), they are left as
placeholders, not supplied.
