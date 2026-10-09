#!/usr/bin/env python3
"""conditional_claims.py - keep conditional claims rigid; prove restatement fidelity.
CC0. stdlib only.

Atoms in [brackets]. Operators: IF..THEN, ->, <->, AND, OR, NOT, parentheses.
compare(original, restatement) runs a full truth table over the union of atoms
and names the collapse. Checks form, not truth.

Usage:
  conditional_claims.py parse "IF [gradient imposed] THEN [plasma relaxes]"
  conditional_claims.py compare "IF [A] THEN [B]" "[B]"
  conditional_claims.py extract notes.txt
  conditional_claims.py new -o claims.json
  conditional_claims.py add claims.json --id C1 --verbatim "exact words" \
      --formal "IF [A] THEN [B]" --scope "where it holds"
  conditional_claims.py check claims.json C1 --restated "[B]"
  conditional_claims.py show claims.json C1
  conditional_claims.py selftest
"""
import argparse, itertools, json, re, sys

TOK = re.compile(r"\[[^\]]*\]|<->|->|\(|\)|[A-Za-z]+")
KEYWORDS = {"IF", "THEN", "AND", "OR", "NOT"}

def _norm(s):
    return " ".join(s.strip().lower().split())

class ParseError(ValueError):
    pass

class _P:
    def __init__(self, text):
        self.t = TOK.findall(text)
        self.i = 0
        for tok in self.t:
            if tok[0] != "[" and tok not in ("->", "<->", "(", ")") \
                    and tok.upper() not in KEYWORDS:
                raise ParseError(f"bare word '{tok}': put atoms in [brackets]")

    def peek(self):
        return self.t[self.i] if self.i < len(self.t) else None

    def up(self):
        p = self.peek()
        return p.upper() if p else None

    def eat(self, want=None):
        tok = self.peek()
        if tok is None:
            raise ParseError(f"unexpected end, wanted {want}")
        if want and tok.upper() != want:
            raise ParseError(f"wanted {want}, got {tok}")
        self.i += 1
        return tok

    def expr(self):
        if self.up() == "IF":
            self.eat("IF")
            a = self.disj()
            self.eat("THEN")
            return ("imp", a, self.expr())
        a = self.disj()
        if self.peek() == "->":
            self.eat()
            return ("imp", a, self.expr())
        if self.peek() == "<->":
            self.eat()
            return ("iff", a, self.expr())
        return a

    def disj(self):
        a = self.conj()
        while self.up() == "OR":
            self.eat()
            a = ("or", a, self.conj())
        return a

    def conj(self):
        a = self.unary()
        while self.up() == "AND":
            self.eat()
            a = ("and", a, self.unary())
        return a

    def unary(self):
        tok = self.peek()
        if tok is None:
            raise ParseError("unexpected end")
        if tok.upper() == "NOT":
            self.eat()
            return ("not", self.unary())
        if tok == "(":
            self.eat()
            e = self.expr()
            self.eat(")")
            return e
        if tok.upper() == "IF":
            return self.expr()
        if tok.startswith("["):
            self.eat()
            name = _norm(tok[1:-1])
            if not name:
                raise ParseError("empty atom []")
            return ("atom", name)
        raise ParseError(f"unexpected token {tok}")

def parse(text):
    p = _P(text)
    e = p.expr()
    if p.peek() is not None:
        raise ParseError(f"trailing tokens from '{p.peek()}'")
    return e

def atoms(e, acc=None):
    acc = set() if acc is None else acc
    if e[0] == "atom":
        acc.add(e[1])
    else:
        for sub in e[1:]:
            atoms(sub, acc)
    return acc

def ev(e, env):
    k = e[0]
    if k == "atom": return env[e[1]]
    if k == "not":  return not ev(e[1], env)
    if k == "and":  return ev(e[1], env) and ev(e[2], env)
    if k == "or":   return ev(e[1], env) or ev(e[2], env)
    if k == "imp":  return (not ev(e[1], env)) or ev(e[2], env)
    if k == "iff":  return ev(e[1], env) == ev(e[2], env)
    raise ValueError(k)

