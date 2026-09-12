# SPDX-License-Identifier: CC0-1.0
"""
cases.py -- the validation entries for valence_divergence.py.

EVERY ENTRY IS CONSTRUCTED. No exchange was observed, no speaker is a real
person, and no utterance here was said by anyone. `speaker` is an opaque
label as the order requires, and the labels are letters.

THE ETYMOLOGICAL CLAIMS ARE CARRIED FROM THE WORK ORDER AND ARE VERIFIED
AGAINST NOTHING HERE. There is no network in this folder and no reference
work in this repository. Every `citation` field says where the claim came
from rather than pretending to a source, which is the honest form: the
instrument stores the result of a lookup and its source, and the lookup that
produced these was somebody else's.

NO EXPECTED VERDICT LIVES IN THIS FILE. The expectations are in
test_valence.py. A case carrying its own answer cannot disagree with the
module, and an agreement produced that way measures nothing.

Branch handling, per the order: case A is TWO entries and case B is FOUR.
Nothing here links the branches of one term -- see [CHOICE 8]. Averaging
branches is the failure the instrument exists to prevent, so the branches
are not in one record to be averaged.
"""

from __future__ import annotations

CARRIED = ("carried from WORK_ORDER.md; verified against nothing in this "
           "folder")


def _e(cid, term, utt, speaker, a, b, flagged, proceeded, note):
    return {"case_id": cid, "term": term, "utterance_id": utt,
            "speaker": speaker, "reading_A": a, "reading_B": b,
            "flagged_by": flagged, "proceeded": proceeded,
            "constructed_note": note}


def _A(valence, source, gloss, demonstrated=None):
    a = {"valence": valence, "source": source, "gloss": gloss}
    if demonstrated is not None:
        a["demonstrated"] = demonstrated
    return a


def _B(valence, source, gloss, citation=None, date_or_period=None):
    b = {"valence": valence, "source": source, "gloss": gloss}
    if citation is not None:
        b["citation"] = citation
    if date_or_period is not None:
        b["date_or_period"] = date_or_period
    return b


# --------------------------------------------------------------------------
# The order's five validation cases.

# A -- hysteria. Two entries, one per branch. The order states reading_B is
# "properly MIXED once the 1939 branch is entered" and instructs that the
# branches be logged separately rather than averaged. So neither entry
# carries MIXED: each carries its own branch's valence, and MIXED is what
# you would get by doing the thing the order forbids.
A1 = _e(
    "A1", "hysteria", "u-A-01", "s1",
    _A("NEG", "DEFAULT", "reads as a pathology label, pejorative",
       demonstrated="IN_USE"),
    _B("NEUTRAL", "ETYMOLOGY",
       "Greek hystera = womb; PIE root for abdomen. Anatomical, flat.",
       CARRIED, "pre-1610s"),
    "NEITHER", True,
    "CONSTRUCTED. Order case A, anatomical branch.")

A2 = _e(
    "A2", "hysteria", "u-A-02", "s1",
    _A("NEG", "DEFAULT", "reads as a pathology label, pejorative"),
    _B("POS", "HISTORICAL_USE",
       "'very funny' sense live from 1939",
       CARRIED, "1939 onward"),
    "NEITHER", True,
    "CONSTRUCTED. Order case A, delight branch. Separate entry, not averaged "
    "with A1 -- the two together are the MIXED the order names, and that "
    "reading is the reader's to make.")

# B -- the location set. Four entries, not one.
B1 = _e(
    "B1", "savage", "u-B-01", "s2",
    _A("NEG", "DEFAULT", "reads as brutal, a slur"),
    _B("NEUTRAL", "ETYMOLOGY", "of the woods", CARRIED, "origin"),
    "NEITHER", True, "CONSTRUCTED. Order case B.")

B2 = _e(
    "B2", "pagan", "u-B-02", "s2",
    _A("NEG", "DEFAULT", "reads as godless"),
    _B("NEUTRAL", "ETYMOLOGY", "rural", CARRIED, "origin"),
    "NEITHER", True, "CONSTRUCTED. Order case B.")

B3 = _e(
    "B3", "feral", "u-B-03", "s2",
    _A("NEG", "DEFAULT", "reads as degenerate"),
    _B("NEUTRAL", "ETYMOLOGY", "wild animal", CARRIED, "origin"),
    "NEITHER", True, "CONSTRUCTED. Order case B.")

B4 = _e(
    "B4", "superstition", "u-B-04", "s2",
    _A("NEG", "DEFAULT", "reads as credulous, unscientific"),
    _B("NEUTRAL", "ETYMOLOGY",
       "an adjective meaning both pious and superstitious", CARRIED,
       "origin"),
    "NEITHER", True, "CONSTRUCTED. Order case B.")

