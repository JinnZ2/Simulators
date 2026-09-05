# ADDENDUM 02 — a units field may name a SCALE, not a TYPE

Attaches to: ADDENDUM 01 (SCOPE-DIFFERENT admissibility)
Forced by: Kimi falsifier survey, Run 2 (gm + g2b), 2026-09-05
Status: rule ADJUSTED

---

## BRANCH ENTRY 02

```
rule as stated   MEASURED requires MEASURED_AS: quantity + units +
                 how obtained. No units -> not MEASURED. Downgrade.

forcing case     96 of 537 MEASURED cells in Run 2 carry a units
                 field that names a DATA TYPE with no number or
                 threshold anywhere in it. Examples as coded:
                   "boolean (contradicts / corroborates)"
                   "boolean verdict in 'empirical_stability' column"
                   "boolean isfinite check per step"
                   "boolean verdict over relabellings"
                 The field is filled. The rule passes them.

axis             does "units" mean the SCALE a quantity is read on,
                 or the TYPE the result is stored as?

derivation       The rule was written to keep prose from passing as
                 a measurement. A type name defeats it without
                 evading it: "boolean" is a legitimate answer to
                 "what units", and it carries no scale, no
                 threshold, and no way for two coders to disagree
                 about a value.

                 The discriminator is visible in the same run.
                 These PASS correctly:
                   "dimensionless exponent with 95% CI
                    (super-linear claim requires beta > 1.2)"
                   "integer count, threshold 3"
                   "lead in steps; null FP rate <= 0.2"
                 Each names a scale and a cut on it. Dimensionless
                 is not the problem. Thresholdless is.

                 So the failure is not in the units REQUIREMENT.
                 It is in what the requirement accepts as
                 satisfying it.

                 Counter-reading considered and rejected: that a
                 boolean check IS the measurement for a
                 pass/fail falsifier ("outputs finite or not").
                 Rejected because the underlying quantity is still
                 scaled — finite/NaN is a cut on a float, count>0 is
                 a cut on an integer. Naming the cut costs one
                 clause and restores the ability to disagree. Where
                 no underlying scale exists, the cell is not
                 MEASURED and the rule is doing its job.

frame note       NARROW, not rescope. The frame is intact — a
                 falsifier still needs a measurable. The boundary
                 was drawn too wide by leaving "units" ungraded.
                 Contrast with ENTRY 01, which was a rescope: there
                 the rule had inherited a two-status frame and had
                 to lose generality. Here it keeps its generality
                 and gains a scope condition.
```

---

## ADJUSTED RULE

```
MEASURED requires MEASURED_AS:
  quantity      what is being read
  units         the SCALE it is read on, and the CUT on that scale
                (threshold, band, or comparison target)
                A data type is not a scale. "boolean", "verdict",
                "integer", "unitless" alone do not satisfy this.
                "integer count, threshold 3" does.
                "dimensionless, beta > 1.2" does.
  how_obtained  unchanged

If the falsifier is a pass/fail check, name the underlying scale and
the cut: not "boolean isfinite check" but "float magnitude; cut at
non-finite". If no underlying scale exists, the cell is not
MEASURED — downgrade with that reason.
```

## RE-CODING REQUIRED

```
scope     the 96 Run-2 MEASURED cells with a type-only units field.
          Run 1 was not scanned for this; scan it under the same
          test before re-coding either run.
action    supply the scale and cut, or downgrade with the reason
          stated. Do NOT delete the cell.
report    report.py emits a separate count: MEASURED cells whose
          units field names a type rather than a scale. That count
          should go to zero and then stay visible as a zero, the
          same way the SCOPE-DIFFERENT-lacking-transform line does.
expected  some fraction will legitimately downgrade. That is the
          instrument working, not the survey failing.
```

## NOT CHANGED

```
- SCOPE_TRANSFORM (reference / maps_to / breaks_at) is unaffected.
  Zero cells lacked a complete transform in either run; that bar
  is holding.
- The MISSING and UNKNOWN definitions are unaffected.
- No verdict field is added. Repair type is judged per case; what
  is recorded is the derivation.
```
