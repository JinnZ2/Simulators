# SPDX-License-Identifier: CC0-1.0
"""
Identifier-level scan for a declared forbidden vocabulary.

Several work orders in this tree ban a class of field NAME rather than a
value: `loop-weight/` bans standing terms, `return-path/` bans the same
family plus audience size. The VOCABULARY is per-order and is declared by
the caller. The SCANNER is one object, here, because two copies of a
checker drift and the repo already has a tool that exists only because
five copies of one gate did (`tools/check_gate_drift.py`).

Why an AST walk and not a substring scan: a module and its README have to
be able to NAME the quantities they refuse, and a substring scan fires on
the sentence saying they are refused -- the checker reading its own subject
matter. Comments and free docstrings are not in the AST at all. Dict keys
are, because a field name is a field name whether it is an attribute or a
string key.

    from tools.authority_scan import scan, split_identifier
    hits = scan(open("mod.py").read(), FORBIDDEN)

A clean result means nothing unless the scanner has been shown to fire, so
every caller is expected to run `scan(PLANT, ...)` beside it.

Stdlib only. Parses under Python 3.9. CC0.
"""

from __future__ import annotations

import ast

# A caller's null test. Two hits: one identifier, one dict key.
PLANT = ("def f():\n"
         "    citation_count = 3\n"
         "    return {'author_rank': citation_count}\n")


def split_identifier(name):
    """`citation_count` and `citationCount` both split to [citation, count]."""
    parts = []
    for chunk in name.split("_"):
        current = ""
        for ch in chunk:
            if ch.isupper() and current:
                parts.append(current)
                current = ch
            else:
                current += ch
        if current:
            parts.append(current)
    return [p.lower() for p in parts if p]


def scan(source_text, forbidden):
    """Return [(identifier, token), ...] for every name carrying a banned token."""
    hits = []
    tree = ast.parse(source_text)
    for node in ast.walk(tree):
        found = []
        if isinstance(node, ast.Name):
            found = [node.id]
        elif isinstance(node, ast.Attribute):
            found = [node.attr]
        elif isinstance(node, ast.arg):
            found = [node.arg]
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            found = [node.name]
        elif isinstance(node, ast.keyword) and node.arg:
            found = [node.arg]
        elif isinstance(node, ast.Dict):
            found = [k.value for k in node.keys
                     if isinstance(k, ast.Constant) and isinstance(k.value, str)]
        for name in found:
            for token in split_identifier(name):
                if token in forbidden:
                    hits.append((name, token))
    return hits
