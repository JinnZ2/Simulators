#!/usr/bin/env python3
# CC0 1.0 Universal. No rights reserved.
"""gate_check.py — four structural presence/absence checks over a repo path.

    python3 gate_check.py [repo_path] [--json]

Reports presence or absence of four structural features, with file and
line. It does not diagnose why, does not judge correctness, and reads no
framework. Thresholds are not in this file: it reads thresholds.txt beside
itself (or in the repo root) and never writes it or threshold_chain.txt.

Labels (from the work order; the per-check mapping onto them is the
BUILDER'S DERIVATION, not part of the order — see derive()):
    HELD_RETRIEVABLE    feature present and locatable (file + line)
    HELD_UNRETRIEVABLE  feature present but not pinnable to a location
    NOT_HELD            feature absent
    OUT_OF_ENVELOPE     check does not apply to this artifact
There is no FAIL label.
"""

import ast
import json
import os
import re
import sys
import tokenize

SOURCE_EXT = (".py", ".sh", ".js", ".ts", ".go", ".rs", ".c", ".h", ".cpp", ".java", ".rb")
PROSE_EXT = (".md", ".txt", ".rst")
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "build", "dist"}

# CHECK 1: the three tokens the order names, in identifier / hyphen / space form.
UNKNOWN_TOKENS = re.compile(r"\b(UNKNOWN|BLOCKED|OUT[_\- ]OF[_\- ]ENVELOPE)\b", re.IGNORECASE)
# CHECK 2 (non-Python): an abort/exit/throw on a line that also carries a condition keyword.
KILL_LINE = re.compile(r"\b(if|unless|when|case)\b.*\b(exit|abort|throw|raise|die|panic|return null|return nil)\b", re.IGNORECASE)
# CHECK 3: an assertion counts as sitting on a failure/null path when its line carries one of these.
FAILURE_WORDS = re.compile(r"\b(None|null|nil|raise|Raises|error|Error|fail|fails|failed|void|empty|refus\w*|reject\w*|"
                           r"block\w*|unknown|invalid|missing|absent|not_?found|abort\w*|exit)\b")
INPUT_READ = re.compile(r"sys\.argv|argparse|input\(|open\(|stdin|environ|getenv|read_jsonl|\.read\(")
DEMO_NAME = re.compile(r"(demo|example|sample)", re.IGNORECASE)


def walk(root):
    for dirpath, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for f in sorted(files):
            yield os.path.join(dirpath, f)


def rel(root, path):
    return os.path.relpath(path, root)


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def py_tree(text, path):
    try:
        return ast.parse(text, path)
    except (SyntaxError, ValueError):
        return None


def docstring_lines(tree):
    lines = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body:
            first = node.body[0]
            if isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant) \
                    and isinstance(first.value.value, str):
                lines.update(range(first.lineno, getattr(first, "end_lineno", first.lineno) + 1))
    return lines


def comment_lines(text):
    lines = set()
    try:
        for tok in tokenize.generate_tokens(iter(text.splitlines(True)).__next__):
            if tok.type == tokenize.COMMENT:
                lines.add(tok.start[0])
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    return lines


# ---------------------------------------------------------------- CHECK 1
def check_unknown_path(root, files):
    """First occurrence of an unknown/blocked/out-of-envelope token. In code
    (identifier or string in a statement) -> retrievable; only in comments,
    docstrings or prose -> unretrievable (a mention, not a path)."""
    code_hit, prose_hit = None, None
    for path in files:
        text = read(path)
        ext = os.path.splitext(path)[1]
        if ext == ".py":
            tree = py_tree(text, path)
            skip = (docstring_lines(tree) if tree else set()) | comment_lines(text)
        else:
            skip = set()
        for n, line in enumerate(text.splitlines(), 1):
            if not UNKNOWN_TOKENS.search(line):
                continue
            if ext in PROSE_EXT or n in skip:
                prose_hit = prose_hit or (rel(root, path), n)
            elif ext in SOURCE_EXT and code_hit is None:
                code_hit = (rel(root, path), n)
        if code_hit:
            break
    return derive(code_hit, prose_hit)


