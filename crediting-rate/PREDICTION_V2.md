# Pre-stated prediction, revision 2 -- recorded 2026-09-23, before any coding exists

    crediting_rate(visible) > crediting_rate(technical_only)
      >= crediting_rate(not_retained)

`technical_only` is the discriminating bin: the word survived and the
reader cannot see it. If it tracks `not_retained`, visibility is the
variable. If it tracks `visible`, retention is.

Stated now so it cannot be fitted afterward. `crediting_rate_v2.py`
refuses to run without this file and prints its sha256 in every report; a
change to this file changes the hash every report carries.

The ordering is the only thing predicted. No gap size, no domain, no
threshold. The null band from N1 is what decides whether an observed gap
is distinguishable from a shuffle, and that band is computed.

## What the ordering does and does not separate

The second comparison is NON-STRICT. `technical_only == not_retained`
satisfies the ordering and so does `technical_only` anywhere strictly
between the other two, so the ordering holds across a continuum and does
not by itself say which of the two readings the discriminating bin
supports. The `position` statistic is reported for that and its cut is a
declared `[CHOICE]`, not a prediction:

    position = (r_technical - r_not) / (r_visible - r_not)

0.0 is "tracks not_retained", 1.0 is "tracks visible". It is UNDEFINED,
never 0.5, when the two outer bins do not separate.

The two readings are not symmetric with respect to this file. "Tracks
`not_retained`" sits INSIDE the predicted ordering; "tracks `visible`"
violates `visible > technical_only` and so REFUTES it. That is recorded
here rather than discovered later: the pre-stated ordering already
encodes the visibility hypothesis, so one branch of the discriminator is
a confirmation and the other is a refutation, and they are not two
outcomes of one neutral test.
