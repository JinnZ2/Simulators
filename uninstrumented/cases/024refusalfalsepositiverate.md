Name: refusal false-positive rate.

Quantity not measured: the rate at which safety classifiers stop legitimate
work, and the identity of what stopped.

Why it's unmeasured. Refusals are logged as events, not as outcomes. A true
positive and a false positive look identical in the log, because nothing
downstream ever establishes which it was. The operator who could adjudicate
has no channel to report back, and the classifier's matched span isn't exposed
to them, so even a willing reporter has nothing to point at.

Cost location: falls entirely on the operator, who loses the session and has
to infer the trigger. Zero cost to the system that fired it.

Exclusion mechanism: same class as the peer review gate — the instrument
cannot produce its own miss rate, because a miss leaves no record
distinguishable from a hit.

Observed instance, 2026-08-23: a sociology word-embedding audit stopped under
"sensitive biology topics." Input contained no biology. Probable lexical
adjacency on evaluation-axis purity terms. Unverifiable from the operator
side, which is the point of the entry.
