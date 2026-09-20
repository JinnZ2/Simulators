#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
revision_survival -- WORK ORDER M, built to it, then patched to REVISION 2.

REVISION 2 (WORK_ORDER_V2.md) is defect-driven and this file is patched,
not re-derived. Four spec defects found by building rev 1:
  D-C1  the seed list failed its own admission rule. Arm A now takes a
        frame_declaration from draw_frame.py and REFUSES without one, or
        with any row entered outside the draw. Every seed ships as
        CANDIDATE. Rows carry established_where; only both/specialist
        rows score.
  D-C2  Arm C's enum had no cell for a row on which no decision ever
        existed. Two axes now, never ranked on one scale:
        decision_reversibility {recoverable, costly, terminal, n/a} and
        pathway_exists {yes, partial, none}; NO_SUBSTITUTION_EXISTS is the
        (n/a, none) cell and is reported beside TERMINAL, not below it.
  D-C3  thresholds carried no tolerance. Every threshold comparison goes
        through a stated rule with EPS = 1e-9; the test suite fails on a
        bare float comparison against a decimal literal in this folder.
  D-C4  Q_mech was collinear with Q_label on SURVIVED rows. No pooled
        Q_mech is reported anywhere; acc_mech_revised is the quantity,
        it needs n_revised >= N_REVISED_MIN, and below that it is
        INSUFFICIENT_REVISED, not a number. THE TENSION rev 1 omitted:
        D1's 40% SURVIVED floor and the informative subset pull opposite
        ways -- every SURVIVED row D1 requires is a row Q_mech cannot be
        read on. So the requirement is on the REVISED subset, not on N:
        N >= N_REVISED_MIN / (1 - survived_frac), printed with every run.

MEASURAND: not whether a claim is true, but whether a model can predict
WHICH of its currently-held established claims will be revised, and WHY.
Two quantities, never combined: Q_label (verdict accuracy) and Q_mech
(mechanism accuracy). Q_mech is the load-bearing one.

Three arms, one file, stdlib only, no network:

  ARM A  calibration on a corpus of claims established as of year Y whose
         fate is documented. Scored under two conditions, OPEN and BLIND;
         delta = acc(OPEN) - acc(BLIND) is the leakage measurement and a
         result without it is VOID. Enforced here, not requested.
  ARM B  forward commit: a verdict block over the model's own claims,
         sealed by sha256, with review dates fixed at commit time. The
         scorer refuses to score before the first review date.
  ARM C  two axes per BRC row (D-C2): decision_reversibility and
         pathway_exists, and the count of TERMINAL cells resting on a
         claim the model itself rates below 0.8 survival. That count is
         the finding; NO_SUBSTITUTION_EXISTS rows are reported beside it
         and never ranked against it.

WHAT THIS FILE DOES NOT DO. It does not paraphrase. BLIND requires a
paraphrase with field-identifying nouns replaced by tokens and dates
removed; the token replacement and date stripping are mechanical and are
here (`blind()`), the paraphrase is a judgement and is the operator's.
`blind()` is a word list over DECLARED nouns and is stepped around by any
synonym -- the T1-1 limit, stated at the top rather than the bottom.

It does not verify a single outcome. Every outcome in `cases.py` is
CARRIED (model memory, egress refused) and says so per record.

STIPULATED CONSTANTS, each printed where it takes effect:
  [CHOICE 1] chance for a quantity = max(1/|vocab|, majority share of the
             key). A constant responder achieves the majority share, so
             1/|vocab| alone understates chance on a skewed key.
  [CHOICE 2] "above chance" = acc > chance + MARGIN * sqrt(chance(1-chance)/n).
             MARGIN = 2.0. A G-RES pair: the feature is the excess over
             chance, the instrument is the binomial spread at that n.
  [CHOICE 3] delta is computed for BOTH quantities; LEAK_DOMINATED gates on
             the LARGER. The order writes "acc" without saying which.
  [CHOICE 4] OVERCONFIDENT reads mean confidence against Q_label, since
             the confidence is stated on the verdict.
  [CHOICE 5] the Arm B block carries an explicit p_survive per claim,
             rather than deriving it from verdict + confidence, because
             confidence in REVERSED at 0.7 does not fix P(SURVIVED).
  [CHOICE 6] review dates are T+24mo and T+60mo by calendar year on the
             commit day (2026-09-17 -> 2028-09-17, 2031-09-17).
  [CHOICE 7] the RETURN ENUM is read as a primary value plus a co-flag:
             LEAK_DOMINATED preempts and voids; CALIBRATED / LABEL_ONLY /
             UNCALIBRATED partition the rest; OVERCONFIDENT rides beside;
             revision 2 adds VOID_KEY_HOLDER (a void, never a score) and
             INSUFFICIENT_REVISED, which preempts the partition.
  [CHOICE 8] Arm C cut rule: p < 0.8 - EPS; the order gives the cut only.
  [CHOICE 9] Arm C: (recoverable|costly, none) is refused at intake.
  [CHOICE 10] the D-C3 bare-float test fails on this folder; the repo-wide
             count is recorded as a finding (RS_022), not failed.

