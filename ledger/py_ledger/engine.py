#!/usr/bin/env python3
"""Exact decimal recomputation of DERIVED claims, and transitive provenance.

Two jobs, both arithmetic over the claim graph:

  recompute(...)           evaluate a DERIVED claim's expression from its
                           operands, exact decimal, no float anywhere
  resolve_provenance(...)  walk the operand graph and mark a DERIVED claim
                           whose support reaches a CARRIED value as
                           DERIVED_WEAK, naming the weak operand

NO eval(). Expressions are parsed with `ast` and walked against a closed node
whitelist; anything outside it is UNPARSEABLE and returns as a result rather
than raising. A qualified reference (`sim:claim_id`) is not valid Python, so
references are substituted for placeholders before parsing and the mapping is
kept, which is also what keeps a name in the expression from ever being read
as a Python builtin.

[CHOICE 1] `precision` is read as SIGNIFICANT DIGITS, which is what
decimal.Context.prec means. The order does not say which reading it intends
and the two disagree on every value that is not an integer; naming the
reading here means a disagreement over it shows up as a disagreement about
this line rather than as a silent mismatch.

[CHOICE 2] Recomputation runs at declared precision + GUARD guard digits and
quantizes to the declared precision once, at the end. Rounding at every step
would make the result depend on the order the emitter happened to write the
expression in.

EVERY FAILURE IS A RESULT. Division by zero returns UNDEFINED and never 0,
never infinity: a zero is a measurement and an absent value is not one.

stdlib only. CC0.
"""

from __future__ import annotations

import ast
import decimal
import re
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Sequence, Set, Tuple

try:
    from ..record import ClaimRecord, Provenance, is_literal, parse_ref
except (ImportError, ValueError):  # run as a script, not as a package
    import os
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from record import ClaimRecord, Provenance, is_literal, parse_ref

GUARD = 8

# One pass, both kinds of leaf. Numbers are placeholdered too, so a decimal
# literal in an expression becomes an exact Decimal rather than reaching the
# parser as a Python float -- which is the thing the order forbids in a value.
LEAF = re.compile(
    r"(?P<ref>[A-Za-z][A-Za-z0-9_]*(?::[A-Za-z][A-Za-z0-9_]*)?)"
    r"|(?P<num>(?:\d+\.?\d*|\.\d+)(?:[eE][+-]?\d+)?)")

_BINOPS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: "div",
    ast.Pow: "pow",
}


class Outcome(str, Enum):
    RECOMPUTED = "RECOMPUTED"
    NOT_DERIVED = "NOT_DERIVED"
    UNRESOLVED_OPERAND = "UNRESOLVED_OPERAND"
    CYCLE = "CYCLE"
    UNDEFINED = "UNDEFINED"
    UNPARSEABLE = "UNPARSEABLE"


@dataclass
class Recomputation:
    outcome: Outcome
    value: Optional[str] = None
    reason: str = ""

    def ok(self) -> bool:
        return self.outcome is Outcome.RECOMPUTED


def _placeholders(expr: str) -> Tuple[str, Dict[str, str]]:
    """Substitute every leaf for a safe name, in ONE pass.

    One pass rather than a substitution per name: sequential substitution lets
    an earlier placeholder be matched by a later pattern, and the order the
    names happen to sort in then decides the arithmetic.
    """
    mapping: Dict[str, str] = {}
    seen: Dict[str, str] = {}
    counter = [0]

    def sub(m: "re.Match") -> str:
        leaf = m.group(0)
        if leaf in seen:
            return seen[leaf]
        ph = "_op%d" % counter[0]
        counter[0] += 1
        seen[leaf] = ph
        mapping[ph] = leaf
        return ph

    return LEAF.sub(sub, expr), mapping


ALLOWED_NODES = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Name,
                 ast.Constant, ast.Load, ast.Add, ast.Sub, ast.Mult,
                 ast.Div, ast.Pow, ast.UAdd, ast.USub)


def _check_nodes(tree: ast.AST) -> None:
    """The whitelist, walked BEFORE any operand is bound.

    Order matters and it was wrong once: binding operands first made
    `abs(a)` come back UNRESOLVED_OPERAND naming `abs`, because the leaf
    substitution cannot tell a function name from a claim reference. The
    refusal was safe -- nothing was ever evaluated -- and the reason was
    false, which is the kind of wrong that survives a reading.
    """
    for n in ast.walk(tree):
        if not isinstance(n, ALLOWED_NODES):
            raise _Unparseable("node not permitted: %s" % type(n).__name__)


