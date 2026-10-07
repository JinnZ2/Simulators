#!/usr/bin/env python3
"""P2 -- SUBSTRATE CHECK. Code introspection: the module reads Python
source with the standard library's own parser, reads nothing else, and
by default reads ITSELF.

The order's question: can adversarial code produce the reasoning chains
necessary for its own existence? The check makes the question countable
rather than arguing it.

    CALL CONTRACTS. Every call site is a contract the caller cannot
    verify. The caller assumes the callee returns what its name implies,
    in the shape the caller will use, having left shared state as the
    caller left it. A call is counted LOCALLY_CHECKED only in two narrow
    forms -- it sits inside an `assert`, or it is an operand of a
    comparison in a branch test -- and even then only ONE clause of the
    contract is bounded: a checked return says nothing about what the
    callee did to shared state on the way. The other clauses are
    unbounded at every call site in the file, including the checked
    ones. So the reported fraction is a CEILING on verification, not a
    measurement of trust.

    LAYER CONTRACTS. The contracts the order names that are not call
    sites: the allocator, IEEE-754 arithmetic, the network stack, the
    scheduler, the compiler, the hardware. Each is listed with the
    failure mode if the layer defected. None is checkable from inside
    the process, and that is the entry, not a gap in the entry.

    NAMING. Adversarially-named parts are not adversarial. The glossary
    is DECLARED and closed: a token in it is mapped to the mechanical
    requirement the name stands for, and a token not in it returns
    UNMAPPED. Nothing is mapped by resemblance, so the glossary cannot
    quietly grow to fit whatever it is pointed at.

    EXISTENCE PROOF. Checkable against itself in the narrow sense the
    order's phrase allows: the file analysed is the file that produced
    the output, its sha256 is printed beside the reading, and the
    analysis ran. Every contract listed had to hold for the output to
    exist at all. The scope is this run, on this machine, at this
    digest -- not a claim about code in general, and not a claim that
    any of these layers is trustworthy. It is the weaker and checkable
    claim: THIS output is evidence that these contracts held here.

    python3 p2_substrate.py                 # reads its own source
    python3 p2_substrate.py --file X.py

Refuses --selftest; checks live in test_proof.py.
"""

import ast
import hashlib
import os
import sys

import scope

UNVERIFIED = "UNVERIFIED"
LOCALLY_CHECKED = "LOCALLY_CHECKED"
UNMAPPED = "UNMAPPED"

# The contracts that are not call sites. `checkable_from_inside` is
# False on every row and that is the reading, not an omission: a process
# cannot step outside itself to audit the allocator that gave it its own
# stack.
LAYERS = (
    ("allocator",
     "memory is handed back on request and is not handed to two holders",
     "the process dies; there is no degraded mode to report from"),
    ("ieee754",
     "arithmetic follows the declared format and rounding",
     "every numeric result is wrong by an unknown amount, silently"),
    ("network_stack",
     "bytes offered in order arrive in order or not at all",
     "a message reads as a different message; no local check sees it"),
    ("scheduler",
     "a runnable thread eventually runs",
     "the process stops without an error, indistinguishable from slow"),
    ("compiler",
     "emitted instructions implement the source as written",
     "the source under review is not the program that ran"),
    ("hardware",
     "an instruction does what its specification says",
     "nothing above it means anything; no software check is above it"),
)

# [CHOICE 1] the glossary is CLOSED. These are the order's own three
# examples plus two the same argument reaches; anything else is
# UNMAPPED. A glossary that grows by resemblance would end up asserting
# whatever it was pointed at.
GLOSSARY = {
    "adversarial training":
        "a gradient signal; the generator and the scorer must agree on "
        "the loss surface or no gradient exists",
    "attention":
        "a weighted composition; the weights must sum over values that "
        "are delivered faithfully or the composition is of nothing",
    "backpropagation":
        "requires each layer to report its output faithfully to the "
        "layer that consumes it; a lying layer breaks its own gradient",
    "competition":
        "a ranking over a shared scale; the scale must mean the same "
        "thing to every ranked party or the ranking is not one",
    "loss":
        "a scalar objective; the objective must be the same one at "
        "every step or the steps do not compose",
}


def sha256_of(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def call_name(node):
    """Best-effort dotted name for a call target. Returns None when the
    target is computed, which is itself a contract the caller cannot
    verify -- recorded as such rather than guessed at."""
    f = node.func
    parts = []
    while isinstance(f, ast.Attribute):
        parts.append(f.attr)
        f = f.value
    if isinstance(f, ast.Name):
        parts.append(f.id)
        return ".".join(reversed(parts))
    return None


def _checked_calls(tree):
    """Call nodes in one of the two narrow checked forms."""
    out = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert):
            for sub in ast.walk(node.test):
                if isinstance(sub, ast.Call):
                    out.add(id(sub))
        elif isinstance(node, (ast.If, ast.While)):
            for sub in ast.walk(node.test):
                if isinstance(sub, ast.Compare):
                    for operand in [sub.left] + list(sub.comparators):
                        for inner in ast.walk(operand):
                            if isinstance(inner, ast.Call):
                                out.add(id(inner))
    return out


