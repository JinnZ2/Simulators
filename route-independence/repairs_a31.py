# SPDX-License-Identifier: CC0-1.0
"""AMENDMENT A-3.1 (2026-09-28): definitional repairs, built over A-1, A-2, A-2.1 and A-3.

The amendment text is landed verbatim as
AMENDMENT_A3.1_2026-09-28_definitional-repairs.md and was committed ALONE at
EXPECTED_COMMIT_A31 before this module existed (rule 1).  Nothing in A-1..A-3's
modules is edited: every section here reads their rows and functions by import.

  section 1  ONE DEFINITION OF MARKET: MARKET_GATES = {TOKEN_PURCHASE, METERED_TOKEN};
             E-A3-2a re-run over the K rows, the prior two-definition result beside it
  section 2  a registry of every EXPECTED entry A-1..A-3 (and A-3.1 itself), each with
             its predicate P and falsifier F QUOTED from the amendment text (the quote is
             checked present), encoded over a finite cell space; F == NOT P is checked
             by enumerating every world of up to two cells [CHOICE 25]; a world where
             neither P nor F holds is UNMET_UNFALSIFIED, one where both hold OVERSHOOT
  section 3  count words carry units: a lint over each EXPECTED block [CHOICE 30]
  section 4  null semantics: every None / UNKNOWN / UNDECIDED on the named fields
             migrated to NONE, NOT_RECORDED or (t fields) OPEN_ENDED under two declared
             rules [CHOICE 31]; every field migrated and every row whose reading moved
  section 5  E-A3-3 over NON_MARKET instruments, the literal (all instruments) beside
  section 6  ABSENCE_BOUND falsifiers; an unfired one is NOT_TESTABLE_AS_POSED, never
             silent; the clothing RETAIN K row added [CHOICE 35]
  section 7  every result prints cells_covered / cells_total beside it [CHOICE 36]
  section 8  E-A3.1-1 and E-A3.1-2 evaluated, MISMATCH rows first (rule 4)

Every source stays CARRIED; nothing here is a statement about the law of any
jurisdiction.  The registry's formal encodings are this module's readings of the
quoted sentences, and where a sentence admits two readings both are registered.
"""
import ast
import itertools
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import gate_state as G          # noqa: E402  A-2
import gate_state_a21 as A21    # noqa: E402  A-2.1
import settlement_split as S    # noqa: E402  A-1
import thermal_gates as T       # noqa: E402  A-3

EXPECTED_COMMIT_A31 = "beb0fc6"
AMENDMENT_FILE = "AMENDMENT_A3.1_2026-09-28_definitional-repairs.md"
AMENDMENTS = (
    ("A-1", "AMENDMENT_A1_2026-09-28_settlement-vs-gate.md"),
    ("A-2", "AMENDMENT_A2_2026-09-28_gate-state.md"),
    ("A-2.1", "AMENDMENT_A2.1_2026-09-28_source-upgrades.md"),
    ("A-3", "AMENDMENT_A3_2026-09-28_thermal.md"),
    ("A-3.1", AMENDMENT_FILE),
)
T_QUERY = T.T_QUERY

CHOICES = {
    24: "each registry entry's P and F are substrings QUOTED from its amendment (whitespace collapsed, checked present); "
        "the encoding of a quote over a cell space is this module's reading, and a sentence admitting two readings is "
        "registered twice, both printed",
    25: "worlds are every multiset of 0..2 cells over the entry's cell space (exactly one cell for a single-outcome "
        "entry); the encoded quantifiers are all decided cell by cell, so two cells reach every mismatch they can have",
    26: "an entry with no falsifier sentence has F = never fires, which is narrower than NOT P by construction; it is "
        "counted as FALSIFIER_UNDECLARED, apart from a stated F that is narrower",
    27: "a conditional sentence naming what to report if the prediction does not hold ('If it does not ... report "
        "that'; 'If it does, that is ...') is read as a declared falsifier",
    28: "E-A3-3 read two ways: literal (P over the WARM and COOL instruments it names, F over 'both sides') and side "
        "(both over HEAT_IN / HEAT_OUT, A-3 [CHOICE 14])",
    29: "E-A3-4 read two ways: literal (P over the whole residue, F over sourced actuators only) and R2-scoped (both "
        "over sourced actuators)",
    30: "a count token is a standalone integer (not touching a letter, digit, '_', '-', '/', '=', ':' or a '.' before a "
        "digit; not a year 1000..2999; not after 'section' or 'row') or a number word zero..twelve; its unit is found "
        "if one of the next three words (skipping 'of' and numerals) is gate(s), position(s), row(s) or cell(s); "
        "otherwise the first such word is reported UNIT_OUTSIDE_LIST, and no word at all is NO_UNIT",
    31: "migration rule EVIDENCE (primary): a None becomes NONE, or OPEN_ENDED on a t field, only where a source text "
        "or the row's own note records it; otherwise NOT_RECORDED.  Rule SCHEMA_DEFAULT (beside): a None takes the "
        "meaning its schema declared -- A-2 3a 'None (open-ended)' for a t with the other end dated, A-2 3a 'no t "
        "reads UNKNOWN' for both t None, A-3 2b 'None | named condition' and 'None | named office' as NONE; a field "
        "whose schema declared no meaning for None takes NOT_RECORDED under both",
    32: "at3 is in force / not in force / UNDETERMINED: a NOT_RECORDED t_from with t_to dated is NOT_IN_FORCE at t >= "
        "t_to and UNDETERMINED before it; a NOT_RECORDED t_to is NOT_IN_FORCE before t_from and UNDETERMINED at or "
        "after it; both NOT_RECORDED is UNDETERMINED everywhere; OPEN_ENDED reads as A-2's open end",
    33: "access_is_right takes no NONE: 'recorded as absent' for a right is FALSE, which the enum already holds, so the "
        "pair would add a synonym of FALSE; UNKNOWN maps to NOT_RECORDED and NONE is refused on this field",
    34: "a row's reading is compared at the query points the expectations use: t = 2026 and A-3's T_WINTER, under "
        "condition None and every named condition carried by a row of the same actuator in the same jurisdiction; no "
        "other t is probed",
    35: "the clothing RETAIN row cites source A31-6 (the amendment's own section-6 statement, grade K), jurisdiction "
        "'state X' (F-T5's), t_from 2024 as A-3 [CHOICE 18], one TOKEN_PURCHASE gate, flagged absence_bound",
    36: "coverage is cells_covered / cells_total on the grid the expectation quantifies over; covered = a row or a zero "
        "declaration exists for the cell (searched), never 'sourced'; the sourced count is printed beside it",
    37: "each falsifier's f_requires (ABSENCE / PRESENCE / MIXED / CODE_BEHAVIOUR) is DECLARED with a reason, not "
        "inferred from wording; ABSENCE and MIXED falsifiers are the ABSENCE_BOUND set",
}

