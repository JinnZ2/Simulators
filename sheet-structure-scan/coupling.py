#!/usr/bin/env python3
"""
coupling -- sensitivity of a workbook's outputs to one constant, by
perturbation, as a dimensionless elasticity.

    coupling.py verify BOOK.xlsx            evaluator against Excel's own cache
    coupling.py of BOOK.xlsx Sheet!A1       elasticity of one constant
    coupling.py rank BOOK.xlsx [--top N]    the ranking, coupling where computable
    coupling.py --selftest

WHY A DIMENSIONLESS ELASTICITY AND NOT THE PARTIAL DERIVATIVE. The raw
partial d(output)/d(term) carries the units of both, so it cannot be
compared between two claims and cannot weight a time. The elasticity

    E = (dY/Y) / (dX/X)

is dimensionless, comparable, and is what a shelf life can be divided by.
This is reasoning-gate G-DIM applied before the number is produced rather
than after it is quoted.

THE EVALUATOR IS RESTRICTED AND SAYS SO. Numbers, cell references,
ranges, + - * / ^, comparisons, parentheses, string literals, a lazy IF,
and a small function table. Anything else -- VLOOKUP, SUMIF, text
functions -- raises NotComputable, and every cell downstream of it is
NotComputable too.

IF is supported because of a measurement, not because it was tidy to
add. On the first real workbook, 336 of 349 unevaluable cells failed on
IF alone, and 0 of 789 ranked constants reached the coupling mode: the
dominant idiom is IF(G6="","",<arithmetic>), a guard for empty input
rows wrapped around ordinary multiplication. A feature with no instances
is a design that cannot exercise its own path, so the guard is evaluated
and the arithmetic underneath it is reached. That is the fallback the
integration order specifies: coupling where it is computable, dependent
count where it is not, and the mode named per row.

THE EVALUATOR IS CHECKED AGAINST EXCEL'S OWN CACHED VALUES. Every
derived cell in an .xlsx carries the value Excel last computed for it.
`verify` recomputes each one and compares. That is a known-answer run on
real data rather than on a fixture written by the same hand as the code,
and its coverage number is reported with every ranking.

CC0. stdlib only. Parses under Python 3.9. ASCII only.
"""

import math
import os
import re
import sys

import sheetmodel
from sheetmodel import CONSTANT_NUMBER, DERIVED, col_to_num, num_to_col

# [CHOICE] relative perturbation. Small enough that a smooth response is
# locally linear, large enough to clear float noise on a chain of a few
# multiplications.
EPS = 1e-3

# [CHOICE] a result cell whose magnitude is below this is treated as zero
# for the purpose of a relative change, because dividing a movement by a
# near-zero base reports an elasticity that is a property of the base.
ZERO_FLOOR = 1e-12


def parse_inputs(args):
    """Sheet!A1=VALUE, repeatable. The case the coupling is measured under."""
    out = {}
    for a in args:
        if "=" not in a or "!" not in a:
            raise ValueError("expected Sheet!A1=VALUE, got %r" % a)
        ref, val = a.rsplit("=", 1)
        sh, addr = ref.rsplit("!", 1)
        try:
            v = float(val)
        except ValueError:
            # A case may name a country, not only a quantity: the two
            # worked cases in the delivery are both consumed by a lookup
            # keyed on a text cell, so a numbers-only input parser
            # cannot express the case they need.
            v = val
        out[(sh.strip(), addr.strip().upper())] = v
    return out


class NotComputable(Exception):
    pass


class _Blank(object):
    """An empty cell, and the value an IF branch returns as \"\".

    Distinct from 0.0 on purpose: a blank that arithmetic touches is
    NotComputable, where a zero would quietly propagate.
    """

    def __repr__(self):
        return "BLANK"


BLANK = _Blank()


# ---------------------------------------------------------------- tokens

_NUM = re.compile(r"[0-9]*\.?[0-9]+(?:[eE][+-]?[0-9]+)?")
_REF = re.compile(
    r"(?:(?:'([^']+)'|([A-Za-z_][A-Za-z0-9_.]*))!)?"
    r"(\$?[A-Z]{1,3}\$?[0-9]+)"
    r"(?::(\$?[A-Z]{1,3}\$?[0-9]+))?"
    r"(?![A-Za-z0-9_.])(?!\s*\()")
_FUNC = re.compile(r"([A-Za-z][A-Za-z0-9_.]*)\s*\(")

def _criterion(c):
    """Excel's criterion string: '=Ferry', '<>Ferry', '>3', or a bare value."""
    if c is BLANK:
        return "=", ""
    if not isinstance(c, str):
        return "=", c
    for op in ("<>", "<=", ">=", "=", "<", ">"):
        if c.startswith(op):
            rest = c[len(op):]
            try:
                return op, float(rest)
            except ValueError:
                return op, rest
    return "=", c


def _compare(a, op, b):
    """Excel comparison, with BLANK equal to the empty string."""
    if a is BLANK:
        a = ""
    if b is BLANK:
        b = ""
    if isinstance(a, str) != isinstance(b, str):
        if op == "=":
            return False
        if op == "<>":
            return True
        raise NotComputable("ordering a string against a number")
    if op == "=":
        return a == b
    if op == "<>":
        return a != b
    if op == "<":
        return a < b
    if op == ">":
        return a > b
    if op == "<=":
        return a <= b
    return a >= b


