#!/usr/bin/env python3
"""stack_audit -- the delivered EXCLUSION STACK read as a structure.

`EXCLUSION_STACK_trucking.md` enumerates twelve filters between an
operator holding a readout and that readout entering a record, coded by
mechanism, with survival multiplicative and every per-layer rate
unmeasured. This module reads the delivered text and computes:

  1. the layer list against the STRUCTURE block -- twelve headings, in
     order, titles matching;
  2. the arithmetic the document states -- the GAO row sum, the three
     percentages, L10's per-hundred figures, the "five to one", the
     "1-in-5", and what 0.5^11 is;
  3. multiplicative survival with None propagating -- a stack with one
     unmeasured layer has no survival fraction, never 1.0;
  4. the L0 list against the trucking row's six-item readout list, by
     content;
  5. the OPEN QUANTITIES against the row's STILL NEEDED list and the
     parent order -- including whether S4 is the survey the row's
     dangling "(N4)" pointed at;
  6. the schema `readout_count.py` implements against the stack: P2's
     three-way definition of RETURN (a reply, a corrective action, a
     report entering a held record) against L11, where a settlement is
     a corrective action that enters no record;
  7. each layer's mechanism against the register's eight, by import,
     as declared readings with the nearest named where none fits;
  8. the SOURCES block, and the hosts, probed once (allowlist egress).

Nothing here is a statement about any regime; the sources were not read.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "uninstrumented"))
import readout_count as RC  # noqa: E402
import row_audit as RA  # noqa: E402
import uninstrumented as UN  # noqa: E402  (imported, not copied)

DOC = os.path.join(HERE, "EXCLUSION_STACK_trucking.md")


def _read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


# ------------------------------------------------------------- 1. layers

def structure(text):
    s = RA.section(text, "STRUCTURE") or ""
    return [(m.group(1), m.group(2).strip()) for m in re.finditer(r"^\s+(L\d+)\s+(.+?)\s*$", s, re.M)]


def headings(text):
    return [(m.group(1), m.group(2).strip())
            for m in re.finditer(r"^## (L\d+) — (.+?)(?:\s{2,}\(.*)?$", text, re.M)]


def layers_match(text):
    st, hd = structure(text), headings(text)
    pairs = []
    for (a, ta), (b, tb) in zip(st, hd):
        pairs.append({"structure": a, "heading": b, "same_id": a == b,
                      "title_match": ta.lower() == tb.lower()})
    return {"structure_n": len(st), "heading_n": len(hd), "pairs": pairs,
            "all_match": len(st) == len(hd) == 12 and all(p["same_id"] and p["title_match"] for p in pairs)}


def layer_body(text, lid):
    m = re.search(r"^## %s — .*?\n(.*?)(?=^## |^---|\Z)" % lid, text, re.S | re.M)
    return m.group(1) if m else ""


# --------------------------------------------------------- 2. arithmetic

def stated_arithmetic(text):
    l8, l10, l7 = layer_body(text, "L8"), layer_body(text, "L10"), layer_body(text, "L7")
    m = re.search(r"N=(\d+)\):\s*dismissed (\d+) \((\d+)%\) · withdrawn (\d+) \((\d+)%\) · merit (\d+) \((\d+)%\)", l8)
    n, d, dp, w, wp, mr, mp = (int(x) for x in m.groups())
    m2 = re.search(r"(\d+) dismissed · (\d+) withdrawn · (\d+) merit", l10)
    h = tuple(int(x) for x in m2.groups())
    m3 = re.search(r"of the (\d+): ~(\d+) private settlements · ~(\d+) formal order", l10)
    of, sett, order = (int(x) for x in m3.groups())
    return {
        "N": n, "counts": (d, w, mr), "counts_sum_to_N": d + w + mr == n,
        "stated_pct": (dp, wp, mp),
        "computed_pct": (round(100 * d / n, 1), round(100 * w / n, 1), round(100 * mr / n, 1)),
        "stated_pct_sum": dp + wp + mp,
        "per_hundred": h, "per_hundred_sum": sum(h),
        "merit_pct_L8_vs_L10": (mp, h[2]),
        "settlement_share_applied": (of, sett, order, round(0.95 * of, 2)),
        "five_to_one": round(100 / h[2], 2),
        "one_in_five_L7": "1-in-5" in l7,
        "one_in_x_from_merit": round(n / mr, 2),
        "half_to_the_eleventh": 0.5 ** 11,
    }


# ------------------------------------------------------ 3. survival

def survival(rates):
    """Product over layers. rates: {layer: fraction or None}. None on any
    layer gives None -- an unmeasured stack has no survival fraction."""
    p = 1.0
    for v in rates.values():
        if v is None:
            return None
        p *= v
    return p


def unmeasured_stack(text):
    return {lid: None for lid, _ in headings(text)}


# ------------------------------------------- 4. L0 against the row's list

L0_KEYS = (("labor", "mental"), ("compensations", "machine"), ("maintenance", "weather"),
           ("social", "route"), ("road", "variable"), ("traffic", "pedestrian"))


def l0_vs_row(text, row_text):
    l0 = layer_body(text, "L0").lower()
    rw = (RA.section(row_text, "WHAT THE DRIVER READOUT CONTAINS") or "").lower()
    out = []
    for keys in L0_KEYS:
        out.append({"keys": keys, "in_stack": all(k in l0 for k in keys),
                    "in_row": all(k in rw for k in keys)})
    return {"items": out, "both": sum(1 for o in out if o["in_stack"] and o["in_row"]),
            "row_item_count": len(re.findall(r"^\s+\d\s+", RA.section(row_text, "WHAT THE DRIVER READOUT CONTAINS") or "", re.M))}


# --------------------------------------------- 5. open quantities vs siblings

def open_quantities(text):
    s = RA.section(text, "OPEN QUANTITIES") or ""
    out = {}
    for m in re.finditer(r"^\s+(S\d)\s+(.+?)(?=^\s+S\d\s|\Z)", s, re.S | re.M):
        out[m.group(1)] = " ".join(m.group(2).split())
    return out


def s4_is_the_n4_survey(text, row_text):
    oq = open_quantities(text)
    s4 = oq.get("S4", "")
    row_open = RA.section(row_text, "OPEN INSTANCE") or ""
    key = "per-carrier reply rate to driver technical submissions"
    return {"S4": s4, "row_names_survey": key in row_open, "S4_matches": "per-carrier reply rate" in s4
            and "technical submissions" in s4, "row_cites_N4": "(N4)" in row_text}


def s5_vs_still_needed(text, row_text):
    still = RA.section(row_text, "STILL NEEDED FOR THIS ROW") or ""
    s5 = open_quantities(text).get("S5", "")
    return {"S5": s5, "row_still_needed_has_it": "NCCDB coercion complaint counts" in still}


# ----------------------------------------- 6. the schema against the stack

P2_DISJUNCTS = ("a reply", "a corrective action", "a report entering a held record")


def p2_vs_l11(order_text, text):
    p2 = re.search(r"P2\s+positions: count only positions whose channel has a documented RETURN\s*\((.+?)\)", order_text, re.S)
    stated = " ".join(p2.group(1).split()) if p2 else ""
    l11 = layer_body(text, "L11")
    return {
        "P2_text": stated,
        "P2_disjuncts_present": all(d in stated for d in P2_DISJUNCTS),
        "L11_settlement_publishes_nothing": "publishes nothing" in l11,
        "L11_condition_enters_no_dataset": "does not enter any safety dataset" in l11,
        "schema_field_for_which_disjunct": "positions_returning" in RC.FIELDS and not any(
            f in RC.FIELDS for f in ("return_kind", "return_type", "enters_record")),
        "reading": "a private settlement is a corrective action (disjunct 2) and enters no "
                   "held record (fails disjunct 3); the schema's positions_returning cannot "
                   "say which disjunct fired",
    }


# -------------------------------------------- 7. mechanisms, by import

# Declared readings. `fit` is a reading; `nearest` names the register
# mechanism closest where none fits. Checked against UN.MECHANISMS.
MECHANISM_MAP = {
    "L0": ("MODALITY", "fit", "the apparatus is a complaint instrument; the quantity is a condition"),
    "L2": ("PROXY_SUBSTITUTION", "fit", "a named rule breach stands in for the condition as the filable target"),
    "L5": ("AUDIT_ASYMMETRY", "partial", "the burden falls on one side only; the register's sense is a guard, not a burden"),
    "L11": (None, "none", "the successful outcome removes the information from the record -- "
                          "nearest is observer-exclusion's classification-note candidate "
                          "(recorded, filed under a category that is not evidence), not one of the eight"),
}


def mechanism_map():
    out = {}
    for lid, (mech, fit, why) in MECHANISM_MAP.items():
        out[lid] = {"mechanism": mech, "fit": fit, "why": why,
                    "in_register": (mech in UN.MECHANISMS) if mech else False}
    return out


# ---------------------------------------------------------- 8. sources

HOST_PROBE = dict(RA.HOST_PROBE, **{"www.osha.gov": "no response", "www.gao.gov": "no response",
                                     "www.dol.gov": "no response"})


def sources(text):
    s = RA.section(text, "SOURCES") or ""
    urls = re.findall(r"https?://\S+", s)
    entries = [l for l in s.splitlines() if l.strip()]
    return {"entries": len(entries), "urls": len(urls),
            "hosts": sorted({re.sub(r"^https?://([^/]+).*$", r"\1", u) for u in urls})}


# ---------------------------------------------------------------- render

def render():
    text, row_text, order = _read(DOC), _read(RA.DOC), _read(RA.ORDER)
    out = []
    w = out.append
    w("stack_audit -- EXCLUSION_STACK_trucking read as a structure")
    w("")
    lm = layers_match(text)
    w("1. LAYERS  structure %d, headings %d, ids and titles match throughout: %s" % (
        lm["structure_n"], lm["heading_n"], lm["all_match"]))
    w("")
    a = stated_arithmetic(text)
    w("2. ARITHMETIC  GAO row N=%d, counts %s sum to N: %s" % (a["N"], a["counts"], a["counts_sum_to_N"]))
    w("   stated %% %s, computed %s, stated sum %d" % (a["stated_pct"], a["computed_pct"], a["stated_pct_sum"]))
    w("   L10 per hundred %s sum %d; merit reads %d%% in L8 and %d in L10 (21.5 rounded both ways)" % (
        a["per_hundred"], a["per_hundred_sum"], a["merit_pct_L8_vs_L10"][0], a["merit_pct_L8_vs_L10"][1]))
    w("   'of the %d: ~%d settlements, ~%d order' against 0.95 x %d = %s" % (
        a["settlement_share_applied"][0], a["settlement_share_applied"][1],
        a["settlement_share_applied"][2], a["settlement_share_applied"][0], a["settlement_share_applied"][3]))
    w("   'roughly five to one' = 100/%d = %s; L7 '1-in-5' against N/merit = %s" % (
        a["per_hundred"][2], a["five_to_one"], a["one_in_x_from_merit"]))
    w("   'a layer that passes 50%% is not minor if there are eleven': 0.5^11 = %.6f" % a["half_to_the_eleventh"])
    w("")
    st = unmeasured_stack(text)
    w("3. SURVIVAL  layers %d, measured rates 0, product: %s" % (len(st), survival(st)))
    w("   an unmeasured layer gives None for the stack; never 1.0 by default.")
    w("")
    l0 = l0_vs_row(text, row_text)
    w("4. L0 AGAINST THE ROW  row lists %d items; %d of %d matched in both by content" % (
        l0["row_item_count"], l0["both"], len(l0["items"])))
    w("")
    s4 = s4_is_the_n4_survey(text, row_text)
    s5 = s5_vs_still_needed(text, row_text)
    w("5. OPEN QUANTITIES  row cites (N4): %s; row names the survey: %s; S4 matches it: %s" % (
        s4["row_cites_N4"], s4["row_names_survey"], s4["S4_matches"]))
    w("   S5 is on the row's STILL NEEDED list: %s" % s5["row_still_needed_has_it"])
    w("   the survey the row pointed at with a phantom id now has an id, S4, in this document.")
    w("")
    p2 = p2_vs_l11(order, text)
    w("6. P2 AGAINST L11  P2 defines RETURN with three disjuncts present: %s" % p2["P2_disjuncts_present"])
    w("   L11: settlement publishes nothing %s; condition enters no dataset %s" % (
        p2["L11_settlement_publishes_nothing"], p2["L11_condition_enters_no_dataset"]))
    w("   schema has positions_returning and no field for which disjunct fired: %s" % p2["schema_field_for_which_disjunct"])
    w("   %s" % p2["reading"])
    w("")
    w("7. MECHANISMS  register carries %d; declared readings:" % len(UN.MECHANISMS))
    for lid, m in mechanism_map().items():
        w("   %-4s %-20s %-8s in register %-5s %s" % (lid, m["mechanism"] or "--", m["fit"], m["in_register"], m["why"]))
    w("")
    src = sources(text)
    w("8. SOURCES  entries %d, URLs %d, hosts %s" % (src["entries"], src["urls"], src["hosts"]))
    w("   probed once: " + ", ".join("%s %s" % (h, HOST_PROBE.get(h, "not probed")) for h in src["hosts"]))
    w("")
    w("Nothing here is a statement about any regime. The sources were not read.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("stack_audit.py has no checks of its own; they live in selftest_rc.py.\n")
        return 2
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
