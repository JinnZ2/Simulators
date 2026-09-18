# failure-mode-register

A mechanism-level failure-mode register for ML components used as
infrastructure, built to `WORK_ORDER.md` (delivered verbatim beside this file).

**Scope, from the order's section 0, restated so it is not read past:**

> DURABILITY AND RECONSTRUCTABILITY ONLY: can the deployed object still be
> identified, re-produced, load-rated and inspected at t + N years, by someone
> who is not the original author and does not hold the tacit stack.

Not model behaviour, alignment, or misuse. Not harm incidents. Not a code of
ethics. Nothing here rates a model, a vendor, a deployment or a person: every
verdict is about whether a RECORD is sufficient to rebuild or identify an
object.

```
WORK_ORDER.md            delivered, verbatim, the single source of truth
      |
      |  parsed at call time -- nothing retyped
      v
  entries.py             12 schema fields, 3 vocabularies, 4 ENTRY blocks,
                         3 control notes, 5 seeds, 6 domains, 8 steps,
                         9 falsifiers, 2 fenced tables
      |
      v
  register.py            filing -> conformance -> control-state axis
                         -> steps 0..7 -> falsifiers -> 6B arithmetic
      |                        |
      |                        +-- imports effective-redundancy-audit::n_eff
      v
  test_register.py       every expected verdict lives here and nowhere else
```

## Run

```
python3 entries.py           what parsed out of WORK_ORDER.md
python3 register.py          the register and every computation over it
python3 test_register.py     the checks (count printed by the run)

python3 entries_v2.py        what parsed out of WORK_ORDER_V2.md
python3 register_v2.py       the revised order, audited
python3 register_v2.py --choices
python3 test_register_v2.py  the v2 checks (count printed by the run)

python3 entries_v3.py        what parsed out of WORK_ORDER_V3.md
python3 register_v3.py       the third order, audited
python3 register_v3.py --choices
python3 test_register_v3.py  the v3 checks (count printed by the run)
```

Stdlib only. No pytest, no network, parses under 3.9, phone-buildable. CC0.

## The revised order

`WORK_ORDER_V2.md` is delivered verbatim **beside** `WORK_ORDER.md`, not
over it, so both stay inspectable — the supersession convention this
repository already uses (`observer-exclusion/SPEC_V2`,
`design-basis-ai/SOURCE_DROP_V2`, `fold-matrix/WORK_ORDER_V2`,
`mining-increment/SOURCE_DROP_V2`). `entries.py` and `register.py` are
unchanged; `entries_v2.py` **imports** the v1 gutter parser rather than
copying it, so one parser reads two documents.

```
v1  524 lines                v2  1218 lines
    inserted  694
    deleted     0
    replaced    0            -> purely additive, measured with difflib
    adds F_K, F_M, F_L, F_J; every v1 falsifier body verbatim
```

Four results, each computed from the delivered text:

```
F3 names 2 wins, the amended map gives 4      V9 argued away in F2 by name
                                              V5 by nothing stated      FMR_027
                                              and V5 is where A-01's own
                                              correction was not applied FMR_028

F_L states a DIRECTION and it is backwards    survival is non-decreasing
                                              in correlation, so failure is
                                              non-increasing: 0.52 -> 0.10
                                              A-07 states the same correction
                                              without a direction and is
                                              right                     FMR_029

F_M empties the set delivered with it         0 of 5 carrier-side conditions
                                              state a measurable rate;
                                              active set EMPTY          FMR_031

F_K cannot be applied at all                  0 of 7 conditions carry a
                                              lifetime; the retention horizon
                                              is named 4x and never valued
                                                                        FMR_030
```

The conjunction model exists to check `F_L`'s **direction** and nothing
else. `F_L`'s own last line is *do not put a number on it*, and none of
these numbers attaches to any firm, product, arrangement or person; no
function takes an entity as an argument.

## The content is the order's; the computations are this build's

The register holds four entries — `DUR-001` retained reference sample,
`DUR-002` stamped validity envelope, `DUR-003` migration attrition, `DUR-004`
stranded under load — and every one of them was delivered in the order.
**Nothing is authored here.** `entries.py` is a parser and carries no entry
value as a literal, asserted; an edit to the order that the parser cannot
follow turns the suite red rather than passing against a stale copy
(`MF_019`: five stale copies of one gate across three drops, none noticed).

Three things the order asks for are **not** written:

- **ENTRY 0.** Named in section 1, never delivered, and not constructible under
  the section 2 schema — its mechanism is a property of the register rather
  than of a deployment, so it has no `load_condition` and its
  `detection_channel` is the field itself (`FMR_012`).
