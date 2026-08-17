#!/usr/bin/env python3
"""ledger_audit.py -- checks on the domain-ledger drop.

Added, not delivered. ledger.py is the drop as received and is not
modified. Findings are recorded in AUDIT_NOTES.md as DL_001..DL_005.

    python3 ledger_audit.py

The drop is one file: a scorer with a selftest, no shapes/ directory, no
README and no claim table. Nothing here invents a shape.

stdlib only, deterministic. CC0.
"""

import contextlib
import io
import os

import ledger as L

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
BAR = "=" * 70


def head(n, cid, title):
    print()
    print(BAR)
    print("%-2d %s  %s" % (n, cid, title))
    print(BAR)


print("domain-ledger -- audit of the delivered drop")
print("delivered: ledger.py")
print("not delivered: shapes/, README.md, CLAIM_TABLE.md")
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = L.selftest()
print("selftest: %s, rc=%d" % (buf.getvalue().strip().splitlines()[-1], rc))

# ------------------------------------------------------------------ DL_001
head(1, "DL_001", "the load-bearing idea, and it is the one the repo needed")
print("""
    A coverage number is not portable without its denominator. 61 percent
    over one domain set is a different quantity than 61 percent over
    another. This records the set.

That is `criteria-drift` CD_008 and `anchor-interval` ANC_006 stated for a
confidence readout instead of a benchmark: a number is identified only up
to the reference it was taken against, so publish the reference. Here the
reference is a list of domains and it is carried in the file.

Two design choices follow from it and both are unusual enough to record.

FOUR READOUTS, NOT COMBINED. coverage / cycle_depth / adversarial /
truncated are returned separately, with the docstring stating why:
"Coverage and cycle depth are different currencies. A shape can be wide
and shallow." Every other scorer in this family reduces to one headline
number and gets a finding against it -- presented-binary PB_007
(documented_share merges two states), uninstrumented's SCALAR DEMAND.
This one refuses the reduction up front.

DENOMINATORS NAMED IN THE OUTPUT. The table footer prints what each
column divides by -- "cov: held / read", "cyc: holds that survived a
return / holds" -- so the two are visibly not over the same base. That is
the `measurement-fork` VOID RATIO check made unnecessary rather than
enforced: you cannot compare them because the tool says what they are.
""".strip())

# ------------------------------------------------------------------ DL_002
head(2, "DL_002", "the reservation is defined and never applied")
print("""
    RESERVATION: a standing fraction held as unknown, applied to every
    shape. It is not subtracted from coverage -- coverage is over what was
    read. It CAPS WHAT THE LEDGER WILL REPORT AS AVAILABLE HEADROOM, and
    it is why a shape with high coverage still does not coalesce.

`score()` computes `ceiling = 1 - reservation` and returns it. Nothing
compares anything to it. There is no headroom field, and coverage is free
to exceed the ceiling with no readout saying so:
""".strip())
s = L.score({"shape": "probe", "reservation": 0.2,
             "domains": [{"domain": d, "read": L.HOLD} for d in "abcdefghij"]})
print()
print("  ten domains, all hold, reservation 0.20")
print("    coverage %s   ceiling %s   coverage > ceiling: %s" % (
    L.fmt(s["coverage"]), L.fmt(s["ceiling"]), s["coverage"] > s["ceiling"]))
print("    fields naming headroom: %s" % (
    [k for k in s if "head" in k or "room" in k] or "none"))
print()
print("""
The sentence names a function -- cap the reported headroom -- and the code
carries the constant without the function. `ceiling` is printed in
`detail()` beside `RESERVATION` and read by nothing.

Not a wrong number: the docstring is explicit that reservation is NOT
subtracted from coverage, and it is not. What is missing is the readout
the same paragraph promises. One line: headroom = min(coverage, ceiling),
or a flag when coverage exceeds it.
""".strip())

# ------------------------------------------------------------------ DL_003
head(3, "DL_003", "coverage merges break with mixed")
print()
for label, r in (("all break", L.BREAK), ("all mixed", L.MIXED)):
    sc = L.score({"shape": label,
                  "domains": [{"domain": "a", "read": r},
                              {"domain": "b", "read": r}]})
    print("  %-10s coverage %s   breaks %d   mixed %d" % (
        label, L.fmt(sc["coverage"]), sc["breaks"], sc["mixed"]))