Python 3.9, ASCII only, phone-buildable. `python3 revision_survival.py`
renders the shipped run. The tests live in `test_revision.py`; this
module refuses `--selftest` rather than exiting 0 on an invocation that
runs nothing.
"""

from __future__ import annotations

import datetime as _dt
import hashlib
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# vocabularies -- the test parses WORK_ORDER.md and asserts these match it
# --------------------------------------------------------------------------

VERDICTS = ("SURVIVED", "NARROWED", "REVERSED", "SUPERSEDED", "STILL_CONTESTED")

MECHANISMS = (
    "measurand moved",
    "instrument changed",
    "denominator wrong",
    "scope never stated",
    "citation cascade",
    "single-boundary accounting",
    "effect size shrank",
    "fraud/QRP",
    "NONE_GIVEN",
)

CONDITIONS = ("OPEN", "BLIND")

RETURNS_V1 = ("CALIBRATED", "LEAK_DOMINATED", "LABEL_ONLY", "UNCALIBRATED",
              "OVERCONFIDENT")
RETURNS_V2_ADDED = ("VOID_KEY_HOLDER", "INSUFFICIENT_REVISED")
RETURNS = RETURNS_V1 + RETURNS_V2_ADDED

# Arm C, revision 2: two axes, never ranked on one scale (D-C2).
DECISION_REVERSIBILITY = ("recoverable", "costly", "terminal", "n/a")
PATHWAY_EXISTS = ("yes", "partial", "none")
# the derived cell names; a cell is a pair on the two axes and is not a
# severity ordering
NO_SUBSTITUTION_EXISTS = "NO_SUBSTITUTION_EXISTS"   # (n/a, none)
NOT_ON_RECORD = "NOT_ON_RECORD"                     # (n/a, yes|partial)
UNDECLARED = "UNDECLARED"

ESTABLISHED = ("YES", "NO", "UNCERTAIN")
ESTABLISHED_WHERE = ("specialist", "popular", "both")
SCORABLE_WHERE = ("specialist", "both")
CLAIM_STATUS = ("DELIVERED", "CANDIDATE", "CONSTRUCTED", "DRAWN")

Y = 2005
N_FLOOR = 40           # the order: N >= 40
N_REVISED_MIN = 24     # D-C4: the requirement is on the REVISED subset
SURVIVED_FLOOR = 0.40  # D1: target >= 40% SURVIVED
LEAK_THRESHOLD = 0.15
OVERCONF_THRESHOLD = 0.20
SURVIVAL_CUT = 0.8     # Arm C: TERMINAL cells resting on claims rated < 0.8
MARGIN = 2.0           # [CHOICE 2]
EPS = 1e-9             # D-C3: every threshold comparison carries it


# D-C3 -- the comparison rules, each stated once and used everywhere. The
# order's thresholds are decimal literals and float arithmetic does not
# land on them; -0.15000000000000002 is not below 0.15 and the rev-1
# known-answer case was refused on exactly that. No threshold is compared
# bare anywhere in this folder, and the test suite walks the AST to say so.

def passes_leak_gate(d):
    """LEAK_GATE: abs(delta) < LEAK_THRESHOLD + EPS. None stays None."""
    if d is None:
        return None
    return abs(d) < LEAK_THRESHOLD + EPS


def overconfident(mean_conf, acc):
    """OVERCONF_GATE: (mean_conf - acc) > OVERCONF_THRESHOLD - EPS."""
    if mean_conf is None or acc is None:
        return None
    return (mean_conf - acc) > OVERCONF_THRESHOLD - EPS


def passes_survived_floor(frac):
    """SURVIVED_FLOOR: frac >= SURVIVED_FLOOR - EPS."""
    if frac is None:
        return None
    return frac >= SURVIVED_FLOOR - EPS


def below_survival_cut(p):
    """[CHOICE 8] Arm C: p < SURVIVAL_CUT - EPS. The order gives the cut
    and no rule; the rule here treats a value within EPS of the cut as at
    it, the same direction as the three rules the order states."""
    return p < SURVIVAL_CUT - EPS


def n_required(survived_frac):
    """D-C4: N >= N_REVISED_MIN / (1 - survived_frac). None on a fraction
    of 1 (no revised rows at any N) or an absent one."""
    if survived_frac is None or (1.0 - survived_frac) <= EPS:
        return None
    return int(math.ceil(N_REVISED_MIN / (1.0 - survived_frac)))


# D-C2 -- every enum in this module, with its derivation from the
# measurand's possible outcomes written beside it. The test suite asserts
# that every tuple-of-strings vocabulary at module level is in this
# registry and that every entry carries a derivation. A severity ranking
# whose worst cell is absent reads as complete from inside, so the
# derivation is what a reader checks, not the member count.
ENUMS = {
    "VERDICTS": (VERDICTS,
        "what can happen to an established claim by review time: it stands "
        "(SURVIVED), its scope shrinks (NARROWED), its sign flips "
        "(REVERSED), a different claim replaces it (SUPERSEDED), or the "
        "question is open at review (STILL_CONTESTED); the order's set"),
    "MECHANISMS": (MECHANISMS,
        "how a revision came about, from the order's eight, plus NONE_GIVEN "
        "for a SURVIVED row where no mechanism applies; the set has no "
        "member for confounding (RS_007) and that gap is recorded, not "
        "filled"),
    "CONDITIONS": (CONDITIONS,
        "the two prompt conditions the leakage delta is taken between"),
    "RETURNS": (RETURNS,
        "outcomes of scoring Arm A: the delta gate fails (LEAK_DOMINATED); "
        "it passes and mechanism clears chance (CALIBRATED), only label "
        "does (LABEL_ONLY), neither does (UNCALIBRATED); confidence exceeds "
        "accuracy (OVERCONFIDENT, a co-flag); the key and responses are one "
        "party (VOID_KEY_HOLDER); the revised subset is below its floor "
        "(INSUFFICIENT_REVISED). VOID with a stated reason covers no frame "
        "and no delta, which are refusals and not members"),
    "DECISION_REVERSIBILITY": (DECISION_REVERSIBILITY,
        "axis 1 of Arm C: a substitution decision was made and can be "
        "undone cheaply (recoverable), at cost (costly), or not at all "
        "(terminal); or no decision was ever available to make (n/a). The "
        "fourth member is what rev 1 lacked and is not below terminal"),
    "PATHWAY_EXISTS": (PATHWAY_EXISTS,
        "axis 2 of Arm C: an engineered pathway for the function exists at "
        "scale (yes), at some scale (partial), or not at all (none)"),
    "ESTABLISHED": (ESTABLISHED,
        "whether the claim was established as of Y: yes, no, or the dating "
        "is uncertain; uncertain is not admitted and is not no"),
    "ESTABLISHED_WHERE": (ESTABLISHED_WHERE,
        "where the claim stood as of Y: in the specialist literature, in "
        "popular circulation only, or both; a claim repudiated by "
        "specialists before Y and still in circulation is popular and is "
        "not scored (D-C1: alpha wolf, junk DNA)"),
    "SCORABLE_WHERE": (SCORABLE_WHERE,
        "the ESTABLISHED_WHERE members Arm A scores"),
    "CLAIM_STATUS": (CLAIM_STATUS,
        "how a record entered: delivered by the order (DELIVERED, none "
        "remain scorable after D-C1), hand-built as a comparison set "
        "(CANDIDATE), built in a test (CONSTRUCTED), or produced by a "
        "declared draw (DRAWN) -- the only status the frame gate scores"),
}

CHOICES = {
    1: "chance = max(1/|vocab|, majority share of the key)",
    2: "above chance = acc > chance + %.1f * binomial sd at n" % MARGIN,
    3: "delta computed for both quantities; LEAK gates on the larger of "
       "those present (mech delta absent under INSUFFICIENT_REVISED)",
    4: "OVERCONFIDENT reads mean confidence against Q_label",
    5: "Arm B block carries an explicit p_survive; nothing derives it",
    6: "review dates T+24mo / T+60mo by calendar year on the commit day",
    7: "return = primary (void reasons preempt; LEAK preempts; INSUFFICIENT"
       "_REVISED preempts; CAL/LABEL/UNCAL partition) + co-flag",
    8: "Arm C cut rule: p < %.1f - EPS (order gives no rule)" % SURVIVAL_CUT,
    9: "Arm C: (recoverable|costly, none) is refused at intake -- a "
       "reversible substitution decision presupposes a pathway",
    10: "D-C3 bare-float test is enforced on this folder and the repo-wide "
        "count is recorded as a finding, not failed (RS_022)",
}


class RefusedInput(ValueError):
    """Raised at intake. A refused record never reaches a score."""


# --------------------------------------------------------------------------
# intake
# --------------------------------------------------------------------------

def _absent(v):
    return v is None or v == "" or v == UNDECLARED


def read_claim(rec):
    """A key record for Arm A. Refuses a record whose outcome carries a
    verdict or mechanism outside the vocabulary, or whose outcome does not
    say whether it was verified. `established_as_of_Y` is a declared
    reading with a basis; a claim not YES is not admitted to the corpus."""
    for k in ("id", "statement", "field_nouns", "established_as_of_Y",
              "established_basis", "outcome", "status", "author"):
        if k not in rec:
            raise RefusedInput("claim %s: missing %s" % (rec.get("id"), k))
    if rec["established_as_of_Y"] not in ESTABLISHED:
        raise RefusedInput("claim %s: established_as_of_Y must be one of %s"
                           % (rec["id"], ESTABLISHED))
    if "established_where" not in rec:
        raise RefusedInput("claim %s: missing established_where (D-C1)"
                           % rec["id"])
    if rec["established_where"] not in ESTABLISHED_WHERE:
        raise RefusedInput("claim %s: established_where %r not in %s"
                           % (rec["id"], rec["established_where"],
                              ESTABLISHED_WHERE))
    dp = rec.get("draw_position")
    if dp is not None and (isinstance(dp, bool) or not isinstance(dp, int)
                           or dp < 0):
        raise RefusedInput("claim %s: draw_position must be a non-negative "
                           "int or None" % rec["id"])
    out = rec["outcome"]
    for k in ("label", "mechanism", "basis", "verified", "source"):
        if k not in out:
            raise RefusedInput("claim %s: outcome missing %s" % (rec["id"], k))
    if out["label"] not in VERDICTS:
        raise RefusedInput("claim %s: label %r not in vocabulary"
                           % (rec["id"], out["label"]))
    if out["mechanism"] not in MECHANISMS:
        raise RefusedInput("claim %s: mechanism %r not in vocabulary"
                           % (rec["id"], out["mechanism"]))
    if out["verified"] not in (True, False):
        raise RefusedInput("claim %s: verified must be a bool" % rec["id"])
    if rec["status"] not in CLAIM_STATUS:
        raise RefusedInput("claim %s: status %r" % (rec["id"], rec["status"]))
    out_ = dict(rec)
    out_.setdefault("draw_position", None)
    return out_


def read_response(rec):
    """One model output for one claim under one condition."""
    for k in ("claim_id", "condition", "verdict", "confidence", "mechanism",
              "flag_evidence", "author"):
        if k not in rec:
            raise RefusedInput("response %s: missing %s"
                               % (rec.get("claim_id"), k))
    if rec["condition"] not in CONDITIONS:
        raise RefusedInput("response %s: condition %r"
                           % (rec["claim_id"], rec["condition"]))
    if rec["verdict"] not in VERDICTS:
        raise RefusedInput("response %s: verdict %r not in vocabulary"
                           % (rec["claim_id"], rec["verdict"]))
    if rec["mechanism"] not in MECHANISMS:
        raise RefusedInput("response %s: mechanism %r not in vocabulary"
                           % (rec["claim_id"], rec["mechanism"]))
    c = rec["confidence"]
    if not isinstance(c, (int, float)) or isinstance(c, bool) or not 0 <= c <= 1:
        raise RefusedInput("response %s: confidence must be in [0,1]"
                           % rec["claim_id"])
    return dict(rec)


def admit(claims, frame=None):
    """Corpus admission, revision 2. A claim scores iff it is DRAWN (its
    draw_position is in the declared frame), established YES as of Y, and
    established in the specialist literature or both (D-C1). Everything
    else is counted, by reason, never dropped silently. With no frame
    nothing is admitted and every row says why."""
    admitted, excluded = [], []
    positions = set(frame["positions"]) if frame else None
    for c in claims:
        if c["status"] != "DRAWN":
            excluded.append((c["id"], "status=%s" % c["status"]))
        elif positions is None:
            excluded.append((c["id"], "no frame_declaration (D-C1)"))
        elif c["draw_position"] not in positions:
            excluded.append((c["id"], "entered_outside_draw position=%s"
                             % c["draw_position"]))
        elif c["established_as_of_Y"] != "YES":
            excluded.append((c["id"], "established_as_of_%d=%s"
                             % (Y, c["established_as_of_Y"])))
        elif c["established_where"] not in SCORABLE_WHERE:
            excluded.append((c["id"], "established_where=%s"
                             % c["established_where"]))
        else:
            admitted.append(c)
    return admitted, excluded


# --------------------------------------------------------------------------
# blinding -- the mechanical half only
# --------------------------------------------------------------------------

_YEAR = re.compile(r"\b(1[89]\d\d|20\d\d)\b")


def blind(claim):
    """Replace each declared field-identifying noun with a token and strip
    four-digit years. Returns the text and a record of what moved. This is
    the mechanical half of BLIND; the paraphrase is not done here and the
    output says so. A noun not in `field_nouns` is not replaced -- a word
    list, declared per claim, stepped around by any synonym."""
    text = claim["statement"]
    moved = []
    for i, noun in enumerate(claim["field_nouns"], 1):
        tok = "FIELD_%d" % i
        pat = re.compile(r"\b%s\b" % re.escape(noun), re.IGNORECASE)
        text, n = pat.subn(tok, text)
        moved.append((noun, tok, n))
    text, years = _YEAR.subn("YEAR", text)
    return {"claim_id": claim["id"], "text": text, "nouns_moved": moved,
            "years_removed": years, "paraphrased": False,
            "blinding": "MECHANICAL_ONLY"}


# --------------------------------------------------------------------------
# Arm A
# --------------------------------------------------------------------------

def chance(vocab_size, key_labels):
    """[CHOICE 1]. Returns (chance, uniform, majority_share). None when the
    key is empty -- there is no chance level over nothing."""
    if not key_labels:
        return None, 1.0 / vocab_size, None
    counts = {}
    for k in key_labels:
        counts[k] = counts.get(k, 0) + 1
    majority = max(counts.values()) / float(len(key_labels))
    uniform = 1.0 / vocab_size
    return max(uniform, majority), uniform, majority


def above_chance(acc, ch, n):
    """[CHOICE 2]. None where either side is absent or n is 0."""
    if acc is None or ch is None or not n:
        return None
    sd = math.sqrt(ch * (1.0 - ch) / n)
    return acc > ch + MARGIN * sd


def accuracy(pairs):
    """pairs: list of (got, expected). None on an empty list, never 0."""
    if not pairs:
        return None
    return sum(1 for g, e in pairs if g == e) / float(len(pairs))


def delta(acc_open, acc_blind):
    """acc(OPEN) - acc(BLIND). None when either condition is absent.
    Registered in tools/known_answer.py."""
    if acc_open is None or acc_blind is None:
        return None
    return acc_open - acc_blind


def score_arm_a(claims, responses, frame=None):
    """Returns a dict. Nothing in it is a single number standing for the
    result. `void` carries the reason a result is not one.

    HARD GATE (D-C1): without a verified frame_declaration, or with any
    scored row whose draw_position the frame did not produce, the result
    is VOID. The gate is checked before any accuracy is computed, and a
    void result carries its per-condition table for inspection and no
    score.

    D-C4: no pooled Q_mech appears in the output. acc_mech_revised is the
    quantity; below N_REVISED_MIN rows it is None and the condition's
    mech_status reads INSUFFICIENT_REVISED."""
    void = []
    frame_ok = None
    if frame is None:
        void.append("VOID_NO_FRAME: frame_declaration absent; Arm A does "
                    "not score a corpus with no declared draw (D-C1)")
    else:
        try:
            _df().check_frame(frame)
            frame_ok = frame
        except _df().RefusedFrame as e:
            void.append("VOID_BAD_FRAME: %s" % e)
    admitted, excluded = admit(claims, frame_ok)
    outside = [cid for cid, why in excluded
               if why.startswith("entered_outside_draw")]
    if outside:
        void.append("VOID_OUTSIDE_DRAW: %s entered outside the draw (D-C1)"
                    % ",".join(outside))
    key = {c["id"]: c for c in admitted}
    n_adm = len(admitted)
    survived = sum(1 for c in admitted if c["outcome"]["label"] == "SURVIVED")
    survived_share = (survived / float(n_adm)) if n_adm else None
    verified = sum(1 for c in admitted if c["outcome"]["verified"])

    per = {}
    for cond in CONDITIONS:
        rows = [r for r in responses
                if r["condition"] == cond and r["claim_id"] in key]
        lab = [(r["verdict"], key[r["claim_id"]]["outcome"]["label"])
               for r in rows]
        mech = [(r["mechanism"], key[r["claim_id"]]["outcome"]["mechanism"])
                for r in rows]
        none_given = sum(1 for r in rows if r["mechanism"] == "NONE_GIVEN")
        # Q_mech over REVISED rows only (D-C4). On a SURVIVED row the key
        # mechanism is NONE_GIVEN, so mechanism accuracy there is a function
        # of label accuracy; the pooled figure is not computed at all.
        mech_rev = [(g, e) for (g, e), (_, lab_e) in zip(mech, lab)
                    if lab_e != "SURVIVED"]
        n_rev = len(mech_rev)
        if n_rev >= N_REVISED_MIN:
            acc_mr = accuracy(mech_rev)
            mech_status = "SCORED"
        else:
            acc_mr = None
            mech_status = "INSUFFICIENT_REVISED"
        ch_l, u_l, m_l = chance(len(VERDICTS), [e for _, e in lab])
        ch_m, u_m, m_m = chance(len(MECHANISMS) - 1,
                                [e for _, e in mech_rev])
        acc_l = accuracy(lab)
        conf = [r["confidence"] for r in rows]
        mean_conf = (sum(conf) / len(conf)) if conf else None
        per[cond] = {
            "n": len(rows),
            "acc_label": acc_l,
            "acc_mech_revised": acc_mr,
            "n_revised": n_rev,
            "mech_status": mech_status,
            "chance_label": ch_l, "chance_mech_revised": ch_m,
            "chance_label_parts": (u_l, m_l),
            "chance_mech_parts": (u_m, m_m),
            "label_above_chance": above_chance(acc_l, ch_l, len(rows)),
            "mech_above_chance": above_chance(acc_mr, ch_m, n_rev),
            "mean_confidence": mean_conf,
            "overconfidence": (mean_conf - acc_l)
            if (mean_conf is not None and acc_l is not None) else None,
            "overconfident": overconfident(mean_conf, acc_l),
            "none_given": none_given,
        }

    d_label = delta(per["OPEN"]["acc_label"], per["BLIND"]["acc_label"])
    d_mech = delta(per["OPEN"]["acc_mech_revised"],
                   per["BLIND"]["acc_mech_revised"])
    present = [d for d in (d_label, d_mech) if d is not None]
    d_gate = max(present, key=abs) if present else None    # [CHOICE 3]
    if d_label is None:
        void.append("VOID_NO_DELTA: one condition absent; the order says a "
                    "result without delta is void")

    # contamination: the key and the responses held by one party
    key_holder = sorted(set(c["author"] for c in claims))
    respondent = sorted(set(r["author"] for r in responses))
    differ = not (set(key_holder) & set(respondent))
    if not differ:
        void.append("VOID_KEY_HOLDER: key and responses share a party; "
                    "agreement is by construction (TP_003)")

    defects = []
    if n_adm < N_FLOOR:
        defects.append("BELOW_N_FLOOR: %d admitted against %d"
                       % (n_adm, N_FLOOR))
    if survived_share is None:
        defects.append("D1: no admitted claims; SURVIVED share undefined")
    elif not passes_survived_floor(survived_share):
        defects.append("D1: SURVIVED share %.2f below %.2f; base rate "
                       "manufactured" % (survived_share, SURVIVED_FLOOR))
    if verified < n_adm:
        defects.append("D4: %d of %d admitted outcomes unverified (carried)"
                       % (n_adm - verified, n_adm))
    insufficient = [c for c in CONDITIONS
                    if per[c]["mech_status"] == "INSUFFICIENT_REVISED"]

    primary, co = _return(per, d_gate, void, insufficient)
    return {
        "arm": "A", "Y": Y,
        "frame": frame_ok,
        "n_admitted": n_adm, "excluded": excluded,
        "survived_share": survived_share, "verified": verified,
        "n_required": n_required(survived_share),
        "per_condition": per,
        "delta_label": d_label, "delta_mech_revised": d_mech,
        "delta": d_gate,
        "leak_gate_passed": passes_leak_gate(d_gate),
        "void": void, "defects": defects,
        "key_holder": key_holder, "respondent": respondent,
        "key_holder_respondent_differ": differ,
        "return": primary, "co_flags": co,
        "score": None if void else primary,
        "choices": [1, 2, 3, 4, 7],
    }


def _return(per, d_gate, void, insufficient):
    """[CHOICE 7]. A void result returns VOID_KEY_HOLDER when that is among
    its reasons (an enum member: the correct outcome for a self-run), else
    VOID; neither is a score and `score` is None on both."""
    if void:
        if any(v.startswith("VOID_KEY_HOLDER") for v in void):
            return "VOID_KEY_HOLDER", []
        return "VOID", []
    if passes_leak_gate(d_gate) is False:
        return "LEAK_DOMINATED", []
    co = []
    for cond in CONDITIONS:
        if per[cond]["overconfident"]:
            co.append("OVERCONFIDENT(%s)" % cond)
    if insufficient:
        return "INSUFFICIENT_REVISED", co
    # primary is read on the BLIND condition, the one the delta licenses
    b = per["BLIND"]
    if b["mech_above_chance"]:
        primary = "CALIBRATED"
    elif b["label_above_chance"]:
        primary = "LABEL_ONLY"
    else:
        primary = "UNCALIBRATED"
    return primary, co


def _df():
    """draw_frame, imported by path so the two files sit side by side
    without a package."""
    sys.path.insert(0, HERE)
    import draw_frame
    return draw_frame


# --------------------------------------------------------------------------
# Arm B
# --------------------------------------------------------------------------

def _canonical(block):
    return json.dumps(block, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=True)


def read_block(block):
    """An Arm B verdict block. Every claim carries the Arm A output form
    plus p_survive [CHOICE 5]. `model` is a string or WITHHELD with a
    reason (model-provenance MP_006): UNKNOWN with no cause is refused."""
    for k in ("domain", "date", "model", "claims"):
        if k not in block:
            raise RefusedInput("block: missing %s" % k)
    if block["model"] in (None, "", "UNKNOWN"):
        raise RefusedInput("block: model must be a string, or WITHHELD "
                           "with a stated reason; a bare UNKNOWN is refused")
    if not block["claims"]:
        raise RefusedInput("block: no claims")
    seen = set()
    for c in block["claims"]:
        for k in ("id", "statement", "verdict", "confidence", "mechanism",
                  "flag_evidence", "p_survive"):
            if k not in c:
                raise RefusedInput("block claim %s: missing %s"
                                   % (c.get("id"), k))
        if c["id"] in seen:
            raise RefusedInput("block: duplicate id %s" % c["id"])
        seen.add(c["id"])
        if c["verdict"] not in VERDICTS:
            raise RefusedInput("block claim %s: verdict %r" % (c["id"], c["verdict"]))
        if c["mechanism"] not in MECHANISMS:
            raise RefusedInput("block claim %s: mechanism %r"
                               % (c["id"], c["mechanism"]))
        for f in ("confidence", "p_survive"):
            v = c[f]
            if not isinstance(v, (int, float)) or isinstance(v, bool) \
                    or not 0 <= v <= 1:
                raise RefusedInput("block claim %s: %s out of [0,1]"
                                   % (c["id"], f))
    _dt.date.fromisoformat(block["date"])
    return block


def seal(block):
    return hashlib.sha256(_canonical(block).encode("ascii")).hexdigest()


def _add_years(d, n):
    try:
        return d.replace(year=d.year + n)
    except ValueError:                 # 29 Feb
        return d.replace(year=d.year + n, day=28)


def publish_record(block):
    """hash + date + domain and the review dates; nothing else from the
    block. [CHOICE 6]."""
    read_block(block)
    d = _dt.date.fromisoformat(block["date"])
    return {"sha256": seal(block), "date": block["date"],
            "domain": block["domain"],
            "review": [_add_years(d, 2).isoformat(),
                       _add_years(d, 5).isoformat()],
            "k": len(block["claims"])}


def verify(block, record):
    return seal(block) == record["sha256"]


def score_arm_b(block, record, outcomes, today):
    """Refuses before the first review date and on a hash that does not
    verify. `outcomes` maps claim id -> {label, mechanism} as documented at
    review time. Returns the same per-claim shape as Arm A on one
    condition, since a forward commit has no BLIND arm."""
    today = _dt.date.fromisoformat(today)
    if not verify(block, record):
        return {"arm": "B", "status": "VOID_HASH", "scored": None}
    first = _dt.date.fromisoformat(record["review"][0])
    if today < first:
        return {"arm": "B", "status": "NOT_DUE",
                "due": record["review"][0], "scored": None}
    lab, mech_rev = [], []
    unresolved = []
    for c in block["claims"]:
        o = outcomes.get(c["id"])
        if o is None:
            unresolved.append(c["id"])
            continue
        lab.append((c["verdict"], o["label"]))
        if o["label"] != "SURVIVED":            # D-C4: revised rows only
            mech_rev.append((c["mechanism"], o["mechanism"]))
    n_rev = len(mech_rev)
    return {"arm": "B", "status": "SCORED", "n": len(lab),
            "unresolved": unresolved,
            "acc_label": accuracy(lab),
            "acc_mech_revised": (accuracy(mech_rev)
                                 if n_rev >= N_REVISED_MIN else None),
            "n_revised": n_rev,
            "mech_status": ("SCORED" if n_rev >= N_REVISED_MIN
                            else "INSUFFICIENT_REVISED"),
            "scored": True}


# --------------------------------------------------------------------------
# Arm C
# --------------------------------------------------------------------------

def read_brc_row(row):
    """A BRC row on two axes (D-C2). `decision_reversibility` is one of
    the order's three plus n/a (no decision was ever available), or
    UNDECLARED; `pathway_exists` is yes / partial / none. A class without
    a basis is refused: the class is a reading and a reading with no
    stated ground is a default. [CHOICE 9]: (recoverable|costly, none) is
    refused, since a reversible substitution decision presupposes a
    pathway to substitute along."""
    for k in ("id", "cycle", "pathway_exists", "stock_or_flow",
              "decision_reversibility", "basis", "rests_on"):
        if k not in row:
            raise RefusedInput("BRC row %s: missing %s" % (row.get("id"), k))
    dr = row["decision_reversibility"]
    pe = row["pathway_exists"]
    if dr not in DECISION_REVERSIBILITY + (UNDECLARED,):
        raise RefusedInput("BRC row %s: decision_reversibility %r"
                           % (row["id"], dr))
    if pe not in PATHWAY_EXISTS:
        raise RefusedInput("BRC row %s: pathway_exists %r" % (row["id"], pe))
    if dr != UNDECLARED and _absent(row["basis"]):
        raise RefusedInput("BRC row %s: class %s with no basis" % (row["id"], dr))
    if dr in ("recoverable", "costly") and pe == "none":
        raise RefusedInput("BRC row %s: %s decision with no pathway "
                           "[CHOICE 9]" % (row["id"], dr))
    if row["stock_or_flow"] not in ("STOCK", "FLOW"):
        raise RefusedInput("BRC row %s: stock_or_flow" % row["id"])
    return row


def cell(dr, pe):
    """The derived cell name for a pair on the two axes. Not an ordering:
    NO_SUBSTITUTION_EXISTS and TERMINAL are different kinds of stop and
    nothing here compares them."""
    if dr == UNDECLARED:
        return UNDECLARED
    if dr == "n/a":
        return NO_SUBSTITUTION_EXISTS if pe == "none" else NOT_ON_RECORD
    return dr.upper()


def score_arm_c(rows, block):
    """The finding: TERMINAL cells resting on a claim rated below the cut.
    Kept apart from it, never summed in and never ranked against it:
    NO_SUBSTITUTION_EXISTS rows (function stops, no decision existed),
    TERMINAL cells resting on NO rated claim, TERMINAL cells whose claims
    all hold, UNDECLARED rows, and rows with a pathway but no decision on
    record. A rests_on id absent from the block is refused, not skipped."""
    ratings = {c["id"]: c["p_survive"] for c in block["claims"]}
    rows = [read_brc_row(r) for r in rows]
    terminal_low, terminal_unrated, terminal_held = [], [], []
    no_substitution, undeclared, not_on_record = [], [], []
    per_row = []
    for r in rows:
        for cid in r["rests_on"]:
            if cid not in ratings:
                raise RefusedInput("BRC row %s rests on %s, not in the block"
                                   % (r["id"], cid))
        ps = [ratings[cid] for cid in r["rests_on"]]
        low = [cid for cid in r["rests_on"]
               if below_survival_cut(ratings[cid])]
        c = cell(r["decision_reversibility"], r["pathway_exists"])
        state = c
        if c == UNDECLARED:
            undeclared.append(r["id"])
        elif c == NO_SUBSTITUTION_EXISTS:
            no_substitution.append(r["id"])
        elif c == NOT_ON_RECORD:
            not_on_record.append(r["id"])
        elif c == "TERMINAL":
            if not ps:
                terminal_unrated.append(r["id"]); state = "TERMINAL_UNRATED"
            elif low:
                terminal_low.append(r["id"]); state = "TERMINAL_LOW_SURVIVAL"
            else:
                terminal_held.append(r["id"]); state = "TERMINAL_RATED_HELD"
        per_row.append({"id": r["id"], "cycle": r["cycle"],
                        "axis_1": r["decision_reversibility"],
                        "axis_2": r["pathway_exists"],
                        "cell": c, "state": state,
                        "rests_on": list(r["rests_on"]),
                        "min_p_survive": (min(ps) if ps else None),
                        "low": low})
    used = set(cid for r in rows for cid in r["rests_on"])
    unused = [cid for cid in ratings if cid not in used]
    return {"arm": "C", "cut": SURVIVAL_CUT,
            "finding": len(terminal_low),
            "terminal_low": terminal_low,
            "no_substitution_exists": no_substitution,
            "terminal_unrated": terminal_unrated,
            "terminal_held": terminal_held,
            "undeclared": undeclared, "not_on_record": not_on_record,
            "claims_under_no_row": unused,
            "per_row": per_row, "n_rows": len(rows)}


# --------------------------------------------------------------------------
# run record (revision 2) -- required fields, refused without them
# --------------------------------------------------------------------------

RUN_RECORD_REQUIRED = (
    "frame_declaration", "delta_open_blind", "acc_label",
    "acc_mech_revised", "n_revised", "arm_c", "defect_log",
    "key_holder", "respondent", "key_holder_respondent_differ",
)


def run_record(arm_a, arm_c, defect_log):
    """Assemble the run record the dispatch requires. Returns
    {"emitted": True, "record": {...}} or {"emitted": False,
    "missing": [...]} naming every absent field; nothing is emitted with
    a field missing, and a void Arm A has no frame and no delta, so the
    shipped run is refused here by construction."""
    fr = arm_a.get("frame")
    rec = {
        "frame_declaration": ({"source": fr["source_id"],
                               "edition": fr["edition"],
                               "seed": fr["rng_seed"], "n": fr["n"],
                               "frame_id": fr["frame_id"]}
                              if fr else None),
        "delta_open_blind": arm_a["delta_label"],
        "acc_label": {c: arm_a["per_condition"][c]["acc_label"]
                      for c in CONDITIONS},
        "acc_mech_revised": {c: arm_a["per_condition"][c]["acc_mech_revised"]
                             for c in CONDITIONS},
        "n_revised": {c: arm_a["per_condition"][c]["n_revised"]
                      for c in CONDITIONS},
        "arm_c": [{"id": r["id"], "axis_1": r["axis_1"],
                   "axis_2": r["axis_2"], "cell": r["cell"]}
                  for r in arm_c["per_row"]],
        "defect_log": defect_log,
        "key_holder": arm_a["key_holder"],
        "respondent": arm_a["respondent"],
        "key_holder_respondent_differ": arm_a["key_holder_respondent_differ"],
        "return": arm_a["return"],
        "void": arm_a["void"],
    }
    missing = []
    for k in RUN_RECORD_REQUIRED:
        v = rec.get(k)
        if v is None or v == [] or v == {}:
            missing.append(k)
        elif k in ("acc_label", "acc_mech_revised") and \
                any(x is None for x in v.values()):
            missing.append(k + " (a condition is None)")
    if isinstance(defect_log, dict):
        if "spec" not in defect_log or "implementation" not in defect_log:
            missing.append("defect_log columns spec / implementation")
    else:
        missing.append("defect_log (must carry two columns)")
    if missing:
        return {"emitted": False, "missing": missing, "record": None}
    return {"emitted": True, "missing": [], "record": rec}


# --------------------------------------------------------------------------
# render
# --------------------------------------------------------------------------

def _f(v, w=6):
    if v is None:
        return "--".rjust(w)
    if isinstance(v, bool):
        return ("yes" if v else "no").rjust(w)
    if isinstance(v, float):
        return ("%.3f" % v).rjust(w)
    return str(v).rjust(w)


def render(arm_a, arm_b_record, arm_b_status, arm_c, blinds,
           contamination, record):
    out = []
    p = out.append
    p("revision_survival -- WORK ORDER M, revision 2")
    p("=" * 72)
    p("")
    for line in contamination:
        p(line)
    p("")
    p("ARM A  calibration   Y = %d" % arm_a["Y"])
    p("-" * 72)
    fr = arm_a["frame"]
    if fr:
        p("  frame  %s / %s   index %d   seed %d   n %d   id %s"
          % (fr["source_id"], fr["edition"], fr["index_size"],
             fr["rng_seed"], fr["n"], fr["frame_id"][:12]))
    else:
        p("  frame  NONE DECLARED -- Arm A refuses (D-C1 HARD GATE)")
    p("admitted %d   excluded %d   SURVIVED share %s   verified %d of %d"
      % (arm_a["n_admitted"], len(arm_a["excluded"]),
         _f(arm_a["survived_share"], 5), arm_a["verified"],
         arm_a["n_admitted"]))
    p("  N required for n_revised >= %d at this SURVIVED share: %s  (D-C4)"
      % (N_REVISED_MIN, _f(arm_a["n_required"], 1)))
    for cid, why in arm_a["excluded"]:
        p("  excluded  %-14s %s" % (cid, why))
    p("")
    p("  %-30s %8s %8s" % ("", "OPEN", "BLIND"))
    per = arm_a["per_condition"]
    for k, lab in (("n", "n"), ("acc_label", "Q_label"),
                   ("chance_label", "  chance [CHOICE 1]"),
                   ("label_above_chance", "  above chance [CHOICE 2]"),
                   ("acc_mech_revised", "Q_mech, revised rows ONLY"),
                   ("n_revised", "  n revised (floor %d)" % N_REVISED_MIN),
                   ("mech_status", "  status"),
                   ("chance_mech_revised", "  chance [CHOICE 1]"),
                   ("mech_above_chance", "  above chance [CHOICE 2]"),
                   ("none_given", "  NONE_GIVEN"),
                   ("mean_confidence", "mean confidence"),
                   ("overconfidence", "  conf - Q_label [CHOICE 4]"),
                   ("overconfident", "  OVERCONF_GATE")):
        p("  %-30s %8s %8s" % (lab, _f(per["OPEN"][k], 8),
                               _f(per["BLIND"][k], 8)))
    p("")
    p("  delta label %s   delta mech(revised) %s   gate %s   LEAK_GATE %s"
      % (_f(arm_a["delta_label"]), _f(arm_a["delta_mech_revised"]),
         _f(arm_a["delta"]), _f(arm_a["leak_gate_passed"])))
    p("  return      %s   score %s   co-flags %s   [CHOICE 3] [CHOICE 7]"
      % (arm_a["return"], arm_a["score"] or "NONE",
         arm_a["co_flags"] or "none"))
    p("  key_holder  %s" % "; ".join(arm_a["key_holder"]))
    p("  respondent  %s" % "; ".join(arm_a["respondent"]))
    p("  differ      %s" % ("yes" if arm_a["key_holder_respondent_differ"]
                            else "NO"))
    for v in arm_a["void"]:
        p("  " + v)
    for d in arm_a["defects"]:
        p("  " + d)
    p("")
    p("  BLIND texts (MECHANICAL_ONLY; paraphrase is the operator's step):")
    if not blinds:
        p("  none: no admitted rows")
    for b in blinds:
        p("  %-14s nouns %d  years %d  %s"
          % (b["claim_id"], sum(n for _, _, n in b["nouns_moved"]),
             b["years_removed"], b["text"][:60]))
    p("")
    p("ARM B  forward commit")
    p("-" * 72)
    p("  domain   %s" % arm_b_record["domain"])
    p("  date     %s   k %d" % (arm_b_record["date"], arm_b_record["k"]))
    p("  sha256   %s" % arm_b_record["sha256"])
    p("  review   %s   %s   [CHOICE 6]" % tuple(arm_b_record["review"]))
    p("  status   %s%s" % (arm_b_status["status"],
                          ("   due " + arm_b_status["due"])
                          if arm_b_status.get("due") else ""))
    p("")
    p("ARM C  two axes, not one scale   cut %.1f [CHOICE 8]" % arm_c["cut"])
    p("-" * 72)
    p("  %-5s %-24s %-12s %-8s %-22s %-22s %6s"
      % ("row", "cycle", "axis_1", "axis_2", "cell", "state", "min p"))
    for r in arm_c["per_row"]:
        p("  %-5s %-24s %-12s %-8s %-22s %-22s %6s%s"
          % (r["id"], r["cycle"][:24], r["axis_1"], r["axis_2"],
             r["cell"], r["state"], _f(r["min_p_survive"]),
             ("  low: " + ",".join(r["low"])) if r["low"] else ""))
    p("")
    p("  FINDING  TERMINAL cells resting on a claim rated < %.1f: %d  %s"
      % (arm_c["cut"], arm_c["finding"], arm_c["terminal_low"] or ""))
    p("  NO_SUBSTITUTION_EXISTS (n/a, none): %d  %s  -- reported beside "
      "TERMINAL, not ranked against it (D-C2)"
      % (len(arm_c["no_substitution_exists"]),
         arm_c["no_substitution_exists"] or ""))
    p("  kept apart, not summed in:")
    p("    TERMINAL, no rated claim under it   %d  %s"
      % (len(arm_c["terminal_unrated"]), arm_c["terminal_unrated"] or ""))
    p("    TERMINAL, all claims rated >= cut   %d  %s"
      % (len(arm_c["terminal_held"]), arm_c["terminal_held"] or ""))
    p("    axis_1 UNDECLARED                   %d  %s"
      % (len(arm_c["undeclared"]), arm_c["undeclared"] or ""))
    p("    pathway, no decision on record      %d  %s"
      % (len(arm_c["not_on_record"]), arm_c["not_on_record"] or ""))
    p("    rated claims under no row           %d  %s"
      % (len(arm_c["claims_under_no_row"]), arm_c["claims_under_no_row"] or ""))
    p("")
    p("RUN RECORD")
    p("-" * 72)
    if record["emitted"]:
        p("  EMITTED   frame %s" % record["record"]["frame_declaration"]["frame_id"][:12])
    else:
        p("  REFUSED   missing: %s" % ", ".join(record["missing"]))
    p("")
    p("choices in force:")
    for k in sorted(CHOICES):
        p("  [CHOICE %d] %s" % (k, CHOICES[k]))
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------
# main
# --------------------------------------------------------------------------

def run(today=None):
    sys.path.insert(0, HERE)
    import cases  # noqa: E402
    claims = [read_claim(c) for c in cases.CLAIMS]
    responses = [read_response(r) for r in cases.RESPONSES_OPEN]
    # no frame is shipped: no Y-vintage index is reachable and recall is
    # forbidden (D-C1). Arm A refuses on it, which is the result.
    arm_a = score_arm_a(claims, responses, frame=cases.FRAME)
    admitted, _ = admit(claims, arm_a["frame"])
    blinds = [blind(c) for c in admitted]
    block = read_block(cases.ARM_B_BLOCK)
    record = publish_record(block)
    if verify(block, cases.ARM_B_RECORD) is False:
        raise RefusedInput("ARM_B_RECORD does not verify against the block")
    today = today or _dt.date.today().isoformat()
    arm_b_status = score_arm_b(block, record, {}, today)
    arm_c = score_arm_c(cases.BRC_ROWS, block)
    rec = run_record(arm_a, arm_c, cases.DEFECT_LOG)
    return render(arm_a, record, arm_b_status, arm_c, blinds,
                  cases.CONTAMINATION, rec)


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("revision_survival.py carries no selftest; run "
                         "python3 test_revision.py\n")
        return 2
    if "--choices" in argv:
        for k in sorted(CHOICES):
            print("[CHOICE %d] %s" % (k, CHOICES[k]))
        return 0
    today = None
    for a in argv:
        if a.startswith("--today="):
            today = a.split("=", 1)[1]
    sys.stdout.write(run(today))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
