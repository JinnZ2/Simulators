# Pre-stated prediction — WORK ORDER L REVISED, recorded before any v2 run

    crediting_rate(visible) > crediting_rate(technical_only)
                           >= crediting_rate(not_retained)

`technical_only` is the discriminating bin: the word survived and a general
reader cannot see it. If it tracks `not_retained`, **visibility** is the
variable. If it tracks `visible`, **retention** is.

Stated now so it cannot be fitted afterward. `crediting_rate_v2.py` refuses to
run without this file and prints its sha256 in every report; a change here
changes the hash the report carries.

The ORDERING is the only thing predicted. No gap size, no domain, no
threshold. The N1 band is computed, not predicted, and decides whether the
observed gap is distinguishable from a shuffle of the bin labels.

## Provenance of the prediction

The three revisions this file belongs to — the three-state bin, the frame
gate, the coding split — are **model-authored** and were sent
un-adjudicated: the dispatch bundle's own send-order table reads *"three
revisions are Claude's, PROPOSED, adopt or strip before sending"*, and it
was sent as delivered. So this prediction is a prediction of the revision,
not of the operator. v1's `PREDICTION.md` is the operator's, and it predicts
a two-state ordering.