def show(e):
    k = e[0]
    if k == "atom": return f"[{e[1]}]"
    if k == "not":  return f"NOT {show(e[1])}"
    op = {"and": "AND", "or": "OR", "imp": "->", "iff": "<->"}[k]
    return f"({show(e[1])} {op} {show(e[2])})"

def _rows(*es):
    names = sorted(set().union(*(atoms(e) for e in es)))
    for vals in itertools.product((False, True), repeat=len(names)):
        yield dict(zip(names, vals))

def equivalent(a, b):
    return all(ev(a, r) == ev(b, r) for r in _rows(a, b))

def entails(a, b):
    return all((not ev(a, r)) or ev(b, r) for r in _rows(a, b))

MEANING = {
    "EQUIVALENT": "same claim in different form",
    "ASSERTED_CONSEQUENT": "operator dropped: premise deleted, consequent stated as unconditional fact",
    "FLATTENED_TO_CONJUNCTION": "operator dropped: the if-then relation read as two separate facts",
    "CONVERSE": "direction flipped, written as converse: THEN-part made the condition",
    "INVERSE": "direction flipped, written as inverse: both sides negated (logically identical to the converse; each is the other's contrapositive)",
    "DIRECTION_FLIPPED": "direction flipped in another written form (same truth table as the converse)",
    "STRONGER": "restatement claims more than was said",
    "WEAKER": "restatement claims less than was said",
    "NOT_ENTAILED": "restatement neither follows from nor implies what was said",
}

def compare(orig, rest):
    oa, ra = atoms(orig), atoms(rest)
    out = {"dropped_atoms": sorted(oa - ra), "new_atoms": sorted(ra - oa)}
    if equivalent(orig, rest):
        v = "EQUIVALENT"
    elif orig[0] == "imp" and equivalent(rest, orig[2]):
        v = "ASSERTED_CONSEQUENT"
    elif orig[0] == "imp" and equivalent(rest, ("and", orig[1], orig[2])):
        v = "FLATTENED_TO_CONJUNCTION"
    elif orig[0] == "imp" and equivalent(rest, ("imp", orig[2], orig[1])):
        P, Q = orig[1], orig[2]
        if rest == ("imp", Q, P):
            v = "CONVERSE"
        elif rest == ("imp", ("not", P), ("not", Q)):
            v = "INVERSE"
        else:
            v = "DIRECTION_FLIPPED"
    elif entails(rest, orig):
        v = "STRONGER"
    elif entails(orig, rest):
        v = "WEAKER"
    else:
        v = "NOT_ENTAILED"
    out["verdict"] = v
    out["meaning"] = MEANING[v]
    return out

# ---- heuristic extractor: list every conditional cue a restatement must honor ----
CUES = re.compile(r"\b(only if|if|unless|whenever|when|provided that|as long as|assuming)\b", re.I)

def extract(text):
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text) if s.strip()]
    found = []
    for n, s in enumerate(sents, 1):
        cues = [c.lower() for c in CUES.findall(s)]
        if cues:
            found.append({"n": n, "cues": cues, "sentence": s})
    return found

# ---- verbatim ledger ----
def load(path):
    with open(path) as f:
        return json.load(f)

def save(d, path):
    with open(path, "w") as f:
        json.dump(d, f, indent=2)

def _get(d, cid):
    for c in d["claims"]:
        if c["id"] == cid:
            return c
    sys.exit(f"no claim {cid}")