def call_contracts(source):
    """Enumerate every call site with its status."""
    tree = ast.parse(source)
    checked = _checked_calls(tree)
    rows = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        rows.append({
            "line": getattr(node, "lineno", 0),
            "target": call_name(node) or "<computed>",
            "status": LOCALLY_CHECKED if id(node) in checked else UNVERIFIED,
        })
    rows.sort(key=lambda r: (r["line"], r["target"]))
    return rows


def unverified_fraction(rows):
    """UNVERIFIED / total, or None on no call sites.

    None is not zero: a file with no calls has nothing to report, and
    reporting 0.0 would read as a file whose every contract is checked.
    """
    if not rows:
        return None
    n = sum(1 for r in rows if r["status"] == UNVERIFIED)
    return float(n) / float(len(rows))


def gloss(token):
    """Closed lookup. UNMAPPED is a state, not a failure."""
    key = (token or "").strip().lower()
    return GLOSSARY.get(key, UNMAPPED)


# Code analysis is not a contest: no win condition, no scalar, no fixed
# resource set. Coded rather than assumed, and the OUTSIDE verdict is
# the point -- the frame does not cover this reading.
ANALYSIS_SCOPE = {
    "window": 2.0, "coupling_time": 1.0,
    "window_unit": "run", "coupling_unit": "run",
    "C2": False, "C3": False, "C4": False,
}


def render(path, rows, digest):
    frac = unverified_fraction(rows)
    lines = []
    lines.append("P2 SUBSTRATE CHECK")
    lines.append("")
    lines.append("  file:   %s" % path)
    lines.append("  sha256: %s" % digest)
    lines.append("")
    lines.append("  CALL CONTRACTS")
    lines.append("    call sites:       %d" % len(rows))
    lines.append("    locally checked:  %d"
                 % sum(1 for r in rows if r["status"] == LOCALLY_CHECKED))
    lines.append("    unverified:       %d"
                 % sum(1 for r in rows if r["status"] == UNVERIFIED))
    lines.append("    unverified share: %s"
                 % ("--" if frac is None else "%.4f" % frac))
    lines.append("    computed targets: %d"
                 % sum(1 for r in rows if r["target"] == "<computed>"))
    lines.append("")
    lines.append("    A checked return bounds ONE clause of the contract.")
    lines.append("    Shared state is unbounded at every call site above,")
    lines.append("    the checked ones included, so the share is a ceiling")
    lines.append("    on verification and not a measurement of trust.")
    lines.append("")
    lines.append("  LAYER CONTRACTS (none checkable from inside)")
    head = "    %-15s %-52s %s" % ("layer", "assumed", "if it defected")
    lines.append(head)
    lines.append("    " + "-" * (len(head) - 4))
    for name, assumed, failure in LAYERS:
        lines.append("    %-15s %-52s %s" % (name, assumed, failure))
    lines.append("")
    lines.append("  NAMING (closed glossary; anything else is UNMAPPED)")
    for token in sorted(GLOSSARY):
        lines.append("    %-22s %s" % (token, GLOSSARY[token]))
    lines.append("    %-22s %s" % ("<any other token>", UNMAPPED))
    lines.append("")
    lines.append("  EXISTENCE PROOF, scoped")
    lines.append("    This output exists. Producing it required every call")
    lines.append("    contract above to have been honoured and every layer")
    lines.append("    contract above to have held, on this machine, for")
    lines.append("    this run, on the file at the digest above. That is")
    lines.append("    the whole claim. It is not a claim that any layer is")
    lines.append("    trustworthy, and not a claim about code in general.")
    lines.append("")
    sr = scope.code(ANALYSIS_SCOPE)
    lines.append("  scope coding (C1-C4): %s" % sr["verdict"])
    lines.append("  %s" % sr["reading"])
    return "\n".join(lines)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write(
            "p2_substrate.py does not carry its own checks.\n"
            "Run: python3 test_proof.py\n")
        return 2
    if "--choices" in argv:
        sys.stdout.write("[CHOICE 1] glossary is closed, %d entries\n"
                         % len(GLOSSARY))
        return 0
    path = os.path.abspath(__file__)
    for i, a in enumerate(argv):
        if a == "--file" and i + 1 < len(argv):
            path = argv[i + 1]
    with open(path, "r", encoding="utf-8") as fh:
        source = fh.read()
    rows = call_contracts(source)
    sys.stdout.write(render(path, rows, sha256_of(path)) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