def _eval_node(node: ast.AST, env: Dict[str, Decimal]) -> Decimal:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body, env)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool) or not isinstance(
                node.value, (int, float)):
            raise _Unparseable("literal is not a number: %r" % (node.value,))
        if isinstance(node.value, float):
            # A float literal in the source is exactly what the order forbids
            # in a value. Refuse rather than converting it.
            raise _Unparseable(
                "float literal %r in expression; write it as a declared "
                "operand string" % node.value)
        return Decimal(node.value)
    if isinstance(node, ast.Name):
        if node.id not in env:
            raise _Unparseable("unbound name in expression: %s" % node.id)
        return env[node.id]
    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.UAdd):
            return _eval_node(node.operand, env)
        if isinstance(node.op, ast.USub):
            return -_eval_node(node.operand, env)
        raise _Unparseable("unary operator not permitted: %s"
                           % type(node.op).__name__)
    if isinstance(node, ast.BinOp):
        op = _BINOPS.get(type(node.op))
        if op is None:
            raise _Unparseable("operator not permitted: %s"
                               % type(node.op).__name__)
        a = _eval_node(node.left, env)
        b = _eval_node(node.right, env)
        if op == "div":
            if b == 0:
                raise _Undefined("division by zero")
            return a / b
        if op == "pow":
            if b != b.to_integral_value():
                raise _Unparseable(
                    "exponent must be an integer, got %s" % b)
            return a ** int(b)
        return op(a, b)
    raise _Unparseable("node not permitted: %s" % type(node).__name__)


class _Unparseable(Exception):
    pass


class _Undefined(Exception):
    pass


def recompute(rec: ClaimRecord,
              values: Dict[Tuple[str, str], str]) -> Recomputation:
    """Evaluate one DERIVED claim from operand values already in hand.

    `values` maps (sim, claim_id) -> decimal string. It is the caller's job to
    have resolved the operands; an operand missing from it returns
    UNRESOLVED_OPERAND rather than being treated as anything.
    """
    if rec.provenance is not Provenance.DERIVED:
        return Recomputation(Outcome.NOT_DERIVED,
                             reason="provenance is %s" % rec.provenance.value)
    if not rec.expression:
        return Recomputation(Outcome.UNPARSEABLE,
                             reason="DERIVED with no expression")

    safe, mapping = _placeholders(rec.expression)
    try:
        tree = ast.parse(safe, mode="eval")
        _check_nodes(tree)
    except SyntaxError as e:
        return Recomputation(Outcome.UNPARSEABLE, reason="syntax: %s" % e.msg)
    except _Unparseable as e:
        return Recomputation(Outcome.UNPARSEABLE, reason=str(e))

    used = {n.id for n in ast.walk(tree) if isinstance(n, ast.Name)}
    env: Dict[str, Decimal] = {}
    ctx = decimal.Context(prec=rec.precision + GUARD,
                          traps=[decimal.InvalidOperation, decimal.Overflow])
    for ph, name in sorted(mapping.items()):
        if ph not in used:
            continue
        if is_literal(name):
            env[ph] = Decimal(name)
            continue
        ref = parse_ref(name, rec.sim)
        if ref is None:
            return Recomputation(
                Outcome.UNPARSEABLE,
                reason="operand name is not a reference: %s" % name)
        if ref not in values:
            return Recomputation(
                Outcome.UNRESOLVED_OPERAND,
                reason="%s:%s" % ref)
        env[ph] = Decimal(values[ref])

    with decimal.localcontext(ctx):
        try:
            raw = _eval_node(tree, env)
        except _Undefined as e:
            return Recomputation(Outcome.UNDEFINED, reason=str(e))
        except _Unparseable as e:
            return Recomputation(Outcome.UNPARSEABLE, reason=str(e))
        except decimal.DecimalException as e:
            return Recomputation(Outcome.UNDEFINED,
                                 reason="decimal: %s" % type(e).__name__)
    return Recomputation(Outcome.RECOMPUTED, value=quantize(raw, rec.precision))


