#!/usr/bin/env python3
"""P2 -- substrate audit. A ledger of the contracts a piece of code
assumes at every call site, read with stdlib ast, dis and sys; one
JSONL line per (call site, layer). Nothing here argues; it counts.

    python3 p2_substrate_audit.py --target <path-or-module> --out contracts.jsonl

`verified_at_callsite` is a syntactic proxy [CHOICE 2]: the call sits
inside a try body with a handler, or its bound result is tested by the
next statement. A try/except catches a raised failure; it does not
verify a returned type, so the verified count is an upper bound on
verification and the unverified count a floor. Refuses --selftest.
"""

import argparse
import ast
import dis
import importlib.util
import json
import os
import sys

CONTRACTS = {
    "function_call": "callee returns declared type, does not corrupt caller state",
    "allocation": "allocator returns usable memory; failure to cooperate = process death",
    "numeric": "IEEE-754 guarantees held by hardware",
    "transport": "protocol peers implement the same spec",
    "compile": "emitted instructions mean what the ISA says",
}

# The counter-list from the order: adversarially NAMED, not adversarial.
ADVERSARIALLY_NAMED = [
    ("adversarial training", "gradient signal, not a contest"),
    ("attention", "weighted composition"),
    ("backpropagation", "requires every layer to faithfully pass what it computed"),
]

# [CHOICE 1] Which callees carry a second layer beside function_call.
ALLOC_NAMES = {"list", "dict", "set", "tuple", "bytearray", "bytes", "str", "frozenset", "sorted", "reversed"}
ALLOC_METHODS = {"append", "extend", "insert", "copy", "setdefault", "update", "join", "format", "split", "splitlines"}
NUMERIC_MODULES = {"math", "statistics", "cmath", "fractions", "decimal"}
NUMERIC_NAMES = {"float", "round", "sum", "abs", "pow", "divmod", "fsum"}
TRANSPORT_MODULES = {"socket", "http", "urllib", "json", "pickle", "struct", "subprocess", "ssl", "ftplib", "smtplib", "xmlrpc"}


def resolve(target):
    if os.path.exists(target):
        return os.path.abspath(target)
    spec = importlib.util.find_spec(target)
    if spec is None or not spec.origin or not spec.origin.endswith(".py"):
        raise SystemExit("cannot resolve %r to a .py source" % target)
    return spec.origin


def dotted(node):
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        base = dotted(node.value)
        return (base + "." if base else "") + node.attr
    if isinstance(node, ast.Call):
        return dotted(node.func) + "()"
    if isinstance(node, ast.Subscript):
        return dotted(node.value) + "[]"
    return "<%s>" % type(node).__name__.lower()


def layers_for(callee):
    head = callee.split(".")[0]
    tail = callee.split(".")[-1]
    out = ["function_call"]
    if head in ALLOC_NAMES or (tail in ALLOC_METHODS and "." in callee):
        out.append("allocation")
    if head in NUMERIC_MODULES or callee in NUMERIC_NAMES:
        out.append("numeric")
    if head in TRANSPORT_MODULES:
        out.append("transport")
    return out


def annotate(tree):
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            child._parent = parent


def enclosing(node):
    """Qualified name of the enclosing function, or <module>."""
    names = []
    n = getattr(node, "_parent", None)
    while n is not None:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            names.append(n.name)
        n = getattr(n, "_parent", None)
    return ".".join(reversed(names)) or "<module>"


def in_try_body(node):
    n, child = getattr(node, "_parent", None), node
    while n is not None:
        if isinstance(n, ast.Try) and n.handlers and any(child is s or _contains(s, child) for s in n.body):
            return True
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            return False
        child, n = n, getattr(n, "_parent", None)
    return False


def _contains(stmt, node):
    return any(x is node for x in ast.walk(stmt))


def result_checked_next(call):
    """Call bound to a name by Assign, and the next statement in the same
    block is an assert or if that mentions that name."""
    stmt = call._parent
    if not (isinstance(stmt, ast.Assign) and stmt.value is call and len(stmt.targets) == 1
            and isinstance(stmt.targets[0], ast.Name)):
        return False
    name = stmt.targets[0].id
    block = getattr(stmt, "_parent", None)
    for field in ("body", "orelse", "finalbody"):
        seq = getattr(block, field, None)
        if isinstance(seq, list) and any(s is stmt for s in seq):
            i = next(i for i, s in enumerate(seq) if s is stmt)
            if i + 1 < len(seq) and isinstance(seq[i + 1], (ast.Assert, ast.If)):
                test = seq[i + 1].test
                return any(isinstance(x, ast.Name) and x.id == name for x in ast.walk(test))
    return False