# ---------------------------------------------------------------- section 1 ---

MARKET_GATES = (T.TOKEN_PURCHASE, T.METERED_TOKEN)
NON_MARKET = tuple(k for k in T.GATE_KINDS if k not in MARKET_GATES)
MET, FALSIFIER, UNMET_UNFALSIFIED, UNSEARCHED = "MET", "FALSIFIER", "UNMET_UNFALSIFIED", "UNSEARCHED"


def nonmarket_gates(gates, jurisdiction, t, condition=None):
    """Section 2d's derived quantity under the one definition."""
    return T.nonmarket_gates(gates, jurisdiction, t, condition, market=MARKET_GATES)


def e32a_cells(gates, zeros, actuators, t=T_QUERY):
    """E-A3-2a per (jurisdiction, external actuator) cell under MARKET_GATES, with the two
    prior counts carried on every cell."""
    out = []
    for c in T._cells(gates, zeros, actuators, t):
        d = dict(c)
        if c["state"] == "UNSEARCHED":
            d["a31"] = UNSEARCHED
        else:
            kinds = c["kinds"] or []
            nm = len([k for k in kinds if k not in MARKET_GATES])
            if nm >= 1:
                d["a31"] = MET
            elif kinds == [T.TOKEN_PURCHASE]:
                d["a31"] = FALSIFIER
            else:
                d["a31"] = UNMET_UNFALSIFIED      # zero gates, or market gates other than purchase alone
        out.append(d)
    return out


def e32a_rerun(gates, zeros, actuators, t=T_QUERY):
    cells = e32a_cells(gates, zeros, actuators, t)
    prior = T.e32a_reading(gates, zeros, actuators, t)
    tally = dict((s, [(c["j"], c["aid"]) for c in cells if c["a31"] == s])
                 for s in (MET, FALSIFIER, UNMET_UNFALSIFIED, UNSEARCHED))
    return {"cells": cells, "tally": tally, "n_cells": len(cells),
            "covered": len(cells) - len(tally[UNSEARCHED]),
            "sourced": len([g for g in gates if g["hold_eligible"]]),
            "prior_met_2d": len(prior["met_2d"]), "prior_met_e32a": len(prior["met_e32a"]),
            "prior_parted": sorted(set(c["aid"] for c in prior["parted"]))}


# ---------------------------------------------------------------- section 2 ---

STATED, CONDITIONAL, UNDECLARED, NOT_A_PREDICTION = "STATED", "CONDITIONAL", "UNDECLARED", "NOT_A_PREDICTION"
ABSENCE, PRESENCE, MIXED, CODE_BEHAVIOUR = "ABSENCE", "PRESENCE", "MIXED", "CODE_BEHAVIOUR"
COMPLEMENT, GAP, OVERSHOOT = "COMPLEMENT", "GAP", "OVERSHOOT"
FALSIFIER_UNDECLARED = "FALSIFIER_UNDECLARED"


def _norm(s):
    return " ".join(s.split())


def amendment_text(amendment):
    return _norm(open(os.path.join(HERE, dict(AMENDMENTS)[amendment])).read())


_HOLD_FAIL = ("HOLDS", "FAILS")
_IN = ("WARM", "RETAIN")
_OUT = ("COOL", "SHED")


def _subsets(items):
    return [frozenset(c) for n in range(len(items) + 1) for c in itertools.combinations(items, n)]


def _undeclared(eid, amendment, p_quote, f_requires, reason, variant=""):
    return {"id": eid, "variant": variant, "amendment": amendment, "p_quote": p_quote, "f_quote": None,
            "f_form": UNDECLARED, "f_requires": f_requires, "requires_reason": reason, "space": _HOLD_FAIL,
            "min_cells": 1, "max_cells": 1, "p": lambda w: w[0] == "HOLDS", "f": lambda w: False}


