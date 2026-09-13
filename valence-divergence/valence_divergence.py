# SPDX-License-Identifier: CC0-1.0
"""
valence_divergence.py -- log a term used by two parties, record what each
decoder returned, and flag divergence.

IT DOES NOT DETERMINE VALENCE. There is no dictionary here and no model of
what words mean. Both readings are supplied. That is not a limitation to be
lifted later: a valence dictionary would be one decoder claiming to be the
answer, and the instrument would then be reporting its own reading as the
finding.

The scored failure is not disagreement. Disagreement is visible and gets
handled. The scored failure is AGREEMENT REACHED OVER AN UNFLAGGED MISMATCH,
which is D3_SILENT_PASS.

THE FIVE CHECKS (WORK_ORDER.md, section "Checks")

    D1_DIVERGENT          the two valences differ, neither UNREAD, B not ABSENT
    D2_UNFLAGGED          D1 and nobody marked the term
    D3_SILENT_PASS        D2 and the exchange continued -- the scored failure
    D4_UNCHECKED          the history was not looked up; a queue entry
    D5_ORPHAN_CANDIDATE   valence now, none at origin

D2 and D3 are nested inside D1 by their own definitions, so `fired` is a
chain on three of the five rather than five independent verdicts.
`reachable_fired_sets()` enumerates the whole lattice by brute force rather
than asserting it.

WHAT THIS MODULE DOES NOT HOLD

    - no lexicon, no valence model, no sentiment scoring. `term` is carried
      and read by NOTHING -- asserted from the AST, which is the strongest
      available statement of "no dictionary": the instrument never looks at
      the word.
    - no field for intent, motive, or what either party meant. Checked with
      the shared identifier scan against a declared vocabulary.
    - no ranking of decoder A over decoder B. D1 is swap-invariant and
      `d1_swap_invariance()` measures it; D5 is directional BY DESIGN,
      being a claim about now against origin, and that asymmetry is
      reported rather than hidden.
    - no averaging, no dominant sense, no resolution to a single valence.
      The return carries both readings intact and has no top-level valence
      field at all. Branches are separate entries.

EIGHT PLACES THE ORDER LEAVES A DECISION OPEN. All are in `CHOICES`,
printed in the header of every render, and none is silent.

Stdlib only. No network. Parses under Python 3.9. ASCII only. CC0.

    python3 valence_divergence.py     # render the case set
    python3 test_valence.py           # the checks
"""

from __future__ import annotations

import itertools
import sys

# --------------------------------------------------------------------------
# vocabularies. Closed, declared, never extended by inference.

# [CHOICE 7] MIXED is admissible as a SUPPLIED value and is produced by
# nothing here. Two branches of one term are two entries; the MIXED that
# would summarise them is the reader's reading, not the log's.
VALENCES = ("POS", "NEG", "NEUTRAL", "MIXED", "UNREAD")
A_SOURCES = ("DEFAULT", "STATED", "CONTEXT")
B_SOURCES = ("ETYMOLOGY", "HISTORICAL_USE", "OTHER_CULTURE", "STATED", "ABSENT")
FLAGGED_BY = ("A", "B", "BOTH", "NEITHER")

# [CHOICE 6] the Open section's provisional handling, recorded not enforced.
DEMONSTRATED = ("IN_USE", "ON_REQUEST", "UNRECORDED")

HISTORY_SOURCES = ("ETYMOLOGY", "HISTORICAL_USE")
CITED_SOURCES = ("ETYMOLOGY", "HISTORICAL_USE", "OTHER_CULTURE")

CHECK_CODES = ("D1_DIVERGENT", "D2_UNFLAGGED", "D3_SILENT_PASS",
               "D4_UNCHECKED", "D5_ORPHAN_CANDIDATE")

ATTRIBUTION_VALUES = ("A", "B", "SPLIT", "NEITHER")

INTAKE_INCOMPLETE = "INTAKE_INCOMPLETE"

