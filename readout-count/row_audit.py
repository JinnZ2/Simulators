#!/usr/bin/env python3
"""row_audit -- the delivered trucking row (v0.1) against the instrument.

`TRUCKING_ROW_v0_1.md` is the first filled row in this folder: sourced,
with a coding rule stated, a correction to its own v0 logged, and a
count of 0.5. This module reads the delivered text and checks, against
the schema `readout_count.py` implements:

  1. the coding rule the row states against the fields the schema
     carries -- which of its three conjuncts has a column;
  2. what the 0.5 is: a per-position partial return weighted at one
     half, which the parent schema (a LIST of returning positions) has
     no way to hold, and the strict reading of the same rule;
  3. the row loaded into the instrument as delivered -- what the
     validator refuses, cell by cell;
  4. the SOURCES block: entries with a URL against entries deferred by
     the document's own "cite before use", and which count rests on a
     deferred one;
  5. the cross-reference "(N4)" against the parent order;
  6. the parent order's seed cells for trucking against v0.1's
     renaming of them.

Every host in the SOURCES block was probed once and refused CONNECT
(allowlist egress); the probe result is recorded, not the sources'
content. Nothing here is a statement about any regime.

CC0. stdlib only. Parses under Python 3.9.
"""

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import readout_count as RC  # noqa: E402

DOC = os.path.join(HERE, "TRUCKING_ROW_v0_1.md")
ORDER = os.path.join(HERE, "WORK_ORDER.md")