def registry():
    """Every EXPECTED entry A-1..A-3 plus A-3.1's own two [CHOICE 24]."""
    R = []
    # ---- A-1 ----
    R.append({"id": "A-1 E-A1", "variant": "", "amendment": "A-1",
              "p_quote": "at least 2 of 3 cases carry zero BIOLOGICAL edges", "f_quote": None,
              "f_form": UNDECLARED, "f_requires": CODE_BEHAVIOUR,
              "requires_reason": "a re-scoring of three declared cases; no sourced absence is read",
              "space": (0, 1, 2, 3), "min_cells": 1, "max_cells": 1,
              "p": lambda w: w[0] >= 2, "f": lambda w: False})
    R.append({"id": "A-1 E-A2", "variant": "", "amendment": "A-1",
              "p_quote": "will force a settlement reading where none applies",
              "f_quote": "If it does not, the defect in section 1 is not present in the code",
              "f_form": CONDITIONAL, "f_requires": CODE_BEHAVIOUR,      # [CHOICE 27]
              "requires_reason": "a property of the unamended code", "space": ("FORCED", "NOT_FORCED"),
              "min_cells": 1, "max_cells": 1, "p": lambda w: w[0] == "FORCED", "f": lambda w: w[0] == "NOT_FORCED"})
    R.append({"id": "A-1 E-A3", "variant": "", "amendment": "A-1",
              "p_quote": "will NOT return INDEPENDENT", "f_quote": "If it does, that is the more interesting result",
              "f_form": CONDITIONAL, "f_requires": CODE_BEHAVIOUR,
              "requires_reason": "a reading computed on declared routes", "space": ("INDEPENDENT", "NOT_INDEPENDENT"),
              "min_cells": 1, "max_cells": 1,
              "p": lambda w: w[0] != "INDEPENDENT", "f": lambda w: w[0] == "INDEPENDENT"})
    # ---- A-2 ----
    R.append(_undeclared("E-A2-1", "A-2", "Unamended code returns identical records for F-W1 and F-W2.",
                         CODE_BEHAVIOUR, "a property of the unamended code"))
    R.append(_undeclared("E-A2-2", "A-2", "F-G1 -> F-G2 registers as one change event, OPEN -> DISCRETIONARY.",
                         CODE_BEHAVIOUR, "an event computed on two declared rows"))
    route_states = [tuple(p) for n in range(3) for p in itertools.product(("OPEN", "OTHER"), repeat=n)]
    R.append({"id": "E-A2-3", "variant": "", "amendment": "A-2",
              "p_quote": "no subsistence route (water, food, shelter) reads OPEN in every sourced jurisdiction",
              "f_quote": "any single route OPEN in all sourced jurisdictions",
              "f_form": STATED, "f_requires": MIXED,
              "requires_reason": "OPEN on the rainwater leg is a claim of absence (A-2.1: no enacting statute sources "
                                 "TX); OPEN on the gleaning leg is a sourced license, a presence (G-1)",
              "space": tuple(route_states), "min_cells": 1, "max_cells": 2,
              "p": lambda w: not any(all(r == "OPEN" for r in route) for route in w),
              "f": lambda w: any(all(r == "OPEN" for r in route) for route in w)})
    R.append(_undeclared("E-A2-4", "A-2", "No expression may treat a DISCRETIONARY route as independent.",
                         CODE_BEHAVIOUR, "an AST property of the code"))
    # ---- A-2.1 ----
    R.append(_undeclared("E-A2.1-1", "A-2.1", "Rainwater is OPEN nowhere SOURCED.", MIXED,
                         "the readings rest on sourced presences (CO, UT) and one claimed absence (TX)"))
    R.append(_undeclared("E-A2.1-2", "A-2.1", "E-A2-3 hold count does not change", CODE_BEHAVIOUR,
                         "a comparison of two runs"))
    # ---- A-3 ----
    R.append(_undeclared("E-A3-1", "A-3", "Unamended code collapses F-T4's four gates to one state", CODE_BEHAVIOUR,
                         "a property of the unamended code"))
    kind_sets = _subsets((T.TOKEN_PURCHASE, T.METERED_TOKEN, "NON_MARKET"))
    R.append({"id": "E-A3-2a", "variant": "", "amendment": "A-3",
              "p_quote": "every EXTERNAL actuator carries >= 1 NON-MARKET gate",
              "f_quote": "any sourced external actuator whose only gate is TOKEN_PURCHASE",
              "f_form": STATED, "f_requires": ABSENCE,
              "requires_reason": "'only gate' is an absence of every other gate on a sourced actuator",
              "space": tuple(kind_sets), "min_cells": 0, "max_cells": 2,
              "p": lambda w: all("NON_MARKET" in c for c in w),
              "f": lambda w: any(c == frozenset((T.TOKEN_PURCHASE,)) for c in w)})
    dirs = _subsets(T.HEAT_DIRECTIONS)
    both_sides = lambda c: bool(c & set(_IN)) and bool(c & set(_OUT))   # noqa: E731
    R.append({"id": "E-A3-3", "variant": "literal [CHOICE 28]", "amendment": "A-3",
              "p_quote": "The WARM-gating and COOL-gating instruments are disjoint in the sourced set",
              "f_quote": "one instrument appearing on both sides", "f_form": STATED, "f_requires": PRESENCE,
              "requires_reason": "an instrument present on two rows", "space": tuple(dirs), "min_cells": 0,
              "max_cells": 2, "p": lambda w: not any({"WARM", "COOL"} <= c for c in w),
              "f": lambda w: any(both_sides(c) for c in w)})
    R.append({"id": "E-A3-3", "variant": "side [CHOICE 28]", "amendment": "A-3",
              "p_quote": "no single instrument gates both directions",
              "f_quote": "one instrument appearing on both sides", "f_form": STATED, "f_requires": PRESENCE,
              "requires_reason": "an instrument present on two rows", "space": tuple(dirs), "min_cells": 0,
              "max_cells": 2, "p": lambda w: not any(both_sides(c) for c in w),
              "f": lambda w: any(both_sides(c) for c in w)})
    cells4 = tuple(itertools.product(("BODY", "NON_BODY"), (True, False), (True, False)))   # locus, sourced, zero
    R.append({"id": "E-A3-4", "variant": "literal [CHOICE 29]", "amendment": "A-3",
              "p_quote": "ungated_residue at t=2026 contains BODY-locus actuators only",
              "f_quote": "any sourced non-body actuator with zero gates", "f_form": STATED, "f_requires": ABSENCE,
              "requires_reason": "zero gates is an absence", "space": cells4, "min_cells": 0, "max_cells": 2,
              "p": lambda w: all(c[0] == "BODY" for c in w if c[2]),
              "f": lambda w: any(c[0] == "NON_BODY" and c[1] and c[2] for c in w)})
    R.append({"id": "E-A3-4", "variant": "R2-scoped [CHOICE 29]", "amendment": "A-3",
              "p_quote": "ungated_residue at t=2026 contains BODY-locus actuators only",
              "f_quote": "any sourced non-body actuator with zero gates", "f_form": STATED, "f_requires": ABSENCE,
              "requires_reason": "zero gates is an absence", "space": cells4, "min_cells": 0, "max_cells": 2,
              "p": lambda w: all(c[0] == "BODY" for c in w if c[2] and c[1]),
              "f": lambda w: any(c[0] == "NON_BODY" and c[1] and c[2] for c in w)})
    R.append(_undeclared("E-A3-5", "A-3", "Removing the coupling row removes the propagation.", CODE_BEHAVIOUR,
                         "a property of propagate()"))
    R.append({"id": "E-A3-6", "variant": "", "amendment": "A-3",
              "p_quote": "Registered as open, not predicted.", "f_quote": None, "f_form": NOT_A_PREDICTION,
              "f_requires": None, "requires_reason": "no prediction", "space": _HOLD_FAIL, "min_cells": 1,
              "max_cells": 1, "p": lambda w: True, "f": lambda w: False})
    # ---- A-3.1, applied to itself ----
    # a world: (E-A3-2a is a mismatch, count of other mismatches)
    R.append({"id": "E-A3.1-1", "variant": "", "amendment": "A-3.1",
              "p_quote": "Section 2 finds at least one mismatch in A-1..A-3 besides E-A3-2a",
              "f_quote": "zero mismatches found", "f_form": STATED, "f_requires": CODE_BEHAVIOUR,
              "requires_reason": "an enumeration over the registry",
              "space": tuple(itertools.product((True, False), (0, 1, 2))), "min_cells": 1, "max_cells": 1,
              "p": lambda w: w[0][1] >= 1, "f": lambda w: (not w[0][0]) and w[0][1] == 0})
    # a world: (some row's reading changed, some row's meaning changed without its reading)
    R.append({"id": "E-A3.1-2", "variant": "", "amendment": "A-3.1",
              "p_quote": "Section 4 changes the reading of at least one existing row",
              "f_quote": "zero rows change meaning", "f_form": STATED, "f_requires": CODE_BEHAVIOUR,
              "requires_reason": "an enumeration over existing rows",
              "space": tuple(itertools.product((True, False), (True, False))), "min_cells": 1, "max_cells": 1,
              "p": lambda w: w[0][0], "f": lambda w: not (w[0][0] or w[0][1])})
    return R


