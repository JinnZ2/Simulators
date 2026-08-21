# CLAIM TABLE — SEARCH SUBSTITUTION

---

**C1.** Physarum polycephalum produces a low-cost connecting network over
distributed sources without enumerating candidate networks, and its cost
expression carries no terminal-count term.

*Falsifier:* convergence time or metabolic cost that scales with the number
of food sources at fixed arena size. That would put a candidate count back
into the expression and the substitution claim fails.

*Status:* the network result is established (Nakagaki 2000; Tero 2010). The
no-k-term claim is **arithmetic on the model, not a measurement**. No source
in the file reports convergence time across a terminal-count sweep at fixed
arena. This is the single most checkable gap in the folder.

---

**C2.** The exact Steiner-tree dynamic program carries a 3^k term, so at the
36 terminals of Tero 2010 an exhaustive method carries ~1.5 x 10^17
subproblem splits.

*Falsifier:* arithmetic error, or a materially cheaper exact algorithm for
the same problem class.

*Status:* reproducible from Dreyfus & Wagner 1971 and checked in
`--selftest`. Note this prices the *exact* DP; heuristics are far cheaper and
the comparison is not to them.

---

**C3.** A corvid recovering caches from memory replaces a search cost with a
storage cost, and the storage cost is paid across the whole interval whether
or not a given cache is recovered.

*Falsifier:* evidence that cache recovery is in fact driven by local search
cues — odour, disturbance, conspecific attention — with memory contributing
little. The transfer claim then collapses into ordinary foraging.

*Status:* memory-driven recovery is established for *Nucifraga columbiana*
(Vander Wall 1982) and *Aphelocoma californica* (Clayton & Dickinson 1998).
The bits-per-cache figure is **a stipulation for arithmetic, not a
measurement** — nothing in the sources licenses 64 bits, or any number, as
the neural cost of one cache.

---

**C4.** Observer-conditioned re-caching indicates a stored model of who could
see what, rather than a response to the competitor present at recovery.

*Falsifier:* re-caching that tracks current visual access rather than access
at the time of caching.

*Status:* supported for *Corvus corax* (Bugnyar & Heinrich 2005; Bugnyar,
Reber & Buckner 2016). Contested in interpretation — whether this is a model
of the observer or a learned contingency over cues is an open dispute in the
literature and this folder does not settle it.

---

**C5.** The platypus obtains prey range from the offset between electrical
and mechanical arrival times, and does so without constructing an
intermediate spatial representation.

*Falsifier:* a demonstrated ranging mechanism that does not use the offset,
or evidence of a topographic map being built and queried.

*Status:* **the weakest claim in the folder and it is a model, not a
result.** The bill's dual receptor arrangement is established (Scheich 1986;
Manger & Pettigrew 1995). Range-from-offset is Pettigrew's proposal (1999).
The "no intermediate representation" half is a stronger claim than the
sources support: cortical mapping of the bill has been described, and absence
of a representation is not something the cited work measured. Held as a
hypothesis.

---

**C6.** The arrival-offset arithmetic is correct: at 100 mm in fresh water
the offset is ~68 microseconds, and range recovers from offset by one
multiplication.

*Falsifier:* arithmetic error, or a sound speed materially different from
1480 m/s in the animal's foraging medium.

*Status:* reproducible and checked in `--selftest`. Independent of whether
C5's mechanism claim holds — the physics is right whether or not the animal
uses it.

---

**C7.** The four crossover figures locate where a method exceeds a 10^120
ceiling: 2^k at 399, 3^k at 252, N^2 at 10^60, N^3 at 10^40.

*Falsifier:* arithmetic error.

*Status:* reproducible from the printed terms and checked tightly in
`--selftest` — each crossover is verified as the first integer over the line,
with the one below it under. The ceiling itself is Lloyd 1999 and is used
only as a fixed reference, not as a claim about any organism here.

---

**C8.** An exponential appearing in a formalism reports on the formalism: it
says variables are being carried that the process is not using.

*Falsifier:* a case where the exponent is shown to be intrinsic — where the
physical state genuinely requires the carried variables and no change of
representation removes it. Volume-law entangled states are the standing
example, and they are why this claim is stated as a prompt rather than a law.

*Status:* not a result. It is the organising cut of the folder, and the three
cases are its demonstration rather than its proof.