- **Section 3C.** Step 4 says populate it and flag every entry PROJECTED.
  Authoring projected entries from inside is exactly what `F_D` names, and the
  order's own fraction rule caps them at one on a register this short
  (`FMR_009`).
- **A correlation entry.** Section 6B-2 says correlation *"needs its own
  entry"*; none was delivered and none is invented (`FMR_017`).

## Three things that cannot run here, each named rather than approximated

| what | why | where |
|---|---|---|
| Step 0 / `F_B` prior-art check | egress is an allowlist; every catalogue host refuses CONNECT | `step0_prior_art()` |
| `F_G` outside reader | no second reader, and `F_G` asks for five entries where four were delivered | `_f_g()` |
| `F_E` what would make it binding | a claim about the world, not a computation | `_f_e()` |

`FMR_001` is the load-bearing one: `F_B` says the absence of prior art *"must
be established, not assumed"*, so **the register is not cleared to ship from
here** regardless of what else computes.

## What the computations found

Full record in [`CLAIM_TABLE.md`](CLAIM_TABLE.md) (`FMR_001..FMR_025`). The
ones that need no reading:

- **Step 1 was never run.** No deployment class is declared anywhere, and
  `DUR-002` refuses to narrow explicitly (*"In practice: all of them"*). Step 5
  and section 5 both rest on it.
- **Step 5's headline is computable for 1 entry of 4.** Two cells state two
  reconstruction values and one states none of the three. And the two
  multi-value cells are **not one axis** — `DUR-001` is control-state,
  `DUR-003` is time — so no merged distribution is emitted.
- **The register is two registers superimposed.** Six of twelve cells across
  three fields carry both the state of current practice and the state under a
  control the same entry proposes, with no axis in the schema for the
  difference. The high-priority set is 3 of 4 under one reading and 0 of 4
  under the other; neither is picked.
- **One priority transport is gated out of its own requirement set.**
  `DUR-002` scores `existing_control = PARTIAL` on purpose; Step 6 gates on
  `NONE`, so it produces no requirement under a literal reading while its own
  text specifies one.
- **`DUR-004` carries MEASURED's label** with neither MEASURED's cite nor
  TRANSPORTED's justification, and says *"by analogy"* — the word the TRANSPORT
  RULE rejects. The mechanical vocabulary check passes it, which is that
  check's own limit shown rather than described.
- **"Compressed by roughly fifty"** is the low end of the order's own band
  (50 to 125) and the equal-N reading.

And one finding against this build rather than the order: the first version of
the `F_A` screen **struck `DUR-001` on the sentence in which `DUR-001`
disclaims resemblance** (`FMR_015`). Repaired; a resemblance mention is now
reported with its surrounding clause and never subtracted, and `F_A`'s `limit`
field carries the record.

## Enforced rather than promised

- **`F_H`, the event boundary.** *"Define the event boundary before any count
  appears anywhere in the deliverable."* Every function returning a count
  returns it in a dict carrying a `unit` naming what is counted; a check walks
  all sixteen of them.
- **The redundancy rule imports.** Section 6B-2's REGISTER RULE is
  `effective-redundancy-audit`'s `n_eff` and is imported, not restated. It
  fires on nothing in the delivered register — a visible zero, shown reachable
  in both directions on constructed claims.
- **Three states where two would collapse.** Missing field vs extra field;
  CONFORMS vs MULTI_VALUE vs OUT_OF_VOCAB; declared budget vs declared absence
  vs UNDECLARED; RESOLVED vs AMBIGUOUS with no pick.
- **The render screens** through `sheet-structure-scan/no_severity`, under one
  declared exemption for two sentences quoted verbatim from the order, measured
  in three arms rather than taken on trust.

Eight `[CHOICE n]` markers, each printed by `--choices` and each cited inline
where it takes effect; both asserted.

## Cross-references

| marker | status | resolves to |
|---|---|---|
| correlated failure at scale (6B-2) | RESOLVED | `effective-redundancy-audit`, `design-basis-ai` |
| silent substitution (section 5) | AMBIGUOUS | `model-provenance`, `criteria-drift`, `machine-record-format` — **no pick made** |

`fraction_cap` is registered in `tools/known_answer.py` with four
distinct-valued cases. No other function here is registered, and the reason is
stated rather than left as a silent absence: every other return is a declared
vocabulary member, a record, or a product whose known answer is its own
definition.

## The value-and-source gate