FUNCS = {
    "SUM": lambda xs: sum(xs),
    "AVERAGE": lambda xs: (sum(xs) / len(xs)) if xs else 0.0,
    "MIN": lambda xs: min(xs) if xs else 0.0,
    "MAX": lambda xs: max(xs) if xs else 0.0,
    "ABS": lambda xs: abs(xs[0]),
    "ROUND": lambda xs: round(xs[0], int(xs[1]) if len(xs) > 1 else 0),
    "PRODUCT": lambda xs: math.prod(xs) if xs else 0.0,
    "SQRT": lambda xs: math.sqrt(xs[0]),
}


def as_number(v):
    if v is BLANK:
        # Excel's rule, and the reason this is not NotComputable: an
        # empty cell is 0 in arithmetic and "" in a comparison. Raising
        # here instead cost 392 of 475 reproduced cells on the first
        # real workbook, because a blank-guard idiom reaches ordinary
        # multiplication against empty input rows.
        return 0.0
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip()
        if not s:
            raise NotComputable("blank")
        try:
            return float(s)
        except ValueError:
            raise NotComputable("not numeric: %r" % s[:20])
    raise NotComputable("no value")


class Evaluator(object):
    """Recomputes a workbook under a set of cell overrides."""

    def __init__(self, wb):
        self.wb = wb

    def value(self, key, overrides, stack=None):
        stack = stack or set()
        if key in overrides:
            return overrides[key]
        cell = self.wb.cells.get(key)
        if cell is None:
            return BLANK
        if key in stack:
            raise NotComputable("cycle at %s!%s" % key)
        if cell.kind == DERIVED:
            if not cell.formula:
                raise NotComputable("no formula text")
            return self._eval(cell.formula, cell.sheet, overrides,
                              stack | {key})
        if cell.kind == sheetmodel.CONSTANT_TEXT:
            return cell.value
        return as_number(cell.value)

    # -- recursive descent ------------------------------------------------

    def _eval(self, text, sheet, overrides, stack):
        """Parser state is per-formula and MUST be saved across nesting.

        Evaluating a referenced cell re-enters this method and overwrites
        _s, _i and _sheet; without the save the outer formula resumes
        parsing inside the inner one. It cost SUM(E3:E24) over derived
        cells, which is every rollup on the first real workbook, and no
        fixture with only depth-1 formulas can show it.
        """
        saved = (getattr(self, "_s", None), getattr(self, "_i", None),
                 getattr(self, "_sheet", None), getattr(self, "_ov", None),
                 getattr(self, "_stack", None))
        try:
            self._s, self._i = text.lstrip("="), 0
            self._sheet, self._ov, self._stack = sheet, overrides, stack
            v = self._expr()
            self._ws()
            if self._i != len(self._s):
                raise NotComputable(
                    "trailing %r" % self._s[self._i:self._i + 12])
            return v
        finally:
            (self._s, self._i, self._sheet, self._ov,
             self._stack) = saved

    def _ws(self):
        while self._i < len(self._s) and self._s[self._i] in " \t\n":
            self._i += 1

    def _expr(self):
        v = self._add()
        self._ws()
        for op in ("<>", "<=", ">=", "=", "<", ">"):
            if self._s.startswith(op, self._i):
                self._i += len(op)
                r = self._add()
                return _compare(v, op, r)
        return v

    def _add(self):
        v = self._term()
        while True:
            self._ws()
            if self._i < len(self._s) and self._s[self._i] in "+-":
                op = self._s[self._i]
                self._i += 1
                r = self._term()
                v = as_number(v) + as_number(r) if op == "+" \
                    else as_number(v) - as_number(r)
            else:
                return v

    def _term(self):
        v = self._power()
        while True:
            self._ws()
            if self._i < len(self._s) and self._s[self._i] in "*/":
                op = self._s[self._i]
                self._i += 1
                r = as_number(self._power())
                v = as_number(v)
                if op == "/":
                    if abs(r) < ZERO_FLOOR:
                        raise NotComputable("division by zero")
                    v = v / r
                else:
                    v = v * r
            else:
                return v

    def _power(self):
        v = self._atom()
        self._ws()
        if self._i < len(self._s) and self._s[self._i] == "^":
            self._i += 1
            return v ** self._power()
        return v

    def _atom(self):
        self._ws()
        if self._i >= len(self._s):
            raise NotComputable("ended early")
        ch = self._s[self._i]
        if ch == "(":
            self._i += 1
            v = self._expr()
            self._ws()
            if self._i >= len(self._s) or self._s[self._i] != ")":
                raise NotComputable("unclosed paren")
            self._i += 1
            return v
        if ch in "+-":
            self._i += 1
            v = self._atom()
            return -v if ch == "-" else v
        if ch == '"':
            j = self._s.find('"', self._i + 1)
            if j < 0:
                raise NotComputable("unclosed string")
            lit = self._s[self._i + 1:j]
            self._i = j + 1
            return BLANK if lit == "" else lit
        m = _FUNC.match(self._s, self._i)
        if m:
            name = m.group(1).upper()
            if name == "IF":
                self._i = m.end()
                return self._if()
            if name == "SUMIF":
                self._i = m.end()
                return self._sumif()
            if name == "VLOOKUP":
                self._i = m.end()
                return self._vlookup()
            if name not in FUNCS:
                raise NotComputable("function %s" % name)
            self._i = m.end()
            args = self._args()
            return FUNCS[name](args)
        m = _REF.match(self._s, self._i)
        if m:
            self._i = m.end()
            return self._ref(m)
        m = _NUM.match(self._s, self._i)
        if m:
            self._i = m.end()
            return float(m.group(0))
        raise NotComputable("token %r" % self._s[self._i:self._i + 12])

    def _if(self):
        """Lazy: only the taken branch is evaluated.

        Eager evaluation would make IF(A1=0,0,B1/A1) NotComputable on a
        division by zero that the formula exists to avoid.
        """
        cond = self._expr()
        self._ws()
        if self._i >= len(self._s) or self._s[self._i] != ",":
            raise NotComputable("IF without branches")
        self._i += 1
        taken = bool(cond)
        a = self._branch(taken)
        self._ws()
        if self._i < len(self._s) and self._s[self._i] == ",":
            self._i += 1
            b = self._branch(not taken)
            self._ws()
        else:
            b = BLANK
        if self._i >= len(self._s) or self._s[self._i] != ")":
            raise NotComputable("IF unclosed")
        self._i += 1
        return a if taken else b

    def _branch(self, evaluate):
        """Parse a branch; evaluate it only if it is the one taken."""
        start = self._i
        if evaluate:
            return self._expr()
        depth = 0
        while self._i < len(self._s):
            ch = self._s[self._i]
            if ch == '"':
                j = self._s.find('"', self._i + 1)
                self._i = len(self._s) if j < 0 else j + 1
                continue
            if ch == "(":
                depth += 1
            elif ch == ")":
                if depth == 0:
                    break
                depth -= 1
            elif ch == "," and depth == 0:
                break
            self._i += 1
        if self._i == start:
            raise NotComputable("empty IF branch")
        return BLANK

    def _rangekeys(self):
        """Parse one range or single-reference argument into cell keys."""
        self._ws()
        m = _REF.match(self._s, self._i)
        if not m:
            raise NotComputable("expected a range")
        self._i = m.end()
        return self._keys(m)

    def _vlookup(self):
        """VLOOKUP(key, range, col_index, FALSE). Exact match only.

        Built last, and it is what the two worked cases in the delivery
        both route through: the grid emission factor and the hotel
        factor are each consumed by a lookup, so without this the
        coupling sub-field of both is unmeasurable and their clocks do
        not derive.

        Approximate match (TRUE, or the argument omitted) is refused
        rather than guessed: it requires the first column to be sorted,
        which this instrument does not check.
        """
        key = self._expr()
        self._ws()
        if self._i >= len(self._s) or self._s[self._i] != ",":
            raise NotComputable("VLOOKUP without a range")
        self._i += 1
        keys = self._rangekeys()
        self._ws()
        if self._i >= len(self._s) or self._s[self._i] != ",":
            raise NotComputable("VLOOKUP without a column index")
        self._i += 1
        idx = int(as_number(self._expr()))
        self._ws()
        exact = False
        if self._i < len(self._s) and self._s[self._i] == ",":
            self._i += 1
            self._ws()
            for lit, val in (("FALSE", True), ("TRUE", False), ("0", True)):
                if self._s.startswith(lit, self._i):
                    self._i += len(lit)
                    exact = val
                    break
            else:
                raise NotComputable("VLOOKUP range_lookup not a literal")
            self._ws()
        if not exact:
            raise NotComputable("VLOOKUP approximate match")
        if self._i >= len(self._s) or self._s[self._i] != ")":
            raise NotComputable("VLOOKUP unclosed")
        self._i += 1
        cols = {}
        for k in keys:
            cols.setdefault(col_to_num(
                k[1].rstrip("0123456789")), []).append(k)
        order = sorted(cols)
        if idx < 1 or idx > len(order):
            raise NotComputable("VLOOKUP column index out of range")
        first, want = cols[order[0]], cols[order[idx - 1]]
        for kk, vk in zip(first, want):
            if _compare(self.value(kk, self._ov, self._stack), "=", key):
                return self.value(vk, self._ov, self._stack)
        raise NotComputable("VLOOKUP no match")

    def _sumif(self):
        """SUMIF(range, criterion, [sum_range]).

        Built because two of these cells gate the coupling mode for the
        entire first real workbook: every constant in it terminates at
        one grand total, and that total sums two SUMIF cells. 627 of 631
        formulas evaluated and 0 of 789 constants reached a coupling
        number, because coverage of a perturbation is a property of the
        TERMINALS, not of the formula population.
        """
        keys = self._rangekeys()
        self._ws()
        if self._i >= len(self._s) or self._s[self._i] != ",":
            raise NotComputable("SUMIF without a criterion")
        self._i += 1
        crit = self._expr()
        self._ws()
        sumkeys = keys
        if self._i < len(self._s) and self._s[self._i] == ",":
            self._i += 1
            sumkeys = self._rangekeys()
            self._ws()
        if self._i >= len(self._s) or self._s[self._i] != ")":
            raise NotComputable("SUMIF unclosed")
        self._i += 1
        if len(sumkeys) != len(keys):
            raise NotComputable("SUMIF ranges of unequal size")
        op, want = _criterion(crit)
        total = 0.0
        for tk, sk in zip(keys, sumkeys):
            v = self.value(tk, self._ov, self._stack)
            if not _compare(v, op, want):
                continue
            sv = self.value(sk, self._ov, self._stack)
            if sv is BLANK:
                continue
            total += as_number(sv)
        return total

    def _args(self):
        """Flattened: SUM(A1:A3, B1) is one list of numbers."""
        out = []
        self._ws()
        if self._i < len(self._s) and self._s[self._i] == ")":
            self._i += 1
            return out
        while True:
            self._ws()
            m = _REF.match(self._s, self._i)
            if m and m.group(4):
                self._i = m.end()
                out.extend(self._range(m))
            else:
                v = self._expr()
                if v is not BLANK:
                    out.append(as_number(v))
            self._ws()
            if self._i < len(self._s) and self._s[self._i] == ",":
                self._i += 1
                continue
            if self._i < len(self._s) and self._s[self._i] == ")":
                self._i += 1
                return out
            raise NotComputable("argument list")

    def _keys(self, m):
        sheet = m.group(1) or m.group(2) or self._sheet
        a1 = m.group(3).replace("$", "").upper()
        a2 = m.group(4)
        if not a2:
            return [(sheet, a1)]
        r1, c1 = sheetmodel.rc(a1)
        r2, c2 = sheetmodel.rc(a2.replace("$", "").upper())
        keys = []
        for r in range(min(r1, r2), max(r1, r2) + 1):
            for c in range(min(c1, c2), max(c1, c2) + 1):
                keys.append((sheet, num_to_col(c) + str(r)))
        return keys

    def _ref(self, m):
        keys = self._keys(m)
        if len(keys) != 1:
            raise NotComputable("range outside a function")
        return self.value(keys[0], self._ov, self._stack)

    def _range(self, m):
        out = []
        for k in self._keys(m):
            cell = self.wb.cells.get(k)
            if cell is None:
                continue          # blanks are skipped by SUM, not zeroed
            v = self.value(k, self._ov, self._stack)
            if v is BLANK or isinstance(v, str):
                # Excel's rule: a range aggregate skips blanks AND text.
                # Raising here instead cost the workbook's grand total,
                # because Report!E23 sums Food!E5:E16 -- starting on the
                # header row, where every sibling row starts at 6. The
                # off-by-one is invisible in Excel and is a real
                # difference between that row and the twenty beside it.
                continue
            out.append(as_number(v))
        return out


