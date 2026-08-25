# scope-bound-shapes

**Marker under exploration.** Delivered spec: [`SPEC_SHAPES.md`](SPEC_SHAPES.md),
landed verbatim.

A **SHAPE** is a structural sequence that recurs across domains, defined by its
sequence and its selection rule, **not by its materials**. A **SCOPE BINDING**
is that shape instantiated with a declared list of FROZEN variables. Scoping
out is releasing entries from FROZEN — it is not a model swap. Domain names
(materials science, geology, cosmology) are scope bindings that acquired names,
and are not different subjects.

```
python3 scope.py       # shapes, bindings, compare() -> SCOPE COLLISION
python3 markers.py     # marker | stability | bindings_tested | exceptions
```

Both take `--selftest`. 29 / 19 checks, 48 in all, green. Samples pinned in
`samples/`, byte-reproducible.

## The CONSTRAINT forces a third state

FROZEN entries are declared by the builder, never inferred — an inferred FROZEN
list would be the tool asserting scope it did not measure. Take that seriously
and a variable is **LIVE**, **FROZEN**, or **UNDECLARED**. The worked example
has two of the third kind:

| variable | slab_concrete | metamorphic_rock |
| --- | --- | --- |
| T range | FROZEN | LIVE |
| aggregate | LIVE | **UNDECLARED** |
| chemistry | FROZEN | LIVE |
| creep | FROZEN | LIVE |
| cure age | LIVE | FROZEN |
| lithostatic load | FROZEN | LIVE |
| moisture gradient | LIVE | **UNDECLARED** |
| restraint | LIVE | LIVE |

The arithmetic to remove UNDECLARED is right there — `frozen := universe − live`
— it completes the table, and it is exactly the inference the constraint
forbids. `infer_frozen()` exists **only to refuse**, and prints what it would
have returned so the refusal is inspectable rather than merely asserted.
UNDECLARED is not FROZEN: one is a claim the builder made, the other is a claim
nobody made.

## The worked example collides totally, in both directions

`compare(slab_concrete, metamorphic_rock)` → **SCOPE_COLLISION**, 5 variables.

- frozen in slab, live in metamorphic: **4 of 4** — T range, chemistry, creep,
  lithostatic load
- frozen in metamorphic, live in slab: **1 of 1** — cure age

Every frozen variable in each binding is live in the other. **There is nothing
these two bindings both hold still.** One variable — `restraint` — is live in
both, and that is the entire overlap.

So the spec's consequence applies at full strength: two modules claiming this
shape at these two bindings are not corroborating each other. That is a
statement about what their agreement is worth. It is **not** a contradiction
and not a defect in either binding — bindings that collide are holding
different things still, which is coverage rather than confirmation. The module
reports the collision and does not grade it.

**"No collision" is not "corroborates."** `compare()` returns
`corroborate=False` on a collision and `None` otherwise — never `True`. Absence
of conflict between two declared lists is not evidence that two bindings test
the shape independently.

## Scoping out is not a model swap, and does not reach compatible

| | verdict | collisions |
| --- | --- | --- |
| as delivered | SCOPE_COLLISION | 5 |
| slab releases its frozen | SCOPE_COLLISION | 1 |
| both release their frozen | UNDECLARED_OVERLAP | **0** |

Same shape and same selection rule throughout — only the live set widened.
Releasing **every** declared FROZEN entry on both sides drives collisions to
zero and still does not reach `COMPATIBLE`: `aggregate` and `moisture gradient`
stay UNDECLARED in `metamorphic_rock`, and only the builder can declare them.
The constraint bites exactly where it should.

## The marker table, and why every row is UNTESTED

`marker | stability | bindings_tested | known_exceptions`, with the spec's rule
enforced in **two** places, not stated once: `set_stability()` guards the write,
and `row()` guards the read — a stability value written straight past the first
guard is still refused on its way to a reader.

| marker | stability | bind | exceptions |
| --- | --- | --- | --- |
| strain accumulation is observable | None | 0 | NOT_LOOKED |
| a limit is crossed rather than approached | None | 0 | NOT_LOOKED |
| release is localised to one path | None | 0 | NOT_LOOKED |
| the release path is the weakest available path | None | 0 | NOT_LOOKED |

The delivered material gives a shape, a selection rule and two bindings, and
**no test record**. So the markers are the ones the shape itself names, and
every one carries `stability=None`, `bindings_tested=[]`, `state=UNTESTED`.
That is the honest state of the table on delivery, not a placeholder for
whoever reads it next.

**Zero known exceptions with zero bindings tested is `NOT_LOOKED`, not
`NONE_FOUND`.** An empty exception list reads as a clean record and here it is
an empty record. Every row carries an explicit exceptions state so the
distinction never rests on the emptiness of a list.

**One binding is where a marker was found, not where it was tested** — the
shape is defined across domains, so `MIN_BINDINGS_FOR_STABILITY` is 2. That
floor is arbitrary, and worse: the only two bindings delivered **collide
totally**, so even a two-binding stability claim over them would sit on a pair
`scope.py` says are not corroborating each other. The floor is met and the
claim is still not what it looks like.

## What is not established

- **The shape is taken on the spec's word.** Whether strain accumulation in
  curing concrete and in metamorphic rock really are one sequence with one
  selection rule is a claim about the world. This assumes it in order to
  compute over it; if the shape is wrong, every collision reported here is a
  collision between two bindings of a shape that does not exist.
- **The markers are derived from the shape, which is the only source available
  and is also circular.** A marker built by restating a sequence step cannot
  fail to indicate the shape when the shape holds. What it can do is fail to be
  observable or fail to discriminate, and neither has been checked anywhere.
- **The double guard can still be walked around.** A caller setting
  `.stability` and `.bindings_tested` together, with nothing behind either,
  passes both. The table checks that the columns move together, not that the
  bindings were really tested.
- **Two bindings is not a list of bindings.** `compare()` is pairwise. Nothing
  here says what a shape with nine bindings looks like, or whether collisions
  across such a set partition into groups that could corroborate within
  themselves.

CC0. Standard library only. Parses under Python 3.9. Phone-buildable.