`FMR_040..FMR_043`. The three defects at `FMR_036` are one defect: each
produced a value whose stated source does not support it, and none was found
by reading. The repair is a shared primitive, `tools/sourced.py`, not three
patches.

```
Sourced(value, source_text, locator, span=... | derivation=...)

    gate(x) -> x                    three fields, mutually consistent
            -> Unrated(reason)      otherwise: not zero, not clean,
                                    not a default
```

Containment of the value in the source is the obvious rule and it is **not
sufficient**:

```
V3   cell "-> --   A-01"   buggy value "+"   not contained   -> caught
V6   cell "-> --   A-02"   buggy value "-"   IS contained    -> missed
                                             (the arrow's hyphen)
```

So the primitive is a **span**, verified by slicing, and the buggy path has
none — it never located the value in the cell it names as its source. A
computed value declares a `derivation` instead; exactly one of the two.

Replayed in `test_register_v2.py` section 17: the amended score slices its
cell, `(see DUR-006)` and `exceeds ~1` refuse with
`no_unit_adjacent_to_numeral`, and `tools/known_answer.py` asserts
`EXPECTED_METRICS` against the registry at end of run — which is what catches
a `register(...)` shadowed by a `finally`, since a count taken from the calls
cannot see a call that did not execute.

**A fourth defect, found by the gate.** One row of fourteen in the
loss-variable map runs its ML cell past column 57, so the fixed-width slice
cuts a token — ML truncated at `data st`, amendment column reading
`ate, hw)`. No score moves; the truncated cell begins with the same sign run.
What is false is the LOCATOR, which is the class an output check cannot see.

## What this is not evidence about

`FMR_025`. No deployed component inspected, no retained record examined, no
reconstruction attempted. Every computation is a property of the four delivered
entries, of the order's own rules, or of this build's arithmetic.

## The third order

`WORK_ORDER_V3.md` lands verbatim beside the other two — three orders, none
overwritten. `entries_v3.py` defines no parser of its own: the gutter parser
and fence walker come from `entries.py`, and the gated score map, the
column-boundary report and the F3 reader come from `entries_v2.py`, which was
**generalised to take a document rather than copied**. One parser, three
documents.

```
WORK_ORDER.md    WORK_ORDER_V2.md    WORK_ORDER_V3.md
      |                 |                   |
      +--------- entries.py ----------------+    gutter, fences, fields
                       |
                 entries_v2.py                   cell parsers, gated map,
                       |                         boundary report, F3 reader
                 entries_v3.py                   section walk only
                       |
                 register_v3.py                  the audit
                       |
              test_register_v3.py                every expected verdict
```

**v2 against v1 was a pure insertion. v3 is a rewrite** — 338 equal lines of
1218 and 1104, similarity 0.2911 — and it is **shorter than v2 while carrying
three sections v2 does not have**. Prose was compressed.

### What moved

```
Step 0     BLOCKED -> reported DONE, with a four-artifact table and a
           named result. FMR_001's blocker is removed BY THE ORDER'S OWN
           REPORT, and arxiv.org refuses CONNECT from here, so the closure
           is by declaration -- which the order says itself: "Verify
           before citing."

the id     moved out of the entry fence and into the `### DUR-00n`
           heading, so every block carries 11 of 12 schema fields and the
           order's own UNRATED PART rule fires on 6 of 6 entries against a
           format change. v2's undeclared NOTE field is gone.

section 6  is new: THE PARSER GATE, this session's own repair delivered
           back as a control inside the order it repairs.