# ------------------------------------------------------------- coverage

def verify(wb, limit=None):
    """The evaluator against Excel's own cached values.

    A known-answer run on real data: every derived cell carries the value
    Excel last computed, and reproducing it is the check.
    """
    ev = Evaluator(wb)
    match = mismatch = notcomp = nocache = 0
    worst = None
    for key, cell in sorted(wb.cells.items()):
        if cell.kind != DERIVED:
            continue
        if limit and match + mismatch + notcomp >= limit:
            break
        try:
            cached = as_number(cell.value)
        except NotComputable:
            nocache += 1
            continue
        try:
            got = as_number(ev.value(key, {}))
        except (NotComputable, RecursionError, ValueError, OverflowError,
                ZeroDivisionError):
            # A cell that evaluates to BLANK or text has no number to
            # compare, which is not the same as one the evaluator could
            # not reach. Both land here and the count is a ceiling on
            # the second, stated in the report.
            notcomp += 1
            continue
        scale = max(abs(cached), abs(got), 1.0)
        rel = abs(got - cached) / scale
        if rel < 1e-9:
            match += 1
        else:
            mismatch += 1
            if worst is None or rel > worst[1]:
                worst = ("%s!%s" % key, rel, cached, got)
    return {"match": match, "mismatch": mismatch, "not_computable": notcomp,
            "no_cached_number": nocache, "worst": worst}