def call_records(tree):
    annotate(tree)
    recs, sites = [], 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        sites += 1
        callee = dotted(node.func)
        caller = enclosing(node)
        verified = in_try_body(node) or result_checked_next(node)
        for layer in layers_for(callee):
            recs.append({"caller": caller, "callee": callee, "layer": layer,
                         "contract_assumed": CONTRACTS[layer],
                         "verified_at_callsite": bool(verified), "line": node.lineno})
    return recs, sites


def compile_records(source, path):
    """One compile-layer record per code object, with the bytecode call
    count beside the ast call count so the two instruments can be read
    against each other. Never verified: nothing at this level can be."""
    code = compile(source, path, "exec")
    out = []

    def walk(co):
        ins = list(dis.get_instructions(co))
        calls = sum(1 for i in ins if i.opname.startswith("CALL") and i.opname != "PRECALL")
        out.append({"caller": co.co_name, "callee": "<bytecode>", "layer": "compile",
                    "contract_assumed": CONTRACTS["compile"], "verified_at_callsite": False,
                    "instructions": len(ins), "bytecode_calls": calls, "line": co.co_firstlineno})
        for c in co.co_consts:
            if hasattr(c, "co_code"):
                walk(c)
    walk(code)
    return out


def audit(target):
    path = resolve(target)
    with open(path, encoding="utf-8") as fh:
        source = fh.read()
    tree = ast.parse(source)
    recs, sites = call_records(tree)
    comp = compile_records(source, path)
    ast_calls = sites
    bc_calls = sum(r["bytecode_calls"] for r in comp)
    unverified = sum(1 for r in recs + comp if not r["verified_at_callsite"])
    by_layer = {}
    for r in recs + comp:
        d = by_layer.setdefault(r["layer"], {"records": 0, "unverified": 0})
        d["records"] += 1
        d["unverified"] += 0 if r["verified_at_callsite"] else 1
    return {
        "target": os.path.relpath(path) if path.startswith(os.getcwd()) else path,
        "python": "%d.%d" % sys.version_info[:2],
        "total_callsites": sites, "records": len(recs) + len(comp),
        "unverified_contracts": unverified,
        "ratio_unverified_over_callsites": (unverified / sites) if sites else None,
        "by_layer": by_layer, "ast_calls": ast_calls, "bytecode_calls": bc_calls,
        "instruments_agree_on_call_count": ast_calls == bc_calls,
        "records_list": recs + comp,
    }


def render(res):
    lines = ["P2 substrate audit: %s (python %s)" % (res["target"], res["python"])]
    lines.append("call sites (ast) %d   bytecode CALL* %d   agree: %s" % (
        res["ast_calls"], res["bytecode_calls"], res["instruments_agree_on_call_count"]))
    for layer in CONTRACTS:
        d = res["by_layer"].get(layer, {"records": 0, "unverified": 0})
        lines.append("  %-14s records %4d  unverified %4d   %s" % (layer, d["records"], d["unverified"], CONTRACTS[layer]))
    r = res["ratio_unverified_over_callsites"]
    lines.append("unverified_contracts / total_callsites = %d / %d = %s" % (
        res["unverified_contracts"], res["total_callsites"], "%.3f" % r if r is not None else "undefined (no call sites)"))
    lines.append("verified_at_callsite is a syntactic proxy [CHOICE 2]; the unverified count is a floor")
    lines.append("adversarially NAMED, not adversarial:")
    for a, b in ADVERSARIALLY_NAMED:
        lines.append("  %-22s -> %s" % (a, b))
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--target")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        print("p2_substrate_audit has no selftest; run selftest_csp.py", file=sys.stderr)
        return 2
    if not a.target:
        print("--target PATH-OR-MODULE is required", file=sys.stderr)
        return 2
    res = audit(a.target)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            for r in res["records_list"]:
                fh.write(json.dumps(r, sort_keys=True) + "\n")
    print(render(res))
    return 0


if __name__ == "__main__":
    sys.exit(main())