# [CHOICE 8] there is no field linking one entry to another. Branch
# grouping is the reader's job and the only handle is `term`, which the
# instrument reads for nothing.
TOP_FIELDS = ("term", "utterance_id", "speaker", "reading_A", "reading_B",
              "flagged_by", "proceeded")


CHOICES = {
    1: ("`decoder_attribution` gains a fourth value, NEITHER. The order "
        "declares three and glosses the field as naming the decoder that "
        "produced the valence 'when only one did' -- which fits A and B, "
        "leaves SPLIT undefined by its own sentence, and covers neither "
        "the both-UNREAD entry nor an entry where the two agree. SPLIT is "
        "read here as 'both decoders produced a valence', agreeing or "
        "not; NEITHER is the state the three values cannot say."),
    2: ("an entry that fails intake returns grade INTAKE_INCOMPLETE with "
        "`fired` None -- not [] -- and `missing`/`invalid` lists. [] would "
        "say five checks ran and none fired, which is case C."),
    3: ("`d5_basis` is emitted beside the fired list: NEUTRAL_AT_ORIGIN or "
        "UNREAD_AT_ORIGIN. D5's own condition admits both and the intake "
        "section says in as many words that the two must not be merged, so "
        "the check is left exactly as the order writes it and the "
        "distinction is carried alongside rather than lost."),
    4: ("citation and date_or_period may be absent or empty when "
        "reading_B.source is STATED or ABSENT, per 'required unless'. They "
        "are required and non-empty for ETYMOLOGY, HISTORICAL_USE and "
        "OTHER_CULTURE."),
    5: ("reading_B.source ABSENT with a valence other than UNREAD is "
        "ADMITTED, not refused. The order says ABSENT means the history "
        "was not looked up, which implies UNREAD, and refusing the "
        "combination would delete the only entry on which D1's ABSENT "
        "clause does any work. See `absent_clause_is_live()`."),
    6: ("reading_A gains an optional `demonstrated` field (IN_USE / "
        "ON_REQUEST / UNRECORDED, default UNRECORDED). The Open section's "
        "provisional handling is to log reading_A only when demonstrated "
        "in use; recorded here and NOT enforced, because refusing an "
        "introspected default empties most real logs and that call belongs "
        "to whoever runs the instrument."),
    7: ("MIXED is a supplied value only. Nothing in this module ever "
        "assigns it, computes it, or derives one valence from two."),
    9: ("the order states `flagged_by` and `proceeded` only for case D. "
        "For A, B and C they are chosen here (NEITHER / True), and that "
        "choice is what makes D2 and D3 fire on them. The order's MUST "
        "lists for A and B name D1 and D5 and are satisfied under every "
        "value of the two unstated fields; `unstated_field_effect()` "
        "reports per entry which fired codes are invariant and which are "
        "contingent on the choice, so a reader is not left reading a "
        "contingent D3 as a property of the case."),
    8: ("nothing links two entries that are branches of one term. The "
        "order makes branch grouping the reader's job (case B: 'the "
        "observation that they share a shape is made by the reader'), and "
        "the only handle is the `term` string, which the instrument reads "
        "for nothing."),
}

SCHEMA_ADDITIONS = ("grade", "missing", "invalid", "d5_basis",
                    "decoder_attribution: NEITHER",
                    "reading_A.demonstrated")


# --------------------------------------------------------------------------
# intake

def _nonempty_str(v):
    return isinstance(v, str) and v != ""


