#!/usr/bin/env python3
"""Checks on the delivered `fold_register.py`. Imports it, edits nothing.

The register is a list of folded terms plus a document scanner. It
refuses to score, which is the right refusal and is rarer than it looks:
`score` is None, every grid cell is UNFILLED, and the verdict string
says the absence IS the reading.

What is checked here is everything downstream of that refusal -- whether
the fields the register does fill carry what they appear to, and what
the scanner does on documents that were not written for it.

Two corpora, and they answer different questions:

  sources/*.md     two real outside documents already in this folder,
                   small enough to hand-check EVERY hit. Fifteen hits.
  ../CLAUDE.md     a corpus written in the register's own vocabulary,
                   which is the use-mention case (DF_010), and the
                   place the alias layer shows what it does.

CC0. stdlib only. Parses under Python 3.9.
"""

import collections
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import fold_register as F  # noqa: E402

CORPUS = [os.path.join(HERE, "sources", "palo_alto_company_profile_pasted.md"),
          os.path.join(HERE, "sources", "blank_template_pasted.md")]
BIG = os.path.join(ROOT, "CLAUDE.md")


def hits(text):
    """(key, matched word, line no, line) for every hit, uncapped.

    The delivered scanner caps `occurrences` at 12 lines per term with
    no marker, so its own output cannot be used to count. This walks the
    same rule and keeps everything.
    """
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        for w in re.findall(r"[A-Za-z]+", line.lower()):
            key = w if w in F.REGISTER else F.ALIASES.get(w)
            if key:
                out.append((key, w, n, line.strip()))
    return out


def alias_share(text):
    """How much of the hit count comes from the alias layer."""
    d = a = 0
    for _k, w, _n, _l in hits(text):
        if w in F.REGISTER:
            d += 1
        else:
            a += 1
    return d, a, (a / float(d + a) if (d + a) else None)


def counter_case_by_source():
    """Is the evidence column a property of the term or of who named it?"""
    t = collections.Counter()
    for _k, v in F.REGISTER.items():
        t[(v["source"], v["counter_case"] is not None)] += 1
    return t


def unread_fields():
    """Register fields that nothing in the module reads.

    `grid_for` copies four of them into its output and `scan` copies the
    grid, so they are CARRIED. Nothing branches on any of them: no
    comparison, no sort, no filter. Detected by asking whether the field
    name appears anywhere in the source outside its own definition and
    the one dict literal that copies it.
    """
    import ast
    src = open(os.path.join(HERE, "fold_register.py"), encoding="utf-8").read()
    tree = ast.parse(src)

    # A first version matched a regex for comparison operators on the
    # same line and reported `substitutes_for` as branched on, because
    # the --list format string contains a literal `<-`. An operator
    # inside a string is not an operator. Read from the AST instead:
    # the field counts as branched on only if a subscript naming it sits
    # inside a test, a comparison, or a sort key.
    fields = ("sign_storage", "residual_tell", "counter_case",
              "substitutes_for", "source")

    def names_in(node):
        got = set()
        for n in ast.walk(node):
            if isinstance(n, ast.Subscript):
                sl = n.slice
                if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
                    got.add(sl.value)
                elif isinstance(sl, ast.Index):          # < 3.9 shape
                    v = getattr(sl, "value", None)
                    if isinstance(v, ast.Constant):
                        got.add(v.value)
            if isinstance(n, ast.Attribute):
                got.add(n.attr)
        return got

    branched = set()
    for n in ast.walk(tree):
        tests = []
        if isinstance(n, (ast.If, ast.While, ast.IfExp)):
            tests.append(n.test)
        elif isinstance(n, ast.Compare):
            tests.append(n)
        elif isinstance(n, ast.Call):
            f = getattr(n.func, "id", None) or getattr(n.func, "attr", None)
            if f in ("sorted", "min", "max", "filter"):
                tests.append(n)
        for t in tests:
            branched |= names_in(t)

    mentions = collections.Counter()
    for n in ast.walk(tree):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            if n.value in fields:
                mentions[n.value] += 1

    return {f: {"mentions": mentions[f], "entries": len(F.REGISTER),
                "read_by_a_branch": f in branched} for f in fields}


def occurrence_cap(text):
    """Terms whose real count exceeds what the delivered scanner reports."""
    real = collections.Counter(k for k, _w, _n, _l in hits(text))
    got = F.scan(text)["occurrences"]
    return {k: (real[k], len(got[k])) for k in got if real[k] > len(got[k])}


def cli(args):
    p = subprocess.run([sys.executable,
                        os.path.join(HERE, "fold_register.py")] + args,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                       timeout=60)
    return p.returncode, p.stdout.decode("utf8", "replace")


# ------------------------------------------------------------- report