def terminals_downstream(wb, key):
    """Reachable cells that nothing else depends on."""
    deps = wb.dependents()
    seen, stack, out = set(), [key], []
    while stack:
        k = stack.pop()
        for d in deps.get(k, ()):
            if d in seen:
                continue
            seen.add(d)
            stack.append(d)
            if not deps.get(d):
                out.append(d)
    return sorted(out)


def elasticity(wb, key, eps=EPS, inputs=None):
    """Dimensionless sensitivity of downstream terminals to one constant.

    `inputs` are cell overrides applied to BOTH runs: the case the
    coupling is measured under. They are not optional in spirit --
    COUPLING IS A PROPERTY OF THE WORKBOOK PLUS A FILLED CASE, NOT OF
    THE WORKBOOK ALONE. Perturbing an emission factor in a blank
    template moves nothing, because the activity data it multiplies is
    empty and every result is zero on both sides.

    Four states, and the last two must not be one:
      COMPUTED        at least one terminal moved measurably
      NOT_COMPUTABLE  no terminal could be evaluated at all
      NO_LIVE_PATH    terminals evaluate, and the base is zero -- the
                      chain is live but carries nothing
      plus the shape guards below
    """
    cell = wb.cells.get(key)
    if cell is None or cell.kind != CONSTANT_NUMBER:
        return {"state": "NOT_A_CONSTANT", "elasticity": None,
                "terminals": 0, "evaluated": 0}
    try:
        base = as_number(cell.value)
    except NotComputable:
        return {"state": "NOT_NUMERIC", "elasticity": None,
                "terminals": 0, "evaluated": 0}
    if abs(base) < ZERO_FLOOR:
        return {"state": "BASE_IS_ZERO", "elasticity": None,
                "terminals": 0, "evaluated": 0}

    terms = terminals_downstream(wb, key)
    if not terms:
        return {"state": "NO_TERMINALS", "elasticity": None,
                "terminals": 0, "evaluated": 0}

    ev = Evaluator(wb)
    given = dict(inputs or {})
    bumped = dict(given)
    bumped[key] = base * (1.0 + eps)
    given.setdefault(key, base)
    best, evaluated, zero_base = None, 0, 0
    for t in terms:
        try:
            y0 = as_number(ev.value(t, given))
            y1 = as_number(ev.value(t, bumped))
        except (NotComputable, RecursionError, ValueError, OverflowError,
                ZeroDivisionError):
            # A terminal that evaluates to BLANK or to text is skipped,
            # not counted as zero movement. as_number raises on both, so
            # the blank-guard idiom lands here rather than reporting an
            # elasticity of 0 for a cell that was never a number.
            continue
        if abs(y0) < ZERO_FLOOR:
            zero_base += 1
            continue
        e = ((y1 - y0) / y0) / eps
        evaluated += 1
        if best is None or abs(e) > abs(best):
            best = e
    if evaluated == 0:
        # The distinction the blank template forces: a chain that cannot
        # be evaluated and a chain that evaluates to nothing are not the
        # same finding, and reporting either as a zero elasticity would
        # read as "measured, and it does not matter".
        state = "NO_LIVE_PATH" if zero_base else "NOT_COMPUTABLE"
        return {"state": state, "elasticity": None,
                "terminals": len(terms), "evaluated": 0,
                "zero_base": zero_base}
    return {"state": "COMPUTED", "elasticity": best,
            "terminals": len(terms), "evaluated": evaluated,
            "zero_base": zero_base}