def selftest():
    o = parse("IF [A] THEN [B]")
    cases = {
        "[B]": "ASSERTED_CONSEQUENT",
        "[A] AND [B]": "FLATTENED_TO_CONJUNCTION",
        "[B] -> [A]": "CONVERSE",
        "NOT [A] -> NOT [B]": "INVERSE",
        "NOT [A] OR [B]": "EQUIVALENT",
        "[A] -> [B] AND [C]": "STRONGER",
        "IF [A] AND [C] THEN [B]": "WEAKER",
        "[C]": "NOT_ENTAILED",
        "NOT [B] OR [A]": "DIRECTION_FLIPPED",
    }
    for rest, want in cases.items():
        got = compare(o, parse(rest))["verdict"]
        assert got == want, (rest, got, want)
    assert equivalent(parse("NOT [A] -> NOT [B]"), parse("[B] -> [A]"))
    r = compare(o, parse("IF [A] AND [C] THEN [B]"))
    assert r["new_atoms"] == ["c"] and r["dropped_atoms"] == []
    assert compare(o, parse("[B]"))["dropped_atoms"] == ["a"]
    assert parse("if [x] then [y]") == ("imp", ("atom", "x"), ("atom", "y"))
    try:
        parse("IF plasma THEN [y]")
        raise AssertionError("bare word accepted")
    except ParseError:
        pass
    ex = extract("If the gradient holds, then it relaxes. It is hot. Unless cooled, it vents.")
    assert [x["n"] for x in ex] == [1, 3], ex
    d = {"claims": [{"id": "C1", "verbatim": "if A then B", "formal": "IF [A] THEN [B]", "scope": ""}]}
    save(d, "_cc_selftest.json")
    import os
    d2 = load("_cc_selftest.json")
    os.remove("_cc_selftest.json")
    assert compare(parse(_get(d2, "C1")["formal"]), parse("[B]"))["verdict"] == "ASSERTED_CONSEQUENT"
    print("SELFTEST OK")

def main(argv=None):
    p = argparse.ArgumentParser(description="operator-preserving conditional claims")
    sp = p.add_subparsers(dest="cmd", required=True)
    sp.add_parser("parse").add_argument("expr")
    c = sp.add_parser("compare"); c.add_argument("original"); c.add_argument("restated")
    sp.add_parser("extract").add_argument("path")
    sp.add_parser("new").add_argument("-o", "--out", default="claims.json")
    a = sp.add_parser("add"); a.add_argument("path")
    a.add_argument("--id", required=True); a.add_argument("--verbatim", required=True)
    a.add_argument("--formal", required=True); a.add_argument("--scope", default="")
    k = sp.add_parser("check"); k.add_argument("path"); k.add_argument("id")
    k.add_argument("--restated", required=True)
    s = sp.add_parser("show"); s.add_argument("path"); s.add_argument("id")
    sp.add_parser("selftest")
    args = p.parse_args(argv)

    if args.cmd == "selftest":
        return selftest()
    if args.cmd == "parse":
        print(show(parse(args.expr))); return
    if args.cmd == "compare":
        print(json.dumps(compare(parse(args.original), parse(args.restated)), indent=2)); return
    if args.cmd == "extract":
        with open(args.path) as f:
            hits = extract(f.read())
        print(f"HEURISTIC: {len(hits)} sentence(s) with conditional cues; "
              f"a restatement must account for each")
        for h in hits:
            print(f"  #{h['n']} {h['cues']}: {h['sentence']}")
        return
    if args.cmd == "new":
        save({"claims": []}, args.out); print(f"-> {args.out}"); return

    d = load(args.path)
    if args.cmd == "add":
        parse(args.formal)  # reject malformed before storing
        d["claims"].append({"id": args.id, "verbatim": args.verbatim,
                            "formal": args.formal, "scope": args.scope})
        save(d, args.path); print(f"{args.id} stored")
    elif args.cmd == "show":
        c = _get(d, args.id)
        print(f"VERBATIM: {c['verbatim']}\nFORMAL:   {c['formal']}\nSCOPE:    {c['scope']}")
    elif args.cmd == "check":
        c = _get(d, args.id)
        r = compare(parse(c["formal"]), parse(args.restated))
        print(f"VERBATIM: {c['verbatim']}")
        print(f"VERDICT:  {r['verdict']} - {r['meaning']}")
        if r["dropped_atoms"]: print(f"DROPPED:  {r['dropped_atoms']}")
        if r["new_atoms"]:     print(f"ADDED:    {r['new_atoms']}")

if __name__ == "__main__":
    main()
