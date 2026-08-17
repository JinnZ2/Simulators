# AUDIT_NOTES — domain-ledger

Added, not delivered. [`ledger.py`](ledger.py) is the drop as received and
is not modified.

    python3 ledger.py --selftest
    python3 ledger_audit.py

## What the drop is

One file. A ledger that makes a confidence readout **derived instead of
asserted**, by recording the domain set a coverage number was taken over.

Four readouts, deliberately not combined: **coverage** (domains where the
shape held / domains read), **cycle depth** (holds that survived a return
/ holds), **adversarial** (domains where the shape was pushed against /
domains read), **truncated** (reads cut short at a discomfort threshold /
domains read). Plus a **reservation** — a standing fraction held as
unknown.

Selftest passes 13/13.

## File status

| file | status |
|------|--------|
| `ledger.py` | delivered, verbatim |
| `shapes/` | not delivered — no shape has been recorded |
| `README.md`, `CLAIM_TABLE.md` | not delivered |
| `ledger_audit.py` | added |
| `AUDIT_NOTES.md` | added |
| `samples/` | added |

Nothing here invents a shape. A shape is data — a claim someone holds and
the domains they read it against — and inventing one would put a position
in the author's mouth.

## Claims

| id | claim | falsified by | status |
|----|-------|--------------|--------|
| DL_001 | The load-bearing idea — a coverage number is not portable without its denominator — is `CD_008`/`ANC_006` restated for a confidence readout, and the tool follows it: four readouts returned separately with their denominators named in the output | a reading on which the four are combinable | SUPPORTED (holds) |
| DL_002 | The reservation is defined as capping reported headroom and nothing applies it: `ceiling` is computed, returned, printed, and read by nothing; coverage may exceed it with no readout saying so | a headroom field, or a flag when coverage exceeds the ceiling | SUPPORTED |
| DL_003 | `coverage` puts `mixed` in the denominator and not the numerator, so all-break and all-mixed both return 0.00 | a footer clause naming what the denominator includes, or a separate ratio | SUPPORTED |
| DL_004 | `detail()` reads `criterion_fixed_in_advance` and `open`; `SKELETON` carries neither, so `--new` never prompts for the pre-registration guard — `CW_015` repeated in a second folder | either field entering `SKELETON` | SUPPORTED |
| DL_005 | With no `shapes/` directory the tool prints a well-formed report with zero rows and exits 0, where all three sibling scorers refuse on stderr with rc 1 | the empty state refusing, or saying it is empty | SUPPORTED |

## 1 — DL_001, the idea and two choices that follow

> A coverage number is not portable without its denominator. 61 percent
> over one domain set is a different quantity than 61 percent over
> another. This records the set.

`criteria-drift` `CD_008` and `anchor-interval` `ANC_006` for a confidence
readout instead of a benchmark: a number is identified only up to the
reference it was taken against, so publish the reference.

**Four readouts, not combined.** The docstring states why — *"Coverage and
cycle depth are different currencies. A shape can be wide and shallow"* —
and `score()` returns them separately. Every other scorer in this family
reduces to one headline number and takes a finding for it
(`PB_007`, `uninstrumented`'s SCALAR DEMAND). This one refuses the
reduction up front, which is why §3 is a one-clause fix rather than a
design problem.

**Denominators printed with the columns.** The table footer says
`cov: held / read` and `cyc: holds that survived a return / holds`, so the
two are visibly not over the same base — `measurement-fork`'s VOID RATIO
made unnecessary rather than enforced.

## 2 — DL_002, the reservation is a constant without its function

> RESERVATION: ... It **caps what the ledger will report as available
> headroom**, and it is why a shape with high coverage still does not
> coalesce.

    ten domains, all hold, reservation 0.20
      coverage 1.00   ceiling 0.80   coverage > ceiling: True
      fields naming headroom: none

`score()` computes `ceiling = 1 - reservation`, returns it, and `detail()`
prints it beside `RESERVATION`. Nothing reads it.

Not a wrong number — the docstring is explicit that reservation is *not*
subtracted from coverage, and it is not. What is missing is the readout
the same paragraph promises: the cap is stated as a function and shipped
as a constant. One line — `headroom = min(coverage, ceiling)`, or a flag
when coverage exceeds it.

## 3 — DL_003, one scalar over two different failures

    all break   coverage 0.00   breaks 2   mixed 0
    all mixed   coverage 0.00   breaks 0   mixed 2

`coverage` is holds / read, and `mixed` sits in the denominator only. A
break is the shape failing; a mixed read is the shape doing something the
two-value vocabulary cannot hold. Both return 0.00.

The information survives — `break_domains` and `mixed_domains` are
returned separately and printed under their own headings — so the loss is
in the derived scalar alone, the shape `PB_007` records one folder over.

Cheapest fix is not a fifth ratio. The footer reads `cov: held / read` and
does not say mixed is in `read`; one clause would.

## 4 — DL_004, the guard field, again

    SKELETON keys            : asserted_coverage, domains, reservation,
                               shape, source, statement
    read by detail(), absent : criterion_fixed_in_advance, open

`criterion_fixed_in_advance` is `category-weld` `CW_015`'s
pre-registration guard **promoted to a first-class field** — there it was
prose inside a term's `open` list, here it has its own key and its own
heading. Right direction, and the same discipline reached a third time
(`reasoning-gate` `G-PRE`, `photoperiod-claim-harness`'s `MechanismEdit`).

And it repeats `CW_015`'s gap exactly: `--new` emits a skeleton without
it, so the field a new shape most needs prompting for is the one the
template is silent about. Two folders, same drop family, same miss.

One thing this tool gets right that the other two do not:

    category-weld/weld.py              --new deep-copies: False
    generation-capacity/capacity.py    --new deep-copies: False
    domain-ledger/ledger.py            --new deep-copies: True

`dict(TEMPLATE)` is a shallow copy sharing nested lists with the module
global — harmless as called in both, one edit away from mutating the
template. `ledger.py` round-trips through JSON.

## 5 — DL_005, the empty report

No `shapes/` directory is delivered. `load()` returns `[]`, `table([])`
prints headers and the full explanatory footer, `main()` returns `None`:

    rows printed  : 0
    lines printed : 9
    exit code     : 0

    category-weld/weld.py              refuses: True
    presented-binary/binary_audit.py   refuses: True
    generation-capacity/capacity.py    refuses: True

Every sibling refuses on stderr with rc 1. This one prints a well-formed
report with no content and exits clean, and the footer's closing line —
*"Unpushed domains are not neutral. Each is an untested surface"* — prints
over zero domains.

The tool's subject is confidence readouts that do not carry their
denominator. Its empty state is a report whose denominator is zero,
rendered as though it had one.

The selftest does cover the empty case at the `score()` level — *"empty
ledger gives none not zero"*, *"empty mismatch is none"* — and those are
the right two checks. The gap is one level up, at a presentation layer the
selftest does not reach.

## Relation to the rest of the repo

- `criteria-drift/`, `anchor-interval/` — §1. Same identifiability
  argument, applied to a self-reported confidence instead of a benchmark
  score.
- `category-weld/` — §4. `criterion_fixed_in_advance` is `CW_015`'s guard
  with a schema slot, and the template gap comes with it.
- `presented-binary/` — §3 is `PB_007`'s shape on a different scalar, in
  a tool that avoided it on three others.
- `triad-playground/`, `reasoning-dial/` — `truncated` and `channel`
  record where a reading stopped and how it was taken, which is the
  observer-state axis `TP_006` and `RD_009` both name as unbuilt. Here it
  is a field; nothing yet reads it against an outcome.