# ---------------------------------------------------------------- CHECK 2
def _if_kills(node):
    for stmt in ast.walk(node):
        if isinstance(stmt, ast.Raise):
            return True
        if isinstance(stmt, ast.Return) and (stmt.value is None or (isinstance(stmt.value, ast.Constant) and stmt.value.value is None)):
            return True
        if isinstance(stmt, ast.Call):
            name = ast.unparse(stmt.func) if hasattr(ast, "unparse") else ""
            if name in ("sys.exit", "exit", "abort", "os._exit", "quit"):
                return True
    return False


def check_kill_rule(root, files):
    """A conditional whose body returns nothing, raises, or exits. Python by
    AST (If node with such a body); other source by a one-line regex; prose
    that states a kill rule in words -> unretrievable."""
    code_hit, prose_hit = None, None
    for path in files:
        text = read(path)
        ext = os.path.splitext(path)[1]
        if ext == ".py":
            tree = py_tree(text, path)
            if tree:
                for node in ast.walk(tree):
                    if isinstance(node, ast.If) and any(_if_kills(b) for b in node.body):
                        code_hit = (rel(root, path), node.lineno)
                        break
        elif ext in SOURCE_EXT:
            for n, line in enumerate(text.splitlines(), 1):
                if KILL_LINE.search(line):
                    code_hit = (rel(root, path), n)
                    break
        elif ext in PROSE_EXT and prose_hit is None:
            for n, line in enumerate(text.splitlines(), 1):
                if re.search(r"\b(kill rule|refuse|refuses|void|abort|returns nothing)\b", line, re.IGNORECASE):
                    prose_hit = (rel(root, path), n)
                    break
        if code_hit:
            break
    return derive(code_hit, prose_hit)


# ---------------------------------------------------------------- CHECK 3
def _is_assertion(node):
    if isinstance(node, ast.Assert):
        return True
    if isinstance(node, ast.Call):
        name = ast.unparse(node.func) if hasattr(ast, "unparse") else ""
        last = name.split(".")[-1]
        return last.startswith("assert") or last == "check"
    return False


def check_tests_failure(root, files):
    """Count assertions on failure/null paths in test files: inside a
    with-assertRaises/pytest.raises block, or an assertRaises/assertIsNone/
    assertFalse call, or an assertion whose own line carries a FAILURE_WORD.
    Returns count and present as SEPARATE values. No threshold here."""
    count, first = 0, None
    for path in files:
        base = os.path.basename(path)
        if not base.endswith(".py"):
            continue
        text = read(path)
        named_test = base.startswith("test_") or base.endswith("_test.py") or "selftest" in base
        if not named_test and not re.search(r"^def (selftest|self_test)\b", text, re.M):
            continue  # a test file by name, or a module carrying a selftest function
        tree = py_tree(text, path)
        if not tree:
            continue
        lines = text.splitlines()
        raises_ranges = []
        for node in ast.walk(tree):
            if isinstance(node, ast.With):
                for item in node.items:
                    src = ast.unparse(item.context_expr) if hasattr(ast, "unparse") else ""
                    if "assertRaises" in src or "pytest.raises" in src or "raises(" in src:
                        raises_ranges.append((node.lineno, getattr(node, "end_lineno", node.lineno)))
        for node in ast.walk(tree):
            if not _is_assertion(node):
                continue
            line = lines[node.lineno - 1] if node.lineno - 1 < len(lines) else ""
            name = ast.unparse(node.func).split(".")[-1] if isinstance(node, ast.Call) and hasattr(ast, "unparse") else ""
            hit = (any(a <= node.lineno <= b for a, b in raises_ranges)
                   or name in ("assertRaises", "assertRaisesRegex", "assertIsNone", "assertFalse")
                   or bool(FAILURE_WORDS.search(line)))
            if hit:
                count += 1
                first = first or (rel(root, path), node.lineno)
    result = derive(first, None)
    result.update({"count": count, "present": count > 0})
    return result