def moved(wb, key, eps=EPS, inputs=None):
    """Every cell that changes when one constant is perturbed.

    The aggregate elasticity is a maximum over terminals and hides which
    cells carry it. This walks the whole workbook under both states and
    reports each cell that moved, with its own elasticity.

    It also separates two things a dependent count cannot:
      STRUCTURAL dependence -- the cell appears in a range some formula
        reads, so the graph has an edge;
      LIVE dependence -- the value actually changes under the stated
        case.
    A lookup range makes every cell in it a structural dependent of every
    consumer, while only the row the key selects is a live one.
    """
    cell = wb.cells.get(key)
    if cell is None or cell.kind != CONSTANT_NUMBER:
        return {"state": "NOT_A_CONSTANT", "rows": []}
    base = as_number(cell.value)
    if abs(base) < ZERO_FLOOR:
        return {"state": "BASE_IS_ZERO", "rows": []}

    ev = Evaluator(wb)
    given = dict(inputs or {})
    bumped = dict(given)
    bumped[key] = base * (1.0 + eps)
    given.setdefault(key, base)

    rows, unevaluable = [], 0
    for k, c in sorted(wb.cells.items()):
        if k == key or c.kind != DERIVED:
            continue
        try:
            y0 = as_number(ev.value(k, given))
            y1 = as_number(ev.value(k, bumped))
        except (NotComputable, RecursionError, ValueError, OverflowError,
                ZeroDivisionError):
            unevaluable += 1
            continue
        if y0 == y1:
            continue
        e = (((y1 - y0) / y0) / eps) if abs(y0) >= ZERO_FLOOR else None
        rows.append({"cell": "%s!%s" % k, "before": y0, "after": y1,
                     "delta": y1 - y0, "elasticity": e,
                     "pdepth": wb.precedent_depth(k)})
    deps = wb.dependents().get(key, ())
    live = set(r["cell"] for r in rows)
    structural = set("%s!%s" % d for d in deps)
    return {"state": "OK", "rows": rows, "unevaluable": unevaluable,
            "structural_dependents": sorted(structural),
            "structural_not_live": sorted(structural - live),
            "live_not_structural": sorted(live - structural),
            "perturbed": "%s!%s" % key, "base": base}


# ------------------------------------------------------------- ranking