```

### What did not move

```
F3 names two wins; the amended map computes four. V9 is argued away by
F2 by name and V5 by nothing.                                    FMR_046
one score row still runs its ML cell past the amendment column.  FMR_047
F_L still states a direction, and it is still backwards.         FMR_053
0 of 7 ambient conditions state a lifetime; 0 of 5 carrier-side
conditions state a rate, so F_M's active set is empty.           FMR_054
Step 1 is still not run: two deployment classes, neither picked.  FMR_045
```

### Section 6, restated one field short

The order states THREE fields on every extracted value — the value, the
literal source text, the locator — and `tools/sourced.py` refuses on a
fourth, the **span**. `span` and `offset` appear zero times in section 6.
The demonstration reads the same two rows three ways:

```
row  amendment cell   buggy  true   containment  searched span   produced span
V3   '-> --   A-01'   '+'    '--'   refuses      refuses         no_provenance
V6   '-> --   A-02'   '-'    '--'   passes       passes at (0,1) no_provenance
```

Containment is what the three fields buy, and it misses V6, where the buggy
value occurs in its own cell through the hyphen of the arrow. A span
*searched for afterwards* misses it too, and points at offset 0 — the arrow —
where the score sits at offset 3. What refuses both is a span **produced by
the extraction**, and section 6 names neither the span nor where it has to
come from.

### A second boundary cut, in new material

`FMR_042` recurs on the same score row, and §0-1's prior-art table — added in
v3 — carries the same shape: one line cuts on both sides of the column
boundary, truncating a cross-reference at `see DUR-` and prefixing its
neighbour with `005`. Found by the same check, on material written after the
check existed.

---

## The fourth order

`WORK_ORDER_V4.md` landed verbatim beside the other three — four orders,
none overwritten. `entries_v4.py` defines no parser of its own: the
gutter parser and the fence walker come from `entries.py`, the
boundary reader from `entries_v2.py`, **generalised to take a column
layout rather than copied**, because v4 rewrote the V-map into five
columns with word score tokens. One parser, four documents.
`register_v4.py` takes its falsifier arithmetic from `register_v2.py` the
same way. Claims `FMR_057..FMR_069`.

```
  python3 entries_v4.py            what the order carries
  python3 register_v4.py           the audit
  python3 register_v4.py --choices every open choice, both modules
  python3 test_register_v4.py      the checks, with the count
```

### What moved, and what did not

```
FMR_058  the prior-art gate REOPENS. v3 read DONE; v4 reads RUN with the
         report NOT_VERIFIABLE_HERE and the ship blocker back. FMR_001 is
         OPEN again by the order's own declaration.
FMR_060  F3 restated as four PROT with one disposed and one claimed --
         and V5 is still undisposed. The restatement reproduces from the
         table; the gap it names does not close.
FMR_064  F_N passes. v3 6 of 6 UNRATED PARTS, v4 0 of 6, computed on both
         documents with the same rule.
FMR_067  F_L prohibits a sign now as well as a number, and A-17 retains
         the statement it withdrew.
FMR_068  the active ambient set is EMPTY, recounted: 0 of 7 lifetimes,
         0 of 5 rates.
```

### D-06's mechanical check

`D-06` asks for *a mechanical check in the harness, not a rule in the
text*. `format_rule_scan` walks **every** fixed-width table in the whole
document, because the recurrence `D-06` records was in a table the V-map
check did not look at. Run on all three documents that carry the rule or
its defect:

```
       tables  cuts  glyphs  col0 wraps
  v2      2      0      1        3
  v3      3      2      5        3      <- both cuts on line 50,
  v4      5      0      1        3         the prior-art table
```

Both v3 cuts land on the prior-art table, truncating a cross-reference at
`see DUR-` and prefixing its neighbour with `005`. v4 has none. What is
in **every** version is §5-1's rate table: a hyphenated line wrap inside
a rate cell, and three rows whose first column is filled while the rest
are blank — a wrap and a one-cell row written the same way. Three
revisions, never repaired, because the rule was in prose and the only
check looked at the V-map. That is `D-06`'s own sentence with a
denominator under it.

The scan reads a table at **three or more columns** and not two, because
a two-column fixed-width block is the same shape as a gutter block. The
cost is stated rather than tuned away, and it is paid immediately:
F3's own restatement block reads `UNDISPOSED   V5   -> D-04`, an arrow in
a status cell one section after §1 applies the rule against one, and the
scan cannot see it. Reported by name (`FMR_061`) with the blind spot
beside it.

### §6's fourth requirement

`A-18` is this session's own `FMR_049` delivered back as a control. The
three fields buy containment and not provenance; a post-hoc span
satisfies all three; the discriminator is the offset. Tested by
constructing both spans on the row the defect was first found on:

```
cell                      '-> --   A-02'
searched span             (0, 1)   offset 0     passes the gate
span emitted by the read  (3, 5)   offset 3     passes the gate
```

The stated failure signature reproduces exactly — and the gate passes
both, because provenance is a property of the **constructor** and the
gate sees fields. `tools/sourced.py` already ships both constructors;
what it does not do is refuse the searched one, and no check of three
fields can. `entries_v4` calls `find_span` nowhere and `slice_sourced`
everywhere, which is the requirement met at the layer that can meet it.

### `note` is declared now. `name` is not.

`A-15` declares `note` optional, closing `FMR_013`. The class does not
close: `name` is carried by 6 of 6 entries and appears in no schema —
same shape, one field over, in the revision that names it. It fires no
rule, correctly, because the UNRATED PART rule is about absence.