def quotes_present(entries=None):
    """Every quote found verbatim (whitespace collapsed) in its amendment: a value and its
    source travel together."""
    out = []
    for e in (registry() if entries is None else entries):
        text = amendment_text(e["amendment"])
        for q in (e["p_quote"], e["f_quote"]):
            if q is not None:
                out.append((e["id"], e["variant"], q, _norm(q) in text))
    return out


def worlds(entry):
    for k in range(entry["min_cells"], entry["max_cells"] + 1):
        for w in itertools.combinations_with_replacement(entry["space"], k):
            yield w


def complement(entry):
    """F == NOT P, checked on every world [CHOICE 25]."""
    if entry["f_form"] == NOT_A_PREDICTION:
        return {"status": NOT_A_PREDICTION, "gap": [], "overshoot": [], "n_worlds": 0, "gap_cells": [],
                "overshoot_cells": []}
    gap, over, n = [], [], 0
    for w in worlds(entry):
        n += 1
        p, f = entry["p"](w), entry["f"](w)
        if not p and not f:
            gap.append(w)
        elif p and f:
            over.append(w)
    if entry["f_form"] == UNDECLARED:
        status = FALSIFIER_UNDECLARED     # [CHOICE 26]
    elif gap and over:
        status = GAP + "+" + OVERSHOOT
    elif gap:
        status = GAP
    elif over:
        status = OVERSHOOT
    else:
        status = COMPLEMENT
    return {"status": status, "gap": gap, "overshoot": over, "n_worlds": n,
            "gap_cells": sorted(set(cell_repr(c) for w in gap if len(w) == 1 for c in w)),
            "overshoot_cells": sorted(set(cell_repr(c) for w in over if len(w) == 1 for c in w))}


def cell_repr(c):
    """Deterministic text for a cell: a frozenset prints as its sorted members."""
    if isinstance(c, frozenset):
        return "{%s}" % ",".join(sorted(c))
    return repr(c)


def complement_table():
    return [(e, complement(e)) for e in registry()]


def is_mismatch(status):
    return status not in (COMPLEMENT, NOT_A_PREDICTION)


def e_a1_internal():
    """A-1's E-A1 states two predicates one sentence apart: 'a MAJORITY [of rows] as
    CONSTRUCTED' and 'at least 2 of 3 cases carry zero BIOLOGICAL edges'.  Three cases of
    one or two rows each, every row CONSTRUCTED or BIOLOGICAL: how many worlds part them."""
    case_states = [tuple(p) for n in (1, 2) for p in itertools.product("CB", repeat=n)]
    parted, n = [], 0
    for w in itertools.product(case_states, repeat=3):
        n += 1
        rows = [r for c in w for r in c]
        majority = rows.count("C") * 2 > len(rows)
        zero_b = len([c for c in w if "B" not in c]) >= 2
        if majority != zero_b:
            parted.append(w)
    return {"worlds": n, "parted": len(parted), "example": parted[0] if parted else None}


# ---------------------------------------------------------------- section 3 ---

UNITS = ("gate", "gates", "position", "positions", "row", "rows", "cell", "cells")
NUMBER_WORDS = ("zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
                "twelve")
_DIGITS = re.compile(r"(?<![A-Za-z0-9_\-/=:.])(\d+)(?![A-Za-z0-9_\-/=:]|\.\d)")
_WORDS = re.compile(r"\b(%s)\b" % "|".join(NUMBER_WORDS), re.I)
_TOKEN = re.compile(r"[A-Za-z][A-Za-z_\-+]*|\d+")
OK, UNIT_OUTSIDE_LIST, NO_UNIT = "OK", "UNIT_OUTSIDE_LIST", "NO_UNIT"


def expected_block(amendment):
    out, on = [], False
    for line in open(os.path.join(HERE, dict(AMENDMENTS)[amendment])).read().splitlines():
        if line.startswith("## "):
            on = "EXPECTED" in line
            continue
        if on:
            out.append(line)
    return _norm(" ".join(out))


def count_tokens(text):
    """[CHOICE 30]"""
    out = []
    for m in _DIGITS.finditer(text):
        v = int(m.group(1))
        if len(m.group(1)) == 4 and 1000 <= v <= 2999:
            continue
        before = text[:m.start()].split()
        if before and before[-1].lower().strip("(") in ("section", "row"):
            continue
        out.append((m.start(), m.group(1)))
    for m in _WORDS.finditer(text):
        out.append((m.start(), m.group(1)))
    out.sort()
    res = []
    for pos, tok in out:
        rest = text[pos + len(tok):]
        window = [w for w in _TOKEN.findall(rest)[:6] if w.lower() != "of" and not w.isdigit()
                  and w.lower() not in NUMBER_WORDS][:3]
        if any(w.lower() in UNITS for w in window):
            unit = [w for w in window if w.lower() in UNITS][0]
            res.append({"token": tok, "status": OK, "unit": unit, "context": text[pos:pos + 40]})
        elif window:
            res.append({"token": tok, "status": UNIT_OUTSIDE_LIST, "unit": window[0], "context": text[pos:pos + 40]})
        else:
            res.append({"token": tok, "status": NO_UNIT, "unit": None, "context": text[pos:pos + 40]})
    return res


def lint():
    out = []
    for a, _ in AMENDMENTS:
        toks = count_tokens(expected_block(a))
        bad = [x for x in toks if x["status"] != OK]
        out.append({"amendment": a, "tokens": toks, "n_fail": len(bad),
                    "verdict": "LINT_FAIL" if bad else ("PASS" if toks else "PASS (no count token)")})
    return out


# ---------------------------------------------------------------- section 4 ---

NONE, NOT_RECORDED, OPEN_ENDED = "NONE", "NOT_RECORDED", "OPEN_ENDED"
EVIDENCE, SCHEMA_DEFAULT = "EVIDENCE", "SCHEMA_DEFAULT"
RULES = (EVIDENCE, SCHEMA_DEFAULT)
IN_FORCE, NOT_IN_FORCE, UNDETERMINED = "IN_FORCE", "NOT_IN_FORCE", "UNDETERMINED"
APPLIES, NOT_APPLIES = "APPLIES", "NOT_APPLIES"
RENAMED, DISAMBIGUATED, READING_CHANGED = "RENAMED", "DISAMBIGUATED", "READING_CHANGED"
FIELDS_A31 = ("revocable_by", "access_is_right", "t_from", "t_to", "trigger_condition", "gate_instrument",
              "obligation_origin")

