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
python3 entries.py          what parsed out of the order
python3 register.py         the register and every computation over it
python3 test_register.py    the checks (count printed by the run)
```

Stdlib only. No pytest, no network, parses under 3.9, phone-buildable. CC0.

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

## What this is not evidence about

`FMR_025`. No deployed component inspected, no retained record examined, no
reconstruction attempted. Every computation is a property of the four delivered
entries, of the order's own rules, or of this build's arithmetic.