def intake(entry):
    """Return (missing, invalid). Either non-empty blocks the read."""
    if not isinstance(entry, dict):
        return list(TOP_FIELDS), ["entry: not a mapping"]

    missing = [f for f in TOP_FIELDS if f not in entry]
    invalid = []

    def bad(field, why):
        invalid.append("%s: %s" % (field, why))

    for f in ("term", "utterance_id", "speaker"):
        if f in entry and not _nonempty_str(entry[f]):
            bad(f, "not a non-empty string")

    if "flagged_by" in entry and entry["flagged_by"] not in FLAGGED_BY:
        bad("flagged_by", "not one of %s" % (FLAGGED_BY,))

    if "proceeded" in entry and not isinstance(entry["proceeded"], bool):
        bad("proceeded", "not a bool")

    a = entry.get("reading_A")
    if "reading_A" in entry:
        if not isinstance(a, dict):
            bad("reading_A", "not a mapping")
        else:
            for f in ("valence", "source", "gloss"):
                if f not in a:
                    missing.append("reading_A.%s" % f)
            if "valence" in a and a["valence"] not in VALENCES:
                bad("reading_A.valence", "not one of %s" % (VALENCES,))
            if "source" in a and a["source"] not in A_SOURCES:
                bad("reading_A.source", "not one of %s" % (A_SOURCES,))
            if "gloss" in a and not isinstance(a["gloss"], str):
                bad("reading_A.gloss", "not a string")
            # [CHOICE 6] optional, but a stated value must be in vocabulary.
            if "demonstrated" in a and a["demonstrated"] not in DEMONSTRATED:
                bad("reading_A.demonstrated",
                    "not one of %s" % (DEMONSTRATED,))

    b = entry.get("reading_B")
    if "reading_B" in entry:
        if not isinstance(b, dict):
            bad("reading_B", "not a mapping")
        else:
            for f in ("valence", "source", "gloss"):
                if f not in b:
                    missing.append("reading_B.%s" % f)
            if "valence" in b and b["valence"] not in VALENCES:
                bad("reading_B.valence", "not one of %s" % (VALENCES,))
            if "source" in b and b["source"] not in B_SOURCES:
                bad("reading_B.source", "not one of %s" % (B_SOURCES,))
            if "gloss" in b and not isinstance(b["gloss"], str):
                bad("reading_B.gloss", "not a string")
            # [CHOICE 5] source ABSENT beside a valence is NOT refused here.
            # It is the only shape on which D1's ABSENT clause changes a
            # verdict, and refusing it would delete the evidence that the
            # clause does anything.
            # [CHOICE 4] required unless STATED or ABSENT.
            if b.get("source") in CITED_SOURCES:
                for f in ("citation", "date_or_period"):
                    if not _nonempty_str(b.get(f)):
                        bad("reading_B.%s" % f,
                            "required and non-empty for source %s"
                            % b.get("source"))
    return missing, invalid


def demonstrated_of(entry):
    """[CHOICE 6] default UNRECORDED. Recording that nothing was recorded is
    not the same as recording a demonstration."""
    a = entry.get("reading_A") or {}
    return a.get("demonstrated", "UNRECORDED")


# --------------------------------------------------------------------------
# the five checks, exactly as the order writes them.

def d1_divergent(entry):
    a, b = entry["reading_A"], entry["reading_B"]
    if a["valence"] == "UNREAD" or b["valence"] == "UNREAD":
        return False
    if b["source"] == "ABSENT":
        return False
    return a["valence"] != b["valence"]


def d2_unflagged(entry):
    return d1_divergent(entry) and entry["flagged_by"] == "NEITHER"


def d3_silent_pass(entry):
    return d2_unflagged(entry) and entry["proceeded"] is True


def d4_unchecked(entry):
    return entry["reading_B"]["source"] == "ABSENT"


def d5_orphan_candidate(entry):
    a, b = entry["reading_A"], entry["reading_B"]
    return (b["source"] in HISTORY_SOURCES
            and b["valence"] in ("NEUTRAL", "UNREAD")
            and a["valence"] in ("POS", "NEG"))


CHECKS = (("D1_DIVERGENT", d1_divergent),
          ("D2_UNFLAGGED", d2_unflagged),
          ("D3_SILENT_PASS", d3_silent_pass),
          ("D4_UNCHECKED", d4_unchecked),
          ("D5_ORPHAN_CANDIDATE", d5_orphan_candidate))


def fired_codes(entry):
    return [code for code, fn in CHECKS if fn(entry)]