# EVIDENCE rule: the only Nones a source or note records [CHOICE 31]
EVIDENCE_BASIS = {
    ("A-2.1:F-W3a", "t_to"): (OPEN_ENDED, "W-2a: 'current text (Justia 2022 codification)'"),
    ("A-2.1:F-W3b", "t_to"): (OPEN_ENDED, "W-2a: 'current text (Justia 2022 codification)'"),
}


def _rid_a2(prefix, row):
    return "%s:%s" % (prefix, row["gate_note"].split(";")[0].split(" ")[0])


def existing_rows():
    """Every row A-1..A-3 carry in the tree, keyed; A-2.1's rows are its own seven (its two
    gleaning rows are A-2's and are listed once, under A-2)."""
    out = []
    for r in G.fixture_rows():
        out.append((_rid_a2("A-2", r), "A-2", r))
    for fn in (A21.fixture_f_w1a, A21.fixture_f_w1b, A21.fixture_f_w2_p, A21.fixture_f_w3a, A21.fixture_f_w3b,
               A21.fixture_f_w3c, A21.fixture_f_w4_unknown):
        r = fn()
        out.append((_rid_a2("A-2.1", r), "A-2.1", r))
    for g in T.fixture_gates():
        out.append(("A-3:%s|%s" % (g["gate_id"], g["condition"]), "A-3.gate", g))
    for z in T.fixture_f_t6():
        out.append(("A-3:F-T6.%s" % z["actuator_id"], "A-3.zero", z))
    for c in G.reread_undecided()["cases"]:
        for cat, dep in sorted(c["dependencies"].items()):
            for r in dep["routes"]:
                out.append(("A-1:%s/%s/%s" % (c["name"], cat, r["route"]), "A-1", r))
    return out


def _nullable(family, field, v):
    if field == "access_is_right":
        return v == "UNKNOWN"
    if field == "obligation_origin":
        return v == S.UNDECIDED
    return v is None


def _fields(family):
    return {"A-2": ("t_from", "t_to", "gate_instrument"), "A-2.1": ("t_from", "t_to", "gate_instrument"),
            "A-3.gate": ("t_from", "t_to", "trigger_condition", "access_is_right", "revocable_by"),
            "A-3.zero": ("t_from", "t_to"), "A-1": ("obligation_origin",)}[family]


def _map(rule, rid, family, field, row):
    """(new value, basis, schema-declared-meaning?) for one nullable value."""
    if field == "obligation_origin":
        return NOT_RECORDED, "A-3.1 section 4: map UNDECIDED -> NOT_RECORDED", True
    if field == "access_is_right":
        return NOT_RECORDED, "UNKNOWN is 'not yet determined'; NONE refused on this field [CHOICE 33]", True
    if rule == EVIDENCE:
        if (rid, field) in EVIDENCE_BASIS:
            v, b = EVIDENCE_BASIS[(rid, field)]
            return v, b, False
        return NOT_RECORDED, "no source text or note records it [CHOICE 31]", False
    # SCHEMA_DEFAULT
    if field in ("t_from", "t_to"):
        other = row["t_to"] if field == "t_from" else row["t_from"]
        if other is not None:
            return OPEN_ENDED, "A-2 3a: 'ISO date or None (open-ended)'", True
        return NOT_RECORDED, "A-2 3a: 'A route with no jurisdiction or no t reads UNKNOWN'", True
    if field in ("trigger_condition", "revocable_by"):
        return NONE, "A-3 2b: 'None | named %s'" % ("condition" if field == "trigger_condition" else "office"), True
    return NOT_RECORDED, "no meaning declared for None on this field [CHOICE 31]", False


def migrate_row(rule, rid, family, row):
    new = dict(row)
    moves = []
    for f in _fields(family):
        v = row.get(f)
        if not _nullable(family, f, v):
            continue
        nv, basis, declared = _map(rule, rid, family, f, row)
        new[f] = nv
        moves.append({"field": f, "old": v, "new": nv, "basis": basis, "schema_declared": declared})
    return new, moves


def at3(row, t):
    """[CHOICE 32]  Three-valued in-force over migrated t fields (and A-2's plain dates)."""
    lo, hi = row.get("t_from"), row.get("t_to")
    lo_d = lo if lo not in (None, NOT_RECORDED, OPEN_ENDED) else None
    hi_d = hi if hi not in (None, NOT_RECORDED, OPEN_ENDED) else None
    if lo == NOT_RECORDED and hi == NOT_RECORDED:
        return UNDETERMINED
    if hi_d is not None and t >= hi_d:
        return NOT_IN_FORCE
    if lo_d is not None and t < lo_d:
        return NOT_IN_FORCE
    if lo == NOT_RECORDED or hi == NOT_RECORDED:
        return UNDETERMINED
    return IN_FORCE


def at2(row, t):
    """The unmigrated reading, in the same vocabulary: A-2's at() as a two-valued answer."""
    return IN_FORCE if G.at(row, t) else NOT_IN_FORCE


def applies3(row, jurisdiction, t, condition):
    if row["jurisdiction"] != jurisdiction:
        return NOT_APPLIES
    time = at3(row, t)
    if time == NOT_IN_FORCE:
        return NOT_APPLIES
    rc = row.get("condition")
    cond = APPLIES
    if condition is not None:
        if rc is not None:
            cond = APPLIES if rc == condition else NOT_APPLIES
        elif row.get("trigger_condition") == NOT_RECORDED:
            cond = UNDETERMINED
    if cond == NOT_APPLIES:
        return NOT_APPLIES
    if UNDETERMINED in (time, cond):
        return UNDETERMINED
    return APPLIES


def applies2(row, jurisdiction, t, condition):
    return APPLIES if T._applies(row, jurisdiction, t, condition) else NOT_APPLIES


def query_points(family, row, rows):
    """[CHOICE 34]"""
    ts = (T_QUERY, T.T_WINTER)
    if family == "A-3.gate":
        conds = [None] + sorted(set(r["condition"] for r in rows if r["actuator_id"] == row["actuator_id"]
                                    and r["jurisdiction"] == row["jurisdiction"] and r["condition"] is not None))
        return [(row["jurisdiction"], t, c) for t in ts for c in conds]
    return [(None, t, None) for t in ts]