# ---------------------------------------------------------------- CHECK 4
def check_demo_can_fail(root, files):
    """Demo/example files by name. Reads an input AND holds a kill-shaped
    conditional -> retrievable. Reads an input, no such conditional ->
    NOT_HELD. No demo reads any input (the demo is the whole artifact) ->
    OUT_OF_ENVELOPE. No demo file at all -> NOT_HELD."""
    demos = [p for p in files if p.endswith(".py") and DEMO_NAME.search(rel(root, p))]
    if not demos:
        return dict(derive(None, None), detail="no demo or example file located by name")
    any_input, kill = None, None
    for path in demos:
        text = read(path)
        tree = py_tree(text, path)
        for n, line in enumerate(text.splitlines(), 1):
            if INPUT_READ.search(line):
                any_input = any_input or (rel(root, path), n)
                break
        if tree and any_input and any_input[0] == rel(root, path):
            for node in ast.walk(tree):
                if isinstance(node, ast.If) and any(_if_kills(b) for b in node.body):
                    kill = (rel(root, path), node.lineno)
                    break
        if kill:
            break
    if any_input is None:
        return {"label": "OUT_OF_ENVELOPE", "location": None,
                "detail": "%d demo file(s), none reads an input; no input under which it could not succeed" % len(demos)}
    return dict(derive(kill, None), detail="input read at %s:%d" % any_input)


# ---------------------------------------------------------------- labels
def derive(code_hit, prose_hit):
    """BUILDER'S DERIVATION (not in the order): a code location -> HELD_RETRIEVABLE;
    only a mention in prose/comment/docstring -> HELD_UNRETRIEVABLE with the
    mention's location reported as `mention`; neither -> NOT_HELD."""
    if code_hit:
        return {"label": "HELD_RETRIEVABLE", "location": "%s:%d" % code_hit}
    if prose_hit:
        return {"label": "HELD_UNRETRIEVABLE", "location": None, "mention": "%s:%d" % prose_hit}
    return {"label": "NOT_HELD", "location": None}


# ---------------------------------------------------------------- thresholds
def read_thresholds(root):
    """Reads thresholds.txt from beside this script, else from the repo root.
    Missing -> {} (not an error). Never writes."""
    for candidate in (os.path.join(os.path.dirname(os.path.abspath(__file__)), "thresholds.txt"),
                      os.path.join(root, "thresholds.txt")):
        if os.path.isfile(candidate):
            out = {}
            for line in read(candidate).splitlines():
                line = line.split("#", 1)[0].strip()
                if "=" in line:
                    k, v = (s.strip() for s in line.split("=", 1))
                    out[k] = v
            return out, candidate
    return {}, None


def run(root):
    files = [p for p in walk(root) if os.path.splitext(p)[1] in SOURCE_EXT + PROSE_EXT]
    thresholds, src = read_thresholds(root)
    c3 = check_tests_failure(root, files)
    t = thresholds.get("check3_failure_assertions_min")
    c3["threshold"] = int(t) if t is not None and t.lstrip("-").isdigit() else None
    c3["at_or_above_threshold"] = None if c3["threshold"] is None else c3["count"] >= c3["threshold"]
    return {"repo": os.path.abspath(root), "files_scanned": len(files), "thresholds_file": src,
            "checks": {"1_unknown_return_path": check_unknown_path(root, files),
                       "2_kill_rule": check_kill_rule(root, files),
                       "3_tests_cover_failure": c3,
                       "4_demo_can_fail": check_demo_can_fail(root, files)}}


def render(result):
    out = ["repo: %s  files_scanned: %d  thresholds: %s" % (result["repo"], result["files_scanned"], result["thresholds_file"] or "absent")]
    for key, r in result["checks"].items():
        extra = " ".join("%s=%s" % (k, v) for k, v in r.items() if k not in ("label", "location"))
        out.append("%-24s %-19s %s %s" % (key, r["label"], r.get("location") or "-", extra))
    return "\n".join(out)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = args[0] if args else "."
    if not os.path.isdir(root):
        print("not a directory: %s" % root, file=sys.stderr)
        sys.exit(2)
    result = run(root)
    print(json.dumps(result, indent=1) if "--json" in sys.argv else render(result))
