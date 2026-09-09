# Pre-stated prediction — recorded 2026-09-07, before any coding exists

crediting_rate(loanword_retained = 1) > crediting_rate(loanword_retained = 0)

Credit tracks the surviving word, not the contribution. Stated now so it
cannot be fitted afterward. `crediting_rate.py` refuses to run without this
file and prints its sha256 in every report; a change to this file changes the
hash the report carries.

The direction is the only thing predicted. No gap size, no domain, no
threshold. The null band from N1 is what decides whether the observed gap is
distinguishable from a shuffle, and that band is computed, not predicted.