def attribution(entry):
    """Which decoder produced a valence. [CHOICE 1] for NEITHER.

    A decoder that returned UNREAD produced no valence. A reading_B whose
    source is ABSENT was never consulted, so it produced none either.
    """
    a, b = entry["reading_A"], entry["reading_B"]
    a_has = a["valence"] != "UNREAD"
    b_has = b["valence"] != "UNREAD" and b["source"] != "ABSENT"
    if a_has and b_has:
        return "SPLIT"
    if a_has:
        return "A"
    if b_has:
        return "B"
    return "NEITHER"


def d5_basis(entry):
    """[CHOICE 3] which of D5's two admitted origin states produced it.

    D5 accepts NEUTRAL or UNREAD at origin. The intake section says those
    two must never be merged -- NEUTRAL is read and found flat, UNREAD is
    not read -- and D5 is the one place in the order that merges them.
    """
    if not d5_orphan_candidate(entry):
        return None
    v = entry["reading_B"]["valence"]
    return "NEUTRAL_AT_ORIGIN" if v == "NEUTRAL" else "UNREAD_AT_ORIGIN"


# --------------------------------------------------------------------------

def read(entry):
    """Log one entry. Both readings come back intact and nothing is averaged."""
    missing, invalid = intake(entry)
    get = entry.get if isinstance(entry, dict) else (lambda k, d=None: d)

    if missing or invalid:
        return {"term": get("term"),
                "utterance_id": get("utterance_id"),
                "fired": None,                      # [CHOICE 2] no check ran
                "reading_A": get("reading_A"),
                "reading_B": get("reading_B"),
                "decoder_attribution": None,
                "d5_basis": None,
                "demonstrated": demonstrated_of(entry)
                if isinstance(entry, dict) else None,
                "grade": INTAKE_INCOMPLETE,
                "missing": missing,
                "invalid": invalid}

    return {"term": entry["term"],
            "utterance_id": entry["utterance_id"],
            "fired": fired_codes(entry),
            "reading_A": dict(entry["reading_A"]),
            "reading_B": dict(entry["reading_B"]),
            "decoder_attribution": attribution(entry),
            "d5_basis": d5_basis(entry),
            "demonstrated": demonstrated_of(entry),
            "grade": "LOGGED",
            "missing": [],
            "invalid": []}


# --------------------------------------------------------------------------
# properties the order states in prose, measured rather than asserted.

def _skeleton(a_val, a_src, b_val, b_src, flagged, proceeded):
    b = {"valence": b_val, "source": b_src, "gloss": ""}
    if b_src in CITED_SOURCES:
        b["citation"] = "probe"
        b["date_or_period"] = "probe"
    return {"term": "probe", "utterance_id": "u0", "speaker": "s",
            "reading_A": {"valence": a_val, "source": a_src, "gloss": ""},
            "reading_B": b, "flagged_by": flagged, "proceeded": proceeded}


def reachable_fired_sets():
    """Brute force the whole schema and collect every distinct `fired` list.

    Not a sample: every combination of the five declared vocabularies plus
    the two booleans, which is small enough to enumerate.
    """
    seen = {}
    total = 0
    for a_val, a_src, b_val, b_src, flagged, proceeded in itertools.product(
            VALENCES, A_SOURCES, VALENCES, B_SOURCES, FLAGGED_BY,
            (True, False)):
        entry = _skeleton(a_val, a_src, b_val, b_src, flagged, proceeded)
        total += 1
        key = tuple(fired_codes(entry))
        seen.setdefault(key, 0)
        seen[key] += 1
    return {"combinations": total,
            "sets": sorted(seen, key=lambda k: (len(k), k)),
            "counts": seen}


def co_firing():
    """Which checks ever appear in one `fired` list with which others."""
    sets = reachable_fired_sets()["sets"]
    pairs = set()
    alone = set()
    for s in sets:
        if len(s) == 1:
            alone.add(s[0])
        for x in s:
            for y in s:
                if x != y:
                    pairs.add(tuple(sorted((x, y))))
    never = [c for c in CHECK_CODES
             if not any(c in p for p in pairs)]
    return {"pairs": sorted(pairs), "fires_alone": sorted(alone),
            "never_co_fires": never}