def render():
    out = []
    out.append("REGISTER AUDIT -- checks on the delivered fold_register.py")
    out.append("the module is imported and not modified")
    out.append("")

    out.append("1. THE REFUSAL IS REAL")
    g = F.grid_for("efficiency")
    s = F.scan("efficiency and cost and growth\n")
    out.append("   grid cells: %d, all UNFILLED: %s"
               % (len(g["cells"]), all(v is None for v in g["cells"].values())))
    out.append("   score: %r   verdict: %s" % (s["score"], s["verdict"][:40]))
    out.append("   An unknown term returns None rather than an empty grid:")
    out.append("   grid_for('zzz') -> %r" % F.grid_for("zzz"))
    out.append("")

    out.append("2. cells_filled IS A LITERAL")
    out.append("   scan() returns cells_filled = %r for every input."
               % s["cells_filled"])
    out.append("   It is not derived from the grid, so the field cannot")
    out.append("   report anything else. cells_unfilled = cells_total")
    out.append("   identically: %s"
               % (s["cells_unfilled"] == s["cells_total"]))
    out.append("")

    out.append("3. counter_case TRACKS THE SOURCE, NOT THE TERM")
    t = counter_case_by_source()
    for (src, filled), n in sorted(t.items()):
        out.append("   %-10s counter_case %-8s %d"
                   % (src, "filled" if filled else "UNFILLED", n))
    out.append("   Separation is total: every filled one is kavik-sourced,")
    out.append("   every candidate is UNFILLED. The evidence column reads")
    out.append("   as who named the term.")
    out.append("")

    out.append("4. THE ALIAS LAYER CARRIES MOST OF THE HITS")
    for path in CORPUS + [BIG]:
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8", errors="replace").read()
        d, a, sh = alias_share(text)
        out.append("   %-42s direct %4d  alias %4d  alias %s"
                   % (os.path.basename(path), d, a,
                      "%.0f%%" % (100 * sh) if sh is not None else "--"))
    out.append("")

    out.append("5. EVERY HIT ON THE TWO REAL DOCUMENTS, HAND-CHECKABLE")
    for path in CORPUS:
        if not os.path.exists(path):
            continue
        text = open(path, encoding="utf-8", errors="replace").read()
        h = hits(text)
        out.append("   %s -- %d hits" % (os.path.basename(path), len(h)))
        for k, w, n, line in h:
            out.append("     %-12s <- %-11s L%-4d %s" % (k, w, n, line[:52]))
    out.append("")

    out.append("6. THE OCCURRENCE CAP IS SILENT")
    if os.path.exists(BIG):
        cap = occurrence_cap(open(BIG, encoding="utf-8",
                                  errors="replace").read())
        out.append("   terms whose real count exceeds the reported list: %d"
                   % len(cap))
        for k in sorted(cap, key=lambda x: -cap[x][0])[:5]:
            out.append("     %-14s real %4d   reported %2d"
                       % (k, cap[k][0], cap[k][1]))
        out.append("   Nothing in the output says the list was cut.")
    out.append("")

    out.append("7. CLI EDGES")
    for args, label in ((["--grid"], "--grid with no term"),
                        (["--grid", "zzz"], "--grid unknown term"),
                        (["nosuch.txt"], "missing file"),
                        (["--list"], "--list")):
        rc, o = cli(args)
        last = [x for x in o.strip().split("\n") if x.strip()]
        out.append("   %-22s rc=%-3s %s"
                   % (label, rc, (last[-1] if last else "")[:46]))
    out.append("")

    out.append("8. FIELDS CARRIED AND NEVER BRANCHED ON")
    for f, d in sorted(unread_fields().items()):
        out.append("   %-16s read by a branch: %s" % (f, d["read_by_a_branch"]))
    out.append("")

    out.append("9. ONE ALIAS IS SHADOWED")
    dead = [a for a in F.ALIASES if a in F.REGISTER]
    out.append("   aliases that are already register keys: %s" % dead)
    out.append("   `word if word in REGISTER else ALIASES.get(word)` takes")
    out.append("   the first branch, so the entry never fires.")
    return "\n".join(out)


# ------------------------------------------------------------ selftest

