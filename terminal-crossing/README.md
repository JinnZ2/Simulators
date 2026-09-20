# terminal-crossing

WO-3, delivered verbatim in `WORK_ORDER.md` and built to. The measurand is
whether any system is TERMINAL — no dependents, no crossings — because the
exemption from engineering standards rests on such systems existing, and
if none exist the exemption has no domain.

Two instruments. `audit.py` is step 1, the attack on the falsifier plus a
reading of the order's three failed candidates. `crossing_rate.py` is step
2, the metric the order's own conversion asks for: not *is it terminal* but
**what is the crossing rate, and over what horizon**.

Steps 3 and 4 are NOT RUN. Step 3 needs one organisation's decision record
and step 4 is a literature search; neither is reachable from here, and
nothing is substituted for either.

## Scope

Every rate, count and horizon in this folder is **CONSTRUCTED** and labelled
so at its declaration. Nothing here is a measurement, and nothing is a
statement about any geological repository, any spacecraft or any black hole
— the three asymptotes are carried from the order as the shapes it names,
with numbers invented so the metric has something to discriminate.

## The six conditions are parsed, not retyped

`conditions()` locates the order's `### Conditions` section by content and
reads its bullets at call time; the channel id is the first word after
`no ` in each, so the vocabulary is derived rather than assigned
(`[CHOICE 2]`). A test asserts no bullet appears as a literal anywhere in
the module. The proposed seventh medium lives in its own constant and is
never merged into the six (`[CHOICE 5]`), because a candidate medium and a
delivered condition are different objects.

## What the metric returns

A system carries a horizon and six channels. A channel is `PRESENT`,
`ABSENT_MEASURED` or `UNSEARCHED`, and an undeclared channel is filled as
`UNSEARCHED` and never as a measured absence (`[CHOICE 1]`) — a silence and
a measured zero are different states, and the verdict reads
`NOT_ESTABLISHED` rather than `TERMINAL` while any channel is silent.

`expected_crossings` returns `None` for an absent rate, an unknown unit, an
absent horizon and the `UNBOUNDED` sentinel, and `0.0` for a rate measured
at zero (`[CHOICE 3]`). `crossing_total` carries a value on `COMPUTED` and
`None` on every other state, so `UNBOUNDED_HORIZON` is a state and not a
large number.

## Results

The three asymptotes return three distinct arithmetic shapes and **none
returns a total of zero** — the order's *"No instance found. Only
asymptotes"* as arithmetic rather than as prose. `TERMINAL` is reachable, on
a constructed control whose six channels are all `ABSENT_MEASURED`, so the
verdict is not `CONSTANT_FIRES`; that is reachability and not existence, and
the control is constructed for exactly that purpose.

The attack on the falsifier lands: gravitational coupling is named by none
of the six conditions and is closed by no expenditure, so the falsifier
would be **UNSATISFIABLE** rather than merely **UNSATISFIED** — a different
epistemic object, since no search closes it. Whether it counts as a crossing
under the order's own usage is carried `UNRESOLVED` with both readings
stated and neither taken.

The order's three failed candidates carry three mechanisms over **two**
channels, both the A/B test and the air gap landing on `operator`; and three
of the six conditions — `physical`, `shared`, `maintenance` — are exercised
by no delivered candidate.

## Running

    python3 crossing_rate.py          # the metric over the corpus
    python3 audit.py                  # step 1 and the candidate reading
    python3 <module>.py --choices     # the declared choices
    python3 test_terminal.py          # the checks; prints its own count

Both modules refuse `--selftest` and name the test file. Stdlib only, no
network, parses under Python 3.9, ASCII, phone-buildable. CC0.