def readings(family, row, rows, migrated):
    """The row's readings at its query points: the derived values a consumer sees."""
    if family == "A-1":
        return (("scorable", migrated["obligation_origin"] not in (S.UNDECIDED, NOT_RECORDED)),)
    if family == "A-3.gate":
        fn = (lambda r, j, t, c: applies3(r, j, t, c)) if migrated is not row else applies2
        pts = [(p, fn(migrated, *p)) for p in query_points(family, row, rows)]
        named = migrated["revocable_by"] not in (None, NONE, NOT_RECORDED)
        known = migrated["access_is_right"] not in ("UNKNOWN", NOT_RECORDED)
        return tuple(pts) + (("office_named", named), ("access_known", known))
    fn = at3 if migrated is not row else at2
    return tuple((p, fn(migrated, p[1])) for p in query_points(family, row, rows))


def migration(rule):
    ex = existing_rows()
    a3 = [r for rid, fam, r in ex if fam == "A-3.gate"]
    out = []
    for rid, fam, row in ex:
        new, moves = migrate_row(rule, rid, fam, row)
        before = readings(fam, row, a3, row)
        after = readings(fam, row, a3, new)
        if not moves:
            cls = None
        elif before != after:
            cls = READING_CHANGED
        elif all(m["schema_declared"] or m["old"] in ("UNKNOWN", S.UNDECIDED) for m in moves):
            cls = RENAMED
        else:
            cls = DISAMBIGUATED
        changed = [(b[0], b[1], a[1]) for b, a in zip(before, after) if b != a]
        out.append({"row": rid, "family": fam, "moves": moves, "class": cls, "changed_at": changed})
    return out


def migration_summary(rule):
    m = migration(rule)
    fields = {}
    for r in m:
        for mv in r["moves"]:
            d = fields.setdefault(mv["field"], {})
            d[mv["new"]] = d.get(mv["new"], 0) + 1
    by_class = dict((c, [r["row"] for r in m if r["class"] == c]) for c in (RENAMED, DISAMBIGUATED, READING_CHANGED))
    return {"rule": rule, "rows": len(m), "rows_migrated": len([r for r in m if r["moves"]]),
            "fields": fields, "by_class": by_class, "table": m}


# ---------------------------------------------------------------- section 5 ---

def e33_a31(gates):
    return {"literal_shared": sorted(T.side_instruments(gates, T.HEAT_IN) & T.side_instruments(gates, T.HEAT_OUT)),
            "nonmarket_shared": sorted(T.side_instruments(gates, T.HEAT_IN, MARKET_GATES)
                                       & T.side_instruments(gates, T.HEAT_OUT, MARKET_GATES)),
            "nonmarket_in": sorted(T.side_instruments(gates, T.HEAT_IN, MARKET_GATES)),
            "nonmarket_out": sorted(T.side_instruments(gates, T.HEAT_OUT, MARKET_GATES))}


# ---------------------------------------------------------------- section 6 ---

SOURCES_A31 = dict(T.SOURCES_A3)
SOURCES_A31["A31-6"] = {"grade": "K", "input": True, "status": "STATED_BY_AMENDMENT",
                        "text": "A-3.1 section 6: 'Add a clothing RETAIN fixture row: gate_kind TOKEN_PURCHASE only, "
                                "grade K, ABSENCE_BOUND.'"}
NOT_TESTABLE_AS_POSED, FIRED, DECIDED_BY_PRESENCE = "NOT_TESTABLE_AS_POSED", "FIRED", "DECIDED_BY_PRESENCE"


def fixture_retain_k():
    """[CHOICE 35]"""
    r = T.tgate("F-A31.retain.purchase", "clothing.retain", 1, T.TOKEN_PURCHASE, "state X", "2024",
                gate_state=G.METERED_PERMISSION, source="A31-6", instrument=T.MARKET_INSTRUMENT, sources=SOURCES_A31,
                note="A-3.1 section 6: grade K, hold-ineligible; its falsifier is absence-bound")
    r["absence_bound"] = True
    return r


def absence_bound(rule=EVIDENCE):
    """Section 6 over the ABSENCE / MIXED falsifiers.  On the sourced set only; an unfired
    one is NOT_TESTABLE_AS_POSED, never silent; one kept from firing by a sourced presence
    elsewhere on its quantifier is DECIDED_BY_PRESENCE."""
    gates = T.fixture_gates() + [fixture_retain_k()]
    zeros, acts = T.fixture_f_t6(), T.seed_actuators()
    src = [g for g in gates if g["hold_eligible"]]
    out = []
    k = e32a_cells(gates, zeros, acts)
    k_fire = [(c["j"], c["aid"]) for c in k if c["a31"] == FALSIFIER]
    out.append({"id": "E-A3-2a", "status": NOT_TESTABLE_AS_POSED if not src else FIRED,
                "detail": "sourced external cells %d; on the K rows the falsifier is reached at %s, hold-ineligible"
                          % (len(src), k_fire)})
    sz = [z for z in zeros if z["hold_eligible"]]
    out.append({"id": "E-A3-4", "status": NOT_TESTABLE_AS_POSED if not sz else FIRED,
                "detail": "sourced zero declarations %d" % len(sz)})
    legs = e23_legs(rule)
    st = FIRED if any(l["status"] == FIRED for l in legs) else (
        NOT_TESTABLE_AS_POSED if any(l["status"] == NOT_TESTABLE_AS_POSED for l in legs) else DECIDED_BY_PRESENCE)
    out.append({"id": "E-A2-3", "status": st, "legs": legs,
                "detail": "; ".join("%s %s (%s)" % (l["route"], l["status"], l["why"]) for l in legs)})
    return out


def e23_legs(rule=EVIDENCE):
    """E-A2-3's falsifier per route over the A-2.1 rows at 2026, sourced rows only."""
    rows = [(rid, r) for rid, fam, r in existing_rows() if fam == "A-2.1"] + \
           [(rid, r) for rid, fam, r in existing_rows() if fam == "A-2" and r["route_id"] == "gleaning"]
    legs = []
    for route in sorted(set(r["route_id"] for _, r in rows)):
        mine = [(rid, r) for rid, r in rows if r["route_id"] == route and r["hold_eligible"]]
        per_j = {}
        for rid, r in mine:
            fam = "A-2.1" if rid.startswith("A-2.1") else "A-2"
            m, _ = migrate_row(rule, rid, fam, r)
            st = at3(m, T_QUERY)
            if st == NOT_IN_FORCE:
                continue
            per_j.setdefault(r["jurisdiction"], []).append(G.UNKNOWN_STATE if st == UNDETERMINED else r["gate_state"])
        known = dict((j, v) for j, v in per_j.items() if G.UNKNOWN_STATE not in v)
        non_open = sorted(j for j, v in known.items() if any(s != G.OPEN for s in v))
        if non_open:
            status, why = DECIDED_BY_PRESENCE, "sourced non-OPEN reading in %s" % non_open
        elif known and len(known) == len(per_j):
            status, why = FIRED, "OPEN in every sourced jurisdiction"
        else:
            status, why = NOT_TESTABLE_AS_POSED, "no sourced known reading at 2026 (%s)" % sorted(per_j)
        legs.append({"route": route, "status": status, "why": why, "per_j": per_j})
    return legs


