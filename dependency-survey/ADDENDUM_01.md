# ADDENDUM 01 — SCOPE-DIFFERENT admissibility, and the taxonomy test

Attaches to: WORK_ORDER.md, cross-substrate dependency survey
Opened: 2026-09-04
Status: the rule below is ADJUSTED; the taxonomy question is OPEN and is
        itself a survey output

---

## 0. THE FORCING CASE

The instrument caught its own work order on first run. The seeded cell
T3 x S5 was coded SCOPE-DIFFERENT with a prose scope note and no
MEASURED_AS, which the order's own units rule rejects.

This is not a defect in the run. It is a branch, and it gets a branch
record rather than a patch.

```
BRANCH ENTRY 01
  rule as stated   MEASURED_AS (quantity + units + how obtained) is
                   required if MEASURED or SCOPE-DIFFERENT. A cell with
                   no units cannot be MEASURED; downgrade it.

  forcing case     T3 x S5 — nation-state boundary accounting, coded
                   SCOPE-DIFFERENT, carries a scope note and no units.

  axis             does SCOPE-DIFFERENT carry the same evidentiary
                   burden, of the same TYPE, as MEASURED?

  derivation       Two readings were available.
                   (a) SCOPE-DIFFERENT is a subtype of MEASURED, the
                       units rule holds, and the seed is uncoded and
                       drops to UNKNOWN.
                   (b) SCOPE-DIFFERENT is a third status whose evidence
                       is of a different type, and the units rule was
                       written as if only two statuses existed.

                   Grounds for (b), on measurement-theory rather than
                   preference: a measurement is a quantity PLUS a frame.
                   Two systems can carry the same quantity in different
                   frames and not be comparable — that is not a
                   deficiency in either measurement, it is the frames
                   differing. A status reporting "measured, but the
                   frame differs" is reporting FRAME information, and
                   frame information is not denominated in the
                   quantity's units. Requiring units for it asks a
                   reference frame to be expressed in meters.

                   Reading (a) is rejected because it would discard
                   real frame information as uncoded, which is the
                   error the status exists to prevent.

                   (b) does NOT license evidence-free coding. A frame
                   difference is specifiable — not in the quantity's
                   units, but in the TRANSFORMATION. So SCOPE-DIFFERENT
                   acquires its own admissibility bar rather than none.

                   Under the adjusted rule the seed STILL FAILS: it has
                   a prose scope note and no stated transformation. It
                   did not fail the units rule; it fails the rule that
                   should have been written.

  frame note       RESCOPE, not narrow. The units rule inherited a
                   two-status frame (measured / not measured) and was
                   correct inside it. It keeps its truth value for
                   MEASURED cells and loses its generality across the
                   third status. Narrowing it — adding an exemption for
                   SCOPE-DIFFERENT — would have stopped the complaint
                   and left the inherited frame undeclared, to re-strain
                   from a different direction later.
```

---

## 1. ADJUSTED RULE

```
MEASURED         requires MEASURED_AS: quantity + units + how obtained.
                 No units -> not MEASURED. Downgrade.

SCOPE-DIFFERENT  requires SCOPE_TRANSFORM, not units:
                   reference    what frame/boundary/baseline this
                                substrate's measure is taken against
                   maps_to      what in the comparison substrate it
                                corresponds to
                   breaks_at    where the correspondence fails, and
                                on what
                 A prose note with none of these three is not admissible.
                 Downgrade to UNKNOWN.

MISSING          unchanged.
UNKNOWN          unchanged; still emitted explicitly, never silent.
```

Any exemption previously applied to keep the seed coded is superseded by
this rule and should be removed. The seed is recoded by the same bar as
every other cell: supply the SCOPE_TRANSFORM or drop it to UNKNOWN.

---

## 2. THE OPEN QUESTION — taxonomy test

Unknown, and not resolvable by argument: whether SCOPE-DIFFERENT is ONE
thing or SEVERAL. Candidate kinds, not asserted, only named so the coder
has something to disagree with:

```
K1  frame difference        same quantity, different reference body
K2  boundary difference     same quantity, different accounting
                            boundary drawn around it
K3  homonym                 different quantity carrying the same name
```

These would not behave the same. K1 may be transformable, K2 may be a
re-draw rather than a transform, K3 may not be a scope-difference at all
and may belong in MISSING.

### Test

```
1  Code every cell that is neither MEASURED nor MISSING.
2  Do NOT assign a kind while coding. Write the SCOPE_TRANSFORM only.
3  When the set is complete, sort the transforms and ask whether they
   fall into kinds or stay one thing.
4  Emit the result either way. "One kind" is a result. So is "three".
```

### Constraints on the test

- The kinds above must not be offered to the coder as a menu during
  coding. Sorting must come from the transforms, or the taxonomy is
  the coder's prior read back.
- Small N is expected. The output is a candidate taxonomy with its N
  stated, not a settled one.
- If the transforms do not sort, that is evidence the third status is
  a single thing and the adjusted rule is sufficient as written.

---

## 3. WHAT CHANGES IN THE BUILD

```
survey.py    SCOPE_TRANSFORM replaces MEASURED_AS for SCOPE-DIFFERENT
             cells; three subfields, all required
             remove any prior SCOPE-DIFFERENT exemption
report.py    emit SCOPE_TRANSFORM fields in the cell records
             emit a count of SCOPE-DIFFERENT cells lacking a complete
             transform, as a separate line from the UNKNOWN count
new          nothing. The taxonomy test consumes the survey's own
             output; it needs no additional module until there is
             something to sort.
```
