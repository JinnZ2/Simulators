# CLAIM TABLE — QRNG PAIR SEARCH

---

**Q1.** A bath set assigned to a source does not price the fielded leg, because
the readout chain couples to baths the source does not.

*Falsifier:* a decay leg whose detector, bias and digitisation demonstrably do
not couple to substrate temperature, supply rail or ambient EM.

*Status:* SUPPORTED as an accounting claim and checked in `--selftest`. The
specific coupling magnitudes are **not measured here** — the direction is
argued from detector physics, the numbers are not in this folder.

---

**Q2.** Under source-plus-readout accounting, no admissible pair in this table
is clean; all ten are welded at TH, PWR and EM.

*Falsifier:* a quantum-quantum pair in this source set with empty fielded
overlap.

*Status:* SUPPORTED, and it follows from the table rather than from data. It
is a statement about this source list, not about all realisable QRNGs.

---

**Q3.** `separable` is a real category distinct from both `clean` and
`structural weld`: where sources share no bath, the fielded weld is an
engineering fact and can be removed by construction.

*Falsifier:* a fielded pair with empty structural overlap that still shows
correlated drift after rail, thermal and EM separation. **This is the
load-bearing claim of the folder** and it is the one most likely to fail,
because it asserts that a coupling nobody has measured is removable.

*Status:* UNTESTED. No measurement in this folder or its sources.

---

**Q4.** Keeping the correlation rule secret adds no min-entropy to the joint
output.

*Falsifier:* a threat model where the attacker has both raw streams and the
combiner's secrecy still bounds their advantage.

*Status:* SUPPORTED by Kerckhoffs's principle as standard practice. Stated as
a design rule, not as a theorem about a specific construction.

---

**Q5.** XOR of two independent streams has min-entropy at least that of the
better leg, so the XOR floor survives one leg being fully compromised.

*Falsifier:* independent legs whose XOR has min-entropy below the maximum of
the two.

*Status:* SUPPORTED, standard. **Conditional on independence** — which is
exactly what Q3 says is unmeasured, so the floor is only as good as the
measurement that is not yet run.

---

**Q6.** The k1 + k2 figure is a budget, not a bound.

*Falsifier:* none needed; the claim is a disclaimer. Reaching it requires a
named two-source extractor with a stated error and min-entropy requirement,
and this folder names none.

*Status:* SUPPORTED as stated. **The extractor choice is the largest unmade
decision here** and it is deliberately unmade — it is a cryptographic design
call, not a search-axis question.

---

**Q7.** A sample count of 1e6 resolves correlations of |r| ≥ 5e-3 at 5σ and is
blind below that; resolving 1e-3 costs 2.5e7.

*Falsifier:* arithmetic error, or an estimator with a materially better
standard error than 1/√N under the null.

*Status:* SUPPORTED and reproducible in `--selftest`. The Bonferroni-equivalent
lag adjustment is an approximation, not an exact multiple-comparison
correction.

---

**Q8.** A resting cross-correlation of zero is not evidence of independence.

*Falsifier:* a coupling mechanism that expresses at rest as strongly as under
perturbation, making the sweep redundant.

*Status:* SUPPORTED in the sense that it follows from what a bath is — a
shared channel that carries signal only when something drives it. Not
measured.

---

**Q9.** `avalanche_diode` is inadmissible as a leg because its gain stage is
classical, and `johnson_noise` because it has no quantum indeterminacy at all.

*Falsifier:* an avalanche construction where the multiplication does not
degrade the quantum character of the shot-noise floor, argued rather than
asserted.

*Status:* SUPPORTED as a conservative exclusion. Real avalanche QRNGs are
fielded and certified; this table excludes them from *this* pairing scheme,
which is a stricter bar than excluding them from use.
