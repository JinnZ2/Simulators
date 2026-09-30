"""
Repo-level test: every .py file in the tree compiles.

License: CC0
Dependencies: stdlib only (unittest)

The instrument that was missing. Three module-level syntax breaks sat on
main for days -- unclosed braces, a stray unindented tail spliced between
two copies of a function, a `from __future__` import pushed below a third
stacked docstring -- and were found only because tools/known_answer.py
happened to load those three files by path. A registry reaches what is
registered; it is not a scan. This is the scan.

Every failure is listed by path with the line and the message. One
declared exemption, a file the tree records as needing Python 3.12
(PEP 701 f-strings); it is compiled when the interpreter is 3.12 or later
and reported as SKIPPED with its reason otherwise, never silently passed.

The gate was committed alone, before any repair, so its first run on the
record is red -- proving it can fail is part of what it is for.

    python3 -m unittest discover tests
"""

import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKIP_DIRS = {".git", "__pycache__"}

# Declared, not inferred: the file names its own requirement (CLAUDE.md,
# relational/ entry: "requires Python 3.12+ (PEP 701 ...)").
REQUIRES_3_12 = {
    "relational/cartesian_vs_relational_demo.py",
}


def python_files(root=ROOT):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        for f in sorted(filenames):
            if f.endswith(".py"):
                yield os.path.relpath(os.path.join(dirpath, f), root)


def compile_one(rel, root=ROOT):
    """Return None if the file compiles, else (lineno, msg).

    compile() rather than ast.parse(): ast.parse does not enforce the
    `from __future__` placement rule, and that is one of the failures.
    """
    path = os.path.join(root, rel)
    with open(path, "rb") as fh:
        src = fh.read()
    try:
        compile(src, path, "exec")
    except SyntaxError as e:
        return (e.lineno, e.msg)
    return None


def sweep(root=ROOT):
    red, skipped, n = [], [], 0
    on_312 = sys.version_info >= (3, 12)
    for rel in python_files(root):
        if rel in REQUIRES_3_12 and not on_312:
            skipped.append((rel, "requires Python 3.12 (PEP 701); interpreter is %d.%d"
                            % sys.version_info[:2]))
            continue
        n += 1
        r = compile_one(rel, root)
        if r is not None:
            red.append((rel,) + r)
    return n, red, skipped


class EveryModuleCompiles(unittest.TestCase):

    def test_every_py_file_compiles(self):
        n, red, skipped = sweep()
        lines = ["compiled %d files, %d red, %d skipped" % (n, len(red), len(skipped))]
        for rel, lineno, msg in red:
            lines.append("  RED  %s:%s  %s" % (rel, lineno, msg))
        for rel, why in skipped:
            lines.append("  SKIP %s  (%s)" % (rel, why))
        report = "\n".join(lines)
        sys.stderr.write(report + "\n")
        self.assertEqual(red, [], report)

    def test_gate_can_fail(self):
        """A planted syntax error is reported by path, line and message."""
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "sub"))
            with open(os.path.join(d, "sub", "bad.py"), "w") as fh:
                fh.write("def f(:\n    pass\n")
            with open(os.path.join(d, "good.py"), "w") as fh:
                fh.write("x = 1\n")
            n, red, skipped = sweep(d)
        self.assertEqual(n, 2)
        self.assertEqual(skipped, [])
        self.assertEqual(len(red), 1)
        self.assertEqual(red[0][0], os.path.join("sub", "bad.py"))
        self.assertEqual(red[0][1], 1)


if __name__ == "__main__":
    unittest.main()