# C -- economy. THE REQUIRED NEGATIVE. Both read NEUTRAL, nothing fires,
# the entry logs clean. An instrument that flags every term is a preference
# dressed as a method.
C_NEUTRAL = _e(
    "C_neutral", "economy", "u-C-01", "s3",
    _A("NEUTRAL", "DEFAULT", "reads as the system of production and trade"),
    _B("NEUTRAL", "ETYMOLOGY", "oikonomia = household management", CARRIED,
       "origin"),
    "NEITHER", True,
    "CONSTRUCTED. Order case C, the required negative. Economy's defect is "
    "scope collapse -- the referent shrank while the name and the authority "
    "stayed -- and this instrument cannot see it. It must not fire on it.")

# The order offers reading_A as "NEUTRAL or POS". The POS arm is the other
# half of the same case and fires, which is what makes the NEUTRAL arm a
# control rather than a case the instrument is blind to.
C_POS = _e(
    "C_pos", "economy", "u-C-02", "s3",
    _A("POS", "DEFAULT", "reads as growth, a good in itself"),
    _B("NEUTRAL", "ETYMOLOGY", "oikonomia = household management", CARRIED,
       "origin"),
    "NEITHER", True,
    "CONSTRUCTED. Order case C, second arm. Fires because the valences "
    "differ, which is the only condition D1 reads.")

# D -- the falsifier. The one failure mode the instrument was built for.
D_SILENT = _e(
    "D_silent", "resilience", "u-D-01", "s4",
    _A("NEG", "STATED", "reads as what gets demanded of whoever absorbs the "
       "cost"),
    _B("POS", "HISTORICAL_USE", "reads as a capacity worth having", CARRIED,
       "20c"),
    "NEITHER", True,
    "CONSTRUCTED. Order case D. Both proceed, neither marks the term, the "
    "divergence never surfaces.")

# Case D is the ONE entry whose flagged_by and proceeded the order fixes
# ("flagged_by NEITHER, proceeded True"). Everywhere else those two fields
# were chosen here, and [CHOICE 9] reports what the choice is carrying.
D_SILENT["order_fixes_flags"] = True


# E -- no false symmetry. An unchecked history is not a divergence.
E_ABSENT = _e(
    "E_absent", "primitive", "u-E-01", "s5",
    _A("NEG", "DEFAULT", "reads as backward"),
    _B("UNREAD", "ABSENT", "not looked up"),
    "NEITHER", True,
    "CONSTRUCTED. Order case E. Strong reading_A, history never consulted.")


# --------------------------------------------------------------------------
# Reachability. A declared value nobody populates cannot be told apart from
# one nobody looked for, so every check code, every attribution value, every
# d5 basis and every grade is reached by some entry below.

# D1 and D2 without D3: the exchange stopped. D3 is the scored failure and
# must not fire on a divergence that halted the exchange.
R_HALTED = _e(
    "R_halted", "sustainable", "u-R-01", "s6",
    _A("POS", "DEFAULT", "reads as good practice"),
    _B("NEG", "HISTORICAL_USE", "reads as the minimum that does not collapse",
       CARRIED, "20c"),
    "NEITHER", False,
    "CONSTRUCTED. Reachability: D1 and D2 fire, D3 does not, because the "
    "exchange did not proceed.")

# D1 without D2: somebody marked the term at the time of use.
R_FLAGGED = _e(
    "R_flagged", "efficient", "u-R-02", "s6",
    _A("POS", "CONTEXT", "reads as well run"),
    _B("NEG", "OTHER_CULTURE", "reads as stripped of slack", CARRIED,
       "contemporary"),
    "BOTH", True,
    "CONSTRUCTED. Reachability: flagged at the time of use, so D2 cannot "
    "fire and neither can D3. Also reaches source OTHER_CULTURE and "
    "flagged_by BOTH.")

# D5 alone, through UNREAD at origin rather than NEUTRAL. D1 is blocked by
# the UNREAD guard. [CHOICE 3] separates this basis from the NEUTRAL one.
R_D5_UNREAD = _e(
    "R_d5_unread", "quaint", "u-R-03", "s7",
    _A("NEG", "DEFAULT", "reads as condescending"),
    _B("UNREAD", "ETYMOLOGY", "the record was opened and no valence assigned",
       CARRIED, "origin"),
    "A", True,
    "CONSTRUCTED. Reachability: D5 alone, UNREAD_AT_ORIGIN. Distinct from "
    "NEUTRAL_AT_ORIGIN, which the intake section says must never be merged "
    "with it, and which D5's own condition merges.")

