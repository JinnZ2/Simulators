#!/usr/bin/env python3
"""The py side of the cobol arm: compile an expression to an op stream, hand
it to GnuCOBOL, read the answers back.

The split is the point. py_ledger PARSES -- it is authoritative for
REACHABILITY, for which claims can be recomputed at all. cobol_ledger
ARITHMETICS -- it is authoritative for PRECISION. So this module does no
arithmetic: it flattens each expression to postfix and every number that
crosses the boundary crosses as a fixed-width signed decimal STRING.

WHAT IS NOT TRUE OF THIS FILE'S COMPANION: LEDGER.cob has never been
compiled and has never been run. GnuCOBOL is absent from the environment it
was written in -- `cobc` and `cobcrun` both resolve to nothing. See
MANIFEST.json. An unavailable arm is reported as UNAVAILABLE and every claim
in the run is marked PRECISION_UNVERIFIED; it is never reported as agreement.

stdlib only. CC0.
"""

from __future__ import annotations

import ast
import os
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from decimal import (Context, Decimal, InvalidOperation,
                     Overflow, localcontext)
from typing import Dict, List, Optional, Sequence, Tuple

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "LEDGER.cob")

# Fixed layout, shared with LEDGER.cob. Any change here is a change there.
W_REF = 40
W_SEQ = 4
W_KIND = 4
W_INT = 18
W_FRAC = 18
W_NUM = 1 + W_INT + W_FRAC          # sign leading separate
OP_LEN = W_REF + W_SEQ + W_KIND + W_NUM
W_STATUS = 4
OUT_LEN = W_REF + W_NUM + W_STATUS

KINDS = ("PUSH", "ADD ", "SUB ", "MUL ", "DIV ", "NEG ", "POW ", "END ")


@dataclass
class Availability:
    available: bool
    reason: str


@dataclass
class CobolRun:
    status: str                      # OK | UNAVAILABLE
    reason: str = ""
    values: Dict[Tuple[str, str], str] = field(default_factory=dict)
    statuses: Dict[Tuple[str, str], str] = field(default_factory=dict)


# ------------------------------------------------------------ availability

def compiler_version() -> Optional[str]:
    """`cobc --version`, first line. None when there is no compiler.

    Recorded per run because the addendum's exposure criterion counts
    distinct machines OR compiler versions, and neither is recoverable
    after the fact from a run that did not write it down.
    """
    cobc = shutil.which("cobc")
    if cobc is None:
        return None
    try:
        p = subprocess.run([cobc, "--version"], capture_output=True,
                           text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return None
    line = (p.stdout or p.stderr or "").strip().splitlines()
    return line[0].strip() if line else None



def availability() -> Availability:
    if not os.path.isfile(SOURCE):
        return Availability(False, "LEDGER.cob is not present")
    if shutil.which("cobcrun") is None and shutil.which("cobc") is None:
        return Availability(
            False,
            "GnuCOBOL absent: neither cobc nor cobcrun is on PATH")
    if shutil.which("cobc") is None:
        return Availability(
            False, "cobcrun is present but cobc is not; cannot build LEDGER")
    return Availability(True, "cobc on PATH at %s" % shutil.which("cobc"))


# -------------------------------------------------------- number encoding

def encode(value: str) -> Optional[str]:
    """A decimal string as sign-leading-separate S9(18)V9(18). None if it
    will not fit -- a truncated number is a wrong number."""
    try:
        d = Decimal(value)
    except InvalidOperation:
        return None
    sign = "-" if d < 0 else "+"
    d = abs(d)
    # A wide local context: quantizing a number too big for the field raises
    # InvalidOperation under the default precision, and a raise here would
    # take down a whole run over one value that simply does not fit.
    try:
        with localcontext(Context(prec=W_INT + W_FRAC + 4)):
            q = d.quantize(Decimal(1).scaleb(-W_FRAC))
    except (InvalidOperation, Overflow):
        return None
    if q != d:
        return None                  # would lose digits below 1e-18
    s = format(q, "f")
    if "." in s:
        whole, frac = s.split(".")
    else:
        whole, frac = s, ""
    if len(whole) > W_INT:
        return None
    return sign + whole.rjust(W_INT, "0") + frac.ljust(W_FRAC, "0")


def decode(text: str) -> Optional[str]:
    if len(text) != W_NUM or text[0] not in "+-":
        return None
    body = text[1:]
    if not body.isdigit():
        return None
    s = "%s%s.%s" % ("-" if text[0] == "-" else "",
                     body[:W_INT], body[W_INT:])
    try:
        return str(Decimal(s))
    except InvalidOperation:
        return None


# ------------------------------------------------------ expression -> RPN

class Unflattenable(Exception):
    pass


def to_ops(expr: str, env: Dict[str, str]) -> List[Tuple[str, str]]:
    """Postfix op stream. `env` maps leaf text -> decimal string.

    Reuses the engine's leaf substitution so the two arms cannot disagree
    about what a leaf is -- which would be a disagreement about parsing, and
    parsing is not what the cobol arm is authoritative for.
    """
    from py_ledger import engine  # local: keeps the import graph one-way

    safe, mapping = engine._placeholders(expr)
    try:
        tree = ast.parse(safe, mode="eval")
    except SyntaxError as e:
        raise Unflattenable("syntax: %s" % e.msg)

    ops: List[Tuple[str, str]] = []

    def walk(node: ast.AST) -> None:
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Name):
            leaf = mapping.get(node.id)
            if leaf is None or leaf not in env:
                raise Unflattenable("unbound leaf: %s" % (leaf or node.id))
            enc = encode(env[leaf])
            if enc is None:
                raise Unflattenable(
                    "%s does not fit S9(%d)V9(%d)" % (leaf, W_INT, W_FRAC))
            ops.append(("PUSH", enc))
            return
        if isinstance(node, ast.UnaryOp):
            walk(node.operand)
            if isinstance(node.op, ast.USub):
                ops.append(("NEG ", "+" + "0" * (W_INT + W_FRAC)))
            elif not isinstance(node.op, ast.UAdd):
                raise Unflattenable("unary %s" % type(node.op).__name__)
            return
        if isinstance(node, ast.BinOp):
            kind = {ast.Add: "ADD ", ast.Sub: "SUB ", ast.Mult: "MUL ",
                    ast.Div: "DIV ", ast.Pow: "POW "}.get(type(node.op))
            if kind is None:
                raise Unflattenable("operator %s" % type(node.op).__name__)
            walk(node.left)
            walk(node.right)
            ops.append((kind, "+" + "0" * (W_INT + W_FRAC)))
            return
        raise Unflattenable("node %s" % type(node).__name__)

    walk(tree)
    ops.append(("END ", "+" + "0" * (W_INT + W_FRAC)))
    return ops