def d1_swap_invariance():
    """No field ranks the decoders. D1 must not change when the two readings
    are exchanged; D5 is directional by design and is reported beside it."""
    d1_moves, d5_moves, tested = [], [], 0
    for a_val, b_val in itertools.product(VALENCES, VALENCES):
        for b_src in B_SOURCES:
            fwd = _skeleton(a_val, "DEFAULT", b_val, b_src, "NEITHER", True)
            # exchange the valences only; sources belong to their decoders.
            rev = _skeleton(b_val, "DEFAULT", a_val, b_src, "NEITHER", True)
            tested += 1
            if d1_divergent(fwd) != d1_divergent(rev):
                d1_moves.append((a_val, b_val, b_src))
            if d5_orphan_candidate(fwd) != d5_orphan_candidate(rev):
                d5_moves.append((a_val, b_val, b_src))
    return {"tested": tested, "d1_asymmetric_on": d1_moves,
            "d1_is_swap_invariant": not d1_moves,
            "d5_asymmetric_count": len(d5_moves)}


def absent_clause_is_live():
    """D1's guard names a VALENCE (UNREAD) and a SOURCE (ABSENT).

    If an ABSENT source always carried an UNREAD valence the source clause
    would be dead. The schema does not require that, so the clause is live
    exactly on the entries the schema should probably refuse. Measured by
    running D1 with the source clause removed.
    """
    def d1_without_source_clause(entry):
        a, b = entry["reading_A"], entry["reading_B"]
        if a["valence"] == "UNREAD" or b["valence"] == "UNREAD":
            return False
        return a["valence"] != b["valence"]

    differs = []
    for a_val, b_val, b_src in itertools.product(VALENCES, VALENCES, B_SOURCES):
        e = _skeleton(a_val, "DEFAULT", b_val, b_src, "NEITHER", True)
        if d1_divergent(e) != d1_without_source_clause(e):
            differs.append({"A": a_val, "B": b_val, "B_source": b_src})
    return {"entries_where_the_clause_changes_the_verdict": differs,
            "count": len(differs),
            "all_are_absent_with_a_valence":
                all(d["B_source"] == "ABSENT" and d["B"] != "UNREAD"
                    for d in differs)}


UNSTATED_IN_ORDER = ("flagged_by", "proceeded")


def unstated_field_effect(entry):
    """[CHOICE 9] split one entry's fired codes into invariant and contingent.

    The order fixes `flagged_by` and `proceeded` for case D alone. Anywhere
    else they were supplied here, so a code that only fires under the values
    chosen is a property of the choice and not of the case. Sweeps both
    fields over their full vocabularies and reports the intersection and the
    union across all eight combinations.
    """
    always, ever = None, set()
    for flagged in FLAGGED_BY:
        for proceeded in (True, False):
            probe = dict(entry)
            probe["flagged_by"] = flagged
            probe["proceeded"] = proceeded
            codes = set(fired_codes(probe))
            ever |= codes
            always = codes if always is None else (always & codes)
    always = always or set()
    return {"invariant": sorted(always),
            "contingent": sorted(ever - always),
            "as_entered": fired_codes(entry)}


def d5_basis_split(entries):
    """How many D5 firings came through NEUTRAL and how many through UNREAD."""
    out = {"NEUTRAL_AT_ORIGIN": 0, "UNREAD_AT_ORIGIN": 0}
    for e in entries:
        r = read(e)
        if r["d5_basis"]:
            out[r["d5_basis"]] += 1
    return out


# --------------------------------------------------------------------------

def _fmt(v, width):
    s = "--" if v is None else str(v)
    return s[:width].ljust(width)


