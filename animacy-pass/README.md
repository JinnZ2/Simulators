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

## unweld.py -- welded evaluative claims

"Cheaper", "efficient", "optimal", "productive", "better", "scalable" and
"clean" are **welded claims**. Each is one word fusing several buried
terms, asserted as if it were one physical fact. The proof that they are
not physical is that the identical process spending identical matter and
energy can be called "expensive" by one company and "cheap" by another.
The label is a property of the framing, so it has to be grounded to a
common variable before it stands.

For each welded term found in a claim, the check lists the buried terms
it must declare. For "cheaper" these are for whom, in what unit, over what
boundary, over what time, counting which inputs and which outputs, and
compared to what. It reports which of those the claim's declarations fill
and which are blank. For the named process it builds the **full balance**:
every prerequisite `dependency_check` derives, plus the outputs the
process has to put somewhere (a seed set). Anything in the full balance
that the stated boundary leaves out is a candidate externality, the cost
the word pushed outside its frame.

The verdicts:

- `GROUNDED` means every buried term is declared and the full balance
  falls inside the boundary.
- `UNGROUNDED` means a buried term is blank, or a balance item lies
  outside the boundary.
- `UNDETERMINED_NO_BALANCE` means the terms are declared but there is no
  balance to check them against. This is never read as `GROUNDED`.
- `NO_WELDED_TERM` means there was nothing to unweld.

`GROUNDED` says the declarations are complete and the boundary covers the
balance. It does not say the label is true.

The demo runs one data center under two framings, with the same 1.2 GWh a
year and the same 11-item balance. Framing A counts electricity and land
and calls it **cheap**: `UNGROUNDED`, with nine items outside. Framing B
counts all eleven and calls it **expensive**: `GROUNDED`. The comparison
returns `LABEL_FLIPS_PHYSICS_IDENTICAL`.

**Standing challenge (the operator's).** If something can be found that
is unanimously cheaper, more efficient or optimal across every framing,
staying grounded and keeping one label wherever the boundary is drawn,
the term earns its use. `unanimous()` is that test. It returns `EARNED`
only when every framing supplied is `GROUNDED` and they all carry the same
label.

**Limit.** A filled buried term is a declaration. The tool checks for
blanks and for balance items outside the boundary. It does not adjudicate
the real-world numbers. It matches boundary items to balance items by name
or alias, so a different word for the same input is reported as outside.
The demo cases are CONSTRUCTED. See `samples/unweld.sample.txt`.

    python3 unweld.py --demo
    python3 unweld.py --terms
    python3 unweld.py CASE.json
    python3 unweld.py --selftest
