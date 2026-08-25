# CLAIM TABLE — custody-verification-band

---

**B1.** The 3/4 metabolic exponent follows from an area-preserving radius
ratio of n^(-1/2) together with a space-filling length ratio of n^(-1/3), and
needs both.

*Falsifier:* arithmetic error, or a derivation reaching 3/4 from one ratio.

*Status:* SUPPORTED. Reproduces to 0.750000 over 20 levels in
`branching.py --selftest`, and is level-count independent. The source is
unread; the arithmetic is checked.

---

**B2.** Under area preservation the aggregate cross-section is constant per
generation, not widening. It widens by n^(1/3) under Murray's law.

*Falsifier:* arithmetic error.

*Status:* SUPPORTED and checked. n*beta^2 = 1 exactly under area preservation
— that is what the name asserts. The delivered anchor claimed widening under
area preservation, which is the two regimes crossed.

---

**B3.** "Trunk never wins by construction" holds in the Murray regime and is
neutral in the area-preserving regime.

*Falsifier:* a route from constant aggregate cross-section to a trunk
disadvantage.

*Status:* SUPPORTED as arithmetic. The conclusion survives the correction;
the stated route to it does not.

---

**B4.** The one-line criterion and the recorded-cut reading are different
instruments.

*Falsifier:* no case where they disagree.

*Status:* **WITHDRAWN.** It was SUPPORTED over six invented SEED cases, two
of which were written to disagree. Those cases were replaced by the eleven
real ones and the disagreement did not survive: the two-cut criterion and the
three recorded cuts agree on all eleven, zero disagreements. The earlier
result measured the seeds, not the world — which is what its own caveat said
it might. Asserted by test in `extract.py --selftest`.

---

**B5.** A layer buffers a system iff self-custodied and locally verifiable.

*Falsifier:* a layer that is both and does not buffer, or buffers while being
neither. Per B4 the seed set already contains a candidate for the first.

*Status:* UNTESTED. This is the folder's central claim and no case in it is
an observation.

---

**B6.** Verification, not custody, is the cut that separates a platform worker
from an owner-operator.

*Falsifier:* a platform arrangement with opaque allocation that nonetheless
buffers.

*Status:* UNTESTED, and currently an artifact of how the seed cases were
written. Listed because it is the sharpest prediction the criterion makes.

---

**B8.** `parallel_path` carries no information that `custody` does not
already carry.

*Falsifier:* a case with routed custody and a working parallel path — a
system where the contributor holds no residual and function survives node
loss. Municipal utilities and open-source infrastructure are the obvious
candidates and neither is in the corpus.

*Status:* SUPPORTED across all eleven cases: `routed→no, mixed→partial,
self→yes`, with no exception. Reported by `extract.py check` on every run.
**Whether this is a regularity or a coding artifact is undetermined** — the
same judgement may have been entered twice under two names. `gaps.md`
G-COLLINEAR states what would separate them. If it is a regularity it is the
strongest structural result here and belongs in this table rather than in the
schema; if it is an artifact the three-cut table is a two-cut table.

---

**B9.** `comfort_threshold` — the level at which an operator would act — is a
second readout distinct from confidence.

*Falsifier:* cases where the two move together, making the second redundant.

*Status:* UNTESTABLE as it stands. The field is declared in the schema and
carried by none of the eleven cases. A second readout that is never taken is
not yet a readout.

---

**B7.** Physical branching geometry licenses an inference about economic
layers.

*Falsifier:* SHAPE_SPEC section 4 supplies the one this claim lacked. State
which constraint, if REMOVED, changes the geometry; then find a case where it
is genuinely absent and check the form differs.

*Status:* **ASSERTED, NOT ARGUED — and SHAPE_SPEC section 2 names this exact
failure.** "Branching form applied to a system with no flux and no dissipation
term looks like insight and carries no information." `branching.py` contains
no flux term and no dissipation term; it computes geometry ratios only. The
transfer from vessels to layers ports a geometry without checking whether the
constraints came with it.

Under SHAPE_SPEC section 1 the shape is the constraint set, not the geometry,
so the ratios are the readout and the transfer is unlicensed until the
constraint set is enumerated on both sides and shown to be shared. Under
section 4 a failed transfer would be a MEASUREMENT — port it, get a different
form, and a differing constraint has been located. That has not been run
either.

The folder therefore has no shape read here, only a geometry note. Recorded as
such rather than left implicit in the anchor block where it reads as physics.
See `gaps.md` G-REGIME.