def render(entries):
    lines = ["term            utterance A            B                     "
             "attrib   fired",
             "-" * 128]
    for e in entries:
        r = read(e)
        a = r["reading_A"] or {}
        b = r["reading_B"] or {}
        fired = "--" if r["fired"] is None else (
            ", ".join(c.split("_")[0] for c in r["fired"]) or "(none)")
        lines.append("%s %s %s %s %s %s" % (
            _fmt(r["term"], 15), _fmt(r["utterance_id"], 9),
            _fmt("%s/%s" % (a.get("valence"), a.get("source")), 12),
            _fmt("%s/%s" % (b.get("valence"), b.get("source")), 21),
            _fmt(r["decoder_attribution"], 8), fired))
        if r["grade"] == INTAKE_INCOMPLETE:
            lines.append("    missing: %s" % (r["missing"] or "(none)"))
            lines.append("    invalid: %s" % (r["invalid"] or "(none)"))
        elif r["d5_basis"]:
            lines.append("    D5 basis: %s" % r["d5_basis"])
    lines.append("")
    lines.append("fired=None means no check ran (intake); fired=(none) means "
                 "five ran and none fired.")
    lines.append("No top-level valence is emitted. Both readings come back "
                 "intact; nothing is averaged.")
    return "\n".join(lines)


def render_choices():
    lines = ["CHOICES -- decisions the order leaves open, taken here:"]
    for n in sorted(CHOICES):
        lines.append("  [CHOICE %d] %s" % (n, CHOICES[n]))
    lines.append("")
    lines.append("SCHEMA ADDITIONS beyond the order's stated return: %s"
                 % ", ".join(SCHEMA_ADDITIONS))
    return "\n".join(lines)


def main():
    if "--selftest" in sys.argv:
        # Exit 2, not 0. A module that exits clean on an invocation which
        # runs nothing reports a pass for a check nobody made -- the
        # DL_005 / CC_006 / TD_009 shape.
        sys.stderr.write("valence_divergence.py has no --selftest. "
                         "The checks are in test_valence.py:\n"
                         "    python3 test_valence.py\n")
        return 2
    import cases
    print(render_choices())
    print()
    print(render(cases.ENTRIES))
    print()
    lat = reachable_fired_sets()
    print("reachable `fired` sets, brute-forced over %d schema combinations:"
          % lat["combinations"])
    for s in lat["sets"]:
        label = "(none)" if not s else ", ".join(c.split("_")[0] for c in s)
        print("  %-24s %d combinations" % (label, lat["counts"][s]))
    co = co_firing()
    print("  fires alone: %s" % ", ".join(c.split("_")[0]
                                          for c in co["fires_alone"]))
    print("  never co-fires with anything: %s"
          % (", ".join(c.split("_")[0] for c in co["never_co_fires"]) or "(none)"))
    print()
    sw = d1_swap_invariance()
    print("no decoder is ranked: D1 swap-invariant over %d pairs: %s"
          % (sw["tested"], sw["d1_is_swap_invariant"]))
    print("  D5 is directional by design; it moves on %d of them"
          % sw["d5_asymmetric_count"])
    ab = absent_clause_is_live()
    print()
    print("D1's guard names a valence (UNREAD) and a source (ABSENT).")
    print("  entries where the source clause changes the verdict: %d"
          % ab["count"])
    print("  every one is an ABSENT source carrying a valence: %s"
          % ab["all_are_absent_with_a_valence"])
    print()
    print("D5 basis across the case set: %s" % d5_basis_split(cases.ENTRIES))
    print()
    print("[CHOICE 9] the order fixes flagged_by and proceeded for case D")
    print("only; case D is omitted below. Elsewhere the two were chosen")
    print("here, and these are the codes that choice is carrying:")
    for e in cases.ENTRIES:
        if intake(e)[0] or intake(e)[1] or e.get("order_fixes_flags"):
            continue
        eff = unstated_field_effect(e)
        if not eff["contingent"]:
            continue
        print("  %-16s invariant: %-18s contingent: %s"
              % (e["term"],
                 ", ".join(c.split("_")[0] for c in eff["invariant"]) or "--",
                 ", ".join(c.split("_")[0] for c in eff["contingent"])))


if __name__ == "__main__":
    sys.exit(main() or 0)