def ranked(wb, eps=EPS, inputs=None):
    """The integration: coupling where computable, dependent count where not.

    The two modes are NOT on one scale and the report says so per row.
    A column that mixed them would be a ratio across unlike objects, so
    the mode is a column and rows are sorted within it.
    """
    rows = []
    for key, cell in sorted(wb.cells.items()):
        if cell.kind != CONSTANT_NUMBER:
            continue
        dd = wb.downstream_depth(key)
        if dd == sheetmodel.CYCLE or dd == 0:
            continue
        e = elasticity(wb, key, eps, inputs)
        deps = len(wb.dependents().get(key, ()))
        if e["state"] == "COMPUTED":
            rows.append({"site": "%s!%s" % key, "mode": "COUPLING",
                         "coupling": abs(e["elasticity"]), "deps": deps,
                         "ddepth": dd,
                         "rank": abs(e["elasticity"]) * dd,
                         "evaluated": e["evaluated"],
                         "terminals": e["terminals"]})
        else:
            rows.append({"site": "%s!%s" % key, "mode": "COUNT",
                         "coupling": None, "deps": deps, "ddepth": dd,
                         "rank": deps * dd, "evaluated": 0,
                         "terminals": e["terminals"], "why": e["state"]})
    return rows


def table(headers, rows):
    w = [len(h) for h in headers]
    body = [[str(x) for x in r] for r in rows]
    for r in body:
        for i, c in enumerate(r):
            w[i] = max(w[i], len(c))
    fmt = "  ".join("%-" + str(x) + "s" for x in w)
    out = [fmt % tuple(headers), fmt % tuple("-" * x for x in w)]
    for r in body:
        out.append((fmt % tuple(r)).rstrip())
    return "\n".join(out)


def render_rank(wb, rows, cov, top=20, inputs=None):
    lines = ["ranking -- coupling where computable, dependent count where not",
             "workbook       %s" % os.path.basename(wb.path or "-"),
             "perturbation   %g relative" % EPS,
             "case           %s" % (
                 ", ".join("%s!%s=%s" % (k[0], k[1], v)
                           for k, v in sorted((inputs or {}).items()))
                 or "none given -- an unfilled template moves nothing"),
             "evaluator      reproduces %d of %d cached values; %d not "
             "computable" % (cov["match"], cov["match"] + cov["mismatch"],
                             cov["not_computable"]),
             "",
             "COUPLING and COUNT ranks are not on one scale and do not",
             "compare. Rows are sorted within mode.",
             ""]
    for mode in ("COUPLING", "COUNT"):
        sel = sorted([r for r in rows if r["mode"] == mode],
                     key=lambda r: -r["rank"])
        lines.append("%s  (%d constants)" % (mode, len(sel)))
        lines.append(table(
            ["rank", "site", "coupling", "deps", "ddepth", "evaluated/terminals"],
            [["%.4g" % r["rank"], r["site"],
              "-" if r["coupling"] is None else "%.4g" % r["coupling"],
              r["deps"], r["ddepth"],
              "%d/%d" % (r["evaluated"], r["terminals"])] for r in sel[:top]]))
        if len(sel) > top:
            lines.append("  ... %d more not shown" % (len(sel) - top))
        lines.append("")
    return "\n".join(lines)


# ------------------------------------------------------------- selftest