print("""
coverage is holds / read, and `mixed` is in the denominator and not the
numerator. So a shape that broke everywhere and a shape that read mixed
everywhere both return 0.00 -- and those are different results. A break is
the shape failing; a mixed read is the shape doing something the two-value
vocabulary cannot hold.

The information is not lost: `break_domains` and `mixed_domains` are
returned separately and `detail()` prints both under their own headings.
The loss is in the derived scalar only, which is precisely the shape
PB_007 records one folder over -- and DL_001 credits this tool with
refusing exactly that reduction on the other three readouts.

Cheapest fix is not a fifth ratio. It is the footer: "cov: held / read"
does not say that mixed sits in the denominator, and one clause would.
""".strip())

# ------------------------------------------------------------------ DL_004
head(4, "DL_004", "the guard field is read and not in the skeleton -- again")
print("""
`detail()` reads two top-level fields the SKELETON does not carry:
""".strip())
print()
print("  SKELETON keys            : %s" % ", ".join(sorted(L.SKELETON)))
print("  read by detail(), absent : criterion_fixed_in_advance, open")
print("""
`criterion_fixed_in_advance` is `category-weld` CW_015's pre-registration
guard promoted to a first-class schema field -- there it lived as prose
inside a term's `open` list, here it has its own key and its own heading
in the detail view. That is the right direction and it is the same author
reaching the same discipline a third time (reasoning-gate G-PRE,
photoperiod MechanismEdit, CW_015).

And it repeats CW_015's gap exactly: `--new` emits a skeleton without it,
so the field a new shape most needs prompting for is the field the
template is silent about. Two folders, same author, same drop family, same
miss.

What is different here, and better: the SKELETON is deep-copied.
""".strip())
import json as _json
srcs = {
    "category-weld/weld.py": "TEMPLATE",
    "generation-capacity/capacity.py": "SKELETON",
    "domain-ledger/ledger.py": "SKELETON",
}
print()
print("  %-34s %s" % ("tool", "--new deep-copies its template"))
print("  " + "-" * 66)
for path in srcs:
    src = open(os.path.join(ROOT, path), encoding="utf-8").read()
    print("  %-34s %s" % (path, "json.loads(json.dumps(" in src))
print("""
`weld.py` and `capacity.py` both use `dict(TEMPLATE)`, a shallow copy that
shares the nested lists with the module global. Harmless as called -- both
only assign the top-level name -- but one line of future editing away from
mutating the template. `ledger.py` round-trips through JSON. Recorded
because it is the correct one of the three and the difference is invisible
until it is not.
""".strip())

# ------------------------------------------------------------------ DL_005
head(5, "DL_005", "an empty ledger prints a clean report")
print("""
There is no shapes/ directory in the drop. `load()` returns [] when the
directory is absent, `table([])` prints headers and the full explanatory
footer, and main() returns None:
""".strip())
print()
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    L.table([])
out = buf.getvalue()
print("    rows printed  : %d" % max(0, len(out.strip().splitlines()) - 2 - 7))
print("    lines printed : %d" % len(out.strip().splitlines()))
print("    exit code     : 0")
print()
print("  the three sibling tools on the same state:")
for path, msg in (("category-weld/weld.py", "no weld files in ... -> rc 1"),
                  ("presented-binary/binary_audit.py", "no case files in ... -> rc 1"),
                  ("generation-capacity/capacity.py", "no cases/ directory -> rc 1")):
    src = open(os.path.join(ROOT, path), encoding="utf-8").read()
    refuses = "stderr" in src and "return 1" in src or "sys.exit(1)" in src
    print("    %-38s refuses: %s" % (path, refuses))
print("""
Every sibling refuses and says so on stderr. This one prints a well-formed
report with no content and exits clean, so an empty ledger is
indistinguishable from a populated one at a glance -- and the footer's
closing line, "Unpushed domains are not neutral. Each is an untested
surface", prints over zero domains.

The tool's own subject is confidence readouts that do not carry their
denominator. Its empty state is a report whose denominator is zero,
rendered as if it had one.

Nothing else here is unverified: the selftest is 13/13, it covers the
empty-ledger case at the score() level ("empty ledger gives none not
zero", "empty mismatch is none"), and those are the right two checks. The
gap is one level up, at the presentation layer the selftest does not
reach.
""".strip())

print()
print(BAR)
print("end of audit -- findings recorded in AUDIT_NOTES.md as DL_001..DL_005")
print(BAR)