# ---------------------------------------------------------------- section 7 ---

def coverage_grid(gates, zeros, actuators, jurisdictions, external_only):
    total = covered = sourced = 0
    for j in jurisdictions:
        for a in actuators:
            if external_only and not T.is_external(a):
                continue
            total += 1
            aid = a["actuator_id"]
            rows = [g for g in gates if g["actuator_id"] == aid and g["jurisdiction"] == j]
            zs = [z for z in zeros if z["actuator_id"] == aid and z["jurisdiction"] in (j, T.ANY_JURISDICTION)]
            if rows or zs:
                covered += 1
            if any(r["hold_eligible"] for r in rows) or any(z["hold_eligible"] for z in zs):
                sourced += 1
    return {"covered": covered, "total": total, "sourced": sourced}


def cov(c):
    return "%d/%d (sourced %d/%d)" % (c["covered"], c["total"], c["sourced"], c["total"])


# ---------------------------------------------------------------- section 8 ---

def e311_counts():
    """E-A3.1-1 under three readings of 'mismatch'."""
    tab = complement_table()
    in_scope = [(e, c) for e, c in tab if e["amendment"] != "A-3.1" and e["f_form"] != NOT_A_PREDICTION]

    def count(filter_fn):
        other = len([1 for e, c in in_scope if e["id"] != "E-A3-2a" and filter_fn(e, c)])
        has_2a = any(e["id"] == "E-A3-2a" and filter_fn(e, c) for e, c in in_scope)
        return has_2a, other

    literal_all = count(lambda e, c: is_mismatch(c["status"]) and "side" not in e["variant"]
                        and "R2-scoped" not in e["variant"])
    declared_literal = count(lambda e, c: e["f_form"] != UNDECLARED and is_mismatch(c["status"])
                             and "side" not in e["variant"] and "R2-scoped" not in e["variant"])
    declared_charitable = count(lambda e, c: e["f_form"] != UNDECLARED and is_mismatch(c["status"])
                                and "literal" not in e["variant"])
    return {"entries": len(in_scope), "LITERAL_ALL": literal_all, "DECLARED_LITERAL": declared_literal,
            "DECLARED_CHARITABLE": declared_charitable}


def _e311_verdict(has_2a, other):
    e = [x for x in registry() if x["id"] == "E-A3.1-1"][0]
    w = ((has_2a, min(other, 2)),)
    p, f = e["p"](w), e["f"](w)
    if p and not f:
        return "MATCH"
    if f and not p:
        return "MISMATCH"
    return UNMET_UNFALSIFIED if not p else OVERSHOOT


def _e312_verdict(summary):
    rc = len(summary["by_class"][READING_CHANGED])
    mc = rc + len(summary["by_class"][DISAMBIGUATED])
    e = [x for x in registry() if x["id"] == "E-A3.1-2"][0]
    w = ((rc > 0, mc > rc),)
    p, f = e["p"](w), e["f"](w)
    if p and not f:
        return "MATCH", rc, mc
    if f and not p:
        return "MISMATCH", rc, mc
    return (UNMET_UNFALSIFIED if not p else OVERSHOOT), rc, mc


def check_expectations():
    rows = []
    c = e311_counts()
    for reading in ("LITERAL_ALL", "DECLARED_LITERAL", "DECLARED_CHARITABLE"):
        has_2a, other = c[reading]
        v = _e311_verdict(has_2a, other)
        rows.append({"id": "E-A3.1-1 (%s)" % reading, "status": v,
                     "hold": "INSTRUMENT (rule 1 met at %s); coverage %d/%d registry entries A-1..A-3 checked"
                             % (EXPECTED_COMMIT_A31, c["entries"], c["entries"]),
                     "detail": "mismatches besides E-A3-2a: %d; E-A3-2a itself a mismatch: %s" % (other, has_2a)})
    for rule in RULES:
        s = migration_summary(rule)
        v, rc, mc = _e312_verdict(s)
        rows.append({"id": "E-A3.1-2 (%s)" % rule, "status": v,
                     "hold": "INSTRUMENT; coverage %d/%d existing rows examined, %d carry a nullable value"
                             % (s["rows"], s["rows"], s["rows_migrated"]),
                     "detail": "rows whose reading moved %d; rows whose meaning moved (reading or disambiguation) %d"
                               % (rc, mc)})
    rank = {"MISMATCH": 0, UNMET_UNFALSIFIED: 1, OVERSHOOT: 1, "MATCH": 2}
    return sorted(rows, key=lambda r: rank[r["status"]])


# ------------------------------------------------------------ fail fixtures ---

def fail_fixture():
    """Rule 3.  (1) Section 2d's unamended market set counts heating.utility as carrying a
    non-market gate; under MARKET_GATES the same cell is UNMET_UNFALSIFIED.  (2) A-2's at()
    reads a row with no t as NOT in force; at3 reads it UNDETERMINED."""
    gates, zeros, acts = T.fixture_gates(), T.fixture_f_t6(), T.seed_actuators()
    before = T.nonmarket_gates(gates, "state A", T_QUERY)["heating.utility"]
    after = [c["a31"] for c in e32a_cells(gates, zeros, acts) if c["j"] == "state A" and c["aid"] == "heating.utility"]
    f_w3 = G.fixture_f_w3()
    m, _ = migrate_row(SCHEMA_DEFAULT, "A-2:F-W3", "A-2", f_w3)
    return {"heating_2d_nonmarket": before, "heating_a31": after[0], "f_w3_at": at2(f_w3, T_QUERY),
            "f_w3_at3": at3(m, T_QUERY)}


# ------------------------------------------------------------------ render ---

def _fmt(v):
    return "--" if v is None else str(v)


