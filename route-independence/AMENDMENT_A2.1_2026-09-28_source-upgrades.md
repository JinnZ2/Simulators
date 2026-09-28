# FWO AMENDMENT A-2.1 — 2026-09-28 — source upgrades + fixture corrections
Additive to A-2. R1: commit this block alone before code. R4 applies.

## 1. GRADE CHANGES
W-1a  CO HB 16-1005, signed bill text:
      content.leg.colorado.gov/sites/default/files/2016a_1005_signed.pdf
      Effective 2016-08-10, CONDITIONAL on sine die 2016-05-11.
      Condition confirmed by CO Division of Real Estate 2016 Annual
      Report. Grade S -> P. Resolves RIN_073 NOT_RUN.
W-2a  UT SB 32 (2010) enacts Utah Code 73-3-1.5 (le.utah.gov/~2010).
      Year precision only; effective date not read.       Grade P (year)
      Current text (Justia 2022 codification): unregistered = max two
      covered containers, EACH <= 100 gal; registered = <= 2,500 gal
      aggregate per parcel.                               Grade P

## 2. FIXTURE CORRECTIONS (the authoring errors are Claude's)
F-W3  WRONG as written (">100 gal unregistered" treats 100 as a
      total). Replace with:
      F-W3a UT, t >= 2010, unregistered, two containers <= 100 gal each
            METERED_PERMISSION
      F-W3b UT, t >= 2010, unregistered, any container > 100 gal
            PROHIBITED
      F-W3c UT, t < 2010   UNKNOWN (no prior-state source)
F-W1  WRONG instrument. Pre-2016 CO had no authorizing statute; the
      gate was the prior appropriation doctrine, not a prohibition
      statute. A 2009 CO law allowed limited collection (bill number
      NOT sourced). Split:
      F-W1a CO, t < 2009    gate_instrument = prior appropriation
            doctrine (cite constitutional article when sourced)
            gate_state PROHIBITED, grade S
      F-W1b CO, 2009..2016-08-09  UNKNOWN until the 2009 bill is sourced
F-W4  TX OPEN is a claim of ABSENCE. No enacting statute can source it.
      It needs an agency or attorney-general statement. Until then:
      UNKNOWN. Do not read it at year precision from the HOA bar.

## 3. NEW FIELD PROPOSED (do not build yet — flag only)
Both CO (HB 16-1005 s.1: rain barrel use "does not constitute a water
right"; State Engineer may curtail under 37-92-502(2)(a)) and UT (the
registration is not a water right, per a secondary source) grant access
that is statutorily declared NOT a right and revocable by an official.
The current enum cannot separate this from OPEN-by-right.
PROPOSED fields: access_is_right {TRUE, FALSE, UNKNOWN};
                 revocable_by {None | named office}.
QUESTION for the build, not an answer: is METERED_PERMISSION with
access_is_right = FALSE a sub-case of DISCRETIONARY? The G-2 transition
(right -> charity) and the CO/UT grants (no right -> permission, not a
right) may be the same state reached from opposite directions. Test,
don't assume.

## 4. SECONDARY, NOT ADOPTED AS INPUT
UT 73-2-27 criminal penalty (Class B misdemeanor default) and
UT 73-1-1 (waters declared property of the public): grade S. They are
the enforcement mechanism and the root gate for W-2. Read the statute
text before any fixture uses them.

## 5. EXPECTED (Claude's, committed before code)
E-A2.1-1  After the corrections, rainwater at t=2026 reads CO
          METERED_PERMISSION (P), UT METERED_PERMISSION or PROHIBITED
          by container size (P), TX UNKNOWN. Rainwater is OPEN nowhere
          SOURCED. Report this as UNMEASURED-OPEN, not as closure: the
          absence of a sourced OPEN row is not evidence of a closed
          route.
E-A2.1-2  E-A2-3 hold count does not change; its grade on rainwater
          moves S -> P for CO and UT.