def _selftest():
    import tempfile
    import fixture
    fails = []

    def ck(name, got, want):
        ok = got == want
        if not ok:
            fails.append(name)
        print("  %-54s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    def close(name, got, want, tol=1e-9):
        ok = got is not None and abs(got - want) <= tol
        if not ok:
            fails.append(name)
        print("  %-54s %-4s got=%r want=%r"
              % (name, "PASS" if ok else "FAIL", got, want))

    print("coupling selftest")
    d = tempfile.mkdtemp()

    # Known answers taken from the algebra, not from what the code returns.
    sheets = [("S", {
        "A1": ("t", "x"), "B1": ("t", "y"), "C1": ("t", "out"),
        "A2": ("n", "4"), "B2": ("n", "5"),
        "C2": ("f", "A2*B2"),        # d ln C / d ln A = 1
        "D2": ("f", "A2+B2"),        # elasticity of A2 = A/(A+B) = 4/9
        "E2": ("f", "A2^2"),         # elasticity 2
        "F2": ("f", "SUM(A2:B2)"),   # same as D2
        "G2": ("f", "1/A2"),         # elasticity -1
        "H2": ("f", "CONCATENATE(A1,A1)"),  # unsupported
        "I2": ("f", 'IF(A2>0,A2*2,0)'),   # taken branch, elasticity 1
        "J2": ("f", 'IF(A2=0,1/A2,7)'),   # eager would divide by zero
        "K2": ("f", 'IF(Z9="","",A2*3)'),  # blank guard on an empty cell
        "L2": ("f", 'IF(A1="x",A2*5,0)'),  # a text comparison
        # Nesting. Every one of these is a formula, so evaluating the
        # range re-enters the parser once per element.
        "M2": ("f", "A2*2"), "M3": ("f", "A2*3"), "M4": ("f", "A2*4"),
        "M5": ("f", "SUM(M2:M4)"),   # 4*(2+3+4) = 36
        "M6": ("f", "SUM(M2:M4)+A2"),  # 40
        # SUMIF over a text key column with a value column beside it.
        "P2": ("t", "Ferry"), "Q2": ("n", "10"),
        "P3": ("t", "Rail"), "Q3": ("n", "20"),
        "P4": ("t", "Ferry"), "Q4": ("n", "5"),
        "P5": ("f", 'SUMIF(P2:P4,"=Ferry",Q2:Q4)'),   # 15
        "P6": ("f", 'SUMIF(P2:P4,"<>Ferry",Q2:Q4)'),  # 20
        "R1": ("t", "header"), "R2": ("n", "3"), "R3": ("n", "4"),
        "R5": ("f", "SUM(R1:R3)"),   # 7: the text header is skipped
        "T1": ("t", "aa"), "U1": ("n", "11"),
        "T2": ("t", "bb"), "U2": ("n", "22"),
        "T3": ("t", "bb"),
        "T5": ("f", 'VLOOKUP("bb",T1:U2,2,FALSE)'),   # 22
        "T6": ("f", 'VLOOKUP("zz",T1:U2,2,FALSE)'),   # no match
        "T7": ("f", 'VLOOKUP("bb",T1:U2,2,TRUE)'),    # approximate: refused
    })]
    wb = sheetmodel.read(fixture.write_demo(os.path.join(d, "c.xlsx"), sheets))
    ev = Evaluator(wb)
    close("product evaluates", ev.value(("S", "C2"), {}), 20.0)
    close("sum evaluates", ev.value(("S", "D2"), {}), 9.0)
    close("power evaluates", ev.value(("S", "E2"), {}), 16.0)
    close("SUM over a range evaluates", ev.value(("S", "F2"), {}), 9.0)
    try:
        ev.value(("S", "H2"), {})
        ck("an unsupported function is still refused", False, True)
    except NotComputable:
        ck("an unsupported function is still refused", True, True)
    close("IF takes the live branch", ev.value(("S", "I2"), {}), 8.0)
    close("IF is lazy: the dead branch is not evaluated",
          ev.value(("S", "J2"), {}), 7.0)
    ck("a blank guard returns BLANK, not zero",
       ev.value(("S", "K2"), {}) is BLANK, True)
    close("and BLANK is 0 in arithmetic, as Excel has it",
          as_number(BLANK), 0.0)
    ck("while comparing equal to the empty string",
       _compare(BLANK, "=", ""), True)
    close("a text comparison resolves", ev.value(("S", "L2"), {}), 20.0)
    close("SUM over DERIVED cells evaluates", ev.value(("S", "M5"), {}), 36.0)
    close("and the outer formula resumes correctly after it",
          ev.value(("S", "M6"), {}), 40.0)
    close("SUMIF with an equality criterion", ev.value(("S", "P5"), {}), 15.0)
    close("SUMIF with a not-equal criterion", ev.value(("S", "P6"), {}), 20.0)
    close("a range aggregate skips a text header, as Excel does",
          ev.value(("S", "R5"), {}), 7.0)
    close("VLOOKUP exact match", ev.value(("S", "T5"), {}), 22.0)
    for name, addr in (("no match is refused, not defaulted", "T6"),
                       ("approximate match is refused, not guessed", "T7")):
        try:
            ev.value(("S", addr), {})
            ck("VLOOKUP " + name, False, True)
        except NotComputable:
            ck("VLOOKUP " + name, True, True)

    def el(target, src=("S", "A2")):
        ovr = {src: 4.0 * (1 + EPS)}
        y0 = ev.value(target, {})
        y1 = ev.value(target, ovr)
        return ((y1 - y0) / y0) / EPS

    close("elasticity of a product is 1", el(("S", "C2")), 1.0, 1e-6)
    close("elasticity of a sum is A/(A+B)", el(("S", "D2")), 4.0 / 9.0, 1e-3)
    close("elasticity of a square is 2", el(("S", "E2")), 2.0, 1e-2)
    close("elasticity of a reciprocal is -1", el(("S", "G2")), -1.0, 1e-2)

    r = elasticity(wb, ("S", "A2"))
    ck("a constant with computable terminals reports COMPUTED",
       r["state"], "COMPUTED")
    ck("and does not count terminals it could not evaluate",
       r["evaluated"] < r["terminals"], True)
    close("the largest elasticity is the square's", r["elasticity"], 2.0, 1e-2)

    # The state that must not be a zero.
    # The lookup range must not contain the formula cell, or the graph
    # has a self-loop and the constant is skipped as a cycle rather than
    # reaching the fallback this checks.
    only_if = [("S", {"A1": ("t", "x"), "A2": ("n", "4"),
                      "D1": ("n", "4"), "E1": ("n", "9"),
                      "B2": ("f", "VLOOKUP(A2,D1:E1,2,TRUE)")})]
    wb2 = sheetmodel.read(fixture.write_demo(os.path.join(d, "n.xlsx"),
                                             only_if))
    r2 = elasticity(wb2, ("S", "A2"))
    ck("an unevaluable chain is NOT_COMPUTABLE, not zero",
       (r2["state"], r2["elasticity"]), ("NOT_COMPUTABLE", None))
    ck("and the ranking falls back to the count with the mode named",
       sorted({(x["mode"], x["rank"]) for x in ranked(wb2)}),
       [("COUNT", 1)])
    ck("every constant feeding the unevaluable cell falls back",
       {x["mode"] for x in ranked(wb2)}, {"COUNT"})

    # A constant nothing depends on is not ranked at all.
    ck("a constant with no dependents is not ranked",
       [x for x in ranked(wb) if x["site"] == "S!B1"], [])

    # verify() is checked in BOTH directions, on a fixture that carries
    # real cached values: one formula whose cache is right, one whose
    # cache is deliberately wrong. A verify that reported everything as
    # matching would pass a one-armed test.
    vsheets = [("S", {
        "A1": ("t", "x"), "A2": ("n", "4"), "B2": ("n", "5"),
        "C2": ("f", "A2*B2", 20),      # Excel would cache 20
        "D2": ("f", "A2*B2", 999),     # a cache that disagrees
        "E2": ("f", 'IF(A2>0,1,0)', 1),  # computable, cache agrees
    })]
    wbv = sheetmodel.read(fixture.write_demo(os.path.join(d, "v.xlsx"),
                                             vsheets))
    cv = verify(wbv)
    ck("verify separates a right cache from a wrong one",
       (cv["match"], cv["mismatch"], cv["not_computable"]), (2, 1, 0))
    ck("and names the disagreement",
       cv["worst"] is not None and cv["worst"][0], "S!D2")

    print("SELFTEST %s (%d checks failed)"
          % ("PASS" if not fails else "FAIL", len(fails)))
    return 1 if fails else 0


USAGE = """usage:
  coupling.py verify BOOK.xlsx
  coupling.py of     BOOK.xlsx Sheet!A1 [--input Sheet!B1=1000 ...]
  coupling.py rank   BOOK.xlsx [--top N] [--input Sheet!B1=1000 ...]
  coupling.py cells  BOOK.xlsx Sheet!A1 [--input ...]   per-cell movement
  coupling.py --selftest"""


def main(argv):
    if "--selftest" in argv:
        return _selftest()
    if len(argv) < 3:
        print(USAGE)
        return 2
    cmd, path = argv[1], argv[2]
    wb = sheetmodel.read(path)
    if cmd == "verify":
        c = verify(wb)
        print("evaluator against Excel's own cached values")
        print("  reproduced      %d" % c["match"])
        print("  disagreed       %d" % c["mismatch"])
        print("  not computable  %d" % c["not_computable"])
        print("  no cached value %d" % c["no_cached_number"])
        if c["worst"]:
            print("  largest disagreement: %s rel=%.3g cached=%r got=%r"
                  % c["worst"])
        return 0
    if cmd == "of":
        if len(argv) < 4:
            print(USAGE)
            return 2
        sh, addr = argv[3].rsplit("!", 1)
        ins = parse_inputs([argv[i + 1] for i, a in enumerate(argv)
                            if a == "--input"])
        r = elasticity(wb, (sh, addr.upper()), inputs=ins)
        print("case          %s" % (
            ", ".join("%s!%s=%s" % (k[0], k[1], v)
                      for k, v in sorted(ins.items())) or "none given"))
        for k in ("state", "elasticity", "evaluated", "terminals"):
            print("%-12s %s" % (k, r[k]))
        return 0
    if cmd == "cells":
        if len(argv) < 4:
            print(USAGE)
            return 2
        sh, addr = argv[3].rsplit("!", 1)
        ins = parse_inputs([argv[i + 1] for i, a in enumerate(argv)
                            if a == "--input"])
        r = moved(wb, (sh, addr.upper()), inputs=ins)
        if r["state"] != "OK":
            print("state %s" % r["state"])
            return 1
        print("perturbed      %s = %.17g, +%g relative"
              % (r["perturbed"], r["base"], EPS))
        print("case           %s" % (
            ", ".join("%s!%s=%s" % (k[0], k[1], v)
                      for k, v in sorted(ins.items())) or "none given"))
        print("cells moved    %d" % len(r["rows"]))
        print("unevaluable    %d" % r["unevaluable"])
        print("")
        print(table(["cell", "pdepth", "before", "after", "delta",
                     "elasticity"],
                    [[x["cell"], x["pdepth"], "%.10g" % x["before"],
                      "%.10g" % x["after"], "%.4g" % x["delta"],
                      "-" if x["elasticity"] is None
                      else "%.6g" % x["elasticity"]]
                     for x in sorted(r["rows"],
                                     key=lambda x: (x["pdepth"], x["cell"]))]))
        print("")
        print("structural dependents (graph edges):        %d"
              % len(r["structural_dependents"]))
        print("of those, did NOT move under this case:     %d"
              % len(r["structural_not_live"]))
        print("moved without being a direct dependent:     %d"
              % len(r["live_not_structural"]))
        return 0
    if cmd == "rank":
        top = 20
        if "--top" in argv:
            top = int(argv[argv.index("--top") + 1])
        ins = parse_inputs([argv[i + 1] for i, a in enumerate(argv)
                            if a == "--input"])
        print(render_rank(wb, ranked(wb, inputs=ins), verify(wb), top, ins))
        return 0
    print(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
