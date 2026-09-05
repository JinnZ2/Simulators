# PLACEMENT — thermal_coupling.py / airblast_extension.py

Repo: earth-systems-physics
Decision: OWN MODULE. Do not attach to the existing cascade chain.
Opened: 2026-09-04

---

## THE CUT

```
existing cascade chain     maps a sequence of processes along a
                           runout path — trigger -> entrainment ->
                           deposit, ordered downstream

these two scripts          change the MAPPING DOMAIN, not a
                           threshold inside that sequence
```

The forcing case is Langtang: the core never reached the village, and
350+ died from the air blast, with tree breakage 550 m up the OPPOSITE
mountain. The object that has to be mapped is the valley cross-section
INCLUDING the counter-slope. A chain module indexed on runout distance
has no slot for a result that lands off the runout path — attaching it
there would file the counter-slope as an extension of runout, which is
the exact conflation the result contradicts.

Second, independent reason: the organizing form differs.

```
cascade chain      sequential, each stage consuming the prior
thermal coupling   hazard = trigger(T_fast) x PRODUCT of
                   primed_i( integral T_slow )
                   one forcing entering at separated lag classes
                   with different signs
```

A product over lag classes is not a stage in a sequence. Filing it as
one would make its non-monotonicity read as a parameter quirk rather
than as structure.

---

## MODULE CONTENTS

```
thermal_coupling.py       one free parameter, CAL_FOS 2.825,
                          calibrated to Mamot et al. 2021
                          ESurf 9:1125
airblast_extension.py     CLAIM_TABLE TC-07..TC-11
README.md                 the product form; the mapping-domain claim;
                          ENVELOPE section
```

## RESULTS THE MODULE CARRIES

```
freeze-thaw non-monotone with a DIP at zero — cycles/yr peak 222 at
  both -3 and +3 C, minimum 169 at 0. Sign of dDamage/dT flips inside
  a 3-degree window.
joint strength convex toward melting — last 3.5 degrees before melt
  remove 35% of shear strength and triple creep sensitivity.
avalanche band moves UP with warming, cascade-coincidence band moves
  DOWN. Filed UNFALSIFIED, NOT SUPPORTED.
snow fraction is the coupling coefficient — all-rock 1.0,
  Langtang >70% snow 10.6, all snow 12.8.
two channels extend footprint in DIFFERENT directions —
  deep snow -> entrainment -> powder cloud -> LATERAL;
  warm air -> meltwater -> lubrication -> LONGITUDINAL.
```

## LIMITS, stated in the module not buried

```
n = 1        everything anchored on one event
meltwater    two-point calibration to the published pair —
             a FIT, not a test
band claim   needs an event catalog pairing release elevation with
             primed-failure elevation. Single-process catalogs do not
             record that pairing, which is why it stays unfalsified.
```

## COUPLING TO THE REST OF THE REPO

Declared as a cross-reference, not as a merge:

```
-> cascade chain module        thermal state as an input to trigger
                               probability; the chain consumes a
                               number from here, it does not contain
                               this
-> terrain screen work         mapping domain = valley cross-section
                               incl. counter-slope. This is the
                               concrete change the screen inherits.
```

If a later result shows the product form IS a stage in the chain, the
merge is cheap and gets its own branch entry. The reverse — pulling a
mapping-domain change back out of a chain that has absorbed it — is not.