# [CHOICE 5]. An ABSENT source carrying a valence. The schema admits it and
# this is the only shape on which D1's source clause does any work: without
# that clause this entry would read as a divergence manufactured from a
# history nobody consulted.
R_ABSENT_VALENCE = _e(
    "R_absent_valence", "robust", "u-R-04", "s7",
    _A("NEG", "DEFAULT", "reads as brittle-in-disguise"),
    _B("POS", "ABSENT", "a valence was entered beside a source saying the "
       "history was not looked up"),
    "NEITHER", True,
    "CONSTRUCTED. Reachability: the incoherent-but-admitted entry. See "
    "[CHOICE 5] and absent_clause_is_live(). Refusing it at intake would "
    "delete the only entry on which D1's ABSENT clause changes a verdict.")

# attribution NEITHER: no decoder produced a valence at all.
R_BOTH_UNREAD = _e(
    "R_both_unread", "stakeholder", "u-R-05", "s8",
    _A("UNREAD", "DEFAULT", "no valence assigned"),
    _B("UNREAD", "STATED", "no valence assigned"),
    "NEITHER", True,
    "CONSTRUCTED. Reachability: attribution NEITHER. The order's three "
    "declared values have no cell for this -- see [CHOICE 1].")

# attribution B: only the history produced a valence.
R_ONLY_B = _e(
    "R_only_b", "husbandry", "u-R-06", "s8",
    _A("UNREAD", "DEFAULT", "the party assigned no valence"),
    _B("POS", "HISTORICAL_USE", "reads as careful keeping", CARRIED,
       "pre-modern"),
    "B", True,
    "CONSTRUCTED. Reachability: attribution B, and flagged_by B.")

# MIXED, supplied and never computed. [CHOICE 7]. The order's intake lists
# MIXED as an admissible supplied value; nothing in the module produces one.
R_MIXED = _e(
    "R_mixed", "ambition", "u-R-07", "s9",
    _A("MIXED", "STATED",
       "the party said it reads as both drive and overreach"),
    _B("NEUTRAL", "ETYMOLOGY", "going around, canvassing for votes", CARRIED,
       "origin"),
    "A", True,
    "CONSTRUCTED. Reachability: MIXED supplied by a party. See [CHOICE 7]: "
    "supplied only, never assigned or derived by this module.")

# reading_A demonstrated IN_USE vs the default UNRECORDED. [CHOICE 6].
R_ON_REQUEST = _e(
    "R_on_request", "articulate", "u-R-08", "s9",
    _A("POS", "DEFAULT", "reads as a compliment", demonstrated="ON_REQUEST"),
    _B("NEUTRAL", "ETYMOLOGY", "jointed, divided into parts", CARRIED,
       "origin"),
    "NEITHER", True,
    "CONSTRUCTED. Reachability: demonstrated ON_REQUEST -- introspected, not "
    "observed in the exchange. The Open section's unresolved problem, "
    "recorded and not enforced.")


# --------------------------------------------------------------------------
# Intake. An entry that does not parse must return INTAKE_INCOMPLETE with
# `fired` None, not an empty list: [] says five checks ran and none fired,
# which is what the required negative returns.

X_MISSING = {"case_id": "X_missing", "term": "grit",
             "utterance_id": "u-X-01", "speaker": "s10",
             "reading_A": _A("POS", "DEFAULT", "reads as perseverance"),
             "flagged_by": "NEITHER", "proceeded": True,
             "constructed_note":
                 "CONSTRUCTED. Intake: reading_B absent entirely."}

X_INVALID = _e(
    "X_invalid", "natural", "u-X-02", "s10",
    _A("GOOD", "DEFAULT", "out of vocabulary"),
    _B("NEUTRAL", "LOOKED_IT_UP", "out of vocabulary"),
    "NEITHER", True,
    "CONSTRUCTED. Intake: two out-of-vocabulary values.")

X_UNCITED = _e(
    "X_uncited", "civilized", "u-X-03", "s10",
    _A("POS", "DEFAULT", "reads as advanced"),
    _B("NEUTRAL", "ETYMOLOGY", "of the city", None, None),
    "NEITHER", True,
    "CONSTRUCTED. Intake: a cited source with no citation and no period. "
    "[CHOICE 4] -- required for ETYMOLOGY, HISTORICAL_USE and OTHER_CULTURE, "
    "optional for STATED and ABSENT.")


ENTRIES = (A1, A2, B1, B2, B3, B4, C_NEUTRAL, C_POS, D_SILENT, E_ABSENT,
           R_HALTED, R_FLAGGED, R_D5_UNREAD, R_ABSENT_VALENCE, R_BOTH_UNREAD,
           R_ONLY_B, R_MIXED, R_ON_REQUEST,
           X_MISSING, X_INVALID, X_UNCITED)

BY_ID = {e["case_id"]: e for e in ENTRIES}

# The order's five validation cases, by the letter the order gives them.
ORDER_CASES = {"A": ("A1", "A2"),
               "B": ("B1", "B2", "B3", "B4"),
               "C": ("C_neutral", "C_pos"),
               "D": ("D_silent",),
               "E": ("E_absent",)}