def quantize(value: Decimal, precision: int) -> str:
    """To `precision` significant digits. See [CHOICE 1]."""
    ctx = decimal.Context(prec=precision, rounding=decimal.ROUND_HALF_EVEN)
    return str(ctx.create_decimal(value))


def same_value(a: str, b: str, precision: int) -> bool:
    """Numeric equality at the declared precision, not string equality.

    `0.214` and `0.2140` are the same value and different strings. A ledger
    comparing strings reports a formatting change as drift.
    """
    try:
        return (Decimal(quantize(Decimal(a), precision))
                == Decimal(quantize(Decimal(b), precision)))
    except decimal.InvalidOperation:
        return False


def topo_order(records: Sequence[ClaimRecord]
               ) -> Tuple[List[ClaimRecord], List[Tuple[str, List[str]]]]:
    """Operand-graph order, plus every cycle found.

    A claim inside a cycle is returned in `cycles` and NOT in the order, so it
    is reported rather than recomputed from a value that depends on itself.
    """
    by_key = {r.key(): r for r in records}
    state: Dict[Tuple[str, str], int] = {}
    order: List[ClaimRecord] = []
    cycles: List[Tuple[str, List[str]]] = []
    in_cycle: Set[Tuple[str, str]] = set()

    def visit(key: Tuple[str, str], stack: List[Tuple[str, str]]) -> None:
        if state.get(key) == 2:
            return
        if state.get(key) == 1:
            i = stack.index(key)
            loop = stack[i:] + [key]
            cycles.append(("%s:%s" % key,
                           ["%s:%s" % k for k in loop]))
            for k in loop:
                in_cycle.add(k)
            return
        rec = by_key.get(key)
        if rec is None:
            return
        state[key] = 1
        stack.append(key)
        for o in rec.operands:
            o = o.strip()
            if is_literal(o):
                continue
            ref = parse_ref(o, rec.sim)
            if ref is not None and ref in by_key:
                visit(ref, stack)
        stack.pop()
        state[key] = 2
        order.append(rec)

    for r in records:
        visit(r.key(), [])
    return [r for r in order if r.key() not in in_cycle], cycles


def resolve_provenance(records: Sequence[ClaimRecord]
                       ) -> Dict[Tuple[str, str], Tuple[Provenance, List[str]]]:
    """Transitive provenance. DERIVED reaching a CARRIED becomes DERIVED_WEAK.

    Returns key -> (resolved provenance, the weak operands that caused it).
    An operand that is not in the record set at all is itself a weakness and
    is named: a value whose support cannot be located is not stronger than one
    whose support is CARRIED.
    """
    by_key = {r.key(): r for r in records}
    out: Dict[Tuple[str, str], Tuple[Provenance, List[str]]] = {}
    seen: Set[Tuple[str, str]] = set()

    def weak_sources(key: Tuple[str, str],
                     stack: Set[Tuple[str, str]]) -> List[str]:
        rec = by_key.get(key)
        if rec is None:
            return ["%s:%s (not in the record set)" % key]
        if rec.provenance is Provenance.CARRIED:
            return ["%s:%s (CARRIED)" % key]
        if rec.provenance is not Provenance.DERIVED:
            return []
        if key in stack:
            return ["%s:%s (cycle)" % key]
        stack = stack | {key}
        found: List[str] = []
        for o in rec.operands:
            o = o.strip()
            if is_literal(o):
                continue
            ref = parse_ref(o, rec.sim)
            if ref is None:
                found.append("%s (unparseable operand)" % o)
                continue
            for w in weak_sources(ref, stack):
                if w not in found:
                    found.append(w)
        return found

    for r in records:
        if r.provenance is not Provenance.DERIVED:
            out[r.key()] = (r.provenance, [])
            continue
        weak = weak_sources(r.key(), set())
        out[r.key()] = ((Provenance.DERIVED_WEAK, weak) if weak
                        else (Provenance.DERIVED, []))
    return out


if __name__ == "__main__":
    import sys as _s
    _s.stderr.write(
        "engine.py is a library and carries no checks of its own. Run:\n"
        "    python3 ledger/selftest_ledger.py\n")
    raise SystemExit(2)
