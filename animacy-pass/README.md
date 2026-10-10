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

- **The map is derived from physics by default.** The prerequisites are
  whatever the thing's mass and energy balance needs in order to close:
  what has to happen for the equation to take place. `TEMPLATES` is a seed
  set of balance templates, and each states its balance (for example,
  data center: electrical power in equals heat out, and the hardware has
  mass and a footprint). `derive_map` walks them recursively. A
  prerequisite with more than one physical route, such as electricity from
  heat, from falling water or from light, gets the route-independent
  requirement (a primary energy source), not one route picked for it. A
  prerequisite with no template of its own is a leaf. Run `--templates` to
  list the set.
- **A supplied map augments the derived one.** Use it for things whose
  balance cannot be closed from standard inputs, such as site-conditioned
  material or a worked process off the corpus. `"replace_derived": true`
  uses the supplied map alone. Every prerequisite shows whether its place
  in the map is `DERIVED`, `DECLARED` or `BOTH`. A thing with neither a
  template nor a supplied map returns `UNDECLARED`, never "fully accounted
  for".
- **Degree is computed.** Degree is the hop count from the thing along the
  declared edges, found breadth-first. Cycles are allowed.
- **Naming is a word match.** It searches with word boundaries over each
  name and its declared aliases. A paraphrase evades it, and a mention does
  not show the coupling is accounted for.
- **Verdict.** The verdict is `FIRST_DEGREE_UNSTATED` or
  `FIRST_DEGREE_NAMED`. Deeper degrees are reported per degree and never
  folded into the verdict. A degree with no prerequisites reads "none
  declared", not zero.

The four demo cases are CONSTRUCTED:

- A data-center claim derived purely from physics, with no map supplied.
  It names none of its nine prerequisites.
- The same thing with the couplings written in.
- A derived map augmented with a site-specific hydro chain.
- A thing with neither a template nor a map. See `samples/demo.sample.txt`. Nothing
here is a measurement of any real facility.

To run:

    python3 dependency_check.py --demo
    python3 dependency_check.py --templates
    python3 dependency_check.py CASE.json
    python3 dependency_check.py --selftest
