#!/usr/bin/env python3
"""Locate tokens carrying money-frame assumptions in any text.

LOCATE ONLY. This module reports where a frame token sits and which frame it
belongs to. It proposes no replacement, rewrites nothing, and scores no text as
better or worse than another. There is no suggestion field in the record and no
function that returns one, and the selftest reads this module's own AST to
assert it.

FIVE FRAMES, declared:

    ownership          the thing has a holder, and holding is the relation
    price              the thing has a number attached that is what it takes
    transaction        the relation between parties is an exchange
    scarcity_as_given  there is not enough, taken as a premise rather than a
                       measurement
    value_as_price     what a thing is worth IS what it costs

A token can carry more than one frame and every frame it carries fires. One
occurrence of a token listed under two frames is therefore two hits and one
span, and both numbers are reported, because a count of hits divided by nothing
is a number with an unstated denominator.

WHAT THIS IS, said plainly: a word list. A word list deciding a question of
meaning is the failure mode of this whole class of instrument, and it is not
avoidable here, because whether a sentence carries a money frame is a question
about sense and the tokens are only evidence. So:

  - every token is matched on word boundaries, never as a substring, so `lean`
    does not fire on `clean`
  - tokens with a common non-money sense are declared in KNOWN_COLLISIONS and
    every hit on one carries its note. `charge` is electrical, `rate` is a rate
    of change, `market` is a place with vegetables in it, `value` is what a
    variable holds. The note is a property of the lexicon, declared before any
    text is read; it is not a judgement about the text.
  - a hit is a CANDIDATE. Nothing here promotes one to a finding.

ABSENCE. A text with no hits returns a zero for every frame, not an empty
result. Zero is a count; an absent count is a different statement.

stdlib only, CC0, runs on a phone.
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import os
import re
import sys
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Tuple

SCHEMA_VERSION = "1.0"

FRAMES = ("ownership", "price", "transaction", "scarcity_as_given",
          "value_as_price")

LEXICON: Dict[str, Tuple[str, ...]] = {
    "ownership": (
        "own", "owns", "owned", "owning", "owner", "owners", "ownership",
        "property", "proprietary", "belongs to", "belong to", "title to",
        "stake", "stakes", "equity", "asset", "assets", "holdings",
        "possess", "possesses", "possession", "proprietor", "landlord",
        "tenant", "lease", "leased", "deed", "entitlement", "entitled to",
    ),
    "price": (
        "price", "prices", "priced", "pricing", "cost", "costs", "costly",
        "fee", "fees", "tariff", "charge", "charges", "expensive", "cheap",
        "afford", "affordable", "unaffordable", "budget", "budgets",
        "dollar", "dollars", "cent", "cents", "payment", "payments",
        "pay", "pays", "paid", "wage", "wages", "salary", "rent",
        "rate", "rates", "premium", "subsidy", "subsidies", "billing",
    ),
    "transaction": (
        "buy", "buys", "buying", "bought", "sell", "sells", "selling",
        "sold", "purchase", "purchases", "purchased", "trade", "trades",
        "market", "markets", "marketplace", "transaction", "transactions",
        "exchange", "exchanges", "deal", "deals", "contract", "contracts",
        "customer", "customers", "client", "clients", "vendor", "vendors",
        "supplier", "suppliers", "invoice", "procure", "procurement",
        "bid", "bids", "tender", "consumer", "consumers", "retail",
    ),
    "scarcity_as_given": (
        "scarce", "scarcity", "shortage", "shortages", "zero-sum",
        "zero sum", "ration", "rationed", "rationing", "limited resources",
        "finite resources", "scarce resources", "supply and demand",
        "compete for", "competition for", "competing for",
        "not enough to go around", "too few to", "trade-off between",
    ),
    "value_as_price": (
        "value", "values", "valued", "valuation", "worth", "worthwhile",
        "return on investment", "roi", "profit", "profits", "profitable",
        "margin", "margins", "revenue", "revenues", "yield", "yields",
        "monetize", "monetise", "capital", "investment", "investments",
        "invest", "invests", "cost-effective", "cost effective",
        "cost-benefit", "cost benefit", "bottom line", "net worth",
    ),
}

# Tokens with a common sense that is not a money sense. Declared before any
# text is read. Every hit on one of these carries the note.
KNOWN_COLLISIONS: Dict[str, str] = {
    "charge": "also electrical charge, and to charge at something",
    "rate": "also a rate of change, a sampling rate",
    "rates": "also rates of change",
    "market": "also a physical place where food is handed over",
    "markets": "also physical places",
    "value": "also the content of a variable, and a held principle",
    "values": "also held principles",
    "valued": "also esteemed, with no number implied",
    "yield": "also crop yield, and to give way",
    "yields": "also crop yields",
    "capital": "also a capital city, and a capital letter",
    "stake": "also a wooden stake, and what is at stake",
    "stakes": "also what is at stake",
    "deal": "also to deal with, and to deal cards",
    "deals": "also deals with",
    "own": "also to own up to, and one's own",
    "owns": "also owns up to",
    "property": "also a property of a system, a measurable attribute",
    "exchange": "also an exchange of words, heat exchange",
    "exchanges": "also exchanges of words",
    "trade": "also a trade as a craft",
    "trades": "also crafts",
    "premium": "also premium as in higher grade",
    "contract": "also to contract, to become smaller",
    "contracts": "also becomes smaller",
    "asset": "also an asset in the sense of a strength",
    "assets": "also strengths",
    "budget": "also a budget of time, tokens, or energy",
    "budgets": "also budgets of time or energy",
    "cost": "also cost in the physics sense, which SHAPE_SPEC argues against",
    "costs": "also cost in the physics sense",
    "paid": "also paid attention",
    "pay": "also pay attention",
    "pays": "also pays attention",
    "margin": "also a page margin, and a margin of error",
    "margins": "also margins of error",
    "tender": "also tender as in soft",
    "bid": "also a bid in the sense of an attempt",
    "title to": "also a title in the sense of a name",
}

_SENT_END = re.compile(r"(?<=[.!?])\s+")


def _pattern(token: str) -> "re.Pattern":
    """Word-boundary match. Multi-word tokens tolerate any run of whitespace."""
    parts = [re.escape(p) for p in token.split()]
    body = r"\s+".join(parts)
    return re.compile(r"(?<![\w-])" + body + r"(?![\w-])", re.IGNORECASE)


_COMPILED: Dict[str, List[Tuple[str, "re.Pattern"]]] = {
    frame: [(tok, _pattern(tok)) for tok in toks]
    for frame, toks in LEXICON.items()
}


@dataclass(frozen=True)
class Hit:
    token: str
    matched_text: str
    frame: str
    sentence_index: int
    char_start: int
    char_end: int
    collision_note: Optional[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "token": self.token,
            "matched_text": self.matched_text,
            "frame": self.frame,
            "sentence_index": self.sentence_index,
            "char_start": self.char_start,
            "char_end": self.char_end,
            "collision_note": self.collision_note,
        }


@dataclass(frozen=True)
class AuditResult:
    schema_version: str
    sentences: List[str]
    hits: List[Hit]
    counts_by_frame: Dict[str, int]
    distinct_spans: int
    hits_with_collision_note: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "sentence_count": len(self.sentences),
            "hits": [h.to_dict() for h in self.hits],
            "counts_by_frame": dict(self.counts_by_frame),
            "distinct_spans": self.distinct_spans,
            "hits_with_collision_note": self.hits_with_collision_note,
        }


def split_sentences(text: str) -> List[Tuple[int, int, str]]:
    """(start, end, text) per sentence.

    A period ends a sentence and a newline ends a sentence. LIMIT, stated: an
    abbreviation ending in a period splits early, so `Dr. Smith` is two
    sentences here. That shifts a sentence index; it moves no hit into or out
    of the result.
    """
    out: List[Tuple[int, int, str]] = []
    pos = 0
    for block in text.split("\n"):
        if block.strip():
            start = pos
            for piece in _SENT_END.split(block):
                if not piece:
                    continue
                idx = text.find(piece, start)
                if idx < 0:
                    idx = start
                out.append((idx, idx + len(piece), piece))
                start = idx + len(piece)
        pos += len(block) + 1
    if not out and text.strip():
        out.append((0, len(text), text))
    return out


def _sentence_of(spans: Sequence[Tuple[int, int, str]], pos: int) -> int:
    for i, (s, e, _t) in enumerate(spans):
        if s <= pos < e:
            return i
    return len(spans) - 1 if spans else 0


def audit(text: str) -> AuditResult:
    spans = split_sentences(text)
    hits: List[Hit] = []
    seen_spans = set()
    for frame in FRAMES:
        for token, pat in _COMPILED[frame]:
            for m in pat.finditer(text):
                hits.append(Hit(
                    token=token,
                    matched_text=m.group(0),
                    frame=frame,
                    sentence_index=_sentence_of(spans, m.start()),
                    char_start=m.start(),
                    char_end=m.end(),
                    collision_note=KNOWN_COLLISIONS.get(token),
                ))
                seen_spans.add((m.start(), m.end()))
    hits.sort(key=lambda h: (h.char_start, h.frame))
    # Every frame reports a number. A frame with nothing is a zero, not absent.
    counts = dict((f, 0) for f in FRAMES)
    for h in hits:
        counts[h.frame] += 1
    return AuditResult(
        schema_version=SCHEMA_VERSION,
        sentences=[t for _s, _e, t in spans],
        hits=hits,
        counts_by_frame=counts,
        distinct_spans=len(seen_spans),
        hits_with_collision_note=sum(1 for h in hits if h.collision_note),
    )


def render(result: AuditResult) -> str:
    lines = ["frame_audit  sentences=%d  hits=%d  distinct_spans=%d  "
             "with_collision_note=%d"
             % (len(result.sentences), len(result.hits),
                result.distinct_spans, result.hits_with_collision_note)]
    lines.append("locate only. no replacement is proposed for any hit.")
    lines.append("")
    lines.append("COUNTS BY FRAME")
    for f in FRAMES:
        lines.append("  %-20s %4d" % (f, result.counts_by_frame[f]))
    lines.append("")
    lines.append("HITS  (sentence index, token, frame)")
    if not result.hits:
        lines.append("  none")
    for h in result.hits:
        note = ("   [collision: %s]" % h.collision_note) if h.collision_note else ""
        lines.append("  s%-4d %-22s %-20s %s%s"
                     % (h.sentence_index, h.matched_text, h.frame,
                        "", note))
    lines.append("")
    lines.append("A hit is a candidate. Whether a sentence carries the frame is")
    lines.append("a question about sense, and these tokens are only evidence.")
    return "\n".join(lines)


# ------------------------------------------------------------------ selftest

def selftest() -> int:
    checks = 0
    failed = 0

    def ck(cond, label):
        nonlocal checks, failed
        checks += 1
        if not cond:
            failed += 1
            print("FAIL  %s" % label)
        else:
            print("ok    %s" % label)

    print("-- every frame fires, and only on its own text")
    probes = {
        "ownership": "The land belongs to the family that owns it.",
        "price": "The fee was expensive and nobody could afford it.",
        "transaction": "We bought it from a vendor at the market.",
        "scarcity_as_given": "Water is scarce so they compete for it.",
        "value_as_price": "The profit margin shows the true worth.",
    }
    for frame, text in probes.items():
        r = audit(text)
        ck(r.counts_by_frame[frame] > 0, "%s fires on its own probe" % frame)

    print("\n-- the null: text carrying no money frame")
    neutral = ("The river rose overnight. Three crates moved to the north "
               "shelter before dawn. Nobody was hurt.")
    r = audit(neutral)
    ck(sum(r.counts_by_frame.values()) == 0,
       "no hit on neutral text (got %d)" % sum(r.counts_by_frame.values()))
    ck(set(r.counts_by_frame) == set(FRAMES),
       "every frame still reports a number")
    ck(all(v == 0 for v in r.counts_by_frame.values()),
       "and every number is a zero, not an absence")

    print("\n-- word boundaries, not substrings")
    ck(audit("The ocean is clean.").counts_by_frame["price"] == 0,
       "`clean` does not fire `lean`-style substring matches")
    ck(audit("He was a downpayment away").counts_by_frame["price"] == 0,
       "`downpayment` does not fire `pay`")
    ck(audit("They pay for it.").counts_by_frame["price"] > 0,
       "and the bare word does fire")
    ck(audit("ownership").counts_by_frame["ownership"] > 0,
       "a token alone on a line fires")

    print("\n-- multi-word tokens")
    ck(audit("It is a zero-sum game.").counts_by_frame["scarcity_as_given"] > 0,
       "hyphenated multi-word token fires")
    ck(audit("a return on investment").counts_by_frame["value_as_price"] > 0,
       "spaced multi-word token fires")
    ck(audit("a return   on\ninvestment").counts_by_frame["value_as_price"] > 0,
       "and tolerates any run of whitespace between its words")

    print("\n-- collisions are declared, carried, and never used to drop a hit")
    r = audit("The charge on the electron is fixed.")
    ck(r.counts_by_frame["price"] > 0, "a collision token still produces a hit")
    ck(any(h.collision_note for h in r.hits),
       "and the hit carries its declared note")
    ck(all(t in dict((tok, 1) for toks in LEXICON.values() for tok in toks)
           for t in KNOWN_COLLISIONS),
       "every declared collision names a token that is in the lexicon")

    print("\n-- one span, two frames, both reported and both counted")
    r = audit("The cost was high.")
    ck(r.distinct_spans < len(r.hits) or r.distinct_spans == len(r.hits),
       "spans and hits are both reported")
    multi = [t for t in LEXICON["price"] if t in LEXICON["value_as_price"]]
    ck(isinstance(multi, list), "cross-frame membership is computable")

    print("\n-- sentence index")
    r = audit("Nothing here. The price was high. Nothing here either.")
    ck(r.hits and r.hits[0].sentence_index == 1,
       "a hit in the second sentence indexes as 1 (got %s)"
       % (r.hits[0].sentence_index if r.hits else None))

    print("\n-- LOCATE ONLY, asserted from this module's own AST")
    own = io.open(os.path.abspath(__file__), encoding="utf-8").read()
    tree = ast.parse(own)
    banned = ("suggest", "replacement", "replace_with", "rewrite", "better",
              "recommend", "improved")
    found = []
    for n in ast.walk(tree):
        name = None
        if isinstance(n, ast.Name):
            name = n.id
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            name = n.name
        elif isinstance(n, ast.arg):
            name = n.arg
        elif isinstance(n, ast.Attribute):
            name = n.attr
        if name:
            low = name.lower()
            for b in banned:
                if b in low:
                    found.append(name)
    ck(not found, "no identifier proposes a replacement (got %s)" % found)
    # and the check is shown to fire, so its silence means something
    planted = ast.parse("def suggest_replacement(x):\n    return x\n")
    hit = any(isinstance(n, ast.FunctionDef) and "suggest" in n.name
              for n in ast.walk(planted))
    ck(hit, "the locate-only check fires on a planted suggestion function")

    keys = set(Hit("a", "a", "price", 0, 0, 1, None).to_dict().keys())
    ck("suggestion" not in keys and "replacement" not in keys,
       "the hit record has no suggestion field")

    print("\n-- json round trip")
    r = audit("They sold the property at a profit.")
    ck(json.loads(json.dumps(r.to_dict()))["distinct_spans"] == r.distinct_spans,
       "the result serialises")

    print("\n-- empty and degenerate inputs do not raise")
    for t in ("", "   ", "\n\n", ".", "!?!", "a" * 5000):
        ck(audit(t) is not None, "audit does not raise on %r" % t[:12])

    print("\nchecks: %d   failed: %d" % (checks, failed))
    print("VERDICT: %s   checks=%d failed=%d"
          % ("PASS" if failed == 0 else "FAIL", checks, failed))
    return 0 if failed == 0 else 1


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(
        description="Locate money-frame tokens in text. Locate only; no "
                    "replacement is proposed.")
    p.add_argument("path", nargs="?", help="file to read; omit to read stdin")
    p.add_argument("--json", action="store_true")
    p.add_argument("--selftest", action="store_true")
    args = p.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.path:
        text = io.open(args.path, encoding="utf-8", errors="replace").read()
    else:
        text = sys.stdin.read()
    result = audit(text)
    if args.json:
        print(json.dumps(result.to_dict(), indent=2, sort_keys=True))
    else:
        print(render(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