def op_line(ref: str, seq: int, kind: str, num: str) -> str:
    if kind not in KINDS:
        raise Unflattenable("kind %r" % kind)
    return "%s%04d%s%s" % (ref[:W_REF].ljust(W_REF), seq % 10000, kind, num)


# ------------------------------------------------------------------- run

def build(workdir: str) -> Tuple[Optional[str], str]:
    exe = os.path.join(workdir, "ledger_cob")
    cobc = shutil.which("cobc")
    if cobc is None:
        return None, "cobc not on PATH"
    try:
        p = subprocess.run([cobc, "-x", "-free", "-o", exe, SOURCE],
                           capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        return None, "cobc failed to start: %s" % e
    if p.returncode != 0 or not os.path.isfile(exe):
        return None, "cobc exit %d: %s" % (p.returncode,
                                           (p.stderr or "").strip()[:400])
    return exe, "built"


def run(records: Sequence[object]) -> CobolRun:
    """Recompute every DERIVED record through GnuCOBOL."""
    from py_ledger import engine
    from record import Provenance, is_literal, parse_ref

    avail = availability()
    if not avail.available:
        return CobolRun("UNAVAILABLE", avail.reason)

    asserted = {r.key(): r.value for r in records}          # type: ignore
    lines: List[str] = []
    skipped: Dict[Tuple[str, str], str] = {}
    for r in records:
        if r.provenance is not Provenance.DERIVED or not r.expression:  # type: ignore
            continue
        env: Dict[str, str] = {}
        _, mapping = engine._placeholders(r.expression)     # type: ignore
        bad = ""
        for leaf in mapping.values():
            if is_literal(leaf):
                env[leaf] = leaf
                continue
            ref = parse_ref(leaf, r.sim)                    # type: ignore
            if ref is None or ref not in asserted:
                bad = "unresolved operand %s" % leaf
                break
            env[leaf] = asserted[ref]
        if bad:
            skipped[r.key()] = bad                          # type: ignore
            continue
        try:
            ops = to_ops(r.expression, env)                 # type: ignore
        except Unflattenable as e:
            skipped[r.key()] = str(e)                       # type: ignore
            continue
        for i, (kind, num) in enumerate(ops):
            lines.append(op_line(r.ref(), i + 1, kind, num))  # type: ignore

    if not lines:
        return CobolRun("OK", "no DERIVED claim reached the cobol arm")

    tmp = tempfile.mkdtemp(prefix="cobol_ledger_")
    exe, why = build(tmp)
    if exe is None:
        return CobolRun("UNAVAILABLE", why)
    inp = os.path.join(tmp, "OPS.DAT")
    outp = os.path.join(tmp, "RESULTS.DAT")
    with open(inp, "w", encoding="ascii") as fh:
        fh.write("\n".join(lines) + "\n")
    # LEDGER.cob names OPS.DAT and RESULTS.DAT as literals and the run is
    # cwd-bound. No DD_* variables are set: GnuCOBOL's filename mapping would
    # rewrite a literal assign name through an environment variable, and an
    # input file silently resolving somewhere else is the one failure this
    # arm could not detect.
    try:
        p = subprocess.run([exe], cwd=tmp, capture_output=True, text=True,
                           timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        return CobolRun("UNAVAILABLE", "run failed: %s" % e)
    if p.returncode != 0 or not os.path.isfile(outp):
        return CobolRun("UNAVAILABLE",
                        "exit %d: %s" % (p.returncode,
                                         (p.stderr or "").strip()[:400]))
    values: Dict[Tuple[str, str], str] = {}
    statuses: Dict[Tuple[str, str], str] = {}
    for line in open(outp, encoding="ascii"):
        line = line.rstrip("\n")
        if len(line) < OUT_LEN:
            continue
        ref = line[:W_REF].strip()
        num = line[W_REF:W_REF + W_NUM]
        st = line[W_REF + W_NUM:W_REF + W_NUM + W_STATUS].strip()
        sim, _, cid = ref.partition(":")
        key = (sim, cid)
        statuses[key] = st
        if st == "OK":
            dec = decode(num)
            if dec is not None:
                values[key] = dec
    return CobolRun("OK", "", values, statuses)


if __name__ == "__main__":
    import sys
    a = availability()
    print("cobol arm: %s" % ("AVAILABLE" if a.available else "UNAVAILABLE"))
    print("reason:    %s" % a.reason)
    sys.exit(0 if a.available else 3)
