# unowned-join

WO-4, delivered verbatim in `WORK_ORDER.md` and built to. The order's object
is a shape it declines to name: a set of failures currently treated as
unrelated domain problems, each with every component locally correct and the
join between them owned by nobody. Seven faces, three of which point at
orders already landed in this tree.

**CONSTRUCTED.** Every structure in the folder is a declared reading written
here. Nothing is a measurement of any container, rule, report, accounting
boundary, channel, organism or institution.

**No term is coined.** The order registers the naming gap as part of the
deliverable and says so in as many words: *"NOT COINED HERE. A term arriving
before a working instrument has no receiving frame, and a name carrying less
than the whole structure would be worse than the gap."* That instruction is
in the code rather than in a comment: `invariant.coin()` raises
`TermCoinageRefused`. The phrase *unowned join* is the order's own title and
is used as a description, not adopted as a term (`[CHOICE 3]`).

## What is built

`invariant.py` is the order's step 1 — *"Attempt a formal statement of the
invariant ... If it can be stated formally, it can be checked."*

    A1  n >= 2 components
    A2  each component is correct within its DECLARED scope S(k)
    A3  the join J is non-empty
    A4  for every k:  NOT (J subset of S(k))
    =>  no check confined to a single S(k) can decide the property on J.

Five verdicts, all reachable, three of them negative — `OWNED`,
`UNOWNED_BY_UNION`, `UNOWNED`, `LOCAL_FAULT`, `NOT_EVALUABLE`.

`faces.py` parses the seven faces out of the delivered order at call time,
puts each through the invariant as a declared structure with the order's own
line as its basis, resolves the three companion work orders by folder path
plus a content marker, and reports the term gap as a state.

## Results

**The statement is short and its inference is immediate.** Once A1–A4 are
written down the conclusion follows in one line. That is the result of
attempting step 1, not a failure of it: the difficulty is not the inference,
it is that A4 is only checkable when every S(k) has been declared, and
nothing in the failures the order lists declares S(k) anywhere.

**Two unowned states, not one.** A join covered by the *union* of scopes and
one covered by nobody are different situations calling for different repairs
— the first is an aggregation that is nobody's job, the second an observable
nobody holds at all. Face 3 (quiet failure) is the first; faces 1, 2, 4, 5
and 7 are the second.

**Face 6 comes back `NOT_EVALUABLE`, for the order's own reason.** The frog
is the one face the order marks UNRESOLVED. Declared per `[CHOICE 7]` on the
order's own sentence — *"You cannot list in advance which binaries will turn
out false, because that is precisely what the environment supplies"* — the
environment's scope is undeclarable in advance, so A4 is not checkable and
the invariant returns no verdict. The formal statement locates the same
face the order could not resolve, and locates it in the same place.

**The strong form of the term claim is refuted here.** The order states
*"Because there is no good word, NO PROCEDURES CAN BE MADE AROUND IT AND NO
CODE CAN BE MADE AROUND IT,"* and its scope limits restate it: *"No term is
coined, so this instrument cannot yet be implemented."* This folder
implements it — a checkable predicate over the structure, five reachable
verdicts, no term coined. The scope of that refutation is one structure and
one folder. What survives is narrower and is the order's own mechanism two
sections on: with a term a claim is a REPORT and status is inherited;
without one the same content is rebuilt across several sentences and reads
as a PROPOSAL. **Code needs a predicate; transmission needs a name.** Those
are different requirements and the order merges them.

## What is not run

- **Step 2, adversarial face-finding** — `NOT_RUN`. It takes a second party,
  and this session holds the seven faces. A face produced here would be the
  same hand widening its own set. The order calls this the cheapest test in
  the set and it still is.
- **Step 3, the cross-language term search** — `NOT_RUN`, `UNSEARCHED`, zero
  languages scored. The sources are not reachable from this environment and
  no vocabulary is scored from memory. The order's expected status is
  `named_elsewhere` rather than `unnamed`, and nothing here moves it.
- **Step 4** is conditional on 1 or 3 and is not reached.
- The transmission mechanism above is the order's, carried and **not tested
  here** — it would take raters reading matched content in two forms.

The fit of six faces of seven is **not evidence for the invariant**: the
invariant was abstracted from those same seven. The render says so above the
counts.

## Running

    python3 unowned-join/invariant.py        # the predicate, five controls
    python3 unowned-join/faces.py            # the faces, the term gap
    python3 unowned-join/invariant.py --choices
    python3 unowned-join/test_unowned.py     # the checks; prints the count

Both modules refuse `--selftest`. `join_coverage` is registered in
`tools/known_answer.py`. Stdlib only, parses under 3.9, phone-buildable,
CC0.
