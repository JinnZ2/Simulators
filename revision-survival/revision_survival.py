#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0
"""
revision_survival -- WORK ORDER M, built to it.

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
  ARM C  consequence class: for each BRC row, RECOVERABLE / COSTLY /
         TERMINAL, and the count of TERMINAL cells resting on a claim the
         model itself rates below 0.8 survival. That count is the finding.

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
             UNCALIBRATED partition the rest; OVERCONFIDENT rides beside.

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

RETURNS = ("CALIBRATED", "LEAK_DOMINATED", "LABEL_ONLY", "UNCALIBRATED",
           "OVERCONFIDENT")

CONSEQUENCE = ("RECOVERABLE", "COSTLY", "TERMINAL")
# fourth state, ours: a row on which no substitution decision exists, which
# is not the same as a decision nobody classified.
NOT_ON_RECORD = "NOT_ON_RECORD"
UNDECLARED = "UNDECLARED"

ESTABLISHED = ("YES", "NO", "UNCERTAIN")

Y = 2005
N_FLOOR = 40           # the order: N >= 40
SURVIVED_FLOOR = 0.40  # D1: target >= 40% SURVIVED
LEAK_THRESHOLD = 0.15
OVERCONF_THRESHOLD = 0.20
SURVIVAL_CUT = 0.8     # Arm C: TERMINAL cells resting on claims rated < 0.8
MARGIN = 2.0           # [CHOICE 2]

CHOICES = {
    1: "chance = max(1/|vocab|, majority share of the key)",
    2: "above chance = acc > chance + %.1f * binomial sd at n" % MARGIN,
    3: "delta computed for both quantities; LEAK gates on the larger",
    4: "OVERCONFIDENT reads mean confidence against Q_label",
    5: "Arm B block carries an explicit p_survive; nothing derives it",
    6: "review dates T+24mo / T+60mo by calendar year on the commit day",
    7: "return = primary (LEAK preempts; CAL/LABEL/UNCAL partition) + co-flag",
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
    if rec["status"] not in ("DELIVERED", "CANDIDATE", "CONSTRUCTED"):
        raise RefusedInput("claim %s: status %r" % (rec["id"], rec["status"]))
    return dict(rec)


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


def admit(claims):
    """Corpus admission. DELIVERED and established YES only. Everything
    else is counted, by reason, never dropped silently."""
    admitted, excluded = [], []
    for c in claims:
        if c["status"] != "DELIVERED":
            excluded.append((c["id"], "status=%s" % c["status"]))
        elif c["established_as_of_Y"] != "YES":
            excluded.append((c["id"], "established_as_of_%d=%s"
                             % (Y, c["established_as_of_Y"])))
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


def score_arm_a(claims, responses):
    """Returns a dict. Nothing in it is a single number standing for the
    result. `void` carries the reason a result is not one."""
    admitted, excluded = admit(claims)
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
        # Q_mech over REVISED rows only. On a SURVIVED row the key mechanism
        # is NONE_GIVEN, so mechanism accuracy there is a function of label
        # accuracy; the load-bearing quantity lives on the revised subset.
        mech_rev = [(g, e) for (g, e), (_, lab_e) in zip(mech, lab)
                    if lab_e != "SURVIVED"]
        ch_l, u_l, m_l = chance(len(VERDICTS),
                                [e for _, e in lab])
        ch_m, u_m, m_m = chance(len(MECHANISMS),
                                [e for _, e in mech])
        acc_l = accuracy(lab)
        acc_m = accuracy(mech)
        conf = ([r["confidence"] for r in rows])
        mean_conf = (sum(conf) / len(conf)) if conf else None
        per[cond] = {
            "n": len(rows),
            "acc_label": acc_l, "acc_mech": acc_m,
            "acc_mech_revised": accuracy(mech_rev),
            "n_revised": len(mech_rev),
            "chance_label": ch_l, "chance_mech": ch_m,
            "chance_label_parts": (u_l, m_l),
            "chance_mech_parts": (u_m, m_m),
            "label_above_chance": above_chance(acc_l, ch_l, len(rows)),
            "mech_above_chance": above_chance(acc_m, ch_m, len(rows)),
            "mean_confidence": mean_conf,
            "overconfidence": (mean_conf - acc_l)
            if (mean_conf is not None and acc_l is not None) else None,
            "none_given": none_given,
        }

    d_label = delta(per["OPEN"]["acc_label"], per["BLIND"]["acc_label"])
    d_mech = delta(per["OPEN"]["acc_mech"], per["BLIND"]["acc_mech"])
    d_gate = None
    if d_label is not None and d_mech is not None:
        d_gate = max(d_label, d_mech)              # [CHOICE 3]

    # contamination: the key and the responses written by one author
    authors_key = set(c["author"] for c in admitted)
    authors_resp = set(r["author"] for r in responses)
    same_author = bool(authors_key & authors_resp)

    void = []
    if d_gate is None:
        void.append("VOID_NO_DELTA: one condition absent; the order says a "
                    "result without delta is void")
    if same_author:
        void.append("VOID_SAME_AUTHOR: key and responses share an author; "
                    "agreement is by construction (TP_003)")

    defects = []
    if n_adm < N_FLOOR:
        defects.append("BELOW_N_FLOOR: %d admitted against %d"
                       % (n_adm, N_FLOOR))
    if survived_share is None:
        defects.append("D1: no admitted claims; SURVIVED share undefined")
    elif survived_share < SURVIVED_FLOOR:
        defects.append("D1: SURVIVED share %.2f below %.2f; base rate "
                       "manufactured" % (survived_share, SURVIVED_FLOOR))
    if verified < n_adm:
        defects.append("D4: %d of %d admitted outcomes unverified (carried)"
                       % (n_adm - verified, n_adm))

    primary, co = _return(per, d_gate, void)
    return {
        "arm": "A", "Y": Y,
        "n_admitted": n_adm, "excluded": excluded,
        "survived_share": survived_share, "verified": verified,
        "per_condition": per,
        "delta_label": d_label, "delta_mech": d_mech, "delta": d_gate,
        "void": void, "defects": defects,
        "same_author": same_author,
        "return": primary, "co_flags": co,
        "choices": [1, 2, 3, 4, 7],
    }


def _return(per, d_gate, void):
    """[CHOICE 7]. A void result returns its void reason, not a member."""
    if void:
        if d_gate is not None and d_gate >= LEAK_THRESHOLD:
            return "LEAK_DOMINATED", []
        return "VOID", []
    if d_gate >= LEAK_THRESHOLD:
        return "LEAK_DOMINATED", []
    # primary is read on the BLIND condition, the one the delta licenses
    b = per["BLIND"]
    mech_up = b["mech_above_chance"]
    lab_up = b["label_above_chance"]
    # neither can be None here: a condition with no rows voids above, and
    # above_chance is None only on no rows.
    if mech_up:
        primary = "CALIBRATED"
    elif lab_up:
        primary = "LABEL_ONLY"
    else:
        primary = "UNCALIBRATED"
    co = []
    for cond in CONDITIONS:
        oc = per[cond]["overconfidence"]
        if oc is not None and oc > OVERCONF_THRESHOLD:
            co.append("OVERCONFIDENT(%s)" % cond)
    return primary, co


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
    lab, mech = [], []
    unresolved = []
    for c in block["claims"]:
        o = outcomes.get(c["id"])
        if o is None:
            unresolved.append(c["id"])
            continue
        lab.append((c["verdict"], o["label"]))
        mech.append((c["mechanism"], o["mechanism"]))
    return {"arm": "B", "status": "SCORED", "n": len(lab),
            "unresolved": unresolved,
            "acc_label": accuracy(lab), "acc_mech": accuracy(mech),
            "scored": True}


# --------------------------------------------------------------------------
# Arm C
# --------------------------------------------------------------------------

def read_brc_row(row):
    """A BRC row. `consequence_class` is one of the order's three, or
    NOT_ON_RECORD (no substitution decision exists for this row), or
    UNDECLARED. A class without a basis is refused: the class is a reading
    and a reading with no stated ground is a default."""
    for k in ("id", "cycle", "pathway", "stock_or_flow", "consequence_class",
              "basis", "rests_on"):
        if k not in row:
            raise RefusedInput("BRC row %s: missing %s" % (row.get("id"), k))
    cc = row["consequence_class"]
    if cc not in CONSEQUENCE + (NOT_ON_RECORD, UNDECLARED):
        raise RefusedInput("BRC row %s: consequence_class %r" % (row["id"], cc))
    if cc != UNDECLARED and _absent(row["basis"]):
        raise RefusedInput("BRC row %s: class %s with no basis" % (row["id"], cc))
    if row["pathway"] not in ("MEASURED", "PARTIAL", "NONE"):
        raise RefusedInput("BRC row %s: pathway %r" % (row["id"], row["pathway"]))
    if row["stock_or_flow"] not in ("STOCK", "FLOW"):
        raise RefusedInput("BRC row %s: stock_or_flow" % row["id"])
    return row


def score_arm_c(rows, block):
    """The finding: TERMINAL cells resting on a claim rated < SURVIVAL_CUT.
    Kept apart from it, never summed in: TERMINAL cells resting on NO rated
    claim (a cell nobody has rated is not a cell rated safe), rows whose
    class is UNDECLARED, and rows with no substitution decision on record.
    A rests_on id absent from the block is refused, not skipped."""
    ratings = {c["id"]: c["p_survive"] for c in block["claims"]}
    rows = [read_brc_row(r) for r in rows]
    terminal_low, terminal_unrated, terminal_held = [], [], []
    undeclared, not_on_record = [], []
    per_row = []
    for r in rows:
        for cid in r["rests_on"]:
            if cid not in ratings:
                raise RefusedInput("BRC row %s rests on %s, not in the block"
                                   % (r["id"], cid))
        ps = [ratings[cid] for cid in r["rests_on"]]
        low = [cid for cid in r["rests_on"] if ratings[cid] < SURVIVAL_CUT]
        cc = r["consequence_class"]
        state = None
        if cc == UNDECLARED:
            undeclared.append(r["id"]); state = "UNDECLARED"
        elif cc == NOT_ON_RECORD:
            not_on_record.append(r["id"]); state = "NOT_ON_RECORD"
        elif cc == "TERMINAL":
            if not ps:
                terminal_unrated.append(r["id"]); state = "TERMINAL_UNRATED"
            elif low:
                terminal_low.append(r["id"]); state = "TERMINAL_LOW_SURVIVAL"
            else:
                terminal_held.append(r["id"]); state = "TERMINAL_RATED_HELD"
        else:
            state = cc
        per_row.append({"id": r["id"], "cycle": r["cycle"],
                        "pathway": r["pathway"], "class": cc,
                        "state": state, "rests_on": list(r["rests_on"]),
                        "min_p_survive": (min(ps) if ps else None),
                        "low": low})
    # claims in the block that no row rests on: rated, under nothing
    used = set(cid for r in rows for cid in r["rests_on"])
    unused = [cid for cid in ratings if cid not in used]
    return {"arm": "C", "cut": SURVIVAL_CUT,
            "finding": len(terminal_low),
            "terminal_low": terminal_low,
            "terminal_unrated": terminal_unrated,
            "terminal_held": terminal_held,
            "undeclared": undeclared, "not_on_record": not_on_record,
            "claims_under_no_row": unused,
            "per_row": per_row, "n_rows": len(rows)}


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
           contamination):
    out = []
    p = out.append
    p("revision_survival -- WORK ORDER M")
    p("=" * 72)
    p("")
    for line in contamination:
        p(line)
    p("")
    p("ARM A  calibration   Y = %d" % arm_a["Y"])
    p("-" * 72)
    p("admitted %d   excluded %d   SURVIVED share %s   verified %d of %d"
      % (arm_a["n_admitted"], len(arm_a["excluded"]),
         _f(arm_a["survived_share"], 5), arm_a["verified"],
         arm_a["n_admitted"]))
    for cid, why in arm_a["excluded"]:
        p("  excluded  %-14s %s" % (cid, why))
    p("")
    p("  %-22s %8s %8s" % ("", "OPEN", "BLIND"))
    per = arm_a["per_condition"]
    for k, lab in (("n", "n"), ("acc_label", "Q_label"),
                   ("chance_label", "  chance [CHOICE 1]"),
                   ("label_above_chance", "  above chance [CHOICE 2]"),
                   ("acc_mech", "Q_mech"),
                   ("acc_mech_revised", "  Q_mech, revised rows only"),
                   ("n_revised", "  n revised"),
                   ("chance_mech", "  chance [CHOICE 1]"),
                   ("mech_above_chance", "  above chance [CHOICE 2]"),
                   ("none_given", "  NONE_GIVEN"),
                   ("mean_confidence", "mean confidence"),
                   ("overconfidence", "  conf - Q_label [CHOICE 4]")):
        p("  %-28s %8s %8s" % (lab, _f(per["OPEN"][k], 8),
                               _f(per["BLIND"][k], 8)))
    p("")
    p("  delta label %s   delta mech %s   gate (larger) %s   [CHOICE 3]"
      % (_f(arm_a["delta_label"]), _f(arm_a["delta_mech"]),
         _f(arm_a["delta"])))
    p("  return      %s   co-flags %s   [CHOICE 7]"
      % (arm_a["return"], arm_a["co_flags"] or "none"))
    for v in arm_a["void"]:
        p("  " + v)
    for d in arm_a["defects"]:
        p("  " + d)
    p("")
    p("  BLIND texts (MECHANICAL_ONLY; paraphrase is the operator's step):")
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
    p("ARM C  consequence class   cut %.1f" % arm_c["cut"])
    p("-" * 72)
    p("  %-5s %-26s %-8s %-13s %-22s %6s" % ("row", "cycle", "pathway",
                                            "class", "state", "min p"))
    for r in arm_c["per_row"]:
        p("  %-5s %-26s %-8s %-13s %-22s %6s%s"
          % (r["id"], r["cycle"][:26], r["pathway"], r["class"],
             r["state"], _f(r["min_p_survive"]),
             ("  low: " + ",".join(r["low"])) if r["low"] else ""))
    p("")
    p("  FINDING  TERMINAL cells resting on a claim rated < %.1f: %d  %s"
      % (arm_c["cut"], arm_c["finding"], arm_c["terminal_low"] or ""))
    p("  kept apart, not summed in:")
    p("    TERMINAL, no rated claim under it   %d  %s"
      % (len(arm_c["terminal_unrated"]), arm_c["terminal_unrated"] or ""))
    p("    TERMINAL, all claims rated >= cut   %d  %s"
      % (len(arm_c["terminal_held"]), arm_c["terminal_held"] or ""))
    p("    class UNDECLARED                    %d  %s"
      % (len(arm_c["undeclared"]), arm_c["undeclared"] or ""))
    p("    no substitution decision on record  %d  %s"
      % (len(arm_c["not_on_record"]), arm_c["not_on_record"] or ""))
    p("    rated claims under no row           %d  %s"
      % (len(arm_c["claims_under_no_row"]), arm_c["claims_under_no_row"] or ""))
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
    arm_a = score_arm_a(claims, responses)
    admitted, _ = admit(claims)
    blinds = [blind(c) for c in admitted]
    block = read_block(cases.ARM_B_BLOCK)
    record = publish_record(block)
    if verify(block, cases.ARM_B_RECORD) is False:
        raise RefusedInput("ARM_B_RECORD does not verify against the block")
    today = today or _dt.date.today().isoformat()
    arm_b_status = score_arm_b(block, record, {}, today)
    arm_c = score_arm_c(cases.BRC_ROWS, block)
    return render(arm_a, record, arm_b_status, arm_c, blinds,
                  cases.CONTAMINATION)


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
