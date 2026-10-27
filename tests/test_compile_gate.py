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

Every failure is listed by path with the line and the message. A second
check reads the AST of every module that compiles: a top-level `def` or
`class` name bound twice in one module is a FAIL, listed by path and name
-- that is what a spliced file looks like when the splice happens to
parse (instrument-index/build_index.py: five names twice, the later
definition winning, invisible to compile()). The interpreter version is
printed on every run and in every report. One declared exemption, a file the tree records as needing Python 3.12
(PEP 701 f-strings); it is compiled when the interpreter is 3.12 or later
and reported as SKIPPED with its reason otherwise, never silently passed.

The gate was committed alone, before any repair, so its first run on the
record is red -- proving it can fail is part of what it is for.

    python3 -m unittest discover tests
"""

import ast
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


def duplicate_toplevel(rel, root=ROOT):
    """Names bound more than once by a top-level def/class in one module.

    Direct children of the module body only: a def inside `if`/`try` is a
    conditional definition and is not read. Returns [(name, [lines])].
    """
    path = os.path.join(root, rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read(), path)
    seen = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            seen.setdefault(node.name, []).append(node.lineno)
    return sorted((k, v) for k, v in seen.items() if len(v) > 1)


def interpreter():
    return "python %d.%d.%d" % sys.version_info[:3]


def sweep(root=ROOT):
    red, skipped, dupes, n = [], [], [], 0
    on_312 = sys.version_info >= (3, 12)
    for rel in python_files(root):
        if rel in REQUIRES_3_12 and not on_312:
            skipped.append((rel, "requires Python 3.12 (PEP 701); interpreter is %s"
                            % interpreter()))
            continue
        n += 1
        r = compile_one(rel, root)
        if r is not None:
            red.append((rel,) + r)
            continue
        for name, lines in duplicate_toplevel(rel, root):
            dupes.append((rel, name, lines))
    return n, red, skipped, dupes


def report(n, red, skipped, dupes):
    lines = ["compile gate under %s" % interpreter(),
             "compiled %d files, %d red, %d skipped, %d duplicate top-level names"
             % (n, len(red), len(skipped), len(dupes))]
    for rel, lineno, msg in red:
        lines.append("  RED  %s:%s  %s" % (rel, lineno, msg))
    for rel, name, at in dupes:
        lines.append("  DUP  %s  %s defined at lines %s" % (rel, name, ", ".join(map(str, at))))
    for rel, why in skipped:
        lines.append("  SKIP %s  (%s)" % (rel, why))
    return "\n".join(lines)


class EveryModuleCompiles(unittest.TestCase):

    def test_every_py_file_compiles(self):
        n, red, skipped, dupes = sweep()
        text = report(n, red, skipped, dupes)
        sys.stderr.write(text + "\n")
        self.assertEqual(red, [], text)

    def test_no_module_binds_a_toplevel_name_twice(self):
        n, red, skipped, dupes = sweep()
        text = report(n, red, skipped, dupes)
        self.assertEqual(dupes, [], text)

    def test_report_names_the_interpreter(self):
        text = report(0, [], [], [])
        self.assertIn(interpreter(), text)
        self.assertRegex(text, r"python \d+\.\d+\.\d+")

    def test_gate_can_fail(self):
        """A planted syntax error is reported by path, line and message."""
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "sub"))
            with open(os.path.join(d, "sub", "bad.py"), "w") as fh:
                fh.write("def f(:\n    pass\n")
            with open(os.path.join(d, "good.py"), "w") as fh:
                fh.write("x = 1\n")
            n, red, skipped, dupes = sweep(d)
        self.assertEqual(n, 2)
        self.assertEqual(skipped, [])
        self.assertEqual(dupes, [])
        self.assertEqual(len(red), 1)
        self.assertEqual(red[0][0], os.path.join("sub", "bad.py"))
        self.assertEqual(red[0][1], 1)

    def test_duplicate_check_can_fail_and_can_pass(self):
        """A planted duplicate def is reported by path and name with both
        lines; a clean control with the same names once, and a conditional
        redefinition inside try/except, are not."""
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "dup.py"), "w") as fh:
                fh.write("def f():\n    return 1\n\nclass K:\n    pass\n\n"
                         "def f():\n    return 2\n")
            with open(os.path.join(d, "clean.py"), "w") as fh:
                fh.write("def f():\n    return 1\n\nclass K:\n    pass\n\n"
                         "try:\n    from os import path as f\nexcept ImportError:\n"
                         "    def f():\n        return 3\n")
            n, red, skipped, dupes = sweep(d)
        self.assertEqual(red, [])
        self.assertEqual(dupes, [("dup.py", "f", [1, 7])])
        text = report(n, red, skipped, dupes)
        self.assertIn("DUP  dup.py  f defined at lines 1, 7", text)

    def test_skip_names_the_version_it_applies_under(self):
        """The PEP 701 skip fires only below 3.12 and says which interpreter
        it fired under; on 3.12+ the file is compiled instead."""
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            rel = next(iter(REQUIRES_3_12))
            os.makedirs(os.path.join(d, os.path.dirname(rel)))
            with open(os.path.join(d, rel), "w") as fh:
                fh.write("x = 1\n")
            n, red, skipped, dupes = sweep(d)
        if sys.version_info >= (3, 12):
            self.assertEqual(skipped, [])
            self.assertEqual(n, 1)
        else:
            self.assertEqual(n, 0)
            self.assertEqual(len(skipped), 1)
            self.assertIn("3.12", skipped[0][1])
            self.assertIn(interpreter(), skipped[0][1])


if __name__ == "__main__":
    unittest.main()
