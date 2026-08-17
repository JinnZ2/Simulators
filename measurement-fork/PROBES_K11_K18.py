#!/usr/bin/env python3
# PROBES_K11_K18.py -- additions to coupling.py / widen.py
# CC0-1.0. Standard library only. Merge, do not import blindly.
#
# sweep: every probe declares which spec variable it must be run
# across, and at how many levels. Default regime.variable, min 2.
# Point-probes declare sweep=None WITH a reason.
#
# STRUCTURAL BUG THIS FIXES: coupling.py generated probes at a
# POINT while the stated falsifier ("ratio flat across the
# provisioning gradient") is about a GRADIENT. The generator
# could not emit a design capable of failing its own falsifier.
# compare.py must flag any falsifier whose terms are not swept
# by any arm.

COUPLING_PROBES = [

    dict(id="K11", base="information_rate", normalizer=None,
         object_of="coupling", sweep=("regime.variable", 2),
         protocol=("distinguishable environmental states registered "
                   "per unit time, by the actor's own sensors"),
         not_="K01 delay, K02 reliability. This is channel capacity.",
         blind_to="whether anything is done with the states"),

    dict(id="K12", base="reliance_weight", normalizer="sensor_validity",
         object_of="coupling", sweep=("regime.variable", 2),
         protocol=("(a) weight given to own read vs alternative "
                   "sources; (b) whether own read tracks outcome. "
                   "Trust is a measurement only if (b) was run."),
         not_="K06 reads confidence. This reads validation history."),

    dict(id="K13", base="tau", normalizer=None,
         object_of="coupling", sweep=("provisioning_level", 2),
         protocol="error vs trials-since-shift, fit tau",
         closes=["reversibility", "falsifier:ratio_flat"],
         predicted="tau rises with provisioning; flat tau falsifies"),

    dict(id="K14", base="practice_rate", normalizer=None,
         object_of="coupling", sweep=("provisioning_level", 2),
         protocol="is the channel exercised during the stable interval",
         signature=("expenditure with zero return, concurrent with "
                    "all-nominal state variables"),
         note="scored as waste by any efficiency instrument"),

    dict(id="K15", base="baseline_freshness", normalizer=None,
         object_of="coupling", sweep=("time_since_clean_reference", 3),
         protocol=("inject small known deviation; measure detection "
                   "threshold"),
         predicted="threshold rises with staleness",
         role="MEDIATOR: K14 acts on K16 through K15"),

    dict(id="K16", base="detection_latency", normalizer=None,
         object_of="coupling", sweep=("baseline_staleness", 3),
         protocol=("small-signal detection before the outcome column "
                   "moves")),
]

PREDICTED_ORDER = """
  practice_rate falls
    -> baseline_freshness degrades   (lag 1)
      -> detection_latency rises     (lag 2)
  all three while state variables read nominal.
  FALSIFIER: if K14 predicts K16 with K15 controlled out, the
  mediation chain is wrong.
"""

# --- widen.py additions. option(), not quantity(): OBJECTS is
# --- closed and object_of="design" is not a legal quantity (MF_008).

WIDEN_OPTIONS = [

    dict(id="W13", axis="instrument", name="AGGREGATION DEPTH",
         ask=("decompose each term in the model; tag each component "
              "with object_of. Count > 1 is a flag."),
         reads="where components with opposite signs cancel silently",
         note=("in-sample fit is EXCELLENT when this failure is "
               "present -- components covary in the sampled range. "
               "Good fit is not evidence against it."),
         falsifier="terms decompose to one object each"),

    dict(id="W14", axis="physical", name="BUDGET CLOSURE",
         ask=("name every input and every disposal path. Which are "
              "inside the boundary, which outside, and who set the "
              "line."),
         reads="ratios comparing a closed budget to an open one",
         example=("leaf quantum yield vs panel: fabrication, repair, "
                  "replication, disposal inside one budget and "
                  "outside the other")),
]
