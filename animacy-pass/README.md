# animacy-pass

The animacy pass from the operator's five-pass method, in its quick form: a
**dependency check**. For the thing a claim names, what matter or energy is
a prerequisite for it?

Animacy here is **degree of coupling**, not alive/dead. A first-degree
prerequisite is one the thing cannot exist or run without. A second-degree
prerequisite is a prerequisite of that one, and so on along the chain. The
leak it catches is a claim that writes a coupled thing as if it stood
alone, at museum-glass distance, while it rests on first-degree matter and
energy the claim never names.

`dependency_check.py` is stdlib only and CC0.

- **The map is declared.** The prerequisite map comes from whoever knows
  the ground, and the tool invents none. A claim with no map returns
  `UNDECLARED`, never "fully accounted for".
- **Degree is computed.** Degree is the hop count from the thing along the
  declared edges, found breadth-first. Cycles are allowed.
- **Naming is a word match.** It searches with word boundaries over each
  name and its declared aliases. A paraphrase evades it, and a mention does
  not show the coupling is accounted for.
- **Verdict.** The verdict is `FIRST_DEGREE_UNSTATED` or
  `FIRST_DEGREE_NAMED`. Deeper degrees are reported per degree and never
  folded into the verdict. A degree with no prerequisites reads "none
  declared", not zero.

The three demo cases are CONSTRUCTED: a data-center claim that names none
of its eight declared prerequisites, the same thing with the couplings
written in, and a claim with no map. See `samples/demo.sample.txt`. Nothing
here is a measurement of any real facility.

To run:

    python3 dependency_check.py --demo
    python3 dependency_check.py CASE.json
    python3 dependency_check.py --selftest