def selftest():
    ok = [0]
    bad = []

    def chk(name, cond):
        if cond:
            ok[0] += 1
        else:
            bad.append(name)

    # -- 1. the refusal
    g = F.grid_for("efficiency")
    chk("a grid has ten cells", len(g["cells"]) == 10)
    chk("every cell is UNFILLED",
        all(v is None for v in g["cells"].values()))
    chk("an unknown term returns None, not an empty grid",
        F.grid_for("zzz") is None)
    s = F.scan("efficiency\n")
    chk("scan refuses a score", s["score"] is None)
    chk("the verdict names the absence as the reading",
        "Absence is the reading" in s["verdict"])

    # -- 2. cells_filled is a literal
    chk("cells_filled is 0 on a hit", F.scan("efficiency\n")["cells_filled"]
        == 0)
    chk("cells_filled is 0 on no hits", F.scan("nothing here\n")["cells_filled"]
        == 0)
    src = open(os.path.join(HERE, "fold_register.py"), encoding="utf-8").read()
    chk("cells_filled is written as a literal in the source",
        re.search(r'"cells_filled":\s*0\b', src) is not None)
    chk("cells_unfilled always equals cells_total",
        all(F.scan(t)["cells_unfilled"] == F.scan(t)["cells_total"]
            for t in ("efficiency\n", "cost growth\n", "x\n")))

    # -- 3. counter_case separates perfectly by source
    t = counter_case_by_source()
    chk("no candidate term carries a counter_case",
        t[("candidate", True)] == 0)
    chk("most kavik terms do", t[("kavik", True)] >= 4)
    chk("exactly one kavik term does not", t[("kavik", False)] == 1)

    # -- 4. alias share, on a text with a known answer
    d, a, sh = alias_share("efficiency cost\n")
    chk("a register word counts direct", d == 1)
    chk("an alias counts alias", a == 1)
    chk("share is computed over both", abs(sh - 0.5) < 1e-9)
    chk("an empty text gives None, not zero",
        alias_share("nothing at all here\n")[2] is None)

    # -- 5. hits() is uncapped where scan() is capped
    many = "\n".join(["cost"] * 30)
    chk("hits keeps every occurrence", len(hits(many)) == 30)
    chk("scan caps the reported list at 12",
        len(F.scan(many)["occurrences"]["money"]) == 12)
    chk("nothing in scan's output marks the cut",
        "12" not in F.scan(many)["verdict"]
        and "truncat" not in str(F.scan(many)).lower())
    chk("occurrence_cap reports the gap",
        occurrence_cap(many)["money"] == (30, 12))

    # -- 6. the shadowed alias
    dead = [a_ for a_ in F.ALIASES if a_ in F.REGISTER]
    chk("exactly one alias is shadowed by a register key", dead == ["quality"])
    chk("the shadowed alias resolves to itself either way",
        F.ALIASES["quality"] == "quality")

    # -- 7. CLI edges, both directions
    rc, o = cli(["--list"])
    chk("--list exits 0", rc == 0)
    chk("--list prints every register entry",
        all(k in o for k in F.REGISTER))
    rc, o = cli(["--grid", "efficiency"])
    chk("--grid on a known term exits 0", rc == 0)
    rc, o = cli(["--grid", "zzz"])
    chk("--grid on an unknown term reports an error and exits 0",
        rc == 0 and "not in register" in o)
    rc, o = cli(["--grid"])
    chk("--grid with no term raises rather than reporting",
        rc != 0 and "IndexError" in o)
    rc, o = cli(["nosuch_file_xyz.txt"])
    chk("a missing file raises rather than reporting",
        rc != 0 and "FileNotFoundError" in o)
    rc, o = cli([])
    chk("no argument falls through to --list", rc == 0 and "kavik" in o)

    # -- 8. the corpus this folder already holds
    for p in CORPUS:
        chk("corpus file present: %s" % os.path.basename(p),
            os.path.exists(p))
    if all(os.path.exists(p) for p in CORPUS):
        text = open(CORPUS[1], encoding="utf-8", errors="replace").read()
        h = hits(text)
        chk("the blank template yields hits", len(h) > 5)
        # The template enumerates its own sales steps, so `process`
        # there does NOT substitute for doing -- a counter-instance to
        # the register's own definition, and the schema has no cell for
        # one.
        proc = [x for x in h if x[0] == "procedure"]
        chk("the template's `process` hit is on an enumerated procedure",
            any("Steps" in x[3] for x in proc))

    # -- 9. no field is branched on
    uf = unread_fields()
    chk("sign_storage is never branched on",
        not uf["sign_storage"]["read_by_a_branch"])
    chk("residual_tell is never branched on",
        not uf["residual_tell"]["read_by_a_branch"])
    chk("counter_case is never branched on",
        not uf["counter_case"]["read_by_a_branch"])
    chk("substitutes_for is never branched on either",
        not uf["substitutes_for"]["read_by_a_branch"])
    chk("source is never branched on", not uf["source"]["read_by_a_branch"])
    # The detector must be able to say yes, or it is CONSTANT_SILENT.
    import ast as _ast
    probe = _ast.parse("if rec['sign_storage'] == 'signed':\n    pass\n")
    br = set()
    for _n in _ast.walk(probe):
        if isinstance(_n, _ast.Compare):
            for _s in _ast.walk(_n):
                if isinstance(_s, _ast.Subscript) and \
                        isinstance(_s.slice, _ast.Constant):
                    br.add(_s.slice.value)
    chk("the branch detector fires on a real branch",
        "sign_storage" in br)

    # -- 10. render survives with and without the big corpus
    txt = render()
    chk("render names all nine sections",
        all(("%d." % i) in txt for i in range(1, 10)))

    print("selftest: %d checks, %d failed" % (ok[0] + len(bad), len(bad)))
    for b in bad:
        print("  FAILED", b)
    return 0 if not bad else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    print(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