def _read(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def section(text, heading):
    m = re.search(r"^## %s.*?\n(.*?)(?=^## |\Z)" % re.escape(heading), text, re.S | re.M)
    return m.group(1) if m else None


# ---------------------------------------------------- 1. the coding rule

# The rule as delivered names three conjuncts. Which has a schema field
# is a declared reading, checked against RC.FIELDS below.
RULE_CONJUNCTS = {
    "NON-ADVERSARIAL": {"field": None,
                        "why": "no field; the nearest is the row's own `type` "
                               "column (complaint | readout | inspection | "
                               "enforcement | remedy), which the schema lacks"},
    "HELD": {"field": "holder",
             "why": "holder is builder | regulator | third_party; 'held' in the "
                    "row's sense (a third party holds the report) is holder == "
                    "third_party"},
    "RETURNING": {"field": "positions_returning",
                  "why": "a list, so a position returns or does not; 'partial' "
                         "has no state"},
}


def rule_coverage():
    out = {}
    for k, v in RULE_CONJUNCTS.items():
        out[k] = dict(v, field_exists=(v["field"] in RC.FIELDS) if v["field"] else False)
    return out


def rule_stated(text):
    s = section(text, "COUNT, WITH THE CODING RULE STATED")
    return bool(s) and "NON-ADVERSARIAL, HELD, RETURNING" in s


# -------------------------------------------------------- 2. the 0.5

# The OTHER LAYERS table, as declared readings of its `type` and
# `returns to operator?` columns; `return` is the state the parent
# schema lacks (y | partial | n).
LAYERS = {
    "carrier HR": {"type": "complaint", "return": "n"},
    "weigh station": {"type": "inspection", "return": "n"},
    "officer": {"type": "enforcement", "return": "n"},
    "NHTSA VOQ / SaferTruck": {"type": "readout", "return": "partial"},
    "FMCSA NCCDB": {"type": "complaint", "return": "n"},
    "OSHA STAA": {"type": "remedy", "return": "n"},
}
PARTIAL_WEIGHT = 0.5   # [CHOICE] the weight the delivered 0.5 implies


def readout_count_from_layers(layers=LAYERS, partial=PARTIAL_WEIGHT):
    """Under the row's own rule: readout-typed layers only, return
    weighted y = 1, partial = `partial`, n = 0. Returns the strict count
    (partial = 0) and the half count beside it."""
    ro = {k: v for k, v in layers.items() if v["type"] == "readout"}
    w = {"y": 1.0, "partial": partial, "n": 0.0}
    half = sum(w[v["return"]] for v in ro.values())
    strict = sum(1.0 for v in ro.values() if v["return"] == "y")
    comp = sum(1 for v in layers.values() if v["type"] == "complaint")
    return {"readout_layers": sorted(ro), "half": half, "strict": strict,
            "complaint_layers": comp}


def stated_counts(text):
    s = section(text, "COUNT, WITH THE CODING RULE STATED") or ""
    out = {}
    for m in re.finditer(r"^\s+(air|rail|trucking)\s+([\d.\-]+)", s, re.M):
        out[m.group(1)] = m.group(2)
    m = re.search(r"complaint_count for trucking is >= (\d+)", s)
    out["complaint_count_trucking_min"] = int(m.group(1)) if m else None
    return out


# ------------------------------------------ 3. the row through the schema

def trucking_row_as_delivered():
    """The v0.1 row transcribed into the parent schema's columns with
    the values the document gives, and the document's own words where
    it gives none. Every cell is what v0.1 states or UNMEASURED; nothing
    is supplied from outside the document."""
    return {
        "regime": "trucking", "year": "2026",
        "positions_declared": "driver (NCCDB coercion);driver (NCCDB harassment);driver (OSHA STAA);driver (NHTSA VOQ equipment)",
        "positions_returning": "driver (NHTSA VOQ equipment)",   # partial, per v0.1
        "holder": "regulator",                                    # NHTSA / FMCSA
        "immunity": "n",                                          # "no immunity"
        "investigator_independent": "n",
        "intake_count": "UNMEASURED",                             # STILL NEEDED
        "return_count": "UNMEASURED",                             # STILL NEEDED
        "external_detection": "n",
        "rate_metric": "fatal crashes per VMT (series STILL NEEDED)",
        "rate_trend": "UNMEASURED",                               # STILL NEEDED
        "source_url": "https://www.ecfr.gov/current/title-49/subtitle-B/chapter-III/subchapter-B/part-386/subpart-B/section-386.12",
    }


def load_attempt(row):
    """What the instrument does with the row as delivered."""
    try:
        RC.validate_rows([row])
        return {"loaded": True, "refused_on": None}
    except RC.SchemaRefused as e:
        return {"loaded": False, "refused_on": str(e)}


def load_attempt_with_trend(row, trend):
    r = dict(row, rate_trend=trend)
    a = load_attempt(r)
    if a["loaded"]:
        d = RC.derive(RC.validate_rows([r])[0])
        a["readout_count"] = d["readout_count"]
        a["declared_count"] = d["declared_count"]
        a["return_rate"] = d["return_rate"]
    return a


# -------------------------------------------------------- 4. the sources

def sources(text):
    s = section(text, "SOURCES") or ""
    entries = []
    cur = None
    for line in s.splitlines():
        if not line.strip():
            continue
        if line.startswith("      "):        # continuation
            if cur is not None:
                cur["text"] += " " + line.strip()
            continue
        cur = {"text": line.strip()}
        entries.append(cur)
    for e in entries:
        m = re.search(r"https?://\S+", e["text"])
        e["url"] = m.group(0) if m else None
        e["deferred"] = e["url"] is None and ("before use" in e["text"] or "to be located" in e["text"])
    return entries


def count_rests_on_deferred(text):
    """The trucking count names NHTSA VOQ; the NHTSA source entry is
    deferred."""
    s = section(text, "COUNT, WITH THE CODING RULE STATED") or ""
    names_voq = "NHTSA VOQ" in s
    src = sources(text)
    voq_deferred = any("NHTSA" in e["text"] and e["deferred"] for e in src)
    return {"count_names_voq": names_voq, "voq_source_deferred": voq_deferred}


HOST_PROBE = {   # one CONNECT each, 2026-09-02; recorded, not asserted
    "www.ecfr.gov": "no response",
    "www.fmcsa.dot.gov": "no response",
    "www.federalregister.gov": "no response",
    "nccdb.fmcsa.dot.gov": "no response",
}


# ------------------------------------------------ 5. the (N4) reference

def n4_reference(text, order_text):
    return {"row_cites_N4": "(N4)" in text,
            "order_has_N4": bool(re.search(r"\bN4\b", order_text)),
            "order_procedure_ids": sorted(set(re.findall(r"^\s{4}(P\d)\s", order_text, re.M))),
            "order_hypothesis_ids": sorted(set(re.findall(r"^\s{4}(H\d)\s", order_text, re.M)))}


# ------------------------------------------------ 6. seed cells vs v0.1

def seed_vs_row(order_text, text):
    seed = [s for s in RC.seed_rows(order_text) if s["regime"] == "trucking"]
    st = stated_counts(text)
    if not seed:
        return None
    s = seed[0]
    return {
        "seed_positions": s["positions"], "seed_intake": s["intake"], "seed_return": s["return"],
        "seed_rate_trend": s["rate_trend"],
        "v01_count": st.get("trucking"), "v01_complaint_min": st.get("complaint_count_trucking_min"),
        "intake_cell_is_complaint_count": s["intake"].rstrip("+").isdigit()
        and st.get("complaint_count_trucking_min") == int(s["intake"].rstrip("+")),
        "rate_trend_now": "STILL NEEDED (the per-VMT crash series)",
    }


# ---------------------------------------------------------------- render

def render():
    text, order = _read(DOC), _read(ORDER)
    out = []
    w = out.append
    w("row_audit -- TRUCKING_ROW_v0_1 against the instrument")
    w("")
    w("1. THE CODING RULE  stated as NON-ADVERSARIAL, HELD, RETURNING: %s" % rule_stated(text))
    for k, v in rule_coverage().items():
        w("   %-16s field %-20s exists %-5s %s" % (k, v["field"] or "--", v["field_exists"], v["why"]))
    w("")
    rc = readout_count_from_layers()
    st = stated_counts(text)
    w("2. THE 0.5  readout-typed layers %s; under the rule with partial return at %.1f: %.1f;"
      % (rc["readout_layers"], PARTIAL_WEIGHT, rc["half"]))
    w("   strict (partial = 0): %.1f;  stated in the row: %s;  complaint-typed layers: %d, stated >= %s"
      % (rc["strict"], st.get("trucking"), rc["complaint_layers"], st.get("complaint_count_trucking_min")))
    w("   the OTHER LAYERS table types two rows complaint (NCCDB is one row there) and one")
    w("   remedy; the count of >= 3 reaches three only by counting NCCDB's two routes apart")
    w("   or by counting the remedy-typed row -- the table and the count use different units.")
    w("   the parent schema holds positions_returning as a list: a position returns or")
    w("   does not, and the 0.5 is a per-position return state (partial) the list cannot carry.")
    w("   air %s, rail %s: ranges again where the schema wants a count." % (st.get("air"), st.get("rail")))
    w("")
    row = trucking_row_as_delivered()
    a = load_attempt(row)
    w("3. THE ROW THROUGH THE SCHEMA  loaded: %s" % a["loaded"])
    if not a["loaded"]:
        w("   refused on: %s" % a["refused_on"])
    for trend in ("up", "flat", "down"):
        b = load_attempt_with_trend(row, trend)
        w("   with rate_trend supplied as %-4s -> loaded %s, readout_count %s, declared_count %s, return_rate %s"
          % (trend, b["loaded"], b.get("readout_count"), b.get("declared_count"), b.get("return_rate")))
    w("   the row's trend is STILL NEEDED by its own list; supplying one is not the")
    w("   row's, and every supplied value gives readout_count 1 -- the list has no half.")
    w("")
    src = sources(text)
    with_url = [e for e in src if e["url"]]
    deferred = [e for e in src if e["deferred"]]
    w("4. SOURCES  entries %d, with URL %d, deferred by the document's own words %d"
      % (len(src), len(with_url), len(deferred)))
    for e in deferred:
        w("   deferred: %s" % e["text"][:80])
    crd = count_rests_on_deferred(text)
    w("   the trucking count names NHTSA VOQ: %s; the NHTSA source entry is deferred: %s"
      % (crd["count_names_voq"], crd["voq_source_deferred"]))
    w("   hosts probed once (allowlist egress): " + ", ".join("%s %s" % kv for kv in HOST_PROBE.items()))
    w("")
    n4 = n4_reference(text, order)
    w("5. (N4)  cited by the row: %s; present in the parent order: %s; the order's ids are %s and %s"
      % (n4["row_cites_N4"], n4["order_has_N4"], n4["order_hypothesis_ids"], n4["order_procedure_ids"]))
    w("")
    sv = seed_vs_row(order, text)
    w("6. SEED CELLS  parent seed row: positions %r, intake %r, return %r, trend %r"
      % (sv["seed_positions"], sv["seed_intake"], sv["seed_return"], sv["seed_rate_trend"]))
    w("   v0.1: readout_count %s, complaint_count >= %s; the seed's intake cell is the"
      % (sv["v01_count"], sv["v01_complaint_min"]))
    w("   complaint count under its new name: %s; the trend is now %s"
      % (sv["intake_cell_is_complaint_count"], sv["rate_trend_now"]))
    w("")
    w("Nothing here is a statement about any regime. The row's sources were not read.")
    return "\n".join(out) + "\n"


def main(argv):
    if "--selftest" in argv:
        sys.stderr.write("row_audit.py has no checks of its own; they live in selftest_rc.py.\n")
        return 2
    sys.stdout.write(render())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