def render(out=None):
    w = (out or sys.stdout).write
    gates, zeros, acts = T.fixture_gates(), T.fixture_f_t6(), T.seed_actuators()
    w("repairs_a31 -- AMENDMENT A-3.1 over A-1 / A-2 / A-2.1 / A-3: one market definition, complement check, unit "
      "lint, null semantics\n")
    w("EXPECTED registered at %s; every source CARRIED; no row read here is a statement about any jurisdiction\n\n"
      % EXPECTED_COMMIT_A31)

    w("-- expected (section 8), MISMATCH rows first, then UNMET_UNFALSIFIED\n")
    for r in check_expectations():
        w("expected %-17s %-33s %s\n" % (r["status"], r["id"], r["detail"]))
        w("         hold: %s\n" % r["hold"])

    w("\n-- section 1: MARKET_GATES %s; NON_MARKET %s\n" % (list(MARKET_GATES), list(NON_MARKET)))
    w("   A-3's E-A3-2a list reads the same market set: %s\n" % (set(T.MARKET_E32A) == set(MARKET_GATES)))
    for label, gs in (("K rows as delivered", gates), ("K rows + the section-6 RETAIN row", gates + [fixture_retain_k()])):
        r = e32a_rerun(gs, zeros, acts)
        w("   E-A3-2a re-run, %s: cells %d/%d covered, sourced rows %d\n" % (label, r["covered"], r["n_cells"],
                                                                          r["sourced"]))
        for s in (MET, FALSIFIER, UNMET_UNFALSIFIED):
            w("      %-18s %s\n" % (s, r["tally"][s]))
        w("      UNSEARCHED         %d cells\n" % len(r["tally"][UNSEARCHED]))
        w("      prior two-definition result: met under 2d %d, under E-A3-2a's list %d, parted on %s\n"
          % (r["prior_met_2d"], r["prior_met_e32a"], r["prior_parted"]))

    w("\n-- section 2: complement check, P and F quoted from each amendment [CHOICE 24]\n")
    for e, c in complement_table():
        w("   %-8s %-10s %-26s %-21s F %-12s requires %s\n"
          % (e["amendment"], e["id"], e["variant"] or "-", c["status"], e["f_form"], _fmt(e["f_requires"])))
        if c["gap_cells"]:
            w("            UNMET_UNFALSIFIED at one-cell worlds: %s\n" % ", ".join(c["gap_cells"]))
        if c["overshoot_cells"]:
            w("            OVERSHOOT at one-cell worlds: %s\n" % ", ".join(c["overshoot_cells"]))
    q = quotes_present()
    w("   quotes found in their amendments: %d/%d\n" % (len([x for x in q if x[3]]), len(q)))
    ea1 = e_a1_internal()
    w("   A-1 E-A1's two predicates ('a MAJORITY as CONSTRUCTED' vs 'at least 2 of 3 cases carry zero BIOLOGICAL "
      "edges') part on %d of %d three-case worlds, e.g. %s\n" % (ea1["parted"], ea1["worlds"], ea1["example"]))

    w("\n-- section 3: count words carry units [CHOICE 30]\n")
    for l in lint():
        w("   %-6s %-22s %s\n" % (l["amendment"], l["verdict"],
                                 "; ".join("%s->%s %s" % (x["token"], x["status"], _fmt(x["unit"]))
                                           for x in l["tokens"]) or "-"))
    w("   A-3's 'four gates' carries a listed unit and passes the lint; the fixture it counts holds 5 gates in 4 "
      "positions (RIN_087): the lint reads that a unit is named, not that the count holds\n")

    w("\n-- section 4: null semantics, two migration rules [CHOICE 31]\n")
    for rule in RULES:
        s = migration_summary(rule)
        w("   %s: %d existing rows, %d carry a nullable value on the named fields\n"
          % (rule, s["rows"], s["rows_migrated"]))
        for f in FIELDS_A31:
            if f in s["fields"]:
                w("      field %-18s %s\n" % (f, s["fields"][f]))
            else:
                w("      field %-18s no nullable value on any row\n" % f)
        for cls in (READING_CHANGED, DISAMBIGUATED, RENAMED):
            w("      %-15s %d rows\n" % (cls, len(s["by_class"][cls])))
        for r in s["table"]:
            if r["class"] == READING_CHANGED:
                w("         %-44s %s\n" % (r["row"][:44], "; ".join("%s: %s -> %s" % (p, b, a)
                                                                     for p, b, a in r["changed_at"][:2])))
        for r in s["table"]:
            if r["class"] == DISAMBIGUATED:
                w("         %-44s meaning set, reading unmoved: %s\n"
                  % (r["row"][:44], ", ".join("%s %s -> %s" % (m["field"], _fmt(m["old"]), m["new"])
                                              for m in r["moves"])))

    w("\n-- section 5: E-A3-3 over NON_MARKET instruments, the literal beside\n")
    for label, gs in (("K rows", gates), ("K rows + one constructed fan purchase", gates + [T.row_fan_purchase()])):
        r = e33_a31(gs)
        w("   %-40s shared non-market %s; shared literal (all instruments) %s\n"
          % (label, r["nonmarket_shared"], r["literal_shared"]))
    src = [g for g in gates if g["hold_eligible"]]
    w("   on the sourced set: %d rows, NOT_EVALUABLE; coverage %s\n"
      % (len(src), cov(coverage_grid(gates, zeros, acts, T.jurisdictions(gates), False))))

    w("\n-- section 6: ABSENCE_BOUND falsifiers [CHOICE 37]; sourced set only\n")
    for rule in RULES:
        for r in absence_bound(rule):
            w("   %-14s %-8s %-22s %s\n" % (rule, r["id"], r["status"], r["detail"]))

    w("\n-- section 7: coverage beside every result [CHOICE 36]\n")
    w("   E-A3-2a  external (jurisdiction, actuator) grid %s\n"
      % cov(coverage_grid(gates, zeros, acts, T.jurisdictions(gates), True)))
    w("   E-A3-3/4 all-actuator grid %s\n" % cov(coverage_grid(gates, zeros, acts, T.jurisdictions(gates), False)))

    ff = fail_fixture()
    w("\nfail fixture 1: heating.utility in state A counts %d non-market gate under section 2d as delivered; under "
      "MARKET_GATES the cell reads %s\n" % (ff["heating_2d_nonmarket"], ff["heating_a31"]))
    w("fail fixture 2: A-2's F-W3 (no t) reads %s under A-2's at(); %s under at3\n" % (ff["f_w3_at"], ff["f_w3_at3"]))
    w("holds: rule 1 met (%s); rule 3 met; rule 2 unmet on every thermal row (all K)\n" % EXPECTED_COMMIT_A31)
    w("choices in force: %s\n" % ", ".join("[CHOICE %d]" % k for k in sorted(CHOICES)))
    w("execution note: test_repairs_a31.py prints the check count; samples/repairs_a31.sample.txt is one recorded "
      "render, compare before quoting\n")


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("library module; run: python3 route-independence/test_repairs_a31.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    render()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
