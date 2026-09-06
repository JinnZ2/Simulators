# WORK ORDER — machine-facing record format
## base layer with no pre-decided categorization

CC0. stdlib only. no network at runtime. phone-buildable.

Companion to WORK_ORDER_labor_instrument.md. That one specifies WHAT
gets recorded about work. This one specifies HOW any record is stored
so that the categorization is not baked in at write time.

---

## The problem this addresses

Existing datasets are shaped by what a reader can hold at once:
aggregated, rounded, collapsed into one canonical categorization.
Each of those steps discards, and the discard is not recoverable.

That shaping is a property of the datasets, not of human cognition.
Holding several parallel frames without collapsing to one is a
practiced skill and some traditions train it directly. The format
below is not compensating for a deficit — it is declining to import
one tradition's collapse.

A record read primarily by machines has no reason to pre-collapse.
Nothing needs to be decided in advance.

---

## Rule 1 — base entries are transformations, not categories

Store the transformation: input state, output state, exposure,
joules. Substrate-agnostic, physically observable, no framework in
the write path.

Do NOT store a category as a base field. A category is a claim about
which distinctions matter, and that claim belongs to a reader with a
question, not to the writer.

    base entry:
      entry_id
      input_state          (observable, declared units)
      output_state         (observable, declared units)
      exposure             (in that substrate class's own unit)
      exposure_unit        (person-hours | substrate-hours |
                            area-time | biomass-time | animal-hours)
      joules_in
      timestamp / period
      observation_method   (how this was measured, not inferred)
      provenance           (source, vintage, collection instrument)

---

## Rule 2 — categorizations are parallel views, never canonical

A categorization is a mapping from base entries to labels. Store any
number of them side by side. None is privileged. None is required.

    view record:
      view_id
      view_name            (e.g. NAICS_2017, ONET_taskclass,
                            metabolic_class, regulatory_scope)
      authoring_frame      (whose question this view answers)
      effective_span       (when this view was valid)
      mapping              entry_id -> label

Adding a view is additive and never rewrites base entries.
Retiring a view removes the mapping and leaves the base intact.

This is the part that breaks from the human-facing convention. A
reader who can only hold one categorization needs the dataset to
pick. A reader who can hold twelve does not, and picking costs
information that cannot be recovered later.

---

## Rule 3 — aggregation is a read operation

No aggregate, rounding, or bucket is stored as a base field.
Every aggregate is computed at read time from raw entries.

Store the recipe, not the result:

    aggregate spec:
      agg_id
      over_view            (which view's labels group by)
      operation            (sum | mean | rate | ratio)
      denominator          (declared explicitly — see Rule 5)
      filter               (which base entries are in scope)

If an aggregate is expensive, cache it — but cache it keyed to the
spec and the base-entry version, and treat it as derived. It is never
the record.

---

## Rule 4 — vintages are retained, nothing is overwritten

Every revision to a base entry is a new versioned observation, not a
replacement. The prior value stays readable with its own release date.

This is what makes late correction visible. A series re-benchmarked
and overwritten annually cannot audit a slow error, because the
vintage in which the error was live has been destroyed. Constraint
that arrives late can only be recorded by an instrument that keeps
the record long enough for the bill to arrive.

Same store as the labor instrument's `vintage_store`. Use it here.

---

## Rule 5 — declared boundary, always

Joule accounting is gameable by scope choice the same way carbon
accounting is. Move the system boundary and the number moves.

Therefore every entry carries an explicit boundary declaration:

    boundary:
      included             (enumerated, not implied)
      excluded             (enumerated, not implied)
      boundary_rationale   (why the cut is here)

An entry with no declared boundary is not comparable to any other
entry and should be flagged unusable for comparison, not silently
included.

Two entries may only be summed if their boundaries match or if a
declared reconciliation exists between them.

This is the outstanding item from the labor instrument work order.
It is closed here.

---

## Rule 6 — no conversion between exposure classes

Exposure units are declared and never converted. Conversion imports
a valuation, and the valuation is what is being audited.

Joules are the common denominator for comparison, not a conversion
rate between hours of different substrates. Report both columns.

---

## Rule 7 — absence is recorded

An entry that could not be measured is recorded as unmeasured, with
the reason. An entry that was measured as zero is recorded as zero.

These are different states and collapsing them is the most common way
a record lies. Unmeasured reads as absence, and absence reads as
"nothing there" rather than "wrong instrument."

    status: measured | unmeasured_no_instrument |
            unmeasured_out_of_scope | measured_zero

---

## Rule 8 — no payment field in the base layer

The base layer records transformations. Whether a payment record
exists for a transformation is NOT a base field, not a flag, and not
a substrate class.

This rule exists because every existing labor dataset carries the
paid/unpaid split, so a builder will import it by default. Do not.

What that split does when imported: work performed without a payment
record gets reclassified as "social" — bonding, cohesion, community
exchange — and then books at zero. The reclassification runs on the
payment record alone, not on anything about the output. Identical
transformation, identical exposure hours, identical joules, opposite
classification.

The affected capacity is not marginal. Volunteer fire and rescue,
disaster response, community maintenance, informal mutual-aid
agreements. Multi-discipline competency in several of these cases
BROADER than the paid equivalent, because there is no roster depth to
specialize into.

Correct handling:

    - transformation recorded on identical footing regardless of
      payment record
    - if payment is of interest to some reader, it enters as a VIEW
      (Rule 2), authored and dated like any other view, never as a
      base field
    - a view that filters to paid transformations must declare that
      filter under Rule 5, because it is a boundary exclusion

Interaction with Rule 7 that matters here: preventive work leaves no
positive record. The output is a failure that did not occur. That is
`unmeasured_no_instrument`, never `measured_zero`. Formal community
agreements leave a document; informal ones leave only the absence of
failure, which is the harder case and the more common one.

Reference material for why this rule is here, including the
comparison cases — commons-style village labor institutions with
documented rule structures and multi-century output records — is in
the marker, not in this spec. Do not reimplement it; consult it if
the rule is challenged.

---

## Test case format — REQUIRED for every test case in this spec

Every test case carries three fields, not one:

    tests:          what a pass establishes
    does not test:  what a pass does NOT establish
    why not:        the structural reason it cannot reach that

The "does not test" field is not a caveat and not modesty. It is
information of the same class as the positive result, and it is
recorded for a mechanical reason:

A positive result gets cited for whatever the citer needs. An
undeclared boundary is filled in by the reader, and the reader was
not present when the case was designed. A case that establishes X and
is silent about Y becomes evidence for Y within one citation, and the
error is then downstream of the record and unrecoverable.

So this is Rule 5 — declared boundary — applied to test cases rather
than to entries. Same rule, same reason. A case with no "does not
test" field is incomplete and must not be cited.

The "why not" field is what makes the boundary auditable rather than
asserted. It states the property of the case that blocks the wider
claim, which lets a later reader check whether a different case
WOULD reach it.

---

## Rule 8 test cases

Three cases, each testing a DIFFERENT thing. Do not merge them into
one validation; a pass on one is not a pass on the others.

### Case A — Amish barn raising. Tests Rule 8 end to end.
This is the only case with a contemporary paid control. Commercially
built agricultural structures exist in the same counties, same
climate, same use class.

    record both:  community-raised frame | contract-built structure
    columns:      exposure hours, crew size x days, materials,
                  joules_in, service life to date, maintenance
                  interval
    verdict:      both entries present on identical footing, summable,
                  neither carrying a payment field

Labor is recoverable rather than inferred — crew size and day count
are documented, the frame is inspectable. Service life 50-100+ years
observed. If the record cannot hold these two side by side without a
paid/unpaid field, Rule 8 is not implemented.

    does not test:  whether the willingness structure is
                    transferable outside a community that already
                    has it; also does not test large-scale or
                    non-structural output classes
    why not:        the community supplying the labor is
                    self-selected and has standing agreements
                    predating any given raising. The comparison
                    holds output class constant, not social
                    substrate. It answers "does the record handle
                    both," not "would this work elsewhere."


### Case B — terra preta. Tests the durability column and Rule 7.
Output is measurable in the present: soil carbon, fertility, depth,
spatial extent, persistence at 500-1000+ years with self-renewal.
Labor accounting is genuinely absent, not merely non-monetary.

    exposure:     inferred from deposit volume — WEAK column, must be
                  flagged unmeasured_no_instrument, not estimated and
                  reported as measured
    tests:        whether the record can carry a strong output figure
                  against an absent exposure figure without either
                  discarding the entry or fabricating the exposure

The failure mode this catches: a pipeline that requires exposure to
accept an entry will drop the best-performing artifact in the set.

    does not test:  output per unit of labor, or any efficiency
                    claim at all
    why not:        the exposure column is absent. A ratio needs
                    both terms, and inferring the missing one from
                    the present one makes the ratio circular.
                    Durability is available; efficiency is not.


### Case C — Machu Picchu / Inca mit'a. Tests Rule 6, no conversion.
Labor was taxed and administered directly. The state kept a labor
accounting system with no monetary layer, so the historical record is
already denominated in labor units.

    tests:        whether labor-unit records can be ingested and
                  compared WITHOUT conversion to a monetary or
                  hour-equivalent common unit
    does not test:  the willingness structure, community capital,
                    or unpaid coordination of any kind
    why not:        mit'a was a labor TAX. Coordination was
                    state-directed and compulsory. Absence of money
                    is not presence of willingness — those are
                    separate axes, and this case is non-monetary and
                    non-voluntary simultaneously, which is exactly
                    why it isolates the units question.

---

## Diagnostic tooling — bisection as structure test

Include a bisection utility, but specify it as a STRUCTURE test, not
a locator.

Standard use: fence the candidate span, test each half, recurse
toward the fault.

Reverse use — the failure modes are the measurement:

    signal on BOTH halves    -> not a locus; it is a property of the
                                whole span. Stop bisecting.
    signal on NEITHER half   -> the test is measuring something other
                                than the target, or the fault is
                                conditional on state the split
                                destroyed.
    signal migrates on
    repeat runs              -> nondeterministic; bisection invalid,
                                do not report a locus.

Run it first to answer "does a single locus exist," then for the
address. Reporting an address from a run that showed both-sides
signal is a false positive and the most likely way this tool produces
a wrong finding.

For instrument drift specifically: bisect on the methodology registry
(which changes are in the span), not on time. Methodology changes
have sharp boundaries; calendar time does not.

---

## Acceptance

1. A base entry written under one view can be re-read under a
   different view added later, with no rewrite of the base entry.
2. Any stored aggregate can be recomputed from base entries and the
   spec alone, and matches.
3. Two entries with mismatched boundaries cannot be summed without an
   explicit reconciliation record — the pipeline refuses.
4. A prior vintage of a revised entry is retrievable with its
   original release date.
5. `unmeasured` and `measured_zero` never collapse in any read path.
6. Bisection utility returns a structure verdict before any locus.
7. No base entry has a payment or compensation field. A paid-only
   aggregate is impossible without a declared view and a declared
   boundary exclusion.

---

## Open

- task boundary definition. Boundaries are currently set by system
  architecture (ten calls vs one call report differently). Must be
  defined by output delivered. "Output delivered" still needs a
  definition that does not drift with architecture. Open item, not
  a gap — it is solvable, just unsolved here.
- transformation vocabulary. The input-state / output-state pair
  needs a controlled vocabulary that is derived from physical
  transformation, not inherited from occupational taxonomy. Draft
  needed.
- merge_in / merge_out mechanics. Deferred until the above two
  settle, since they determine the merge semantics.
